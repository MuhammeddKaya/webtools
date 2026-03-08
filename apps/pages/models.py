from django.db import models
from django.utils.translation import gettext_lazy as _


class StaticPage(models.Model):
    """
    Simple CMS-like model for static pages such as:
    - About (Hakkında)
    - Contact (İletişim)
    - Privacy
    - Terms
    - FAQ (SSS)
    """

    key = models.CharField(
        max_length=50,
        unique=True,
        help_text=_("Internal key, e.g. 'about', 'contact', 'privacy', 'terms', 'faq'."),
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_("URL slug, e.g. 'about', 'contact'."),
    )
    title = models.CharField(max_length=150, verbose_name=_("Title"))
    content = models.TextField(blank=True, verbose_name=_("Content"))

    is_active = models.BooleanField(default=True, verbose_name=_("Active (visible)"))
    show_in_nav = models.BooleanField(default=True, verbose_name=_("Show in main menu"))
    show_in_footer = models.BooleanField(default=False, verbose_name=_("Show in footer"))

    nav_order = models.IntegerField(default=100, verbose_name=_("Menu order"))
    footer_order = models.IntegerField(default=100, verbose_name=_("Footer order"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Static Page")
        verbose_name_plural = _("Static Pages")
        ordering = ["nav_order", "title"]

    def __str__(self) -> str:
        return self.title

