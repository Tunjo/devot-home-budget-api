from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AccountBudget

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class AccountBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBudget
        fields = ['budget'] 