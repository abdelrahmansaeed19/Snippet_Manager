from __future__ import annotations
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, UserFavoriteViewSet
# Removed incorrect import of obtain_auth_token

router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', include('rest_framework.urls')),  # For browsable API login
    path("users/<uuid:user_id>/favorites", UserFavoriteViewSet.as_view({"get": "list"}), name="user-favorites"),
]