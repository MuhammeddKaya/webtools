from typing import Dict, Any, List

from .models import StaticPage


def _get_default_pages() -> List[dict]:
    # Titles are in Turkish as you described; you can edit in admin later.
    return [
        {
            "key": "about",
            "slug": "hakkinda",
            "title": "Hakkında",
            "show_in_nav": True,
            "show_in_footer": True,
            "nav_order": 10,
            "footer_order": 10,
        },
        {
            "key": "contact",
            "slug": "iletisim",
            "title": "İletişim",
            "show_in_nav": True,
            "show_in_footer": True,
            "nav_order": 20,
            "footer_order": 20,
        },
        {
            "key": "privacy",
            "slug": "gizlilik",
            "title": "Gizlilik",
            "show_in_nav": True,
            "show_in_footer": True,
            "nav_order": 30,
            "footer_order": 30,
        },
        {
            "key": "terms",
            "slug": "kullanim-kosullari",
            "title": "Kullanım Koşulları",
            "show_in_nav": True,
            "show_in_footer": False,
            "nav_order": 40,
            "footer_order": 40,
        },
        {
            "key": "faq",
            "slug": "sss",
            "title": "SSS",
            "show_in_nav": True,
            "show_in_footer": False,
            "nav_order": 50,
            "footer_order": 50,
        },
    ]


def _ensure_default_pages() -> None:
    """
    Make sure the default static pages exist.
    This is idempotent and safe to call on every request.
    """
    for data in _get_default_pages():
        obj, created = StaticPage.objects.get_or_create(
            key=data["key"],
            defaults={
                "slug": data["slug"],
                "title": data["title"],
                "show_in_nav": data["show_in_nav"],
                "show_in_footer": data["show_in_footer"],
                "nav_order": data["nav_order"],
                "footer_order": data["footer_order"],
            },
        )
        if not created:
            changed = False
            for field in ("slug", "title", "show_in_nav", "show_in_footer", "nav_order", "footer_order"):
                if getattr(obj, field) != data[field]:
                    setattr(obj, field, data[field])
                    changed = True
            if changed:
                obj.save()


def static_pages(request) -> Dict[str, Any]:
    """
    Inject nav and footer static pages into all templates.
    """
    _ensure_default_pages()

    nav_pages = StaticPage.objects.filter(is_active=True, show_in_nav=True).order_by("nav_order", "title")
    footer_pages = StaticPage.objects.filter(is_active=True, show_in_footer=True).order_by(
        "footer_order", "title"
    )

    return {
        "nav_static_pages": nav_pages,
        "footer_static_pages": footer_pages,
    }

