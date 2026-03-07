from django.shortcuts import render
from django.http import HttpResponse
from pptx import Presentation
from PIL import Image
import io

def index(request):
    if request.method == 'POST' and request.FILES.get('ppt_file'):
        ppt_file = request.FILES['ppt_file']
        
        try:
            # Read PowerPoint
            prs = Presentation(ppt_file)
            
            # For now, we'll create a simple message
            # Note: Converting PPT to PDF properly requires LibreOffice or similar
            # This is a simplified version that shows it's not directly supported
            return render(request, 'ppt_to_pdf/index.html', {
                'error': 'PPT to PDF conversion requires LibreOffice to be installed on the server. This feature is currently unavailable in the web version.'
            })
            
        except Exception as e:
            return render(request, 'ppt_to_pdf/index.html', {'error': f"Error processing PowerPoint: {str(e)}"})

    return render(request, 'ppt_to_pdf/index.html')
