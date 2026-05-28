#!/usr/bin/env python3
"""
Pharma Daily - Output Generator Script
Generates HTML and Markdown from fetched news.

Usage:
    python generate_output.py [--date DATE] [--theme THEME] [--analysis TEXT]

Examples:
    python generate_output.py --date today --theme minimal
    python generate_output.py --date 2024-01-15 --theme pharma-blue
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.fetcher import NewsItem
from src.generator import PharmaGenerator, generate_daily_output
from src.config import OUTPUT_DIR, THEMES, DEFAULT_THEME


def parse_date(date_str: str) -> tuple[datetime, str]:
    """Parse date string into datetime and formatted string."""
    date_str_lower = date_str.lower().strip()

    if date_str_lower in ["today", "今天"]:
        dt = datetime.now()
    elif date_str_lower in ["yesterday", "昨天"]:
        dt = datetime.now() - timedelta(days=1)
    else:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            dt = datetime.now()

    return dt, dt.strftime("%Y-%m-%d")


def load_news_from_cache(date_str: str) -> list[NewsItem]:
    """Load news from cached JSON file."""
    output_dir = Path(OUTPUT_DIR) / date_str.replace("-", "")

    # Try different file names
    for filename in ["news.json", "raw_news.json"]:
        json_file = output_dir / filename
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both formats
            items_data = data.get("items", data) if isinstance(data, dict) else data

            items = []
            for d in items_data:
                items.append(NewsItem(
                    title=d["title"],
                    link=d["link"],
                    summary=d.get("summary", ""),
                    published=datetime.fromisoformat(d["published"]),
                    source=d["source"],
                    language=d["language"],
                    category=d.get("category", "综合"),
                    importance=d.get("importance", 0)
                ))
            return items

    return []


def main():
    parser = argparse.ArgumentParser(
        description="Generate HTML and Markdown output from news"
    )
    parser.add_argument(
        "--date", "-d",
        default="today",
        help="Date to generate: today, yesterday, or YYYY-MM-DD"
    )
    parser.add_argument(
        "--theme", "-t",
        choices=THEMES,
        default=DEFAULT_THEME,
        help="HTML theme: minimal, pharma-blue, warm"
    )
    parser.add_argument(
        "--analysis", "-a",
        help="Analysis text to include in output"
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch fresh news if no cache exists"
    )

    args = parser.parse_args()

    # Parse date
    dt, date_str = parse_date(args.date)

    # Load news from cache
    items = load_news_from_cache(date_str)

    # Fetch if needed and requested
    if not items and args.fetch:
        from src.fetcher import fetch_pharma_news
        items = fetch_pharma_news(date_str=args.date)

    if not items:
        print(f"Error: No news data found for {date_str}", file=sys.stderr)
        print(f"Run fetch_news.py --date {args.date} --save first", file=sys.stderr)
        sys.exit(1)

    # Generate output
    result = generate_daily_output(
        items=items,
        date_str=date_str,
        theme=args.theme,
        analysis=args.analysis
    )

    # Print results
    print(f"✅ Generated output for {date_str}")
    print(f"")
    print(f"📁 Directory: {result['directory']}")
    print(f"📄 Markdown:  {result['markdown']}")
    print(f"🌐 HTML:      {result['html']} (theme: {args.theme})")


if __name__ == "__main__":
    main()
