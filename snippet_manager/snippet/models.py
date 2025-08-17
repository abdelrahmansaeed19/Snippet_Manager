from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
#from __future__ import annotations
from typing import Any

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)


    def __str__(self) -> str:
        return f"Profile({self.user.username})"