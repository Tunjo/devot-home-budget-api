from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CategoryViewSet,
    ExpenseViewSet
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')

category_urls = router.urls