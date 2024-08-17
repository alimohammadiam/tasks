from django.contrib import admin
from .models import BankAccount, Transaction

# Register your models here.


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_number', 'password', 'balance']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'create_time', 'status']
