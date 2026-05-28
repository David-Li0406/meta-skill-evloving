#!/usr/bin/env python3
"""
Pharma Daily - List RSS Sources
Shows all configured pharmaceutical news sources.

Usage:
    python list_sources.py [--language LANG] [--format FORMAT]
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import CHINESE_SOURCES, INTERNATIONAL_SOURCES, ALL_SOURCES


def main():
    parser = argparse.ArgumentParser(
        description="List configured RSS sources"
    )
    parser.add_argument(
        "--language", "-l",
        choices=["zh", "en", "all"],
        default="all",
        help="Filter by language"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    args = parser.parse_args()

    # Select sources
    if args.language == "zh":
        sources = CHINESE_SOURCES
    elif args.language == "en":
        sources = INTERNATIONAL_SOURCES
    else:
        sources = ALL_SOURCES

    if args.format == "json":
        data = [
            {
                "name": s.name,
                "url": s.url,
                "language": s.language,
                "category": s.category,
                "enabled": s.enabled
            }
            for s in sources
        ]
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print("📡 Pharma Daily - RSS Sources")
        print("=" * 50)

        if args.language in ["zh", "all"]:
            print("\n🇨🇳 中文源 Chinese Sources:")
            for s in CHINESE_SOURCES:
                status = "✅" if s.enabled else "❌"
                print(f"  {status} {s.name}")
                print(f"     类别: {s.category}")
                print(f"     URL: {s.url}")

        if args.language in ["en", "all"]:
            print("\n🇺🇸 英文源 International Sources:")
            for s in INTERNATIONAL_SOURCES:
                status = "✅" if s.enabled else "❌"
                print(f"  {status} {s.name}")
                print(f"     Category: {s.category}")
                print(f"     URL: {s.url}")

        print(f"\nTotal: {len(sources)} sources")


if __name__ == "__main__":
    main()
