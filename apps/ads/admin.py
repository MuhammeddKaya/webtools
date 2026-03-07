from django.contrib import admin
from .models import AdPlacement


@admin.register(AdPlacement)
class AdPlacementAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'page', 'is_active', 'order', 'updated_at']
    list_editable = ['is_active', 'order']
    list_filter = ['position', 'page', 'is_active']
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'page', 'order', 'is_active')
        }),
        ('Ad Code', {
            'fields': ('ad_code',),
            'description': 'Paste your Google AdSense or other ad network HTML code below.'
        }),
    )
