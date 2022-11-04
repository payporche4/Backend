from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
# for documentation generation
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from api.views import MyObtainTokenPairView

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("docs/", include_docs_urls(title="Payporche Documentation")),
    path(
        "schema/",
        get_schema_view(
            title="Your Project", description="API for all things …", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]
# api/password-reset/
# api/password-reset/confirm
# api/password-reset/validate_token
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
