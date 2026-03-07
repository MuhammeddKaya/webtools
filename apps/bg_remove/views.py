from django.shortcuts import render
from django.http import HttpResponse
from rembg import remove
import io

def index(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        
        try:
            input_image = image_file.read()
            output_image = remove(input_image)
            
            response = HttpResponse(output_image, content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="no_bg.png"'
            return response
            
        except Exception as e:
            return render(request, 'bg_remove/index.html', {'error': f"Error removing background: {str(e)}"})

    return render(request, 'bg_remove/index.html')
