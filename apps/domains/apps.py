from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DomainsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.domains'
    verbose_name = _('Domain Settings')
