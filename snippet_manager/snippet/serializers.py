from __future__ import annotations
from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from tags.serializers import TagSerializer
from tags.models import Tag
from .models import Favorite, Snippet

User = get_user_model()

class SnippetSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Snippet
        fields = (
        "id",
        "user",
        "title",
        "content",
        "language",
        "tags",
        "created_at",
        "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at" "user", "tags")

    def create(self, validated_data: dict[str, Any]) -> Snippet:
        request = self.context.get("request")
        assert request is not None and request.user.is_authenticated
        return Snippet.objects.create(user=request.user, **validated_data)
    
class SnippetWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ("title", "content", "language")

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "snippet", "user", "created_at")
        read_only_fields = ("id", "user", "created_at")