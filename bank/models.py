from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BankAccount(models.Model):
    STATUS_ACCOUNT = (
        ('active', 'Active'),
        ('deactivate', 'Deactivate')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_account')
    account_number = models.CharField(max_length=16, unique=True)
    password = models.CharField(max=128)
    cvv2 = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=20, decimal_places=1)
    account_status = models.CharField(max_length=10, choices=STATUS_ACCOUNT, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    from_market = models.CharField(max_length=250, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    reference_id = models.DecimalField(max_digits=10, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    last_market_ok = models.BooleanField(default=False)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"




