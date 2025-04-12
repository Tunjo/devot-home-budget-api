from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import Lower
from django.db.models import Q

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
        Prevent predefined categories (user=None) from being updated.
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
        Prevent predefined categories (user=None) from being deleted.
        """
        category = self.get_object()
        if category.user is None:
            return Response(
                {'error': 'Predefined categories cannot be deleted.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


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

        # Check if the field is a string field (e.g., category__name)
        string_fields = ['category__name', 'description']
        if order_by.lstrip('-') in string_fields:
            if order_by.startswith('-'):
                return qs.order_by(Lower(order_by[1:])).reverse()
            return qs.order_by(Lower(order_by))

        # For non-string fields (e.g., date, amount), use direct ordering
        return qs.order_by(order_by)

    def list(self, request, *args, **kwargs):
        """
        Return a list of all expenses as a paginated response.
        """
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