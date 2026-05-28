#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flutter Pro Max Search - CLI for Flutter knowledge base search
Usage: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--top 5]
       python search.py "<query>" --design-system [-p "Project Name"]
       python search.py "<query>" --design-system --persist [-p "Project Name"] [--page "dashboard"]

Domains: widget, package, pattern, architect, chart, color, typography, style, ux, icon, landing, naming, product, prompt, performance, ui-reasoning, accessibility
Stacks: riverpod, bloc, provider

Persistence (Master + Overrides pattern):
  --persist    Save design system to design-system/MASTER.md
  --page       Also create a page-specific override file in design-system/pages/
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
from design_system import generate_design_system, persist_design_system
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
    # Design system generation
    parser.add_argument(
        "--design-system", "-ds",
        action="store_true",
        help="Generate complete design system recommendation"
    )
    parser.add_argument(
        "--project-name", "-p",
        type=str,
        default=None,
        help="Project name for design system output"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["ascii", "markdown"],
        default="ascii",
        help="Output format for design system"
    )
    # Persistence (Master + Overrides pattern)
    parser.add_argument(
        "--persist",
        action="store_true",
        help="Save design system to design-system/MASTER.md (creates hierarchical structure)"
    )
    parser.add_argument(
        "--page",
        type=str,
        default=None,
        help="Create page-specific override file in design-system/pages/"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=None,
        help="Output directory for persisted files (default: current directory)"
    )

    args = parser.parse_args()

    # Design system takes priority
    if args.design_system:
        result = generate_design_system(
            args.query,
            args.project_name,
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # Print persistence confirmation
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system persisted to design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md (Global Source of Truth)")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (Screen Overrides)")
            print("")
            print(f"📖 Usage: When building a screen, check design-system/{project_slug}/pages/[screen].md first.")
            print(f"   If exists, its rules override MASTER.md. Otherwise, use MASTER.md.")
            print("=" * 60)
        return

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
