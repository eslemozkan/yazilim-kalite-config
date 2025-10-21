#!/usr/bin/env python3
"""
HTTP Security Headers Test Script
Yazılım Kalite ve Güvence - Konfigürasyon/Güvenlik Başlıkları Testi

Bu script, hedef uygulamalarda HTTP güvenlik başlıklarını kontrol eder
ve güvenlik açıklarını tespit eder.

Kullanım:
    python scripts/header_check.py --targets all
    python scripts/header_check.py --targets dvwa,juice-shop
    python scripts/header_check.py --targets dvwa --strict
"""

import requests
import json
import csv
import argparse
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse
import ssl
import socket

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/raw_reports/errors.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class SecurityHeaderChecker:
    """HTTP güvenlik başlıkları kontrol sınıfı"""
    
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.targets = {
            'dvwa': 'http://localhost:8081',
            'bwapp': 'http://localhost:8082',
            'xvwa': 'http://localhost:8083',
            'juice-shop': 'http://localhost:3000',
            'opencart': 'http://localhost:8084'
        }
        
    def check_headers(self, url: str, target_name: str) -> Dict:
        """Hedef URL'de güvenlik başlıklarını kontrol eder"""
        try:
            logger.info(f"Checking headers for {target_name} at {url}")
            
            # HTTP isteği gönder
            response = requests.get(url, timeout=30, allow_redirects=True)
            
            # Temel bilgileri topla
            result = {
                'url': url,
                'target': target_name,
                'timestamp': datetime.now().isoformat(),
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'findings': []
            }
            
            # Güvenlik başlıklarını kontrol et
            findings = self._analyze_headers(response.headers, response.status_code)
            result['findings'] = findings
            
            # HTTPS yönlendirme kontrolü
            if url.startswith('http://'):
                https_url = url.replace('http://', 'https://')
                try:
                    https_response = requests.get(https_url, timeout=10, verify=False)
                    if https_response.status_code == 200:
                        result['findings'].append({
                            'name': 'HTTPS_Redirect',
                            'value': 'HTTP to HTTPS redirect missing',
                            'status': 'fail',
                            'severity': 'High',
                            'remark': 'HTTPS is available but HTTP does not redirect'
                        })
                except:
                    pass
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {target_name}: {str(e)}")
            return {
                'url': url,
                'target': target_name,
                'timestamp': datetime.now().isoformat(),
                'status_code': 0,
                'headers': {},
                'findings': [{
                    'name': 'Connection_Error',
                    'value': str(e),
                    'status': 'fail',
                    'severity': 'High',
                    'remark': 'Unable to connect to target'
                }]
            }
        except Exception as e:
            logger.error(f"Unexpected error for {target_name}: {str(e)}")
            return {
                'url': url,
                'target': target_name,
                'timestamp': datetime.now().isoformat(),
                'status_code': 0,
                'headers': {},
                'findings': [{
                    'name': 'Unexpected_Error',
                    'value': str(e),
                    'status': 'fail',
                    'severity': 'High',
                    'remark': 'Unexpected error occurred'
                }]
            }
    
    def _analyze_headers(self, headers: Dict[str, str], status_code: int) -> List[Dict]:
        """HTTP başlıklarını analiz eder ve güvenlik bulgularını döndürür"""
        findings = []
        
        # HSTS kontrolü
        hsts = headers.get('Strict-Transport-Security', '')
        if not hsts:
            findings.append({
                'name': 'HSTS',
                'value': 'Missing',
                'status': 'fail',
                'severity': 'High',
                'remark': 'HSTS header is missing - allows protocol downgrade attacks'
            })
        else:
            if 'max-age' in hsts:
                max_age = self._extract_max_age(hsts)
                if max_age < 31536000:  # 1 yıl
                    findings.append({
                        'name': 'HSTS',
                        'value': f'max-age={max_age}',
                        'status': 'warn',
                        'severity': 'Medium',
                        'remark': 'HSTS max-age is less than 1 year'
                    })
                else:
                    findings.append({
                        'name': 'HSTS',
                        'value': hsts,
                        'status': 'pass',
                        'severity': 'Low',
                        'remark': 'HSTS properly configured'
                    })
        
        # CSP kontrolü
        csp = headers.get('Content-Security-Policy', '')
        if not csp:
            findings.append({
                'name': 'CSP',
                'value': 'Missing',
                'status': 'fail',
                'severity': 'High',
                'remark': 'Content Security Policy is missing'
            })
        else:
            if 'unsafe-inline' in csp or '*' in csp:
                findings.append({
                    'name': 'CSP',
                    'value': csp,
                    'status': 'fail',
                    'severity': 'High',
                    'remark': 'CSP contains unsafe directives (unsafe-inline or wildcard)'
                })
            else:
                findings.append({
                    'name': 'CSP',
                    'value': csp,
                    'status': 'pass',
                    'severity': 'Low',
                    'remark': 'CSP properly configured'
                })
        
        # X-Content-Type-Options kontrolü
        x_content_type = headers.get('X-Content-Type-Options', '')
        if not x_content_type or x_content_type.lower() != 'nosniff':
            findings.append({
                'name': 'X-Content-Type-Options',
                'value': x_content_type or 'Missing',
                'status': 'fail' if not x_content_type else 'warn',
                'severity': 'Medium',
                'remark': 'X-Content-Type-Options should be set to nosniff'
            })
        else:
            findings.append({
                'name': 'X-Content-Type-Options',
                'value': x_content_type,
                'status': 'pass',
                'severity': 'Low',
                'remark': 'X-Content-Type-Options properly configured'
            })
        
        # X-Frame-Options kontrolü
        x_frame_options = headers.get('X-Frame-Options', '')
        csp_frame_ancestors = 'frame-ancestors' in headers.get('Content-Security-Policy', '')
        
        if not x_frame_options and not csp_frame_ancestors:
            findings.append({
                'name': 'X-Frame-Options',
                'value': 'Missing',
                'status': 'fail',
                'severity': 'Medium',
                'remark': 'X-Frame-Options or CSP frame-ancestors directive is missing'
            })
        else:
            findings.append({
                'name': 'X-Frame-Options',
                'value': x_frame_options or 'CSP frame-ancestors',
                'status': 'pass',
                'severity': 'Low',
                'remark': 'Clickjacking protection is configured'
            })
        
        # Set-Cookie kontrolü
        set_cookie = headers.get('Set-Cookie', '')
        if set_cookie:
            if 'HttpOnly' not in set_cookie:
                findings.append({
                    'name': 'Cookie_HttpOnly',
                    'value': 'Missing',
                    'status': 'fail',
                    'severity': 'High',
                    'remark': 'Cookie is missing HttpOnly flag'
                })
            
            if 'Secure' not in set_cookie:
                findings.append({
                    'name': 'Cookie_Secure',
                    'value': 'Missing',
                    'status': 'fail',
                    'severity': 'High',
                    'remark': 'Cookie is missing Secure flag'
                })
        
        # Server header kontrolü
        server = headers.get('Server', '')
        if server and any(char.isdigit() for char in server):
            findings.append({
                'name': 'Server_Info_Leak',
                'value': server,
                'status': 'warn',
                'severity': 'Low',
                'remark': 'Server header contains version information'
            })
        
        # Referrer-Policy kontrolü
        referrer_policy = headers.get('Referrer-Policy', '')
        if not referrer_policy:
            findings.append({
                'name': 'Referrer-Policy',
                'value': 'Missing',
                'status': 'warn',
                'severity': 'Low',
                'remark': 'Referrer-Policy header is missing'
            })
        
        return findings
    
    def _extract_max_age(self, hsts_header: str) -> int:
        """HSTS header'ından max-age değerini çıkarır"""
        try:
            for part in hsts_header.split(';'):
                if 'max-age' in part:
                    return int(part.split('=')[1].strip())
        except:
            pass
        return 0
    
    def run_checks(self, targets: List[str], output_dir: str = 'data/raw_reports') -> None:
        """Belirtilen hedefler için güvenlik kontrollerini çalıştırır"""
        # Output dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        all_results = []
        
        # Hedefleri belirle
        if 'all' in targets:
            target_list = list(self.targets.keys())
        else:
            target_list = [t.strip() for t in targets]
        
        for target in target_list:
            if target not in self.targets:
                logger.warning(f"Unknown target: {target}")
                continue
                
            url = self.targets[target]
            result = self.check_headers(url, target)
            all_results.append(result)
            
            # JSON raporu kaydet
            json_file = f"{output_dir}/{target}_headers_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # CSV özeti oluştur
            csv_file = f"data/processed/{target}_headers_summary_{timestamp}.csv"
            self._create_csv_summary(result, csv_file)
            
            logger.info(f"Results saved for {target}: {json_file}")
        
        # Tüm sonuçları birleştir
        combined_file = f"{output_dir}/all_headers_{timestamp}.json"
        with open(combined_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Combined results saved: {combined_file}")
    
    def _create_csv_summary(self, result: Dict, csv_file: str) -> None:
        """JSON sonucundan CSV özeti oluşturur"""
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Target', 'Header_Name', 'Value', 'Status', 'Severity', 'Remark'])
            
            for finding in result['findings']:
                writer.writerow([
                    result['target'],
                    finding['name'],
                    finding['value'],
                    finding['status'],
                    finding['severity'],
                    finding['remark']
                ])

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description='HTTP Security Headers Test Tool')
    parser.add_argument('--targets', required=True, 
                       help='Comma-separated list of targets (all, dvwa, bwapp, xvwa, juice-shop, opencart)')
    parser.add_argument('--outdir', default='data/raw_reports',
                       help='Output directory for reports')
    parser.add_argument('--strict', action='store_true',
                       help='Enable strict mode for more rigorous checks')
    
    args = parser.parse_args()
    
    # Targets'ı parse et
    targets = [t.strip() for t in args.targets.split(',')]
    
    # Checker'ı başlat
    checker = SecurityHeaderChecker(strict_mode=args.strict)
    
    # Kontrolleri çalıştır
    checker.run_checks(targets, args.outdir)

if __name__ == '__main__':
    main()
