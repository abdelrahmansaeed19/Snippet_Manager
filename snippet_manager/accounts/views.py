from __future__ import annotations
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


class LogoutView(APIView):
    """POST /api/auth/logout – blacklist refresh token."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> Response: # noqa: D401
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"detail": "Missing refresh token."},
        status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token."},
        status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_205_RESET_CONTENT)
    
class IsSelfOrAdmin(permissions.BasePermission):
    """Allow users to access their own profile or admins to access any."""

    def has_permission(self, request: Request, view: APIView) -> bool: # type:ignore[override]

        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request: Request, view: APIView, obj: User)-> bool: # type: ignore[override]

        return bool(request.user.is_superuser or obj == request.user)

class UserDetailView(APIView):
    """GET/PUT/DELETE /api/users/{user_id}"""
    permission_classes = (IsSelfOrAdmin,)

    def get_object(self, user_id: str):
        return get_object_or_404(User, id=user_id)
    
    def get(self, request: Request, user_id: str) -> Response:
        user = self.get_object(user_id)
        self.check_object_permissions(request, user)
        return Response(UserSerializer(user).data)  
    
    def put(self, request: Request, user_id: str) -> Response:
        user = self.get_object(user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request: Request, user_id: str) -> Response:
        user = self.get_object(user_id)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)