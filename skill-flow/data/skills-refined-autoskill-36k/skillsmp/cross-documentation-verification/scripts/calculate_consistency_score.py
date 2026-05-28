#!/usr/bin/env python3
"""
Calculate cross-documentation consistency score from issue counts.

Usage:
    python calculate_consistency_score.py --conflicts 1 --gaps 3 --duplication 2 --drift 5
    python calculate_consistency_score.py --issues-json issues.json
"""

import argparse
import json
import sys


def calculate_score(conflicts, gaps, duplication, drift):
    """
    Calculate consistency score (0-100).

    Scoring:
    - Start at 100
    - Conflicts: -20 points each
    - Gaps: -5 points each
    - Duplication: -3 points each
    - Drift: -1 point each
    - Minimum score: 0
    """
    score = 100
    score -= (conflicts * 20)
    score -= (gaps * 5)
    score -= (duplication * 3)
    score -= (drift * 1)

    return max(0, score)


def get_recommendation(score, phase="feature"):
    """Get recommendation based on score and verification phase."""
    if phase == "feature":
        if score >= 70:
            return "PROCEED", "✅"
        elif score >= 50:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    elif phase == "wave":
        if score >= 80:
            return "PROCEED", "✅"
        elif score >= 60:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    elif phase == "implementation":
        if score >= 90:
            return "PROCEED", "✅"
        elif score >= 75:
            return "REVISE", "⚠️"
        else:
            return "BLOCK", "❌"
    elif phase == "audit":
        if score >= 85:
            return "EXCELLENT", "✅"
        elif score >= 70:
            return "GOOD", "✅"
        elif score >= 50:
            return "NEEDS_WORK", "⚠️"
        else:
            return "POOR", "❌"
    else:
        return "UNKNOWN", "❓"


def main():
    parser = argparse.ArgumentParser(
        description="Calculate cross-documentation consistency score"
    )

    # Option 1: Individual counts
    parser.add_argument("--conflicts", type=int, default=0,
                       help="Number of conflicts")
    parser.add_argument("--gaps", type=int, default=0,
                       help="Number of gaps")
    parser.add_argument("--duplication", type=int, default=0,
                       help="Number of duplication issues")
    parser.add_argument("--drift", type=int, default=0,
                       help="Number of drift items")

    # Option 2: JSON input
    parser.add_argument("--issues-json", type=str,
                       help="Path to JSON file with issue counts")

    # Phase for recommendation
    parser.add_argument("--phase", type=str, default="feature",
                       choices=["feature", "wave", "implementation", "audit"],
                       help="Verification phase for recommendation threshold")

    # Output format
    parser.add_argument("--format", type=str, default="text",
                       choices=["text", "json"],
                       help="Output format")

    args = parser.parse_args()

    # Load counts
    if args.issues_json:
        try:
            with open(args.issues_json, 'r') as f:
                data = json.load(f)
                conflicts = data.get("conflicts", 0)
                gaps = data.get("gaps", 0)
                duplication = data.get("duplication", 0)
                drift = data.get("drift", 0)
        except Exception as e:
            print(f"Error loading JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        conflicts = args.conflicts
        gaps = args.gaps
        duplication = args.duplication
        drift = args.drift

    # Calculate score
    score = calculate_score(conflicts, gaps, duplication, drift)
    recommendation, emoji = get_recommendation(score, args.phase)

    # Output
    if args.format == "json":
        result = {
            "score": score,
            "max_score": 100,
            "issues": {
                "conflicts": conflicts,
                "gaps": gaps,
                "duplication": duplication,
                "drift": drift
            },
            "recommendation": recommendation,
            "phase": args.phase
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Consistency Score: {score}/100 {emoji}")
        print(f"")
        print(f"Issues:")
        print(f"  Conflicts:    {conflicts} (-{conflicts * 20} points)")
        print(f"  Gaps:         {gaps} (-{gaps * 5} points)")
        print(f"  Duplication:  {duplication} (-{duplication * 3} points)")
        print(f"  Drift:        {drift} (-{drift * 1} points)")
        print(f"")
        print(f"Recommendation ({args.phase} phase): {recommendation} {emoji}")

    # Exit code based on recommendation
    if recommendation in ["BLOCK", "POOR"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
