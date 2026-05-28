#!/usr/bin/env python3
"""
Backmerge Workflow Script

Syncs release changes back to development branches.

Uses the release/* branch directly to PR to develop (no separate backmerge branch).
This requires the release branch to still exist when running step 7.

Pattern:
    release/vX.Y.Z ──PR──> develop
                    └──> (delete release/* after merge)

Usage:
    podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/backmerge_workflow.py <step>

Steps:
    pr-develop      - Create PR from release branch to develop
    rebase-contrib  - Rebase contrib branch on develop
    cleanup-release - Delete release branch
    full            - Run all steps in sequence
    status          - Show current backmerge status
"""

import argparse
import subprocess
import sys


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"  → {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_current_branch() -> str:
    """Get current git branch name."""
    result = run_cmd(["git", "branch", "--show-current"], check=False)
    return result.stdout.strip()


def get_contrib_branch() -> str:
    """Get the contrib branch name (contrib/<username>)."""
    result = run_cmd(["gh", "api", "user", "-q", ".login"], check=False)
    username = result.stdout.strip() or "stharrold"
    return f"contrib/{username}"


def return_to_editable_branch() -> bool:
    """Return to the editable branch (contrib/*) after workflow completion."""
    contrib = get_contrib_branch()
    current = get_current_branch()

    if current == contrib:
        print(f"  Already on editable branch: {contrib}")
        return True

    print(f"\n[Return] Switching to editable branch: {contrib}")
    result = run_cmd(["git", "checkout", contrib], check=False)

    if result.returncode != 0:
        print(f"✗ Failed to checkout {contrib}: {result.stderr}")
        return False

    print(f"✓ Now on editable branch: {contrib}")
    return True


def get_latest_version() -> str | None:
    """Get the latest version tag from main."""
    run_cmd(["git", "fetch", "origin", "--tags"], check=False)
    result = run_cmd(["git", "describe", "--tags", "--abbrev=0", "origin/main"], check=False)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def find_release_branch(version: str | None = None) -> str | None:
    """Find the release branch for a version, or the most recent release branch.

    Args:
        version: Specific version to find (e.g., 'v1.6.0'). If None, finds most recent.

    Returns:
        Release branch name (e.g., 'release/v1.6.0') or None if not found.
    """
    run_cmd(["git", "fetch", "origin"], check=False)

    if version:
        # Look for specific version
        branch = f"release/{version}"
        result = run_cmd(["git", "branch", "-r", "--list", f"origin/{branch}"], check=False)
        if result.stdout.strip():
            return branch
        return None

    # Find most recent release branch using semantic version sorting
    # Use git for-each-ref with version sorting to handle v1.10.0 > v1.9.0 correctly
    result = run_cmd(
        ["git", "for-each-ref", "--sort=-version:refname", "--format=%(refname:short)", "refs/remotes/origin/release/"],
        check=False,
    )
    output = result.stdout.strip()
    if not output:
        return None
    # First line is the highest version
    latest = output.split("\n")[0].strip()
    return latest.replace("origin/", "")


def step_pr_develop(version: str | None = None) -> bool:
    """Create PR from release branch to develop.

    Requires the release/* branch to exist. PRs directly from release to develop.
    """
    print("\n" + "=" * 60)
    print("STEP 1: PR Release → Develop")
    print("=" * 60)

    # Determine version from latest tag if not provided
    if not version:
        version = get_latest_version()

    if not version:
        print("✗ Could not determine version (no tags on origin/main?). Specify --version.")
        return False

    print(f"  Backmerging version: {version}")

    # Fetch latest
    run_cmd(["git", "fetch", "origin"], check=False)

    # Find release branch
    release_branch = find_release_branch(version)
    if not release_branch:
        print(f"✗ Release branch release/{version} not found.")
        print("  Step 7 requires the release branch to exist.")
        print("  If the release branch was already deleted, you may need to:")
        print(f"    1. Recreate it from main: git checkout -b release/{version} origin/main")
        print(f"    2. Push it: git push -u origin release/{version}")
        return_to_editable_branch()
        return False

    print(f"  Found release branch: {release_branch}")

    # Check if develop is behind main
    result = run_cmd(["git", "rev-list", "--count", "origin/develop..origin/main"], check=False)
    commits_behind = result.stdout.strip()

    # Handle git rev-list command failure
    if result.returncode != 0:
        print(f"✗ Failed to check commits behind: {result.stderr}")
        return_to_editable_branch()
        return False

    if commits_behind == "0":
        print("⚠️  develop is already up to date with main")
        return_to_editable_branch()
        return True

    print(f"  develop is {commits_behind} commits behind main")

    # Checkout release branch
    print(f"\n[Checkout] Switching to {release_branch}...")
    result = run_cmd(["git", "checkout", release_branch], check=False)
    if result.returncode != 0:
        # Try checking out from remote
        result = run_cmd(["git", "checkout", "-b", release_branch, f"origin/{release_branch}"], check=False)
        if result.returncode != 0:
            print(f"✗ Failed to checkout {release_branch}: {result.stderr}")
            return_to_editable_branch()
            return False

    # Create PR
    print(f"\n[PR] Creating PR: {release_branch} → develop...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "develop",
            "--head",
            release_branch,
            "--title",
            f"backmerge: {version} → develop",
            "--body",
            f"""## Summary

Backmerge release {version} to develop.

Keeps develop in sync with production.

🤖 Generated with [Claude Code](https://claude.com/claude-code)""",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("⚠️  PR already exists")
            return_to_editable_branch()
            return True
        else:
            print(f"✗ PR creation failed: {result.stderr}")
            return_to_editable_branch()
            return False

    # Return to editable branch
    return_to_editable_branch()

    print(f"✓ Step 1 complete: PR created {release_branch} → develop")
    print("\nNext: Merge PR in GitHub, then run: backmerge_workflow.py rebase-contrib")
    return True


def step_rebase_contrib() -> bool:
    """Rebase contrib branch on develop."""
    print("\n" + "=" * 60)
    print("STEP 2: Rebase Contrib on Develop")
    print("=" * 60)

    contrib = get_contrib_branch()

    # Fetch latest
    print("\n[Fetch] Fetching latest...")
    run_cmd(["git", "fetch", "origin"], check=False)

    # Checkout contrib
    print(f"\n[Checkout] Switching to {contrib}...")
    result = run_cmd(["git", "checkout", contrib], check=False)
    if result.returncode != 0:
        print(f"✗ Failed to checkout {contrib}: {result.stderr}")
        return False

    # Check for uncommitted changes
    result = run_cmd(["git", "status", "--porcelain"], check=False)
    if result.stdout.strip():
        print("✗ Uncommitted changes detected. Commit or stash before rebase.")
        return False

    # Rebase on develop
    print(f"\n[Rebase] Rebasing {contrib} onto origin/develop...")
    result = run_cmd(["git", "rebase", "origin/develop"], check=False)

    if result.returncode != 0:
        print("⚠️  Rebase conflict detected!")
        print("  Resolve conflicts manually, then run:")
        print("    git rebase --continue")
        print("    git push --force-with-lease")
        return False

    # Force push with lease
    print(f"\n[Push] Force pushing {contrib}...")
    result = run_cmd(["git", "push", "--force-with-lease", "origin", contrib], check=False)

    if result.returncode != 0:
        print(f"✗ Push failed: {result.stderr}")
        return False

    print(f"✓ Step 2 complete: {contrib} rebased on develop")
    return True


def step_cleanup_release(version: str | None = None) -> bool:
    """Delete release branch locally and remotely."""
    print("\n" + "=" * 60)
    print("STEP 3: Cleanup Release Branch")
    print("=" * 60)

    # Determine version
    if not version:
        version = get_latest_version()

    if not version:
        print("⚠️  No version found, skipping cleanup")
        return True

    # Make sure we're not on a branch we're about to delete
    return_to_editable_branch()

    # Cleanup release branch
    release_branch = f"release/{version}"
    print(f"\n[Delete] Cleaning up {release_branch}...")
    run_cmd(["git", "branch", "-D", release_branch], check=False)
    result = run_cmd(["git", "push", "origin", "--delete", release_branch], check=False)
    if result.returncode != 0:
        if "remote ref does not exist" in result.stderr:
            print("  Release branch already deleted or never existed")
        else:
            print(f"⚠️  Release branch delete warning: {result.stderr}")

    print("✓ Step 3 complete: Release branch cleaned up")
    return True


def show_status() -> None:
    """Show current backmerge status."""
    print("\n" + "=" * 60)
    print("BACKMERGE STATUS")
    print("=" * 60)

    current = get_current_branch()
    contrib = get_contrib_branch()

    print(f"\nCurrent branch: {current}")
    print(f"Contrib branch: {contrib}")

    # Show latest version
    version = get_latest_version()
    if version:
        print(f"Latest version: {version}")
    else:
        print("Latest version: None")

    # Show release branch
    release_branch = find_release_branch()
    if release_branch:
        print(f"Release branch: {release_branch}")
    else:
        print("Release branch: None (already cleaned up)")

    # Check if develop is behind main
    run_cmd(["git", "fetch", "origin"], check=False)
    result = run_cmd(["git", "rev-list", "--count", "origin/develop..origin/main"], check=False)
    if result.returncode != 0:
        print(f"⚠️  Could not check develop status: {result.stderr.strip()}")
        behind_main = None
    else:
        behind_main = result.stdout.strip()
    if behind_main and behind_main != "0":
        print(f"\n⚠️  develop is {behind_main} commits behind main")

    # Check if contrib is behind develop
    result = run_cmd(["git", "rev-list", "--count", f"{contrib}..origin/develop"], check=False)
    if result.returncode != 0:
        print(f"⚠️  Could not check {contrib} status: {result.stderr.strip()}")
        behind_develop = None
    else:
        behind_develop = result.stdout.strip()
    if behind_develop and behind_develop != "0":
        print(f"⚠️  {contrib} is {behind_develop} commits behind develop")

    # Determine next step
    print("\n" + "-" * 40)
    if behind_main and behind_main != "0":
        if release_branch:
            print("Next step: backmerge_workflow.py pr-develop")
        else:
            print("⚠️  develop behind main but no release branch found.")
            print("    Recreate release branch from main if needed.")
    elif behind_develop and behind_develop != "0":
        print("Next step: backmerge_workflow.py rebase-contrib")
    elif release_branch:
        print("Next step: backmerge_workflow.py cleanup-release")
    else:
        print("Status: All synced, ready for next feature")


def run_full_workflow(version: str | None = None) -> bool:
    """Run all workflow steps in sequence."""
    print("\n" + "=" * 60)
    print("FULL BACKMERGE WORKFLOW")
    print("=" * 60)

    # Note: pr-develop requires manual PR merge, so we split the workflow
    print("\n⚠️  Full workflow requires manual PR merge between steps.")
    print("Running pr-develop first...")

    if not step_pr_develop(version):
        return_to_editable_branch()
        return False

    print("\n" + "-" * 40)
    print("MANUAL STEP: Merge the PR in GitHub")
    print("Then run: backmerge_workflow.py rebase-contrib")
    print("-" * 40)

    return True


def main():
    parser = argparse.ArgumentParser(description="Backmerge Workflow", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    parser.add_argument("step", choices=["pr-develop", "rebase-contrib", "cleanup-release", "full", "status"], help="Workflow step to execute")
    parser.add_argument("--version", help="Version for release (e.g., v1.6.0). Auto-detected from tags if not provided.")

    args = parser.parse_args()

    step_map = {
        "pr-develop": lambda: step_pr_develop(args.version),
        "rebase-contrib": step_rebase_contrib,
        "cleanup-release": lambda: step_cleanup_release(args.version),
        "full": lambda: run_full_workflow(args.version),
        "status": show_status,
    }

    success = step_map[args.step]()

    if args.step != "status":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
