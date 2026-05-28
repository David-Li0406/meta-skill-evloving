#!/usr/bin/env python3
"""
Deep Research CLI - Unified interface for Perplexity and Gemini Research

Intelligent Model Selection:
- deep_research: Force Deep Research Agent (expensive, 30-60 min)
- perplexity: Force Perplexity Sonar (fast, 30 sec)
- balanced: Deep Research for Phase 1 market analysis, Gemini Pro/Flash otherwise
- auto: Smart detection based on query complexity and context

Usage:
    python deep_research_cli.py "query" --research-mode {perplexity|deep_research|balanced|auto}
    python deep_research_cli.py "query" --output results.md
    python deep_research_cli.py "query" --phase 1 --task-type competitive-analysis
"""

import os
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# Import Gemini research module
from gemini_research import execute_deep_research

# Import Perplexity research
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
from research_lookup import ResearchLookup


DEEP_RESEARCH_KEYWORDS = [
    "competitive landscape", "market analysis", "competitor analysis",
    "comprehensive analysis", "deep dive", "in-depth analysis",
    "strategic analysis", "market landscape", "industry overview",
    "technology evaluation", "architecture decision", "feasibility study",
]


def should_use_gemini(query: str, research_mode: str, phase: Optional[int] = None, task_type: Optional[str] = None) -> bool:
    """Determine if Gemini (vs Perplexity) should be used.

    Note: If True, execute_deep_research will intelligently select:
    - Deep Research Agent (expensive, 30-60 min) for complex analysis
    - Gemini Pro (high quality, 1-5 min) for standard research
    - Gemini Flash (fast, 30-60 sec) for simple lookups
    """

    # Force modes
    if research_mode == "deep_research":
        return True
    elif research_mode == "perplexity":
        return False

    # Balanced mode: Gemini for Phase 1 only (with smart model selection)
    if research_mode == "balanced":
        if phase == 1:
            return True
        return False

    # Auto mode: Smart detection
    if research_mode == "auto":
        # Check for research keywords
        query_lower = query.lower()
        for keyword in DEEP_RESEARCH_KEYWORDS:
            if keyword in query_lower:
                return True

        # Phase-based triggers
        if phase == 1 and task_type in ["competitive-analysis", "market-research"]:
            return True

        # Complex queries (likely need Gemini's deeper reasoning)
        if len(query) > 300:
            return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Deep Research CLI - Unified Perplexity and Gemini interface"
    )
    parser.add_argument(
        "query",
        type=str,
        help="Research query"
    )
    parser.add_argument(
        "--research-mode",
        type=str,
        choices=["perplexity", "deep_research", "balanced", "auto"],
        default="auto",
        help="Research mode selection"
    )
    parser.add_argument(
        "--phase",
        type=int,
        help="Planning phase number (1-6) for context-aware routing"
    )
    parser.add_argument(
        "--task-type",
        type=str,
        help="Task type (e.g., 'competitive-analysis', 'market-research')"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file path"
    )
    parser.add_argument(
        "--force-model",
        type=str,
        choices=["pro", "reasoning"],
        help="Force specific Perplexity model (only used if research_mode=perplexity)"
    )

    args = parser.parse_args()

    # Determine provider (Gemini with smart model selection vs Perplexity)
    use_gemini = should_use_gemini(
        args.query,
        args.research_mode,
        args.phase,
        args.task_type
    )

    print(f"Query: {args.query[:80]}{'...' if len(args.query) > 80 else ''}")
    print(f"Research mode: {args.research_mode}")

    if use_gemini:
        print("Provider: Gemini Deep Research (intelligent model selection)")
        print("="*70)

        # Progress callback
        def progress(msg):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

        # Build context for smart routing
        context = {}
        if args.phase is not None:
            context["phase"] = args.phase
        if args.task_type is not None:
            context["task_type"] = args.task_type

        # Execute Gemini research with smart model selection
        result = execute_deep_research(
            args.query,
            output_file=args.output,
            progress_callback=progress,
            research_mode=args.research_mode,
            context=context if context else None
        )

        if result["success"]:
            print("\n" + "="*70)
            print("RESEARCH RESULTS")
            print("="*70)
            print(result["response"])

            if result.get("sources"):
                print("\n" + "="*70)
                print(f"SOURCES ({len(result['sources'])})")
                print("="*70)
                for i, source in enumerate(result['sources'], 1):
                    if source.get('title'):
                        print(f"{i}. {source['title']}")
                    if source.get('url'):
                        print(f"   {source['url']}")
                    print()

            print("="*70)
            print(f"Duration: {result['metadata']['duration_seconds']/60:.1f} minutes")
            print(f"Model: {result['metadata']['model']}")
        else:
            print(f"\n❌ Deep Research failed: {result['error']}", file=sys.stderr)
            sys.exit(1)

    else:
        print("Provider: Perplexity Sonar (~30 seconds)")
        print("="*70)

        # Execute Perplexity research
        try:
            research = ResearchLookup(force_model=args.force_model)
            result = research.lookup(args.query)

            if result["success"]:
                print("\n" + "="*70)
                print("RESEARCH RESULTS")
                print("="*70)
                print(result["response"])

                if result.get("sources"):
                    print("\n" + "="*70)
                    print(f"SOURCES ({len(result['sources'])})")
                    print("="*70)
                    for i, source in enumerate(result['sources'], 1):
                        if source.get('title'):
                            print(f"{i}. {source['title']}")
                        if source.get('url'):
                            print(f"   {source['url']}")
                        print()

                print("="*70)
                print(f"Model: {result.get('model', 'Perplexity Sonar')}")

                # Save to file if requested
                if args.output:
                    args.output.parent.mkdir(parents=True, exist_ok=True)

                    content = f"""# Research Results

**Query**: {args.query}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Provider**: Perplexity Sonar

---

{result['response']}

"""
                    if result.get("sources"):
                        content += "\n## Sources\n\n"
                        for i, source in enumerate(result['sources'], 1):
                            if source.get("title"):
                                content += f"{i}. **{source['title']}**\n"
                            if source.get("url"):
                                content += f"   {source['url']}\n"
                            content += "\n"

                    args.output.write_text(content, encoding='utf-8')
                    print(f"✅ Results saved to: {args.output}")
            else:
                print(f"\n❌ Research failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"\n❌ Perplexity research failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
