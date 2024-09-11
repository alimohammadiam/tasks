from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Market(models.Model):
    name = models.CharField(max_length=250)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_market')
    account_number = models.CharField(max_length=16, unique=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_user')
    product_name = models.CharField(max_length=250)
    product_price = models.DecimalField(max_digits=20, decimal_places=1)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product_price * self.quantity


class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction_user')
    account_number = models.CharField(max_length=16, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=1)
    status = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=100, unique=True)
    create_time = models.DateTimeField()

    reference_id = models.DecimalField(max_digits=10, unique=True, decimal_places=0)
    last_market_ok = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
