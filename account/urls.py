from .views import (
    RegisterView,
    AccountBudgetViewSet
)
from django.urls import (
    path,
)


account_urls = [
    path('register/', RegisterView.as_view({'post': 'create'}), name='register'),
    path('budget/', AccountBudgetViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='account_budget'),
]