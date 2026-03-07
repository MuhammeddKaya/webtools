from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from pypdf import PdfReader, PdfWriter
import fitz  # pymupdf for thumbnails
import io
import base64

def index(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        page_range = request.POST.get('pages', '')

        try:
            reader = PdfReader(pdf_file)
            writer = PdfWriter()

            pages_to_extract = set()
            if page_range:
                parts = page_range.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        pages_to_extract.update(range(start - 1, end))
                    else:
                        pages_to_extract.add(int(part) - 1)

            for p in sorted(pages_to_extract):
                if 0 <= p < len(reader.pages):
                    writer.add_page(reader.pages[p])

            if not writer.pages:
                return render(request, 'pdf_split/index.html', {'error': 'No valid pages selected.'})

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)

            response = HttpResponse(output, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="extracted_pages.pdf"'
            return response

        except Exception as e:
            return render(request, 'pdf_split/index.html', {'error': f"Error processing PDF: {str(e)}"})

    return render(request, 'pdf_split/index.html')


def preview(request):
    """AJAX endpoint: returns page count and thumbnails as base64 images."""
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        try:
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            pages = []
            for i, page in enumerate(doc):
                # Generate thumbnail (150px wide)
                mat = fitz.Matrix(150 / page.rect.width, 150 / page.rect.width)
                pix = page.get_pixmap(matrix=mat)
                img_bytes = pix.tobytes("jpg")
                b64 = base64.b64encode(img_bytes).decode('utf-8')
                pages.append({
                    'index': i + 1,
                    'thumbnail': f'data:image/jpeg;base64,{b64}',
                    'width': round(page.rect.width * 0.3528),  # pts to mm
                    'height': round(page.rect.height * 0.3528),
                })
            return JsonResponse({'pages': pages, 'total': len(pages)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'No file provided'}, status=400)
