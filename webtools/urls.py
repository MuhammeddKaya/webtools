from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('deploy/', include('apps.deploy.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('pdf-split/', include('apps.pdf_split.urls')),
    path('pdf-merge/', include('apps.pdf_merge.urls')),
    path('bg-remove/', include('apps.bg_remove.urls')),
    path('image-resize/', include('apps.image_resize.urls')),
    path('text-tools/', include('apps.text_tools.urls')),
    path('text-cleaner/', include('apps.text_cleaner.urls')),
    path('pdf-to-img/', include('apps.pdf_to_img.urls')),
    path('img-to-pdf/', include('apps.img_to_pdf.urls')),
    path('audio-to-text/', include('apps.audio_to_text.urls')),
    path('word-counter/', include('apps.word_counter.urls')),
    path('qr-generator/', include('apps.qr_generator.urls')),
    path('ppt-to-pdf/', include('apps.ppt_to_pdf.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
