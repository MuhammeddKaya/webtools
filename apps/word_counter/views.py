from django.shortcuts import render

def index(request):
    stats = None
    input_text = ''
    
    if request.method == 'POST':
        input_text = request.POST.get('text', '')
        words = input_text.split()
        stats = {
            'words': len(words),
            'chars': len(input_text),
            'chars_no_space': len(input_text.replace(' ', '')),
            'lines': len(input_text.splitlines()) if input_text else 0
        }

    return render(request, 'word_counter/index.html', {'stats': stats, 'input_text': input_text})
