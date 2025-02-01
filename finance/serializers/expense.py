from rest_framework import serializers
from finance.models.expense import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'date', 'description']
        read_only_fields = ['id', 'date'] 
