from django_filters import rest_framework as filters
from .models import Expense

class ExpenseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    date = filters.DateFilter(field_name='date')
    category = filters.CharFilter(method='filter_category')

    class Meta:
        model = Expense
        fields = ['min_price', 'max_price', 'date', 'start_date', 'end_date', 'category', ]
    
    def filter_category(self, queryset, name, value):
        """
        Filter by category name or ID.
        If the value is numeric, filter by ID.
        Otherwise, filter by name (case-insensitive).
        """
        if value.isdigit():
            return queryset.filter(category__id=value)
        return queryset.filter(category__name__icontains=value)