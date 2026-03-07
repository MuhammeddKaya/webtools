from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class YoutubeDownloaderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.youtube_downloader"
    verbose_name = _("YouTube Downloader")

