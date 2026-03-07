from django.shortcuts import render
import re


def index(request):
    result = ''
    input_text = ''
    options = {}

    if request.method == 'POST':
        input_text = request.POST.get('text', '')
        text = input_text

        # Get selected cleaning options
        options = {
            'extra_spaces': request.POST.get('extra_spaces') == 'on',
            'empty_lines': request.POST.get('empty_lines') == 'on',
            'trim_lines': request.POST.get('trim_lines') == 'on',
            'tabs_to_spaces': request.POST.get('tabs_to_spaces') == 'on',
            'duplicate_lines': request.POST.get('duplicate_lines') == 'on',
            'html_tags': request.POST.get('html_tags') == 'on',
            'special_chars': request.POST.get('special_chars') == 'on',
        }

        # If no options selected, default to extra_spaces
        if not any(options.values()):
            options['extra_spaces'] = True

        if options.get('html_tags'):
            text = re.sub(r'<[^>]+>', '', text)
        if options.get('tabs_to_spaces'):
            text = text.replace('\t', '    ')
        if options.get('trim_lines'):
            text = '\n'.join(line.strip() for line in text.splitlines())
        if options.get('extra_spaces'):
            text = re.sub(r'[ \t]+', ' ', text)
            text = '\n'.join(line.strip() for line in text.splitlines())
        if options.get('empty_lines'):
            text = '\n'.join(line for line in text.splitlines() if line.strip())
        if options.get('duplicate_lines'):
            text = re.sub(r'\n{3,}', '\n\n', text)
        if options.get('special_chars'):
            text = re.sub(r'[^\w\s.,!?;:\'"()\-\n]', '', text)

        result = text

    return render(request, 'text_cleaner/index.html', {
        'result': result,
        'input_text': input_text,
        'options': options
    })
