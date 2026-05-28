#!/usr/bin/env python3
"""
Create a GitHub pull request from a description file in docs/prs/.

This script reads the most recent (or specified) PR description file from docs/prs/
and creates a pull request using the gh CLI tool.
"""

from pathlib import Path
import subprocess
import sys


def get_latest_pr_file(pr_dir: Path) -> Path:
    """Get the most recently created PR description file."""
    pr_files = sorted(pr_dir.glob("pr_*.md"), reverse=True)
    if not pr_files:
        raise FileNotFoundError(f"No PR description files found in {pr_dir}")
    return pr_files[0]


def parse_pr_description(filepath: Path) -> tuple[str, str]:
    """
    Parse PR description file to extract title and body.

    Args:
        filepath: Path to the PR description file

    Returns:
        Tuple of (title, body)
    """
    content = filepath.read_text()
    lines = content.split("\n")

    # Extract title (first line after removing '# ' prefix)
    title = lines[0].lstrip("# ").strip() if lines else ""

    # Extract body (everything after the title)
    body = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""

    return title, body


def create_pull_request(title: str, body: str, base: str = "main") -> str:
    """
    Create a pull request using gh CLI.

    Args:
        title: PR title
        body: PR body content
        base: Base branch (default: main)

    Returns:
        The PR URL
    """
    cmd = ["gh", "pr", "create", "--title", title, "--body", body, "--base", base]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main():
    pr_dir = Path("docs/prs")

    if not pr_dir.exists():
        print(f"Error: {pr_dir} directory does not exist", file=sys.stderr)
        print(
            "Run write_pr_description.py first to create a PR description",
            file=sys.stderr,
        )
        sys.exit(1)

    # Get PR file (either specified or latest)
    if len(sys.argv) > 1:
        pr_file = Path(sys.argv[1])
        if not pr_file.exists():
            print(f"Error: File not found: {pr_file}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            pr_file = get_latest_pr_file(pr_dir)
            print(f"Using latest PR description: {pr_file}")
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Parse the PR description
    title, body = parse_pr_description(pr_file)

    if not title:
        print("Error: PR description file is missing a title", file=sys.stderr)
        sys.exit(1)

    # Get base branch (default to main, but can be overridden)
    base = sys.argv[2] if len(sys.argv) > 2 else "main"

    # Create the PR
    try:
        pr_url = create_pull_request(title, body, base)
        print("\n✅ Pull request created successfully!")
        print(f"URL: {pr_url}")

        # Clean up the PR description file
        pr_file.unlink()
        print(f"\n🧹 Cleaned up: {pr_file}")

    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr if isinstance(e.stderr, str) else ""  # pyright: ignore[reportAny]
        print(f"Error creating pull request: {stderr_output}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
