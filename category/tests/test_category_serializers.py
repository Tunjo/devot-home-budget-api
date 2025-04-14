import pytest
from decimal import Decimal
from category.serializers import CategorySerializer, ExpenseSerializer


@pytest.mark.django_db
def test_category_serializer_create(user):
    """
    Test that the CategorySerializer correctly creates a Category instance.
    """
    data = {
        'name': 'Test Category',
    }
    serializer = CategorySerializer(data=data, context={'request': {'user': user}})
    assert serializer.is_valid(), serializer.errors

    category = serializer.save(user=user)
    assert category.name == 'Test Category'
    assert category.user == user

@pytest.mark.django_db
def test_category_serializer_read_only_fields(user, category):
    """
    Test that the `user` field in CategorySerializer is read-only.
    """
    serializer = CategorySerializer(category)
    data = serializer.data

    assert 'user' in data
    assert data['user'] == user.id

@pytest.mark.django_db
def test_expense_serializer_create(user, category):
    """
    Test that the ExpenseSerializer correctly creates an Expense instance.
    """
    data = {
        'amount': '50.00',
        'description': 'Test expense',
        'category': category.id
    }
    serializer = ExpenseSerializer(data=data, context={'request': {'user': user}})
    assert serializer.is_valid(), serializer.errors

    expense = serializer.save(user=user)
    assert expense.amount == Decimal('50.00')
    assert expense.description == 'Test expense'
    assert expense.category == category
    assert expense.user == user

@pytest.mark.django_db
def test_expense_serializer_read_only_fields(user, expense):
    """
    Test that the `user` and `date` fields in ExpenseSerializer are read-only.
    """

    serializer = ExpenseSerializer(expense)
    data = serializer.data

    assert 'user' in data
    assert data['user'] == user.id
    assert 'date' in data
    assert data['date'] == str(expense.date) 