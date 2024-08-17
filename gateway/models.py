from django.db import models
from django.contrib.auth.models import User
from market.models import Market


# Create your models here.

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_account')
    account_number = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=128)
    balance = models.DecimalField(max_digits=20, decimal_places=1)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # from_market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='from_market')
    from_market = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=20, decimal_places=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
