from __future__ import annotations
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value
    
    def create(self, validated_data: dict):
        user = User(username=validated_data["username"],
        email=validated_data.get("email"))
        user.set_password(validated_data["password"])
        user.save()
        
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "date_joined")
        read_only_fields = ("id", "date_joined")