#!/usr/bin/env python3
"""
Calculate architectural conformance score from violation counts.

Usage:
    python calculate_conformance_score.py --critical 2 --warnings 5 --info 3
    python calculate_conformance_score.py --violations-json violations.json
"""

import argparse
import json
import sys


def calculate_score(critical, warnings, info):
    """
    Calculate conformance score (0-100).

    Scoring:
    - Start at 100
    - Critical violations: -20 points each
    - Warnings: -5 points each
    - Info items: -1 point each
    - Minimum score: 0
    """
    score = 100
    score -= (critical * 20)
    score -= (warnings * 5)
    score -= (info * 1)

    return max(0, score)


def get_recommendation(score, phase="design"):
    """Get recommendation based on score and validation phase."""
    if phase == "design":
        if score >= 70:
            return "PROCEED", "✅"
        elif score >= 50:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    elif phase == "implementation":
        if score >= 80:
            return "PROCEED", "✅"
        elif score >= 60:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    elif phase == "production":
        if score >= 90:
            return "PROCEED", "✅"
        elif score >= 75:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    else:
        return "UNKNOWN", "❓"


def main():
    parser = argparse.ArgumentParser(
        description="Calculate architectural conformance score"
    )

    # Option 1: Individual counts
    parser.add_argument("--critical", type=int, default=0,
                       help="Number of critical violations")
    parser.add_argument("--warnings", type=int, default=0,
                       help="Number of warnings")
    parser.add_argument("--info", type=int, default=0,
                       help="Number of info items")

    # Option 2: JSON input
    parser.add_argument("--violations-json", type=str,
                       help="Path to JSON file with violation counts")

    # Phase for recommendation
    parser.add_argument("--phase", type=str, default="design",
                       choices=["design", "implementation", "production"],
                       help="Validation phase for recommendation threshold")

    # Output format
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load counts
    if args.violations_json:
        try:
            with open(args.violations_json, 'r') as f:
                data = json.load(f)
                critical = data.get("critical", 0)
                warnings = data.get("warnings", 0)
                info = data.get("info", 0)
        except Exception as e:
            print(f"Error loading JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        critical = args.critical
        warnings = args.warnings
        info = args.info

    # Calculate score
    score = calculate_score(critical, warnings, info)
    recommendation, emoji = get_recommendation(score, args.phase)

    # Output
    if args.format == "json":
        result = {
            "score": score,
            "max_score": 100,
            "violations": {
                "critical": critical,
                "warnings": warnings,
                "info": info
            },
            "recommendation": recommendation,
            "phase": args.phase
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Conformance Score: {score}/100 {emoji}")
        print(f"")
        print(f"Violations:")
        print(f"  Critical: {critical} (-{critical * 20} points)")
        print(f"  Warnings: {warnings} (-{warnings * 5} points)")
        print(f"  Info:     {info} (-{info * 1} points)")
        print(f"")
        print(f"Recommendation ({args.phase} phase): {recommendation} {emoji}")

    # Exit code based on recommendation
    if recommendation == "BLOCK":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
