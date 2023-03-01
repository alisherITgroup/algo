from django.contrib import admin
from .models import Post, PostComment, Tag

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ["tag"]
    search_fields = ["tag"]

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "count_likes"]
    search_fields = ["name"]

@admin.register(PostComment)
class PostCommentModelAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "date"]
    list_filter = ["post", "author", "date"]
