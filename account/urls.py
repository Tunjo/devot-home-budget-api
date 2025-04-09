from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
)
from django.urls import (
    path,
    include
)


router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')

account_urls = [
    path('', include(router.urls))
]