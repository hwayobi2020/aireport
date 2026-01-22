# AI Report 개발 로그

## 프로젝트 개요

**목적**: 증권사 PDF 보고서를 자동으로 다운로드하고 인터랙티브한 웹 리포트로 변환하는 시스템 개발

**개발 기간**: 2026.01.22

**개발 환경**:
- Python 3.x
- Windows 회사 환경 (SSL 인증서 제약)
- 작업 디렉토리: `d:\projects\aireport`

---

## 개발 과정

### 1. 환경 설정 및 SSL 우회

**문제**: 회사 네트워크에서 SSL 인증서 검증 문제 발생

**해결책**:
- `D:\projects\utils\ssl_bypass.py` 모듈 활용
- requests, urllib 요청에 자동으로 `verify=False` 적용
- pip 설치 시 `--trusted-host` 옵션 사용

```python
import sys
sys.path.append('D:\\projects')
import utils.ssl_bypass  # 자동 적용
```

### 2. PDF 보고서 다운로드 및 파싱

**대상**: 하나증권 Quant Weekly 보고서
- URL: `https://www.hanaw.com/download/research/FileServer/WEB/strategy/market/2026/01/20/EDIT_Quant_Weekly_260121.pdf`
- 총 16페이지

**구현 기능**:
1. SSL 우회를 통한 PDF 다운로드
2. pdfplumber를 이용한 텍스트/표 추출
3. 페이지별 데이터 구조화
4. 텍스트 파일로 백업 저장

**핵심 코드**:
```python
class PDFDownloader:
    def download(self, url: str) -> Path:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        return pdf_path

    def extract_text(self, pdf_path: Path) -> List[Dict]:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                tables = page.extract_tables()
                # 데이터 구조화
```

### 3. 보고서 내용 분석

**핵심 투자 전략 (2026.01.21 기준)**:

1. **시장 환경**
   - 미국 금리 상승 영향으로 저평가/중형주 강세
   - 금리 상승 시 저평가, 중소형주 팩터 유리
   - 달러 하락 시 배당모멘텀, 저평가 유리

2. **코스피 투자 포인트**
   - 글로벌 자산 배분에서 금리 상승 시 유리
   - 미국 중소형주와 연동성 높음
   - 2월은 배당 상향, 목표가 변화, 저평가 중심

3. **추천 종목** (저평가 실적주)
   - 지주회사: SK, 한화, GS
   - 유틸리티: 한국전력
   - 산업재: HD현대건설기계, 팬오션, 현대위아
   - 금융: 증권, 은행, iM금융지주

4. **MSCI 리뷰 (2026.02.11)**
   - **편입 예상**: 삼성에피스홀딩스, 현대건설, 에이비엘바이오
   - **편출 예상**: LG생활건강, 코웨이

### 4. 인터랙티브 웹 보고서 생성

**요구사항**:
- 요약 정보를 상단에 표시
- 탭 기반 UI로 정보 분류
- 차트 시각화
- 원본 PDF 뷰어 포함

**구현된 기능**:

#### 5개 탭 구성
1. **요약 탭**: 핵심 포인트와 투자 전략
2. **추천 종목 탭**: 상위 10개 종목 테이블
3. **MSCI 리뷰 탭**: 편입/편출 예상 종목
4. **차트 분석 탭**: PER, 배당수익률 시각화
5. **전체 보고서 탭**: PDF 뷰어

#### 디자인 특징
- 그라디언트 헤더 (보라색 계열)
- 카드 기반 레이아웃
- 호버 효과 및 애니메이션
- 반응형 디자인
- 컬러 코딩 (상승=빨강, 하락=파랑)

#### 기술 스택
- **백엔드**: Python, pdfplumber, requests
- **템플릿**: Jinja2
- **프론트엔드**: HTML5, CSS3, JavaScript
- **차트**: Chart.js
- **PDF 뷰어**: HTML iframe

### 5. 프로젝트 구조화

**모듈 설계**:

```
aireport/
├── src/
│   ├── config.py              # 설정 관리
│   ├── pdf_downloader.py      # PDF 처리 (다운로드/파싱)
│   ├── report_generator.py    # HTML 생성
│   └── __init__.py            # 패키지 초기화
├── data/                      # PDF 저장소
├── output/                    # HTML 출력
├── templates/                 # 템플릿 (선택)
├── example.py                 # 사용 예제
├── requirements.txt           # 의존성
└── README.md                  # 문서
```

**클래스 구조**:

1. **PDFDownloader**: PDF 다운로드 및 파싱
   - `download()`: URL에서 PDF 다운로드
   - `extract_text()`: 텍스트/표 추출
   - `save_as_text()`: 텍스트 파일로 저장

2. **ReportGenerator**: HTML 보고서 생성
   - `generate()`: Jinja2 템플릿으로 HTML 생성
   - `_get_default_template()`: 기본 템플릿 제공

**헬퍼 함수**:
- `download_report()`: 원스텝 다운로드/파싱
- `generate_hanaw_report()`: 하나증권 보고서 전용

### 6. 사용 방법

#### 기본 사용
```python
from src import generate_hanaw_report

html_path = generate_hanaw_report(
    output_filename="report.html"
)
```

#### CLI 사용
```bash
python -m src.report_generator --url [PDF_URL] --output report.html
```

#### 모듈별 사용
```python
from src.pdf_downloader import download_report
from src.report_generator import ReportGenerator

# 1. PDF 다운로드
pdf_path, pages_data = download_report(url)

# 2. HTML 생성
generator = ReportGenerator()
html_path = generator.generate(report_data, pdf_path.name)
```

---

## 기술적 해결 과제

### 1. Windows 콘솔 인코딩 문제
**문제**: `UnicodeEncodeError: 'cp949' codec can't encode character`

**해결**:
- 콘솔 출력 대신 파일로 저장 (UTF-8 인코딩)
- 이모지 제거

### 2. 큰 파일 읽기
**문제**: 51,301 토큰의 텍스트 파일 (제한: 25,000)

**해결**:
- `offset`, `limit` 파라미터로 부분 읽기
- 필요한 섹션만 추출

### 3. SSL 인증서 검증 우회
**문제**: 회사 프록시로 인한 SSL 에러

**해결**:
- 전역 SSL 컨텍스트 변경
- requests 몽키패칭
- pip 설치 시 `--trusted-host` 사용

---

## 향후 개선 사항

### 기능 추가
1. **AI 요약 기능**: Claude API로 보고서 자동 요약
2. **다중 증권사 지원**: 키움, 미래에셋, KB증권 등
3. **종목 비교 차트**: 여러 보고서 간 종목 비교
4. **알림 기능**: 신규 보고서 자동 다운로드 및 알림
5. **검색 기능**: 보고서 내 키워드 검색

### 기술 개선
1. **비동기 다운로드**: asyncio로 대량 보고서 처리
2. **캐싱**: 다운로드된 보고서 캐시 관리
3. **테스트**: pytest로 유닛 테스트 추가
4. **로깅**: 구조화된 로깅 시스템
5. **설정 파일**: YAML/TOML로 설정 외부화

### UI/UX 개선
1. **다크 모드**: 테마 전환 기능
2. **종목 필터링**: 업종, PER, 배당 등으로 필터
3. **즐겨찾기**: 관심 종목 북마크
4. **PDF 하이라이트**: 중요 섹션 자동 강조
5. **모바일 최적화**: 터치 인터페이스 개선

---

## 참고 자료

### 라이브러리 문서
- [pdfplumber](https://github.com/jsvine/pdfplumber): PDF 텍스트/표 추출
- [Jinja2](https://jinja.palletsprojects.com/): 템플릿 엔진
- [Chart.js](https://www.chartjs.org/): 차트 라이브러리

### 보고서 출처
- 하나증권 리서치: https://www.hanaw.com/

---

## 결론

**성과**:
- ✅ SSL 우회를 통한 회사 환경에서 PDF 다운로드 성공
- ✅ 16페이지 보고서 자동 파싱 및 구조화
- ✅ 인터랙티브 HTML 보고서 생성 (5개 탭)
- ✅ Chart.js로 데이터 시각화
- ✅ 모듈화된 재사용 가능한 구조

**교훈**:
1. 회사 환경의 제약은 공통 유틸리티로 해결
2. 큰 파일은 스트리밍/부분 처리로 대응
3. 모듈화로 확장성 확보
4. 템플릿 엔진으로 HTML 관리 효율화

**다음 단계**:
- 다른 증권사 보고서 지원 확대
- AI 요약 기능 추가
- 스케줄링 자동화 구축
