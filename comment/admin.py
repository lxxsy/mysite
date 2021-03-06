from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'comment_time', 'user', 'root', 'parent', 'content_type', 'object_id', 'content_object']

