from django.contrib import admin
from .models import BankAccount, Transaction

# Register your models here.


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_number', 'balance', 'account_status']
    list_editable = ['status']
