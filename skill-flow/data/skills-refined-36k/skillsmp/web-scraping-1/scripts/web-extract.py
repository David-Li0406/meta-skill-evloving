#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "beautifulsoup4", "lxml"]
# ///
"""
Generic web content extractor - extracts structured data from any URL.

Usage:
    uv run web-extract.py <url> [--selector SELECTOR] [--fields FIELDS]

Examples:
    # Extract title and meta description
    uv run web-extract.py "https://example.com"

    # Extract specific elements
    uv run web-extract.py "https://example.com" --selector ".article" --fields "text,href"

Output: JSON to stdout with extracted data.
"""
from __future__ import annotations

import argparse
import json
import sys

import requests
from bs4 import BeautifulSoup


def extract_metadata(soup: BeautifulSoup) -> dict:
    """Extract common metadata from page."""
    return {
        "title": (
            soup.find("title").get_text(strip=True) if soup.find("title") else None
        ),
        "description": (
            soup.find("meta", {"name": "description"})["content"]
            if soup.find("meta", {"name": "description"})
            else None
        ),
        "h1": soup.find("h1").get_text(strip=True) if soup.find("h1") else None,
    }


def extract_selector(
    soup: BeautifulSoup, selector: str, fields: list[str]
) -> list[dict]:
    """Extract elements matching selector with specified fields."""
    results = []
    elements = soup.select(selector)

    for elem in elements[:50]:  # Limit results
        item = {}
        for field in fields:
            if field == "text":
                item[field] = elem.get_text(strip=True)[:500]
            elif field == "html":
                item[field] = str(elem)[:1000]
            elif field == "href":
                link = elem.find("a")
                item[field] = link["href"] if link and link.get("href") else None
            else:
                # Try to find element with class matching field name
                child = elem.select_one(f".{field}")
                item[field] = child.get_text(strip=True) if child else None
        results.append(item)

    return results


def fetch_and_extract(
    url: str, selector: str | None = None, fields: list[str] | None = None
) -> dict:
    """Fetch URL and extract data."""
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; Vibe4Vets research)"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    result = {
        "url": url,
        "status": response.status_code,
        "metadata": extract_metadata(soup),
    }

    if selector:
        result["elements"] = extract_selector(soup, selector, fields or ["text"])
        result["element_count"] = len(result["elements"])

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from web pages"
    )
    parser.add_argument("url", help="URL to fetch and extract from")
    parser.add_argument("--selector", "-s", help="CSS selector for elements to extract")
    parser.add_argument(
        "--fields",
        "-f",
        help="Comma-separated fields to extract (text,html,href,class-name)",
    )

    args = parser.parse_args()

    fields = args.fields.split(",") if args.fields else None

    try:
        result = fetch_and_extract(args.url, args.selector, fields)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except requests.exceptions.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.response.status_code}", "url": args.url}))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "type": type(e).__name__}))
        sys.exit(1)


if __name__ == "__main__":
    main()
