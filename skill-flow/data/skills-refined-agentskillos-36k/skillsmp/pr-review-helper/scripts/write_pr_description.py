#!/usr/bin/env python3
"""
Write a PR description to a deterministic location for review.

This script creates a PR description file in docs/prs/ with a timestamp-based
filename for easy tracking and review before submission.
"""

from datetime import datetime
from pathlib import Path
import sys


def write_pr_description(title: str, body: str) -> str:
    """
    Write PR description to docs/prs/ directory.

    Args:
        title: The PR title
        body: The PR body content

    Returns:
        The path to the created file
    """
    # Create docs/prs directory if it doesn't exist
    pr_dir = Path("docs/prs")
    pr_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = pr_dir / f"pr_{timestamp}.md"

    # Write the PR description
    content = f"# {title}\n\n{body}"
    _ = filename.write_text(content)

    return str(filename)


def main():
    if len(sys.argv) < 3:
        print("Usage: write_pr_description.py <title> <body>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print(
            '  write_pr_description.py "Add new feature" "## Summary\\n- Added X\\n- Fixed Y"',
            file=sys.stderr,
        )
        sys.exit(1)

    title = sys.argv[1]
    body = sys.argv[2]

    filepath = write_pr_description(title, body)
    print(f"PR description written to: {filepath}")
    print("\nPlease review and edit the file before creating the PR.")


if __name__ == "__main__":
    main()
