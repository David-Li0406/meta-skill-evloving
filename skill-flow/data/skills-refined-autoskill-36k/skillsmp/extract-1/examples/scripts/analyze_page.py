#!/usr/bin/env python3
"""
HTML Page Structure Analyzer

Analyzes a webpage's HTML structure to identify:
- Element counts
- Common CSS classes
- Potential container patterns

Usage:
    Replace 'URL_HERE' with the target URL and run:
    .venv/bin/python analyze_page.py
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from collections import Counter

# Configuration
TARGET_URL = 'URL_HERE'  # Replace with your target URL

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(TARGET_URL, wait_until='networkidle')
    page.wait_for_timeout(2000)

    html = page.content()
    soup = BeautifulSoup(html, 'lxml')

    # Element counts
    elements = Counter(tag.name for tag in soup.find_all(True))
    print('=== Elements ===')
    for e, c in elements.most_common(15):
        print(f'  {e}: {c}')

    # Class frequency
    classes = Counter()
    for tag in soup.find_all(True):
        for cls in tag.get('class', []):
            classes[cls] += 1
    print('\n=== Classes ===')
    for cls, c in classes.most_common(20):
        print(f'  .{cls}: {c}')

    browser.close()
