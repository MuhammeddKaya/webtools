from django.db import models
from django.utils.translation import gettext_lazy as _

class Tool(models.Model):
    CATEGORY_CHOICES = (
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('text', 'Text'),
        ('other', 'Other'),
    )

    id_name = models.CharField(_('Tool ID (URL name)'), max_length=100, unique=True, help_text="e.g. video_to_audio:index")
    name = models.CharField(_('Tool Name'), max_length=100)
    desc = models.CharField(_('Description'), max_length=255)
    icon = models.CharField(_('Bootstrap Icon Class'), max_length=50, help_text="e.g. bi-scissors")
    category = models.CharField(_('Category'), max_length=20, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(_('Active (Visible)'), default=True)
    order = models.IntegerField(_('Display Order'), default=0)

    class Meta:
        verbose_name = _('Tool')
        verbose_name_plural = _('Tools')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Hidden'})"
