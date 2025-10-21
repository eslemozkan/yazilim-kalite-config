# Kurulum Rehberi - HTTP Security Headers Test Projesi

## Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **RAM**: 8GB (16GB önerilen)
- **Disk**: 10GB boş alan
- **CPU**: 4 çekirdek (8 çekirdek önerilen)

### Yazılım Gereksinimleri
- **Docker**: 20.10+ ve Docker Compose 2.0+
- **Python**: 3.9+ (3.11 önerilen)
- **Git**: 2.30+
- **Node.js**: 16+ (opsiyonel, geliştirme için)

## Adım Adım Kurulum

### 1. Docker Kurulumu

#### Windows
```powershell
# Docker Desktop'ı indirin ve kurun
# https://www.docker.com/products/docker-desktop/
# Kurulum sonrası bilgisayarı yeniden başlatın

# Docker'ın çalıştığını kontrol edin
docker --version
docker compose version
```

#### macOS
```bash
# Homebrew ile kurulum
brew install --cask docker

# Veya Docker Desktop'ı manuel indirin
# https://www.docker.com/products/docker-desktop/
```

#### Ubuntu/Linux
```bash
# Docker'ı kaldırın (varsa)
sudo apt-get remove docker docker-engine docker.io containerd runc

# Gerekli paketleri yükleyin
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Docker'ın resmi GPG anahtarını ekleyin
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Repository'yi ekleyin
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker'ı yükleyin
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Docker Compose'u yükleyin
sudo apt-get install docker-compose-plugin

# Docker servisini başlatın
sudo systemctl start docker
sudo systemctl enable docker

# Kullanıcıyı docker grubuna ekleyin
sudo usermod -aG docker $USER
# Yeni oturum açın veya şu komutu çalıştırın:
newgrp docker
```

### 2. Python Kurulumu

#### Windows
```powershell
# Python'u indirin ve kurun
# https://www.python.org/downloads/
# "Add Python to PATH" seçeneğini işaretleyin

# Kurulumu kontrol edin
python --version
pip --version
```

#### macOS
```bash
# Homebrew ile
brew install python@3.11

# Veya pyenv ile
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Ubuntu/Linux
```bash
# Python 3.11 yükleyin
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip

# Alternatif olarak deadsnakes PPA kullanın
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

### 3. Proje Kurulumu

```bash
# Repository'yi klonlayın
git clone <repo-url>
cd yazilim-kalite-config

# Python virtual environment oluşturun
python3 -m venv .venv

# Virtual environment'ı aktifleştirin
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Bağımlılıkları yükleyin
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Docker Containerları Başlatma

```bash
# Containerları başlatın
docker compose up -d

# Containerların çalıştığını kontrol edin
docker compose ps

# Logları kontrol edin
docker compose logs
```

### 5. Test Çalıştırma

```bash
# Header testlerini çalıştırın
python scripts/header_check.py --targets all

# Karşılaştırma raporu oluşturun
python scripts/generate_comparison_xlsx.py

# Sonuçları kontrol edin
ls data/processed/
```

## VSCode DevContainer Kurulumu (Opsiyonel)

### .devcontainer/devcontainer.json
```json
{
    "name": "Security Headers Test",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.11",
    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {}
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.pylint",
                "ms-vscode.vscode-json"
            ]
        }
    },
    "postCreateCommand": "pip install -r requirements.txt",
    "forwardPorts": [8081, 8082, 8083, 3000, 8084],
    "portsAttributes": {
        "8081": {
            "label": "DVWA",
            "onAutoForward": "notify"
        },
        "8082": {
            "label": "bWAPP",
            "onAutoForward": "notify"
        },
        "8083": {
            "label": "XVWA",
            "onAutoForward": "notify"
        },
        "3000": {
            "label": "Juice Shop",
            "onAutoForward": "notify"
        },
        "8084": {
            "label": "OpenCart",
            "onAutoForward": "notify"
        }
    }
}
```

## Ekran Görüntüsü Alma Rehberi

### Gerekli Ekran Görüntüleri

1. **Docker Container Durumu**
   - `docker compose ps` çıktısı
   - Container logları

2. **Test Sonuçları**
   - JSON raporları
   - Excel karşılaştırma tablosu
   - Özet raporları

3. **Güvenlik Bulguları**
   - High severity bulgular
   - Medium severity bulgular
   - Header eksiklikleri

### Ekran Görüntüsü Alma Adımları

#### Windows
```powershell
# Ekran görüntüsü alma
# Windows + Shift + S (kısmi ekran görüntüsü)
# Print Screen (tam ekran)

# PowerShell ile otomatik
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
$bitmap.Save("screenshot.png")
```

#### macOS
```bash
# Ekran görüntüsü alma
# Cmd + Shift + 3 (tam ekran)
# Cmd + Shift + 4 (kısmi ekran)

# Terminal ile
screencapture screenshot.png
```

#### Linux
```bash
# Ekran görüntüsü alma
# Print Screen tuşu
# veya

# scrot ile
sudo apt install scrot
scrot screenshot.png

# gnome-screenshot ile
gnome-screenshot -f screenshot.png
```

### Ekran Görüntüsü Formatı

- **Dosya Adı**: `screenshot_YYYYMMDD_HHMMSS.png`
- **Çözünürlük**: Minimum 1920x1080
- **Format**: PNG (kalite için)
- **Konum**: `docs/screenshots/` klasörü

### Yükleme Talimatları

1. Ekran görüntülerini `docs/screenshots/` klasörüne kaydedin
2. Dosya adlarını açıklayıcı yapın:
   - `docker_containers_running.png`
   - `header_test_results.png`
   - `excel_comparison_report.png`
   - `security_findings_summary.png`

## Sorun Giderme

### Docker Sorunları

```bash
# Docker servisini yeniden başlatın
sudo systemctl restart docker

# Containerları temizleyin
docker compose down
docker system prune -a

# Yeniden başlatın
docker compose up -d
```

### Python Sorunları

```bash
# Virtual environment'ı yeniden oluşturun
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Port Çakışmaları

```bash
# Port kullanımını kontrol edin
netstat -tulpn | grep :8081
netstat -tulpn | grep :8082
netstat -tulpn | grep :8083
netstat -tulpn | grep :3000
netstat -tulpn | grep :8084

# Çakışan servisleri durdurun
sudo systemctl stop apache2  # Apache varsa
sudo systemctl stop nginx    # Nginx varsa
```

### Log Kontrolü

```bash
# Container logları
docker compose logs dvwa
docker compose logs bwapp
docker compose logs xvwa
docker compose logs juice-shop
docker compose logs opencart

# Test logları
tail -f data/raw_reports/errors.log
```

## Performans Optimizasyonu

### Docker Optimizasyonu
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  dvwa:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Python Optimizasyonu
```bash
# Virtual environment'ı optimize edin
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

## Güvenlik Notları

⚠️ **ÖNEMLİ UYARILAR**:

1. **İzolasyon**: Bu proje sadece eğitim amaçlıdır
2. **Ağ Güvenliği**: Containerları production ağında çalıştırmayın
3. **Veri Güvenliği**: Test verilerini production'da kullanmayın
4. **Erişim Kontrolü**: Containerlara sadece localhost'tan erişim sağlayın

## İletişim

- **Proje Sorumlusu**: Eslem
- **Konu**: Konfigürasyon/Güvenlik Başlıkları Testi
- **Ders**: Yazılım Kalite ve Güvence
