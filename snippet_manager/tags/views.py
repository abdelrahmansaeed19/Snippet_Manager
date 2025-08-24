from __future__ import annotations
from rest_framework import mixins, permissions, viewsets
from .models import Tag
from .serializers import TagSerializer

class TagViewSet(mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    """/api/tags, /api/tags/{id}"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)