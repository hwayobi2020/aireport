"""
PDF 다운로드 및 파싱 모듈
"""
import sys
from pathlib import Path
import requests
import pdfplumber
from typing import Dict, List, Tuple

from .config import DATA_DIR, USE_SSL_BYPASS, SSL_BYPASS_PATH, DOWNLOAD_TIMEOUT

# SSL 우회 (회사 환경)
if USE_SSL_BYPASS:
    sys.path.append(SSL_BYPASS_PATH)
    import utils.ssl_bypass


class PDFDownloader:
    """PDF 다운로드 및 파싱 클래스"""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, filename: str = None) -> Path:
        """
        PDF 다운로드

        Args:
            url: PDF URL
            filename: 저장할 파일명 (None이면 URL에서 추출)

        Returns:
            다운로드된 PDF 파일 경로
        """
        if filename is None:
            filename = url.split("/")[-1]

        pdf_path = self.output_dir / filename

        print(f"[*] PDF 다운로드 중: {url}")
        response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
        response.raise_for_status()

        with open(pdf_path, 'wb') as f:
            f.write(response.content)

        print(f"[OK] 다운로드 완료: {pdf_path}")
        return pdf_path

    def extract_text(self, pdf_path: Path) -> List[Dict]:
        """
        PDF에서 텍스트와 표 추출

        Args:
            pdf_path: PDF 파일 경로

        Returns:
            페이지별 데이터 리스트
        """
        pages_data = []

        print(f"[*] PDF 파싱 중: {pdf_path}")
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"[*] 총 페이지 수: {total_pages}")

            for i, page in enumerate(pdf.pages, 1):
                page_data = {
                    'page_num': i,
                    'text': '',
                    'tables': []
                }

                # 텍스트 추출
                text = page.extract_text()
                if text:
                    page_data['text'] = text

                # 표 추출
                tables = page.extract_tables()
                if tables:
                    page_data['tables'] = tables

                pages_data.append(page_data)
                print(f"[*] 페이지 {i}/{total_pages} 처리 완료")

        print(f"[OK] PDF 파싱 완료")
        return pages_data

    def save_as_text(self, pages_data: List[Dict], output_path: Path):
        """
        추출된 데이터를 텍스트 파일로 저장

        Args:
            pages_data: 페이지별 데이터
            output_path: 저장할 텍스트 파일 경로
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"총 페이지 수: {len(pages_data)}\n")
            f.write("=" * 80 + "\n")

            for page_data in pages_data:
                f.write(f"\n[페이지 {page_data['page_num']}]\n")
                f.write("-" * 80 + "\n")
                f.write(page_data['text'] + "\n")

                if page_data['tables']:
                    f.write(f"\n[표 {len(page_data['tables'])}개 발견]\n")
                    for j, table in enumerate(page_data['tables'], 1):
                        f.write(f"\n<표 {j}>\n")
                        for row in table:
                            f.write(" | ".join([str(cell) if cell else "" for cell in row]) + "\n")

                f.write("=" * 80 + "\n")

        print(f"[OK] 텍스트 파일 저장: {output_path}")


def download_report(url: str, output_dir: Path = None) -> Tuple[Path, List[Dict]]:
    """
    보고서 다운로드 및 파싱 헬퍼 함수

    Args:
        url: PDF URL
        output_dir: 저장 디렉토리

    Returns:
        (PDF 파일 경로, 페이지 데이터)
    """
    downloader = PDFDownloader(output_dir)
    pdf_path = downloader.download(url)
    pages_data = downloader.extract_text(pdf_path)

    # 텍스트 파일로도 저장
    txt_path = pdf_path.with_suffix('.txt')
    downloader.save_as_text(pages_data, txt_path)

    return pdf_path, pages_data


if __name__ == "__main__":
    # 테스트
    url = "https://www.hanaw.com/download/research/FileServer/WEB/strategy/market/2026/01/20/EDIT_Quant_Weekly_260121.pdf"
    pdf_path, pages_data = download_report(url)
    print(f"\n[*] 다운로드 완료: {pdf_path}")
    print(f"[*] 총 {len(pages_data)} 페이지")
