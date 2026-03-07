from django.core.exceptions import DisallowedHost
from django.conf import settings
from urllib.parse import urlparse
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
        
        is_allowed = False
        if host in env_allowed or '*' in env_allowed or host == '127.0.0.1' or host == 'localhost':
            is_allowed = True
        elif CustomDomain.objects.filter(domain=host, is_active=True).exists():
            is_allowed = True
            
        if not is_allowed:
            raise DisallowedHost(f"Invalid HTTP_HOST header: '{host}'.")

        # Dynamically append CSRF trusted origins for our custom domains
        origin = request.META.get('HTTP_ORIGIN')
        if origin:
            try:
                parsed = urlparse(origin)
                schema_domain = f"{parsed.scheme}://{parsed.hostname}"
                if schema_domain not in settings.CSRF_TRUSTED_ORIGINS:
                    if CustomDomain.objects.filter(domain=parsed.hostname, is_active=True).exists():
                        settings.CSRF_TRUSTED_ORIGINS.append(schema_domain)
            except Exception:
                pass

        return self.get_response(request)
