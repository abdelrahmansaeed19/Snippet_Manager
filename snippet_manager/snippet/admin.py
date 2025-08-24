from django.contrib import admin
from .models import Snippet, Favorite, SnippetTag

admin.site.register(Snippet)
admin.site.register(Favorite)
admin.site.register(SnippetTag)

