from rest_framework import serializers

class FinancialReportSerializer(serializers.Serializer):
    total_income = serializers.FloatField()
    total_expenses = serializers.FloatField()
    net_income = serializers.FloatField()
