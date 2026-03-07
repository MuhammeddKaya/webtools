from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import qrcode
import qrcode.image.svg
import io
import base64


def index(request):
    qr_data = None

    if request.method == 'POST':
        text = request.POST.get('text', '')
        fg_color = request.POST.get('fg_color', '#000000')
        bg_color = request.POST.get('bg_color', '#ffffff')
        size = int(request.POST.get('size', '10'))
        error_level = request.POST.get('error_level', 'M')
        download = request.POST.get('download', '')

        if text:
            error_map = {
                'L': qrcode.constants.ERROR_CORRECT_L,
                'M': qrcode.constants.ERROR_CORRECT_M,
                'Q': qrcode.constants.ERROR_CORRECT_Q,
                'H': qrcode.constants.ERROR_CORRECT_H,
            }

            qr = qrcode.QRCode(
                version=1,
                error_correction=error_map.get(error_level, qrcode.constants.ERROR_CORRECT_M),
                box_size=max(5, min(20, size)),
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            if download == 'svg':
                # SVG download
                factory = qrcode.image.svg.SvgPathImage
                img = qr.make_image(image_factory=factory)
                buffer = io.BytesIO()
                img.save(buffer)
                buffer.seek(0)
                response = HttpResponse(buffer, content_type='image/svg+xml')
                response['Content-Disposition'] = 'attachment; filename="qrcode.svg"'
                return response

            img = qr.make_image(fill_color=fg_color, back_color=bg_color)

            if download == 'png':
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)
                response = HttpResponse(buffer, content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
                return response

            # Generate preview (base64)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode('utf-8')
            qr_data = {
                'image': f'data:image/png;base64,{b64}',
                'text': text,
                'fg_color': fg_color,
                'bg_color': bg_color,
                'size': size,
                'error_level': error_level,
            }

    return render(request, 'qr_generator/index.html', {'qr_data': qr_data})
