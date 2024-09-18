from django.contrib import admin
from .models import BankAccount, Transaction

# Register your models here.


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_number', 'balance', 'account_status']
    list_editable = ['account_status']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['from_market', 'amount', 'status', 'reference_id', 'last_market_ok']
    list_editable = ['last_market_ok', 'status']