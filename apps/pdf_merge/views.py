from django.shortcuts import render
from django.http import HttpResponse
from pypdf import PdfWriter
import io

def index(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')
        
        try:
            writer = PdfWriter()
            
            for pdf in pdf_files:
                writer.append(pdf)
            
            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            
            response = HttpResponse(output, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="merged.pdf"'
            return response
            
        except Exception as e:
            return render(request, 'pdf_merge/index.html', {'error': f"Error merging PDFs: {str(e)}"})

    return render(request, 'pdf_merge/index.html')
