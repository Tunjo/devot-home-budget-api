import pytest
from .conftest import user
from account.models import AccountBudget
from account.serializers import (
    UserSerializer,
    AccountBudgetSerializer
)

@pytest.mark.django_db
def test_user_serializer_create():
    """
    Test that the UserSerializer correctly creates a user with a hashed password.
    """
    data = {
        'username': 'testuser',
        'password': 'password123',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.first_name == 'Test'
    assert user.last_name == 'User'
    assert user.check_password('password123')

@pytest.mark.django_db
def test_user_serializer_password_write_only(user):
    """
    Test that the password field is write-only in the UserSerializer.
    """
    serializer = UserSerializer(user)
    data = serializer.data

    assert 'password' not in data

@pytest.mark.django_db
def test_account_budget_serializer(user):
    """
    Test that the AccountBudgetSerializer correctly serializes the budget field.
    """
    account_budget = AccountBudget.objects.get(user=user)

    serializer = AccountBudgetSerializer(account_budget)
    data = serializer.data

    assert data['budget'] == '1000.00'