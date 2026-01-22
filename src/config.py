"""
AI Report 설정 파일
"""
from pathlib import Path

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent

# 데이터 디렉토리
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATE_DIR = PROJECT_ROOT / "templates"

# SSL 우회 설정 (회사 환경)
USE_SSL_BYPASS = True
SSL_BYPASS_PATH = "D:\\projects"

# PDF 다운로드 설정
DOWNLOAD_TIMEOUT = 60

# 보고서 설정
DEFAULT_CHART_HEIGHT = 400
