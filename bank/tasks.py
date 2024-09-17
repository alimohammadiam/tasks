from celery import shared_task
from django.utils import timezone
from .models import BankAccount, Transaction
import requests


@shared_task
def check_last_ok(transaction_id):
    try:
        transaction = Transaction.objects.get(transaction_id=transaction_id)

        if not transaction.last_market_ok:
            account = BankAccount.objects.get(account_number=transaction.account_number)
            account.balance += transaction.amount
            account.save()

            transaction.status = 'not-confirmed'
            transaction.save()

            psp_response = requests.post('http://psp-server/transaction-status/', json={
                'transaction_id': transaction.transaction_id,
                'reference_id': transaction.reference_id,
                'status': 'not-confirmed',
                'message': 'The transaction was not verified and the amount has been refunded.',

            })

            if psp_response.status_code == 200:
                print(f"Transaction {transaction.transaction_id} status sent to PSP successfully.")
            else:
                print(f"Failed to notify PSP about the transaction {transaction.transaction_id} status.")
        else:
            print(f"Transaction {transaction.transaction_id} is already verified or refunded.")

    except Transaction.DoesNotExist:
        print(f'Transaction {transaction_id} not found.')



















