#!/usr/bin/env python3
"""Delete release branch after successful release and back-merge.

This script implements Step 5.7 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It safely deletes the release branch after verifying the
release is complete and properly merged.

Usage:
    python cleanup_release.py <version>

Example:
    python cleanup_release.py v1.1.0

Requirements:
    - Release branch release/<version> must exist
    - Tag <version> must exist
    - Tag must be on main branch
    - Release commits must be in develop branch
    - All safety checks must pass
"""

import re
import subprocess
import sys
from pathlib import Path

# Constants with documented rationale
VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency

RELEASE_BRANCH_PREFIX = "release/"
# Rationale: git-flow release branch naming convention

REQUIRED_BRANCHES = ["main", "develop"]
# Rationale: Ensures release is in both production and integration branches


def validate_version_format(version):
    """
    Validate version follows semantic versioning pattern.

    Args:
        version: Version string to validate (e.g., 'v1.1.0')

    Raises:
        ValueError: If version doesn't match vX.Y.Z pattern
    """
    if not re.match(VERSION_PATTERN, version):
        raise ValueError(f"Invalid version format '{version}'. Must match pattern vX.Y.Z (e.g., v1.1.0, v2.0.0)")


def verify_branch_exists(branch_name):
    """
    Verify that a git branch exists.

    Args:
        branch_name: Name of branch to verify

    Raises:
        ValueError: If branch doesn't exist
    """
    try:
        subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        raise ValueError(f"Branch '{branch_name}' does not exist. Use 'git branch -a' to list available branches.")


def verify_tag_exists(version):
    """
    Verify that version tag exists.

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag doesn't exist
    """
    try:
        result = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True, check=True)

        if not result.stdout.strip():
            raise ValueError(
                f"Tag '{version}' not found. Release may not be complete. "
                f"Ensure release was tagged: python .claude/skills/git-workflow-manager/scripts/tag_release.py {version} main"
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git tags: {e.stderr.strip()}") from e


def verify_tag_on_branch(version, branch_name):
    """
    Verify that tag exists on specified branch.

    Args:
        version: Version tag (e.g., 'v1.1.0')
        branch_name: Branch to check (e.g., 'main')

    Raises:
        ValueError: If tag not on branch
    """
    try:
        # Get commit SHA for tag
        result = subprocess.run(["git", "rev-list", "-n", "1", version], capture_output=True, text=True, check=True)
        tag_commit = result.stdout.strip()

        # Check if commit is in branch
        result = subprocess.run(["git", "branch", "--contains", tag_commit], capture_output=True, text=True, check=True)

        branches = result.stdout.strip()

        if branch_name not in branches:
            raise ValueError(f"Tag '{version}' not on {branch_name}. Release merge incomplete. Ensure release PR was merged to {branch_name}.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to verify tag on branch: {e.stderr.strip()}") from e


def verify_commits_in_branch(release_branch, target_branch):
    """
    Verify all commits from release branch are in target branch.

    Args:
        release_branch: Release branch name (e.g., 'release/v1.1.0')
        target_branch: Target branch to check (e.g., 'develop')

    Raises:
        ValueError: If release commits not in target branch
    """
    try:
        # Get commits in release branch but not in target
        result = subprocess.run(["git", "log", f"{target_branch}..{release_branch}", "--oneline"], capture_output=True, text=True, check=True)

        missing_commits = result.stdout.strip()

        if missing_commits:
            commit_count = len(missing_commits.split("\n"))
            raise ValueError(
                f"Release not back-merged to {target_branch}. "
                f"{commit_count} commit(s) from {release_branch} not in {target_branch}. "
                f"Run: python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop"
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to verify commits in branch: {e.stderr.strip()}") from e


def delete_local_branch(branch_name):
    """
    Delete local git branch (uses -d for safety).

    Args:
        branch_name: Branch to delete

    Raises:
        RuntimeError: If deletion fails
    """
    try:
        # Use -d (not -D) to ensure branch is fully merged
        subprocess.run(["git", "branch", "-d", branch_name], capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"

        if "not fully merged" in error_msg:
            raise RuntimeError(f"Branch '{branch_name}' is not fully merged. This indicates release workflow is incomplete. Safety check failed - branch not deleted.")
        else:
            raise RuntimeError(f"Failed to delete local branch: {error_msg}") from e


def delete_remote_branch(branch_name):
    """
    Delete remote git branch.

    Args:
        branch_name: Branch to delete (without 'origin/' prefix)

    Raises:
        RuntimeError: If deletion fails
    """
    try:
        subprocess.run(["git", "push", "origin", "--delete", branch_name], capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        raise RuntimeError(f"Failed to delete remote branch: {error_msg}") from e


def find_todo_file(version):
    """
    Find TODO file for release version.

    Args:
        version: Release version (e.g., 'v1.1.0')

    Returns:
        Path to TODO file, or None if not found
    """
    version_slug = version.replace(".", "-")

    # Get repo root
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        repo_root = Path(result.stdout.strip())

    except subprocess.CalledProcessError:
        return None

    # Search for TODO file matching pattern
    # Pattern: TODO_release_<timestamp>_<version-slug>.md
    todo_files = list(repo_root.glob(f"TODO_release_*_{version_slug}.md"))

    if not todo_files:
        return None

    # Return most recent if multiple found
    return sorted(todo_files)[-1]


def archive_todo_file(todo_path, version):
    """
    Archive TODO file using deprecate_files.py.

    Args:
        todo_path: Path to TODO file
        version: Release version for description

    Raises:
        RuntimeError: If archival fails
    """
    deprecate_script = Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts" / "deprecate_files.py"

    if not deprecate_script.exists():
        print("Warning: deprecate_files.py not found, skipping TODO archival", file=sys.stderr)
        return

    try:
        description = f"release-{version.replace('.', '-')}"

        subprocess.run(["python3", str(deprecate_script), str(todo_path), description, str(todo_path)], capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to archive TODO file: {e.stderr.decode()}", file=sys.stderr)
        print(f"You may need to manually archive: {todo_path}", file=sys.stderr)


def main():
    """Main entry point for cleanup_release.py script."""
    if len(sys.argv) != 2:
        print("Usage: cleanup_release.py <version>", file=sys.stderr)
        print("Example: cleanup_release.py v1.1.0", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_version_format(version)
        verify_branch_exists(release_branch)

        # Step 2: Safety Checks
        print("Running safety checks...", file=sys.stderr)

        print("  Checking tag exists...", file=sys.stderr)
        verify_tag_exists(version)

        print("  Checking tag on main...", file=sys.stderr)
        verify_tag_on_branch(version, "main")

        print("  Checking back-merge to develop...", file=sys.stderr)
        verify_commits_in_branch(release_branch, "develop")

        # Step 3: Delete Branches
        print("Deleting branches...", file=sys.stderr)

        print("  Deleting local branch...", file=sys.stderr)
        delete_local_branch(release_branch)

        print("  Deleting remote branch...", file=sys.stderr)
        delete_remote_branch(release_branch)

        # Step 4: Archive TODO File
        print("Archiving TODO file...", file=sys.stderr)
        todo_path = find_todo_file(version)

        if todo_path:
            archive_todo_file(todo_path, version)
        else:
            print(f"  Note: No TODO file found for {version}", file=sys.stderr)

        # Success output
        print(f"\n✓ Verified tag {version} exists")
        print("✓ Verified tag on main branch")
        print("✓ Verified back-merge to develop complete")
        print(f"✓ Deleted local branch: {release_branch}")
        print(f"✓ Deleted remote branch: origin/{release_branch}")

        if todo_path:
            print(f"✓ Archived: {todo_path.name}")

        print(f"✓ Release workflow complete for {version}")

        print("\nNext steps:")
        print("  1. Update contrib branch: python .claude/skills/git-workflow-manager/scripts/daily_rebase.py contrib/<gh-user>")
        print("  2. Continue development on develop or feature branches")

    except (ValueError, RuntimeError) as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        print("\nSafety checks failed. Release branch NOT deleted.", file=sys.stderr)
        print("\nManual cleanup commands (use with caution):", file=sys.stderr)
        print(f"  git branch -D {release_branch}", file=sys.stderr)
        print(f"  git push origin --delete {release_branch}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCleanup cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
