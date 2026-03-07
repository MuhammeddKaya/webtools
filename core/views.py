from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from apps.tool_manager.models import Tool

def _get_default_tools():
    return [
        {'name': _('PDF Split'), 'desc': _('Split PDF files into individual pages or custom ranges'), 'id_name': 'pdf_split:index', 'icon': 'bi-scissors', 'category': 'pdf', 'order': 10},
        {'name': _('PDF Merge'), 'desc': _('Combine multiple PDF files into a single document'), 'id_name': 'pdf_merge:index', 'icon': 'bi-files', 'category': 'pdf', 'order': 20},
        {'name': _('PDF to Image'), 'desc': _('Convert PDF pages to JPG, PNG or WEBP images'), 'id_name': 'pdf_to_img:index', 'icon': 'bi-file-earmark-image', 'category': 'pdf', 'order': 30},
        {'name': _('Image to PDF'), 'desc': _('Convert and merge images into a PDF document'), 'id_name': 'img_to_pdf:index', 'icon': 'bi-file-earmark-pdf', 'category': 'pdf', 'order': 40},
        {'name': _('PPT to PDF'), 'desc': _('Convert PowerPoint presentations to PDF'), 'id_name': 'ppt_to_pdf:index', 'icon': 'bi-file-earmark-slides', 'category': 'pdf', 'order': 50},
        {'name': _('Background Remover'), 'desc': _('Remove background from any image with AI'), 'id_name': 'bg_remove:index', 'icon': 'bi-eraser', 'category': 'image', 'order': 60},
        {'name': _('Image Resize'), 'desc': _('Resize images with presets for social media'), 'id_name': 'image_resize:index', 'icon': 'bi-aspect-ratio', 'category': 'image', 'order': 70},
        {'name': _('Text Tools'), 'desc': _('Format JSON, convert case, encode/decode text'), 'id_name': 'text_tools:index', 'icon': 'bi-code-slash', 'category': 'text', 'order': 80},
        {'name': _('Text Cleaner'), 'desc': _('Remove extra spaces, blank lines and special characters'), 'id_name': 'text_cleaner:index', 'icon': 'bi-magic', 'category': 'text', 'order': 90},
        {'name': _('Word Counter'), 'desc': _('Count words, characters, sentences and reading time'), 'id_name': 'word_counter:index', 'icon': 'bi-bar-chart-line', 'category': 'text', 'order': 100},
        {'name': _('Audio to Text'), 'desc': _('Transcribe audio files to text in multiple languages'), 'id_name': 'audio_to_text:index', 'icon': 'bi-mic', 'category': 'other', 'order': 110},
        {'name': _('QR Generator'), 'desc': _('Generate customizable QR codes with colors'), 'id_name': 'qr_generator:index', 'icon': 'bi-qr-code', 'category': 'other', 'order': 120},
        {'name': _('Video to Audio'), 'desc': _('Extract MP3 audio from video files'), 'id_name': 'video_to_audio:index', 'icon': 'bi-file-earmark-music', 'category': 'other', 'order': 130},
        {'name': _('YouTube Downloader'), 'desc': _('Download YouTube videos as MP3 or MP4'), 'id_name': 'youtube_downloader:index', 'icon': 'bi-youtube', 'category': 'other', 'order': 135},
        {'name': _('Password Generator'), 'desc': _('Generate secure random passwords'), 'id_name': 'password_generator:index', 'icon': 'bi-shield-lock', 'category': 'other', 'order': 140},
        {'name': _('Text Diff'), 'desc': _('Compare two texts and find differences'), 'id_name': 'text_diff:index', 'icon': 'bi-intersect', 'category': 'text', 'order': 150},
        {'name': _('Lorem Ipsum'), 'desc': _('Generate placeholder dummy text'), 'id_name': 'lorem_ipsum:index', 'icon': 'bi-text-paragraph', 'category': 'text', 'order': 160},
    ]

def _sync_default_tools():
    """
    Ensure all default tools exist and keep basic fields updated.
    Safe to run on every request.
    """
    for t in _get_default_tools():
        obj, created = Tool.objects.get_or_create(
            id_name=t["id_name"],
            defaults={
                "name": t["name"],
                "desc": t["desc"],
                "icon": t["icon"],
                "category": t["category"],
                "order": t["order"],
            },
        )
        if not created:
            changed = False
            if obj.name != t["name"]:
                obj.name = t["name"]
                changed = True
            if obj.desc != t["desc"]:
                obj.desc = t["desc"]
                changed = True
            if obj.icon != t["icon"]:
                obj.icon = t["icon"]
                changed = True
            if obj.category != t["category"]:
                obj.category = t["category"]
                changed = True
            if obj.order != t["order"]:
                obj.order = t["order"]
                changed = True
            if changed:
                obj.save()


def home(request):
    # Her istekte eksik default tool'ları (örneğin yeni eklenen YouTube Downloader) senkronize et
    _sync_default_tools()

    active_tools = Tool.objects.filter(is_active=True)
    tools = []
    for t in active_tools:
        tools.append({'name': t.name, 'desc': t.desc, 'url': t.id_name, 'icon': t.icon, 'category': t.category})

    return render(request, 'core/home.html', {'tools': tools})
