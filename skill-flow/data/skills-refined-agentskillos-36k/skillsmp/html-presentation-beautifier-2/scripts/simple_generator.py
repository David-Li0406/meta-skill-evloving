#!/usr/bin/env python3
"""
Simple HTML Presentation Generator
基于模板生成 McKinsey 风格演示文稿的简单生成器
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any


def read_template() -> str:
    """读取 HTML 模板"""
    template_path = Path(__file__).parent.parent / 'assets' / 'presentation-template.html'
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_title_slide(title: str, subtitle: str = '', slide_num: int = 1) -> str:
    """生成标题幻灯片"""
    active = ' active' if slide_num == 1 else ''
    return f'''        <div class="slide title-slide{active}" data-slide="{slide_num}">
            <h1 class="title">{title}</h1>
            {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
        </div>'''


def generate_bullet_slide(title: str, bullets: List[str], slide_num: int) -> str:
    """生成项目符号列表幻灯片"""
    bullets_html = '\n'.join([f'                <li>{bullet}</li>' for bullet in bullets])
    return f'''        <div class="slide" data-slide="{slide_num}">
            <h2 class="slide-title">{title}</h2>
            <ul class="bullet-list">
{bullets_html}
            </ul>
        </div>'''


def generate_emphasis_slide(title: str, points: List[Dict[str, str]], slide_num: int) -> str:
    """生成强调框幻灯片"""
    boxes_html = []
    for point in points:
        icon = point.get('icon', '💡')
        text = point.get('text', '')
        boxes_html.append(f'''                <div class="emphasis-box">
                    <div class="emphasis-icon">{icon}</div>
                    <div class="emphasis-text">{text}</div>
                </div>''')

    return f'''        <div class="slide" data-slide="{slide_num}">
            <h2 class="slide-title">{title}</h2>
            <div class="emphasis-container">
{chr(10).join(boxes_html)}
            </div>
        </div>'''


def generate_chart_slide(title: str, chart_id: str, slide_num: int) -> str:
    """生成图表幻灯片"""
    return f'''        <div class="slide" data-slide="{slide_num}">
            <h2 class="slide-title">{title}</h2>
            <div class="chart-container">
                <canvas id="{chart_id}"></canvas>
            </div>
        </div>'''


def generate_conclusion_slide(title: str, conclusions: List[Dict[str, str]], slide_num: int) -> str:
    """生成结论卡片网格幻灯片"""
    cards_html = []
    for idx, conclusion in enumerate(conclusions, 1):
        number = conclusion.get('number', f'{idx:02d}')
        card_title = conclusion.get('title', '')
        text = conclusion.get('text', '')
        cards_html.append(f'''                <div class="conclusion-card">
                    <div class="conclusion-number">{number}</div>
                    <h3 class="conclusion-title">{card_title}</h3>
                    <p class="conclusion-text">{text}</p>
                </div>''')

    return f'''        <div class="slide" data-slide="{slide_num}">
            <h2 class="slide-title">{title}</h2>
            <div class="conclusions-grid">
{chr(10).join(cards_html)}
            </div>
        </div>'''


def generate_chart_js(charts: List[Dict[str, Any]]) -> str:
    """生成 Chart.js 初始化代码"""
    if not charts:
        return ''

    chart_codes = []
    for chart in charts:
        chart_id = chart['id']
        chart_type = chart.get('type', 'bar')
        labels = chart.get('labels', [])
        data = chart.get('data', [])
        colors = chart.get('colors', ['#F85d42', '#556EE6', '#34c38f', '#50a5f1'])

        chart_code = f'''
            const {chart_id}Canvas = document.getElementById('{chart_id}');
            if ({chart_id}Canvas) {{
                new Chart({chart_id}Canvas, {{
                    type: '{chart_type}',
                    data: {{
                        labels: {json.dumps(labels)},
                        datasets: [{{
                            label: '{chart.get("label", "数据")}',
                            data: {json.dumps(data)},
                            backgroundColor: {json.dumps(colors[:len(data)])}
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            title: {{ display: false }}
                        }},
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                title: {{ display: true, text: '{chart.get("y_label", "")}' }}
                            }}
                        }}
                    }}
                }});
            }}'''
        chart_codes.append(chart_code)

    return '\n'.join(chart_codes)


def generate_presentation(config: Dict[str, Any], output_path: str) -> str:
    """生成完整的 HTML 演示文稿"""

    # 读取模板
    template = read_template()

    # 生成幻灯片
    slides = []
    slide_num = 1

    for slide_config in config.get('slides', []):
        slide_type = slide_config.get('type')

        if slide_type == 'title':
            slide_html = generate_title_slide(
                slide_config.get('title', ''),
                slide_config.get('subtitle', ''),
                slide_num
            )
        elif slide_type == 'bullets':
            slide_html = generate_bullet_slide(
                slide_config.get('title', ''),
                slide_config.get('bullets', []),
                slide_num
            )
        elif slide_type == 'emphasis':
            slide_html = generate_emphasis_slide(
                slide_config.get('title', ''),
                slide_config.get('points', []),
                slide_num
            )
        elif slide_type == 'chart':
            slide_html = generate_chart_slide(
                slide_config.get('title', ''),
                slide_config.get('chart_id', f'chart{slide_num}'),
                slide_num
            )
        elif slide_type == 'conclusions':
            slide_html = generate_conclusion_slide(
                slide_config.get('title', ''),
                slide_config.get('conclusions', []),
                slide_num
            )
        else:
            continue

        slides.append(slide_html)
        slide_num += 1

    total_slides = len(slides)
    slides_html = '\n\n'.join(slides)

    # 生成图表代码
    charts = config.get('charts', [])
    chart_js = generate_chart_js(charts)

    # 替换模板内容
    # 1. 替换标题
    html = template.replace('{{PRESENTATION_TITLE}}', config.get('title', '演示文稿'))

    # 2. 替换幻灯片内容（删除示例幻灯片，插入实际幻灯片）
    # 找到示例幻灯片的起始和结束位置
    start_marker = '        <!-- SLIDES GO HERE -->'
    end_marker = '    </div>\n\n    <!-- Fullscreen Button -->'

    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        # 保留标记，替换中间的示例幻灯片
        html = html[:start_idx + len(start_marker)] + '\n' + slides_html + '\n    ' + html[end_idx:]

    # 3. 替换幻灯片总数
    html = html.replace('<span id="totalSlides">1</span>', f'<span id="totalSlides">{total_slides}</span>')

    # 4. 插入图表初始化代码（在 initializeCharts() 函数中）
    if chart_js:
        init_charts_marker = '        function initializeCharts() {\n            // Example chart initialization'
        init_charts_replacement = f'        function initializeCharts() {{{chart_js}'
        html = html.replace(init_charts_marker, init_charts_replacement)

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("用法: python simple_generator.py <config.json> <output.html>")
        print("\n示例配置文件格式:")
        print(json.dumps({
            "title": "演示文稿标题",
            "slides": [
                {
                    "type": "title",
                    "title": "主标题",
                    "subtitle": "副标题"
                },
                {
                    "type": "bullets",
                    "title": "章节标题",
                    "bullets": ["要点1", "要点2", "要点3"]
                }
            ],
            "charts": [
                {
                    "id": "chart1",
                    "type": "bar",
                    "labels": ["A", "B", "C"],
                    "data": [10, 20, 30],
                    "label": "数据标签",
                    "y_label": "Y轴标签"
                }
            ]
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    config_path = sys.argv[1]
    output_path = sys.argv[2]

    # 读取配置
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 生成演示文稿
    result = generate_presentation(config, output_path)
    print(f"✓ 成功生成演示文稿: {result}")


if __name__ == '__main__':
    main()
