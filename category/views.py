from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import Lower
from django.db.models import (
    Q,
    Sum,
    Avg
)
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

from account.models import BudgetHistory

from .models import (
    Category,
    Expense
)
from .serializers import (
    CategorySerializer,
    ExpenseSerializer
)
from .filters import ExpenseFilter
from .expense_pagination import ExpensePagination
from .schemas.aggregation_schemas import aggregation_schema
from .schemas.categories_schemas import categories_schemas
from .schemas.expense_schemas import expense_schema

@categories_schemas
class CategoryViewSet(ModelViewSet):
    """
    ViewSet for managing categories (CRUD).
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None


    def get_queryset(self):
        return Category.objects.filter(Q(user=self.request.user) | Q(user__isnull=True))
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing category. Predefined categories (shared across all users)
        cannot be updated.
        """
        category = self.get_object()
        if category.user is None:
            return Response(
                {'error': 'Predefined categories cannot be updated.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing category. Predefined categories (shared across all users)
        cannot be deleted.
        """
        category = self.get_object()
        if category.user is None:
            return Response(
                {'error': 'Predefined categories cannot be deleted.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


@expense_schema
class ExpenseViewSet(ModelViewSet):
    """
    ViewSet for managing expenses with dynamic filtering, search, pagination,
    and case-insensitive ordering.
    """
    serializer_class = ExpenseSerializer
    pagination_class = ExpensePagination
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExpenseFilter

    search_fields = ['description', 'category__name']
    ordering_fields = ['amount', 'date', 'category__name']
    ordering = ['-date']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_ordered_queryset(self, qs, initial_order):
        """
        Support case-insensitive ordering.
        Args:
            qs: Queryset of Expense instances.
            initial_order: Default ordering if query_params are not provided.
        Returns:
            Ordered queryset.
        """
        order_by = self.request.query_params.get('ordering')

        if not order_by:
            order_by = initial_order

        string_fields = ['category__name', 'description']
        if order_by.lstrip('-') in string_fields:
            if order_by.startswith('-'):
                return qs.order_by(Lower(order_by[1:])).reverse()
            return qs.order_by(Lower(order_by))

        return qs.order_by(order_by)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_ordered_queryset(
                self.filter_queryset(self.get_queryset()),
                '-date'
            )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@aggregation_schema
class AggregationView(APIView):
    """
    API View for dynamic aggregations based on query parameters.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        date = request.query_params.get('date')
        categories = request.query_params.get('categories')
        agg_type = request.query_params.get('type')

        if categories:
            try:
                categories = list(map(int, categories.split(',')))
            except ValueError:
                return Response(
                    {'error': 'Invalid category IDs. Must be integers.'},
                    status=400
                )

        filters = Q(user=request.user)
        if year:
            filters &= Q(date__year=year)
        if month:
            filters &= Q(date__month=month)
        if date:
            filters &= Q(date=date)
        if categories:
            filters &= Q(category_id__in=categories)

        if agg_type == 'total':
            return self.get_total(filters)
        elif agg_type == 'categories':
            return self.get_expenses_by_categories(filters)
        elif agg_type == 'average':
            return self.get_average_expenses(filters)
        else:
            return Response(
                {'error': 'Invalid type parameter. Use "total", "categories", or "average".'},
                status=400
            )

    def get_total(self, filters):
        """
        Calculate total earned and spent.
        """
        budget_filters = filters & ~Q(category_id__in=[])
        earnings = BudgetHistory.objects.filter(budget_filters).aggregate(
            total_earned=Sum('amount', filter=Q(change_type='income')),
            total_spent=Sum('amount', filter=Q(change_type='expense'))
        )

        total_earnings = (earnings['total_earned'] or 0) - (earnings['total_spent'] or 0)
        if total_earnings < 0:
            total_earnings = 0
        return Response({
            'total_earned': earnings['total_earned'] or 0,
            'total_spent': earnings['total_spent'] or 0,
            'net_earnings': total_earnings
        })

    def get_expenses_by_categories(self, filters):
        """
        Calculate expenses grouped by categories.
        """
        expenses_by_category = Expense.objects.filter(filters).values('category__name').annotate(
            total_expenses=Sum('amount')
        ).order_by('-total_expenses')

        return Response({
            'expenses_by_category': list(expenses_by_category)
        })

    def get_average_expenses(self, filters):
        """
        Calculate average expenses, optionally filtered by categories.
        """

        average_expenses = Expense.objects.filter(filters).values('category__name').annotate(
            average_expense=Avg('amount')
        ).order_by('-average_expense')

        return Response({
            'average_expenses': list(average_expenses)
        })