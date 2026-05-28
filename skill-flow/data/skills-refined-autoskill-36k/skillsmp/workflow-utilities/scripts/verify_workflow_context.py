#!/usr/bin/env python3
"""Verify workflow context - ensures commands run in correct location/branch.

This script validates that workflow commands are executed in the correct
context (main repo vs worktree, correct branch prefix).

Usage:
    # Explicit flags
    python verify_workflow_context.py --require-main-repo --require-branch contrib/

    # Step shortcuts (recommended)
    python verify_workflow_context.py --step 1   # Main repo, contrib/*
    python verify_workflow_context.py --step 2   # Worktree, feature/*
    python verify_workflow_context.py --step 3   # Worktree, feature/*
    python verify_workflow_context.py --step 4   # Worktree, feature/*
    python verify_workflow_context.py --step 5   # Main repo, contrib/*
    python verify_workflow_context.py --step 6   # Main repo, contrib/*
    python verify_workflow_context.py --step 7   # Main repo, release/*

Exit codes:
    0 - Context validation passed
    1 - Context validation failed
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Safe cross-platform output
try:
    from .safe_output import format_check, format_cross, safe_print
except ImportError:
    from safe_output import format_check, format_cross, safe_print

# Step definitions: (require_worktree, require_main_repo, branch_prefix, step_name)
STEP_REQUIREMENTS = {
    1: (False, True, "contrib/", "/1_specify - Create feature spec"),
    2: (True, False, "feature/", "/2_plan - Generate specifications"),
    3: (True, False, "feature/", "/3_tasks - Validate task list"),
    4: (True, False, "feature/", "/4_implement - Execute tasks"),
    5: (False, True, "contrib/", "/5_integrate - Integrate feature"),
    6: (False, True, "contrib/", "/6_release - Create release"),
    7: (False, True, "contrib/", "/7_backmerge - Sync release"),
}


def run_command(cmd: list[str]) -> str | None:
    """Run command and return output or None on error."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None


def get_repo_root() -> Path | None:
    """Get the git repository root."""
    result = run_command(["git", "rev-parse", "--show-toplevel"])
    return Path(result) if result else None


def get_current_branch() -> str | None:
    """Get current branch name."""
    return run_command(["git", "branch", "--show-current"])


def is_worktree() -> bool:
    """Check if current directory is a git worktree (not main repo)."""
    # Get the common git dir (shared across worktrees)
    git_common_dir = run_command(["git", "rev-parse", "--git-common-dir"])
    # Get the git dir for this worktree
    git_dir = run_command(["git", "rev-parse", "--git-dir"])

    if not git_common_dir or not git_dir:
        return False

    # In main repo: git_dir is ".git" and git_common_dir is ".git"
    # In worktree: git_dir is ".git" but git_common_dir points to main repo's .git
    # Normalize paths for comparison
    git_common_path = Path(git_common_dir).resolve()
    git_dir_path = Path(git_dir).resolve()

    # If they're different, we're in a worktree
    return git_common_path != git_dir_path


def validate_context(
    require_worktree: bool = False,
    require_main_repo: bool = False,
    branch_prefix: str | None = None,
    step: int | None = None,
) -> tuple[bool, str]:
    """Validate the current workflow context.

    Returns:
        (success, message) tuple
    """
    errors = []
    current_branch = get_current_branch()
    in_worktree = is_worktree()
    repo_root = get_repo_root()
    cwd = Path.cwd()

    # Build context info for messages
    context_info = f"Current: branch={current_branch}, "
    context_info += f"location={'worktree' if in_worktree else 'main repo'}"

    # Check worktree requirement
    if require_worktree and not in_worktree:
        errors.append(
            f"Must run from a WORKTREE directory, not main repo.\n"
            f"  Current directory: {cwd}\n"
            f"  Repository root: {repo_root}\n"
            f"  \n"
            f"  To switch to worktree, use:\n"
            f"    cd <worktree-directory>"
        )

    if require_main_repo and in_worktree:
        errors.append(
            f"Must run from MAIN REPO directory, not a worktree.\n"
            f"  Current directory: {cwd}\n"
            f"  Repository root: {repo_root}\n"
            f"  \n"
            f"  To switch to main repo, use:\n"
            f"    cd {repo_root}"
        )

    # Check branch prefix requirement
    if branch_prefix and current_branch:
        if not current_branch.startswith(branch_prefix):
            errors.append(
                f"Must be on a branch starting with '{branch_prefix}'.\n"
                f"  Current branch: {current_branch}\n"
                f"  \n"
                f"  To switch branches, use:\n"
                f"    git checkout <branch-name>"
            )
    elif branch_prefix and not current_branch:
        errors.append("Could not determine current branch (detached HEAD?)")

    if errors:
        error_msg = "\n\n".join(errors)
        return False, error_msg

    return True, context_info


def main():
    parser = argparse.ArgumentParser(
        description="Verify workflow context for slash commands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Step shortcuts:
  --step 1   Main repo, contrib/*   (/1_specify)
  --step 2   Worktree, feature/*    (/2_plan)
  --step 3   Worktree, feature/*    (/3_tasks)
  --step 4   Worktree, feature/*    (/4_implement)
  --step 5   Main repo, contrib/*   (/5_integrate)
  --step 6   Main repo, contrib/*   (/6_release)
  --step 7   Main repo, release/*   (/7_backmerge)
""",
    )

    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7],
        help="Workflow step number (uses predefined requirements)",
    )
    parser.add_argument(
        "--require-worktree",
        action="store_true",
        help="Require execution from a worktree directory",
    )
    parser.add_argument(
        "--require-main-repo",
        action="store_true",
        help="Require execution from main repo (not worktree)",
    )
    parser.add_argument(
        "--require-branch",
        type=str,
        metavar="PREFIX",
        help="Require branch name to start with PREFIX",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output on failure",
    )

    args = parser.parse_args()

    # Resolve step shortcut
    if args.step:
        require_worktree, require_main_repo, branch_prefix, step_name = STEP_REQUIREMENTS[args.step]
    else:
        require_worktree = args.require_worktree
        require_main_repo = args.require_main_repo
        branch_prefix = args.require_branch
        step_name = None

    # Validate conflicting options
    if require_worktree and require_main_repo:
        print("ERROR: Cannot require both worktree and main repo", file=sys.stderr)
        sys.exit(1)

    # Run validation
    success, message = validate_context(
        require_worktree=require_worktree,
        require_main_repo=require_main_repo,
        branch_prefix=branch_prefix,
        step=args.step,
    )

    if success:
        if not args.quiet:
            if step_name:
                safe_print(format_check(f"Context valid for {step_name}"))
            else:
                safe_print(format_check("Context valid"))
            safe_print(f"  {message}")
        sys.exit(0)
    else:
        safe_print("=" * 70)
        safe_print(format_cross("WORKFLOW CONTEXT VALIDATION FAILED"))
        safe_print("=" * 70)
        if step_name:
            safe_print(f"\nStep: {step_name}")
        safe_print(f"\n{message}")
        safe_print("\n" + "=" * 70)
        safe_print("STOP: Fix the context issue above before proceeding.")
        safe_print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
