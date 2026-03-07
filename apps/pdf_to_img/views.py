from django.shortcuts import render
from django.http import HttpResponse
import fitz  # pymupdf
import io
import zipfile

def index(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        output_format = request.POST.get('format', 'jpg').lower()
        dpi = int(request.POST.get('dpi', '150'))
        page_selection = request.POST.get('pages', 'all')

        if output_format not in ('jpg', 'png', 'webp'):
            output_format = 'jpg'
        if dpi not in (72, 150, 300):
            dpi = 150

        try:
            pdf_bytes = pdf_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            # Determine which pages to convert
            if page_selection and page_selection != 'all':
                page_indices = set()
                for part in page_selection.split(','):
                    part = part.strip()
                    if '-' in part:
                        s, e = map(int, part.split('-'))
                        page_indices.update(range(s - 1, e))
                    else:
                        page_indices.add(int(part) - 1)
                pages = sorted(p for p in page_indices if 0 <= p < len(doc))
            else:
                pages = list(range(len(doc)))

            if not pages:
                return render(request, 'pdf_to_img/index.html', {'error': 'No valid pages selected.'})

            # Single page: return direct image
            scale = dpi / 72.0
            mat = fitz.Matrix(scale, scale)

            # Map format names for fitz
            fitz_format = 'jpeg' if output_format == 'jpg' else output_format
            mime_type = f'image/{fitz_format}' if output_format != 'jpg' else 'image/jpeg'

            if len(pages) == 1:
                page = doc[pages[0]]
                pix = page.get_pixmap(matrix=mat)
                img_data = pix.tobytes(fitz_format)
                response = HttpResponse(img_data, content_type=mime_type)
                response['Content-Disposition'] = f'attachment; filename="page_{pages[0]+1}.{output_format}"'
                return response

            # Multiple pages: return ZIP
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for i in pages:
                    page = doc[i]
                    pix = page.get_pixmap(matrix=mat)
                    img_data = pix.tobytes(fitz_format)
                    zip_file.writestr(f"page_{i+1}.{output_format}", img_data)

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="pdf_images.zip"'
            return response

        except Exception as e:
            return render(request, 'pdf_to_img/index.html', {'error': f"Error converting PDF: {str(e)}"})

    return render(request, 'pdf_to_img/index.html')
