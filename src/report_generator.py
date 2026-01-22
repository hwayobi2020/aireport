"""
인터랙티브 HTML 보고서 생성 모듈
"""
import json
import argparse
from pathlib import Path
from typing import Dict, List
from jinja2 import Template

from .config import OUTPUT_DIR, TEMPLATE_DIR
from .pdf_downloader import download_report


class ReportGenerator:
    """HTML 보고서 생성기"""

    def __init__(self, template_path: Path = None):
        self.template_path = template_path or (TEMPLATE_DIR / "report_template.html")
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, report_data: Dict, pdf_filename: str, output_filename: str = None) -> Path:
        """
        HTML 보고서 생성

        Args:
            report_data: 보고서 데이터
            pdf_filename: PDF 파일명
            output_filename: 출력 HTML 파일명

        Returns:
            생성된 HTML 파일 경로
        """
        if output_filename is None:
            output_filename = "report.html"

        # 템플릿 로드
        if self.template_path.exists():
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        else:
            # 기본 템플릿 사용
            template_content = self._get_default_template()

        template = Template(template_content)

        # HTML 생성
        html_content = template.render(
            data=report_data,
            pdf_filename=pdf_filename,
            json_data=json.dumps(report_data.get('top_stocks', []))
        )

        # 파일 저장
        output_path = self.output_dir / output_filename
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[OK] HTML 보고서 생성: {output_path}")
        return output_path

    def _get_default_template(self) -> str:
        """기본 템플릿 반환"""
        return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ data.title }} - {{ data.subtitle }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', 'Malgun Gothic', sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .container { max-width: 1400px; margin: 0 auto; padding: 0 2rem; }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 700; }
        .header .meta { opacity: 0.9; font-size: 1.1rem; }
        .tabs { background: white; margin-top: -2rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
        .tab-buttons { display: flex; border-bottom: 2px solid #e0e0e0; background: #fafafa; }
        .tab-button { flex: 1; padding: 1.2rem; background: none; border: none; cursor: pointer; font-size: 1.1rem; font-weight: 600; color: #666; transition: all 0.3s; position: relative; }
        .tab-button:hover { background: #f0f0f0; color: #333; }
        .tab-button.active { color: #667eea; background: white; }
        .tab-button.active::after { content: ''; position: absolute; bottom: -2px; left: 0; right: 0; height: 3px; background: #667eea; }
        .tab-content { display: none; padding: 2rem; animation: fadeIn 0.5s; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); border-left: 4px solid #667eea; }
        .card h3 { color: #667eea; margin-bottom: 1rem; font-size: 1.3rem; display: flex; align-items: center; gap: 0.5rem; }
        .card h3::before { content: '▶'; font-size: 0.8rem; }
        .card ul { list-style: none; }
        .card li { padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; padding-left: 1.5rem; position: relative; }
        .card li:last-child { border-bottom: none; }
        .card li::before { content: '•'; position: absolute; left: 0; color: #667eea; font-weight: bold; }
        .stock-table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.08); }
        .stock-table thead { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .stock-table th { padding: 1rem; text-align: left; font-weight: 600; }
        .stock-table td { padding: 1rem; border-bottom: 1px solid #f0f0f0; }
        .stock-table tbody tr:hover { background: #f8f9ff; }
        .positive { color: #e74c3c; font-weight: 600; }
        .negative { color: #3498db; font-weight: 600; }
        .chart-container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-bottom: 2rem; height: 400px; }
        .pdf-viewer { background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-top: 1rem; }
        .pdf-viewer iframe { width: 100%; height: 800px; border: none; border-radius: 4px; }
        .badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }
        .badge-high { background: #e74c3c; color: white; }
        .badge-medium { background: #f39c12; color: white; }
        .badge-low { background: #95a5a6; color: white; }
        .msci-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
        .msci-item { background: #f8f9ff; padding: 1rem; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border-left: 3px solid #667eea; }
        .footer { text-align: center; padding: 2rem; color: #999; margin-top: 3rem; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>{{ data.title }}</h1>
            <div class="meta">{{ data.subtitle }} | {{ data.date }} | {% for analyst in data.analysts %}{{ analyst }}{% if not loop.last %}, {% endif %}{% endfor %}</div>
        </div>
    </div>

    <div class="container" style="margin-top: 3rem;">
        <div class="tabs">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="openTab(event, 'summary')">요약</button>
                <button class="tab-button" onclick="openTab(event, 'stocks')">추천 종목</button>
                <button class="tab-button" onclick="openTab(event, 'msci')">MSCI 리뷰</button>
                <button class="tab-button" onclick="openTab(event, 'charts')">차트 분석</button>
                <button class="tab-button" onclick="openTab(event, 'pdf')">전체 보고서</button>
            </div>

            <div id="summary" class="tab-content active">
                <h2 style="margin-bottom: 1.5rem; color: #333;">핵심 요약</h2>
                <div class="summary-grid">
                    <div class="card">
                        <h3>주요 포인트</h3>
                        <ul>
                            {% for point in data.summary.key_points %}
                            <li>{{ point }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="card">
                        <h3>투자 전략</h3>
                        <ul>
                            {% for strategy in data.summary.strategy %}
                            <li>{{ strategy }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>

            <div id="stocks" class="tab-content">
                <h2 style="margin-bottom: 1.5rem; color: #333;">고금리 상황에서 유리한 저평가 실적주</h2>
                <table class="stock-table">
                    <thead>
                        <tr>
                            <th>종목명</th>
                            <th>PER (배)</th>
                            <th>PBR (배)</th>
                            <th>OP 3M 변화 (%)</th>
                            <th>배당수익률 (%)</th>
                            <th>목표가 1M 변화 (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for stock in data.top_stocks %}
                        <tr>
                            <td><strong>{{ stock.name }}</strong></td>
                            <td>{{ stock.per }}</td>
                            <td>{{ stock.pbr }}</td>
                            <td class="{% if stock.op_3m > 0 %}positive{% else %}negative{% endif %}">{{ '%+.1f' | format(stock.op_3m) }}</td>
                            <td>{{ stock.dividend }}</td>
                            <td class="{% if stock.target_1m > 0 %}positive{% else %}negative{% endif %}">{{ '%+.1f' | format(stock.target_1m) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <div id="msci" class="tab-content">
                <h2 style="margin-bottom: 1.5rem; color: #333;">2월 MSCI KOREA 리뷰 예상 ({{ data.msci_review.date }})</h2>
                <h3 style="color: #667eea; margin: 2rem 0 1rem 0;">신규 편입 예상</h3>
                <div class="msci-grid">
                    {% for entry in data.msci_review.new_entries %}
                    <div class="msci-item">
                        <span><strong>{{ entry.name }}</strong></span>
                        <span class="badge badge-{% if entry.probability == '높음' %}high{% elif entry.probability == '중간' %}medium{% else %}low{% endif %}">{{ entry.probability }}</span>
                    </div>
                    {% endfor %}
                </div>
                <h3 style="color: #e74c3c; margin: 2rem 0 1rem 0;">편출 예상</h3>
                <div class="msci-grid">
                    {% for removal in data.msci_review.removals %}
                    <div class="msci-item" style="border-left-color: #e74c3c;">
                        <span><strong>{{ removal.name }}</strong></span>
                        <span class="badge badge-{% if removal.probability == '높음' %}high{% else %}medium{% endif %}">{{ removal.probability }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <div id="charts" class="tab-content">
                <h2 style="margin-bottom: 1.5rem; color: #333;">데이터 시각화</h2>
                <div class="chart-container"><canvas id="perChart"></canvas></div>
                <div class="chart-container"><canvas id="dividendChart"></canvas></div>
            </div>

            <div id="pdf" class="tab-content">
                <h2 style="margin-bottom: 1.5rem; color: #333;">전체 보고서</h2>
                <div class="pdf-viewer"><iframe src="{{ pdf_filename }}"></iframe></div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>AI Report - Interactive Financial Report Generator</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">본 자료는 투자 참고용이며, 투자 결정은 본인의 판단과 책임 하에 이루어져야 합니다.</p>
    </div>

    <script>
        function openTab(evt, tabName) {
            var i, tabcontent, tabbuttons;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].classList.remove("active");
            }
            tabbuttons = document.getElementsByClassName("tab-button");
            for (i = 0; i < tabbuttons.length; i++) {
                tabbuttons[i].classList.remove("active");
            }
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }

        const stockData = {{ json_data | safe }};

        const perCtx = document.getElementById('perChart').getContext('2d');
        new Chart(perCtx, {
            type: 'bar',
            data: {
                labels: stockData.map(s => s.name),
                datasets: [{
                    label: 'PER (배)',
                    data: stockData.map(s => s.per),
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: 'PER 비교 (낮을수록 저평가)', font: { size: 16 } },
                    legend: { display: false }
                },
                scales: { y: { beginAtZero: true, title: { display: true, text: 'PER (배)' } } }
            }
        });

        const divCtx = document.getElementById('dividendChart').getContext('2d');
        new Chart(divCtx, {
            type: 'bar',
            data: {
                labels: stockData.map(s => s.name),
                datasets: [{
                    label: '배당수익률 (%)',
                    data: stockData.map(s => s.dividend),
                    backgroundColor: 'rgba(231, 76, 60, 0.7)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: { display: true, text: '배당수익률 비교 (높을수록 유리)', font: { size: 16 } },
                    legend: { display: false }
                },
                scales: { y: { beginAtZero: true, title: { display: true, text: '배당수익률 (%)' } } }
            }
        });
    </script>
</body>
</html>"""


def generate_hanaw_report(url: str = None, output_filename: str = "hanaw_report.html"):
    """
    하나증권 Quant Weekly 보고서 생성

    Args:
        url: PDF URL (기본값: 최신 보고서)
        output_filename: 출력 파일명
    """
    if url is None:
        url = "https://www.hanaw.com/download/research/FileServer/WEB/strategy/market/2026/01/20/EDIT_Quant_Weekly_260121.pdf"

    # PDF 다운로드
    pdf_path, pages_data = download_report(url, DATA_DIR)

    # 보고서 데이터 구성
    report_data = {
        "title": "우상향 금리, 저평가 실적주가 답",
        "subtitle": "실전 퀀트",
        "date": "2026.01.21",
        "analysts": ["이경수 (gang@hanafn.com)", "이철현 (lch2678@hanafn.com)"],
        "summary": {
            "key_points": [
                "연초 미국 금리 상승 영향으로 글로벌 저평가 및 중형주 강세",
                "금리 상승 시기에 미국 저평가 및 중소형주 강세 뚜렷",
                "달러 하락 시기에도 배당모멘텀, 저평가, 중형주 팩터 유리",
                "코스피는 금리 상승 시기에 유리한 자산 (미국 중소형주와 연동성 높음)",
                "2월은 배당 상향, 목표주가 변화, 고배당, 저평가, 실적 상향 컨셉 유리"
            ],
            "strategy": [
                "지주회사: SK, 한화, GS 등",
                "유틸리티: 한국전력",
                "산업재: HD현대건설기계, 팬오션, 현대위아",
                "소재: 한국타이어앤테크놀로지",
                "금융: 유통, 증권, 은행"
            ]
        },
        "msci_review": {
            "date": "2026.02.11",
            "new_entries": [
                {"name": "삼성에피스홀딩스", "probability": "높음"},
                {"name": "현대건설", "probability": "높음"},
                {"name": "에이비엘바이오", "probability": "높음"},
                {"name": "레인보우로보틱스", "probability": "중간"},
                {"name": "현대오토에버", "probability": "낮음"}
            ],
            "removals": [
                {"name": "LG생활건강", "probability": "높음"},
                {"name": "코웨이", "probability": "높음"}
            ]
        },
        "top_stocks": [
            {"name": "이마트", "per": 9.1, "pbr": 0.2, "op_3m": 6.9, "dividend": 2.7, "target_1m": 21.0},
            {"name": "GS", "per": 7.2, "pbr": 0.4, "op_3m": 7.6, "dividend": 4.4, "target_1m": 25.9},
            {"name": "롯데쇼핑", "per": 8.5, "pbr": 0.1, "op_3m": 2.5, "dividend": 5.0, "target_1m": 17.3},
            {"name": "iM금융지주", "per": 4.6, "pbr": 0.4, "op_3m": 3.4, "dividend": 4.9, "target_1m": 26.2},
            {"name": "팬오션", "per": 6.3, "pbr": 0.4, "op_3m": 2.1, "dividend": 2.9, "target_1m": 12.5},
            {"name": "SK", "per": 8.4, "pbr": 0.6, "op_3m": 29.1, "dividend": 2.4, "target_1m": 32.1},
            {"name": "BNK금융지주", "per": 5.6, "pbr": 0.5, "op_3m": 3.8, "dividend": 4.8, "target_1m": 8.9},
            {"name": "한국타이어앤테크놀로지", "per": 6.1, "pbr": 0.7, "op_3m": 18.4, "dividend": 3.6, "target_1m": 25.6},
            {"name": "신세계", "per": 11.0, "pbr": 0.6, "op_3m": 7.3, "dividend": 1.6, "target_1m": -5.5},
            {"name": "한국금융지주", "per": 5.9, "pbr": 1.1, "op_3m": 18.4, "dividend": 4.3, "target_1m": 33.7}
        ]
    }

    # HTML 생성
    generator = ReportGenerator()
    html_path = generator.generate(report_data, pdf_path.name, output_filename)

    return html_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Report - 인터랙티브 금융 보고서 생성기")
    parser.add_argument("--url", type=str, help="PDF URL")
    parser.add_argument("--output", type=str, default="report.html", help="출력 파일명")

    args = parser.parse_args()

    if args.url:
        print(f"[*] URL에서 보고서 생성: {args.url}")
        # 커스텀 URL 처리 (현재는 하나증권만 지원)
        html_path = generate_hanaw_report(args.url, args.output)
    else:
        # 기본 하나증권 보고서
        html_path = generate_hanaw_report(output_filename=args.output)

    print(f"\n[OK] 완료!")
    print(f"[*] HTML 보고서: {html_path}")
    print(f"[*] 브라우저에서 열어보세요.")
