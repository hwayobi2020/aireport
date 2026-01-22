# Examples

이 폴더에는 AI Report로 생성된 샘플 보고서가 포함되어 있습니다.

## 샘플 보고서

### sample_report.html

하나증권 Quant Weekly 보고서 (2026.01.21)로 생성된 인터랙티브 HTML 리포트입니다.

**특징**:
- 5개 탭 구조 (요약, 추천 종목, MSCI 리뷰, 차트 분석, PDF 뷰어)
- Chart.js 기반 데이터 시각화
- 반응형 디자인
- 저평가 실적주 TOP 10 종목 정보

**사용 방법**:
1. 브라우저에서 `sample_report.html` 파일 열기
2. 각 탭을 클릭해서 내용 확인
3. PDF 뷰어 탭은 원본 PDF가 있어야 작동 (별도 다운로드 필요)

## 직접 생성하기

프로젝트 루트에서 다음 명령으로 새로운 보고서를 생성할 수 있습니다:

```bash
# 기본 예제 실행
python example.py

# CLI로 실행
python -m src.report_generator --output my_report.html
```

생성된 파일은 `output/` 폴더에 저장됩니다.
