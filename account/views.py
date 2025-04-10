
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, AccountBudgetSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import AccountBudget
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
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
        try:
            return AccountBudget.objects.get(user=self.request.user)
        except AccountBudget.DoesNotExist:

            raise NotFound(detail="AccountBudget not found.")

    @extend_schema(
        description="Retrieve the budget for the authenticated user.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Update the budget for the authenticated user.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
