#!/usr/bin/env python3
"""
Code Hotspot Analyzer

Identifies high-risk code areas using git churn + complexity analysis.

Hotspot = High Code Churn + High Complexity
Research shows 4-5x more bugs in hotspots than other code.

Usage:
    python analyze_hotspots.py src/
    python analyze_hotspots.py src/ --since "6 months ago"
    python analyze_hotspots.py src/ --top 10
    python analyze_hotspots.py src/ --json > hotspots.json

Requirements:
    pip install radon
    git repository (for churn analysis)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def get_git_churn(path: str, since: str = "6 months ago") -> Dict[str, int]:
    """
    Get code churn (number of commits) for each file.

    Args:
        path: Directory to analyze
        since: Time period for churn analysis (e.g., "6 months ago")

    Returns:
        Dict mapping file path to commit count
    """
    try:
        # Get all commits that modified Python files in path
        result = subprocess.run(
            [
                "git", "log",
                f"--since={since}",
                "--pretty=format:",
                "--name-only",
                "--",
                path
            ],
            capture_output=True,
            text=True,
            check=True
        )

        # Count occurrences of each file
        files = [line.strip() for line in result.stdout.splitlines() if line.strip().endswith('.py')]

        churn = {}
        for file_path in files:
            churn[file_path] = churn.get(file_path, 0) + 1

        return churn

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running git log: {e.stderr}", file=sys.stderr)
        print("   Make sure you're in a git repository", file=sys.stderr)
        sys.exit(1)


def get_complexity_stats(path: str) -> Dict[str, Dict]:
    """
    Get complexity statistics for each file.

    Args:
        path: Directory to analyze

    Returns:
        Dict mapping file path to {avg_cc, max_cc, functions}
    """
    try:
        # Run radon with JSON output
        result = subprocess.run(
            ["radon", "cc", path, "-a", "--json"],
            capture_output=True,
            text=True,
            check=True
        )

        radon_data = json.loads(result.stdout)

        # Calculate stats per file
        stats = {}
        for file_path, items in radon_data.items():
            if not items:
                continue

            complexities = [item.get("complexity", 0) for item in items]
            stats[file_path] = {
                "avg_cc": sum(complexities) / len(complexities) if complexities else 0,
                "max_cc": max(complexities) if complexities else 0,
                "function_count": len(items),
                "functions": [
                    {
                        "name": item.get("name", ""),
                        "lineno": item.get("lineno", 0),
                        "complexity": item.get("complexity", 0),
                    }
                    for item in items
                ]
            }

        return stats

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running radon: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing radon output: {e}", file=sys.stderr)
        sys.exit(1)


def classify_hotspot(churn: int, max_cc: int) -> Tuple[str, int]:
    """
    Classify file as hotspot based on churn and complexity.

    Returns:
        (priority_label, priority_number)
        Priority: 0 (Critical), 1 (Monitor), 2 (Tech Debt), 3 (Stable)
    """
    high_churn = churn > 15
    high_complexity = max_cc > 10

    if high_churn and high_complexity:
        return ("P0 - CRITICAL", 0)
    elif high_churn and not high_complexity:
        return ("P1 - Monitor", 1)
    elif not high_churn and high_complexity:
        return ("P2 - Tech Debt", 2)
    else:
        return ("P3 - Stable", 3)


def print_analysis(hotspots: List[Dict], top: int = None, since: str = "6 months ago"):
    """
    Print formatted hotspot analysis.

    Args:
        hotspots: List of hotspot data
        top: Show only top N hotspots
        since: Time period analyzed
    """
    print("=" * 60)
    print(f"HOTSPOT ANALYSIS (Last {since})")
    print("=" * 60)
    print()

    # Group by priority
    by_priority = {0: [], 1: [], 2: [], 3: []}
    for hotspot in hotspots:
        priority = hotspot["priority_number"]
        by_priority[priority].append(hotspot)

    # P0 - Critical
    p0_hotspots = by_priority[0]
    if p0_hotspots:
        print("P0 - CRITICAL HOTSPOTS (High Churn + High Complexity):")
        print("━" * 60)

        for hs in sorted(p0_hotspots, key=lambda x: x["churn"], reverse=True)[:top]:
            print(f"  🔥 {hs['file']}")
            print(f"     Commits: {hs['churn']} | Avg CC: {hs['avg_cc']:.1f} | Max CC: {hs['max_cc']}")

            # Show top complex functions
            if hs['top_functions']:
                print(f"     Top complex functions:")
                for func in hs['top_functions'][:3]:
                    print(f"       • {func['name']} (line {func['lineno']}) - CC: {func['complexity']}")

            print(f"     🚨 Action: PRIORITY REFACTOR")
            print()

    # P1 - Monitor
    p1_hotspots = by_priority[1]
    if p1_hotspots:
        print("P1 - MONITOR (High Churn + Low Complexity):")
        print("━" * 60)

        for hs in sorted(p1_hotspots, key=lambda x: x["churn"], reverse=True)[:top]:
            print(f"  ⚠️  {hs['file']}")
            print(f"     Commits: {hs['churn']} | Avg CC: {hs['avg_cc']:.1f} | Max CC: {hs['max_cc']}")
            print(f"     Action: Add integration tests, monitor complexity")
            print()

    # P2 - Tech Debt
    p2_hotspots = by_priority[2]
    if p2_hotspots:
        print("P2 - TECHNICAL DEBT (Low Churn + High Complexity):")
        print("━" * 60)

        for hs in sorted(p2_hotspots, key=lambda x: x["max_cc"], reverse=True)[:top]:
            print(f"  📝 {hs['file']}")
            print(f"     Commits: {hs['churn']} | Avg CC: {hs['avg_cc']:.1f} | Max CC: {hs['max_cc']}")
            print(f"     Action: Refactor when modifying")
            print()

    # Summary
    print("Summary:")
    print("━" * 60)

    total_files = len(hotspots)
    p0_count = len(p0_hotspots)
    p1_count = len(p1_hotspots)
    p2_count = len(p2_hotspots)
    p3_count = len(by_priority[3])

    print(f"  Total Files Analyzed: {total_files}")
    print(f"  P0 Critical: {p0_count} files ({p0_count / total_files * 100:.1f}%)" if total_files > 0 else "  P0 Critical: 0")
    print(f"  P1 Monitor: {p1_count} files ({p1_count / total_files * 100:.1f}%)" if total_files > 0 else "  P1 Monitor: 0")
    print(f"  P2 Tech Debt: {p2_count} files ({p2_count / total_files * 100:.1f}%)" if total_files > 0 else "  P2 Tech Debt: 0")
    print(f"  P3 Stable: {p3_count} files ({p3_count / total_files * 100:.1f}%)" if total_files > 0 else "  P3 Stable: 0")
    print()

    # Recommendations
    if p0_count > 0:
        print("Recommendations:")
        for hs in sorted(p0_hotspots, key=lambda x: x["churn"], reverse=True)[:3]:
            print(f"  🔥 URGENT: Refactor {hs['file']} ({hs['churn']} commits, CC {hs['max_cc']})")

        if p1_count > 0:
            print()
            for hs in sorted(p1_hotspots, key=lambda x: x["churn"], reverse=True)[:2]:
                print(f"  ⚠️  Add tests to {hs['file']} before complexity increases")


def print_json(hotspots: List[Dict]):
    """Print hotspot data as JSON."""
    print(json.dumps(hotspots, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Identify code hotspots using git churn + complexity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_hotspots.py src/
  python analyze_hotspots.py src/ --since "3 months ago"
  python analyze_hotspots.py src/ --top 10
  python analyze_hotspots.py src/ --json > hotspots.json

Priority Levels:
  P0 - Critical: High churn + High complexity (refactor immediately)
  P1 - Monitor: High churn + Low complexity (add tests, watch complexity)
  P2 - Tech Debt: Low churn + High complexity (refactor when touching)
  P3 - Stable: Low churn + Low complexity (no action needed)
        """
    )

    parser.add_argument(
        "path",
        help="Directory to analyze"
    )

    parser.add_argument(
        "--since",
        default="6 months ago",
        help="Time period for churn analysis (default: 6 months ago)"
    )

    parser.add_argument(
        "--top",
        type=int,
        help="Show only top N hotspots per priority level"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Validate path exists
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Error: Path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)

    # Get churn and complexity data
    churn_data = get_git_churn(args.path, args.since)
    complexity_data = get_complexity_stats(args.path)

    # Combine data
    hotspots = []
    for file_path in set(churn_data.keys()) | set(complexity_data.keys()):
        churn = churn_data.get(file_path, 0)
        complexity = complexity_data.get(file_path, {})

        max_cc = complexity.get("max_cc", 0)
        avg_cc = complexity.get("avg_cc", 0)
        functions = complexity.get("functions", [])

        # Sort functions by complexity
        top_functions = sorted(functions, key=lambda x: x["complexity"], reverse=True)

        priority_label, priority_number = classify_hotspot(churn, max_cc)

        hotspots.append({
            "file": file_path,
            "churn": churn,
            "avg_cc": avg_cc,
            "max_cc": max_cc,
            "function_count": complexity.get("function_count", 0),
            "top_functions": top_functions,
            "priority_label": priority_label,
            "priority_number": priority_number,
        })

    # Output results
    if args.json:
        print_json(hotspots)
    else:
        print_analysis(hotspots, args.top, args.since)


if __name__ == "__main__":
    main()
