import os
import uuid
import subprocess
from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpResponse

def index(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        
        # Validations
        if video_file.size > 200 * 1024 * 1024:  # 200MB limit
            return render(request, 'video_to_audio/index.html', {'error': 'Dosya boyutu 200MB limitini aşıyor.'})
            
        ext = os.path.splitext(video_file.name)[1].lower()
        if ext not in ['.mp4', '.avi', '.mov', '.mkv']:
            return render(request, 'video_to_audio/index.html', {'error': 'Desteklenmeyen video formatı.'})

        # Process
        file_id = str(uuid.uuid4())
        
        # Ensure media directory exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        input_path = os.path.join(settings.MEDIA_ROOT, f'{file_id}{ext}')
        output_path = os.path.join(settings.MEDIA_ROOT, f'{file_id}.mp3')

        with open(input_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        try:
            # Run ffmpeg to extract audio: ffmpeg -i input.mp4 -vn -ar 44100 -ac 2 -b:a 192k output.mp3
            result = subprocess.run([
                'ffmpeg', '-y', '-i', input_path, 
                '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', 
                output_path
            ], capture_output=True, text=True)

            if result.returncode != 0:
                return render(request, 'video_to_audio/index.html', {'error': 'Dönüştürme sırasında hata oluştu.'})

            response = FileResponse(open(output_path, 'rb'), as_attachment=True, filename=f'{os.path.splitext(video_file.name)[0]}.mp3')
            
            # Clean up files after sending
            import threading
            def cleanup():
                import time
                time.sleep(5)
                try:
                    if os.path.exists(input_path): os.remove(input_path)
                    if os.path.exists(output_path): os.remove(output_path)
                except: pass
            threading.Thread(target=cleanup).start()

            return response

        except Exception as e:
            return render(request, 'video_to_audio/index.html', {'error': str(e)})

    return render(request, 'video_to_audio/index.html')
