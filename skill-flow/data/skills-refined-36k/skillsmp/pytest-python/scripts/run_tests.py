#!/usr/bin/env python3
"""
Pytest test runner with common configurations.

Usage:
    python run_tests.py [options] [path]

Options:
    --fast          Run only fast tests (exclude @pytest.mark.slow)
    --failed        Run only previously failed tests
    --coverage      Run with coverage report
    --verbose       Verbose output
    --parallel      Run tests in parallel (requires pytest-xdist)
    --watch         Watch for changes and rerun (requires pytest-watch)

Examples:
    python run_tests.py                    # Run all tests
    python run_tests.py tests/unit/        # Run tests in directory
    python run_tests.py --fast --coverage  # Fast tests with coverage
    python run_tests.py --failed           # Rerun failed tests
"""

import subprocess
import sys
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run pytest with common configurations")
    parser.add_argument("path", nargs="?", default="tests", help="Test path (default: tests)")
    parser.add_argument("--fast", action="store_true", help="Exclude slow tests")
    parser.add_argument("--failed", action="store_true", help="Run only failed tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", action="store_true", help="Run in parallel")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch mode")
    parser.add_argument("--durations", type=int, default=0, help="Show N slowest tests")

    args = parser.parse_args()

    # Build pytest command
    cmd = ["pytest"]

    # Add path
    cmd.append(args.path)

    # Verbose
    if args.verbose:
        cmd.append("-v")

    # Fast mode - exclude slow tests
    if args.fast:
        cmd.extend(["-m", "not slow"])

    # Failed only
    if args.failed:
        cmd.append("--lf")

    # Coverage
    if args.coverage:
        cmd.extend(["--cov", "--cov-report=term-missing"])

    # Parallel (requires pytest-xdist)
    if args.parallel:
        cmd.extend(["-n", "auto"])

    # Show slowest tests
    if args.durations > 0:
        cmd.extend(["--durations", str(args.durations)])

    # Watch mode (requires pytest-watch)
    if args.watch:
        cmd = ["ptw", "--"] + cmd[1:]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
