#!/usr/bin/env python3
"""
Extraction Script with Debug Mode

Same as basic template but adds debug output to help troubleshoot:
- Show which selectors matched (and count)
- Print sample extracted values
- Identify missing/null fields

Usage:
    .venv/bin/python scripts/extract_with_debug.py --debug
"""

import asyncio
import yaml
import argparse
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


def extract_items(soup: BeautifulSoup, config: dict, debug: bool = False) -> list[dict]:
    """Extract items with optional debug output."""
    results = []

    for pattern in config.get('items', []):
        selector = pattern['selector']
        elements = soup.select(selector)

        if debug:
            print(f"\n=== Pattern: {pattern.get('name', 'item')} ===")
            print(f"Selector: {selector}")
            print(f"Matches: {len(elements)} elements")

        for idx, elem in enumerate(elements):
            item = {'_type': pattern.get('name', 'item')}

            # Extract fields
            for name, cfg in pattern.get('fields', {}).items():
                if isinstance(cfg, str):
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

            results.append(item)

            # Debug: Print first 3 sample items
            if debug and idx < 3:
                print(f"\nSample item {idx + 1}:")
                for key, value in item.items():
                    if value and len(str(value)) > 100:
                        print(f"  {key}: {str(value)[:97]}...")
                    else:
                        print(f"  {key}: {value}")

    return results


def validate_results(results: list[dict]) -> None:
    """Validate extraction results and print warnings."""
    if not results:
        print("\n⚠️  No items extracted!")
        return

    print(f"\n=== Validation Report ===")
    print(f"Total items: {len(results)}")

    # Count null/missing fields
    if results:
        all_fields = set()
        for item in results:
            all_fields.update(item.keys())

        for field in sorted(all_fields):
            null_count = sum(1 for item in results if item.get(field) is None or item.get(field) == '')
            null_pct = (null_count / len(results)) * 100

            if null_pct > 0:
                status = "⚠️" if null_pct > 50 else "ℹ️"
                print(f"{status} {field}: {null_count}/{len(results)} null ({null_pct:.1f}%)")


async def main():
    """Main extraction workflow with debug support."""
    parser = argparse.ArgumentParser(description='Extract data with optional debug mode')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--validate', action='store_true', help='Validate results and show warnings')
    args = parser.parse_args()

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
    results = extract_items(soup, config, debug=args.debug)

    # Validate
    if args.validate:
        validate_results(results)

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
            print(f"\nSaved to {json_path}")

        elif fmt == 'csv' and results:
            import csv
            csv_path = output_path.with_suffix('.csv')
            with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
            print(f"Saved to {csv_path}")

    print(f"Extracted {len(results)} items")


if __name__ == "__main__":
    asyncio.run(main())
