from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TransactionSerializer
import uuid
from rest_framework.response import Response
from rest_framework import status
from .models import BankAccount

# Create your views here.


class TransactionCreate(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save(tranacyion_id=str(uuid.uuid4()))
            if self.process_payment(transaction):
                transaction.status = 'success'
                transaction.save()
                return Response({'transaction_id': transaction.transaction_id, 'status': 'success'},
                                status=status.HTTP_200_OK)
            else:
                transaction.status = 'failed'
                transaction.save()
                return Response({'transaction_id': transaction.transaction_id, 'status': 'failed'},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_payment(self, transaction):
        try:
            account = BankAccount.objects.get(user=transaction.user)
            if int(account.balance) >= int(transaction.amount):
                account.balance = str(int(account.balance) - int(transaction.amount))
                account.save()
                return True
            return False
        except BankAccount.DoesNotExist:
            return False
