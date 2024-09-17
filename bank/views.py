from django.shortcuts import render, get_object_or_404
from .models import BankAccount, Transaction
from django.http import JsonResponse
import random
from .tasks import check_last_ok


# Create your views here.


def bank_transaction_view(request):
    if request.method == 'POST':
        data = request.json()
        account_number = data.get('account_number')
        password = data.get('password')
        cvv2 = data.get('cvv2')
        amount = data.get('total_price')
        transaction_id = data.get('transaction_id')

        account = get_object_or_404(BankAccount, account_number=account_number)

        if account.password != password or account.cvv2 != cvv2:
            return JsonResponse({'status': 'failed', 'message': 'رمز اشتباه !'}, status=400)

        if account.balance < amount:
            return JsonResponse({'status': 'failed', 'message': 'موجودی ناکافی !'}, status=400)

        account.balance -= amount
        account.save()

        reference_id = random.randint(100000000, 999999999)

        transaction = Transaction.objects.create(
            account_number=account_number,
            amount=amount,
            transaction_id=transaction_id,
            reference_id=reference_id,
            status='success'

        )

        check_last_ok.apply_async((transaction.transaction_id,), countdown=300)  # 300 ثانیه = 5 دقیقه

        return JsonResponse({
            'status': 'success',
            'reference_id': reference_id,
            'message': 'تراکنش موفق',

        }, status=200)

    return JsonResponse({'status': 'failed', 'message': 'خطا درخواست !'}, status=400)


