from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .serializers import TransactionSerializer
import uuid
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .forms import BankAccountInfo
from .models import Transaction

# Create your views here.


def payment_page_view(request):
    user = request.session.get('user')
    product_name = request.session.get('product_name')
    total_price = request.session.get('total_price_cart')

    form = BankAccountInfo()

    context = {
        'user': user,
        'product_name': product_name,
        'total_price': total_price,
        'form': form,
    }

    return render(request, 'gateway/payment_page.html', context)


def process_payment_view(request):
    if request.method == 'POST':
        form = BankAccountInfo(request.POST)

        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            cvv2 = form.cleaned_data['cvv2']
            password = form.cleaned_data['password']

            user = request.session.get('user')
            total_price = request.session.get('total_price_cart')
            product_name = request.session.get('product_name')

            transaction_id = str(uuid.uuid4())

            transaction = Transaction.objects.create(
                user=user,
                from_market='market A',
                account_number=account_number,
                amount=total_price,
                product_name=product_name,
                transaction_id=transaction_id
            )

            data_to_send = {
                'user': user,
                'total_price': total_price,
                'account_number': account_number,
                'cvv2': cvv2,
                'password': password,
                'transaction_id': transaction_id,
            }

            response = requests.post('http://server/process_payment', json=data_to_send)

            if response.status_code == 200:
                result = response.json().get('result')
                request.session['transaction_result'] = result

                if result == 'success':
                    transaction.status = 'success'
                else:
                    transaction.status = 'failed'

                transaction.save()

                return redirect('show transaction result')
            else:
                return render(request, 'gateway/error.html', {'error': 'خطا در ارتباط با بانک'})

        else:
            form = BankAccountInfo()

        return render(request, 'gateway/payment_page.html', {'form': form})


def show_bank_result_view(request):
    result = request.session.get('transaction_result')
    if result == 'success':
        message = 'تراکنش با موفقیت انجام شد'
    else:
        message = 'تراکنشئ رد شد'

    return render(request, 'gateway/show_result.html', {'message': message})


def return_to_market_view(request):
    user = request.session.get('user')
    transaction_result = request.session.get('transaction_result')

    date_to_send = {
        'user': user,
        'transaction_result': transaction_result,
    }

    response = requests.post('http://server-market/update_transaction/', json=date_to_send)

    if response.status_code == 200:
        return redirect('http://server-market/cart/')
    else:
        return render(request, 'gateway/error.html', {'error': 'خطا در بازگشت به فروشگاه'})





































# Create your views here.
#
#
# class TransactionCreate(APIView):
    # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         print("Received data:", request.data)  # چاپ داده‌های دریافتی
#
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             print("valid")
#             transaction = serializer.save(transaction_id=str(uuid.uuid4()))
#             print(transaction)
#             if self.process_payment(transaction):
#                 print("transaction OK")
#                 transaction.status = 'success'
#                 transaction.save()
#
#                 callback_url = request.data.get('callback_url')
#                 if callback_url:
#                     requests.post(callback_url, json={"transaction_id": transaction.transaction_id, "status": "success"})
#
#                 return Response({'transaction_id': transaction.transaction_id, 'status': 'success'},
#                                 status=status.HTTP_200_OK)          ####
#             else:
#                 transaction.status = 'failed'
#                 transaction.save()
#                 return Response({'transaction_id': transaction.transaction_id, 'status': 'failed'},
#                                 status=status.HTTP_400_BAD_REQUEST)
#         else:
#             print("Errors in serializer:", serializer.errors)  # برای اشکال زدایی
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def process_payment(self, transaction):
    #     try:
    #         account = BankAccount.objects.get(user=transaction.user)
    #         if account.balance >= transaction.amount:
    #             account.balance = account.balance - transaction.amount
    #             account.save()
    #             return True
    #         else:
    #             return False
    #     except BankAccount.DoesNotExist:
    #         return False
