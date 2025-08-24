from __future__ import annotations
from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "created_at")
        read_only_fields = ("id", "created_at")