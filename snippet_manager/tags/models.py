from __future__ import annotations
import uuid
from django.db import models

class Tag(models.Model):
    """Tags for snippets."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str: # pragma: no cover - for admin readability
        return self.name