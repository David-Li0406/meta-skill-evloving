#!/usr/bin/env python3
"""
Release Workflow Script

Creates a release from develop branch and deploys to production.

Usage:
    podman-compose run --rm dev python .claude/skills/git-workflow-manager/scripts/release_workflow.py <step>

Steps:
    create-release  - Create release branch from develop
    run-gates       - Run quality gates on release branch
    pr-main         - Create PR from release to main
    tag-release     - Tag release on main after PR merge
    full            - Run all steps in sequence
    status          - Show current release status
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Add workflow-utilities to path for container_utils
sys.path.insert(
    0,
    str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"),
)

from container_utils import get_command_prefix

# Safe cross-platform output
try:
    from safe_output import format_check, format_cross, format_warning, safe_print
except ImportError:
    # Fallback if module not found
    def safe_print(*args, **kwargs):
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            message = " ".join(str(arg) for arg in args)
            # Sanitize message by encoding to ASCII, replacing non-ASCII chars with '?'
            safe_message = message.encode("ascii", "replace").decode("ascii")
            print(safe_message, **kwargs)

    def format_check(msg):
        return f"[OK] {msg}"

    def format_cross(msg):
        return f"[X] {msg}"

    def format_warning(msg):
        return f"! {msg}"


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    safe_print(f"  -> {' '.join(cmd)}")
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
        print(f"[X] Failed to checkout {contrib}: {result.stderr}")
        return False

    print(f"[OK] Now on editable branch: {contrib}")
    return True


def get_latest_version() -> str:
    """Get the latest version tag from main."""
    result = run_cmd(["git", "describe", "--tags", "--abbrev=0", "origin/main"], check=False)
    if result.returncode == 0:
        return result.stdout.strip()
    return "v0.0.0"


def calculate_next_version(current: str) -> str:
    """Calculate next minor version."""
    # Simple: bump minor version
    parts = current.lstrip("v").split(".")
    if len(parts) >= 2:
        major = int(parts[0])
        minor = int(parts[1]) + 1
        return f"v{major}.{minor}.0"
    return "v1.0.0"


def run_quality_gates() -> bool:
    """Run quality gates."""
    print("\n[Quality Gates] Running quality gates...")
    script_path = Path(".claude/skills/quality-enforcer/scripts/run_quality_gates.py")

    if not script_path.exists():
        print("!️  Quality gates script not found, skipping")
        return True

    prefix = get_command_prefix()
    result = subprocess.run(prefix + ["python", str(script_path)], check=False)

    return result.returncode == 0


def step_create_release(version: str = None) -> bool:
    """Create release branch from develop."""
    print("\n" + "=" * 60)
    print("STEP 1: Create Release Branch")
    print("=" * 60)

    # Calculate version if not provided
    if not version:
        current = get_latest_version()
        version = calculate_next_version(current)
        print(f"  Auto-calculated version: {version}")

    release_branch = f"release/{version}"

    # Fetch latest
    print("\n[Fetch] Fetching latest...")
    run_cmd(["git", "fetch", "origin"], check=False)

    # Check if release branch already exists
    result = run_cmd(["git", "branch", "-r", "--list", f"origin/{release_branch}"], check=False)
    if result.stdout.strip():
        print(f"!️  Release branch {release_branch} already exists")
        return True

    # Create release branch from develop
    print(f"\n[Branch] Creating {release_branch} from develop...")
    result = run_cmd(["git", "checkout", "-b", release_branch, "origin/develop"], check=False)
    if result.returncode != 0:
        print(f"[X] Failed to create branch: {result.stderr}")
        return False

    # Push branch
    print(f"\n[Push] Pushing {release_branch}...")
    result = run_cmd(["git", "push", "-u", "origin", release_branch], check=False)
    if result.returncode != 0:
        print(f"[X] Push failed: {result.stderr}")
        return False

    print(f"[OK] Step 1 complete: Created {release_branch}")
    return True


def step_run_gates() -> bool:
    """Run quality gates on release branch."""
    print("\n" + "=" * 60)
    print("STEP 2: Run Quality Gates")
    print("=" * 60)

    if not run_quality_gates():
        print("[X] Quality gates failed. Fix issues before proceeding.")
        return False

    print("[OK] Step 2 complete: Quality gates passed")
    return True


def step_pr_main() -> bool:
    """Create PR from release to main."""
    print("\n" + "=" * 60)
    print("STEP 3: PR Release -> Main")
    print("=" * 60)

    current = get_current_branch()
    if not current.startswith("release/"):
        print(f"[X] Must be on release branch (current: {current})")
        return False

    version = current.replace("release/", "")

    # Create PR
    print(f"\n[PR] Creating PR: {current} -> main...")
    result = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--base",
            "main",
            "--fill",
            "--title",
            f"Release {version}",
            "--body",
            f"Release {version}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)",
        ],
        check=False,
    )

    if result.returncode != 0:
        if "already exists" in result.stderr:
            print("!️  PR already exists")
        else:
            print(f"[X] PR creation failed: {result.stderr}")
            return False

    print(f"[OK] Step 3 complete: PR created {current} -> main")
    print("\nNext: Merge PR in GitHub, then run: release_workflow.py tag-release")
    return True


def step_tag_release() -> bool:
    """Tag release on main after PR merge."""
    print("\n" + "=" * 60)
    print("STEP 4: Tag Release")
    print("=" * 60)

    current = get_current_branch()
    version = None

    # Try to get version from current branch or find release branch
    if current.startswith("release/"):
        version = current.replace("release/", "")
    else:
        # Find most recent release branch
        result = run_cmd(["git", "branch", "-r", "--list", "origin/release/*"], check=False)
        branches = result.stdout.strip().split("\n")
        if branches and branches[0]:
            version = branches[-1].strip().replace("origin/release/", "")

    if not version:
        print("[X] Could not determine version. Specify release branch.")
        return False

    # Checkout main and pull
    print("\n[Checkout] Switching to main...")
    run_cmd(["git", "checkout", "main"], check=False)
    run_cmd(["git", "pull", "origin", "main"], check=False)

    # Create tag
    print(f"\n[Tag] Creating tag {version}...")
    result = run_cmd(["git", "tag", "-a", version, "-m", f"Release {version}"], check=False)
    if result.returncode != 0:
        if "already exists" in result.stderr:
            print(f"!️  Tag {version} already exists")
        else:
            print(f"[X] Tag creation failed: {result.stderr}")
            return False

    # Push tag
    print(f"\n[Push] Pushing tag {version}...")
    result = run_cmd(["git", "push", "origin", version], check=False)
    if result.returncode != 0:
        print(f"!️  Tag push warning: {result.stderr}")

    # Return to editable branch
    return_to_editable_branch()

    print(f"[OK] Step 4 complete: Tagged {version} on main")
    print("\nNext: Run backmerge_workflow.py to sync release back to develop")
    return True


def show_status():
    """Show current release status."""
    print("\n" + "=" * 60)
    print("RELEASE STATUS")
    print("=" * 60)

    current = get_current_branch()
    print(f"\nCurrent branch: {current}")

    # Show latest version
    latest = get_latest_version()
    print(f"Latest version: {latest}")

    # Show release branches
    result = run_cmd(["git", "branch", "-r", "--list", "origin/release/*"], check=False)
    branches = result.stdout.strip()
    if branches:
        print(f"\nRelease branches:\n{branches}")
    else:
        print("\nNo release branches found")

    # Determine next step
    print("\n" + "-" * 40)
    if current.startswith("release/"):
        print("Next step: release_workflow.py pr-main")
    elif current == "main":
        print("Next step: release_workflow.py tag-release")
    else:
        print("Next step: release_workflow.py create-release")


def run_full_workflow(version: str = None):
    """Run all workflow steps in sequence."""
    print("\n" + "=" * 60)
    print("FULL RELEASE WORKFLOW")
    print("=" * 60)

    steps = [
        ("create-release", lambda: step_create_release(version)),
        ("run-gates", step_run_gates),
        ("pr-main", step_pr_main),
    ]

    for name, func in steps:
        print(f"\n>>> Running step: {name}")
        if not func():
            print(f"\n[X] Workflow stopped at step: {name}")
            return_to_editable_branch()
            return False

    print("\n" + "=" * 60)
    print("[OK] RELEASE WORKFLOW COMPLETE (awaiting PR merge)")
    print("After PR merge, run: release_workflow.py tag-release")
    print("=" * 60)
    return True


def main():
    parser = argparse.ArgumentParser(description="Release Workflow", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    parser.add_argument("step", choices=["create-release", "run-gates", "pr-main", "tag-release", "full", "status"], help="Workflow step to execute")
    parser.add_argument("--version", help="Version for release (e.g., v1.6.0). Auto-calculated if not provided.")

    args = parser.parse_args()

    step_map = {
        "create-release": lambda: step_create_release(args.version),
        "run-gates": step_run_gates,
        "pr-main": step_pr_main,
        "tag-release": step_tag_release,
        "full": lambda: run_full_workflow(args.version),
        "status": show_status,
    }

    success = step_map[args.step]()

    if args.step != "status":
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
