from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'from_market', 'amount', 'transaction_id', 'status', 'created_at']
        read_only_fields = ['status', 'transaction_id', 'created_at']