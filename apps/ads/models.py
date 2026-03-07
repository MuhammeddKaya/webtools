from django.db import models
from django.utils.translation import gettext_lazy as _


class AdPlacement(models.Model):
    """Manages ad slots across the website."""

    POSITION_CHOICES = [
        ('sidebar_left', _('Sidebar Left')),
        ('sidebar_right', _('Sidebar Right')),
        ('header_banner', _('Header Banner')),
        ('footer_banner', _('Footer Banner')),
        ('in_content', _('In Content')),
    ]

    PAGE_CHOICES = [
        ('all', _('All Pages')),
        ('home', _('Home Page Only')),
        ('tools', _('Tool Pages Only')),
    ]

    name = models.CharField(_('Ad Name'), max_length=100)
    position = models.CharField(_('Position'), max_length=20, choices=POSITION_CHOICES)
    page = models.CharField(_('Show On'), max_length=20, choices=PAGE_CHOICES, default='all')
    ad_code = models.TextField(
        _('Ad Code (HTML)'),
        help_text=_('Paste your Google AdSense or ad network HTML code here.')
    )
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    class Meta:
        verbose_name = _('Ad Placement')
        verbose_name_plural = _('Ad Placements')
        ordering = ['position', 'order']

    def __str__(self):
        return f"{self.name} ({self.get_position_display()})"
