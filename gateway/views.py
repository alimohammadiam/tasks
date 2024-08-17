from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TransactionSerializer
import uuid
from rest_framework.response import Response
from rest_framework import status
from .models import BankAccount
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


class TransactionCreate(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(transaction_id=str(uuid.uuid4()))
            if self.process_payment(transaction):
                transaction.status = 'success'
                transaction.save()

                callback_url = request.data.get('callback_url')
                if callback_url:
                    requests.post(callback_url, json={"transaction_id": transaction.transaction_id, "status": "success"})
                    return Response({'transaction_id': transaction.transaction_id, 'status': 'success'},
                                    status=status.HTTP_200_OK)
            else:
                transaction.status = 'failed'
                transaction.save()
                return Response({'transaction_id': transaction.transaction_id, 'status': 'failed'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Errors in serializer:", serializer.errors)  # برای اشکال زدایی
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_payment(self, transaction):
        try:
            account = BankAccount.objects.get(user=transaction.user)
            if account.balance >= transaction.amount:
                account.balance = account.balance - transaction.amount
                account.save()
                return True
            return False
        except BankAccount.DoesNotExist:
            return False
