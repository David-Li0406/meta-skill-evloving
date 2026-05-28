#!/usr/bin/env python3
"""
HTML Presentation Generator - Generate McKinsey-style HTML presentations from parsed documents.

Optimized version with:
- Inline CSS and JavaScript (single-file output)
- Improved data label extraction
- Smart chart type selection
- Enhanced chart configurations
"""

import json
import re
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
        """Generate a complete, self-contained HTML presentation."""

        # Load CSS and JavaScript
        css_content = self._get_css()
        js_content = self._get_js()

        # Generate slides and scripts
        slides_html = self._generate_slides(parsed_doc)
        chart_scripts = self._generate_chart_scripts(parsed_doc)

        # Build complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{parsed_doc.get('title', 'Presentation')}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
{css_content}
    </style>
</head>
<body>
    <nav class="navbar">
        <button class="nav-btn" id="prevBtn" onclick="navigate(-1)">← Previous</button>
        <span class="slide-counter">Slide <span id="currentSlide">1</span> of <span id="totalSlides">1</span></span>
        <button class="nav-btn" id="nextBtn" onclick="navigate(1)">Next →</button>
    </nav>

    <!-- Slides Container -->
    <div class="presentation-container">
{slides_html}
    </div>

    <button class="fullscreen-btn" onclick="toggleFullscreen()">⛶ Fullscreen</button>

    <script>
        let currentSlide = 1;
        let totalSlides = 0;

        function init() {{
            const slides = document.querySelectorAll('.slide');
            totalSlides = slides.length;
            document.getElementById('totalSlides').textContent = totalSlides;

            document.addEventListener('keydown', handleKeyPress);
        }}

        function navigate(direction) {{
            const newSlide = currentSlide + direction;

            if (newSlide >= 1 && newSlide <= totalSlides) {{
                document.querySelector(`.slide[data-slide="${{currentSlide}}"]`).classList.remove('active');
                currentSlide = newSlide;
                document.querySelector(`.slide[data-slide="${{currentSlide}}"]`).classList.add('active');
                document.getElementById('currentSlide').textContent = currentSlide;
                updateNavButtons();
            }}
        }}

        function handleKeyPress(e) {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                navigate(1);
            }} else if (e.key === 'ArrowLeft') {{
                navigate(-1);
            }} else if (e.key === 'Escape') {{
                if (document.fullscreenElement) {{
                    document.exitFullscreen();
                }}
            }}
        }}

        function updateNavButtons() {{
            document.getElementById('prevBtn').disabled = currentSlide === 1;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
        }}

        function toggleFullscreen() {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen();
            }} else {{
                document.exitFullscreen();
            }}
        }}

        document.addEventListener('DOMContentLoaded', init);

        // Chart.js configurations
{chart_scripts}
    </script>
</body>
</html>"""

        output = Path(output_path)
        output.write_text(html, encoding='utf-8')

        return str(output.absolute())

    def _get_css(self) -> str:
        """Return inline CSS for McKinsey-style design."""
        return """/* McKinsey/BCG Style Presentation CSS */

/* Color Variables */
:root {
    --primary-bg: #FFFFFF;
    --header-bg: #000000;
    --primary-accent: #F85d42;
    --secondary-accent: #74788d;
    --deep-blue: #556EE6;
    --green: #34c38f;
    --blue: #50a5f1;
    --yellow: #f1b44c;
    --text-primary: #000000;
    --text-secondary: #333333;
    --text-muted: #666666;
    --text-light: #FFFFFF;
}

/* Global Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--primary-bg);
    color: var(--text-secondary);
    line-height: 1.6;
    overflow: hidden;
}

/* Navigation Bar */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background-color: var(--header-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
    z-index: 1000;
}

.nav-btn {
    background-color: var(--primary-accent);
    color: var(--text-light);
    border: none;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.nav-btn:hover {
    background-color: #e04a31;
}

.nav-btn:disabled {
    background-color: var(--secondary-accent);
    cursor: not-allowed;
}

.slide-counter {
    color: var(--text-light);
    font-size: 18px;
    font-weight: 600;
}

/* Presentation Container */
.presentation-container {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
}

/* Slide Styles */
.slide {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 60px 80px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease, visibility 0.5s ease;
    overflow-y: auto;
}

.slide.active {
    opacity: 1;
    visibility: visible;
    z-index: 1;
}

/* Title Slide */
.title-slide {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.title {
    font-size: 64px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 30px;
    letter-spacing: -1px;
}

.subtitle {
    font-size: 36px;
    font-weight: 600;
    color: var(--primary-accent);
    margin-bottom: 20px;
}

.date {
    font-size: 20px;
    color: var(--secondary-accent);
    font-weight: 400;
}

/* Header Bar */
.header-bar {
    background-color: var(--header-bg);
    padding: 20px 40px;
    margin: -60px -80px 40px -80px;
}

.slide-title {
    font-size: 48px;
    font-weight: 700;
    color: var(--text-light);
    letter-spacing: -0.5px;
}

/* Slide Content */
.slide-content {
    max-width: 1400px;
    margin: 0 auto;
}

/* Key Points */
.key-points {
    list-style: none;
    padding: 0;
}

.key-point {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    padding: 20px 0;
    border-bottom: 2px solid var(--secondary-accent);
    margin-bottom: 10px;
}

.key-point::before {
    content: "✓ ";
    color: var(--primary-accent);
    margin-right: 15px;
    font-weight: 700;
}

/* Two-Column Layout */
.two-column {
    display: flex;
    gap: 60px;
    align-items: flex-start;
}

.column {
    flex: 1;
}

.chart-container {
    min-height: 400px;
}

.chart-caption {
    text-align: center;
    font-size: 14px;
    color: var(--secondary-accent);
    margin-top: 20px;
    font-weight: 600;
}

/* Section Header */
.section-header {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 20px;
}

.accent-text {
    color: var(--primary-accent);
}

/* Body Text */
.body-text {
    font-size: 18px;
    line-height: 1.8;
    color: var(--text-secondary);
    margin-bottom: 30px;
}

/* Bullet Points */
.bullet-points {
    list-style: none;
    padding: 0;
}

.bullet-points li {
    font-size: 18px;
    color: var(--text-secondary);
    padding: 12px 0 12px 30px;
    position: relative;
}

.bullet-points li::before {
    content: "•";
    color: var(--primary-accent);
    font-size: 24px;
    position: absolute;
    left: 0;
    top: 8px;
}

/* Conclusions Grid */
.conclusions-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin: 30px 0;
}

.conclusion-card {
    background-color: #f8f9fa;
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid var(--primary-accent);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 15px;
}

.card-text {
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-secondary);
}

/* Recommendations Box */
.recommendations-box {
    background-color: #fff3e0;
    padding: 30px;
    border-radius: 8px;
    border-left: 4px solid var(--yellow);
    margin: 30px 0;
}

/* Numbered List */
.numbered-list {
    list-style: none;
    counter-reset: recommendation-counter;
    padding: 0;
}

.numbered-list li {
    font-size: 18px;
    color: var(--text-secondary);
    padding: 15px 0 15px 40px;
    position: relative;
    counter-increment: recommendation-counter;
}

.numbered-list li::before {
    content: counter(recommendation-counter);
    background-color: var(--primary-accent);
    color: var(--text-light);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    position: absolute;
    left: 0;
    top: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
}

/* Full-screen Button */
.fullscreen-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: var(--header-bg);
    color: var(--text-light);
    border: none;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    z-index: 1001;
    transition: background-color 0.3s ease;
}

.fullscreen-btn:hover {
    background-color: var(--secondary-accent);
}

/* Responsive Design */
@media (max-width: 1200px) {
    .slide {
        padding: 60px 40px;
    }

    .two-column {
        flex-direction: column;
        gap: 40px;
    }

    .conclusions-grid {
        grid-template-columns: 1fr;
    }

    .title {
        font-size: 48px;
    }

    .slide-title {
        font-size: 36px;
    }
}

@media (max-width: 768px) {
    .navbar {
        padding: 0 20px;
    }

    .slide {
        padding: 40px 20px;
    }

    .title {
        font-size: 36px;
    }

    .slide-title {
        font-size: 28px;
    }

    .subtitle {
        font-size: 24px;
    }

    .key-point {
        font-size: 18px;
    }
}

/* Scrollbar Styles */
.slide::-webkit-scrollbar {
    width: 8px;
}

.slide::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.slide::-webkit-scrollbar-thumb {
    background: var(--secondary-accent);
    border-radius: 4px;
}

.slide::-webkit-scrollbar-thumb:hover {
    background: var(--primary-accent);
}"""

    def _get_js(self) -> str:
        """Return inline JavaScript for navigation and interactivity."""
        return """let currentSlide = 1;
let totalSlides = 0;

function init() {
    const slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;
    document.getElementById('totalSlides').textContent = totalSlides;

    document.addEventListener('keydown', handleKeyPress);
}

function navigate(direction) {
    const newSlide = currentSlide + direction;

    if (newSlide >= 1 && newSlide <= totalSlides) {
        document.querySelector(`.slide[data-slide="${currentSlide}"]`).classList.remove('active');
        currentSlide = newSlide;
        document.querySelector(`.slide[data-slide="${currentSlide}"]`).classList.add('active');
        document.getElementById('currentSlide').textContent = currentSlide;
        updateNavButtons();
    }
}

function handleKeyPress(e) {
    if (e.key === 'ArrowRight' || e.key === ' ') {
        navigate(1);
    } else if (e.key === 'ArrowLeft') {
        navigate(-1);
    } else if (e.key === 'Escape') {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        }
    }
}

function updateNavButtons() {
    document.getElementById('prevBtn').disabled = currentSlide === 1;
    document.getElementById('nextBtn').disabled = currentSlide === totalSlides;
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

document.addEventListener('DOMContentLoaded', init);"""

    def _generate_slides(self, doc: Dict[str, Any]) -> str:
        """Generate all slide HTML."""
        slides = []

        title = doc.get('title', 'Untitled')
        sections = doc.get('sections', [])
        data_points = doc.get('data_points', [])
        conclusions = doc.get('conclusions', [])

        slide_num = 1

        # Title slide
        slide_num = self._add_title_slide(slides, slide_num, title)

        # Executive summary
        slide_num = self._add_executive_summary(slides, slide_num, conclusions)

        # Data slides with charts
        slide_num = self._add_data_slides(slides, slide_num, data_points, sections)

        # Detailed slides
        slide_num = self._add_detailed_slides(slides, slide_num, sections)

        # Conclusions and recommendations
        slide_num = self._add_conclusions(slides, slide_num, conclusions)

        return '\n'.join(slides)

    def _add_title_slide(self, slides: List[str], slide_num: int, title: str) -> int:
        """Add title slide."""
        date_str = datetime.now().strftime('%B %Y')

        slide = f'''        <div class="slide active" data-slide="{slide_num}">
            <div class="title-slide">
                <h1 class="title">{title}</h1>
                <h2 class="subtitle">Data Analysis & Insights</h2>
                <p class="date">Date: {date_str}</p>
            </div>
        </div>'''
        slides.append(slide)
        return slide_num + 1

    def _add_executive_summary(self, slides: List[str], slide_num: int, conclusions: List[Dict]) -> int:
        """Add executive summary slide."""
        top_conclusions = conclusions[:5] if len(conclusions) > 5 else conclusions

        points_html = ''
        for conc in top_conclusions:
            text = conc.get('text', conc) if isinstance(conc, dict) else str(conc)
            points_html += f'                <li class="key-point">{text}</li>\n'

        slide = f'''        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">Executive Summary</h1>
            </div>
            <div class="slide-content">
                <ul class="key-points">
{points_html}                </ul>
            </div>
        </div>'''
        slides.append(slide)
        return slide_num + 1

    def _add_data_slides(
        self,
        slides: List[str],
        slide_num: int,
        data_points: List[Dict],
        sections: List[Dict]
    ) -> int:
        """Add data visualization slides."""
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
            insights = self._extract_insights(section)
            chart_type = self._determine_chart_type(section_data)

            insights_html = '\n                    '.join([
                f'<li>{insight.strip()}</li>' for insight in insights if insight.strip()
            ])

            slide = f'''        <div class="slide" data-slide="{slide_num}">
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
                        <li>{insights_html}</li>
                    </ul>
                </div>
            </div>
        </div>'''
            slides.append(slide)
            slide_num += 1

        return slide_num

    def _add_detailed_slides(self, slides: List[str], slide_num: int, sections: List[Dict]) -> int:
        """Add detailed content slides."""
        for section in sections[3:]:
            if not section.get('content', '').strip():
                continue

            content_lines = section.get('content', '').split('\n')
            content_html = '\n            '.join([
                f'<p class="body-text">{line.strip()}</p>' for line in content_lines if line.strip() and len(line.strip()) > 20
            ])

            slide = f'''        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{section.get('title', 'Detailed Findings')}</h1>
            </div>
            <div class="slide-content">
            {content_html}
            </div>
        </div>'''
            slides.append(slide)
            slide_num += 1

        return slide_num

    def _add_conclusions(self, slides: List[str], slide_num: int, conclusions: List[Dict]) -> int:
        """Add conclusions and recommendations slide."""
        if not conclusions:
            return slide_num

        conclusions_html = ''
        for i, conc in enumerate(conclusions[:6]):
            text = conc.get('text', conc) if isinstance(conc, dict) else str(conc)
            conclusions_html += f'''                <div class="conclusion-card">
                    <h3 class="card-title">Conclusion {i+1}</h3>
                    <p class="card-text">{text}</p>
                </div>
'''

        recommendations_html = '\n                    '.join([
            f'<li>{(rec.get("text", rec) if isinstance(rec, dict) else str(rec)).strip()}</li>'
            for rec in conclusions[:5]
        ])

        slide = f'''        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">Conclusions & Recommendations</h1>
            </div>
            <div class="slide-content">
                <div class="conclusions-grid">
{conclusions_html}                </div>

                <div class="recommendations-box">
                    <h3 class="section-header accent-text">Key Recommendations</h3>
                    <ol class="numbered-list">
                        <li>{recommendations_html}</li>
                    </ol>
                </div>
            </div>
        </div>'''
        slides.append(slide)
        return slide_num + 1

    def _generate_chart_scripts(self, doc: Dict[str, Any]) -> str:
        """Generate Chart.js initialization scripts."""
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

        return '\n\n'.join(chart_scripts)

    def _generate_chart_script(self, chart_id: str, data_points: List[Dict]) -> str:
        """Generate Chart.js configuration for a single chart."""
        # Extract better labels from the data
        labels = self._extract_chart_labels(data_points[:10])
        values = [dp.get('value', 0) for dp in data_points[:10]]

        # Determine chart type
        chart_type = self._determine_chart_type(data_points)

        # Build chart configuration
        chart_data = json.dumps({
            'labels': labels,
            'datasets': [{
                'label': 'Value',
                'data': values,
                'backgroundColor': [
                    self.colors['deep_blue'],
                    self.colors['green'],
                    self.colors['blue'],
                    self.colors['yellow'],
                    self.colors['primary']
                ] * 2,
                'borderWidth': 0,
                'borderRadius': 4
            }]
        })

        options = {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'display': chart_type == 'pie'
                },
                'tooltip': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.8)',
                    'padding': 12,
                    'titleFont': {'size': 14, 'weight': 'bold'},
                    'bodyFont': {'size': 13}
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'},
                    'ticks': {'font': {'size': 12}}
                } if chart_type != 'pie' else {},
                'x': {
                    'grid': {'display': False},
                    'ticks': {'font': {'size': 11}}
                } if chart_type != 'pie' else {}
            }
        }

        options_json = json.dumps(options, indent=8)

        return f'''new Chart(document.getElementById('{chart_id}'), {{
        type: '{chart_type}',
        data: {chart_data},
        options: {options_json}
    }});'''

    def _extract_chart_labels(self, data_points: List[Dict]) -> List[str]:
        """Extract meaningful labels from data points."""
        labels = []

        for i, dp in enumerate(data_points):
            # Try to get a meaningful label
            label = dp.get('label', '')

            # If label is generic, try to create one from context
            if not label or 'Data Point' in label:
                unit = dp.get('unit', '')
                value = dp.get('value', 0)

                if unit == '%':
                    label = f'Percentage {i+1}'
                elif unit in ['$', 'k', 'm', 'b']:
                    label = f'Metric {i+1}'
                else:
                    label = f'Item {i+1}'

            labels.append(label)

        return labels

    def _extract_insights(self, section: Dict) -> List[str]:
        """Extract key insights from section content."""
        content = section.get('content', '')
        lines = content.split('\n')

        # Filter out empty lines and very short lines
        insights = [line.strip() for line in lines if line.strip() and len(line.strip()) > 20]

        return insights[:3] if insights else ['Key insights from the data analysis']

    def _determine_chart_type(self, data_points: List[Dict]) -> str:
        """
        Determine the best chart type based on data characteristics.

        Returns:
            'bar' for comparisons (default)
            'line' for trends/time series
            'pie' for proportions/percentages
        """
        if not data_points:
            return 'bar'

        # Check if data is mostly percentages (good for pie chart)
        percent_count = sum(1 for dp in data_points if dp.get('unit') == '%')
        if len(data_points) <= 5 and percent_count == len(data_points):
            return 'pie'

        # Check for time series patterns (could use line chart)
        # For now, default to bar chart
        return 'bar'


def main():
    generator = PresentationGenerator()

    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
            print("Usage: python generator_optimized.py <parsed_json_file> [output_path]")
            sys.exit(1)

        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            parsed_doc = json.load(f)

        output = sys.argv[2] if len(sys.argv) > 2 else 'presentation.html'
        result = generator.generate(parsed_doc, output)
        print(f"Generated presentation: {result}")


if __name__ == "__main__":
    main()
