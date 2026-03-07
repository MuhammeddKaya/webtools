from django.shortcuts import render
import json
import re
import base64
import hashlib
import html as html_lib
from urllib.parse import quote, unquote


def index(request):
    result = ''
    input_text = ''
    action = 'json'

    if request.method == 'POST':
        input_text = request.POST.get('text', '')
        action = request.POST.get('action', 'json')

        try:
            if action == 'json':
                parsed = json.loads(input_text)
                result = json.dumps(parsed, indent=4, ensure_ascii=False)
            elif action == 'upper':
                result = input_text.upper()
            elif action == 'lower':
                result = input_text.lower()
            elif action == 'title':
                result = input_text.title()
            elif action == 'capitalize':
                result = input_text.capitalize()
            elif action == 'camelCase':
                words = re.split(r'[\s_\-]+', input_text)
                result = words[0].lower() + ''.join(w.capitalize() for w in words[1:]) if words else ''
            elif action == 'snake_case':
                s = re.sub(r'([A-Z])', r'_\1', input_text)
                result = re.sub(r'[\s\-]+', '_', s).strip('_').lower()
            elif action == 'kebab-case':
                s = re.sub(r'([A-Z])', r'-\1', input_text)
                result = re.sub(r'[\s_]+', '-', s).strip('-').lower()
            elif action == 'slug':
                s = input_text.lower().strip()
                s = re.sub(r'[^\w\s-]', '', s)
                result = re.sub(r'[\s_]+', '-', s).strip('-')
            elif action == 'reverse':
                result = input_text[::-1]
            elif action == 'base64_encode':
                result = base64.b64encode(input_text.encode('utf-8')).decode('utf-8')
            elif action == 'base64_decode':
                result = base64.b64decode(input_text.encode('utf-8')).decode('utf-8')
            elif action == 'url_encode':
                result = quote(input_text, safe='')
            elif action == 'url_decode':
                result = unquote(input_text)
            elif action == 'html_encode':
                result = html_lib.escape(input_text)
            elif action == 'html_decode':
                result = html_lib.unescape(input_text)
            elif action == 'md5':
                result = hashlib.md5(input_text.encode('utf-8')).hexdigest()
            elif action == 'sha256':
                result = hashlib.sha256(input_text.encode('utf-8')).hexdigest()
            else:
                result = input_text
        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'text_tools/index.html', {
        'result': result,
        'input_text': input_text,
        'action': action
    })
