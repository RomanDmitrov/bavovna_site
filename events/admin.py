from django.contrib import admin
from .models import Event, GalleryItem

# Register your models here.

class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 3


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title_ua', 'event_type', 'date', 'is_published']
    list_filter = ['event_type', 'is_published']
    search_fields = ['title_ua', 'title_en']
    list_editable = ['is_published']
    inlines = [GalleryItemInline]


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['event', 'order', 'created_at']