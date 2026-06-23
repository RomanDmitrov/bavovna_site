from django.contrib import admin
from .models import Comment
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['name', 'text']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']

