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

## Lisans

Bu proje eğitim amaçlıdır ve akademik kullanım için tasarlanmıştır.