from django.shortcuts import render
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile


SUPPORTED_LANGUAGES = [
    ('en-US', 'English'),
    ('tr-TR', 'Türkçe'),
    ('de-DE', 'Deutsch'),
    ('fr-FR', 'Français'),
    ('es-ES', 'Español'),
    ('it-IT', 'Italiano'),
    ('pt-BR', 'Português'),
    ('ru-RU', 'Русский'),
    ('ar-SA', 'العربية'),
    ('ja-JP', '日本語'),
    ('ko-KR', '한국어'),
    ('zh-CN', '中文'),
]


def index(request):
    result = ''
    selected_lang = 'en-US'

    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        selected_lang = request.POST.get('language', 'en-US')

        try:
            recognizer = sr.Recognizer()
            file_ext = os.path.splitext(audio_file.name)[1].lower()

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_audio:
                for chunk in audio_file.chunks():
                    temp_audio.write(chunk)
                temp_audio_path = temp_audio.name

            try:
                if file_ext != '.wav':
                    audio = AudioSegment.from_file(temp_audio_path)
                    wav_path = temp_audio_path.rsplit('.', 1)[0] + '.wav'
                    audio.export(wav_path, format='wav')
                    os.unlink(temp_audio_path)
                    temp_audio_path = wav_path

                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = recognizer.record(source)
                    result = recognizer.recognize_google(audio_data, language=selected_lang)

            finally:
                if os.path.exists(temp_audio_path):
                    os.unlink(temp_audio_path)

        except sr.UnknownValueError:
            result = 'ERROR:Could not understand the audio. Try a clearer recording.'
        except sr.RequestError as e:
            result = f'ERROR:Speech recognition service error: {str(e)}'
        except Exception as e:
            result = f'ERROR:Error transcribing audio: {str(e)}'

    return render(request, 'audio_to_text/index.html', {
        'result': result,
        'languages': SUPPORTED_LANGUAGES,
        'selected_lang': selected_lang,
    })
