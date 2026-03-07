from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomDomain(models.Model):
    """
    Allows adding dynamic domains from the Django admin.
    These domains will be allowed by Django's ALLOWED_HOSTS middleware.
    """
    domain = models.CharField(_('Domain Name'), max_length=255, unique=True, help_text="e.g. webtools.example.com")
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Custom Domain')
        verbose_name_plural = _('Custom Domains')

    def __str__(self):
        return f"{self.domain} ({'Active' if self.is_active else 'Inactive'})"
