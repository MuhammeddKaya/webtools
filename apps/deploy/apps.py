from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeployConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.deploy'
    verbose_name = _('Deployment')
