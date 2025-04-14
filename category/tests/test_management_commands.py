import pytest
from django.core.management import call_command
from category.models import Category, Expense
from decimal import Decimal


@pytest.mark.django_db
def test_create_predefined_categories():
    """
    Test the create_predefined_categories management command.
    """
    assert Category.objects.filter(user=None).count() == 0

    call_command('create_predefined_categories')

    predefined_categories = [
        'Food & Groceries',
        'Transportation',
        'Rent & Utilities',
        'Healthcare',
        'Entertainment'
    ]
    for category_name in predefined_categories:
        assert Category.objects.filter(name=category_name, user=None).exists()


@pytest.mark.django_db
def test_trigger_expense_signals(user, category):
    """
    Test the trigger_expense_signals management command.
    """
    expense = Expense.objects.create(
        user=user,
        category=category,
        amount=Decimal('100.00'),
        description='Test expense'
    )

    call_command('trigger_expense_signals')

    expense.refresh_from_db()
    assert expense.amount == Decimal('100.00')  