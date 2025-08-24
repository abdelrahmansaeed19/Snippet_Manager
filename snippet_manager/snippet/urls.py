from __future__ import annotations
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, UserFavoriteViewSet

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')

urlpatterns = [
    path('', include(router.urls)),
    path("users/<uuid:user_id>/favorites", UserFavoriteViewSet.as_view({"get": "list"}), name="user-favorites"),
]