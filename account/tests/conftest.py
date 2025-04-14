import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from account.models import AccountBudget

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

