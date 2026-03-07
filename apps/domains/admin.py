from django.contrib import admin
from .models import CustomDomain

@admin.register(CustomDomain)
class CustomDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('domain',)
