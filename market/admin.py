from django.contrib import admin
from.models import Market, CartItem

# Register your models here.


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'account_number']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'product_name', 'quantity']
