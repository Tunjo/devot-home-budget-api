
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, AccountBudgetSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AccountBudget
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema

class RegisterView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class AccountBudgetViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountBudgetSerializer

    @extend_schema(
        description="Retrieve the budget for the authenticated user.",
        request=AccountBudgetSerializer,
        responses={200: AccountBudgetSerializer},
    )
    def retrieve(self, request):
        try:
            account_budget = AccountBudget.objects.get(user=request.user)
        except AccountBudget.DoesNotExist:
            return Response({"error": "AccountBudget not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountBudgetSerializer(account_budget)
        return Response(serializer.data)

    @extend_schema(
        description="Update the budget for the authenticated user.",
        request=AccountBudgetSerializer,
        responses={200: AccountBudgetSerializer},
    )
    def update(self, request):
        try:
            account_budget = AccountBudget.objects.get(user=request.user)
        except AccountBudget.DoesNotExist:
            return Response({"error": "AccountBudget not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountBudgetSerializer(account_budget, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
