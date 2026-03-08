from datetime import timedelta

from django.contrib import admin
from django.db.models import Sum

from .models import VisitStat


@admin.register(VisitStat)
class VisitStatAdmin(admin.ModelAdmin):
    list_display = ("date", "path", "country_code", "device_type", "visits")
    list_filter = ("date", "country_code", "device_type")
    search_fields = ("path",)
    date_hierarchy = "date"
    ordering = ("-date", "-visits")
    change_list_template = "admin/analytics/visitstat/change_list.html"

    def changelist_view(self, request, extra_context=None):
        from django.utils import timezone

        extra_context = extra_context or {}
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        agg = lambda qs: qs.aggregate(t=Sum("visits"))["t"] or 0

        extra_context["stats_today"] = agg(VisitStat.objects.filter(date=today))
        extra_context["stats_week"] = agg(VisitStat.objects.filter(date__gte=week_ago))
        extra_context["stats_total"] = agg(VisitStat.objects.all())
        extra_context["stats_top_pages"] = (
            VisitStat.objects.values("path")
            .annotate(total=Sum("visits"))
            .order_by("-total")[:10]
        )
        extra_context["stats_by_country"] = (
            VisitStat.objects.values("country_code")
            .annotate(total=Sum("visits"))
            .order_by("-total")[:10]
        )
        extra_context["stats_by_device"] = (
            VisitStat.objects.values("device_type")
            .annotate(total=Sum("visits"))
            .order_by("-total")
        )

        return super().changelist_view(request, extra_context)

