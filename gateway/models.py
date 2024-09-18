from django.db import models
from django.contrib.auth.models import User
from market.models import Market


# Create your models here.


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('not-confirm', 'Not-confirm')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psp_transaction_user')
    # from_market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='from_market')
    from_market = models.CharField(max_length=250)

    account_number = models.CharField(max_length=16, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=1)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)

    reference_id = models.DecimalField(max_digits=10, unique=True, decimal_places=0, null=True, blank=True)
    last_market_ok = models.BooleanField(default=False)
    bank_message = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
