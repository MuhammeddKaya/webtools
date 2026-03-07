from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_name', 'category', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'id_name')
