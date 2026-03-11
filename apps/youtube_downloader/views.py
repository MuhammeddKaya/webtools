import os
import uuid
import shutil
import threading
import time

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import yt_dlp


def index(request):
    context = {}

    if request.method == "POST":
        url = (request.POST.get("url") or "").strip()
        fmt = (request.POST.get("format") or "mp3").lower()

        if not url:
            context["error"] = _("Lütfen bir YouTube video bağlantısı girin.")
            return render(request, "youtube_downloader/index.html", context)

        if "youtube.com" not in url and "youtu.be" not in url:
            context["error"] = _("Şu anda sadece YouTube bağlantıları destekleniyor.")
            return render(request, "youtube_downloader/index.html", context)

        if fmt not in ("mp3", "mp4"):
            fmt = "mp3"

        tmp_dir = os.path.join(settings.MEDIA_ROOT, "yt", str(uuid.uuid4()))
        os.makedirs(tmp_dir, exist_ok=True)

        ydl_opts = {
            "outtmpl": os.path.join(tmp_dir, "%(title).200B-%(id)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "restrictfilenames": True,
            "js_runtimes": {"nodejs": {}, "node": {}, "deno": {}},
            "extractor_args": {"youtube": {"player-client": ["web", "default"]}},
        }

        cookies_from_browser = getattr(settings, "YT_COOKIES_FROM_BROWSER", "").strip()
        cookies_browser_profile = getattr(settings, "YT_COOKIES_BROWSER_PROFILE", "").strip()
        cookies_file = getattr(settings, "YT_COOKIES_FILE", "")

        if cookies_from_browser:
            if cookies_browser_profile:
                ydl_opts["cookiesfrombrowser"] = (cookies_from_browser, cookies_browser_profile)
            else:
                ydl_opts["cookiesfrombrowser"] = (cookies_from_browser,)
        elif cookies_file and os.path.isfile(cookies_file):
            ydl_opts["cookiefile"] = cookies_file

        if fmt == "mp3":
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ],
                }
            )
        else:
            ydl_opts.update(
                {
                    "format": "bv*[ext=mp4]+ba/best[ext=mp4]/best",
                    "merge_output_format": "mp4",
                }
            )

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                download_path = ydl.prepare_filename(info)

            if fmt == "mp3":
                file_path = os.path.splitext(download_path)[0] + ".mp3"
            else:
                file_path = download_path

            if not os.path.exists(file_path):
                raise FileNotFoundError("İndirme tamamlandı ancak dosya bulunamadı.")

            filename = os.path.basename(file_path)
            response = FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=filename,
            )

            def cleanup():
                time.sleep(60)
                shutil.rmtree(tmp_dir, ignore_errors=True)

            threading.Thread(target=cleanup, daemon=True).start()

            return response
        except Exception as e:
            import traceback
            traceback.print_exc()
            context["error"] = _(
                f"İndirme sırasında bir hata oluştu: {str(e)}. Lütfen bağlantıyı kontrol edin veya daha sonra tekrar deneyin."
            )

    return render(request, "youtube_downloader/index.html", context)

