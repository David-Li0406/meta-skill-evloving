#!/usr/bin/env python3
"""
Extract work item ID from git commit message.

Usage:
    python extract_work_item_from_commit.py --commit-sha abc123
    python extract_work_item_from_commit.py --commit-message "feat(#1234): Description"
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Optional, Dict


def get_commit_message(commit_sha: str) -> Optional[str]:
    """Get commit message for given SHA."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit message: {e}", file=sys.stderr)
        return None


def extract_work_item_id(commit_message: str) -> Optional[int]:
    """
    Extract work item ID from commit message.

    Supports patterns:
    - feat(#1234): Description
    - fix: Description (#1234)
    - Description [#1234]
    - #1234: Description
    """
    patterns = [
        r'\(#(\d+)\)',      # feat(#1234)
        r'\(#(\d+)\)',      # (#1234)
        r'#(\d+)',          # #1234
        r'\[#(\d+)\]',      # [#1234]
    ]

    for pattern in patterns:
        match = re.search(pattern, commit_message)
        if match:
            return int(match.group(1))

    return None


def get_commit_details(commit_sha: str) -> Optional[Dict]:
    """Get detailed commit information."""
    try:
        # Get commit message
        message_result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%s', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )

        # Get commit body
        body_result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%b', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )

        # Get files changed
        files_result = subprocess.run(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )

        # Get commit date
        date_result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%ci', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )

        # Get author
        author_result = subprocess.run(
            ['git', 'log', '-1', '--pretty=format:%an', commit_sha],
            capture_output=True,
            text=True,
            check=True
        )

        files_changed = [f for f in files_result.stdout.strip().split('\n') if f]

        return {
            "commit_sha": commit_sha,
            "message": message_result.stdout.strip(),
            "body": body_result.stdout.strip(),
            "files_changed": files_changed,
            "date": date_result.stdout.strip(),
            "author": author_result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit details: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Extract work item ID from git commit message"
    )

    parser.add_argument("--commit-sha", type=str,
                       help="Git commit SHA")
    parser.add_argument("--commit-message", type=str,
                       help="Commit message (if not using commit SHA)")
    parser.add_argument("--format", type=str, default="json",
                       choices=["json", "text"],
                       help="Output format")
    parser.add_argument("--include-details", action="store_true",
                       help="Include full commit details")

    args = parser.parse_args()

    # Get commit message
    if args.commit_message:
        commit_message = args.commit_message
        commit_details = None
    elif args.commit_sha:
        commit_message = get_commit_message(args.commit_sha)
        if not commit_message:
            print("Error: Could not retrieve commit message", file=sys.stderr)
            sys.exit(1)

        if args.include_details:
            commit_details = get_commit_details(args.commit_sha)
        else:
            commit_details = None
    else:
        print("Error: Must specify either --commit-sha or --commit-message", file=sys.stderr)
        sys.exit(1)

    # Extract work item ID
    work_item_id = extract_work_item_id(commit_message)

    if work_item_id is None:
        if args.format == "json":
            result = {
                "work_item_id": None,
                "commit_message": commit_message,
                "error": "No work item ID found in commit message"
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"No work item ID found in commit message: {commit_message}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.format == "json":
        result = {
            "work_item_id": work_item_id,
            "commit_message": commit_message
        }

        if commit_details:
            result["commit_details"] = commit_details

        print(json.dumps(result, indent=2))
    else:
        print(f"Work Item ID: {work_item_id}")
        print(f"Commit Message: {commit_message}")

        if commit_details:
            print(f"Commit SHA: {commit_details['commit_sha']}")
            print(f"Author: {commit_details['author']}")
            print(f"Date: {commit_details['date']}")
            print(f"Files Changed: {len(commit_details['files_changed'])}")


if __name__ == "__main__":
    main()
