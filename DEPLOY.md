# 🚀 WebTools — Sunucu Kurulum Kılavuzu

## Gereksinimler (Sunucuda)

- Ubuntu 22.04+ veya Debian 12+
- Docker ve Docker Compose yüklü
- Git yüklü
- En az 2GB RAM

---

## 1. Sunucuya Docker Kurulumu

```bash
# Docker kurulumu
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Oturumu kapatıp tekrar açın

# Docker Compose (genelde Docker ile birlikte gelir)
docker compose version
```

---

## 2. Projeyi Sunucuya Çekme

```bash
cd /opt
sudo git clone https://github.com/KULLANICI/webtools.git
cd webtools
sudo chown -R $USER:$USER .
```

---

## 3. Ortam Değişkenlerini Ayarlama

```bash
cp .env.example .env
nano .env
```

**Değiştirilmesi GEREKEN değerler:**

```env
# Güçlü bir secret key oluşturun:
# python3 -c "import secrets; print(secrets.token_urlsafe(50))"
DJANGO_SECRET_KEY=buraya-uzun-rastgele-key

DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=SUNUCU_IP_ADRESI,localhost

# Veritabanı şifresi
DB_PASSWORD=guclu-bir-sifre-buraya

# Deploy token (webhook için)
GIT_DEPLOY_TOKEN=gizli-deploy-token

# CSRF (alan adınız olunca ekleyin)
# CSRF_TRUSTED_ORIGINS=https://webtools.com
```

---

## 4. Docker ile Başlatma

```bash
# İlk build ve başlatma
docker compose up -d --build

# Logları takip edin
docker compose logs -f web

# Superuser oluşturun (admin paneli için)
docker compose exec web python manage.py createsuperuser
```

**İlk başlatmada otomatik olarak:**
- ✅ PostgreSQL veritabanı oluşturulacak
- ✅ Django migration'ları çalışacak
- ✅ Static dosyalar toplanacak
- ✅ Çeviriler derlenecek
- ✅ Gunicorn 3 worker ile başlatılacak

---

## 5. Sunucuya Erişim

Domain olmadan doğrudan IP ile erişebilirsiniz:

```
http://SUNUCU_IP_ADRESI/           → Ana sayfa
http://SUNUCU_IP_ADRESI/admin/     → Admin paneli
```

---

## 6. Admin Panelden Git Deploy

Admin paneline giriş yapın (`/admin/`) ve:

1. **Deploy > Deploy Logs** bölümüne gidin
2. Üstteki yeşil **"⬇️ Deploy Now"** butonuna tıklayın
3. Sistem otomatik olarak:
   - `git pull origin main` çalıştırır
   - `collectstatic` çalıştırır
   - `migrate` çalıştırır
   - Sonucu log olarak kaydeder

---

## 7. GitHub Webhook ile Otomatik Deploy

Git'e push yapınca otomatik deploy istiyorsanız:

### GitHub'da Webhook Ayarı:

1. GitHub repo → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL:** `http://SUNUCU_IP/deploy/webhook/`
3. **Content type:** `application/json`
4. **Secret:** `.env` dosyasındaki `GIT_DEPLOY_TOKEN` değeri
5. **Events:** sadece "Push" olayı

Artık `main` branch'e push yapınca sunucu otomatik güncellenir!

### Manuel test:
```bash
curl -X POST http://SUNUCU_IP/deploy/webhook/ \
     -H "X-Deploy-Token: GIT_DEPLOY_TOKEN_DEGERI"
```

---

## 8. Alan Adı Ekleme (Sonrası İçin)

Alan adınız olduğunda:

### a) `.env` dosyasını güncelleyin:
```env
DJANGO_ALLOWED_HOSTS=webtools.com,www.webtools.com,SUNUCU_IP
CSRF_TRUSTED_ORIGINS=https://webtools.com,https://www.webtools.com
```

### b) Nginx config'i güncelleyin:
```bash
nano nginx/default.conf
```
`server_name _;` satırını şu şekilde değiştirin:
```nginx
server_name webtools.com www.webtools.com;
```

### c) SSL (Let's Encrypt) ekleyin:
```bash
# Certbot kurulumu
sudo apt install certbot python3-certbot-nginx

# SSL sertifikası alın
sudo certbot --nginx -d webtools.com -d www.webtools.com

# Otomatik yenileme
sudo crontab -e
# Ekleyin: 0 3 * * * certbot renew --quiet
```

### d) Servisleri yeniden başlatın:
```bash
docker compose restart
```

---

## 9. Yararlı Komutlar

```bash
# Servisleri durdur
docker compose down

# Yeniden başlat
docker compose restart

# Logları gör
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f db

# Veritabanı yedeği
docker compose exec db pg_dump -U webtools webtools > backup.sql

# Yedeği geri yükle
cat backup.sql | docker compose exec -T db psql -U webtools webtools

# Django shell
docker compose exec web python manage.py shell

# Yeni superuser
docker compose exec web python manage.py createsuperuser

# Container'a giriş
docker compose exec web bash
```

---

## 10. Proje Yapısı

```
webtools/
├── docker-compose.yml     ← Docker servisleri
├── Dockerfile             ← Python image build
├── docker-entrypoint.sh   ← Başlangıç script'i
├── .env                   ← Ortam değişkenleri (git'e ekleme!)
├── .env.example           ← Örnek .env
├── nginx/
│   └── default.conf       ← Nginx reverse proxy config
├── requirements.txt       ← Python bağımlılıkları
├── apps/
│   ├── ads/               ← Reklam yönetimi
│   ├── deploy/            ← Git deploy sistemi
│   └── ...                ← Diğer araçlar
└── webtools/
    └── settings.py        ← Django ayarları (env-based)
```

---

## Güvenlik Notları

⚠️ **Yapılması gerekenler:**
- [ ] `.env` dosyasındaki `DJANGO_SECRET_KEY` değerini değiştirin
- [ ] `DB_PASSWORD` değerini güçlü bir şifre yapın
- [ ] `GIT_DEPLOY_TOKEN` benzersiz bir token belirleyin
- [ ] `DJANGO_DEBUG=False` olduğundan emin olun
- [ ] `.env` dosyasını asla git'e pushlamayın
- [ ] Firewall kurun (sadece 80, 443, 22 portları açık)
