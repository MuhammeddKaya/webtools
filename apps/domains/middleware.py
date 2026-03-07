from django.core.exceptions import DisallowedHost
from django.conf import settings
from .models import CustomDomain

class DynamicHostedMiddleware:
    """
    Safely filter incoming requests by Host header, pulling from settings
    and dynamic admin-configured domains.
    Required because ALLOWED_HOSTS will be ['*'] to let Nginx proxy to Django dynamically.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            return self.get_response(request)
            
        host = request.get_host().split(':')[0].lower()
        
        env_allowed = getattr(settings, 'ENV_ALLOWED_HOSTS', [])
        
        if host in env_allowed or '*' in env_allowed or host == '127.0.0.1' or host == 'localhost':
            return self.get_response(request)
            
        if CustomDomain.objects.filter(domain=host, is_active=True).exists():
            return self.get_response(request)
            
        raise DisallowedHost(f"Invalid HTTP_HOST header: '{host}'.")
