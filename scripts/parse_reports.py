#!/usr/bin/env python3
"""
Rapor Parsing ve Analiz Scripti
Yazılım Kalite ve Güvence - Konfigürasyon/Güvenlik Başlıkları Testi

Bu script, ham JSON raporlarını parse eder ve analiz eder.

Kullanım:
    python scripts/parse_reports.py --input data/raw_reports/
    python scripts/parse_reports.py --input data/raw_reports/all_headers_20231201_120000.json
"""

import json
import argparse
import os
import sys
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

class ReportParser:
    """Rapor parsing ve analiz sınıfı"""
    
    def __init__(self):
        self.results = []
    
    def parse_json_file(self, file_path: str) -> Dict:
        """JSON dosyasını parse eder"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error parsing {file_path}: {str(e)}")
            return None
    
    def parse_directory(self, directory: str) -> List[Dict]:
        """Dizin içindeki tüm JSON dosyalarını parse eder"""
        results = []
        
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return results
        
        for filename in os.listdir(directory):
            if filename.endswith('.json') and not filename.startswith('all_'):
                file_path = os.path.join(directory, filename)
                data = self.parse_json_file(file_path)
                if data:
                    results.append(data)
        
        return results
    
    def analyze_findings(self, data: List[Dict]) -> Dict[str, Any]:
        """Bulguları analiz eder ve istatistikler üretir"""
        analysis = {
            'total_targets': len(data),
            'total_findings': 0,
            'severity_counts': {'High': 0, 'Medium': 0, 'Low': 0},
            'status_counts': {'pass': 0, 'warn': 0, 'fail': 0},
            'header_stats': {},
            'target_summary': {}
        }
        
        for target_data in data:
            target_name = target_data.get('target', 'unknown')
            findings = target_data.get('findings', [])
            
            target_summary = {
                'total_findings': len(findings),
                'high_severity': 0,
                'medium_severity': 0,
                'low_severity': 0,
                'failed_checks': 0,
                'passed_checks': 0,
                'warnings': 0
            }
            
            for finding in findings:
                analysis['total_findings'] += 1
                target_summary['total_findings'] += 1
                
                # Severity sayımı
                severity = finding.get('severity', 'Low')
                analysis['severity_counts'][severity] += 1
                target_summary[f'{severity.lower()}_severity'] += 1
                
                # Status sayımı
                status = finding.get('status', 'fail')
                analysis['status_counts'][status] += 1
                target_summary[f'{status}ed_checks'] += 1
                
                # Header istatistikleri
                header_name = finding.get('name', 'Unknown')
                if header_name not in analysis['header_stats']:
                    analysis['header_stats'][header_name] = {
                        'total': 0,
                        'pass': 0,
                        'warn': 0,
                        'fail': 0
                    }
                analysis['header_stats'][header_name]['total'] += 1
                analysis['header_stats'][header_name][status] += 1
            
            analysis['target_summary'][target_name] = target_summary
        
        return analysis
    
    def generate_summary_report(self, analysis: Dict[str, Any]) -> str:
        """Özet rapor oluşturur"""
        report = []
        report.append("=" * 60)
        report.append("HTTP SECURITY HEADERS ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Genel istatistikler
        report.append("GENERAL STATISTICS")
        report.append("-" * 20)
        report.append(f"Total Targets Analyzed: {analysis['total_targets']}")
        report.append(f"Total Findings: {analysis['total_findings']}")
        report.append("")
        
        # Severity dağılımı
        report.append("SEVERITY DISTRIBUTION")
        report.append("-" * 25)
        for severity, count in analysis['severity_counts'].items():
            percentage = (count / analysis['total_findings'] * 100) if analysis['total_findings'] > 0 else 0
            report.append(f"{severity}: {count} ({percentage:.1f}%)")
        report.append("")
        
        # Status dağılımı
        report.append("STATUS DISTRIBUTION")
        report.append("-" * 20)
        for status, count in analysis['status_counts'].items():
            percentage = (count / analysis['total_findings'] * 100) if analysis['total_findings'] > 0 else 0
            report.append(f"{status.upper()}: {count} ({percentage:.1f}%)")
        report.append("")
        
        # Hedef özetleri
        report.append("TARGET SUMMARIES")
        report.append("-" * 18)
        for target, summary in analysis['target_summary'].items():
            report.append(f"\n{target.upper()}:")
            report.append(f"  Total Findings: {summary['total_findings']}")
            report.append(f"  High Severity: {summary['high_severity']}")
            report.append(f"  Medium Severity: {summary['medium_severity']}")
            report.append(f"  Low Severity: {summary['low_severity']}")
            report.append(f"  Failed Checks: {summary['failed_checks']}")
            report.append(f"  Passed Checks: {summary['passed_checks']}")
            report.append(f"  Warnings: {summary['warnings']}")
        
        # Header istatistikleri
        report.append("\nHEADER STATISTICS")
        report.append("-" * 18)
        for header, stats in analysis['header_stats'].items():
            report.append(f"\n{header}:")
            report.append(f"  Total Checks: {stats['total']}")
            report.append(f"  Passed: {stats['pass']}")
            report.append(f"  Warnings: {stats['warn']}")
            report.append(f"  Failed: {stats['fail']}")
        
        return "\n".join(report)
    
    def save_analysis(self, analysis: Dict[str, Any], output_file: str) -> None:
        """Analizi JSON dosyası olarak kaydeder"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    def run_analysis(self, input_path: str, output_dir: str = 'data/processed') -> None:
        """Analizi çalıştırır"""
        # Output dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Veriyi yükle
        if os.path.isfile(input_path):
            data = [self.parse_json_file(input_path)]
        else:
            data = self.parse_directory(input_path)
        
        if not data:
            print("No data to analyze")
            return
        
        # Analizi çalıştır
        analysis = self.analyze_findings(data)
        
        # Sonuçları kaydet
        analysis_file = f"{output_dir}/analysis_{timestamp}.json"
        self.save_analysis(analysis, analysis_file)
        
        # Özet raporu oluştur
        summary_report = self.generate_summary_report(analysis)
        summary_file = f"{output_dir}/summary_report_{timestamp}.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_report)
        
        print(f"Analysis completed!")
        print(f"Analysis file: {analysis_file}")
        print(f"Summary report: {summary_file}")
        print("\n" + summary_report)

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description='Parse and analyze security header reports')
    parser.add_argument('--input', required=True,
                       help='Input JSON file or directory containing JSON files')
    parser.add_argument('--output', default='data/processed',
                       help='Output directory for analysis results')
    
    args = parser.parse_args()
    
    # Parser'ı başlat
    parser_obj = ReportParser()
    
    # Analizi çalıştır
    parser_obj.run_analysis(args.input, args.output)

if __name__ == '__main__':
    main()
