#!/usr/bin/env python3
"""
Pharma Daily - News Fetcher Script
Fetches pharmaceutical news from configured RSS sources.

Usage:
    python fetch_news.py [--date DATE] [--language LANG] [--output FORMAT]

Examples:
    python fetch_news.py --date today
    python fetch_news.py --date yesterday --language zh
    python fetch_news.py --date 2024-01-15 --output json
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

from src.fetcher import fetch_pharma_news, NewsItem
from src.config import OUTPUT_DIR, CATEGORIES


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


def format_news_text(items: list[NewsItem], date_str: str) -> str:
    """Format news items as readable text."""
    lines = [
        f"# 制药日报 Pharma Daily - {date_str}",
        f"",
        f"**获取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**新闻总数**: {len(items)}",
        "",
        "---",
        ""
    ]

    # Group by category
    categories = {}
    for item in items:
        cat = item.category or "综合"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    # Statistics
    lines.append("## 分类统计\n")
    for cat, cat_items in sorted(categories.items(), key=lambda x: -len(x[1])):
        en_name = CATEGORIES.get(cat, {}).get("en", "")
        lines.append(f"- **{cat}** ({en_name}): {len(cat_items)} 条")
    lines.append("")

    # News by category
    for cat, cat_items in categories.items():
        en_name = CATEGORIES.get(cat, {}).get("en", cat)
        lines.append(f"\n## {cat} | {en_name}\n")

        # Sort by importance
        cat_items.sort(key=lambda x: x.importance, reverse=True)

        for item in cat_items:
            flag = "🇨🇳" if item.language == "zh" else "🇺🇸"
            stars = "⭐" * item.importance if item.importance else ""

            lines.append(f"### {flag} {item.title}")
            lines.append(f"- **来源**: {item.source}")
            lines.append(f"- **时间**: {item.published.strftime('%Y-%m-%d %H:%M')}")
            if stars:
                lines.append(f"- **重要性**: {stars}")
            if item.summary:
                lines.append(f"\n> {item.summary}\n")
            lines.append(f"🔗 [阅读原文]({item.link})")
            lines.append("")

    return "\n".join(lines)


def format_news_json(items: list[NewsItem], date_str: str) -> str:
    """Format news items as JSON."""
    data = {
        "date": date_str,
        "generated_at": datetime.now().isoformat(),
        "total_count": len(items),
        "items": [
            {
                "title": item.title,
                "link": item.link,
                "summary": item.summary,
                "published": item.published.isoformat(),
                "source": item.source,
                "language": item.language,
                "category": item.category,
                "importance": item.importance
            }
            for item in items
        ]
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch pharmaceutical news from RSS sources"
    )
    parser.add_argument(
        "--date", "-d",
        default="today",
        help="Date to fetch: today, yesterday, or YYYY-MM-DD"
    )
    parser.add_argument(
        "--language", "-l",
        choices=["zh", "en", "all"],
        default="all",
        help="Filter by language"
    )
    parser.add_argument(
        "--category", "-c",
        help="Filter by category"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save output to docs directory"
    )

    args = parser.parse_args()

    # Parse date
    dt, date_str = parse_date(args.date)

    # Fetch news
    language = None if args.language == "all" else args.language
    items = fetch_pharma_news(
        date_str=args.date,
        language=language,
        category=args.category
    )

    if not items:
        print(f"No news found for {date_str}", file=sys.stderr)
        sys.exit(1)

    # Format output
    if args.output == "json":
        output = format_news_json(items, date_str)
    else:
        output = format_news_text(items, date_str)

    # Save if requested
    if args.save:
        output_dir = Path(OUTPUT_DIR) / date_str.replace("-", "")
        output_dir.mkdir(parents=True, exist_ok=True)

        if args.output == "json":
            output_file = output_dir / "news.json"
        else:
            output_file = output_dir / "news.md"

        output_file.write_text(output, encoding="utf-8")
        print(f"Saved to: {output_file}", file=sys.stderr)

    print(output)


if __name__ == "__main__":
    main()
