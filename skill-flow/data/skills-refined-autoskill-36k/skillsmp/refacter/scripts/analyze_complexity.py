#!/usr/bin/env python3
"""
Code Complexity Analyzer

Analyzes Python code complexity using radon and provides actionable recommendations.

Usage:
    python analyze_complexity.py src/
    python analyze_complexity.py src/ --max-cc 10 --max-cognitive 15
    python analyze_complexity.py src/ --json > complexity.json

Requirements:
    pip install radon
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def run_radon_cc(path: str) -> List[Dict]:
    """
    Run radon cyclomatic complexity analysis.

    Args:
        path: Directory or file to analyze

    Returns:
        List of complexity results (file, function, cc, cognitive)
    """
    try:
        # Run radon with JSON output
        result = subprocess.run(
            ["radon", "cc", path, "-a", "--json"],
            capture_output=True,
            text=True,
            check=True
        )

        # Parse JSON output
        radon_data = json.loads(result.stdout)

        # Flatten to list of functions
        functions = []
        for file_path, items in radon_data.items():
            for item in items:
                functions.append({
                    "file": file_path,
                    "name": item.get("name", ""),
                    "lineno": item.get("lineno", 0),
                    "col_offset": item.get("col_offset", 0),
                    "complexity": item.get("complexity", 0),
                    "rank": item.get("rank", "A"),
                })

        return functions

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running radon: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing radon output: {e}", file=sys.stderr)
        sys.exit(1)


def rank_to_severity(rank: str) -> str:
    """Convert radon rank to severity level."""
    severity_map = {
        "A": "✅ Simple",
        "B": "⚠️  Moderate",
        "C": "🔧 Complex",
        "D": "🚨 Very Complex",
        "F": "🔥 Extremely Complex",
    }
    return severity_map.get(rank, "Unknown")


def print_analysis(functions: List[Dict], max_cc: int = 10, max_cognitive: int = 15):
    """
    Print formatted complexity analysis.

    Args:
        functions: List of function complexity data
        max_cc: Maximum acceptable cyclomatic complexity
        max_cognitive: Maximum acceptable cognitive complexity
    """
    # Filter high complexity functions
    high_complexity = [
        f for f in functions
        if f["complexity"] > max_cc
    ]

    print("=" * 60)
    print("CODE COMPLEXITY ANALYSIS")
    print("=" * 60)
    print()

    if not high_complexity:
        print("✅ All functions are within complexity thresholds!")
        print(f"   Max CC threshold: {max_cc}")
        print()
    else:
        print(f"High Complexity Functions (CC > {max_cc}):")
        print("━" * 60)

        # Group by file
        by_file = {}
        for func in high_complexity:
            file_path = func["file"]
            if file_path not in by_file:
                by_file[file_path] = []
            by_file[file_path].append(func)

        for file_path, funcs in sorted(by_file.items()):
            print(f"  📄 {file_path}")

            for func in sorted(funcs, key=lambda x: x["complexity"], reverse=True):
                severity = rank_to_severity(func["rank"])
                print(f"     {severity} {func['name']} (line {func['lineno']}) - CC: {func['complexity']}")

                # Recommend action based on complexity
                if func["complexity"] > 20:
                    print(f"        Action: 🚨 URGENT - Major refactoring required")
                elif func["complexity"] > 15:
                    print(f"        Action: 🔧 Extract multiple methods, simplify conditionals")
                elif func["complexity"] > 10:
                    print(f"        Action: ⚠️  Extract method or simplify logic")

            print()

    # Summary statistics
    print("Summary:")
    print("━" * 60)

    total_functions = len(functions)
    high_count = len(high_complexity)
    avg_cc = sum(f["complexity"] for f in functions) / total_functions if total_functions > 0 else 0
    max_func = max(functions, key=lambda x: x["complexity"]) if functions else None

    print(f"  Total Functions: {total_functions}")
    print(f"  High Complexity (CC > {max_cc}): {high_count} ({high_count / total_functions * 100:.1f}%)" if total_functions > 0 else "  High Complexity: 0")
    print(f"  Average CC: {avg_cc:.1f}")

    if max_func:
        print(f"  Max CC: {max_func['complexity']} ({max_func['file']}:{max_func['name']})")

    print()

    # Recommendations
    if high_count > 0:
        print("Recommendations:")
        print("  🔧 Refactor high complexity functions")
        print("  ⚠️  Add tests before refactoring")
        print("  📊 Monitor complexity trends over time")
        print()
        print("See REFACTORING-PATTERNS.md for refactoring techniques.")


def print_json(functions: List[Dict]):
    """Print complexity data as JSON."""
    print(json.dumps(functions, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python code complexity using radon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_complexity.py src/
  python analyze_complexity.py src/ --max-cc 10 --max-cognitive 15
  python analyze_complexity.py src/ --json > complexity.json
        """
    )

    parser.add_argument(
        "path",
        help="Directory or file to analyze"
    )

    parser.add_argument(
        "--max-cc",
        type=int,
        default=10,
        help="Maximum acceptable cyclomatic complexity (default: 10)"
    )

    parser.add_argument(
        "--max-cognitive",
        type=int,
        default=15,
        help="Maximum acceptable cognitive complexity (default: 15)"
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

    # Run analysis
    functions = run_radon_cc(args.path)

    # Output results
    if args.json:
        print_json(functions)
    else:
        print_analysis(functions, args.max_cc, args.max_cognitive)


if __name__ == "__main__":
    main()
