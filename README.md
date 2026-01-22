# AI Report - 인터랙티브 금융 보고서 생성기

증권사 PDF 보고서를 다운로드하고 인터랙티브한 웹 리포트로 변환하는 프로젝트

## 기능

- PDF 보고서 자동 다운로드 (SSL 우회 지원)
- PDF 텍스트 및 표 추출
- 인터랙티브 HTML 보고서 생성
- 차트 시각화 (Chart.js)
- PDF 뷰어 내장

## 프로젝트 구조

```
aireport/
├── src/
│   ├── pdf_downloader.py      # PDF 다운로드 및 파싱
│   ├── report_generator.py    # HTML 보고서 생성
│   └── config.py               # 설정 파일
├── templates/
│   └── report_template.html   # HTML 템플릿
├── data/                       # 다운로드된 PDF 저장
├── output/                     # 생성된 HTML 보고서
├── requirements.txt
└── README.md
```

## 설치

```bash
pip install -r requirements.txt
```

## 사용법

### 1. 보고서 다운로드 및 HTML 생성

```python
from src.pdf_downloader import download_report
from src.report_generator import generate_html_report

# PDF 다운로드
pdf_path = download_report("https://example.com/report.pdf")

# HTML 보고서 생성
html_path = generate_html_report(pdf_path)
```

### 2. CLI 사용

```bash
python -m src.report_generator --url "https://example.com/report.pdf"
```

## 예제

하나증권 Quant Weekly 보고서:
```bash
python -m src.report_generator --url "https://www.hanaw.com/download/research/FileServer/WEB/strategy/market/2026/01/20/EDIT_Quant_Weekly_260121.pdf"
```

## 요구사항

- Python 3.8+
- pdfplumber
- requests
- jinja2

## 라이선스

MIT
