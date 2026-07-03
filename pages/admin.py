from django.contrib import admin
from .models import FAQ, Partner, PricePackage


# Register your models here.
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_ua', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    filter_horizontal = ['events']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(PricePackage)
class PricePackageAdmin(admin.ModelAdmin):
    list_display = ['name_ua', 'price_from', 'price_to', 'is_featured', 'order', 'is_active']
    list_editable = ['order', 'is_featured', 'is_active']