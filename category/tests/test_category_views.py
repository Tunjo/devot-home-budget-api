import pytest
from decimal import Decimal
from rest_framework.test import force_authenticate
from category.views import (
    CategoryViewSet,
    ExpenseViewSet,
    AggregationView
)
from category.models import (
    Category,
    Expense
)


@pytest.mark.django_db
def test_category_viewset_list(api_request_factory, user, category):
    """
    Test the list action of CategoryViewSet.
    """
    view = CategoryViewSet.as_view({'get': 'list'})
    request = api_request_factory.get('/categories/')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'TestCategory'


@pytest.mark.django_db
def test_category_viewset_create(api_request_factory, user):
    """
    Test the create action of CategoryViewSet.
    """
    view = CategoryViewSet.as_view({'post': 'create'})
    data = {'name': 'Test Utilities'}
    request = api_request_factory.post('/categories/', data, format='json')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 201
    assert response.data['name'] == 'Test Utilities'
    assert Category.objects.filter(name='Test Utilities', user=user).exists()


@pytest.mark.django_db
def test_category_viewset_update(api_request_factory, user, category):
    """
    Test the update action of CategoryViewSet.
    """
    view = CategoryViewSet.as_view({'put': 'update'})
    data = {'name': 'Updated Category'}
    request = api_request_factory.put(f'/categories/{category.id}/', data, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=category.id)

    assert response.status_code == 200
    assert response.data['name'] == 'Updated Category'
    category.refresh_from_db()
    assert category.name == 'Updated Category'


@pytest.mark.django_db
def test_expense_viewset_list(api_request_factory, user, expense):
    """
    Test the list action of ExpenseViewSet.
    """
    view = ExpenseViewSet.as_view({'get': 'list'})
    request = api_request_factory.get('/expenses/')
    force_authenticate(request, user=user)
    response = view(request)

    results = response.data.get('results', [])

    assert response.status_code == 200
    assert len(results) == 1
    assert results[0]['description'] == 'Test expense'


@pytest.mark.django_db
def test_expense_viewset_create(api_request_factory, user, category):
    """
    Test the create action of ExpenseViewSet.
    """
    view = ExpenseViewSet.as_view({'post': 'create'})
    data = {
        'amount': '100.00',
        'description': 'Test bill',
        'category': category.id
    }
    request = api_request_factory.post('/expenses/', data, format='json')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 201
    assert response.data['description'] == 'Test bill'
    assert Expense.objects.filter(description='Test bill', user=user).exists()


@pytest.mark.django_db
def test_expense_viewset_update(api_request_factory, user, expense):
    """
    Test the update action of ExpenseViewSet.
    """
    view = ExpenseViewSet.as_view({'put': 'update'})
    data = {
        'amount': '200.00',
        'description': 'Updated expense',
        'category': expense.category.id
    }
    request = api_request_factory.put(f'/expenses/{expense.id}/', data, format='json')
    force_authenticate(request, user=user)
    response = view(request, pk=expense.id)

    assert response.status_code == 200
    expense.refresh_from_db()
    assert expense.amount == Decimal('200.00')
    assert expense.description == 'Updated expense'


@pytest.mark.django_db
def test_expense_viewset_delete(api_request_factory, user, expense):
    """
    Test the delete action of ExpenseViewSet.
    """
    view = ExpenseViewSet.as_view({'delete': 'destroy'})
    request = api_request_factory.delete(f'/expenses/{expense.id}/')
    force_authenticate(request, user=user)
    response = view(request, pk=expense.id)

    assert response.status_code == 204
    assert not Expense.objects.filter(id=expense.id).exists()


@pytest.mark.django_db
def test_expense_viewset_filter_by_category(api_request_factory, user, expense, category):
    """
    Test filtering expenses by category.
    """
    view = ExpenseViewSet.as_view({'get': 'list'})
    request = api_request_factory.get(f'/expenses/?category={category.id}')
    force_authenticate(request, user=user)
    response = view(request)

    results = response.data.get('results', [])
    assert response.status_code == 200
    assert len(results) == 1
    assert results[0]['category'] == category.id


@pytest.mark.django_db
def test_expense_viewset_ordering(api_request_factory, user, expense):
    """
    Test ordering expenses by amount.
    """
    view = ExpenseViewSet.as_view({'get': 'list'})
    request = api_request_factory.get('/expenses/?ordering=amount')
    force_authenticate(request, user=user)
    response = view(request)

    results = response.data.get('results', [])
    assert response.status_code == 200
    assert len(results) == 1
    assert results[0]['amount'] == str(expense.amount)

@pytest.mark.django_db
def test_aggregation_view_total(api_request_factory, user, expense):
    """
    Test the total aggregation in AggregationView.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=total')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert response.data['total_spent'] == Decimal('50.00')
    assert response.data['total_earned'] == 1000.00
    assert response.data['net_earnings'] == 950.00


@pytest.mark.django_db
def test_aggregation_view_categories(api_request_factory, user, expense):
    """
    Test the categories aggregation in AggregationView.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=categories')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert len(response.data['expenses_by_category']) == 1
    assert response.data['expenses_by_category'][0]['category__name'] == 'TestCategory'
    assert response.data['expenses_by_category'][0]['total_expenses'] == Decimal('50.00')


@pytest.mark.django_db
def test_aggregation_view_average(api_request_factory, user, expense, category):
    """
    Test the average aggregation in AggregationView.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=average')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert len(response.data['average_expenses']) == 1
    assert response.data['average_expenses'][0]['category__name'] == 'TestCategory'
    assert response.data['average_expenses'][0]['average_expense'] == Decimal('50.00')


@pytest.mark.django_db
def test_aggregation_view_invalid_type(api_request_factory, user):
    """
    Test AggregationView with an invalid aggregation type.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=invalid')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 400
    assert response.data['error'] == 'Invalid type parameter. Use "total", "categories", or "average".'


@pytest.mark.django_db
def test_aggregation_view_filter_by_year(api_request_factory, user, expense):
    """
    Test AggregationView with a filter by year.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=total&year=2025')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert response.data['total_spent'] == Decimal('50.00')


@pytest.mark.django_db
def test_aggregation_view_invalid_category_ids(api_request_factory, user):
    """
    Test AggregationView with invalid category IDs.
    """
    view = AggregationView.as_view()
    request = api_request_factory.get('/aggregation/?type=categories&categories=invalid')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 400
    assert response.data['error'] == 'Invalid category IDs. Must be integers.'