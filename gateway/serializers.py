from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'from_market', 'amount', 'transaction_id', 'status', 'create_time', 'reference_id',
                  'last_market_ok']
        read_only_fields = ['status', 'transaction_id', 'create_time', 'reference_id', 'last_market_ok']
