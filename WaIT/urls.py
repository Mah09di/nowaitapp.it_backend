<<<<<<< HEAD
"""
URL configuration for WaIT project.
"""
=======
>>>>>>> develop
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework.permissions import AllowAny

schema_view = swagger_get_schema_view(
    openapi.Info(
<<<<<<< HEAD
        title="WaIT API",
        default_version='v1',
        description="WaIT API",
=======
        title="🚀 WaIT API",
        default_version="v1",
        description="WaIT Queue Management System API",
        contact=openapi.Contact(email="support@nowaitapp.ir"),
        license=openapi.License(name="MIT License"),
        terms_of_service="https://nowaitapp.ir/terms/",
>>>>>>> develop
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    
    # مسیر قبلی (api/v1/) با Swagger
    path('api/v1/',
         include([
             path('core/', include('core.urls')),
             path('accounts/', include('accounts.urls')),
             path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-v1')
         ])),
    
    # مسیر جدید (api/services/app/v1/) - بدون Swagger
    path('api/services/app/v1/',
         include([
             path('accounts/', include('accounts.urls')),
             path('', include('core.urls')),
         ])),
    
    # یا اضافه کردن Swagger به مسیر جدید هم
    path('api/services/app/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-services'),
]
=======
    path("admin/", admin.site.urls),
    # ============================================================
    # 📚 Swagger (دسترسی مستقیم)
    # ============================================================
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # ============================================================
    # 📱 فقط مسیر اپلیکیشن موبایل (services/app/v1)
    # ============================================================
    path(
        "api/services/app/v1/",
        include(
            [
                path("accounts/", include("accounts.urls")),
                path("", include("core.urls")),
            ]
        ),
    ),
]

# Customize Swagger UI - توضیحات تکمیل‌شده
swagger_info = {
    "title": "WaIT API Documentation",
    "description": """
# 🚀 WaIT Queue Management System API

## 🔐 Authentication
Use **Manager Login** endpoints to authenticate and get JWT token.
Include token in header: `Authorization: Bearer <your-token>`

## 📋 Available Endpoints

### 🔐 Authentication
- `POST /api/services/app/v1/accounts/auth/login/manager/` - Check user & send OTP
- `POST /api/services/app/v1/accounts/auth/register/manager/` - Register new manager with location
- `POST /api/services/app/v1/accounts/auth/login/manager/verify/` - Verify OTP & Login
- `POST /api/services/app/v1/accounts/auth/login/visitor/` - Visitor login (no OTP)
- `POST /api/services/app/v1/accounts/auth/refresh/` - Refresh token
- `POST /api/services/app/v1/accounts/auth/logout/` - Logout

### 🏢 Centers Management
- `POST /api/services/app/v1/centers/` - Create center
- `GET /api/services/app/v1/centers/{id}/` - Get center details
- `DELETE /api/services/app/v1/centers/{id}/` - Delete center

### 👥 Visitors Management
- `GET /api/services/app/v1/visitors/` - List visitors
- `POST /api/services/app/v1/visitors/` - Add visitor to queue
- `GET /api/services/app/v1/visitors/{id}/` - Get visitor details
- `PATCH /api/services/app/v1/visitors/{id}/` - Update visitor
- `DELETE /api/services/app/v1/visitors/{id}/` - Delete visitor

### 🚶 Queue Management
- `GET /api/services/app/v1/queue/{center_id}/` - Get queue list
- `POST /api/services/app/v1/queue/{center_id}/` - Add to queue
- `DELETE /api/services/app/v1/queue/{id}/delete` - Remove from queue
- `PATCH /api/services/app/v1/queue/{id}/status/` - Update status
- `GET /api/services/app/v1/queue/{center_id}/stats/` - Queue statistics
- `POST /api/services/app/v1/queue/{center_id}/next/` - Call next person
- `POST /api/services/app/v1/queue/{id}/reorder/` - Reorder queue

### 🌐 Public Endpoints (No Auth)
- `GET /api/services/app/v1/public/queue/{token}/stats/` - Public queue status
- `POST /api/services/app/v1/public/queue/rate/` - Submit rating

### 🔔 Notifications
- `GET /api/services/app/v1/notification/{center_id}/` - Get notifications
- `DELETE /api/services/app/v1/notification/{center_id}/delete/` - Clear notifications

## 🚀 Quick Start
1. `POST /api/services/app/v1/accounts/auth/login/manager/` - Check user
2. If new user: `POST /api/services/app/v1/accounts/auth/register/manager/` - Register
3. `POST /api/services/app/v1/accounts/auth/login/manager/verify/` - Verify OTP
4. Use received `access` token for all requests
""",
}
>>>>>>> develop
