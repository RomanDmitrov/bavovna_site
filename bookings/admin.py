from django.contrib import admin
from .models import BookingRequest
# Register your models here.

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'event_type', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']