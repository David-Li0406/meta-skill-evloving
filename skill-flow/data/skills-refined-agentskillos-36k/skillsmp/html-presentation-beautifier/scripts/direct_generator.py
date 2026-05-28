#!/usr/bin/env python3
"""
Direct HTML Generator - Generate McKinsey-style HTML from SlideSpec objects.

This module generates complete, self-contained HTML presentations from slide
specifications, eliminating the need for JSON serialization.
"""

import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from data_structures import SlideSpec, SlideType, SlidePlan


class DirectGenerator:
    """Generate HTML presentations directly from slide specifications."""

    def __init__(self):
        self.colors = {
            'primary': '#F85d42',
            'secondary': '#74788d',
            'deep_blue': '#556EE6',
            'green': '#34c38f',
            'blue': '#50a5f1',
            'yellow': '#f1b44c'
        }
        self._chart_counter = 0

    def generate(
        self,
        slide_plan: SlidePlan,
        output_path: str = 'presentation.html'
    ) -> str:
        """Generate a complete, self-contained HTML presentation.

        Args:
            slide_plan: SlidePlan containing list of SlideSpec objects
            output_path: Where to save the HTML file

        Returns:
            Absolute path to the generated HTML file
        """
        # Reset chart counter
        self._chart_counter = 0

        # Load CSS and JavaScript
        css_content = self._get_css()
        js_content = self._get_js()

        # Generate slides and chart scripts
        slides_html = self._generate_slides(slide_plan.slides)
        chart_scripts = self._generate_chart_scripts(slide_plan.slides)

        # Build complete HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_plan.title}</title>
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

    def _generate_slides(self, slides: List[SlideSpec]) -> str:
        """Generate all slide HTML."""
        slides_html = []

        for i, slide in enumerate(slides):
            slide_num = i + 1
            active_class = 'active' if i == 0 else ''

            if slide.slide_type == SlideType.TITLE:
                slides_html.append(self._render_title_slide(slide, slide_num, active_class))
            elif slide.slide_type == SlideType.EXECUTIVE_SUMMARY:
                slides_html.append(self._render_executive_summary(slide, slide_num, active_class))
            elif slide.slide_type == SlideType.DATA_VISUALIZATION:
                slides_html.append(self._render_data_slide(slide, slide_num, active_class))
            elif slide.slide_type == SlideType.CONCEPTUAL:
                slides_html.append(self._render_conceptual_slide(slide, slide_num, active_class))
            elif slide.slide_type == SlideType.CONTENT:
                slides_html.append(self._render_content_slide(slide, slide_num, active_class))
            elif slide.slide_type == SlideType.CONCLUSIONS:
                slides_html.append(self._render_conclusions_slide(slide, slide_num, active_class))

        return '\n'.join(slides_html)

    def _render_title_slide(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render title slide."""
        date_str = datetime.now().strftime('%B %Y')

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="title-slide">
                <h1 class="title">{slide.title}</h1>
                <h2 class="subtitle">Data Analysis & Insights</h2>
                <p class="date">Date: {date_str}</p>
            </div>
        </div>'''

    def _render_executive_summary(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render executive summary slide."""
        points_html = ''
        for point in slide.key_points or []:
            points_html += f'                <li class="key-point">{point}</li>\n'

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{slide.title}</h1>
            </div>
            <div class="slide-content">
                <ul class="key-points">
{points_html}                </ul>
            </div>
        </div>'''

    def _render_data_slide(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render data visualization slide with chart."""
        self._chart_counter += 1
        chart_id = f"chart{self._chart_counter}"
        chart_container_class = self._get_chart_container_class(slide.chart_type or 'bar')
        chart_type_name = self._get_chart_type_display_name(slide.chart_type or 'bar')

        insights_html = '\n                    '.join([
            f'<li>{insight.strip()}</li>' for insight in (slide.key_points or [])
    ])

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{slide.title}</h1>
            </div>
            <div class="slide-content two-column">
                <div class="column {chart_container_class}">
                    <span class="chart-type-badge">{chart_type_name}</span>
                    <canvas id="{chart_id}" style="height: 400px !important; max-height: 400px;"></canvas>
                    <p class="chart-caption">{slide.title} - Smart Chart Selection</p>
                </div>
                <div class="column">
                    <h3 class="section-header">Key Insights</h3>
                    <ul class="bullet-points">
                        <li>{insights_html}</li>
                    </ul>
                </div>
            </div>
        </div>'''

    def _render_conceptual_slide(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render conceptual visualization slide."""
        conceptual_viz = self._render_conceptual_visualization(slide)
        conceptual_name = self._get_conceptual_viz_name(slide.conceptual_type or 'emphasis')

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{slide.title}</h1>
            </div>
            <div class="slide-content">
                <span class="chart-type-badge">{conceptual_name}</span>
                {conceptual_viz}
            </div>
        </div>'''

    def _render_content_slide(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render regular content slide."""
        content_lines = slide.content.split('\n')
        content_html = '\n            '.join([
            f'<p class="body-text">{line.strip()}</p>' for line in content_lines if line.strip() and len(line.strip()) > 20
        ])

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{slide.title}</h1>
            </div>
            <div class="slide-content">
            {content_html}
            </div>
        </div>'''

    def _render_conclusions_slide(self, slide: SlideSpec, slide_num: int, active_class: str) -> str:
        """Render conclusions and recommendations slide."""
        conclusions_html = ''
        for i, point in enumerate((slide.key_points or [])[:6]):
            conclusions_html += f'''                <div class="conclusion-card">
                    <h3 class="card-title">Conclusion {i+1}</h3>
                    <p class="card-text">{point}</p>
                </div>
'''

        recommendations_html = '\n                    '.join([
            f'<li>{rec.strip()}</li>' for rec in (slide.key_points or [])[:5]
        ])

        return f'''        <div class="slide {active_class}" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{slide.title}</h1>
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

    def _generate_chart_scripts(self, slides: List[SlideSpec]) -> str:
        """Generate Chart.js initialization scripts."""
        chart_scripts = []
        self._chart_counter = 0

        for slide in slides:
            if slide.slide_type == SlideType.DATA_VISUALIZATION and slide.data_points:
                self._chart_counter += 1
                chart_id = f"chart{self._chart_counter}"
                chart_scripts.append(self._generate_chart_script(chart_id, slide))

        return '\n\n'.join(chart_scripts)

    def _generate_chart_script(self, chart_id: str, slide: SlideSpec) -> str:
        """Generate Chart.js configuration for a single chart."""
        data_points = slide.data_points or []

        # Extract labels and values
        labels = [dp.get('label', f'Point {i+1}') for i, dp in enumerate(data_points[:10])]
        values = [dp.get('value', 0) for dp in data_points[:10]]

        # Build chart data and options
        chart_type = slide.chart_type or 'bar'
        chart_data = self._build_chart_data(chart_type, labels, values, data_points)
        options = self._build_chart_options(chart_type, data_points)

        chart_data_json = json.dumps(chart_data, indent=8)
        options_json = json.dumps(options, indent=8)

        return f'''new Chart(document.getElementById('{chart_id}'), {{
        type: '{chart_type}',
        data: {chart_data_json},
        options: {options_json}
    }});'''

    def _build_chart_data(self, chart_type: str, labels: List[str], values: List[float], data_points: List[Dict]) -> Dict:
        """Build chart data configuration."""
        # Generate color palette
        colors = [
            '#F85d42', '#556EE6', '#34c38f', '#50a5f1', '#f1b44c',
            '#74788d', '#F85d42', '#556EE6', '#34c38f', '#50a5f1'
        ]
        bg_colors = colors[:len(values)]
        border_colors = bg_colors

        if chart_type in ['line', 'radar']:
            bg_colors = [self.colors['deep_blue']] + ['rgba(85, 110, 230, 0.1)'] * (len(values) - 1)
            border_colors = [self.colors['deep_blue']] * len(values)

        return {
            'labels': labels,
            'datasets': [{
                'label': 'Value',
                'data': values,
                'backgroundColor': bg_colors,
                'borderColor': border_colors,
                'borderWidth': 2
            }]
        }

    def _build_chart_options(self, chart_type: str, data_points: List[Dict]) -> Dict:
        """Build chart options based on chart type."""
        base_options = {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'display': chart_type in ['pie', 'doughnut', 'polarArea'],
                    'position': 'bottom'
                },
                'tooltip': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.8)',
                    'padding': 12,
                    'titleFont': {'size': 14, 'weight': 'bold'},
                    'bodyFont': {'size': 12}
                }
            }
        }

        if chart_type in ['bar', 'line']:
            base_options['scales'] = {
                'y': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'}
                },
                'x': {
                    'grid': {'display': False}
                }
            }

        return base_options

    def _render_conceptual_visualization(self, slide: SlideSpec) -> str:
        """Render conceptual visualization HTML based on type."""
        viz_type = slide.conceptual_type or 'emphasis'
        key_points = slide.key_points or []

        if viz_type == 'pyramid':
            return self._render_pyramid(key_points, slide.title)
        elif viz_type == 'progression':
            return self._render_progression(key_points, slide.title)
        elif viz_type == 'emphasis':
            return self._render_emphasis(key_points, slide.title)
        elif viz_type == 'cycle':
            return self._render_cycle(key_points, slide.title)
        elif viz_type == 'comparison':
            return self._render_comparison(key_points, slide.title)
        elif viz_type == 'framework':
            return self._render_framework(key_points, slide.title)
        else:
            return self._render_emphasis(key_points, slide.title)

    def _render_pyramid(self, points: List[str], title: str) -> str:
        """Render pyramid visualization."""
        if not points:
            return '<p class="body-text">No content available for pyramid visualization</p>'

        width_percentages = [100 - (i * 15) for i in range(len(points))]
        colors = [
            'background-color: var(--primary-accent);',
            'background-color: var(--deep-blue);',
            'background-color: var(--green);',
            'background-color: var(--blue);',
            'background-color: var(--yellow);'
        ]

        pyramid_html = '<div class="pyramid-container">\n'
        for point, width, color in zip(points, width_percentages, colors):
            pyramid_html += f'''            <div class="pyramid-level" style="width: {width}%; {color} margin: 0 auto 8px;">
                <div class="pyramid-text">{point}</div>
            </div>\n'''
        pyramid_html += '        </div>'

        return pyramid_html

    def _render_progression(self, points: List[str], title: str) -> str:
        """Render progression/step visualization."""
        if not points:
            return '<p class="body-text">No content available for progression visualization</p>'

        progression_html = '<div class="progression-container">\n'
        for i, point in enumerate(points, 1):
            progression_html += f'''            <div class="progression-step">
                <div class="step-number">{i}</div>
                <div class="step-content">{point}</div>
                {'' if i == len(points) else '<div class="step-arrow">→</div>'}
            </div>\n'''
        progression_html += '        </div>'

        return progression_html

    def _render_emphasis(self, points: List[str], title: str) -> str:
        """Render emphasis box visualization."""
        if not points:
            return '<p class="body-text">No content available for emphasis visualization</p>'

        emphasis_html = '<div class="emphasis-container">\n'
        for i, point in enumerate(points, 1):
            emphasis_html += f'''            <div class="emphasis-box" style="animation-delay: {i * 0.1}s;">
                <div class="emphasis-icon">✦</div>
                <div class="emphasis-text">{point}</div>
            </div>\n'''
        emphasis_html += '        </div>'

        return emphasis_html

    def _render_cycle(self, points: List[str], title: str) -> str:
        """Render cycle/circle visualization."""
        if not points:
            return '<p class="body-text">No content available for cycle visualization</p>'

        colors = [
            'var(--primary-accent)',
            'var(--deep-blue)',
            'var(--green)',
            'var(--blue)',
            'var(--yellow)'
        ]

        cycle_html = '<div class="cycle-container">\n'
        cycle_html += '            <div class="cycle-center">核心</div>\n'
        for i, (point, color) in enumerate(zip(points, colors)):
            angle = (360 / len(points)) * i
            cycle_html += f'''            <div class="cycle-node" style="transform: rotate({angle}deg) translate(120px) rotate(-{angle}deg); background-color: {color};">
                <div class="cycle-text">{point}</div>
            </div>\n'''
        cycle_html += '        </div>'

        return cycle_html

    def _render_comparison(self, points: List[str], title: str) -> str:
        """Render before/after or pros/cons comparison."""
        if not points:
            return '<p class="body-text">No content available for comparison visualization</p>'

        mid = len(points) // 2
        left_points = points[:mid]
        right_points = points[mid:]

        comparison_html = '''        <div class="comparison-container">
            <div class="comparison-column">
                <h4 class="comparison-header">当前 / Before</h4>
'''
        for point in left_points:
            comparison_html += f'                <div class="comparison-item left">{point}</div>\n'

        comparison_html += '            </div>\n            <div class="comparison-divider">VS</div>\n            <div class="comparison-column">\n                <h4 class="comparison-header">目标 / After</h4>\n'

        for point in right_points:
            comparison_html += f'                <div class="comparison-item right">{point}</div>\n'

        comparison_html += '            </div>\n        </div>'

        return comparison_html

    def _render_framework(self, points: List[str], title: str) -> str:
        """Render framework visualization."""
        if not points:
            return '<p class="body-text">No content available for framework visualization</p>'

        framework_html = '<div class="framework-container">\n'
        for i, point in enumerate(points, 1):
            framework_html += f'''            <div class="framework-item">
                <div class="framework-label">{i}</div>
                <div class="framework-content">{point}</div>
            </div>\n'''
        framework_html += '        </div>'

        return framework_html

    # ===== Helper Methods =====

    def _get_chart_container_class(self, chart_type: str) -> str:
        """Get CSS class for chart container based on chart type."""
        class_map = {
            'radar': 'chart-container radar-chart',
            'bubble': 'chart-container bubble-chart',
            'scatter': 'chart-container bubble-chart',
            'polarArea': 'chart-container polar-chart',
            'doughnut': 'chart-container',
            'pie': 'chart-container',
            'line': 'chart-container',
            'bar': 'chart-container'
        }
        return class_map.get(chart_type, 'chart-container')

    def _get_chart_type_display_name(self, chart_type: str) -> str:
        """Get display name for chart type."""
        name_map = {
            'bar': '柱状图 (Bar Chart)',
            'line': '折线图 (Line Chart)',
            'pie': '饼图 (Pie Chart)',
            'doughnut': '环形图 (Doughnut Chart)',
            'radar': '雷达图 (Radar Chart)',
            'polarArea': '玫瑰图 (Polar Area Chart)',
            'bubble': '气泡图 (Bubble Chart)',
            'scatter': '散点图 (Scatter Plot)'
        }
        return name_map.get(chart_type, '数据可视化 (Chart)')

    def _get_conceptual_viz_name(self, viz_type: str) -> str:
        """Get display name for conceptual visualization type."""
        name_map = {
            'pyramid': '金字塔图 (Pyramid)',
            'progression': '递进图 (Progression)',
            'emphasis': '强调框 (Emphasis)',
            'cycle': '循环图 (Cycle)',
            'comparison': '对比图 (Comparison)',
            'framework': '框架图 (Framework)'
        }
        return name_map.get(viz_type, '概念可视化 (Conceptual)')

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
    height: 100vh;
    width: 100vw;
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
    max-height: calc(100vh - 60px);
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
    max-height: calc(100vh - 60px);
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
    max-height: 450px;
    position: relative;
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
}

/* Special Chart Type Styles */
.chart-container.radar-chart {
    min-height: 450px;
    max-height: 500px;
}

.chart-container.bubble-chart {
    min-height: 450px;
    max-height: 500px;
}

.chart-container.polar-chart {
    min-height: 450px;
    max-height: 500px;
}

/* Chart Type Badge */
.chart-type-badge {
    display: inline-block;
    background-color: var(--secondary-accent);
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* ===== Conceptual Visualization Styles ===== */

/* Pyramid Container */
.pyramid-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
    min-height: 400px;
}

.pyramid-level {
    padding: 15px 30px;
    color: white;
    text-align: center;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    max-width: 80%;
}

.pyramid-level:hover {
    transform: scale(1.05);
}

.pyramid-text {
    color: white;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Progression/Step Container */
.progression-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    padding: 40px 20px;
    flex-wrap: wrap;
}

.progression-step {
    display: flex;
    align-items: center;
    gap: 15px;
    flex: 1;
    min-width: 200px;
}

.step-number {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary-accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 700;
    flex-shrink: 0;
}

.step-content {
    flex: 1;
    font-size: 16px;
    color: var(--text-secondary);
    background-color: #f8f9fa;
    padding: 15px 20px;
    border-radius: 8px;
    border-left: 4px solid var(--primary-accent);
}

.step-arrow {
    font-size: 32px;
    color: var(--secondary-accent);
    font-weight: 700;
    flex-shrink: 0;
}

/* Emphasis Box Container */
.emphasis-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 30px;
    max-width: 1200px;
    margin: 0 auto;
}

.emphasis-box {
    display: flex;
    align-items: center;
    gap: 20px;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 25px 30px;
    border-radius: 12px;
    border-left: 6px solid var(--primary-accent);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.emphasis-box:hover {
    transform: translateX(10px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.emphasis-icon {
    font-size: 36px;
    color: var(--primary-accent);
    flex-shrink: 0;
}

.emphasis-text {
    flex: 1;
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
}

/* Cycle/Circle Container */
.cycle-container {
    position: relative;
    width: 100%;
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}

.cycle-center {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: var(--header-bg);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    z-index: 10;
}

.cycle-node {
    position: absolute;
    padding: 20px;
    border-radius: 50%;
    color: white;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease;
    max-width: 150px;
}

.cycle-node:hover {
    transform: scale(1.15) !important;
    z-index: 20;
}

.cycle-text {
    font-size: 14px;
    line-height: 1.4;
}

/* Comparison Container */
.comparison-container {
    display: flex;
    align-items: stretch;
    gap: 30px;
    padding: 40px 20px;
    min-height: 400px;
}

.comparison-column {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.comparison-header {
    font-size: 24px;
    font-weight: 700;
    color: var(--primary-accent);
    text-align: center;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 10px;
}

.comparison-item {
    padding: 20px;
    border-radius: 8px;
    font-size: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.comparison-item.left {
    background-color: #e3f2fd;
    border-left: 4px solid var(--blue);
}

.comparison-item.right {
    background-color: #e8f5e9;
    border-left: 4px solid var(--green);
}

.comparison-divider {
    display: flex;
    align-items: center;
    font-size: 32px;
    font-weight: 900;
    color: var(--primary-accent);
    padding: 0 20px;
}

/* Framework Container */
.framework-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
    padding: 30px;
    max-width: 1400px;
    margin: 0 auto;
}

.framework-item {
    display: flex;
    gap: 20px;
    padding: 25px;
    background-color: #f8f9fa;
    border-radius: 12px;
    border-top: 5px solid var(--deep-blue);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.framework-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.framework-label {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background-color: var(--deep-blue);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    font-weight: 700;
    flex-shrink: 0;
}

.framework-content {
    flex: 1;
    font-size: 16px;
    color: var(--text-secondary);
    line-height: 1.6;
}

/* Responsive adjustments for conceptual visualizations */
@media (max-width: 1200px) {
    .progression-container {
        flex-direction: column;
    }

    .progression-step {
        width: 100%;
    }

    .comparison-container {
        flex-direction: column;
    }

    .comparison-divider {
        transform: rotate(90deg);
    }

    .cycle-container {
        height: 350px;
    }

    .framework-container {
        grid-template-columns: 1fr;
    }
}
"""

    def _get_js(self) -> str:
        """Return inline JavaScript for interactivity."""
        return """// Navigation and interactivity are already included in the main HTML template
// This is a placeholder for any additional JavaScript needed
"""


def main():
    """Command-line interface for testing."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python direct_generator.py <slide_plan_file> <output_html>")
        sys.exit(1)

    # For testing, you would need to load a SlidePlan from a file
    # This is just a placeholder
    print("DirectGenerator - generates HTML from SlidePlan objects")


if __name__ == "__main__":
    main()
