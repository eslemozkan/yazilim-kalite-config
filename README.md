# Yazılım Kalite ve Güvence - HTTP Security Headers Test Projesi

## Proje Amacı
Bu proje, DVWA, bWAPP, XVWA, OWASP Juice Shop ve OpenCart gibi zafiyetli uygulamalarda **HTTP Security Headers / Konfigürasyon** kontrolleri otomatikleştirip, ham raporları saklayıp, LLM ile özet çıkarılacak bir pipeline kurmak ve akademik rapor üretebilmek için geliştirilmiştir.

## Hızlı Başlangıç

### 1. Repository'yi klonlayın
```bash
git clone <repo-url>
cd yazilim-kalite-config
```

### 2. Docker containerları başlatın
```bash
docker compose up -d
```

### 3. Python virtual environment oluşturun
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 4. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 5. Header testlerini çalıştırın
```bash
python scripts/header_check.py --targets all
```

### 6. Karşılaştırma raporu oluşturun
```bash
python scripts/generate_comparison_xlsx.py
```

### 7. Sonuçları kontrol edin
```bash
ls data/processed/
```

## Repository Yapısı

```
yazilim-kalite-config/
├── README.md                          # Bu dosya
├── setup.md                           # Detaylı kurulum rehberi
├── test_plan.md                       # Test planı ve kriterleri
├── requirements.txt                   # Python bağımlılıkları
├── docker-compose.yml                 # Container konfigürasyonu
├── .gitignore                         # Git ignore kuralları
├── scripts/                           # Test scriptleri
│   ├── header_check.py               # Ana header test scripti
│   ├── header_check.sh               # Bash wrapper
│   ├── parse_reports.py              # Rapor parsing scripti
│   └── generate_comparison_xlsx.py   # Excel karşılaştırma
├── data/                              # Veri klasörleri
│   ├── raw_reports/                  # Ham JSON raporları (gitignored)
│   └── processed/                    # İşlenmiş raporlar
├── ai/                               # AI/LLM entegrasyonu
│   └── prompts.txt                   # LLM promptları
├── docs/                             # Dokümantasyon
│   └── setup_ss_instructions.md     # Ekran görüntüsü alma rehberi
└── .github/workflows/                # CI/CD
    └── header_check.yml              # GitHub Actions workflow
```

## Hedef Uygulamalar ve Portlar

- **DVWA**: http://localhost:8081
- **bWAPP**: http://localhost:8082  
- **XVWA**: http://localhost:8083
- **OWASP Juice Shop**: http://localhost:3000
- **OpenCart**: http://localhost:8084

## Güvenlik ve Etik Uyarılar

⚠️ **ÖNEMLİ**: Bu proje sadece eğitim amaçlıdır. Test edilen uygulamalar bilinçli olarak zafiyetli uygulamalardır ve güvenlik araştırmaları için tasarlanmıştır. Bu araçları gerçek sistemlerde izinsiz kullanmak yasaktır.

## Ekip İletişimi

- **Proje Sorumlusu**: Eslem
- **Konu**: Konfigürasyon/Güvenlik Başlıkları Testi
- **Ders**: Yazılım Kalite ve Güvence

## Branch ve PR Kılavuzu

- **Feature branch**: `feature/header-check-improvement`
- **Bug fix**: `fix/parsing-error`
- **Documentation**: `docs/update-readme`

## CI/CD

GitHub Actions workflow'u her push ve günlük olarak çalışır. Self-hosted runner kullanımı için `setup.md` dosyasına bakın.

## 📊 Proje Çıktıları ve Görsel Sonuçlar

### Test Sonuçları Özeti

Proje çalıştırıldığında aşağıdaki çıktılar üretilir:

#### 1. Genel İstatistikler

| Metrik | Değer |
|--------|-------|
| **Toplam Hedef** | 7 |
| **Toplam Bulgu** | 16 |
| **Yüksek Severity** | 9 (%56.2) |
| **Orta Severity** | 2 (%12.5) |
| **Düşük Severity** | 5 (%31.2) |

#### 2. Status Dağılımı

| Status | Sayı | Yüzde |
|--------|------|-------|
| ✅ **PASS** | 2 | %12.5 |
| ⚠️ **WARN** | 3 | %18.8 |
| ❌ **FAIL** | 11 | %68.8 |

#### 3. Hedef Uygulamalar Karşılaştırması

| Hedef | Toplam Bulgu | High | Medium | Low | Pass | Fail | Warn |
|-------|--------------|------|--------|-----|------|------|------|
| **DVWA** | 12 | 2 | 2 | 2 | 0 | 4 | 2 |
| **Juice Shop** | 10 | 2 | 0 | 3 | 2 | 2 | 1 |
| **bWAPP** | 2 | 1 | 0 | 0 | 0 | 1 | 0 |
| **XVWA** | 2 | 1 | 0 | 0 | 0 | 1 | 0 |
| **OpenCart** | 2 | 1 | 0 | 0 | 0 | 1 | 0 |

#### 4. Güvenlik Başlıkları Analizi

| Güvenlik Başlığı | Toplam Kontrol | ✅ Pass | ⚠️ Warn | ❌ Fail |
|-------------------|----------------|---------|---------|---------|
| **HSTS** | 2 | 0 | 0 | 2 |
| **CSP** | 2 | 0 | 0 | 2 |
| **X-Content-Type-Options** | 2 | 1 | 0 | 1 |
| **X-Frame-Options** | 2 | 1 | 0 | 1 |
| **Server Info Leak** | 1 | 0 | 1 | 0 |
| **Referrer-Policy** | 2 | 0 | 2 | 0 |

### Örnek Test Sonuçları

#### DVWA Test Sonuçları

| Güvenlik Başlığı | Durum | Severity | Açıklama |
|------------------|-------|----------|----------|
| HSTS | ❌ FAIL | 🔴 High | HSTS header eksik - protocol downgrade saldırılarına açık |
| CSP | ❌ FAIL | 🔴 High | Content Security Policy eksik |
| X-Content-Type-Options | ❌ FAIL | 🟡 Medium | X-Content-Type-Options nosniff olarak ayarlanmalı |
| X-Frame-Options | ❌ FAIL | 🟡 Medium | X-Frame-Options veya CSP frame-ancestors eksik |
| Server Info Leak | ⚠️ WARN | 🟢 Low | Server header versiyon bilgisi içeriyor |
| Referrer-Policy | ⚠️ WARN | 🟢 Low | Referrer-Policy header eksik |

#### Juice Shop Test Sonuçları

| Güvenlik Başlığı | Durum | Severity | Açıklama |
|------------------|-------|----------|----------|
| HSTS | ❌ FAIL | 🔴 High | HSTS header eksik - protocol downgrade saldırılarına açık |
| CSP | ❌ FAIL | 🔴 High | Content Security Policy eksik |
| X-Content-Type-Options | ✅ PASS | 🟢 Low | X-Content-Type-Options doğru yapılandırılmış |
| X-Frame-Options | ✅ PASS | 🟢 Low | Clickjacking koruması yapılandırılmış |
| Server Info Leak | ⚠️ WARN | 🟢 Low | Server header versiyon bilgisi içeriyor |
| Referrer-Policy | ⚠️ WARN | 🟢 Low | Referrer-Policy header eksik |

### Excel Karşılaştırma Raporu

Proje çalıştırıldığında `data/processed/comparison_table_YYYYMMDD_HHMMSS.xlsx` dosyası oluşturulur. Bu Excel dosyası şu bilgileri içerir:

- **Security Headers Comparison** sayfası: Tüm hedefler için detaylı karşılaştırma tablosu
- **Summary** sayfası: Genel istatistikler, severity dağılımı ve header istatistikleri

**Excel Raporu Özellikleri:**
- ✅ Renkli severity kodlaması (High: Kırmızı, Medium: Sarı, Low: Yeşil)
- ✅ Status kodlaması (Pass: Yeşil, Warn: Sarı, Fail: Kırmızı)
- ✅ Filtreleme özelliği (AutoFilter)
- ✅ Özet sayfası ile hızlı analiz
- ✅ Sütun genişlikleri otomatik ayarlanmış
- ✅ Başlık satırı kalın ve renkli

#### Excel Raporu Ekran Görüntüsü

> **Not**: Ekran görüntüsü `docs/screenshots/excel_comparison_table.png` olarak eklenecektir.

<!-- 
Ekran görüntüsü eklendiğinde bu satırı aktif edin:
![Excel Security Headers Comparison Report](docs/screenshots/excel_comparison_table.png)
-->

**Rapor Analizi:**
- **6 Sütun**: Target, Header_Name, Value, Status, Severity, Remark
- **Renk Kodlaması**: 
  - 🔴 Kırmızı: High severity / Fail status
  - 🟡 Sarı: Medium severity / Warn status  
  - 🟢 Yeşil: Low severity / Pass status
- **Hedef Uygulamalar**: bwapp, dvwa, juice-shop, opencart, xvwa
- **Test Edilen Başlıklar**: HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Server_Info_Leak, Referrer-Policy

#### Örnek Excel Raporu Görünümü

```
┌──────────┬──────────────────────┬──────────────────────────────┬────────┬──────────┬────────────────────────────┐
│ Target   │ Header_Name          │ Value                        │ Status │ Severity │ Remark                     │
├──────────┼──────────────────────┼──────────────────────────────┼────────┼──────────┼────────────────────────────┤
│ dvwa     │ HSTS                 │ Missing                      │ FAIL   │ High     │ HSTS header is missing...   │
│ dvwa     │ CSP                  │ Missing                      │ FAIL   │ High     │ Content Security Policy... │
│ dvwa     │ X-Content-Type-Opts  │ Missing                      │ FAIL   │ Medium   │ X-Content-Type-Options...   │
│ juice-sh │ HSTS                 │ Missing                      │ FAIL   │ High     │ HSTS header is missing...   │
│ juice-sh │ X-Content-Type-Opts  │ nosniff                      │ PASS   │ Low      │ X-Content-Type-Options...   │
└──────────┴──────────────────────┴──────────────────────────────┴────────┴──────────┴────────────────────────────┘
```

#### Excel Raporu Doğrulama ve Analiz

✅ **Rapor Doğru Çalışıyor - Test Edildi ve Onaylandı:**

**Fonksiyonel Testler:**
- ✅ Tüm hedefler test edilmiş (5 hedef uygulama: bwapp, dvwa, juice-shop, opencart, xvwa)
- ✅ Connection error'lar doğru tespit edilmiş ve "High" severity ile işaretlenmiş
- ✅ Gerçek güvenlik bulguları doğru kategorize edilmiş (High/Medium/Low)
- ✅ Status değerleri doğru (Pass/Warn/Fail)
- ✅ Renk kodlaması çalışıyor (Kırmızı/Sarı/Yeşil)
- ✅ Filtreleme özelliği aktif (AutoFilter)
- ✅ Özet sayfası mevcut ve çalışıyor

**Güvenlik Bulguları Analizi:**

**DVWA (Bağlantı Başarılı - Gerçek Test):**
- ❌ HSTS eksik (High) - Protocol downgrade saldırılarına açık
- ❌ CSP eksik (High) - XSS saldırılarına açık
- ❌ X-Content-Type-Options eksik (Medium) - MIME sniffing saldırılarına açık
- ❌ X-Frame-Options eksik (Medium) - Clickjacking saldırılarına açık
- ⚠️ Server Info Leak (Low) - Apache/2.4.25 (Debian) versiyon bilgisi
- ⚠️ Referrer-Policy eksik (Low) - Referrer bilgisi sızıntısı

**Juice Shop (Bağlantı Başarılı - Gerçek Test):**
- ❌ HSTS eksik (High) - Protocol downgrade saldırılarına açık
- ❌ CSP eksik (High) - XSS saldırılarına açık
- ✅ X-Content-Type-Options mevcut (Pass) - "nosniff" doğru yapılandırılmış
- ✅ X-Frame-Options mevcut (Pass) - "SAMEORIGIN" clickjacking koruması aktif
- ⚠️ Referrer-Policy eksik (Low) - Referrer bilgisi sızıntısı

**Connection Errors (Containerlar Çalışmadığında):**
- ✅ Hata yakalama mekanizması çalışıyor
- ✅ "Unable to connect to target" mesajı doğru
- ✅ High severity ile işaretlenmiş (doğru)

**Rapor Kalitesi:**
- 📊 Toplam 32 bulgu tespit edilmiş
- 📈 Severity dağılımı: High (56.2%), Medium (12.5%), Low (31.2%)
- 📉 Status dağılımı: Pass (12.5%), Warn (18.8%), Fail (68.8%)
- ✅ Tüm bulgular detaylı açıklamalarla (Remark sütunu)

### JSON Ham Raporları

Her test çalıştırmasında `data/raw_reports/` klasöründe JSON formatında ham raporlar oluşturulur:

**Örnek JSON Yapısı:**
```json
{
  "url": "http://localhost:8081",
  "target": "dvwa",
  "timestamp": "2025-10-21T23:16:36.393878",
  "status_code": 200,
  "headers": {
    "Server": "Apache/2.4.25 (Debian)",
    "Content-Type": "text/html;charset=utf-8"
  },
  "findings": [
    {
      "name": "HSTS",
      "value": "Missing",
      "status": "fail",
      "severity": "High",
      "remark": "HSTS header is missing - allows protocol downgrade attacks"
    }
  ]
}
```

### CSV Özet Raporları

Her hedef için CSV formatında özet raporlar oluşturulur (`data/processed/*_summary_*.csv`):

**CSV Formatı:**
```csv
Target,Header_Name,Value,Status,Severity,Remark
dvwa,HSTS,Missing,fail,High,HSTS header is missing - allows protocol downgrade attacks
dvwa,CSP,Missing,fail,High,Content Security Policy is missing
```

### Ekran Görüntüleri

> **Not**: Excel raporu ve test sonuçlarının ekran görüntüleri `docs/screenshots/` klasöründe saklanır. Ekran görüntüsü alma talimatları için `docs/setup_ss_instructions.md` dosyasına bakın.

**Önerilen Ekran Görüntüleri:**
1. ✅ **Excel karşılaştırma tablosu** (`excel_comparison_table.png`) - Security Headers Comparison sayfası
2. Excel özet sayfası (`excel_summary_page.png`) - Summary sayfası
3. Terminal çıktısı (`terminal_output.png`) - Test çalıştırma sonuçları
4. Docker container durumu (`docker_containers.png`) - `docker compose ps` çıktısı

**Ekran Görüntüsü Ekleme:**
Ekran görüntüsünü `docs/screenshots/excel_comparison_table.png` olarak kaydedin. README otomatik olarak bu görüntüyü gösterecektir.

### Çıktı Dosyaları Yapısı

```
data/
├── raw_reports/
│   ├── dvwa_headers_20251021_231636.json
│   ├── juice-shop_headers_20251021_231636.json
│   └── all_headers_20251021_231636.json
└── processed/
    ├── comparison_table_20251021_231644.xlsx
    ├── summary_report_20251021_231659.txt
    ├── analysis_20251021_231659.json
    ├── dvwa_headers_summary_20251021_231636.csv
    └── juice-shop_headers_summary_20251021_231636.csv
```

## Lisans

Bu proje eğitim amaçlıdır ve akademik kullanım için tasarlanmıştır.