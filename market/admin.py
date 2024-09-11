from django.contrib import admin
from.models import Market, CartItem, Transaction

# Register your models here.


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'account_number']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'product_price', 'quantity']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'amount', 'status', 'transaction_id', 'create_time']

