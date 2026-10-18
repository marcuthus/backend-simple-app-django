from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


from django.views.generic import RedirectView


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({'status': 'ok', 'app': 'backend-simple-app-django'})


urlpatterns = [
    # Root redirects to Swagger docs
    path('', RedirectView.as_view(url='/api/docs/', permanent=False), name='root-redirect'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Health Check
    path('api/health/', health_check, name='health-check'),

    # API Endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),

    # OpenAPI 3 / Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
