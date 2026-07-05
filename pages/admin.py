from django.contrib import admin
from .models import FAQ, Partner, PricePackage


# Register your models here.
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_ua', 'order', 'is_active']
    list_filter = ['show_on_all_events', 'is_active']
    list_editable = ['order', 'is_active']
    filter_horizontal = ['events']
    fields = [
        'question_ua', 'question_en',
        'answer_ua', 'answer_en',
        'show_on_all_events', 'events',
        'order', 'is_active',
    ]

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    fields = [
        'name',
        'description_ua', 'description_en',
        'logo', 'website', 'instagram',
        'order', 'is_active',
    ]


@admin.register(PricePackage)
class PricePackageAdmin(admin.ModelAdmin):
    list_display = ['name_ua', 'price_from', 'price_to', 'is_featured', 'order', 'is_active']
    list_filter = ['is_active', 'is_featured']
    list_editable = ['order', 'is_featured', 'is_active']
    fields = [
        'name_ua', 'name_en',
        'price_from', 'price_to',
        'guests_ua', 'guests_en',
        'features_ua', 'features_en',
        'is_featured', 'order', 'is_active',
    ]