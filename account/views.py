
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated
)
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import status
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from .contrib.unique_none import get_unique_or_none
from .serializers import (
    UserSerializer,
    AccountBudgetSerializer
)
from .models import AccountBudget, BudgetHistory
from .permissions import IsOwner 

class RegisterView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

class AccountBudgetViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """
    A GenericViewSet for retrieving and updating the user's account budget.
    - Overrides `get_object` to fetch the budget based on the authenticated user.
    - Uses RetrieveModelMixin and UpdateModelMixin for GET and PATCH/PUT actions.
    """
    queryset = AccountBudget.objects.all()
    serializer_class = AccountBudgetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        budget = get_unique_or_none(AccountBudget, user=self.request.user)
        if budget is None:
            raise NotFound(detail='AccountBudget not found.')
        return budget

    @extend_schema(
        description='Retrieve the budget for the authenticated user.',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Increase the budget for the authenticated user.',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'budget_increase': {
                        'type': 'number',
                        'description': 'The amount to increase the budget by. Must be greater than zero.',
                        'example': 100.00
                    }
                },
                'required': ['budget_increase']
            }
        },
        responses={
            200: AccountBudgetSerializer,
        }
    )
    def update(self, request, *args, **kwargs):
        budget = self.get_object()

        budget_increase = request.data.get('budget_increase')

        if budget_increase is None:
            return Response({'error': "The 'budget_increase' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            budget_increase = Decimal(budget_increase)
        except (ValueError, TypeError):
            return Response({'error': "Invalid value for 'budget_increase'. It must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        if budget_increase <= 0:
            return Response({'error': "'budget_increase' must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

        budget.budget += budget_increase
        budget.save()

        BudgetHistory.objects.create(
            user=request.user,
            change_type=BudgetHistory.INCOME,
            amount=budget_increase,
            description='Manual budget increase'
        )

        serializer = self.get_serializer(budget)
        return Response(serializer.data, status=status.HTTP_200_OK)
