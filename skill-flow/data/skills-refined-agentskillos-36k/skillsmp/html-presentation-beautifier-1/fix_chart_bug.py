#!/usr/bin/env python3
"""
Chart Bug Fixer - 修复图表导致的浏览器卡死问题

问题诊断:
1. 图表容器没有最大高度限制
2. Chart.js maintainAspectRatio: false 可能导致无限增长
3. Canvas 元素高度未明确设置
"""

import json
import re
from pathlib import Path


def fix_chart_bug(html_path: str) -> str:
    """修复 HTML 文件中的图表 bug"""

    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 修复 1: 限制图表容器的最大高度
    old_chart_container = r'.chart-container {\s+min-height: 400px;\s+}'
    new_chart_container = '''.chart-container {
        min-height: 400px;
        max-height: 450px;
        position: relative;
    }'''

    html = re.sub(old_chart_container, new_chart_container, html)

    # 修复 2: 为 canvas 元素添加高度限制
    old_canvas_style = r'<canvas id="chart1"></canvas>'
    new_canvas_style = '''<canvas id="chart1" style="height: 400px !important; max-height: 400px;"></canvas>'''
    html = html.replace(old_canvas_style, new_canvas_style)

    old_canvas_style2 = r'<canvas id="chart2"></canvas>'
    new_canvas_style2 = '''<canvas id="chart2" style="height: 400px !important; max-height: 400px;"></canvas>'''
    html = html.replace(old_canvas_style2, new_canvas_style2)

    # 修复 3: 添加 body 的 overflow 防止无限滚动
    # 找到 body 的 CSS 定义
    old_body = r'''body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--primary-bg);
    color: var(--text-secondary);
    line-height: 1.6;
    overflow: hidden;
}'''

    new_body = '''body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: var(--primary-bg);
    color: var(--text-secondary);
    line-height: 1.6;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
}'''

    html = html.replace(old_body, new_body)

    # 修复 4: 确保 presentation-container 不会无限增长
    old_container = r'''.presentation-container {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
}'''

    new_container = '''.presentation-container {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: hidden;
    max-height: calc(100vh - 60px);
}'''

    html = html.replace(old_container, new_container)

    # 修复 5: 限制 slide 的最大高度
    old_slide = r'''.slide {
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
}'''

    new_slide = '''.slide {
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
}'''

    html = html.replace(old_slide, new_slide)

    return html


def main():
    if __name__ == "__main__":
        import sys

        if len(sys.argv) < 2:
            print("Usage: python fix_chart_bug.py <input_html> [output_html]")
            sys.exit(1)

        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.html', '_fixed.html')

        # 修复 bug
        fixed_html = fix_chart_bug(input_file)

        # 保存修复后的文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_html)

        print(f"✅ 图表 bug 已修复！")
        print(f"输入文件: {input_file}")
        print(f"输出文件: {output_file}")
        print(f"\n修复内容:")
        print(f"  ✅ 限制图表容器最大高度 (450px)")
        print(f"  ✅ 设置 canvas 元素高度 (400px)")
        print(f"  ✅ 修复 body 的 overflow")
        print(f"  ✅ 限制 presentation-container 高度")
        print(f"  ✅ 限制 slide 最大高度")


if __name__ == "__main__":
    main()
