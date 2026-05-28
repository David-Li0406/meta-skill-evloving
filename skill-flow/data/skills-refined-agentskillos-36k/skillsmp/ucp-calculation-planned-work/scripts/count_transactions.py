#!/usr/bin/env python3
"""
Transaction Counter for Use Case Points (UCP) Analysis

This script parses work item descriptions and acceptance criteria to count
weighted transactions for UCP calculations.

Weighting:
- Framework/SDK operations: 0.5 transactions
- Custom business logic: 1.0 transactions

Usage:
    python count_transactions.py "acceptance criteria text"
    python count_transactions.py --file work_item.txt
"""

import re
import argparse
from typing import Tuple


def count_transactions(text: str) -> Tuple[int, float]:
    """
    Count transactions from acceptance criteria text.

    Args:
        text: Work item description or acceptance criteria

    Returns:
        Tuple of (raw_count, weighted_count)
    """
    if not text:
        return (0, 0.0)

    raw_count = 0

    # Numbered lists (1., 2., etc.)
    numbered = len(re.findall(r'^\s*\d+[\.)]\s+', text, re.MULTILINE))
    raw_count += numbered

    # Bullet points (-, *, •)
    bullets = len(re.findall(r'^\s*[-*•]\s+', text, re.MULTILINE))
    raw_count += bullets

    # "Should" statements (testable requirements)
    shoulds = len(re.findall(r'\bshould\b', text, re.IGNORECASE))
    raw_count += shoulds

    # "Must" statements (mandatory requirements)
    musts = len(re.findall(r'\bmust\b', text, re.IGNORECASE))
    raw_count += musts

    # Estimate weighted count (default: 80% custom, 20% framework)
    # User should adjust based on actual framework usage
    weighted_count = raw_count * 0.9  # Conservative estimate

    return (raw_count, weighted_count)


def classify_use_case(transaction_count: float) -> Tuple[str, int]:
    """
    Classify use case complexity based on transaction count.

    Args:
        transaction_count: Weighted transaction count

    Returns:
        Tuple of (classification, UUCW)
    """
    if transaction_count <= 3:
        return ("Simple", 5)
    elif transaction_count <= 7:
        return ("Average", 10)
    else:
        return ("Complex", 15)


def analyze_work_item(text: str, verbose: bool = False) -> dict:
    """
    Analyze a work item and return UCP metrics.

    Args:
        text: Work item description/acceptance criteria
        verbose: Print detailed breakdown

    Returns:
        Dictionary with analysis results
    """
    raw_count, weighted_count = count_transactions(text)
    classification, uucw = classify_use_case(weighted_count)

    result = {
        "raw_transactions": raw_count,
        "weighted_transactions": weighted_count,
        "classification": classification,
        "uucw": uucw
    }

    if verbose:
        print(f"Raw Transactions: {raw_count}")
        print(f"Weighted Transactions: {weighted_count:.1f}")
        print(f"Classification: {classification}")
        print(f"UUCW: {uucw}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Count transactions for UCP analysis"
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Work item text to analyze"
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Read work item from file"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed breakdown"
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return

    result = analyze_work_item(text, verbose=args.verbose)

    if not args.verbose:
        print(f"{result['weighted_transactions']:.1f} transactions → "
              f"{result['classification']} → {result['uucw']} UUCW")


if __name__ == "__main__":
    main()
