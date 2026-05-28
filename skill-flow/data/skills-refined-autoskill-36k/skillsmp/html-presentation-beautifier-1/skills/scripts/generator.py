#!/usr/bin/env python3
"""
HTML Presentation Generator - Generate McKinsey-style HTML presentations from parsed documents.

Transforms structured content into professional HTML slides with charts and visualizations.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class PresentationGenerator:
    def __init__(self, template_path: Optional[str] = None):
        self.template_path = template_path or 'assets/template.html'
        self.colors = {
            'primary': '#F85d42',
            'secondary': '#74788d',
            'deep_blue': '#556EE6',
            'green': '#34c38f',
            'blue': '#50a5f1',
            'yellow': '#f1b44c'
        }

    def generate(
        self,
        parsed_doc: Dict[str, Any],
        output_path: str = 'presentation.html'
    ) -> str:
        template = self._load_template()
        slides_html = self._generate_slides(parsed_doc)
        scripts_html = self._generate_scripts(parsed_doc)

        html = template.replace(
            '<!-- Slides Container -->\n    <div class="presentation-container">',
            f'<!-- Slides Container -->\n    <div class="presentation-container">\n{slides_html}'
        )

        html = html.replace(
            '<script src="script.js"></script>',
            f'{scripts_html}\n</body>'
        )

        output = Path(output_path)
        output.write_text(html, encoding='utf-8')

        return str(output.absolute())

    def _load_template(self) -> str:
        template_file = Path(self.template_path)
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        return self._get_default_template()

    def _get_default_template(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <nav class="navbar">
        <button class="nav-btn" id="prevBtn" onclick="navigate(-1)">← Previous</button>
        <span class="slide-counter">Slide <span id="currentSlide">1</span> of <span id="totalSlides">1</span></span>
        <button class="nav-btn" id="nextBtn" onclick="navigate(1)">Next →</button>
    </nav>

    <!-- Slides Container -->
    <div class="presentation-container">
        <!-- Slides will be generated here -->
    </div>

    <button class="fullscreen-btn" onclick="toggleFullscreen()">⛶ Fullscreen</button>

    <script src="script.js"></script>
</body>
</html>
"""

    def _generate_slides(self, doc: Dict[str, Any]) -> str:
        slides = []

        title = doc.get('title', 'Untitled')
        sections = doc.get('sections', [])
        data_points = doc.get('data_points', [])
        conclusions = doc.get('conclusions', [])

        slide_num = 1

        slide_num = self._add_title_slide(slides, slide_num, title)
        slide_num = self._add_executive_summary(slides, slide_num, conclusions)
        slide_num = self._add_data_slides(slides, slide_num, data_points, sections)
        slide_num = self._add_detailed_slides(slides, slide_num, sections)
        slide_num = self._add_conclusions(slides, slide_num, conclusions)

        return '\n'.join(slides)

    def _add_title_slide(self, slides: List[str], slide_num: int, title: str) -> int:
        date_str = datetime.now().strftime('%B %Y')

        slide = f'''
        <div class="slide active" data-slide="{slide_num}">
            <div class="title-slide">
                <h1 class="title">{title}</h1>
                <h2 class="subtitle">Data Analysis & Insights</h2>
                <p class="date">Date: {date_str}</p>
            </div>
        </div>
        '''
        slides.append(slide)
        return slide_num + 1

    def _add_executive_summary(self, slides: List[str], slide_num: int, conclusions: List[Dict]) -> int:
        top_conclusions = conclusions[:5] if len(conclusions) > 5 else conclusions

        points_html = ''
        for conc in top_conclusions:
            text = conc.get('text', conc) if isinstance(conc, dict) else str(conc)
            points_html += f'<li class="key-point">{text}</li>\n'

        slide = f'''
        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">Executive Summary</h1>
            </div>
            <div class="slide-content">
                <ul class="key-points">
                    {points_html}
                </ul>
            </div>
        </div>
        '''
        slides.append(slide)
        return slide_num + 1

    def _add_data_slides(
        self,
        slides: List[str],
        slide_num: int,
        data_points: List[Dict],
        sections: List[Dict]
    ) -> int:
        if not data_points:
            return slide_num

        chart_num = 0
        for i, section in enumerate(sections[:3]):
            section_data = [
                dp for dp in data_points
                if dp.get('category') == section.get('title', '')
            ]

            if not section_data:
                continue

            chart_num += 1
            chart_id = f"chart{chart_num}"
            insights = section.get('content', '').split('\n')[:3]

            insights_html = '\n'.join([
                f'<li>{insight.strip()}</li>' for insight in insights if insight.strip()
            ])

            slide = f'''
        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{section.get('title', 'Data Analysis')}</h1>
            </div>
            <div class="slide-content two-column">
                <div class="column chart-container">
                    <canvas id="{chart_id}"></canvas>
                    <p class="chart-caption">{section.get('title', 'Chart')} - Data Visualization</p>
                </div>
                <div class="column">
                    <h3 class="section-header">Key Insights</h3>
                    <ul class="bullet-points">
                        {insights_html}
                    </ul>
                </div>
            </div>
        </div>
            '''
            slides.append(slide)
            slide_num += 1

        return slide_num

    def _add_detailed_slides(self, slides: List[str], slide_num: int, sections: List[Dict]) -> int:
        for section in sections[3:]:
            if not section.get('content', '').strip():
                continue

            content_lines = section.get('content', '').split('\n')
            content_html = '\n'.join([
                f'<p class="body-text">{line.strip()}</p>' for line in content_lines if line.strip() and len(line.strip()) > 20
            ])

            slide = f'''
        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{section.get('title', 'Detailed Findings')}</h1>
            </div>
            <div class="slide-content">
                {content_html}
            </div>
        </div>
            '''
            slides.append(slide)
            slide_num += 1

        return slide_num

    def _add_conclusions(self, slides: List[str], slide_num: int, conclusions: List[Dict]) -> int:
        if not conclusions:
            return slide_num

        conclusions_html = ''
        for i, conc in enumerate(conclusions[:6]):
            text = conc.get('text', conc) if isinstance(conc, dict) else str(conc)
            conclusions_html += f'''
                <div class="conclusion-card">
                    <h3 class="card-title">Conclusion {i+1}</h3>
                    <p class="card-text">{text}</p>
                </div>
            '''

        recommendations_html = '\n'.join([
            f'<li>{(rec.get("text", rec) if isinstance(rec, dict) else str(rec)).strip()}</li>'
            for rec in conclusions[:5]
        ])

        slide = f'''
        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">Conclusions & Recommendations</h1>
            </div>
            <div class="slide-content">
                <div class="conclusions-grid">
                    {conclusions_html}
                </div>

                <div class="recommendations-box">
                    <h3 class="section-header accent-text">Key Recommendations</h3>
                    <ol class="numbered-list">
                        {recommendations_html}
                    </ol>
                </div>
            </div>
        </div>
        '''
        slides.append(slide)
        return slide_num + 1

    def _generate_scripts(self, doc: Dict[str, Any]) -> str:
        data_points = doc.get('data_points', [])
        sections = doc.get('sections', [])

        chart_scripts = []

        chart_num = 0
        for i, section in enumerate(sections[:3]):
            section_data = [
                dp for dp in data_points
                if dp.get('category') == section.get('title', '')
            ]

            if not section_data:
                continue

            chart_num += 1
            chart_id = f"chart{chart_num}"
            chart_scripts.append(self._generate_chart_script(chart_id, section_data))

        return '\n'.join(chart_scripts)

    def _generate_chart_script(self, chart_id: str, data_points: List[Dict]) -> str:
        labels = [dp.get('label', f'Item {i+1}') for i, dp in enumerate(data_points[:10])]
        values = [dp.get('value', 0) for dp in data_points[:10]]

        chart_data = json.dumps({
            'labels': labels,
            'datasets': [{
                'label': 'Value',
                'data': values,
                'backgroundColor': self.colors['deep_blue'],
                'borderWidth': 0
            }]
        })

        return f'''
    new Chart(document.getElementById('{chart_id}'), {{
        type: 'bar',
        data: {chart_data},
        options: {{
            responsive: true,
            plugins: {{
                legend: {{
                    display: false
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: true,
                    grid: {{
                        color: '#e0e0e0'
                    }}
                }},
                x: {{
                    grid: {{
                        display: false
                    }}
                }}
            }}
        }}
    }});'''


def main():
    generator = PresentationGenerator()

    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
            print("Usage: python generator.py <parsed_json_file> [output_path]")
            sys.exit(1)

        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            parsed_doc = json.load(f)

        output = sys.argv[2] if len(sys.argv) > 2 else 'presentation.html'
        result = generator.generate(parsed_doc, output)
        print(f"Generated presentation: {result}")


if __name__ == "__main__":
    main()
