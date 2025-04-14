import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from decimal import Decimal
from account.models import AccountBudget
from category.models import Category, Expense

@pytest.fixture
def api_request_factory():
    """
    Fixture to create an APIRequestFactory for testing.
    """
    return APIRequestFactory()

@pytest.fixture
def user(db):
    """
    Fixture to create a test user.
    """
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def account_budget(db, user):
    """
    Fixture to return a test account budget.
    """

    return AccountBudget.objects.get(user=user)

@pytest.fixture
def category(db, user):
    """
    Fixture to create a test category.
    """

    return Category.objects.create(name='TestCategory', user=user)

@pytest.fixture
def expense(db, user, category):
    """
    Fixture to create a test expense.
    """
    return Expense.objects.create(
        user=user,
        category=category,
        amount=Decimal('50.00'),
        description='Test expense'
    )