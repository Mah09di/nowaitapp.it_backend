"""
URL configuration for WaIT project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.permissions import AllowAny

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="WaIT API",
        default_version='v1',
        description="WaIT API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # مسیر قبلی (api/v1/)
    path('api/v1/',
         include([
             path('core/', include('core.urls')),
             path('accounts/', include('accounts.urls')),
             path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger')
         ])),
    
    # مسیر جدید (api/services/app/v1/) - به سبک عکس
    path('api/services/app/v1/',
         include([
             path('accounts/', include('accounts.urls')),
             path('', include('core.urls')),  # core.urls باید مسیرهای center, visitor, queue رو داشته باشه
         ])),
]