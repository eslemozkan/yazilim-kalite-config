# Test Planı - HTTP Security Headers Test Projesi

## Proje Bilgileri

- **Proje Adı**: HTTP Security Headers Test
- **Ders**: Yazılım Kalite ve Güvence
- **Sorumlu**: Eslem
- **Konu**: Konfigürasyon/Güvenlik Başlıkları Testi
- **Tarih**: 2024

## Test Kapsamı

### Hedef Uygulamalar
1. **DVWA** (Damn Vulnerable Web Application)
2. **bWAPP** (Buggy Web Application)
3. **XVWA** (Xtreme Vulnerable Web Application)
4. **OWASP Juice Shop**
5. **OpenCart**

### Test Edilecek Güvenlik Başlıkları
- Strict-Transport-Security (HSTS)
- Content-Security-Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options
- Set-Cookie (HttpOnly, Secure)
- Referrer-Policy
- Server Header (Information Disclosure)
- HTTPS Redirect

## Test Case Tablosu

| ID | Hedef | Test Adımı | Beklenen Sonuç | Kriter | Severity |
|----|-------|------------|----------------|--------|----------|
| TC001 | All | HSTS header kontrolü | HSTS header mevcut ve max-age ≥ 31536000 | Pass/Warn/Fail | High |
| TC002 | All | CSP header kontrolü | CSP header mevcut ve unsafe-inline/* yok | Pass/Warn/Fail | High |
| TC003 | All | X-Content-Type-Options kontrolü | Header = "nosniff" | Pass/Warn/Fail | Medium |
| TC004 | All | X-Frame-Options kontrolü | Header mevcut veya CSP frame-ancestors | Pass/Warn/Fail | Medium |
| TC005 | All | Cookie HttpOnly kontrolü | Set-Cookie'de HttpOnly flag | Pass/Warn/Fail | High |
| TC006 | All | Cookie Secure kontrolü | Set-Cookie'de Secure flag | Pass/Warn/Fail | High |
| TC007 | All | Server header kontrolü | Version bilgisi yok | Pass/Warn/Fail | Low |
| TC008 | All | HTTPS redirect kontrolü | HTTP → HTTPS yönlendirme | Pass/Warn/Fail | High |
| TC009 | All | Referrer-Policy kontrolü | Header mevcut | Pass/Warn/Fail | Low |
| TC010 | All | Directory listing kontrolü | Index listing yok | Pass/Warn/Fail | Medium |

## Severity Kriterleri

### High Severity
- **HSTS yok**: Protocol downgrade saldırılarına açık
- **CSP yok**: XSS saldırılarına açık
- **CSP unsafe-inline/***: XSS saldırılarına açık
- **Cookie HttpOnly yok**: XSS ile cookie çalınabilir
- **Cookie Secure yok**: Man-in-the-middle saldırılarına açık
- **HTTPS redirect yok**: Man-in-the-middle saldırılarına açık

### Medium Severity
- **HSTS max-age < 1 yıl**: Kısa süreli koruma
- **X-Content-Type-Options yok**: MIME sniffing saldırılarına açık
- **X-Frame-Options yok**: Clickjacking saldırılarına açık
- **Directory listing**: Bilgi sızıntısı riski

### Low Severity
- **Server version bilgisi**: Bilgi toplama için kullanılabilir
- **Referrer-Policy yok**: Referrer bilgisi sızıntısı

## Test Ortamı

### Gereksinimler
- **İşletim Sistemi**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **RAM**: 8GB (16GB önerilen)
- **Disk**: 10GB boş alan
- **CPU**: 4 çekirdek (8 çekirdek önerilen)

### Yazılım Gereksinimleri
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.9+
- **Git**: 2.30+

### Ağ Konfigürasyonu
- **Port Mapping**:
  - DVWA: 8081
  - bWAPP: 8082
  - XVWA: 8083
  - Juice Shop: 3000
  - OpenCart: 8084

## Test Senaryoları

### Senaryo 1: Temel Header Kontrolü
1. Tüm hedeflere HTTP isteği gönder
2. Response header'larını analiz et
3. Güvenlik başlıklarını kontrol et
4. Sonuçları raporla

### Senaryo 2: HTTPS Yönlendirme Kontrolü
1. HTTP URL'lerine istek gönder
2. HTTPS yönlendirmesi kontrol et
3. SSL/TLS konfigürasyonunu kontrol et
4. Sonuçları raporla

### Senaryo 3: Cookie Güvenliği Kontrolü
1. Login işlemi gerçekleştir
2. Set-Cookie header'larını analiz et
3. HttpOnly ve Secure flag'lerini kontrol et
4. Sonuçları raporla

### Senaryo 4: CSP Analizi
1. CSP header'ını parse et
2. Unsafe direktifleri kontrol et
3. Wildcard kaynakları kontrol et
4. Sonuçları raporla

## Risk Analizi

### Yüksek Risk
- **Güvenlik başlıkları eksik**: XSS, clickjacking, MIME sniffing saldırıları
- **HTTPS yönlendirme yok**: Man-in-the-middle saldırıları
- **Cookie güvenliği**: Session hijacking

### Orta Risk
- **Kısa süreli HSTS**: Kısa süreli koruma
- **Directory listing**: Bilgi sızıntısı

### Düşük Risk
- **Server bilgisi**: Bilgi toplama
- **Referrer sızıntısı**: Gizlilik ihlali

## Test Verileri

### Örnek Test Verileri
```json
{
  "targets": [
    "dvwa",
    "bwapp", 
    "xvwa",
    "juice-shop",
    "opencart"
  ],
  "expected_headers": [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy"
  ],
  "cookie_flags": [
    "HttpOnly",
    "Secure"
  ]
}
```

## Test Sonuçları

### Başarı Kriterleri
- **Pass**: Güvenlik başlığı mevcut ve doğru konfigüre edilmiş
- **Warn**: Güvenlik başlığı mevcut ancak suboptimal
- **Fail**: Güvenlik başlığı eksik veya yanlış konfigüre edilmiş

### Rapor Formatı
- **JSON**: Ham test sonuçları
- **CSV**: İnsan okunabilir özet
- **Excel**: Karşılaştırma tablosu
- **TXT**: Analiz raporu

## Güvenlik ve Etik Uyarılar

⚠️ **ÖNEMLİ UYARILAR**:

1. **Eğitim Amaçlı**: Bu proje sadece eğitim amaçlıdır
2. **İzolasyon**: Test ortamı production'dan izole edilmelidir
3. **Yetkisiz Kullanım**: Gerçek sistemlerde izinsiz test yasaktır
4. **Veri Güvenliği**: Test verilerini production'da kullanmayın
5. **Ağ Güvenliği**: Containerları güvenli ağda çalıştırın

## Sorumlular

- **Test Sorumlusu**: Eslem
- **Konu**: Konfigürasyon/Güvenlik Başlıkları Testi
- **Ders**: Yazılım Kalite ve Güvence
- **Tarih**: 2024

## Test Takvimi

| Aşama | Süre | Açıklama |
|-------|------|----------|
| Hazırlık | 1 gün | Ortam kurulumu, container başlatma |
| Test | 2 gün | Header kontrolleri, rapor oluşturma |
| Analiz | 1 gün | Sonuç analizi, öneriler |
| Rapor | 1 gün | Final rapor hazırlama |

## Kalite Kontrol

### Test Doğrulama
- [ ] Tüm hedefler test edildi
- [ ] Tüm güvenlik başlıkları kontrol edildi
- [ ] Sonuçlar doğru kategorize edildi
- [ ] Raporlar oluşturuldu
- [ ] Analiz tamamlandı

### Kalite Metrikleri
- **Test Kapsamı**: %100 (tüm hedefler)
- **Header Kapsamı**: %100 (tüm başlıklar)
- **Rapor Kalitesi**: Yüksek (detaylı analiz)
- **Sonuç Doğruluğu**: Yüksek (manuel doğrulama)

## Sonuç

Bu test planı, HTTP güvenlik başlıklarının kapsamlı bir şekilde test edilmesini sağlar. Test sonuçları, güvenlik açıklarının tespit edilmesi ve önerilerin sunulması için kullanılacaktır.
