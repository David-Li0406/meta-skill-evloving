#!/usr/bin/env python3
"""Create PR to merge release branch back to develop after main merge.

⚠️ BRANCH PROTECTION EXCEPTION POLICY ⚠️

This script handles the ONLY workflow that merges to the protected branch
`develop` outside of feature PRs. The develop branch is a protected branch
that requires PRs (but not approvals) for ALL merges. This script creates a
pull request (never pushes directly) to ensure proper workflow and compliance.

Previous versions of this script merged directly to develop, which violated
branch protection. This was fixed in v1.8.0 to enforce PR workflow. As of
v1.8.0, PR approval is no longer required (self-merge enabled).

This script implements Step 5.6 of Phase 5 (Release Workflow) as documented
in WORKFLOW.md. It rebases the release branch onto the target branch first
to ensure clean, linear history, then creates a pull request to merge the
release branch back into develop.

⚠️ PRE-PR REBASE REQUIREMENT ⚠️

This script ALWAYS rebases the release branch onto the target branch before
creating the PR. This ensures:
- Clean, linear git history (no merge commits)
- PR is up-to-date with target branch (no "branch out-of-date" warnings)
- Easier code review (only shows actual changes from release)
- Follows git best practices

Usage:
    python backmerge_release.py <version> <target_branch>

Example:
    python backmerge_release.py v1.1.0 develop

Requirements:
    - Release branch release/<version> must exist
    - Target branch must exist
    - Tag <version> must exist (ensures release was tagged)
    - Working directory must be clean (no uncommitted changes)
    - gh CLI or az CLI required for PR creation
"""

import re
import subprocess
import sys

# Constants with documented rationale
VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"
# Rationale: Enforce semantic versioning (vMAJOR.MINOR.PATCH) for consistency

RELEASE_BRANCH_PREFIX = "release/"
# Rationale: git-flow release branch naming convention

MERGE_STRATEGY = "--no-ff"
# Rationale: Preserves release branch history in develop, easier to track releases

INVALID_SOURCE_BRANCHES = ["main", "master", "develop"]
# Rationale: Backmerge must be from release/* branch, NEVER from main/develop.
# Merging main → develop is incorrect git-flow and can cause issues.


def validate_not_main_or_develop(version: str) -> None:
    """
    Validate that backmerge source is NOT main, master, or develop.

    This prevents the common mistake of merging main → develop instead of
    release/vX.Y.Z → develop. The correct git-flow backmerge is always
    from the release branch.

    Args:
        version: Version string (should be vX.Y.Z, NOT a branch name)

    Raises:
        ValueError: If version looks like main, master, or develop
    """
    version_lower = version.lower()
    if version_lower in INVALID_SOURCE_BRANCHES:
        raise ValueError(
            f"❌ INVALID BACKMERGE SOURCE: '{version}'\n\n"
            f"Backmerge must be from a release/* branch, NOT from {version}.\n\n"
            f"CORRECT: backmerge_release.py v1.1.0 develop\n"
            f"         (merges release/v1.1.0 → develop)\n\n"
            f"WRONG:   Manually creating PR from main → develop\n"
            f"         This violates git-flow and can cause issues.\n\n"
            f"The release branch contains release-specific changes that need\n"
            f"to be merged back to develop. Use the release branch, not main."
        )


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
    Verify that version tag exists (ensures release was tagged).

    Args:
        version: Version tag to check (e.g., 'v1.1.0')

    Raises:
        ValueError: If tag doesn't exist
    """
    try:
        result = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True, check=True)

        if not result.stdout.strip():
            raise ValueError(
                f"Tag '{version}' does not exist. "
                f"Release must be tagged before back-merge. "
                f"Run: python .claude/skills/git-workflow-manager/scripts/tag_release.py {version} main"
            )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git tags: {e.stderr.strip()}") from e


def check_working_directory_clean():
    """
    Verify working directory has no uncommitted changes.

    Raises:
        RuntimeError: If working directory has uncommitted changes
    """
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)

        if result.stdout.strip():
            raise RuntimeError("Working directory has uncommitted changes. Please commit or stash changes before back-merge.")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to check git status: {e.stderr.strip()}") from e


def rebase_release_branch(release_branch, target_branch):
    """
    Rebase release branch onto target branch before creating PR.

    This ensures the PR has a clean, linear history and is up-to-date
    with the target branch, avoiding "branch out-of-date" warnings and
    merge commits.

    Args:
        release_branch: Release branch name (e.g., 'release/v1.9.0')
        target_branch: Target branch name (e.g., 'develop')

    Raises:
        RuntimeError: If rebase fails or encounters conflicts
    """
    try:
        # Fetch latest target and release branches (Issue #137)
        subprocess.run(["git", "fetch", "origin", target_branch, release_branch], capture_output=True, text=True, check=True)

        # Checkout release branch
        subprocess.run(["git", "checkout", release_branch], capture_output=True, text=True, check=True)

        # Rebase onto target branch
        result = subprocess.run(
            ["git", "rebase", f"origin/{target_branch}"],
            capture_output=True,
            text=True,
            check=False,  # Don't raise on conflict
        )

        if result.returncode != 0:
            # Rebase failed - abort and provide helpful error (Issue #136)
            subprocess.run(["git", "rebase", "--abort"], capture_output=True, check=False)
            # Check both stderr and stdout to distinguish conflict from other failures (Issue #140, #146)
            # Extract error parts with intermediate variables for clarity (Issue #152)
            stderr_part = result.stderr or ""
            stdout_part = result.stdout or ""
            separator = "\n" if stderr_part and stdout_part else ""
            error_output = stderr_part + separator + stdout_part
            if "CONFLICT" in error_output or "conflict" in error_output.lower():
                error_type = "Rebase conflict"
            else:
                error_type = "Rebase failed"

            raise RuntimeError(
                f"{error_type} when rebasing {release_branch} onto origin/{target_branch}.\n"
                f"Error output: {error_output.strip()}\n\n"
                f"Manual resolution required:\n"
                f"  1. git checkout {release_branch}\n"
                f"  2. git rebase origin/{target_branch}\n"
                f"  3. Resolve conflicts (if any)\n"
                f"  4. git rebase --continue\n"
                f"  5. git push --force-with-lease origin {release_branch}\n"
                f"  6. Re-run this script"
            )

        # Force push rebased branch
        subprocess.run(["git", "push", "--force-with-lease", "origin", release_branch], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        # More specific error message (Issue #135, #141)
        error_msg = e.stderr.strip() if e.stderr else str(e)
        if "fetch" in str(e.cmd):
            operation = "fetch"
        elif "checkout" in str(e.cmd):
            operation = "checkout"
        elif "push" in str(e.cmd):
            operation = "push"
        else:
            # e.cmd check is safe: empty lists are falsy in Python (Issue #147)
            operation = f"git command ({e.cmd[0] if e.cmd else 'unknown'})"
        raise RuntimeError(f"Failed to {operation} during rebase operation: {error_msg}") from e


def create_pr(version, target_branch):
    """
    Create PR to merge release branch back to target branch.

    This function creates a PR for back-merge. The release branch is rebased
    onto the target branch first to ensure clean, linear history and avoid
    "branch out-of-date" warnings.

    Args:
        version: Release version (e.g., 'v1.1.0')
        target_branch: Target branch (e.g., 'develop')

    Returns:
        PR URL if successful

    Raises:
        RuntimeError: If gh/az CLI not available or PR creation fails
    """
    # Check if gh CLI is available
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("gh CLI not available. Cannot create PR. Install gh CLI: https://cli.github.com/")

    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    # Build PR title and body
    pr_title = f"chore(release): back-merge {version} to {target_branch}"

    # Get tag URL
    try:
        result = subprocess.run(["gh", "repo", "view", "--json", "url", "--jq", ".url"], capture_output=True, text=True, check=True)
        repo_url = result.stdout.strip()
        tag_url = f"{repo_url}/releases/tag/{version}"
    except subprocess.CalledProcessError:
        tag_url = f"Release {version}"

    pr_body = f"""## Back-merge Release to Develop

This PR merges `{release_branch}` back to `{target_branch}` to complete the release cycle.

### Release Information
- **Version:** {version}
- **Release Tag:** {tag_url}
- **Source Branch:** `{release_branch}`
- **Target Branch:** `{target_branch}`

### What This PR Does

Merges release-specific changes (documentation, version bumps) from the release branch back to develop, ensuring develop stays in sync with production releases.

### Review Instructions

1. **Review changes** - Verify documentation updates and version changes
2. **Wait for CI** - Ensure all tests pass
3. **Merge** - Use GitHub/Azure DevOps portal merge button when ready (no approval required)

GitHub will automatically detect any merge conflicts. If conflicts exist, resolve them in the PR.

This follows the git-flow release workflow where all merges to develop go through PRs, even for release back-merges.

### Next Steps After Merge

Run cleanup script:
```bash
python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}
```

---
*Generated by backmerge_release.py*
"""

    try:
        # Create PR
        result = subprocess.run(
            ["gh", "pr", "create", "--base", target_branch, "--head", release_branch, "--title", pr_title, "--body", pr_body], capture_output=True, text=True, check=True
        )

        pr_url = result.stdout.strip()
        return pr_url

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create PR: {e.stderr.strip()}") from e


def main():
    """Main entry point for backmerge_release.py script."""
    if len(sys.argv) != 3:
        print("Usage: backmerge_release.py <version> <target_branch>", file=sys.stderr)
        print("Example: backmerge_release.py v1.1.0 develop", file=sys.stderr)
        sys.exit(1)

    version = sys.argv[1]
    target_branch = sys.argv[2]

    release_branch = f"{RELEASE_BRANCH_PREFIX}{version}"

    try:
        # Step 1: Input Validation
        print("Validating inputs...", file=sys.stderr)
        validate_not_main_or_develop(version)  # Prevent main → develop mistake
        validate_version_format(version)
        verify_branch_exists(release_branch)
        verify_branch_exists(target_branch)
        verify_tag_exists(version)

        # Step 2: Check working directory is clean (Issue #134)
        check_working_directory_clean()

        # Step 3: Rebase release branch onto target branch
        print(f"Rebasing {release_branch} onto {target_branch}...", file=sys.stderr)
        rebase_release_branch(release_branch, target_branch)
        print("✓ Rebase successful", file=sys.stderr)

        # Step 4: Create PR
        print("Creating pull request for back-merge...", file=sys.stderr)
        pr_url = create_pr(version, target_branch)

        # Output
        print(f"\n✓ Created PR: {pr_url}")
        print(f'  Title: "chore(release): back-merge {version} to {target_branch}"')
        print("\n📋 Next steps:")
        print("  1. Review PR in GitHub/Azure DevOps portal")
        print("  2. Wait for CI checks to pass")
        print("  3. Merge through portal when ready")
        print(f"  4. Run cleanup: python .claude/skills/git-workflow-manager/scripts/cleanup_release.py {version}")

    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBack-merge cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
