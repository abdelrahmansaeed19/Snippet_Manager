from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
#from __future__ import annotations
from typing import Any
import uuid
from django.conf import settings
from django.db import models
from tags.models import Tag 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)


    def __str__(self) -> str:
        return f"Profile({self.user.username})"
    

class Snippet(models.Model):
    """Code snippet model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    related_name="snippets")
    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through="SnippetTag", related_name="snippets")
    class Meta:
        ordering = ("-created_at",)
    def __str__(self) -> str: # pragma: no cover
        return self.title
    
class SnippetTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("snippet", "tag")

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE,
    related_name="favorites")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("snippet", "user")
        ordering = ("-created_at",)