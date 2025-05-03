# serializers.py
from rest_framework import serializers
from .models import Transactions
from .models import Bill, RecurringExpense, Budget

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['user', 'type', 'subtype', 'amount', 'description', 'timestamp']
        
        
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class RecurringExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpense
        fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'        