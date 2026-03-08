from django.contrib import admin

from .models import StaticPage


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active", "show_in_nav", "show_in_footer")
    list_editable = ("is_active", "show_in_nav", "show_in_footer")
    list_filter = ("is_active", "show_in_nav", "show_in_footer")
    search_fields = ("title", "slug", "key")
    ordering = ("nav_order", "title")
    prepopulated_fields = {"slug": ("title",)}

