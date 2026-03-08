import ipaddress
from functools import lru_cache

from django.db.models import F
from django.utils import timezone

import requests

from .models import VisitStat


def detect_device_type(user_agent: str) -> str:
    ua = (user_agent or "").lower()
    if "bot" in ua or "spider" in ua or "crawl" in ua:
        return "bot"
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        return "mobile"
    if "ipad" in ua or "tablet" in ua:
        return "tablet"
    if "windows" in ua or "macintosh" in ua or "linux" in ua:
        return "desktop"
    return "other"


def _is_public_ip(ip: str) -> bool:
    try:
        parsed = ipaddress.ip_address(ip)
        return not (parsed.is_private or parsed.is_loopback or parsed.is_reserved or parsed.is_link_local)
    except ValueError:
        return False


@lru_cache(maxsize=10000)
def _lookup_country_code(ip: str) -> str:
    """
    Best-effort IP -> country code lookup.
    Uses a public IP geolocation API; if anything fails, returns empty string.
    """
    if not ip or not _is_public_ip(ip):
        return ""

    try:
        # ipapi.co returns plain country code for /country/ endpoint, e.g. "TR"
        resp = requests.get(f"https://ipapi.co/{ip}/country/", timeout=1.5)
        if resp.status_code == 200:
            code = (resp.text or "").strip().upper()
            if len(code) == 2:
                return code
    except Exception:
        return ""

    return ""


def get_country_code_from_ip(ip: str) -> str:
    try:
        return _lookup_country_code(ip)
    except Exception:
        return ""


class VisitStatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path
        if path.startswith("/static/") or path.startswith("/media/") or path.startswith("/admin/"):
            return response

        raw_ip = request.META.get("HTTP_X_FORWARDED_FOR", "") or request.META.get("REMOTE_ADDR", "")
        ip = (raw_ip.split(",")[0] or "").strip()
        if not ip or not _is_public_ip(ip):
            return response

        today = timezone.now().date()
        ua = request.META.get("HTTP_USER_AGENT", "")
        device_type = detect_device_type(ua)
        country_code = get_country_code_from_ip(ip)

        obj, created = VisitStat.objects.get_or_create(
            date=today,
            path=path,
            country_code=country_code,
            device_type=device_type,
            defaults={"visits": 0},
        )

        if created:
            obj.visits = 1
            obj.save(update_fields=["visits"])
        else:
            VisitStat.objects.filter(pk=obj.pk).update(visits=F("visits") + 1)

        return response

