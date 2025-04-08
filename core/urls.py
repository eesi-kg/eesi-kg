from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from applications.real_estate_advertisement.admin import RealEstateAdForm
from core import settings


admin.site.site_header = "EESi KG"
admin.site.index_title = "Administration"
admin.site.site_title = "EESi Admin Panel"


schema_view = get_schema_view(
    openapi.Info(
        title="EESi KG API",
        default_version='v1',
        description="API documentation for Advertisement Platform",
    ),
    public=True,
)

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('applications.user.urls')),
    path('real-estate/', include('applications.real_estate_advertisement.urls')),
    path('vehicle/', include('applications.vehicle_advertisement.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
