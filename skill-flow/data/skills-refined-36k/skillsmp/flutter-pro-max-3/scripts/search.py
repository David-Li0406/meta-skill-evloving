#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Search - CLI for Flutter knowledge base search
Usage: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--top 5]

Domains: widget, package, pattern, architect, chart, color, typography, style, ux, icon, landing, naming, product, prompt, performance, ui-reasoning, accessibility
Stacks: riverpod, bloc, provider
"""

import argparse
import json
from core import (
    CSV_CONFIG, 
    AVAILABLE_DOMAINS, 
    AVAILABLE_STACKS, 
    MAX_RESULTS, 
    search, 
    search_with_stack
)
from typing import Any


def format_output(result: dict[str, Any]) -> str:
    """Format results for human-readable output (token-optimized for AI)"""
    if "error" in result:
        return f"❌ Error: {result['error']}"

    output = []
    
    # Header
    output.append(f"\n🔍 Flutter Pro Max Search Results")
    if result.get("stack"):
        output.append(f"   Stack: {result['stack']} (excluding: {', '.join(result.get('excluded', []))})")
    output.append(f"   Domain: {result['domain']} | Query: '{result['query']}'")
    output.append(f"   Source: {result['file']} | Found: {result['count']} results\n")

    # Results
    for i, row in enumerate(result['results'], 1):
        output.append(f"{'='*60}")
        output.append(f"[{i}] Score: {row.get('_score', 'N/A')}")
        
        for key, value in row.items():
            if key == "_score":
                continue
            value_str = str(value)
            if len(value_str) > 200:
                value_str = value_str[:200] + "..."
            output.append(f"    {key}: {value_str}")
        output.append("")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Flutter Pro Max Search - BM25 search for Flutter knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search.py "ListView pagination" --top 3
  python search.py "network http" --domain package
  python search.py "state management" --stack riverpod
  python search.py "login" --json
        """
    )
    
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--domain", "-d", 
        choices=AVAILABLE_DOMAINS, 
        help=f"Search domain (auto-detected if not specified)"
    )
    parser.add_argument(
        "--stack", "-s", 
        choices=AVAILABLE_STACKS, 
        help="Stack preference to exclude conflicting packages"
    )
    parser.add_argument(
        "--top", "-n", 
        type=int, 
        default=MAX_RESULTS, 
        help=f"Max results (default: {MAX_RESULTS})"
    )
    parser.add_argument(
        "--json", "-j", 
        action="store_true", 
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Perform search
    if args.stack:
        result = search_with_stack(args.query, args.stack, args.domain, args.top)
    else:
        result = search(args.query, args.domain, args.top)

    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
