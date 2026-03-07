from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io

def index(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        width = request.POST.get('width')
        height = request.POST.get('height')
        
        try:
            img = Image.open(image_file)
            
            if width and not height:
                w = int(width)
                h = int((w / img.width) * img.height)
            elif height and not width:
                h = int(height)
                w = int((h / img.height) * img.width)
            elif width and height:
                w = int(width)
                h = int(height)
            else:
                w, h = img.width, img.height
            
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            
            output = io.BytesIO()
            # Default to PNG if format is missing (e.g. uploaded bytes)
            img_format = img.format if img.format else 'PNG'
            img.save(output, format=img_format)
            output.seek(0)
            
            response = HttpResponse(output, content_type=f'image/{img_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="resized.{img_format.lower()}"'
            return response
            
        except Exception as e:
            return render(request, 'image_resize/index.html', {'error': f"Error resizing image: {str(e)}"})

    return render(request, 'image_resize/index.html')
