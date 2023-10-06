from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

admin.site.site_header = 'Omtogether'

schema_view = get_schema_view(
    openapi.Info(
        title="Медитация API",
        default_version="v1",
        description="API для Медитации",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="1"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/onboard/', include('onboarding.urls')),
    path('api/meditations/', include('meditacia.urls')),
    path('api/wallet/', include('wallet.urls')),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
