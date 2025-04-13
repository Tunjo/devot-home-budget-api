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
from django.db.models import (
    Q,
    Sum
)
from drf_spectacular.utils import (
    extend_schema, extend_schema_view
)

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

@extend_schema_view(
    list=extend_schema(
        description=(
            'Retrieve a list of categories. This includes both user-specific categories '
            'and predefined categories (shared across all users).'
        ),
        responses={200: CategorySerializer(many=True)},
    ),
    create=extend_schema(
        description=(
            'Create a new category. The `user` field is automatically set to the authenticated user.'
        ),
        request=CategorySerializer,
        responses={201: CategorySerializer},
    ),
    update=extend_schema(
        description=(
            'Update an existing category. Predefined categories (shared across all users) '
            'cannot be updated.'
        ),
        request=CategorySerializer,
        responses={200: CategorySerializer},
    ),
    destroy=extend_schema(
        description=(
            'Delete an existing category. Predefined categories (shared across all users) '
            'cannot be deleted.'
        ),
        responses={204: None},
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        description=(
            'Retrieve a list of expenses with the following options:\n\n'
            '**Filters**:\n'
            '- `min_price`: Filter by an amount greater than or equal to this value.\n'
            '- `max_price`: Filter by an amount less than or equal to this value.\n'
            '- `start_date`: Filter by a date greater than or equal to this value.\n'
            '- `end_date`: Filter by a date less than or equal to this value.\n'
            '- `date`: Filter by an exact date.\n'
            '- `category`: Filter by category name (case-insensitive) or category ID.\n\n'
            '**Search**:\n'
            '- `search`: Search by description or category name.\n\n'
            '**Ordering**:\n'
            '- `ordering`: Order results by a field. Prefix with "-" for descending order. Available fields: `date`, `amount`, `category__name`.\n\n'
            '**Pagination**:\n'
            '- `page`: Page number for pagination.'
        ),
        responses={200: ExpenseSerializer(many=True)},
    ),
    create=extend_schema(
        description=(
            'Create a new expense. The `user` field is automatically set to the authenticated user.\n\n'
            '**Request Body**:\n'
            '- `amount` (required): The amount of the expense.\n'
            '- `description` (optional): A description of the expense.\n'
            '- `category` (required): The ID of the category associated with the expense.\n\n'
            '**Response**:\n'
            'Returns the created expense object with its details.'
        ),
        request=ExpenseSerializer,
        responses={201: ExpenseSerializer},
    ),
    update=extend_schema(
        description=(
            'Update an existing expense. The `user` field cannot be modified.'
        ),
        request=ExpenseSerializer,
        responses={200: ExpenseSerializer},
    ),
    destroy=extend_schema(
        description=(
            'Delete an existing expense.'
        ),
        responses={204: None},
    ),
)
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