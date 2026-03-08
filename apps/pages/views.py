from django.shortcuts import get_object_or_404, render

from .models import StaticPage


def detail(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_active=True)
    return render(request, "pages/detail.html", {"page": page})

