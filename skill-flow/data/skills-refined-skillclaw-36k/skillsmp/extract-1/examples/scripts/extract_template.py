#!/usr/bin/env python3
"""
Basic Extraction Script Template

A starting template for writing custom extraction scripts that:
- Load YAML configuration
- Fetch HTML with Playwright (handles JS rendering)
- Extract data using BeautifulSoup + CSS selectors
- Save results to JSON/CSV

Usage:
    1. Copy this template to your project's scripts/ directory
    2. Customize the extract_items() function for your needs
    3. Run: .venv/bin/python scripts/extract.py
"""

import asyncio
import yaml
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json


async def fetch_html(url: str, wait_for: str = None) -> str:
    """Fetch HTML with Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        if wait_for:
            await page.wait_for_selector(wait_for)
        await page.wait_for_timeout(2000)
        html = await page.content()
        await browser.close()
        return html


def extract_items(soup: BeautifulSoup, config: dict) -> list[dict]:
    """Extract items using YAML config.

    This is a simplified implementation. For production use, handle:
    - Full field config format (selector, extract, transform)
    - Context inheritance
    - Transforms (regex, replace, absolute_url)
    - Schema validation
    """
    results = []
    for pattern in config.get('items', []):
        selector = pattern['selector']
        elements = soup.select(selector)

        for elem in elements:
            item = {'_type': pattern.get('name', 'item')}

            # Extract fields
            for name, cfg in pattern.get('fields', {}).items():
                if isinstance(cfg, str):
                    # Short form: "selector::attribute"
                    sel, attr = cfg.rsplit('::', 1) if '::' in cfg else (cfg, 'text')
                    target = elem.select_one(sel.strip()) if sel.strip() else elem

                    if target:
                        if attr == 'text':
                            item[name] = target.get_text(strip=True)
                        else:
                            item[name] = target.get(attr)
                    else:
                        item[name] = None

                elif isinstance(cfg, dict):
                    # Full form with selector, extract, transform
                    sel = cfg.get('selector', '')
                    target = elem.select_one(sel) if sel else elem
                    attr = cfg.get('extract', 'text')

                    if target:
                        if attr == 'text':
                            item[name] = target.get_text(strip=True)
                        else:
                            item[name] = target.get(attr)
                    else:
                        item[name] = None

                    # TODO: Apply transforms if specified

            results.append(item)

    return results


async def main():
    """Main extraction workflow."""
    # Load config
    config_path = 'configs/extraction.yaml'
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Fetch HTML
    url = config['source']['url']
    wait_for = config['source'].get('options', {}).get('wait_for')
    print(f"Fetching {url}...")
    html = await fetch_html(url, wait_for)

    # Extract
    soup = BeautifulSoup(html, 'lxml')
    results = extract_items(soup, config)

    # Save
    output_path = Path(config['output']['path'])
    output_formats = config['output'].get('format', ['json'])
    if isinstance(output_formats, str):
        output_formats = [output_formats]

    for fmt in output_formats:
        if fmt == 'json':
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Saved to {json_path}")

        elif fmt == 'csv' and results:
            import csv
            csv_path = output_path.with_suffix('.csv')
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            print(f"Saved to {csv_path}")

    print(f"\nExtracted {len(results)} items")


if __name__ == "__main__":
    asyncio.run(main())
