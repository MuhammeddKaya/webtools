from django.db import models
from django.utils.translation import gettext_lazy as _


class DeployLog(models.Model):
    """Keeps a log of git deployments triggered from admin."""
    STATUS_CHOICES = [
        ('success', _('Success')),
        ('error', _('Error')),
        ('running', _('Running')),
    ]

    triggered_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True,
        verbose_name=_('Triggered By')
    )
    status = models.CharField(_('Status'), max_length=10, choices=STATUS_CHOICES, default='running')
    branch = models.CharField(_('Branch'), max_length=100, default='main')
    commit_before = models.CharField(_('Commit Before'), max_length=40, blank=True)
    commit_after = models.CharField(_('Commit After'), max_length=40, blank=True)
    output = models.TextField(_('Output'), blank=True)
    created_at = models.DateTimeField(_('Triggered At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Deploy Log')
        verbose_name_plural = _('Deploy Logs')
        ordering = ['-created_at']

    def __str__(self):
        return f"Deploy #{self.pk} — {self.status} ({self.created_at:%Y-%m-%d %H:%M})"
