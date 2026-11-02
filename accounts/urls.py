from django.urls import path
from .views import (
    VisitorLoginView,
    ManagerLoginStartView,
    ManagerRegisterView,
    ManagerVerifyView,
    TokenRefreshView,
    LogoutView,
)

app_name = "accounts"

urlpatterns = [
    # ============================================================
    # 🔐 Manager Authentication (Mobile App)
    # ============================================================
    path(
        "auth/login/manager/",
        ManagerLoginStartView.as_view(),
        name="login-manager-start",
    ),
    path(
        "auth/register/manager/",
        ManagerRegisterView.as_view(),
        name="register-manager",
    ),
    path(
        "auth/login/manager/verify/",
        ManagerVerifyView.as_view(),
        name="login-manager-verify",
    ),
    # ============================================================
    # 👤 Visitor Authentication
    # ============================================================
    path(
        "auth/login/visitor/",
        VisitorLoginView.as_view(),
        name="login-visitor",
    ),
    # ============================================================
    # 🔄 Token Management
    # ============================================================
    path(
        "auth/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
