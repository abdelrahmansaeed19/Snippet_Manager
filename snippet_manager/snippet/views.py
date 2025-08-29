from __future__ import annotations
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from tags.models import Tag
from .models import Favorite, Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import FavoriteSerializer, SnippetSerializer, SnippetWriteSerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

class SnippetViewSet(viewsets.ModelViewSet):
    """
    Endpoints:
    - GET /api/snippets
    - POST /api/snippets
    - GET /api/snippets/{id}
    - PUT /api/snippets/{id}
    - DELETE /api/snippets/{id}
    - POST /api/snippets/{id}/tags/{tag_id}
    - DELETE /api/snippets/{id}/tags/{tag_id}
    - POST /api/snippets/{id}/favorite
    - DELETE /api/snippets/{id}/favorite
    """
    queryset = Snippet.objects.select_related("user").prefetch_related("tags")
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Fields that can be filtered with `?language=python`
    filterset_fields = ["language", "user", "tags__name"]

    # Fields that can be searched with `?search=keyword`
    search_fields = ["title", "content", "language", "tags__name"]

    # Fields that can be ordered with `?ordering=created_at` or `?ordering=-created_at`
    ordering_fields = ["created_at", "updated_at", "title", "language"]
    ordering = ["-created_at"]  # default ordering


    def get_serializer_class(self): # type: ignore[override]
        if self.action in {"create", "update", "partial_update"}:
            return SnippetWriteSerializer
        return SnippetSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Re-serialize with the full read serializer (includes id, user, tags, etc.)
        read_serializer = SnippetSerializer(serializer.instance, context={"request": request})
        headers = self.get_success_headers(read_serializer.data)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def perform_create(self, serializer): # type: ignore[override]
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Snippet deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_destroy(self, instance):
        instance.delete()
    # <<< -------------------- >>>

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request: Request) -> Response:
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response({"detail": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        snippets = self.queryset.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(language__icontains=query)
        )

        page = self.paginate_queryset(snippets)

        if page is not None:
            serializer = SnippetSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        
        serializer = SnippetSerializer(snippets, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path=r"tags/(?P<tag_id>[0-9a-f\-]{32,36})")
    def add_tag(self, request: Request, pk: str, tag_id: str) -> Response:
        snippet = self.get_object()
        self.check_object_permissions(request, snippet)
        tag = get_object_or_404(Tag, id=tag_id)
        snippet.tags.add(tag)
        return Response(SnippetSerializer(snippet, context={"request": request}).data, status=status.HTTP_200_OK)
    
    @add_tag.mapping.delete
    def remove_tag(self, request: Request, pk: str, tag_id: str) -> Response:
        snippet = self.get_object()
        self.check_object_permissions(request, snippet)
        tag = get_object_or_404(Tag, id=tag_id)
        snippet.tags.remove(tag)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["post", "delete"], url_path="favorite")
    def favorite(self, request: Request, pk: str) -> Response:
        snippet = self.get_object()
        if request.method.lower() == "post":
            Favorite.objects.get_or_create(snippet=snippet, user=request.user)
            return Response({"detail": "Favorited."}, status=status.HTTP_201_CREATED)
        
        Favorite.objects.filter(snippet=snippet, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserFavoriteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """GET /api/users/{user_id}/favorites"""

    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self): # type: ignore[override]
        user_id = self.kwargs["user_id"]
        return Favorite.objects.select_related("snippet").filter(user_id=user_id)