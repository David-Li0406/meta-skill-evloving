#!/usr/bin/env python3
"""Create annotated tag on main branch after release merge.

This script implements Step 5.5 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It creates an annotated git tag for the release version and
optionally creates a GitHub release.

Usage:
    python tag_release.py <version> <branch>

Example:
    python tag_release.py v1.1.0 main

Requirements:
    - Version must follow semantic versioning (vX.Y.Z)
    - Branch must exist and be up-to-date with remote
    - Tag must not already exist (locally or remotely)
    - Optional: gh CLI for GitHub release creation
"""

import re
import subprocess
import sys
from pathlib import Path

# Constants with documented rationale
VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency

TAG_MESSAGE_TEMPLATE = "Release {version}: {summary}"
# Rationale: Annotated tags include metadata, recommended for releases


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


def verify_tag_not_exists(version):
    """
    Verify that a version tag doesn't already exist locally or remotely.

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag already exists
    """
    # Check local tags
    try:
        result = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            raise ValueError(f"Tag '{version}' already exists locally. Use 'git tag -l' to list existing tags.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check local git tags: {e.stderr.strip()}") from e

    # Check remote tags
    try:
        result = subprocess.run(["git", "ls-remote", "--tags", "origin", version], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            raise ValueError(f"Tag '{version}' already exists on remote. Use 'git ls-remote --tags origin' to list remote tags.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check remote git tags: {e.stderr.strip()}") from e


def checkout_and_pull_branch(branch_name):
    """
    Checkout branch and pull latest changes from remote.

    Args:
        branch_name: Branch to checkout and update

    Returns:
        Latest commit SHA

    Raises:
        RuntimeError: If checkout or pull fails
    """
    try:
        # Checkout branch
        subprocess.run(["git", "checkout", branch_name], capture_output=True, check=True)

        # Pull latest
        subprocess.run(["git", "pull", "origin", branch_name], capture_output=True, check=True)

        # Get commit SHA
        result = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True)

        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        raise RuntimeError(f"Failed to checkout/pull branch '{branch_name}': {error_msg}") from e


def verify_branch_up_to_date(branch_name):
    """
    Verify local branch is up-to-date with remote.

    Args:
        branch_name: Branch to verify

    Raises:
        RuntimeError: If branch is not up-to-date with remote
    """
    try:
        # Fetch remote refs
        subprocess.run(["git", "fetch", "origin"], capture_output=True, check=True)

        # Compare local and remote
        result = subprocess.run(["git", "rev-list", "--count", f"{branch_name}..origin/{branch_name}"], capture_output=True, text=True, check=True)

        behind_count = int(result.stdout.strip())

        if behind_count > 0:
            raise RuntimeError(f"Branch '{branch_name}' is {behind_count} commit(s) behind origin/{branch_name}. Please pull latest changes first.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to verify branch status: {e.stderr.strip()}") from e


def extract_release_summary(version):
    """
    Extract one-line summary for release from recent commits or CHANGELOG.

    Args:
        version: Release version (e.g., 'v1.1.0')

    Returns:
        One-line summary string
    """
    # Try to extract from CHANGELOG.md first
    changelog_path = Path("CHANGELOG.md")

    if changelog_path.exists():
        try:
            content = changelog_path.read_text()
            # Look for version header in CHANGELOG
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if version in line and i + 1 < len(lines):
                    # Get first non-empty line after version header
                    for j in range(i + 1, min(i + 10, len(lines))):
                        summary = lines[j].strip().lstrip("-").strip()
                        if summary and not summary.startswith("#"):
                            return summary
        except Exception:
            pass  # Fall through to git log method

    # Fallback: use most recent commit message
    try:
        result = subprocess.run(["git", "log", "-1", "--pretty=%s"], capture_output=True, text=True, check=True)

        summary = result.stdout.strip()
        if summary:
            return summary

    except subprocess.CalledProcessError:
        pass

    # Default summary
    return f"Production release {version}"


def create_annotated_tag(version, commit_sha):
    """
    Create annotated git tag with release metadata.

    Args:
        version: Release version (e.g., 'v1.1.0')
        commit_sha: Commit SHA to tag

    Returns:
        Tag message used

    Raises:
        RuntimeError: If tag creation fails
    """
    summary = extract_release_summary(version)
    tag_message = TAG_MESSAGE_TEMPLATE.format(version=version, summary=summary)

    try:
        # Create annotated tag
        subprocess.run(["git", "tag", "-a", version, "-m", tag_message], capture_output=True, check=True)

        return tag_message

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create annotated tag: {e.stderr.decode() if e.stderr else 'Unknown error'}") from e


def push_tag_to_remote(version):
    """
    Push tag to remote origin.

    Args:
        version: Tag name to push

    Raises:
        RuntimeError: If push fails
    """
    try:
        subprocess.run(["git", "push", "origin", version], capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        # Cleanup: delete local tag on push failure
        print("ERROR: Failed to push tag to remote, cleaning up...", file=sys.stderr)
        subprocess.run(["git", "tag", "-d", version], capture_output=True, check=False)

        raise RuntimeError(f"Failed to push tag to remote: {e.stderr.decode() if e.stderr else 'Unknown error'}") from e


def verify_tag_pushed(version):
    """
    Verify tag was successfully pushed to remote.

    Args:
        version: Tag to verify

    Raises:
        RuntimeError: If tag not found on remote
    """
    try:
        result = subprocess.run(["git", "ls-remote", "--tags", "origin", version], capture_output=True, text=True, check=True)

        if not result.stdout.strip():
            raise RuntimeError(f"Tag '{version}' not found on remote after push. Push may have failed silently.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to verify tag on remote: {e.stderr.strip()}") from e


def create_github_release(version):
    """
    Create GitHub release using gh CLI (optional).

    Args:
        version: Release version

    Returns:
        GitHub release URL if successful, None if gh CLI unavailable
    """
    # Check if gh CLI is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Note: gh CLI not available, skipping GitHub release creation", file=sys.stderr)
        return None

    # Create GitHub release
    try:
        result = subprocess.run(["gh", "release", "create", version, "--generate-notes"], capture_output=True, text=True, check=True)

        # Extract URL from output
        release_url = result.stdout.strip()
        return release_url

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to create GitHub release: {e.stderr.strip()}", file=sys.stderr)
        print(f"You can create it manually: gh release create {version} --generate-notes", file=sys.stderr)
        return None


def main():
    """Main entry point for tag_release.py script."""
    if len(sys.argv) != 3:
        print("Usage: tag_release.py <version> <branch>", file=sys.stderr)
        print("Example: tag_release.py v1.1.0 main", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    branch = sys.argv[2]

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_version_format(version)
        verify_branch_exists(branch)
        verify_tag_not_exists(version)

        # Step 2: Branch Operations
        print(f"Checking out {branch} and pulling latest...", file=sys.stderr)
        commit_sha = checkout_and_pull_branch(branch)

        print("Verifying branch is up-to-date...", file=sys.stderr)
        verify_branch_up_to_date(branch)

        # Step 3: Tag Creation
        print("Creating annotated tag...", file=sys.stderr)
        tag_message = create_annotated_tag(version, commit_sha)

        # Step 4: Tag Push
        print("Pushing tag to origin...", file=sys.stderr)
        push_tag_to_remote(version)

        print("Verifying tag push...", file=sys.stderr)
        verify_tag_pushed(version)

        # Step 5: GitHub Release (Optional)
        print("Creating GitHub release...", file=sys.stderr)
        release_url = create_github_release(version)

        # Success output
        print(f"\n✓ Checked out {branch} branch")
        print(f"✓ Pulled latest changes (commit {commit_sha})")
        print(f"✓ Created annotated tag: {version}")
        print(f'  Message: "{tag_message}"')
        print("✓ Pushed tag to origin")

        if release_url:
            print(f"✓ GitHub release created: {release_url}")
        else:
            print("  GitHub release: skipped (gh CLI not available or failed)")

        print("\nNext steps:")
        print("  1. Back-merge to develop: python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py pr-develop")
        print("  2. After PR merged, rebase contrib: python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py rebase-contrib")
        print("  3. Cleanup release branch: python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py cleanup-release")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nTag creation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
