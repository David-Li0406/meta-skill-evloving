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
/* Radar Chart Container */
.chart-container.radar-chart {
    min-height: 450px;
    max-height: 500px;
}

/* Bubble Chart Container */
.chart-container.bubble-chart {
    min-height: 450px;
    max-height: 500px;
}

/* Polar Area Chart Container */
.chart-container.polar-chart {
    min-height: 450px;
    max-height: 500px;
}

/* Doughnut Chart Container - Center Text */
.doughnut-center-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    pointer-events: none;
}

.doughnut-center-value {
    font-size: 48px;
    font-weight: 700;
    color: var(--text-primary);
}

/* ===== ENHANCED VISUAL DESIGN - PHASE 3 ===== */

/* Enhanced Typography */
.slide-title {
    font-size: 48px;
    font-weight: 700;
    color: var(--text-light);
    letter-spacing: 0.5px;
    line-height: 1.2;
}

.section-header {
    font-size: 28px;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.5;
    letter-spacing: 0.3px;
}

.body-text {
    font-size: 18px;
    line-height: 1.8;
    letter-spacing: 0.2px;
}

.bullet-points li, .numbered-list li {
    font-size: 18px;
    line-height: 1.6;
}

.chart-caption {
    font-size: 14px;
    color: var(--secondary-accent);
    margin-top: 20px;
    font-weight: 600;
    letter-spacing: 0.5px;
    line-height: 1.6;
    text-align: center;
}

/* Enhanced Animations */
@keyframes chartEntryUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes chartEntryLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.chart-container {
    animation: chartEntryUp 0.6s ease-out;
}

.chart-container.bar-chart {
    animation: chartEntryLeft 0.6s ease-out;
}

.chart-container.pie-chart {
    animation: chartEntryUp 0.8s ease-out;
}

.data-point:hover {
    animation: pulse 1s ease-in-out infinite;
}

/* Colorblind-Safe Palettes */
.colorblind-viridis {
    --cb-1: #440154;
    --cb-2: #31688e;
    --cb-3: #35b779;
    --cb-4: #fde725;
    --cb-5: #f0f921;
}

.colorblind-plasma {
    --cb-1: #0d0887;
    --cb-2: #6a00a8;
    --cb-3: #b12a9b;
    --cb-4: #e16462;
    --cb-5: #fca636;
}

.colorblind-cividis {
    --cb-1: #003c30;
    --cb-2: #54986b;
    --cb-3: #b1b29b;
    --cb-4: #fec52d;
    --cb-5: #ffffe0;
}

/* Apply colorblind palette to charts */
.chart-container.colorblind-viridis canvas,
.chart-container.colorblind-viridis .chartjs-render-monitor {
    --primary-accent: var(--cb-1);
    --deep-blue: var(--cb-2);
    --green: var(--cb-3);
    --blue: var(--cb-4);
    --yellow: var(--cb-5);
}

/* Enhanced Tooltip Styling */
#chartjs-tooltip {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    background: rgba(0, 0, 0, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#chartjs-tooltip .tooltip-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-light);
    margin-bottom: 6px;
}

#chartjs-tooltip .tooltip-body {
    font-size: 14px;
    color: var(--text-light);
    line-height: 1.5;
}

/* ===== RESPONSIVE DESIGN - PHASE 6 ===== */

/* Mobile Portrait (<480px) */
@media (max-width: 480px) {
    .chart-container {
        min-height: 250px !important;
        max-height: 300px !important;
    }
    
    .chart-caption {
        font-size: 12px;
    }
    
    /* Horizontal bars on mobile for better readability */
    .chart-container[data-chart-type="bar"] canvas {
        writing-mode: horizontal-tb;
    }
    
    /* Hide legend/data labels on mobile */
    .chartjs-plugin-legend,
    .chartjs-plugin-datalabels {
        display: none;
    }
    
    /* Mobile navigation adjustments */
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
}

/* Mobile Landscape (481-767px) */
@media (min-width: 481px) and (max-width: 767px) {
    .chart-container {
        min-height: 300px !important;
        max-height: 350px !important;
    }
}

/* Tablet (768-1024px) */
@media (min-width: 768px) and (max-width: 1024px) {
    .two-column {
        flex-direction: column;
        gap: 30px;
    }
    
    .chart-container {
        min-height: 350px !important;
        max-height: 400px !important;
    }
    
    .chartjs-plugin-legend {
        position: 'bottom';
        labels: {
            box-width: 12px;
            padding: 10px;
            font: {
                size: 11px;
            }
        }
    }
}

/* Desktop (>1024px) */
@media (min-width: 1025px) {
    .chart-container {
        min-height: 400px !important;
        max-height: 450px !important;
    }
    
    .chart-caption {
        font-size: 16px;
    }
}

/* Ultra-wide screens (>1600px) */
@media (min-width: 1600px) {
    .chart-container {
        max-height: 500px !important;
    }
    
    .chart-caption {
        font-size: 16px;
    }
}

/* ===== ACCESSIBILITY - PHASE 4 ===== */

/* ARIA labels and roles */
canvas {
    role: img;
}

.canvas-data-table {
    display: none;
}

canvas[aria-describedby] + .canvas-data-table {
    display: block;
    margin-top: 20px;
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
    line-height: 1.6;
}

.canvas-data-table thead {
    background-color: var(--header-bg);
    color: var(--text-light);
}

.canvas-data-table th {
    padding: 12px;
    text-align: left;
    font-weight: 600;
}

.canvas-data-table tbody tr {
    border-bottom: 1px solid var(--secondary-accent);
}

.canvas-data-table td {
    padding: 10px;
    border-right: 1px solid #e0e0e0;
}

.canvas-data-table td:last-child {
    border-right: none;
}

.canvas-data-table tr:last-child {
    border-bottom: none;
}

/* Keyboard navigation focus styles */
.chart-wrapper:focus,
.chart-container:focus {
    outline: 3px solid var(--primary-accent);
    outline-offset: 2px;
    border-radius: 4px;
}

.chart-wrapper:focus-visible {
    outline: 3px solid var(--primary-accent);
    animation: focusPulse 1s ease-in-out;
}

@keyframes focusPulse {
    0%, 100% {
        outline-color: var(--primary-accent);
        outline-width: 3px;
    }
    50% {
        outline-color: var(--deep-blue);
        outline-width: 5px;
    }
}

/* ===== PERFORMANCE - PHASE 5 ===== */

/* Lazy loading styles */
.chart-lazy {
    position: relative;
    min-height: 400px;
}

.chart-lazy[data-loaded="false"] {
    opacity: 0.6;
    transition: opacity 0.3s ease;
}

.chart-lazy[data-loaded="true"] {
    opacity: 1;
}

.chart-loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    color: var(--secondary-accent);
}

.chart-loading-indicator .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--secondary-accent);
    border-top: 4px solid var(--primary-accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
        border-top-color: var(--secondary-accent);
        border-right-color: var(--secondary-accent);
    }
    25% {
        transform: rotate(90deg);
        border-top-color: var(--primary-accent);
        border-right-color: var(--secondary-accent);
    }
    50% {
        transform: rotate(180deg);
        border-top-color: var(--secondary-accent);
        border-right-color: var(--secondary-accent);
    }
    75% {
        transform: rotate(270deg);
        border-top-color: var(--primary-accent);
        border-right-color: var(--secondary-accent);
    }
    100% {
        transform: rotate(360deg);
        border-top-color: var(--secondary-accent);
        border-right-color: var(--secondary-accent);
    }
}

.doughnut-center-label {
    font-size: 16px;
    color: var(--secondary-accent);
    margin-top: 5px;
}

/* Multi-Chart Layout */
.multi-chart-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
    margin: 20px 0;
}

.multi-chart-grid.three-col {
    grid-template-columns: repeat(3, 1fr);
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

/* Comparison Chart Styles */
.comparison-bar-positive {
    background-color: var(--green);
}

.comparison-bar-negative {
    background-color: var(--primary);
}

/* Matrix Chart Container */
.matrix-chart-container {
    min-height: 500px;
    max-height: 550px;
    position: relative;
}

/* Heatmap Styles */
.heatmap-cell {
    border-radius: 2px;
    transition: opacity 0.2s;
}

.heatmap-cell:hover {
    opacity: 0.8;
}

/* Funnel Chart Styles */
.funnel-bar {
    margin: 10px auto;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.funnel-bar:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Progress Ring Styles */
.progress-ring-circle {
    transition: stroke-dashoffset 0.35s;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
}

/* Gauge Chart Styles */
.gauge-needle {
    transition: transform 1s ease-out;
    transform-origin: 50% 50%;
}

/* Waterfall Chart Styles */
.waterfall-bar-positive {
    background-color: var(--green);
}

.waterfall-bar-negative {
    background-color: var(--primary);
}

.waterfall-bar-total {
    background-color: var(--header-bg);
}

/* Bullet Chart Styles */
.bullet-background {
    fill: #e0e0e0;
}

.bullet-measure {
    fill: var(--deep-blue);
}

.bullet-marker {
    fill: var(--primary);
}

/* Scatter Plot with Size */
.bubble-chart-tooltip {
    position: absolute;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    pointer-events: none;
    z-index: 100;
}

/* Strategic Matrix Quadrants */
.matrix-quadrant {
    position: absolute;
    border: 1px dashed #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    color: var(--secondary-accent);
}

/* Responsive Adjustments for Special Charts */
@media (max-width: 1200px) {
    .multi-chart-grid {
        grid-template-columns: 1fr;
    }

    .multi-chart-grid.three-col {
        grid-template-columns: 1fr;
    }

    .chart-container.radar-chart,
    .chart-container.bubble-chart,
    .chart-container.polar-chart {
        min-height: 350px;
        max-height: 400px;
    }

    .matrix-chart-container {
        min-height: 400px;
        max-height: 450px;
    }
}

/* Animation for Chart Entry */
@keyframes chartFadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chart-container {
    animation: chartFadeIn 0.5s ease-out;
}

/* Chart Legend Customization */
.chart-legend {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
    margin-top: 15px;
}

.chart-legend-item {
    display: flex;
    align-items: center;
    font-size: 12px;
    color: var(--secondary-accent);
}

.chart-legend-color {
    width: 12px;
    height: 12px;
    border-radius: 2px;
    margin-right: 5px;
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

@media (max-width: 768px) {
    .pyramid-level {
        font-size: 14px;
        padding: 12px 20px;
    }

    .emphasis-box {
        flex-direction: column;
        text-align: center;
    }

    .step-content {
        font-size: 14px;
    }

    .framework-item {
        padding: 20px;
    }
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
        """Add data visualization slides with smart chart type selection, including conceptual visualizations."""
        if not data_points and not sections:
            return slide_num

        chart_num = 0
        for i, section in enumerate(sections):
            # Skip "关键洞察" section - will be handled separately
            if section.get('title') == '关键洞察':
                continue

            section_data = [
                dp for dp in data_points
                if dp.get('category') == section.get('title', '')
            ]

            # Check if section has numerical data or is conceptual
            has_data = len(section_data) > 0
            conceptual_type = self._detect_conceptual_type(section, section_data)

            # Skip if no data and not conceptual
            if not has_data and not conceptual_type:
                continue

            insights = self._extract_insights(section)

            if has_data:
                # Generate chart for numerical data
                chart_num += 1
                chart_id = f"chart{chart_num}"
                chart_type = self._determine_chart_type(section_data)
                chart_container_class = self._get_chart_container_class(chart_type)
                chart_type_name = self._get_chart_type_display_name(chart_type)

                insights_html = '\n                    '.join([
                    f'<li>{insight.strip()}</li>' for insight in insights if insight.strip()
                ])

                slide = f'''        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{section.get('title', 'Data Analysis')}</h1>
            </div>
            <div class="slide-content two-column">
                <div class="column {chart_container_class}">
                    <span class="chart-type-badge">{chart_type_name}</span>
                    <canvas id="{chart_id}" style="height: 400px !important; max-height: 400px;"></canvas>
                    <p class="chart-caption">{section.get('title', 'Chart')} - Smart Chart Selection</p>
                </div>
                <div class="column">
                    <h3 class="section-header">Key Insights</h3>
                    <ul class="bullet-points">
                        <li>{insights_html}</li>
                    </ul>
                </div>
            </div>
        </div>'''

            elif conceptual_type:
                # Generate conceptual visualization
                conceptual_viz = self._render_conceptual_visualization(section, conceptual_type)
                conceptual_name = self._get_conceptual_viz_name(conceptual_type)

                slide = f'''        <div class="slide" data-slide="{slide_num}">
            <div class="header-bar">
                <h1 class="slide-title">{section.get('title', 'Conceptual Visualization')}</h1>
            </div>
            <div class="slide-content">
                <span class="chart-type-badge">{conceptual_name}</span>
                {conceptual_viz}
            </div>
        </div>'''
            else:
                continue

            slides.append(slide)
            slide_num += 1

        return slide_num

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
        for i, section in enumerate(sections):
            section_data = [
                dp for dp in data_points
                if dp.get('category') == section.get('title', '')
            ]

            # Skip sections without data or "关键洞察" section
            if not section_data or section.get('title') == '关键洞察':
                continue

            chart_num += 1
            chart_id = f"chart{chart_num}"
            chart_scripts.append(self._generate_chart_script(chart_id, section_data))

        return '\n\n'.join(chart_scripts)

    def _generate_chart_script(self, chart_id: str, data_points: List[Dict]) -> str:
        """Generate Chart.js configuration for a single chart with smart type detection."""
        # Extract better labels from the data
        labels = self._extract_chart_labels(data_points[:10])
        values = [dp.get('value', 0) for dp in data_points[:10]]

        # Determine chart type
        chart_type = self._determine_chart_type(data_points)

        # Build chart-specific configuration
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
        """Build chart data configuration based on chart type."""

        # Generate color palette
        base_colors = [
            self.colors['deep_blue'],
            self.colors['green'],
            self.colors['blue'],
            self.colors['yellow'],
            self.colors['primary']
        ]

        # Extend colors for more data points
        background_colors = base_colors * ((len(values) // len(base_colors)) + 1)
        background_colors = background_colors[:len(values)]

        # Add transparency for some chart types
        alpha_colors = [self._add_alpha(color, 0.7) for color in background_colors]

        base_dataset = {
            'label': 'Value',
            'data': values,
            'backgroundColor': background_colors if chart_type in ['pie', 'doughnut', 'polarArea'] else alpha_colors,
            'borderColor': background_colors,
            'borderWidth': 2 if chart_type == 'line' else 0,
            'borderRadius': 4,
            'fill': chart_type == 'line'
        }

        # Chart type specific configurations
        if chart_type == 'line':
            base_dataset['tension'] = 0.3
            base_dataset['pointRadius'] = 5
            base_dataset['pointHoverRadius'] = 7
        elif chart_type == 'radar':
            base_dataset['backgroundColor'] = self._add_alpha(self.colors['deep_blue'], 0.2)
            base_dataset['borderColor'] = self.colors['deep_blue']
            base_dataset['pointBackgroundColor'] = self.colors['deep_blue']
        elif chart_type == 'bubble':
            # Generate random sizes for bubble effect
            import random
            base_dataset['data'] = [
                {'x': i, 'y': v, 'r': random.randint(5, 20)}
                for i, v in enumerate(values)
            ]
        elif chart_type == 'scatter':
            base_dataset['data'] = [
                {'x': i, 'y': v}
                for i, v in enumerate(values)
            ]

        return {
            'labels': labels,
            'datasets': [base_dataset]
        }

    def _build_chart_options(self, chart_type: str, data_points: List[Dict]) -> Dict:
        """Build chart options based on chart type."""

        base_options = {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'display': chart_type in ['pie', 'doughnut', 'polarArea', 'radar'],
                    'position': 'bottom'
                },
                'tooltip': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.8)',
                    'padding': 12,
                    'titleFont': {'size': 14, 'weight': 'bold'},
                    'bodyFont': {'size': 13}
                }
            }
        }

        # Add scales for Cartesian charts
        if chart_type in ['bar', 'line']:
            base_options['scales'] = {
                'y': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'},
                    'ticks': {'font': {'size': 12}}
                },
                'x': {
                    'grid': {'display': False},
                    'ticks': {'font': {'size': 11}}
                }
            }
        elif chart_type == 'radar':
            base_options['scales'] = {
                'r': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'},
                    'angleLines': {'color': '#e0e0e0'},
                    'pointLabels': {'font': {'size': 12}}
                }
            }
        elif chart_type in ['bubble', 'scatter']:
            base_options['scales'] = {
                'x': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'},
                    'ticks': {'font': {'size': 12}}
                },
                'y': {
                    'beginAtZero': True,
                    'grid': {'color': '#e0e0e0'},
                    'ticks': {'font': {'size': 12}}
                }
            }

        return base_options

    def _add_alpha(self, hex_color: str, alpha: float) -> str:
        """Add alpha channel to hex color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r}, {g}, {b}, {alpha})'

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

    def _determine_chart_type_v4(self, data_points: List[Dict], section: Optional[Dict] = None) -> str:
        """
        ENHANCED chart type selection with multi-dimensional analysis.

        Combines three analysis layers from real-world implementations:
        - Layer 1: Semantic analysis (field names, keywords) - Superset pattern
        - Layer 2: Structure inference (data format, properties) - variant-agents pattern  
        - Layer 3: Rule-based decision tree - OpenObserve pattern

        Determines most appropriate chart type by analyzing:
        - Data structure and values
        - Labels and units
        - Keywords in labels
        - Data patterns (time series, rankings, distributions, etc.)

        Returns:
            Chart type string compatible with Chart.js or custom visualization name
        """
        if not data_points:
            return 'bar'

        # Extract content features for analysis
        labels = [dp.get('label', '').lower() for dp in data_points]
        units = [dp.get('unit', '') for dp in data_points]
        values = [dp.get('value', 0) for dp in data_points]
        all_text = ' '.join(labels)

        # ===== Enhanced Multi-Dimensional Analysis =====
        if section is None:
            section = {'title': '', 'content': ''}
        
        # Layer 1: Semantic field analysis
        x_analysis = self._analyze_fields_semantic(data_points)
        
        # Layer 2: Structure inference
        structure_analysis = self._analyze_data_structure(data_points)
        
        # Layer 3: Rule-based decision tree
        return self._apply_decision_tree(x_analysis, structure_analysis, section, data_points)


    def _determine_chart_type(self, data_points: List[Dict]) -> str:
        """
        LEGACY chart type selection - Kept for backward compatibility.

        Smart chart type selection based on content analysis.

        Determines most appropriate chart type by analyzing:
        - Data structure and values
        - Labels and units
        - Keywords in labels
        - Data patterns (time series, rankings, distributions, etc.)

        Returns:
            Chart type string compatible with Chart.js
        """
        if not data_points:
            return 'bar'

        # Extract content features for analysis
        labels = [dp.get('label', '').lower() for dp in data_points]
        units = [dp.get('unit', '') for dp in data_points]
        values = [dp.get('value', 0) for dp in data_points]
        all_text = ' '.join(labels)

        # ===== 看"排名" (Rankings) =====
        ranking_keywords = ['排名', 'rank', 'level', 'tier', 'priority', '等级', '优先级', 'top', 'best', 'market share']
        if any(kw in all_text for kw in ranking_keywords):
            if len(data_points) <= 8:
                return 'polarArea'  # 玫瑰图
            return 'bar'  # 金字塔图用柱状模拟

        # ===== 看"流向" (Flow) =====
        flow_keywords = ['转化', '漏斗', 'flow', 'journey', 'process', 'stage', '阶段', '流程', 'step', '用户路径', '流失', 'customer']
        if any(kw in all_text for kw in flow_keywords):
            if 'funnel' in all_text or '漏斗' in all_text:
                return 'bar'  # 漏斗图用特殊柱状模拟
            return 'line'  # 瀑布图/流向用折线表示

        # ===== 看"分布" (Distribution) =====
        distribution_keywords = ['分布', 'distribution', 'spread', 'range', 'variance', 'outlier', 'deviation', 'scatter']
        if any(kw in all_text for kw in distribution_keywords):
            if len(data_points) >= 5:
                return 'bubble'  # 气泡图
            return 'polarArea'  # 玫瑰图

        # ===== 看"时间周期" (Time/Cyclical) =====
        time_keywords = ['q1', 'q2', 'q3', 'q4', '季度', '月', '年', 'week', 'month', 'year', '周期', 'season', '季节', '循环']
        time_pattern_keywords = ['阶梯', 'step', 'discrete', '周期性']
        if any(kw in all_text for kw in time_keywords + time_pattern_keywords):
            if any(kw in all_text for kw in ['周期', 'season', '循环', 'polar', 'arc']):
                return 'polarArea'  # 极坐标弧长图
            return 'line'  # 阶梯图/时间趋势

        # ===== 看"KPI达标" (KPI/Target) =====
        kpi_keywords = ['kpi', 'target', 'goal', '目标', '达标', 'achieve', 'variance', 'budget', 'actual', 'forecast', '预测']
        if any(kw in all_text for kw in kpi_keywords):
            return 'bar'  # 子弹图/差异图用特殊柱状

        # ===== 看"多维度比较" (Multi-dimensional) =====
        multi_dim_keywords = ['雷达', 'radar', 'spider', '多维', 'dimension', 'skill', '能力', 'feature', 'competitor', '对比', 'matrix']
        if any(kw in all_text for kw in multi_dim_keywords):
            return 'radar'  # 雷达图

        # ===== 看"占比关系" (Proportions) =====
        proportion_keywords = ['占比', 'share', 'composition', 'breakdown', '构成', '分配', 'split', 'mix', 'portion']
        has_proportion_keywords = any(kw in all_text for kw in proportion_keywords)
        percent_count = sum(1 for u in units if u == '%')

        # 饼图/环形图/华夫图条件
        if (len(data_points) <= 7 and percent_count >= len(data_points) * 0.6) or has_proportion_keywords:
            if len(data_points) <= 5:
                return 'doughnut'  # 环形图
            return 'pie'  # 饼图

        # ===== 看"趋势变化" (Trends) =====
        trend_keywords = ['趋势', 'growth', '增长', 'trend', 'change', 'increase', 'decrease', '变化', '上升', '下降', '历史']
        if any(kw in all_text for kw in trend_keywords):
            return 'line'  # 折线图/面积图

        # ===== 看"横向对比" (Comparison) =====
        comparison_keywords = ['对比', 'compare', 'vs', 'versus', 'difference', '差异', 'regional', 'region', '区域', 'survey']
        long_labels = any(len(label) > 15 for label in labels)
        if any(kw in all_text for kw in comparison_keywords) or long_labels:
            return 'bar'  # 条形图（横向）

        # ===== 看"战略分析" (Strategic Analysis) =====
        strategy_keywords = ['bcg', 'matrix', 'portfolio', 'portfolio', 'strategy', '战略', 'positioning', '定位', '投资', 'growth', 'share']
        if any(kw in all_text for kw in strategy_keywords):
            return 'scatter'  # 矩阵图用散点模拟

        # ===== 看"流程关系" (Process Flow) =====
        process_keywords = ['泳道', 'swimlane', 'value', 'stream', 'value stream', '流程', 'process', 'responsibility', '责任']
        if any(kw in all_text for kw in process_keywords):
            return 'bar'  # 流程图用柱状模拟

        # ===== 看"概率/风险" (Probability/Risk) =====
        risk_keywords = ['概率', 'probability', 'risk', '风险', 'uncertainty', 'monte carlo', 'simulation', 'simulation', 'forecast', '估计']
        if any(kw in all_text for kw in risk_keywords):
            return 'line'  # 蒙特卡洛云用散点/折线模拟

        # ===== Default heuristics =====

        # Small number of data points with percentages → pie/doughnut
        if len(data_points) <= 5 and percent_count == len(data_points):
            return 'doughnut'

        # Time series detected → line chart
        if self._detect_time_series(data_points):
            return 'line'

        # Otherwise default to bar chart
        return 'bar'

    def _detect_time_series(self, data_points: List[Dict]) -> bool:
        """Detect if data represents a time series."""
        time_patterns = [
            r'\d{4}',  # Years like 2020, 2021
            r'q[1-4]',  # Quarters Q1-Q4
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
            r'(一月|二月|三月|四月|五月|六月|七月|八月|九月|十月|十一月|十二月)',
        ]

        labels = [dp.get('label', '').lower() for dp in data_points]

        for label in labels:
            for pattern in time_patterns:
                if re.search(pattern, label):
                    return True

        return False

    def _analyze_fields_semantic(self, data_points: List[Dict]) -> Dict[str, Any]:
        """
        Analyze field characteristics for semantic analysis (Superset pattern).
        
        Returns:
            Dictionary with semantic field type indicators
        """
        labels = [dp.get('label', '').lower() for dp in data_points]
        units = [dp.get('unit', '').lower() for dp in data_points]
        all_text = ' '.join(labels + units)
        
        return {
            'is_temporal': any(kw in all_text for kw in [
                'date', 'time', 'year', 'month', 'day', 'hour',
                'created', 'updated', 'q1', 'q2', 'q3', 'q4',
                '年', '月', '日', '时', '季度', 'week', '星期',
                '周期', 'season', '时期', '时间'
            ]),
            'is_categorical': any(kw in all_text for kw in [
                'category', 'type', 'status', 'department',
                'region', 'country', 'state', 'category',
                '类别', '类型', '状态', '部门', '地区', '城市', '国家'
            ]),
            'is_geographic': any(kw in all_text for kw in [
                'map', 'location', 'country', 'city', 'region',
                '地图', '位置', '城市', '国家', '省', '州'
            ]),
            'is_hierarchical': any(kw in all_text for kw in [
                'hierarchy', 'level', 'tier', 'tree', 'parent',
                '层级', '级别', '树', '父级', '子级', '金字塔'
            ]),
            'is_financial': any(kw in all_text for kw in [
                'revenue', 'profit', 'cost', 'margin', 'budget',
                '收入', '利润', '成本', '毛利', '预算', '财务'
            ]),
            'is_performance': any(kw in all_text for kw in [
                'kpi', 'metric', 'score', 'rating', 'efficiency',
                '指标', '评分', '评级', '效率', '绩效'
            ])
        }

    def _analyze_data_structure(self, data_points: List[Dict]) -> Dict[str, Any]:
        """
        Infer chart type from data structure (variant-agents pattern).
        
        Returns:
            Dictionary with structural analysis indicators
        """
        if not data_points:
            return {'has_xy': False, 'has_xyz': False, 'has_ranges': False, 'has_matrix': False, 'has_flow': False}
        
        # Check first data point structure
        first = data_points[0]
        keys_str = str(first.keys()).lower()
        
        # Check for 2D data (x, y) - scatter plot
        has_xy = 'x' in keys_str or 'y' in keys_str
        
        # Check for 3D data (x, y, z/size) - bubble chart
        has_xyz = ('x' in keys_str or 'y' in keys_str) and ('z' in keys_str or 'size' in keys_str or 'r' in keys_str)
        
        # Check for range data - box plot, histogram
        has_ranges = any(kw in keys_str for kw in ['min', 'max', 'range', 'quartile', 'median', 'std', 'deviation'])
        
        # Check for matrix structure - heatmap
        has_matrix = 'row' in keys_str or 'column' in keys_str or len(data_points) > 20
        
        # Check for flow data - sankey
        has_flow = any(kw in keys_str for kw in ['source', 'target', 'from', 'to', 'flow', '源', '目标', '流向'])
        
        return {
            'has_xy': has_xy,
            'has_xyz': has_xyz,
            'has_ranges': has_ranges,
            'has_matrix': has_matrix,
            'has_flow': has_flow,
            'has_progress': any(kw in keys_str for kw in ['progress', 'duration', 'start', 'end']),
            'has_coordinates': any(kw in keys_str for kw in ['lat', 'lng', 'latitude', 'longitude', '坐标'])
        }

    def _apply_decision_tree(self, x_analysis: Dict, structure: Dict, section: Dict, data_points: List[Dict]) -> str:
        """
        Apply decision tree for chart type selection (OpenObserve pattern).
        
        Combines semantic analysis, structure inference, and rule-based logic.
        
        Returns:
            Chart type string compatible with Chart.js or custom visualization name
        """
        # Extract analysis values
        x_temporal = x_analysis.get('is_temporal', False)
        x_categorical = x_analysis.get('is_categorical', False)
        x_hierarchical = x_analysis.get('is_hierarchical', False)
        x_geographic = x_analysis.get('is_geographic', False)
        
        has_xy = structure.get('has_xy', False)
        has_xyz = structure.get('has_xyz', False)
        has_ranges = structure.get('has_ranges', False)
        has_matrix = structure.get('has_matrix', False)
        has_flow = structure.get('has_flow', False)
        has_progress = structure.get('has_progress', False)
        
        section_title = section.get('title', '').lower()
        all_text = ' '.join([section_title, section.get('content', '')]).lower()
        
        # ===== Priority 1: Special Data Structures =====
        if has_matrix:
            return 'heatmap'
        
        if has_flow:
            return 'sankey'
        
        if has_xyz:
            return 'bubble'
        
        if has_xy and not x_temporal:
            # Check if it's a correlation or distribution
            if any(kw in all_text for kw in ['correl', 'correlation', '相关', '关系']):
                return 'scatter'
            return 'scatter'
        
        if has_ranges:
            return 'boxplot'
        
        if has_progress:
            # Check for waterfall keywords
            if any(kw in all_text for kw in ['waterfall', '瀑布', 'cumul', '累积', 'seq', '顺序']):
                return 'waterfall'
            return 'gantt'
        
        # ===== Priority 2: Strategic Analysis Charts =====
        strategy_keywords = ['bcg', 'matrix', 'portfolio', 'strategy', '战略', 'positioning', '定位', 'quadrant', '象限', 'growth', 'share']
        if any(kw in all_text for kw in strategy_keywords):
            # Check if we have the right data structure for BCG matrix
            if len(data_points) >= 2:
                # Check for share + growth data
                has_share = any('share' in str(dp).lower() or '市场份额' in str(dp).lower() for dp in data_points)
                has_growth = any('growth' in str(dp).lower() or '增长' in str(dp).lower() for dp in data_points)
                if has_share and has_growth:
                    return 'bcg_matrix'
            return 'scatter'
        
        # ===== Priority 3: Hierarchical Data =====
        if x_hierarchical:
            # Check number of levels
            if len(data_points) <= 5:
                return 'pyramid'
            return 'treemap'
        
        # ===== Priority 4: Temporal Data =====
        if x_temporal:
            # Check for step/discrete keywords
            if any(kw in all_text for kw in ['step', 'discrete', 'stage', '阶段', '离散', '阶梯']):
                return 'step'
            # Check for cyclical keywords
            if any(kw in all_text for kw in ['cycle', 'seasonal', 'periodic', '循环', '周期', '季节']):
                return 'polarArea'
            return 'line'
        
        # ===== Priority 5: Categorical Data =====
        if x_categorical:
            num_points = len(data_points)
            units = [dp.get('unit', '') for dp in data_points]
            percent_count = sum(1 for u in units if '%' in u)
            
            # Small number with percentages → pie/doughnut
            if num_points <= 5 and percent_count >= num_points * 0.6:
                return 'doughnut'
            elif num_points <= 8 and percent_count >= num_points * 0.5:
                return 'pie'
            # Many categories → bar or horizontal bar
            elif num_points > 10:
                return 'bar'
            else:
                # Check if long labels → horizontal bar
                if any(len(dp.get('label', '')) > 15 for dp in data_points):
                    return 'bar'
                return 'bar'
        
        # ===== Priority 6: Multi-dimensional Comparison =====
        multi_dim_keywords = ['radar', 'spider', '多维', 'dimension', 'skill', 'ability', '能力', 'feature', 'competitor', '对比']
        if any(kw in all_text for kw in multi_dim_keywords):
            if len(data_points) >= 3 and len(data_points) <= 8:
                return 'radar'
        
        # ===== Priority 7: Geographic Data =====
        if x_geographic:
            return 'map'
        
        # ===== Default fallback =====
        # Check original keywords as fallback
        labels = [dp.get('label', '').lower() for dp in data_points]
        all_label_text = ' '.join(labels)
        
        # Check for existing keyword patterns
        ranking_keywords = ['排名', 'rank', 'level', 'tier', 'priority', '等级', '优先级', 'top', 'best']
        if any(kw in all_label_text for kw in ranking_keywords):
            if len(data_points) <= 8:
                return 'polarArea'
            return 'bar'
        
        proportion_keywords = ['占比', 'share', 'composition', 'breakdown', '构成', '分配']
        if any(kw in all_label_text for kw in proportion_keywords):
            units = [dp.get('unit', '') for dp in data_points]
            percent_count = sum(1 for u in units if '%' in u)
            if len(data_points) <= 5:
                return 'doughnut'
            elif percent_count >= len(data_points) * 0.5:
                return 'pie'
        
        trend_keywords = ['趋势', 'growth', '增长', 'trend', 'change', 'increase', 'decrease']
        if any(kw in all_label_text for kw in trend_keywords):
            return 'line'
        
        # Final default
        return 'bar'

    def _detect_conceptual_type(self, section: Dict, data_points: List[Dict]) -> Optional[str]:
        """
        Detect if section content is conceptual (non-numerical) and determine visualization type.

        Returns:
            'pyramid', 'progression', 'emphasis', 'cycle', 'comparison', 'framework', or None
        """
        title = section.get('title', '').lower()
        content = section.get('content', '').lower()

        # Combine all text from conclusions if no data points
        if not data_points:
            all_text = f"{title} {content}"
        else:
            all_text = title

        # ===== 看"层级" (Hierarchy) =====
        hierarchy_keywords = ['层级', 'hierarchy', 'level', 'tier', '金字塔', 'pyramid', 'structure', '架构', '组织', 'organization']
        if any(kw in all_text for kw in hierarchy_keywords):
            return 'pyramid'

        # ===== 看"递进" (Progression) =====
        progression_keywords = ['递进', 'progression', '步骤', 'step', 'phase', '阶段', '流程', 'process', 'journey', '路径', 'roadmap', 'timeline']
        if any(kw in all_text for kw in progression_keywords):
            return 'progression'

        # ===== 看"强调" (Emphasis) =====
        emphasis_keywords = ['强调', 'emphasis', '关键', 'key', '重点', 'important', '核心', 'core', 'highlight', '亮点', 'takeaway']
        if any(kw in all_text for kw in emphasis_keywords):
            return 'emphasis'

        # ===== 看"循环" (Cycle) =====
        cycle_keywords = ['循环', 'cycle', '闭环', 'loop', '迭代', 'iteration', '持续', 'continuous', '反馈', 'feedback']
        if any(kw in all_text for kw in cycle_keywords):
            return 'cycle'

        # ===== 看"对比" (Comparison) =====
        comparison_keywords = ['对比', 'comparison', '比较', 'versus', 'vs', 'before', 'after', '前后', '优劣', 'pros', 'cons']
        if any(kw in all_text for kw in comparison_keywords):
            return 'comparison'

        # ===== 看"框架" (Framework) =====
        framework_keywords = ['框架', 'framework', '模型', 'model', '法则', 'principle', '5w1h', 'star', '黄金圈', 'golden circle']
        if any(kw in all_text for kw in framework_keywords):
            return 'framework'

        return None

    def _render_conceptual_visualization(self, section: Dict, viz_type: str) -> str:
        """
        Render conceptual visualization HTML based on type.

        Returns:
            HTML string for the conceptual visualization
        """
        title = section.get('title', '')
        content = section.get('content', '')

        # Extract bullet points or key messages
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        key_points = []
        for line in lines:
            if line.startswith(('-', '*', '•')):
                key_points.append(line.lstrip('-*•').strip())
            elif len(line) > 10 and len(line) < 100:
                key_points.append(line)

        key_points = key_points[:5]  # Limit to 5 points

        if viz_type == 'pyramid':
            return self._render_pyramid(key_points, title)
        elif viz_type == 'progression':
            return self._render_progression(key_points, title)
        elif viz_type == 'emphasis':
            return self._render_emphasis(key_points, title)
        elif viz_type == 'cycle':
            return self._render_cycle(key_points, title)
        elif viz_type == 'comparison':
            return self._render_comparison(key_points, title)
        elif viz_type == 'framework':
            return self._render_framework(key_points, title)
        else:
            return self._render_emphasis(key_points, title)

    def _render_pyramid(self, points: List[str], title: str) -> str:
        """Render pyramid visualization."""
        levels = len(points)
        if levels == 0:
            return '<p class="body-text">No content available for pyramid visualization</p>'

        width_percentages = [100 - (i * 15) for i in range(levels)]
        colors = [
            'background-color: var(--primary-accent);',
            'background-color: var(--deep-blue);',
            'background-color: var(--green);',
            'background-color: var(--blue);',
            'background-color: var(--yellow);'
        ]

        pyramid_html = '<div class="pyramid-container">\n'
        for i, (point, width, color) in enumerate(zip(points, width_percentages, colors)):
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
        """Render framework visualization (e.g., 5W1H, STAR)."""
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

    def _render_bcg_matrix(self, data_points: List[Dict]) -> str:
        """Render BCG Matrix: Market Share vs Growth Rate (4 quadrants)."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">BCG Matrix requires at least 2 data points with market share and growth rate</p>'
        
        # Calculate quadrant averages
        share_values = [dp.get('market_share', dp.get('value', 0)) for dp in data_points]
        growth_values = [dp.get('growth_rate', dp.get('value', 0)) for dp in data_points]
        
        avg_share = sum(share_values) / len(share_values)
        avg_growth = sum(growth_values) / len(growth_values)
        
        # Generate data points for scatter plot
        scatter_data = [
            {
                'x': dp.get('market_share', dp.get('value', 0)),
                'y': dp.get('growth_rate', dp.get('value', 0)),
                'label': dp.get('label', dp.get('label', ''))
            }
            for dp in data_points
        ]
        
        chart_id = f"bcg_matrix_{id(data_points)}"
        data_json = json.dumps(scatter_data).replace('"', '&quot;')
        
        return f'''
        <div class="chart-container matrix-chart-container">
            <span class="chart-type-badge">BCG Matrix (波士顿矩阵)</span>
            <canvas id="{chart_id}" style="height: 450px !important;"></canvas>
            <div class="matrix-quadrants">
                <div class="matrix-quadrant" style="top: 0; left: 0;">
                    <strong>High Growth<br>High Share</strong>
                </div>
                <div class="matrix-quadrant" style="top: 0; right: 0;">
                    <strong>High Growth<br>Low Share</strong>
                </div>
                <div class="matrix-quadrant" style="bottom: 0; left: 0;">
                    <strong>Low Growth<br>High Share</strong>
                </div>
                <div class="matrix-quadrant" style="bottom: 0; right: 0;">
                    <strong>Low Growth<br>Low Share</strong>
                </div>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'scatter',
            data: {{
                labels: {[dp['label'] for dp in data_points]},
                datasets: [{{
                    data: [
                        {{
                            'x': dp.get('market_share', dp.get('value', 0)),
                            'y': dp.get('growth_rate', dp.get('value', 0)),
                            'label': dp.get('label', dp.get('label', ''))
                        }}
                        for dp in data_points
                    ],
                    backgroundColor: 'var(--deep-blue)',
                    borderColor: 'var(--deep-blue)',
                    pointRadius: 10,
                    pointHoverRadius: 14,
                    pointBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        title: {{display: true, text: 'Market Share (%)', font: {{size: 14, weight: '600'}}}},
                        min: 0,
                        max: Math.max(...{share_values}) * 1.1,
                        grid: {{color: '#e0e0e0'}},
                        afterDraw: (ctx) => {{
                            const ctxChart = ctx.chart;
                            ctxChart.ctx.save();
                            ctxChart.ctx.beginPath();
                            ctxChart.ctx.strokeStyle = 'var(--secondary-accent)';
                            ctxChart.ctx.lineWidth = 2;
                            ctxChart.ctx.setLineDash([8, 8]);
                            ctxChart.ctx.moveTo({avg_share}, 0);
                            ctxChart.ctx.lineTo({avg_share}, ctxChart.scales.y.max);
                            ctxChart.ctx.stroke();
                            ctxChart.ctx.restore();
                        }}
                    }},
                    y: {{
                        title: {{display: true, text: 'Growth Rate (%)', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}},
                        afterDraw: (ctx) => {{
                            const ctxChart = ctx.chart;
                            ctxChart.ctx.save();
                            ctxChart.ctx.beginPath();
                            ctxChart.ctx.strokeStyle = 'var(--secondary-accent)';
                            ctxChart.ctx.lineWidth = 2;
                            ctxChart.ctx.setLineDash([8, 8]);
                            ctxChart.ctx.moveTo(0, {avg_growth});
                            ctxChart.ctx.lineTo(ctxChart.scales.x.max, {avg_growth});
                            ctxChart.ctx.stroke();
                            ctxChart.ctx.restore();
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const dataPoint = ctx.raw;
                                return `${{dataPoint.label}}: Share=${{dataPoint.x.toFixed(1)}}%, Growth=${{dataPoint.y.toFixed(1)}}%`;
                            }},
                            title: (ctx) => ctx[0].label
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    def _render_gantt_chart(self, data_points: List[Dict]) -> str:
        """Render Gantt Chart: Project timeline with horizontal bars."""
        if not data_points:
            return '<p class="body-text">No data available for Gantt chart</p>'
        
        # Extract task information
        tasks = []
        for dp in data_points:
            task = {{
                'label': dp.get('label', dp.get('task', 'Task')),
                'start': dp.get('start', '2024-01'),
                'end': dp.get('end', '2024-12'),
                'duration': dp.get('duration', dp.get('progress', 0)),
                'progress': dp.get('progress', dp.get('progress', 0)),
                'category': dp.get('category', '')
            }}
            tasks.append(task)
        
        chart_id = f"gantt_{id(data_points)}"
        
        # Generate chart HTML with horizontal bars
        return f'''
        <div class="chart-container gantt-chart-container">
            <span class="chart-type-badge">Gantt Chart (甘特图)</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {[task['label'] for task in tasks]},
                datasets: [{{
                    data: {[task['progress'] for task in tasks]},
                    backgroundColor: [self._get_color_by_progress(task['progress']) for task in tasks],
                    borderColor: 'var(--text-primary)',
                    borderWidth: 1,
                    barPercentage: 0.6
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        grid: {{display: false}}
                    }},
                    x: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{display: true, text: 'Progress (%)', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const task = tasks[ctx.dataIndex];
                                return `${{task['label']}}: Progress=${{task['progress']}}%`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    def _render_waterfall_chart(self, data_points: List[Dict]) -> str:
        """Render Waterfall Chart: Sequential additions/subtractions."""
        if not data_points:
            return '<p class="body-text">No data available for waterfall chart</p>'
        
        # Calculate cumulative values
        cumulative = 0
        waterfall_data = []
        colors = []
        
        for dp in data_points:
            value = dp.get('value', 0)
            
            if 'start' in str(dp.get('label', '')).lower() or dp.get('is_start', False):
                # Start value - cumulative is set directly
                cumulative = value
                colors.append('var(--header-bg)')
            else:
                # Calculate change
                change = value
                cumulative += change
                colors.append('var(--green)' if value >= 0 else 'var(--primary-accent)')
            
            waterfall_data.append({
                'label': dp.get('label', ''),
                'value': value,
                'cumulative': cumulative
            })
        
        chart_id = f"waterfall_{id(data_points)}"
        
        return f'''
        <div class="chart-container waterfall-chart-container">
            <span class="chart-type-badge">Waterfall Chart (瀑布图)</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {[dp['label'] for dp in waterfall_data]},
                datasets: [{{
                    data: {[dp['cumulative'] for dp in waterfall_data]},
                    backgroundColor: colors,
                    borderColor: 'var(--text-primary)',
                    borderWidth: 2,
                    barPercentage: 0.7
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: false,
                        grid: {{color: '#e0e0e0'}}
                    }},
                    x: {{
                        grid: {{display: false}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const dp = waterfall_data[ctx.dataIndex];
                                const sign = dp.value >= 0 ? '+' : '';
                                return `${{dp['label']}}: ${{sign}}${{dp['value']}} (Cumulative: ${{dp['cumulative']}})`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    def _render_sankey_diagram(self, data_points: List[Dict]) -> str:
        """Render Sankey Diagram: Flow between stages (simulated with Chart.js)."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Sankey diagram requires at least 2 data points with source/target information</p>'
        
        # Group data by source
        sources = {}
        for dp in data_points:
            source = dp.get('source', dp.get('label', ''))
            if source not in sources:
                sources[source] = 0
            sources[source] += dp.get('value', 0)
        
        # Create stacked bar to simulate flow
        chart_id = f"sankey_{id(data_points)}"
        
        source_labels = list(sources.keys())
        flow_values = list(sources.values())
        
        return f'''
        <div class="chart-container sankey-container">
            <span class="chart-type-badge">Sankey Diagram (桑基图) - Flow Visualization</span>
            <canvas id="{chart_id}" style="height: 450px !important;"></canvas>
            <div class="flow-legend">
                <p style="font-size: 14px; color: var(--secondary-accent);">
                    <strong>Flow Pattern:</strong> Shows data movement between stages
                </p>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(source_labels)},
                datasets: [{{
                    data: {json.dumps(flow_values)},
                    backgroundColor: [
                        'var(--deep-blue)',
                        'var(--green)',
                        'var(--primary-accent)',
                        'var(--blue)',
                        'var(--yellow)'
                    ],
                    borderColor: 'var(--text-primary)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        grid: {{display: false}}
                    }},
                    x: {{
                        beginAtZero: true,
                        title: {{display: true, text: 'Flow Volume', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const source = source_labels[ctx.dataIndex];
                                const value = flow_values[ctx.dataIndex];
                                return `${{source}} → Flow: ${{value}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    def _render_heatmap(self, data_points: List[Dict]) -> str:
        """Render Heatmap: 2D data intensity using custom HTML/CSS."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Heatmap requires matrix data structure</p>'
        
        chart_id = f"heatmap_{id(data_points)}"
        
        # Convert data points to matrix format
        matrix = []
        max_value = 0
        
        for dp in data_points:
            if 'row' in dp and 'values' in dp:
                matrix.append(dp)
                max_value = max(max_value, max(dp['values']))
            elif 'value' in dp:
                matrix.append({'row': dp.get('label', ''), 'values': [dp.get('value', 0)]})
                max_value = max(max_value, dp.get('value', 0))
        
        # Generate heatmap cells
        cells_html = ''
        for row in matrix:
            row_name = row.get('row', '')
            values = row.get('values', [])
            
            cells_html = '<div style="display: flex;">\n'
            for val in values:
                intensity = val / max_value if max_value > 0 else 0
                color = f'rgba(85, 103, 230, {intensity:.2f})'
                cells_html += f'                <div style="width: 60px; height: 60px; background-color: {color}; margin: 2px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; font-size: 14px;">{val}</div>\n'
            cells_html += '            </div>\n'
            cells_html += f'            <div style="display: flex; align-items: center; font-weight: 600; color: var(--text-secondary); margin: 5px 0px;">{row_name}</div>\n'
            cells_html += '        </div>\n'
        
        return f'''
        <div class="chart-container heatmap-container">
            <span class="chart-type-badge">Heatmap (热点矩阵/热力图)</span>
            <div style="display: flex; flex-direction: column; gap: 10px; align-items: center; padding: 20px;">
                {cells_html}
            </div>
            <div style="text-align: center; margin-top: 20px; font-size: 14px; color: var(--secondary-accent);">
                <strong>Scale:</strong> Light (Low) → Dark (High)
            </div>
        </div>
        '''

    def _get_color_by_progress(self, progress: int) -> str:
        """Get color based on progress percentage."""
        if progress >= 80:
            return 'var(--green)'
        elif progress >= 50:
            return 'var(--blue)'
        elif progress >= 25:
            return 'var(--primary-accent)'
        else:
            return 'var(--yellow)'

    def _render_funnel_chart(self, data_points: List[Dict]) -> str:
        """Render Funnel Chart: Process stages/conversion with decreasing width bars."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Funnel chart requires at least 2 data points</p>'
        
        # Extract funnel data
        funnel_data = []
        for dp in data_points:
            funnel_data.append({
                'label': dp.get('label', dp.get('stage', 'Stage')),
                'value': dp.get('value', dp.get('count', 0)),
                'conversion': dp.get('conversion', dp.get('rate', ''))
            })
        
        # Sort by value (largest at top)
        funnel_data.sort(key=lambda x: x['value'], reverse=True)
        
        chart_id = f"funnel_{id(data_points)}"
        
        return f'''
        <div class="chart-container funnel-chart-container">
            <span class="chart-type-badge">Funnel Chart (漏斗图)</span>
            <canvas id="{chart_id}" style="height: 450px !important;"></canvas>
            <div class="funnel-legend">
                <p style="font-size: 14px; color: var(--secondary-accent);">
                    <strong>Conversion Pattern:</strong> Shows flow through sequential stages
                </p>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {[dp['label'] for dp in funnel_data]},
                datasets: [{{
                    data: {[dp['value'] for dp in funnel_data]},
                    backgroundColor: [
                        'var(--deep-blue)',
                        'var(--primary-accent)',
                        'var(--green)',
                        'var(--blue)',
                        'var(--yellow)'
                    ],
                    borderColor: 'var(--text-primary)',
                    borderWidth: 1,
                    barPercentage: [0.8, 0.7, 0.6, 0.5, 0.4].slice(0, {len(funnel_data)}),
                    categoryPercentage: 0.9
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        grid: {{display: false}},
                        ticks: {{font: {{size: 14, weight: '600'}}}}
                    }},
                    x: {{
                        beginAtZero: true,
                        title: {{display: true, text: 'Count / Volume', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const dp = funnel_data[ctx.dataIndex];
                                return `${{dp['label']}}: ${{dp['value']}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''
    
    def _render_bullet_chart(self, data_points: List[Dict]) -> str:
        """Render Bullet Chart: Target vs actual with KPI comparison."""
        if not data_points:
            return '<p class="body-text">No data available for bullet chart</p>'
        
        bullet_data = []
        for dp in data_points:
            bullet_data.append({
                'label': dp.get('label', 'Metric'),
                'target': dp.get('target', dp.get('goal', 100)),
                'actual': dp.get('actual', dp.get('value', 0)),
                'range_max': dp.get('range_max', dp.get('max', 120)),
                'range_min': dp.get('range_min', dp.get('min', 80))
            })
        
        chart_id = f"bullet_{id(data_points)}"
        
        actual_colors = [
            'var(--green)' if dp['actual'] >= dp['target'] else 'var(--primary-accent)'
            for dp in bullet_data
        ]
        
        return f'''
        <div class="chart-container bullet-chart-container">
            <span class="chart-type-badge">Bullet Chart (子弹图)</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
            <div class="bullet-legend">
                <p style="font-size: 14px; color: var(--secondary-accent);">
                    <strong>Legend:</strong> Bar=Actual, Line=Target, Background=Target Range
                </p>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {[dp['label'] for dp in bullet_data]},
                datasets: [
                    {{
                        type: 'line',
                        label: 'Target',
                        data: {[dp['target'] for dp in bullet_data]},
                        borderColor: 'var(--deep-blue)',
                        backgroundColor: 'transparent',
                        borderWidth: 3,
                        pointRadius: 0,
                        order: 0,
                        tension: 0
                    }},
                    {{
                        type: 'bar',
                        label: 'Actual',
                        data: {[dp['actual'] for dp in bullet_data]},
                        backgroundColor: {json.dumps(actual_colors)},
                        borderColor: 'var(--text-primary)',
                        borderWidth: 1,
                        barPercentage: 0.4,
                        order: 1
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        grid: {{display: false}},
                        ticks: {{font: {{size: 14, weight: '600'}}}}
                    }},
                    y: {{
                        beginAtZero: true,
                        title: {{display: true, text: 'Value', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const dp = bullet_data[ctx.dataIndex];
                                const status = dp['actual'] >= dp['target'] ? '✓ Met' : '✗ Below';
                                return `Target: ${{dp['target']}}, Actual: ${{dp['actual']}} ${{status}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''
    
    def _render_step_chart(self, data_points: List[Dict]) -> str:
        """Render Step Chart: Discrete time changes with step transitions."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Step chart requires at least 2 data points</p>'
        
        # Extract step data
        step_data = []
        for dp in data_points:
            step_data.append({
                'label': dp.get('label', ''),
                'value': dp.get('value', 0),
                'category': dp.get('category', '')
            })
        
        chart_id = f"step_{id(data_points)}"
        
        return f'''
        <div class="chart-container step-chart-container">
            <span class="chart-type-badge">Step Chart (阶梯图)</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
            <div class="step-legend">
                <p style="font-size: 14px; color: var(--secondary-accent);">
                    <strong>Pattern:</strong> Shows discrete value changes at specific points
                </p>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'line',
            data: {{
                labels: {[dp['label'] for dp in step_data]},
                datasets: [{{
                    data: {[dp['value'] for dp in step_data]},
                    borderColor: 'var(--deep-blue)',
                    backgroundColor: 'rgba(85, 103, 230, 0.1)',
                    borderWidth: 3,
                    fill: false,
                    stepped: true,
                    pointRadius: 6,
                    pointHoverRadius: 9,
                    pointBackgroundColor: 'var(--deep-blue)',
                    pointBorderColor: 'var(--text-primary)',
                    pointBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{
                        grid: {{display: false}},
                        ticks: {{font: {{size: 12, weight: '600'}}}}
                    }},
                    y: {{
                        beginAtZero: false,
                        title: {{display: true, text: 'Value', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }}
                }},
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                const dp = step_data[ctx.dataIndex];
                                return `${{dp['label']}}: ${{dp['value']}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    # ===== Backward Compatibility Methods =====

    def generate_from_parsed_doc(
        self,
        parsed_doc,
        output_path: str = 'presentation.html'
    ) -> str:
        """Generate presentation from ParsedDocument object (new direct pipeline).

        This method provides backward compatibility by accepting a ParsedDocument
        object and converting it to the dict format expected by the original
        generate() method.

        Args:
            parsed_doc: ParsedDocument object from DocumentParser
            output_path: Where to save the HTML file

        Returns:
            Absolute path to the generated HTML file
        """
        parsed_doc_dict = self._parsed_document_to_dict(parsed_doc)
        return self.generate(parsed_doc_dict, output_path)

    def generate_from_specs(
        self,
        slide_plan,
        output_path: str = 'presentation.html'
    ) -> str:
        """Generate presentation from SlidePlan object (new direct pipeline).

        This method provides integration with the new direct conversion pipeline
        by accepting a SlidePlan object and generating HTML from it.

        Args:
            slide_plan: SlidePlan object from SlidePlanner
            output_path: Where to save the HTML file

        Returns:
            Absolute path to the generated HTML file
        """
        # Import here to avoid circular dependencies
        from direct_generator import DirectGenerator

        generator = DirectGenerator()
        return generator.generate(slide_plan, output_path)

    def _parsed_document_to_dict(self, doc) -> dict:
        """Convert ParsedDocument to dict for backward compatibility.

        This helper method converts a ParsedDocument object (from parser.py)
        into the dictionary format expected by the original generate() method.
        """
        return {
            'title': doc.title,
            'doc_type': doc.doc_type.value if hasattr(doc.doc_type, 'value') else str(doc.doc_type),
            'sections': [
                {
                    'title': s.title,
                    'content': s.content,
                    'level': s.level,
                    'subsections': [
                        {
                            'title': sub.title,
                            'content': sub.content,
                            'level': sub.level
                        }
                        for sub in s.subsections
                    ]
                }
                for s in doc.sections
            ],
            'data_points': [
                {
                    'label': dp.label,
                    'value': dp.value,
                    'unit': dp.unit,
                    'category': dp.category
                }
                for dp in doc.data_points
            ],
            'conclusions': [
                {
                    'text': c.text,
                    'category': c.category,
                    'priority': c.priority
                }
                for c in doc.conclusions
            ],
            'raw_content': doc.raw_content
        }


def main():
    import sys

    generator = PresentationGenerator()

    if len(sys.argv) < 2:
        print("Usage: python generator_v3.py <parsed_json_file> [output_path]")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        parsed_doc = json.load(f)

    output = sys.argv[2] if len(sys.argv) > 2 else 'presentation.html'
    result = generator.generate(parsed_doc, output)
    print(f"Generated presentation: {result}")


if __name__ == "__main__":
    main()

    # ========== 新增图表渲染方法 ==========
    
    def _render_gauge_chart(self, data_points: List[Dict]) -> str:
        """Render Gauge Chart: KPI metrics with speedometer-style visualization."""
        if not data_points:
            return '<p class="body-text">No data available for gauge chart</p>'
        
        # Take first data point for gauge
        dp = data_points[0]
        value = dp.get('value', dp.get('actual', 0))
        target = dp.get('target', dp.get('goal', 100))
        label = dp.get('label', 'KPI')
        
        chart_id = f"gauge_{id(data_points)}"
        max_value = dp.get('max', target * 1.2)
        
        return f'''
        <div class="chart-container gauge-chart-container">
            <span class="chart-type-badge">Gauge/Speedometer (仪表盘)</span>
            <canvas id="{chart_id}" style="height: 350px !important;"></canvas>
            <div class="gauge-info" style="text-align: center; margin-top: 15px;">
                <h3 style="font-size: 24px; color: var(--deep-blue);">{value}</h3>
                <p style="font-size: 14px; color: var(--secondary-accent);">{label}</p>
                <p style="font-size: 12px; color: #74788d;">Target: {target}</p>
            </div>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'doughnut',
            data: {{
                labels: ['Actual', 'Remaining'],
                datasets: [{{
                    data: [{value}, {max_value - value}],
                    backgroundColor: [
                        '{self.colors["green"] if value >= target else self.colors["primary"]}',
                        '#e0e0e0'
                    ],
                    borderWidth: 0,
                    circumference: 180,
                    rotation: 270
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {{
                    legend: {{display: false}},
                    tooltip: {{enabled: false}}
                }}
            }}
        }});
        </script>
        '''
    
    def _render_venn_diagram(self, data_points: List[Dict]) -> str:
        """Render Venn Diagram: Set relationships and overlaps using CSS."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Venn diagram requires at least 2 sets</p>'
        
        # Extract set data
        sets = data_points[:3]  # Support up to 3 sets
        set_count = len(sets)
        
        colors = [self.colors['deep_blue'], self.colors['primary'], self.colors['green']]
        
        sets_html = ""
        for i, s in enumerate(sets):
            name = s.get('label', s.get('name', f'Set {i+1}'))
            value = s.get('value', s.get('count', ''))
            overlap = s.get('overlap', '')
            
            position = ""
            if set_count == 2:
                if i == 0:
                    position = "left: 25%; top: 50%; transform: translate(-50%, -50%);"
                else:
                    position = "left: 75%; top: 50%; transform: translate(-50%, -50%);"
            elif set_count == 3:
                if i == 0:
                    position = "left: 25%; top: 35%; transform: translate(-50%, -50%);"
                elif i == 1:
                    position = "left: 75%; top: 35%; transform: translate(-50%, -50%);"
                else:
                    position = "left: 50%; top: 70%; transform: translate(-50%, -50%);"
            
            sets_html += f'''
            <div class="venn-set" style="
                position: absolute;
                {position}
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: {colors[i]}33;
                border: 3px solid {colors[i]};
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-weight: bold;
                z-index: {3-i};
            ">
                <div style="font-size: 16px; color: {colors[i]};">{name}</div>
                <div style="font-size: 14px; color: #333;">{value}</div>
            </div>
            '''
        
        # Add overlap label for 2 sets
        if set_count == 2:
            overlap_value = sets[0].get('overlap', sets[1].get('overlap', ''))
            sets_html += f'''
            <div style="
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                font-size: 12px;
                font-weight: bold;
                color: #74788d;
                z-index: 4;
            ">{overlap_value}</div>
            '''
        
        return f'''
        <div class="chart-container venn-diagram-container" style="position: relative; height: 350px;">
            <span class="chart-type-badge">Venn Diagram (韦恩图)</span>
            {sets_html}
        </div>
        '''
    
    def _render_timeline(self, data_points: List[Dict]) -> str:
        """Render Timeline: Sequential events or milestones."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Timeline requires at least 2 events</p>'
        
        events_html = ""
        for i, dp in enumerate(data_points):
            date = dp.get('date', dp.get('time', dp.get('label', f'Event {i+1}')))
            title = dp.get('title', dp.get('name', ''))
            description = dp.get('description', dp.get('detail', ''))
            position = 'left' if i % 2 == 0 else 'right'
            
            events_html += f'''
            <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content timeline-{position}">
                    <div class="timeline-date" style="color: {self.colors['primary']}; font-weight: bold;">{date}</div>
                    <div class="timeline-title" style="font-size: 16px; font-weight: 600; margin: 5px 0;">{title}</div>
                    <div class="timeline-desc" style="font-size: 14px; color: #74788d;">{description}</div>
                </div>
            </div>
            '''
        
        return f'''
        <div class="chart-container timeline-container" style="padding: 20px;">
            <span class="chart-type-badge">Timeline (时间轴)</span>
            <div class="timeline">
                {events_html}
            </div>
        </div>
        <style>
        .timeline {{
            position: relative;
            max-width: 800px;
            margin: 0 auto;
        }}
        .timeline::before {{
            content: '';
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 2px;
            background: {self.colors['secondary']};
            transform: translateX(-50%);
        }}
        .timeline-item {{
            position: relative;
            margin-bottom: 40px;
        }}
        .timeline-dot {{
            position: absolute;
            left: 50%;
            top: 0;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: {self.colors['primary']};
            transform: translateX(-50%);
            border: 3px solid white;
            box-shadow: 0 0 0 3px {self.colors['primary']}33;
        }}
        .timeline-content {{
            position: relative;
            width: 45%;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid {self.colors['primary']};
        }}
        .timeline-left {{
            left: 0;
        }}
        .timeline-right {{
            left: 55%;
        }}
        </style>
        '''
    
    def _render_flowchart(self, data_points: List[Dict]) -> str:
        """Render Flowchart: Process with decision points using CSS."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Flowchart requires at least 2 steps</p>'
        
        nodes_html = ""
        arrows_html = ""
        
        for i, dp in enumerate(data_points):
            label = dp.get('label', dp.get('name', dp.get('text', f'Step {i+1}')))
            node_type = dp.get('type', 'process')  # process, decision, start, end
            
            # Determine shape based on type
            if node_type == 'decision':
                shape_style = 'transform: rotate(45deg); width: 120px; height: 120px;'
                content_style = 'transform: rotate(-45deg);'
            elif node_type == 'start':
                shape_style = 'border-radius: 25px; background: {self.colors["green"]};'
                content_style = ''
            elif node_type == 'end':
                shape_style = 'border-radius: 25px; background: {self.colors["primary"]};'
                content_style = ''
            else:
                shape_style = 'border-radius: 4px;'
                content_style = ''
            
            # Position nodes vertically
            top_pos = i * 140 + 20
            
            nodes_html += f'''
            <div class="flow-node flow-node-{node_type}" style="
                position: absolute;
                left: 50%;
                top: {top_pos}px;
                transform: translateX(-50%);
                {shape_style}
                width: 160px;
                height: 80px;
                background: white;
                border: 2px solid {self.colors['deep_blue']};
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 10px;
                font-weight: 600;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            ">
                <div style="{content_style}">{label}</div>
            </div>
            '''
            
            # Add arrow to next node
            if i < len(data_points) - 1:
                arrows_html += f'''
                <div style="
                    position: absolute;
                    left: 50%;
                    top: {top_pos + 85}px;
                    transform: translateX(-50%);
                    width: 2px;
                    height: 50px;
                    background: {self.colors['secondary']};
                "></div>
                <div style="
                    position: absolute;
                    left: 50%;
                    top: {top_pos + 130}px;
                    transform: translateX(-50%) rotate(180deg);
                    width: 0;
                    height: 0;
                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                    border-top: 10px solid {self.colors['secondary']};
                "></div>
                '''
        
        total_height = len(data_points) * 140 + 100
        
        return f'''
        <div class="chart-container flowchart-container" style="position: relative; height: {total_height}px; padding: 20px;">
            <span class="chart-type-badge">Flowchart (流程图)</span>
            {nodes_html}
            {arrows_html}
        </div>
        '''

    def _render_mindmap(self, data_points: List[Dict]) -> str:
        """Render Mind Map: Central topic with radiating branches using CSS."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Mind map requires at least 1 central topic and 1 branch</p>'
        
        central_topic = data_points[0].get('label', data_points[0].get('topic', data_points[0].get('title', 'Central Topic')))
        branches = data_points[1:] if len(data_points) > 1 else []
        
        colors = [self.colors['deep_blue'], self.colors['green'], self.colors['blue'], 
                  self.colors['yellow'], self.colors['primary'], self.colors['secondary']]
        
        positions = [
            {'left': '15%', 'top': '15%'},
            {'right': '15%', 'top': '15%'},
            {'left': '10%', 'top': '50%', 'transform': 'translateY(-50%)'},
            {'right': '10%', 'top': '50%', 'transform': 'translateY(-50%)'},
            {'left': '20%', 'bottom': '15%'},
            {'right': '20%', 'bottom': '15%'}
        ]
        
        branches_html = ''
        for i, branch in enumerate(branches):
            if i >= len(positions):
                break
                
            pos = positions[i]
            color = colors[i % len(colors)]
            label = branch.get('label', branch.get('title', f'Branch {i+1}'))
            desc = branch.get('description', branch.get('desc', branch.get('detail', '')))
            
            pos_style = ''
            for key, value in pos.items():
                pos_style += f'{key}: {value}; '
            
            branches_html += f'''
            <div class="mindmap-branch" style="
                position: absolute;
                {pos_style}
                display: flex;
                align-items: center;
                gap: 15px;
                padding: 15px 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                transition: all 0.3s;
                cursor: pointer;
                border-left: 4px solid {color};
                max-width: 250px;
            ">
                <div class="branch-dot" style="
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    flex-shrink: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 14px;
                    font-weight: bold;
                    color: white;
                    background: {color};
                ">{i+1}</div>
                <div class="branch-text" style="flex: 1;">
                    <div class="branch-title" style="font-size: 16px; font-weight: 600; color: #333;">{label}</div>
                    {f'<div class="branch-desc" style="font-size: 13px; color: #74788d;">{desc}</div>' if desc else ''}
                </div>
            </div>
            '''
        
        return f'''
        <div class="chart-container mindmap-container" style="
            position: relative;
            width: 100%;
            height: 500px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            overflow: hidden;
            margin: 20px 0;
        ">
            <span class="chart-type-badge" style="position: absolute; top: 10px; left: 10px; z-index: 20;">Mind Map (思维导图)</span>
            <div class="mindmap-center" style="
                position: absolute;
                left: 50%;
                top: 50%;
                transform: translate(-50%, -50%);
                width: 200px;
                height: 80px;
                background: {self.colors['primary']};
                color: white;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                font-weight: bold;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                z-index: 10;
            ">{central_topic}</div>
            {branches_html}
        </div>
        <style>
        .mindmap-branch:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
            z-index: 5;
        }
        </style>
        '''

    def _render_pareto_chart(self, data_points: List[Dict]) -> str:
        """Render Pareto Chart: Bar + Line chart for 80/20 rule visualization."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Pareto chart requires at least 2 data points</p>'
        
        labels = [dp.get('label', f'Cat {i+1}') for i, dp in enumerate(data_points)]
        values = [dp.get('value', 0) for dp in data_points]
        
        # Calculate cumulative percentage
        total = sum(values)
        cumulative = []
        running_sum = 0
        for val in values:
            running_sum += val
            cumulative.append(round((running_sum / total) * 100, 1) if total > 0 else 0)
        
        chart_id = f"pareto_{id(data_points)}"
        
        return f'''
        <div class="chart-container pareto-chart-container">
            <span class="chart-type-badge">Pareto Chart (帕累托图) - 80/20 Rule</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
            <div class="pareto-legend">
                <p style="font-size: 14px; color: var(--secondary-accent);">
                    <strong>80/20 Principle:</strong> 80% of effects come from 20% of causes
                </p>
            </div>
        </div>
        <script>
        const {chart_id}_data = {{
            labels: {json.dumps(labels)},
            values: {json.dumps(values)},
            cumulative: {json.dumps(cumulative)}
        }};
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'bar',
            data: {{
                labels: {chart_id}_data.labels,
                datasets: [
                    {{
                        type: 'bar',
                        label: 'Count',
                        data: {chart_id}_data.values,
                        backgroundColor: 'var(--deep-blue)',
                        borderColor: 'var(--text-primary)',
                        borderWidth: 1,
                        yAxisID: 'y'
                    }},
                    {{
                        type: 'line',
                        label: 'Cumulative %',
                        data: {chart_id}_data.cumulative,
                        borderColor: 'var(--primary-accent)',
                        backgroundColor: 'rgba(248, 93, 66, 0.1)',
                        pointBackgroundColor: 'var(--primary-accent)',
                        pointBorderColor: '#fff',
                        pointRadius: 5,
                        tension: 0.3,
                        yAxisID: 'y1'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                scales: {{
                    y: {{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        beginAtZero: true,
                        title: {{display: true, text: 'Count', font: {{size: 14, weight: '600'}}}},
                        grid: {{color: '#e0e0e0'}}
                    }},
                    y1: {{
                        type: 'linear',
                        display: true,
                        position: 'right',
                        min: 0,
                        max: 100,
                        title: {{display: true, text: 'Cumulative %', font: {{size: 14, weight: '600'}}}},
                        grid: {{drawOnChartArea: false}}
                    }},
                    x: {{
                        grid: {{display: false}}
                    }}
                }},
                plugins: {{
                    legend: {{display: true, position: 'top'}},
                    tooltip: {{
                        callbacks: {{
                            label: (ctx) => {{
                                if (ctx.dataset.type === 'line') {{
                                    return `Cumulative: ${{ctx.parsed.y}}%`;
                                }}
                                return `${{ctx.dataset.label}}: ${{ctx.parsed.y}}`;
                            }}
                        }}
                    }}
                }}
            }}
        }});
        </script>
        '''

    def _render_polar_chart(self, data_points: List[Dict]) -> str:
        """Render Polar Area Chart (Rose Chart): Categorical comparison."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Polar chart requires at least 2 data points</p>'
        
        labels = [dp.get('label', f'Cat {i+1}') for i, dp in enumerate(data_points)]
        values = [dp.get('value', 0) for dp in data_points]
        colors = [
            self.colors['deep_blue'], self.colors['green'], self.colors['primary'],
            self.colors['blue'], self.colors['yellow'], self.colors['secondary']
        ]
        
        chart_id = f"polar_{id(data_points)}"
        
        return f'''
        <div class="chart-container polar-chart-container">
            <span class="chart-type-badge">Polar Area Chart (极坐标图/玫瑰图)</span>
            <canvas id="{chart_id}" style="height: 400px !important;"></canvas>
        </div>
        <script>
        new Chart(document.getElementById('{chart_id}'), {{
            type: 'polarArea',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    data: {json.dumps(values)},
                    backgroundColor: {json.dumps(colors)},
                    borderColor: 'var(--text-primary)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        grid: {{color: '#e0e0e0'}},
                        ticks: {{display: true}}
                    }}
                }},
                plugins: {{
                    legend: {{display: true, position: 'right'}}
                }}
            }}
        }});
        </script>
        '''

    def _render_problem_solution(self, data_points: List[Dict]) -> str:
        """Render Problem-Solution: Two-column comparison layout."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Problem-Solution requires at least 1 problem and 1 solution</p>'
        
        # Extract problems and solutions
        problems = []
        solutions = []
        for dp in data_points:
            if dp.get('type') == 'problem' or dp.get('category') == 'problem':
                problems.append(dp.get('label', dp.get('text', '')))
            elif dp.get('type') == 'solution' or dp.get('category') == 'solution':
                solutions.append(dp.get('label', dp.get('text', '')))
        
        # If no explicit type, split evenly
        if not problems and not solutions:
            mid = len(data_points) // 2
            problems = [dp.get('label', '') for dp in data_points[:mid]]
            solutions = [dp.get('label', '') for dp in data_points[mid:]]
        
        problems_html = '\n'.join(f'<div class="ps-item problem-item">🔴 {p}</div>' for p in problems if p)
        solutions_html = '\n'.join(f'<div class="ps-item solution-item">✅ {s}</div>' for s in solutions if s)
        
        return f'''
        <div class="chart-container problem-solution-container">
            <span class="chart-type-badge">Problem-Solution (问题/解决方案)</span>
            <div class="ps-layout" style="display: flex; gap: 30px; margin-top: 30px;">
                <div class="ps-column" style="flex: 1; background: #fff5f5; padding: 25px; border-radius: 10px; border-left: 4px solid #dc3545;">
                    <h3 style="color: #dc3545; margin-bottom: 20px; font-size: 22px;">❌ 问题</h3>
                    <div style="display: flex; flex-direction: column; gap: 15px;">{problems_html}</div>
                </div>
                <div class="ps-column" style="flex: 1; background: #f0fff4; padding: 25px; border-radius: 10px; border-left: 4px solid #28a745;">
                    <h3 style="color: #28a745; margin-bottom: 20px; font-size: 22px;">✅ 解决方案</h3>
                    <div style="display: flex; flex-direction: column; gap: 15px;">{solutions_html}</div>
                </div>
            </div>
        </div>
        <style>
        .ps-item {{ padding: 12px; background: rgba(255,255,255,0.7); border-radius: 6px; }}
        </style>
        '''

    def _render_pros_cons(self, data_points: List[Dict]) -> str:
        """Render Pros-Cons: Two-column advantages and disadvantages."""
        if not data_points or len(data_points) < 2:
            return '<p class="body-text">Pros-Cons requires at least 1 advantage and 1 disadvantage</p>'
        
        # Extract pros and cons
        pros = []
        cons = []
        for dp in data_points:
            if dp.get('type') == 'pro' or dp.get('category') == 'advantage':
                pros.append(dp.get('label', dp.get('text', '')))
            elif dp.get('type') == 'con' or dp.get('category') == 'disadvantage':
                cons.append(dp.get('label', dp.get('text', '')))
        
        # If no explicit type, split evenly
        if not pros and not cons:
            mid = len(data_points) // 2
            pros = [dp.get('label', '') for dp in data_points[:mid]]
            cons = [dp.get('label', '') for dp in data_points[mid:]]
        
        pros_html = '\n'.join(f'<div class="pc-item pro-item">✓ {p}</div>' for p in pros if p)
        cons_html = '\n'.join(f'<div class="pc-item con-item">✗ {c}</div>' for c in cons if c)
        
        return f'''
        <div class="chart-container pros-cons-container">
            <span class="chart-type-badge">Pros-Cons (优缺点分析)</span>
            <div class="pc-layout" style="display: flex; gap: 30px; margin-top: 30px;">
                <div class="pc-column" style="flex: 1; background: #f0fff4; padding: 25px; border-radius: 10px; border-left: 4px solid {self.colors['green']};">
                    <h3 style="color: {self.colors['green']}; margin-bottom: 20px; font-size: 22px;">✓ 优点</h3>
                    <div style="display: flex; flex-direction: column; gap: 15px;">{pros_html}</div>
                </div>
                <div class="pc-column" style="flex: 1; background: #fff5f5; padding: 25px; border-radius: 10px; border-left: 4px solid {self.colors['primary']};">
                    <h3 style="color: {self.colors['primary']}; margin-bottom: 20px; font-size: 22px;">✗ 缺点</h3>
                    <div style="display: flex; flex-direction: column; gap: 15px;">{cons_html}</div>
                </div>
            </div>
        </div>
        <style>
        .pc-item {{ padding: 12px; background: rgba(255,255,255,0.7); border-radius: 6px; }}
        </style>
        '''

    def _render_swot_analysis(self, data_points: List[Dict]) -> str:
        """Render SWOT Analysis: 2x2 matrix of Strengths, Weaknesses, Opportunities, Threats."""
        if not data_points or len(data_points) < 4:
            return '<p class="body-text">SWOT analysis requires at least 4 categories</p>'
        
        # Group by SWOT categories
        swot_data = {'S': [], 'W': [], 'O': [], 'T': []}
        
        for dp in data_points:
            category = dp.get('category', dp.get('type', '')).upper()
            label = dp.get('label', dp.get('text', ''))
            if category in swot_data and label:
                swot_data[category].append(label)
        
        # Generate SWOT quadrant HTML
        swot_quadrants = [
            {'key': 'S', 'title': '优势', 'color': self.colors['green'], 'items': swot_data['S']},
            {'key': 'W', 'title': '劣势', 'color': self.colors['primary'], 'items': swot_data['W']},
            {'key': 'O', 'title': '机会', 'color': self.colors['blue'], 'items': swot_data['O']},
            {'key': 'T', 'title': '威胁', 'color': self.colors['yellow'], 'items': swot_data['T']}
        ]
        
        quadrants_html = ''
        for i, quad in enumerate(swot_quadrants):
            position = 'left: 0; top: 0;' if i == 0 else 'right: 0; top: 0;' if i == 1 else 'left: 0; bottom: 0;' if i == 2 else 'right: 0; bottom: 0;'
            items_html = '\n'.join(f'<li>{item}</li>' for item in quad['items'])
            quadrants_html += f'''
            <div class="swot-quadrant" style="
                position: absolute;
                {position}
                width: calc(50% - 15px);
                height: calc(50% - 15px);
                background: rgba({hex_to_rgb(quad['color'])}, 0.1);
                border: 2px solid {quad['color']};
                border-radius: 10px;
                padding: 20px;
            ">
                <h3 style="color: {quad['color']}; font-size: 24px; margin-bottom: 15px; border-bottom: 2px solid {quad['color']}; padding-bottom: 10px;">
                    {quad['title']} ({quad['key']})
                </h3>
                <ul style="margin-left: 20px; line-height: 1.8;">{items_html}</ul>
            </div>
            '''
        
        return f'''
        <div class="chart-container swot-container" style="position: relative; height: 500px; margin: 20px 0;">
            <span class="chart-type-badge" style="position: absolute; top: 10px; left: 10px; z-index: 10;">SWOT Analysis (态势分析)</span>
            {quadrants_html}
        </div>
        '''

    def _render_kano_model(self, data_points: List[Dict]) -> str:
        """Render Kano Model: Customer satisfaction vs functionality matrix."""
        if not data_points or len(data_points) < 3:
            return '<p class="body-text">Kano model requires at least 3 features</p>'
        
        # Kano quadrants
        kano_regions = [
            {'name': '必备属性', 'desc': '没有不满意，有也很正常', 'color': self.colors['yellow'], 'pos': 'bottom-left'},
            {'name': '期望属性', 'desc': '越满意越好', 'color': self.colors['blue'], 'pos': 'top-left'},
            {'name': '魅力属性', 'desc': '没有没关系，有会很惊喜', 'color': self.colors['green'], 'pos': 'top-right'},
            {'name': '反向属性', 'desc': '越多越不满意', 'color': self.colors['primary'], 'pos': 'bottom-right'}
        ]
        
        # Place features
        features_html = ''
        for dp in data_points:
            label = dp.get('label', dp.get('feature', ''))
            quadrant = dp.get('quadrant', dp.get('category', 0))
            if label:
                colors_list = [self.colors['yellow'], self.colors['blue'], self.colors['green'], self.colors['primary']]
                color = colors_list[min(quadrant, 3)]
                features_html += f'<div class="kano-feature" style="background: {color}; padding: 8px 15px; border-radius: 20px; color: white; font-size: 13px; font-weight: 600; display: inline-block; margin: 5px;">{label}</div>'
        
        regions_html = '\n'.join(f'''
        <div class="kano-region" style="
            position: absolute;
            {reg['pos'] == 'bottom-left' and 'left: 0; bottom: 0;' or reg['pos'] == 'top-left' and 'left: 0; top: 0;' or reg['pos'] == 'top-right' and 'right: 0; top: 0;' or 'right: 0; bottom: 0;'}
            width: calc(50% - 10px);
            height: calc(50% - 10px);
            background: rgba({hex_to_rgb(reg['color'])}, 0.15);
            border: 2px solid {reg['color']};
            border-radius: 8px;
            padding: 15px;
        ">
            <h4 style="color: {reg['color']}; margin-bottom: 8px;">{reg['name']}</h4>
            <p style="font-size: 13px; color: #666;">{reg['desc']}</p>
        </div>
        ''' for reg in kano_regions)
        
        return f'''
        <div class="chart-container kano-container" style="position: relative; height: 450px; margin: 20px 0; background: #f8f9fa; border-radius: 10px; padding: 20px;">
            <span class="chart-type-badge" style="position: absolute; top: 10px; left: 10px; z-index: 10;">Kano Model (满意度模型)</span>
            <div style="position: absolute; top: 50%; left: 10px; transform: translateY(-50%) rotate(-90deg); color: {self.colors['secondary']}; font-weight: 600;">满意度 →</div>
            <div style="position: absolute; left: 50%; bottom: 10px; transform: translateX(-50%); color: {self.colors['secondary']}; font-weight: 600;">功能度 →</div>
            {regions_html}
        </div>
        '''

    def _render_ansoff_matrix(self, data_points: List[Dict]) -> str:
        """Render Ansoff Matrix: Growth strategies 2x2."""
        if not data_points or len(data_points) < 4:
            return '<p class="body-text">Ansoff matrix requires at least 4 strategies</p>'
        
        # Ansoff quadrants
        ansoff_quadrants = [
            {'key': 'market_penetration', 'title': '市场渗透', 'desc': '现有市场，现有产品', 'color': self.colors['green']},
            {'key': 'product_development', 'title': '产品开发', 'desc': '现有市场，新产品', 'color': self.colors['blue']},
            {'key': 'market_development', 'title': '市场开发', 'desc': '新市场，现有产品', 'color': self.colors['primary']},
            {'key': 'diversification', 'title': '多元化', 'desc': '新市场，新产品', 'color': self.colors['yellow']}
        ]
        
        quadrants_html = '\n'.join(f'''
        <div class="ansoff-quadrant" style="
            position: absolute;
            {q['key'] == 'market_development' and 'left: 0; top: 0;' or q['key'] == 'diversification' and 'right: 0; top: 0;' or q['key'] == 'market_penetration' and 'left: 0; bottom: 0;' or 'right: 0; bottom: 0;'}
            width: calc(50% - 10px);
            height: calc(50% - 10px);
            background: rgba({hex_to_rgb(q['color'])}, 0.15);
            border: 3px solid {q['color']};
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        ">
            <h3 style="color: {q['color']}; font-size: 22px; margin-bottom: 10px;">{q['title']}</h3>
            <p style="color: #666; font-size: 14px;">{q['desc']}</p>
        </div>
        ''' for q in ansoff_quadrants)
        
        return f'''
        <div class="chart-container ansoff-container" style="position: relative; height: 400px; margin: 20px 0; background: #f8f9fa; border-radius: 10px; padding: 20px;">
            <span class="chart-type-badge" style="position: absolute; top: 10px; left: 10px; z-index: 10;">Ansoff Matrix (安索夫增长矩阵)</span>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #999; font-weight: 600; font-size: 14px;">现有市场</div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #999; font-weight: 600; font-size: 14px;">新市场</div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #999; font-weight: 600; font-size: 14px;">现有产品</div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #999; font-weight: 600; font-size: 14px;">新产品</div>
            {quadrants_html}
        </div>
        '''
