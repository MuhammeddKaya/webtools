import os
import subprocess
from django.contrib import admin, messages
from .models import CustomDomain

@admin.action(description="Seçili Alan Adlarına SSL (Yeşil Kilit) Kur")
def request_ssl(modeladmin, request, queryset):
    for obj in queryset:
        domain = obj.domain

        # E-posta adresini ortam değişkenlerinden al veya varsayılan kullan
        email = os.environ.get('DEFAULT_SSL_EMAIL', 'yenieposta0476@gmail.com')

        # Certbot komutu
        certbot_cmd = [
            'certbot', 'certonly', '--webroot', '-w', '/var/www/certbot',
            '-d', domain, '--email', email, '--agree-tos', '--non-interactive'
        ]

        try:
            # 1. Certbot'u çalıştır (arka planda /var/www/certbot üzerinden challenge yapar)
            result = subprocess.run(certbot_cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # 2. SSL başarıyla alındı, bu domain için Nginx konfigürasyonunu oluştur
                config_content = f"""
server {{
    listen 80;
    server_name {domain};
    
    location /.well-known/acme-challenge/ {{
        root /var/www/certbot;
    }}
    
    location / {{
        return 301 https://$host$request_uri;
    }}
}}

server {{
    listen 443 ssl;
    server_name {domain};

    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 50M;

    location /static/ {{
        alias /app/staticfiles/;
        expires 30d;
    }}

    location /media/ {{
        alias /app/media/;
    }}

    location / {{
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
                conf_path = f"/etc/nginx/conf.d/{domain}.conf"
                with open(conf_path, 'w') as f:
                    f.write(config_content)
                
                # 3. Nginx'i yeniden başlat (Docker CLI kullanarak diğer konteynere sinyal gönder)
                # Docker daemon /var/run/docker.sock üzerinden erişilebilir olmalı
                subprocess.run(['docker', 'exec', 'webtools-nginx', 'nginx', '-s', 'reload'], check=False)

                messages.success(request, f"{domain} için SSL başarıyla kuruldu ve Nginx yenilendi!")
            else:
                messages.error(request, f"{domain} için SSL kurulamadı: {result.stderr}")
                
        except Exception as e:
            messages.error(request, f"{domain} işlemi sırasında hata oluştu: {str(e)}")

@admin.register(CustomDomain)
class CustomDomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('domain',)
    actions = [request_ssl]
