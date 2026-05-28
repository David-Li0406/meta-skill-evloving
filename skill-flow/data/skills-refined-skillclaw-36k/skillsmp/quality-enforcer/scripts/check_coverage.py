#!/usr/bin/env python3
"""Check test coverage meets threshold."""

import json
import subprocess
import sys
from pathlib import Path


def check_coverage(threshold=80):
    """
    Run pytest with coverage and verify threshold.

    Args:
        threshold: Minimum coverage percentage required

    Returns:
        (passed: bool, coverage: float)
    """
    try:
        # Run pytest with coverage
        # Measure coverage for: src/ (main application code)
        subprocess.run(
            ["uv", "run", "pytest", "--cov=src", "--cov-report=term", "--cov-report=json"],
            capture_output=True,
            text=True,
            check=False,
        )

        # Parse coverage from JSON report
        coverage_json = Path("coverage.json")
        if coverage_json.exists():
            with open(coverage_json) as f:
                coverage_data = json.load(f)

            total_coverage = coverage_data["totals"]["percent_covered"]
        else:
            # Fallback: try to parse from stdout
            print("Warning: coverage.json not found, parsing stdout", file=sys.stderr)
            total_coverage = 0.0

        passed = total_coverage >= threshold

        print(f"Coverage: {total_coverage:.1f}%")
        print(f"Threshold: {threshold}%")
        print(f"Status: {'✓ PASS' if passed else '✗ FAIL'}")

        if not passed:
            print(f"\nCoverage is below {threshold}%. Add more tests.")

        return passed, total_coverage

    except FileNotFoundError:
        print("Error: 'uv' command not found. Is uv installed?", file=sys.stderr)
        return False, 0.0
    except Exception as e:
        print(f"Error checking coverage: {e}", file=sys.stderr)
        return False, 0.0


if __name__ == "__main__":
    threshold = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    passed, coverage = check_coverage(threshold)
    sys.exit(0 if passed else 1)
