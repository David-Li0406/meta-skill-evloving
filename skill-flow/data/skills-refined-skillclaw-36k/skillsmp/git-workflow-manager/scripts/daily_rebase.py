#!/usr/bin/env python3
"""Perform daily rebase workflow.

Constants:
- TARGET_BRANCH: 'origin/develop'
  Rationale: All contrib branches rebase onto develop for integration

The --force-with-lease flag is used instead of --force for safety:
it only force-pushes if the remote branch hasn't changed since last fetch,
preventing accidental overwrites of others' work.
"""

import subprocess
import sys

# Constants with documented rationale
TARGET_BRANCH = "origin/develop"  # Integration branch for all contributions


def daily_rebase(contrib_branch):
    """
    Rebase contrib branch onto develop.

    Steps:
    1. Verify branch exists and no uncommitted changes
    2. Checkout contrib branch
    3. Fetch origin
    4. Rebase onto origin/develop
    5. Force push with lease (safe force push)

    Args:
        contrib_branch: Name of contrib branch (e.g., 'contrib/username')

    Returns:
        bool: True if successful, False if failed

    Raises:
        ValueError: If inputs are invalid
    """
    # Input validation
    if not contrib_branch or not contrib_branch.startswith("contrib/"):
        raise ValueError(f"Invalid contrib branch '{contrib_branch}'. Must start with 'contrib/' (e.g., 'contrib/username')")

    print(f"Rebasing {contrib_branch} onto develop...", file=sys.stderr)

    # Check for uncommitted changes
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("ERROR: You have uncommitted changes. Please commit or stash them first.", file=sys.stderr)
            print("\nUncommitted changes:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print("ERROR: Failed to check git status", file=sys.stderr)
        print(f"Git error: {e.stderr}", file=sys.stderr)
        return False

    # Verify contrib branch exists
    try:
        subprocess.run(["git", "rev-parse", "--verify", contrib_branch], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print(f"ERROR: Branch '{contrib_branch}' does not exist", file=sys.stderr)
        print("\nAvailable contrib branches:", file=sys.stderr)
        subprocess.run(["git", "branch", "--list", "contrib/*"], check=False)
        return False

    try:
        # Checkout contrib branch
        print(f"Checking out {contrib_branch}...", file=sys.stderr)
        subprocess.run(["git", "checkout", contrib_branch], check=True, capture_output=True)

        # Fetch latest from origin
        print("Fetching from origin...", file=sys.stderr)
        subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)

        # Rebase onto origin/develop
        print(f"Rebasing onto {TARGET_BRANCH}...", file=sys.stderr)
        result = subprocess.run(["git", "rebase", TARGET_BRANCH], check=True, capture_output=True, text=True)

        # Force push with lease (safe force push - only pushes if remote hasn't changed)
        print("Pushing to origin...", file=sys.stderr)
        subprocess.run(["git", "push", "origin", contrib_branch, "--force-with-lease"], check=True, capture_output=True)

        print(f"✓ {contrib_branch} successfully rebased onto develop", file=sys.stderr)
        return True

    except subprocess.CalledProcessError as e:
        print("✗ Rebase failed", file=sys.stderr)
        if e.stderr:
            print(f"\nGit error: {e.stderr.strip()}", file=sys.stderr)

        print("\nTo resolve conflicts:", file=sys.stderr)
        print("  1. Fix conflicts in affected files", file=sys.stderr)
        print("  2. git add <resolved-files>", file=sys.stderr)
        print("  3. git rebase --continue", file=sys.stderr)
        print(f"  4. git push origin {contrib_branch} --force-with-lease", file=sys.stderr)
        print("\nOr to abort the rebase:", file=sys.stderr)
        print("  git rebase --abort", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: daily_rebase.py <contrib_branch>", file=sys.stderr)
        print("\nExample: daily_rebase.py contrib/johndoe", file=sys.stderr)
        print("\nThis rebases your contrib branch onto origin/develop.", file=sys.stderr)
        sys.exit(1)

    try:
        success = daily_rebase(sys.argv[1])
        sys.exit(0 if success else 1)
    except ValueError as e:
        print(f"\n{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)
