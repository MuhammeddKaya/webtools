from django.db import models
from django.utils import timezone


class VisitStat(models.Model):
    DEVICE_CHOICES = (
        ("desktop", "Desktop"),
        ("mobile", "Mobile"),
        ("tablet", "Tablet"),
        ("bot", "Bot"),
        ("other", "Other"),
    )

    date = models.DateField(default=timezone.now)
    path = models.CharField(max_length=512)
    country_code = models.CharField(max_length=2, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default="other")

    visits = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("date", "path", "country_code", "device_type")
        verbose_name = "Visit Stat"
        verbose_name_plural = "Visit Stats"
        ordering = ("-date", "-visits")

    def __str__(self) -> str:
        return f"{self.date} {self.path} {self.country_code} {self.device_type}: {self.visits}"

