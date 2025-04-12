from django_filters import rest_framework as filters
from .models import Expense

class ExpenseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    date = filters.DateFilter(field_name="date")
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Expense
        fields = ['min_price', 'max_price', 'date', 'start_date', 'end_date', 'category']