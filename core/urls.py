from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from account.urls import account_urls

spectacular_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
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
    path('', include(spectacular_urls)),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls))

]
