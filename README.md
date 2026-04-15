# 🚀 412hi Loader

<div align="center">
  <img src="https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6">
  <img src="https://img.shields.io/badge/KeyAuth-5865F2?style=for-the-badge&logo=key&logoColor=white" alt="KeyAuth">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License MIT">
</div>

<br>

**412hi Loader**, PyQt6 ile geliştirilmiş, modern ve kullanıcı dostu bir lisans yönetim panelidir. KeyAuth lisanslama sistemi ile tam entegre çalışır. Çok dilli desteği (Türkçe & İngilizce), şık arayüzü ve kolay kullanımı ile öne çıkar.

---

## ✨ Özellikler

- 🔐 **KeyAuth Entegrasyonu** – Lisans anahtarlarını KeyAuth API üzerinden doğrular.
- 🌍 **Çok Dilli Destek** – Türkçe ve İngilizce arayüz seçeneği.
- 🎨 **Modern Arayüz** – PyQt6 ile özel olarak tasarlanmış, karanlık tema ve animasyonlu bileşenler.
- 📋 **Duyuru Paneli** – Güncel duyuruları gösterir.
- 🛒 **Ürünler Sayfası** – Ürünlerin listelendiği sade ve şık kartlar.
- 👤 **Hesap Durumu** – Lisans süresi, kalan gün, plan tipi ve dahil özellikleri gösterir.
- 🖱️ **Frameless Pencere** – Başlık çubuğu olmadan sürüklenebilir pencere.
- ⚡ **Demo Mod** – Test için ön tanımlı demo anahtar (`412HI-DEMO*2026`).

---

## 📸 Ekran Görüntüleri

| Dil Seçimi | Lisans Doğrulama |
|:---:|:---:|
| <img width="775" alt="Dil Seçimi" src="https://github.com/user-attachments/assets/e46c7a59-b4f7-45f0-9710-c6b2897f65a1"> | <img width="773" alt="Lisans Doğrulama" src="https://github.com/user-attachments/assets/28e6e458-ac84-408b-bea6-ec64e4b7b570"> 


| Duyurular | Hesap Durumu |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/e5a097a3-f75c-4c1e-9615-95ed3f637729" width="400"> | <img src="https://github.com/user-attachments/assets/9f8bb65e-eedb-444a-bdbe-3bfe8bda3389" width="400"> |

---

## 🛠️ Kullanılan Teknolojiler

- **Python 3.9+**
- **PyQt6** – Masaüstü arayüzü için.
- **KeyAuth API** – Lisanslama ve kullanıcı yönetimi.
- **Requests** – HTTP istekleri (KeyAuth kütüphanesi bağımlılığı).

---

## 🚦 Başlangıç

### Gereksinimler

- Python 3.9 veya üstü
- `pip` paket yöneticisi

### Kurulum

1. **Depoyu klonlayın:**
   
   git clone https://github.com/kullaniciadi/412hi-loader.git
   cd 412hi-loader
   
3. **Gerekli kütüphaneleri yükleyin:
   
    pip install -r requirements.txt

4. KeyAuth Kütüphanesini Ekleyin:

   KeyAuth'un Python kütüphanesini (keyauth.py) resmi GitHub sayfasından indirin.

   İndirdiğiniz keyauth.py dosyasını proje ana dizinine (main.py ile aynı klasöre) kopyalayın.

5. KeyAuth Bilgilerinizi Girin:

   main.py dosyasının başındaki KeyAuth yapılandırmasını kendi panel bilgilerinizle güncelleyin:

   
   keyauthapp = api(
    name = "UYGULAMA_ADINIZ",   # KeyAuth panelindeki Application Name \
    ownerid = "OWNER_ID",       # KeyAuth panelindeki Owner ID \
    version = "1.0",            # Versiyon \
    hash_to_check = None \
)
 7. Uygulamayı Çalıştırın:
   python main.py

🧪 Test için Demo Anahtar = 412HI-DEMO*2026
  
