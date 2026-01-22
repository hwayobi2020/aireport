"""
AI Report 사용 예제
"""
from src import generate_hanaw_report

if __name__ == "__main__":
    # 하나증권 Quant Weekly 보고서 생성
    print("=" * 80)
    print("AI Report - 인터랙티브 금융 보고서 생성기")
    print("=" * 80)

    # 보고서 생성
    html_path = generate_hanaw_report(
        output_filename="hanaw_quant_weekly.html"
    )

    print(f"\n[OK] 보고서가 생성되었습니다!")
    print(f"  파일 위치: {html_path}")
    print(f"\n브라우저에서 열어보세요.")
