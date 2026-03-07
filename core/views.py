from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

def home(request):
    tools = [
        {'name': _('PDF Split'), 'desc': _('Split PDF files into individual pages or custom ranges'), 'url': 'pdf_split:index', 'icon': 'bi-scissors', 'category': 'pdf'},
        {'name': _('PDF Merge'), 'desc': _('Combine multiple PDF files into a single document'), 'url': 'pdf_merge:index', 'icon': 'bi-files', 'category': 'pdf'},
        {'name': _('PDF to Image'), 'desc': _('Convert PDF pages to JPG, PNG or WEBP images'), 'url': 'pdf_to_img:index', 'icon': 'bi-file-earmark-image', 'category': 'pdf'},
        {'name': _('Image to PDF'), 'desc': _('Convert and merge images into a PDF document'), 'url': 'img_to_pdf:index', 'icon': 'bi-file-earmark-pdf', 'category': 'pdf'},
        {'name': _('PPT to PDF'), 'desc': _('Convert PowerPoint presentations to PDF'), 'url': 'ppt_to_pdf:index', 'icon': 'bi-file-earmark-slides', 'category': 'pdf'},
        {'name': _('Background Remover'), 'desc': _('Remove background from any image with AI'), 'url': 'bg_remove:index', 'icon': 'bi-eraser', 'category': 'image'},
        {'name': _('Image Resize'), 'desc': _('Resize images with presets for social media'), 'url': 'image_resize:index', 'icon': 'bi-aspect-ratio', 'category': 'image'},
        {'name': _('Text Tools'), 'desc': _('Format JSON, convert case, encode/decode text'), 'url': 'text_tools:index', 'icon': 'bi-code-slash', 'category': 'text'},
        {'name': _('Text Cleaner'), 'desc': _('Remove extra spaces, blank lines and special characters'), 'url': 'text_cleaner:index', 'icon': 'bi-magic', 'category': 'text'},
        {'name': _('Word Counter'), 'desc': _('Count words, characters, sentences and reading time'), 'url': 'word_counter:index', 'icon': 'bi-bar-chart-line', 'category': 'text'},
        {'name': _('Audio to Text'), 'desc': _('Transcribe audio files to text in multiple languages'), 'url': 'audio_to_text:index', 'icon': 'bi-mic', 'category': 'other'},
        {'name': _('QR Generator'), 'desc': _('Generate customizable QR codes with colors'), 'url': 'qr_generator:index', 'icon': 'bi-qr-code', 'category': 'other'},
    ]
    return render(request, 'core/home.html', {'tools': tools})
