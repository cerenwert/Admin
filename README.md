# Proje Durumu

## Repository Bilgisi
- **Repo linki:** https://github.com/<org>/<repo>
- **Son commit:** 2d6793277bac12cc7a24f0bce143c2c867046343  docs: add setup, run, errors & reproduction to README
- **Son commit saati (Europe/Istanbul): 2025-09-05 13:29

## Kurulum
- Python 3.13 ve PowerShell ile test edildi.
- Windows'ta venv aktivasyonu için gerekirse geçici izin:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

\\\powershell
cd C:\Users\victus\OneDrive\Masaüstü\admin
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt   # varsa
pip install celery djangorestframework
\\\

## Çalıştırma
\\\powershell
cd C:\Users\victus\OneDrive\Masaüstü\admin
.\.venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
\\\

- Admin: http://127.0.0.1:8000/admin/
- Geçici health/metrics: http://127.0.0.1:8000/metrics/summary/

## Neden /admin/metrics/summary/ (ve public /metrics/summary/)?
- Hızlı sağlık/durum kontrolü, operasyonel görünürlük, hata ayıklama.
- İlerde Prometheus/Grafana gibi araçlara veri çıkarmak için sabit uç.
- Canlıda sadece yetkili kullanıcılara açık olacak (şimdilik public uç test için açık).

## Karşılaşılan Hatalar ve Tekrar Üretme

**1) Eksik bağımlılık (Celery)**
- Hata: ModuleNotFoundError: No module named 'celery' (config/celery.py)
- Üretme: Celery kurulmadan Django komutları.
- Çözüm: pip install celery (tercihen pip install -r requirements.txt).

**2) PowerShell script izni (venv)**
- Hata: Activate.ps1 cannot be loaded because running scripts is disabled...
- Üretme: Execution Policy düşükken venv aktivasyonu.
- Çözüm: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass veya CurrentUser/RemoteSigned.

**3) Sunucuya bağlanılamıyor**
- Hata: Invoke-WebRequest : Uzak sunucuya bağlanılamıyor / TcpTestSucceeded: False
- Üretme: Runserver kapalıyken istek atmak.
- Çözüm: python manage.py runserver 127.0.0.1:8000 açık pencere, testler ikinci pencereden.

**4) Kök URL 404**
- Log: Not Found: / ve "GET / HTTP/1.1" 404
- Üretme: / için view yokken anasayfa.
- Çözüm: Kök URLyi admine yönlendirme veya basit home view.

**5) Admin altında metrik erişimi login istiyor**
- Davranış: /admin/metrics/summary/ logine yönlendirir.
- Üretme: Admin path + staff gerekli.
- Çözüm: Test için /metrics/summary/ public; canlıda tekrar staff-only.

## Şu Anki Durum
- Venv aktif, bağımlılıklar (Celery + DRF) yüklü.
- Geliştirme sunucusu lokal çalışıyor.
- contracts içinde metrics_summary mevcut (public path).
- DRF ile API uçları (models/offers) için zemin hazır.


## 5 Eylül 2025 – Yeni Hatalar ve Çözümler

**6) Admin panelinde `pdf_generated_at` alanı bulunamadı**
- Hata: `(admin.E108) The value of 'list_display[6]' refers to 'pdf_generated_at'`
- Üretme: Contract modelinde alan tanımlı değilken admin list_display içinde kullanmak.
- Çözüm: `Contract` modeline `pdf_generated_at` alanı eklendi, migration yapıldı.

**7) Eksik `contracts.utils` modülü**
- Hata: `ModuleNotFoundError: No module named 'contracts.utils'`
- Üretme: utils.py oluşturulmamışken import etmek.
- Çözüm: `contracts/utils.py` dosyası eklendi, HTML→PDF fonksiyonları tanımlandı.

**8) `reportlab` / `xhtml2pdf` sürüm çakışması**
- Hata: `ResolutionImpossible` hatası, sürümler uyumsuz.
- Üretme: `reportlab==3.6.13` ile `xhtml2pdf==0.2.15` aynı anda kurulmaya çalışıldığında.
- Çözüm: `pip install "reportlab>=4.0.4,<4.1" "xhtml2pdf==0.2.15"` ile uyumlu kurulum yapıldı.

**9) WeasyPrint kütüphane hatası**
- Hata: `OSError: cannot load library 'gobject-2.0-0'`
- Üretme: Windows’ta gerekli GTK kütüphaneleri olmadan WeasyPrint çalıştırıldığında.
- Çözüm: WeasyPrint yerine `xhtml2pdf` kullanılarak PDF üretim sağlandı.

**10) `remind_expiring_contracts` komutunda eksik import**
- Hata: `ModuleNotFoundError: No module named 'contracts.reminders'`
- Üretme: reminders.py olmadan komutu çalıştırmak.
- Çözüm: `contracts/reminders.py` eklendi, komut başarıyla çalıştı.

## Şu Anki Son Durum – 5 Eylül 2025

- Teklif onaylandığında otomatik sözleşme oluşturma çalışıyor.  
- Teklif ve sözleşmeler için PDF üretim altyapısı hazır, HTML şablon + CSS üzerinden PDF çıktısı alınabiliyor.  
- Admin paneline sözleşme alanları (kalan gün, auto_renew, hizmet adı vb.) eklendi.  
- Hatırlatma ve yenileme için komutlar (`remind_expiring_contracts`, `update_contract_statuses`, `propose_renewals`) başarıyla çalışıyor.  
- “Hatırlatmaları Çalıştır” butonu admin panelinde mevcut.  
- E-posta altyapısı şu anda **console backend** ile test modunda; SMTP ayarı eklenirse gerçek müşterilere gönderilebilecek.  
- Celery/Redis kurulumu yapılmadı, fakat Windows Task Scheduler ile komutlar zamanlanarak çalıştırılabilecek.  
- GitHub’a tüm değişiklikler aktarıldı (branch: `main`), repo yapısı sadeleştirildi.  

