from django.contrib import admin
from .models import BookingRequest, PartnershipRequest
# Register your models here.

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'event_type', 'status', 'created_at']
    list_filter = ['status', 'event_type']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PartnershipRequest)
class PartnershipRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'partnership_type', 'status', 'created_at']
    list_filter = ['status', 'partnership_type']
    search_fields = ['name', 'email', 'phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']