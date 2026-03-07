from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io

def index(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        
        try:
            img_list = []
            for img_file in images:
                img = Image.open(img_file)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img_list.append(img)
            
            if not img_list:
                raise ValueError("No valid images uploaded")

            output = io.BytesIO()
            img_list[0].save(output, save_all=True, append_images=img_list[1:], format='PDF')
            output.seek(0)
            
            response = HttpResponse(output, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="images.pdf"'
            return response
            
        except Exception as e:
            return render(request, 'img_to_pdf/index.html', {'error': f"Error converting images: {str(e)}"})

    return render(request, 'img_to_pdf/index.html')
