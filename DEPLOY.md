# 🚀 WebTools — Sıfırdan Kurulum Kılavuzu (Docker Nginx + Admin SSL)

Bu kılavuz, tertemiz (sıfırlanmış) bir Ubuntu sunucuya projenin nasıl kurulacağını ve tek tıkla SSL alınacağını anlatır.

---

## 1. Sunucu Hazırlığı ve Projeyi İndirme

Sunucunuza SSH ile bağlanın ve şu komutları sırasıyla çalıştırın:

```bash
# Gerekli klasörü oluşturup içine girelim
sudo mkdir -p /opt/webtools
sudo chown -R $USER:$USER /opt/webtools
cd /opt/webtools

# Projeyi GitHub'dan indirelim
git clone https://github.com/MuhammeddKaya/webtools.git .
```

Eğer sunucunuzda Docker yüklü değilse, tek komutla yükleyin:
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# (Docker yüklendikten sonra komut satırından çıkıp tekrar SSH ile bağlanmanız gerekebilir)
```

---

## 2. Ortam Değişkenlerini (Ayarları) Yapılandırma

Projeyi çalıştırmadan önce güvenlik ayarlarını (şifreler vs.) belirlemeliyiz:

```bash
cp .env.example .env
nano .env
```

Açılan dosyada şu üç değeri kendi bilgilerinize göre doldurun:
```env
# Güçlü, rastgele bir şifre yazın
DJANGO_SECRET_KEY=rastgele-uzun-sifre-yaz

# Buraya sadece ve sadece sunucunuzun IP aresini yazın! (Örn: 77.42.87.77)
DJANGO_ALLOWED_HOSTS=SUNUCU_IP_ADRESI_BURAYA

# Veritabanı şifreniz
DB_PASSWORD=guclu-bir-sifre
```
*Kaydetmek için: Ctrl+O, Enter, Ctrl+X*

---

## 3. Sistemi Başlatma (İlk Kurulum)

Tüm hizmetleri (Veritabanı, Django, Nginx) arka planda başlatalım:

```bash
docker compose up -d --build
```
İşlem bittiğinde (hepsi `Started` olduğunda), admin paneline girebilmek için yönetici hesabınızı oluşturun:
```bash
docker compose exec web python manage.py createsuperuser
```
(Kullanıcı adı, e-mail ve şifre belirleyin).

---

## 4. Alan Adı Ekleme ve Otomatik SSL (Yeşil Kilit) Kurulumu

Artık komut satırıyla işiniz bitti! 

1. Tarayıcınızı açın ve sunucunuzun IP adresi üzerinden admin paneline girin:
   👉 `http://SUNUCU_IP_ADRESI/admin/`
2. Oluşturduğunuz superuser (yönetici) hesabıyla giriş yapın.
3. Ana sayfada **Domain Settings -> Custom Domains** menüsüne tıklayın.
4. Sağ üstten "ADD CUSTOM DOMAIN" butonuna tıklayıp sahip olduğunuz alan adını girin (Örn: `muhamedkaya.com.tr`).
5. Kaydettikten sonra, listede o alan adının sol tarafındaki kutucuğu (checkbox) işaretleyin.
6. Sol üstteki **Açılır Menüye (Action)** tıklayın ve listeden şunu seçin:
   👉 **"Seçili Alan Adlarına SSL (Yeşil Kilit) Kur"**
7. Hemen yanındaki **Go (Git)** butonuna basın!

Sistem saniyeler içinde Let's Encrypt'e bağlanacak, sertifikaları çekecek, Nginx ayarlarını baştan yazacak ve Nginx'i otomatik olarak yeniden başlatacaktır. Ekrandaki yeşil başarı mesajını gördükten sonra, yeni bir sekmede `https://muhamedkaya.com.tr` yazarak sitenize giriş yapabilirsiniz! 🎉

> Not: Bu sistemi kullanabilmeniz için alan adınızın (DNS) A kayıtlarının sunucunuzun IP adresine en az 1-2 saat önceden yönlendirilmiş olması gerekmektedir, aksi halde Let's Encrypt hata verir.
