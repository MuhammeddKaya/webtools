from django import template
from django.utils.safestring import mark_safe
from apps.ads.models import AdPlacement

register = template.Library()


@register.simple_tag(takes_context=True)
def show_ad(context, position):
    """
    Render ad(s) for a given position if active ads exist.
    Usage: {% load ads_tags %}{% show_ad "sidebar_left" %}
    Returns empty string if no active ads for that position.
    """
    request = context.get('request')
    page_type = 'home' if request and request.resolver_match and request.resolver_match.url_name == 'home' else 'tools'

    ads = AdPlacement.objects.filter(
        is_active=True,
        position=position
    ).filter(
        page__in=['all', page_type]
    ).order_by('order')

    if not ads.exists():
        return ''

    html_parts = []
    for ad in ads:
        html_parts.append(ad.ad_code)

    return mark_safe('\n'.join(html_parts))
