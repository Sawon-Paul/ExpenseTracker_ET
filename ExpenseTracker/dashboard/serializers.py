# serializers.py
from rest_framework import serializers
from .models import Transactions

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['user', 'type', 'subtype', 'amount', 'description', 'timestamp']
