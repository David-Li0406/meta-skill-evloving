#!/usr/bin/env python3
"""
Calculate requirements coverage score from coverage counts.

Usage:
    python calculate_coverage_score.py --total 20 --covered 15 --partial 3
    python calculate_coverage_score.py --coverage-json coverage.json
"""

import argparse
import json
import sys


def calculate_coverage(total, covered, partial):
    """
    Calculate requirements coverage score (0-100%).

    Scoring:
    - Fully covered requirements: 100% weight
    - Partially covered requirements: 50% weight
    - Uncovered requirements: 0% weight

    Formula: ((covered × 1.0) + (partial × 0.5)) / total × 100
    """
    if total == 0:
        return 0.0

    weighted_coverage = (covered * 1.0) + (partial * 0.5)
    coverage = (weighted_coverage / total) * 100

    return round(coverage, 2)


def get_recommendation(coverage, phase="feature"):
    """Get recommendation based on coverage and analysis phase."""
    if phase == "feature":
        # After feature planning, all critical requirements should be covered
        if coverage >= 95:
            return "EXCELLENT", "✅"
        elif coverage >= 85:
            return "GOOD", "✅"
        elif coverage >= 70:
            return "ACCEPTABLE", "⚠️"
        else:
            return "INSUFFICIENT", "❌"
    elif phase == "wave":
        # Before wave implementation, feature requirements must be complete
        if coverage >= 100:
            return "COMPLETE", "✅"
        elif coverage >= 90:
            return "NEAR_COMPLETE", "⚠️"
        else:
            return "INCOMPLETE", "❌"
    elif phase == "epic":
        # Epic completion review
        if coverage >= 95:
            return "ACHIEVED", "✅"
        elif coverage >= 85:
            return "MOSTLY_ACHIEVED", "✅"
        elif coverage >= 70:
            return "PARTIALLY_ACHIEVED", "⚠️"
        else:
            return "NOT_ACHIEVED", "❌"
    elif phase == "release":
        # Release planning
        if coverage >= 98:
            return "READY", "✅"
        elif coverage >= 90:
            return "NEAR_READY", "⚠️"
        else:
            return "NOT_READY", "❌"
    else:
        return "UNKNOWN", "❓"


def main():
    parser = argparse.ArgumentParser(
        description="Calculate requirements coverage score"
    )

    # Option 1: Individual counts
    parser.add_argument("--total", type=int, default=0,
                       help="Total number of requirements")
    parser.add_argument("--covered", type=int, default=0,
                       help="Number of fully covered requirements")
    parser.add_argument("--partial", type=int, default=0,
                       help="Number of partially covered requirements")

    # Option 2: JSON input
    parser.add_argument("--coverage-json", type=str,
                       help="Path to JSON file with coverage counts")

    # Phase for recommendation
    parser.add_argument("--phase", type=str, default="feature",
                       choices=["feature", "wave", "epic", "release"],
                       help="Analysis phase for recommendation threshold")

    # Output format
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load counts
    if args.coverage_json:
        try:
            with open(args.coverage_json, 'r') as f:
                data = json.load(f)
                total = data.get("total", 0)
                covered = data.get("covered", 0)
                partial = data.get("partial", 0)
        except Exception as e:
            print(f"Error loading JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        total = args.total
        covered = args.covered
        partial = args.partial

    # Validate
    if total < (covered + partial):
        print("Error: covered + partial cannot exceed total", file=sys.stderr)
        sys.exit(1)

    # Calculate coverage
    uncovered = total - covered - partial
    coverage = calculate_coverage(total, covered, partial)
    recommendation, emoji = get_recommendation(coverage, args.phase)

    # Output
    if args.format == "json":
        result = {
            "coverage_percentage": coverage,
            "total_requirements": total,
            "fully_covered": covered,
            "partially_covered": partial,
            "uncovered": uncovered,
            "recommendation": recommendation,
            "phase": args.phase
        }
        print(json.dumps(result, indent=2))
    else:
        covered_pct = (covered / total * 100) if total > 0 else 0
        partial_pct = (partial / total * 100) if total > 0 else 0
        uncovered_pct = (uncovered / total * 100) if total > 0 else 0

        print(f"Requirements Coverage: {coverage}% {emoji}")
        print(f"")
        print(f"Coverage Breakdown:")
        print(f"  Total Requirements: {total}")
        print(f"  Fully Covered:      {covered} ({covered_pct:.1f}%)")
        print(f"  Partially Covered:  {partial} ({partial_pct:.1f}%)")
        print(f"  Uncovered:          {uncovered} ({uncovered_pct:.1f}%)")
        print(f"")
        print(f"Recommendation ({args.phase} phase): {recommendation} {emoji}")

        # Additional guidance
        if recommendation in ["INSUFFICIENT", "INCOMPLETE", "NOT_ACHIEVED", "NOT_READY"]:
            print(f"")
            print(f"⚠️  Action Required:")
            if uncovered > 0:
                print(f"   - Address {uncovered} uncovered requirement(s)")
            if partial > 0:
                print(f"   - Complete {partial} partially covered requirement(s)")

    # Exit code based on recommendation
    if recommendation in ["INSUFFICIENT", "INCOMPLETE", "NOT_ACHIEVED", "NOT_READY"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
