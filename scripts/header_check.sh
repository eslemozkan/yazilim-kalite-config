#!/bin/bash
# HTTP Security Headers Test Script - Bash Wrapper
# Yazılım Kalite ve Güvence - Konfigürasyon/Güvenlik Başlıkları Testi

set -e

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}HTTP Security Headers Test Tool${NC}"
echo "=================================="

# Python virtual environment kontrolü
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv .venv
fi

# Virtual environment'ı aktifleştir
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Bağımlılıkları yükle
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Docker containerları kontrol et
echo -e "${YELLOW}Checking Docker containers...${NC}"
if ! docker compose ps | grep -q "Up"; then
    echo -e "${RED}Warning: No Docker containers are running. Please run 'docker compose up -d' first.${NC}"
    exit 1
fi

# Script parametrelerini geç
echo -e "${GREEN}Running header checks...${NC}"
python scripts/header_check.py "$@"

echo -e "${GREEN}Header checks completed!${NC}"
echo "Check the following directories for results:"
echo "- Raw reports: data/raw_reports/"
echo "- Processed reports: data/processed/"
