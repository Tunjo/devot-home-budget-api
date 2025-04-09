from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view

from rest_framework import permissions
from drf_yasg import openapi
from account.urls import account_urls

schema_view = get_schema_view(
   openapi.Info(
      title="Devot-home-budget-API",
      default_version='v1',
      description=(
          "Documentation for Devot-home-budget API.\n\n"
          "### Authentication\n"
          "To authenticate, use the `/api/login/` endpoint to obtain an access token. "
          "Include the token in the `Authorization` header for all authenticated requests:\n\n"
          "`Authorization: Bearer <your_access_token>`\n\n"
          "You can also refresh your token using the `/api/login/refresh/` endpoint."
      ),
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="antun.franjin@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_urls = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

auth_urls = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

api_urls = [
    path('', include(auth_urls)),
    path('', include(account_urls))
]

urlpatterns = [
    path('', include(swagger_urls)),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))

]
