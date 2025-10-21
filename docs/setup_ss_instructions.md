# Ekran Görüntüsü Alma Rehberi
# HTTP Security Headers Test Projesi

## Gerekli Ekran Görüntüleri

### 1. Docker Container Durumu
- **Dosya Adı**: `docker_containers_running.png`
- **Açıklama**: Tüm containerların çalışır durumda olduğunu gösteren ekran görüntüsü
- **Komut**: `docker compose ps`
- **Beklenen Görünüm**: 5 container (dvwa, bwapp, xvwa, juice-shop, opencart) "Up" durumunda

### 2. Test Sonuçları
- **Dosya Adı**: `header_test_results.png`
- **Açıklama**: Header test sonuçlarının terminal çıktısı
- **Komut**: `python scripts/header_check.py --targets all`
- **Beklenen Görünüm**: Test sonuçları, bulgular ve rapor dosyaları

### 3. Excel Karşılaştırma Raporu
- **Dosya Adı**: `excel_comparison_report.png`
- **Açıklama**: Excel karşılaştırma tablosunun açık hali
- **Dosya**: `data/processed/comparison_table_YYYYMMDD_HHMMSS.xlsx`
- **Beklenen Görünüm**: Renkli karşılaştırma tablosu, özet sayfası

### 4. Güvenlik Bulguları Özeti
- **Dosya Adı**: `security_findings_summary.png`
- **Açıklama**: Güvenlik bulgularının özet raporu
- **Dosya**: `data/processed/summary_report_YYYYMMDD_HHMMSS.txt`
- **Beklenen Görünüm**: Severity dağılımı, hedef özetleri, header istatistikleri

### 5. JSON Ham Raporları
- **Dosya Adı**: `json_raw_reports.png`
- **Açıklama**: Ham JSON raporlarının içeriği
- **Dosya**: `data/raw_reports/` klasörü
- **Beklenen Görünüm**: JSON dosyaları, timestamp'li dosya adları

## Ekran Görüntüsü Alma Adımları

### Windows

#### Yöntem 1: Snipping Tool
1. `Windows + Shift + S` tuşlarına basın
2. Ekran görüntüsü almak istediğiniz alanı seçin
3. Görüntüyü `docs/screenshots/` klasörüne kaydedin
4. Dosya adını açıklayıcı yapın

#### Yöntem 2: Print Screen
1. `Print Screen` tuşuna basın
2. Paint uygulamasını açın
3. `Ctrl + V` ile yapıştırın
4. Görüntüyü kaydedin

#### Yöntem 3: PowerShell
```powershell
# Ekran görüntüsü alma scripti
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$Screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$Width = $Screen.Width
$Height = $Screen.Height
$Left = $Screen.Left
$Top = $Screen.Top

$bitmap = New-Object System.Drawing.Bitmap $Width, $Height
$graphic = [System.Drawing.Graphics]::FromImage($bitmap)
$graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$filename = "docs\screenshots\screenshot_$timestamp.png"
$bitmap.Save($filename)
```

### macOS

#### Yöntem 1: Klavye Kısayolları
1. `Cmd + Shift + 3`: Tam ekran
2. `Cmd + Shift + 4`: Kısmi ekran
3. `Cmd + Shift + 5`: Ekran kaydı aracı

#### Yöntem 2: Terminal
```bash
# Ekran görüntüsü alma
screencapture -T 1 screenshot.png

# Belirli alan seçimi
screencapture -i screenshot.png

# Timestamp ile
timestamp=$(date +"%Y%m%d_%H%M%S")
screencapture "docs/screenshots/screenshot_${timestamp}.png"
```

### Linux

#### Yöntem 1: GNOME Screenshot
```bash
# GNOME Screenshot
gnome-screenshot -f screenshot.png

# Belirli alan
gnome-screenshot -a -f screenshot.png

# Timestamp ile
timestamp=$(date +"%Y%m%d_%H%M%S")
gnome-screenshot -f "docs/screenshots/screenshot_${timestamp}.png"
```

#### Yöntem 2: scrot
```bash
# scrot kurulumu
sudo apt install scrot

# Ekran görüntüsü alma
scrot screenshot.png

# Belirli alan
scrot -s screenshot.png

# Timestamp ile
scrot "docs/screenshots/screenshot_%Y%m%d_%H%M%S.png"
```

## Dosya Organizasyonu

### Klasör Yapısı
```
docs/
├── screenshots/
│   ├── docker_containers_running.png
│   ├── header_test_results.png
│   ├── excel_comparison_report.png
│   ├── security_findings_summary.png
│   └── json_raw_reports.png
└── setup_ss_instructions.md
```

### Dosya Adlandırma Kuralları
- **Format**: `{açıklama}_{timestamp}.png`
- **Örnek**: `docker_containers_running_20231201_120000.png`
- **Timestamp**: `YYYYMMDD_HHMMSS`
- **Açıklama**: İngilizce, kısa, açıklayıcı

## Ekran Görüntüsü Kalitesi

### Teknik Gereksinimler
- **Çözünürlük**: Minimum 1920x1080
- **Format**: PNG (kalite için)
- **Renk Derinliği**: 24-bit
- **Sıkıştırma**: Kayıpsız

### Görsel Kalite
- **Netlik**: Metin okunabilir olmalı
- **Kontrast**: Yeterli kontrast
- **Boyut**: Dosya boyutu makul (1-5MB)
- **Format**: PNG veya JPG

## Test Senaryoları

### Senaryo 1: Docker Container Kontrolü
1. Terminal açın
2. `docker compose ps` komutunu çalıştırın
3. Tüm containerların "Up" durumunda olduğunu kontrol edin
4. Ekran görüntüsü alın
5. `docs/screenshots/docker_containers_running.png` olarak kaydedin

### Senaryo 2: Header Test Çalıştırma
1. Terminal açın
2. `python scripts/header_check.py --targets all` komutunu çalıştırın
3. Test sonuçlarını bekleyin
4. Ekran görüntüsü alın
5. `docs/screenshots/header_test_results.png` olarak kaydedin

### Senaryo 3: Excel Rapor Açma
1. Excel dosyasını açın
2. Karşılaştırma tablosunu gösterin
3. Özet sayfasını gösterin
4. Ekran görüntüsü alın
5. `docs/screenshots/excel_comparison_report.png` olarak kaydedin

### Senaryo 4: Güvenlik Bulguları
1. Özet raporu açın
2. Severity dağılımını gösterin
3. Hedef özetlerini gösterin
4. Ekran görüntüsü alın
5. `docs/screenshots/security_findings_summary.png` olarak kaydedin

## Sorun Giderme

### Ekran Görüntüsü Alınamıyor
```bash
# Linux'ta izin sorunu
sudo chmod +x /usr/bin/gnome-screenshot

# macOS'ta izin sorunu
System Preferences > Security & Privacy > Privacy > Screen Recording
```

### Dosya Kaydedilemiyor
```bash
# Klasör oluştur
mkdir -p docs/screenshots

# İzin ver
chmod 755 docs/screenshots
```

### Görüntü Kalitesi Düşük
- Çözünürlüğü artırın
- PNG formatını kullanın
- Sıkıştırmayı azaltın

## Yükleme Talimatları

### GitHub'a Yükleme
1. Ekran görüntülerini `docs/screenshots/` klasörüne kaydedin
2. Git ile commit yapın:
```bash
git add docs/screenshots/
git commit -m "Add screenshots for security headers test"
git push origin main
```

### Alternatif Yükleme
1. Ekran görüntülerini ZIP dosyası olarak sıkıştırın
2. E-posta ile gönderin
3. Cloud storage'a yükleyin
4. Paylaşım linkini gönderin

## Notlar

- Tüm ekran görüntüleri eğitim amaçlıdır
- Kişisel bilgileri gizleyin
- Dosya boyutlarını kontrol edin
- Timestamp'leri doğru kullanın
- Açıklayıcı dosya adları kullanın
