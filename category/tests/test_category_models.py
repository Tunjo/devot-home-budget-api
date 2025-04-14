import pytest
from decimal import Decimal
from account.models import BudgetHistory


@pytest.mark.django_db
def test_category_creation(user, category):
    """
    Test that a Category instance can be created successfully.
    """
    assert category.name == 'TestCategory'
    assert category.user == user
    assert str(category) == 'TestCategory'

@pytest.mark.django_db
def test_expense_creation(user, account_budget, category, expense):
    """
    Test that an Expense instance can be created successfully and updates the budget.
    """

    assert expense.user == user
    assert expense.category == category
    assert expense.amount == Decimal('50.00')
    assert expense.description == 'Test expense'
    assert str(expense) == f'{expense.amount} - {expense.category.name}'

    account_budget.refresh_from_db()
    assert account_budget.budget == Decimal('950.00')

    budget_history = BudgetHistory.objects.filter(user=user).last()

    assert budget_history is not None
    assert budget_history.change_type == BudgetHistory.EXPENSE
    assert budget_history.amount == Decimal('50.00')
    assert budget_history.description == 'Expense created: Test expense'

@pytest.mark.django_db
def test_expense_update(user, account_budget, category, expense):
    """
    Test that updating an Expense instance adjusts the budget and creates a BudgetHistory entry.
    """
    expense.amount = Decimal('30.00')
    expense.save()

    account_budget.refresh_from_db()
    assert account_budget.budget == Decimal('970.00')

    budget_history = BudgetHistory.objects.filter(user=user).last()
    assert budget_history is not None
    assert budget_history.change_type == BudgetHistory.INCOME
    assert budget_history.amount == Decimal('20.00')
    assert budget_history.description == 'Expense updated (difference treated as income): Test expense'

@pytest.mark.django_db
def test_expense_deletion(user, account_budget, expense):
    """
    Test that deleting an Expense instance adjusts the budget and creates a BudgetHistory entry.
    """
    expense.delete()

    account_budget.refresh_from_db()
    assert account_budget.budget == Decimal('1000.00')

    budget_history = BudgetHistory.objects.filter(user=user).last()
    assert budget_history is not None
    assert budget_history.change_type == BudgetHistory.INCOME
    assert budget_history.amount == Decimal('50.00')
    assert budget_history.description == 'Expense deleted: Test expense'