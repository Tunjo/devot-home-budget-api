import pytest
from account.models import (
    AccountBudget,
    BudgetHistory
)


@pytest.mark.django_db
def test_account_budget_creation(user):
    """
    Test that an AccountBudget instance is created when a User is created.
    """
    account_budget = AccountBudget.objects.get(user=user)
    assert account_budget is not None
    assert account_budget.budget == 1000.00

@pytest.mark.django_db
def test_budget_history_creation_on_user_creation(user):
    """
    Test that a BudgetHistory entry is created when a User is created.
    """
    budget_history = BudgetHistory.objects.filter(user=user).first()
    assert budget_history is not None
    assert budget_history.change_type == BudgetHistory.INCOME
    assert budget_history.amount == 1000.00
    assert budget_history.description == 'Initial budget allocation'

@pytest.mark.django_db
def test_budget_history_str_representation(user):
    """
    Test the string representation of BudgetHistory.
    """
    budget_history = BudgetHistory.objects.filter(user=user).first()
    expected_str = f'{user.username} - {budget_history.change_type} - {budget_history.amount} on {budget_history.date}'
    assert str(budget_history) == expected_str

@pytest.mark.django_db
def test_account_budget_str_representation(user):
    """
    Test the string representation of AccountBudget.
    """
    account_budget = AccountBudget.objects.get(user=user)
    expected_str = f"{user.username}'s Budget: {account_budget.budget}"
    assert str(account_budget) == expected_str