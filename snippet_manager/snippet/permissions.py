from __future__ import annotations
from rest_framework import permissions
from rest_framework.request import Request
from .models import Snippet

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only owners can modify."""

    def has_object_permission(self, request: Request, view, obj: Snippet) -> bool: # type: ignore[override]

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(request.user and request.user.is_authenticated and
        obj.user_id == request.user.id)