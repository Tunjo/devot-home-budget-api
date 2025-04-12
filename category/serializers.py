from rest_framework import serializers
from .models import (
    Category,
    Expense
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']
        read_only_fields = ['user']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'date', 'category', 'user']
        read_only_fields = ['user', 'date']