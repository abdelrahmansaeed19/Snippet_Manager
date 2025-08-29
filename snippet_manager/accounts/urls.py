from __future__ import annotations
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LogoutView, RegisterView, UserDetailView

urlpatterns = [
    # Auth
    path("auth/register", RegisterView.as_view(), name="auth-register"),
    path("auth/login", TokenObtainPairView.as_view(), name="auth-login"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="tokenrefresh"),
    path("auth/logout", LogoutView.as_view(), name="auth-logout"),
    # Users
    path("users/<int:user_id>", UserDetailView.as_view(), name="user-detail"),
]