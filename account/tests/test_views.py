import pytest
from account.views import AccountBudgetViewSet, RegisterView
from account.models import BudgetHistory
from rest_framework.test import force_authenticate
from .conftest import api_request_factory, user, account_budget


@pytest.mark.django_db
def test_register_view(api_request_factory):
    """
    Test the RegisterView to ensure a user can be created using APIRequestFactory.
    """
    view = RegisterView.as_view({'post': 'create'})
    factory = api_request_factory
    data = {
        'username': 'newuser',
        'password': 'newpassword123',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User'
    }
    request = factory.post('/register/', data, format='json')
    response = view(request)

    assert response.status_code == 201
    assert response.data['username'] == 'newuser'


@pytest.mark.django_db
def test_account_budget_retrieve(api_request_factory, user, account_budget):
    """
    Test the retrieve action of AccountBudgetViewSet using APIRequestFactory.
    """
    view = AccountBudgetViewSet.as_view({'get': 'retrieve'})
    factory = api_request_factory
    request = factory.get('/budget/')
    
    force_authenticate(request, user=user)
    response = view(request, pk=account_budget.id)

    assert response.status_code == 200
    assert response.data['budget'] == '1000.00'


@pytest.mark.django_db
def test_account_budget_update(api_request_factory, user, account_budget):
    """
    Test the update action of AccountBudgetViewSet to increase the budget using APIRequestFactory.
    """
    view = AccountBudgetViewSet.as_view({'patch': 'update'})
    factory = api_request_factory
    data = {'budget_increase': 200.00}
    request = factory.patch('/budget/', data, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=account_budget.id)

    assert response.status_code == 200
    account_budget.refresh_from_db()
    assert account_budget.budget == 1200.00

    # Check that a BudgetHistory entry was created
    budget_history = BudgetHistory.objects.filter(user=user).last()
    assert budget_history is not None
    assert budget_history.change_type == BudgetHistory.INCOME
    assert budget_history.amount == 200.00
    assert budget_history.description == 'Manual budget increase'


@pytest.mark.django_db
def test_account_budget_update_invalid(api_request_factory, user, account_budget):
    """
    Test the update action of AccountBudgetViewSet with invalid data using APIRequestFactory.
    """
    view = AccountBudgetViewSet.as_view({'patch': 'update'})
    factory = api_request_factory

    # Test missing budget_increase
    request = factory.patch('/budget/', {}, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=account_budget.id)
    assert response.status_code == 400
    assert response.data['error'] == "The 'budget_increase' field is required."

    # Test invalid budget_increase
    request = factory.patch('/budget/', {'budget_increase': 'invalid'}, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=account_budget.id)
    assert response.status_code == 400
    assert response.data['error'] == "Invalid value for 'budget_increase'. It must be a number."

    # Test negative budget_increase
    request = factory.patch('/budget/', {'budget_increase': -100.00}, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=account_budget.id)
    assert response.status_code == 400
    assert response.data['error'] == "'budget_increase' must be greater than zero."