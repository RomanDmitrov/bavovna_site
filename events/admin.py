from django.contrib import admin
from .models import Event, GalleryItem, Category

# Register your models here.

class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 5

    class Media:
        js = ('events/admin_presigned_upload.js',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title_ua', 'date', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title_ua', 'title_en']
    list_editable = ['is_published']
    date_hierarchy = 'date'
    inlines = [GalleryItemInline]

    def save_formset(self, request, form, formset, change):
        if formset.model == GalleryItem:
            instances = formset.save(commit=False)
            for i, instance in enumerate(instances):
                prefix = formset.forms[i].prefix
                r2_key = request.POST.get(f'{prefix}-image_r2_key')
                if r2_key:
                    instance._r2_key = r2_key
                instance.save()
            formset.save_m2m()
        else:
            formset.save()

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['event', 'created_at']
    list_filter = ['event']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_ua', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name_ua',)}