#!/usr/bin/env python3
"""Cleanup feature worktree and optionally archive TODO.

This script ensures proper cleanup: (optional) Archive TODO → Delete worktree → Delete branches.

Constants:
- WORKTREE_PREFIX: '../{project}_feature_' or '../feature_'
  Rationale: Feature worktrees created by create_worktree.py use this pattern
- TODO_PATTERN: 'TODO_feature_{timestamp}_{slug}.md'
  Rationale: TODO files created by create_worktree.py follow this naming

Note: The --no-archive flag (default) skips TODO archival since TODO*.md files are
deprecated in favor of GitHub Issues and specs/*/tasks.md.

Usage:
    # Skip TODO archival (default, recommended)
    python cleanup_feature.py <slug> --no-archive

    # With TODO archival (deprecated)
    python cleanup_feature.py <slug> --archive --summary "..." --version "X.Y.Z"

Created: 2025-11-18
Issue: Workflow enforcement - ensure TODO archival before worktree deletion
"""

import argparse
import glob
import subprocess
import sys
from pathlib import Path

# Add workflow-utilities to path for archiver
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts"))


def find_todo_file(slug: str) -> Path:
    """Find TODO file matching slug pattern.

    Args:
        slug: Feature slug (e.g., 'auth-system', 'issue-243-todo-status')

    Returns:
        Path to TODO file

    Raises:
        FileNotFoundError: If TODO file not found
        ValueError: If multiple TODO files match pattern
    """
    # Get repository root
    repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE).strip())

    # Search for TODO file matching pattern
    pattern = str(repo_root / f"TODO_feature_*_{slug}.md")
    matches = glob.glob(pattern)

    if not matches:
        raise FileNotFoundError(f"No TODO file found for slug '{slug}'\nExpected pattern: TODO_feature_*_{slug}.md\nSearched in: {repo_root}")

    if len(matches) > 1:
        raise ValueError(f"Multiple TODO files found for slug '{slug}':\n" + "\n".join(f"  - {m}" for m in matches))

    return Path(matches[0])


def find_worktree(slug: str, project_name: str = None) -> Path:
    """Find worktree directory matching slug pattern.

    Args:
        slug: Feature slug
        project_name: Optional project name (e.g., 'german'). If None, uses generic pattern.

    Returns:
        Path to worktree directory, or None if not found
    """
    # Get repository root
    repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE).strip())

    # Try both project-specific and generic patterns
    patterns = []
    if project_name:
        patterns.append(repo_root.parent / f"{project_name}_feature_{slug}")
    patterns.append(repo_root.parent / f"feature_{slug}")

    for worktree_path in patterns:
        if worktree_path.exists():
            return worktree_path

    return None


def find_branch(slug: str) -> str:
    """Find branch name matching slug pattern.

    Args:
        slug: Feature slug

    Returns:
        Branch name (e.g., 'feature/20251118T115035Z_issue-243-todo-status')

    Raises:
        ValueError: If branch not found or multiple branches match
    """
    # List all local branches matching pattern
    result = subprocess.run(["git", "branch", "--list", f"feature/*_{slug}"], capture_output=True, text=True, check=True)

    branches = [b.strip().lstrip("* ") for b in result.stdout.strip().split("\n") if b.strip()]

    if not branches:
        raise ValueError(f"No branch found for slug '{slug}'\nExpected pattern: feature/*_{slug}")

    if len(branches) > 1:
        raise ValueError(f"Multiple branches found for slug '{slug}':\n" + "\n".join(f"  - {b}" for b in branches))

    return branches[0]


def archive_todo(todo_file: Path, summary: str, version: str):
    """Archive TODO file using workflow_archiver.py.

    Args:
        todo_file: Path to TODO file
        summary: Completion summary
        version: Semantic version

    Raises:
        subprocess.CalledProcessError: If archiver fails
    """
    archiver_script = Path(__file__).parent.parent.parent / "workflow-utilities" / "scripts" / "workflow_archiver.py"

    print(f"📦 Archiving TODO: {todo_file.name}")
    subprocess.run([sys.executable, str(archiver_script), str(todo_file), "--summary", summary, "--version", version], check=True)
    print(f"✓ TODO archived to ARCHIVED/{todo_file.name}")


def delete_worktree(worktree_path: Path):
    """Delete worktree directory.

    Args:
        worktree_path: Path to worktree

    Raises:
        subprocess.CalledProcessError: If git worktree remove fails
    """
    print(f"🗑️  Removing worktree: {worktree_path}")
    subprocess.run(["git", "worktree", "remove", str(worktree_path)], check=True)
    print(f"✓ Worktree removed: {worktree_path}")


def delete_branch(branch_name: str):
    """Delete local and remote branches.

    Args:
        branch_name: Branch name (e.g., 'feature/20251118T115035Z_slug')

    Raises:
        subprocess.CalledProcessError: If git branch deletion fails
    """
    # Delete local branch
    print(f"🗑️  Deleting local branch: {branch_name}")
    subprocess.run(["git", "branch", "-D", branch_name], check=True)
    print(f"✓ Local branch deleted: {branch_name}")

    # Delete remote branch (if exists)
    print(f"🗑️  Deleting remote branch: origin/{branch_name}")
    result = subprocess.run(["git", "push", "origin", "--delete", branch_name], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ Remote branch deleted: origin/{branch_name}")
    else:
        # Remote branch might not exist - not an error
        print(f"ℹ️  Remote branch not found (may have been deleted): origin/{branch_name}")


def cleanup_feature(slug: str, summary: str = None, version: str = None, project_name: str = None, archive_todo_file: bool = False):
    """Cleanup feature: optionally archive TODO, delete worktree, delete branches.

    This is the main entry point that ensures correct ordering of cleanup operations.

    Args:
        slug: Feature slug
        summary: Completion summary for archive (required if archive_todo_file=True)
        version: Semantic version for archive (required if archive_todo_file=True)
        project_name: Optional project name for worktree pattern
        archive_todo_file: If True, archive TODO file before cleanup (default False, deprecated)

    Raises:
        FileNotFoundError: If TODO file not found (when archive_todo_file=True)
        ValueError: If branch not found or multiple matches
        subprocess.CalledProcessError: If any git operation fails
    """
    print(f"\n🚀 Cleaning up feature: {slug}")
    print("=" * 70)

    todo_file = None

    # Step 1: Find TODO file (only required if archiving)
    if archive_todo_file:
        try:
            todo_file = find_todo_file(slug)
            print(f"✓ Found TODO: {todo_file.name}")
        except FileNotFoundError as e:
            print(f"\n❌ ERROR: {e}", file=sys.stderr)
            print("\nℹ️  TODO file must exist before cleanup with --archive.", file=sys.stderr)
            print("   If TODO was already archived, this feature is already cleaned up.", file=sys.stderr)
            print("   Use --no-archive to skip TODO archival.", file=sys.stderr)
            sys.exit(1)
    else:
        print("ℹ️  Skipping TODO archival (deprecated)")

    # Step 2: Find worktree (optional - may not exist)
    worktree_path = find_worktree(slug, project_name)
    if worktree_path:
        print(f"✓ Found worktree: {worktree_path}")
    else:
        print("ℹ️  No worktree found (may have been deleted or work done on contrib directly)")

    # Step 3: Find branch (fail if missing)
    try:
        branch_name = find_branch(slug)
        print(f"✓ Found branch: {branch_name}")
    except ValueError as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 70)
    print("Starting cleanup operations...")
    print("=" * 70 + "\n")

    # Step 4: Archive TODO (only if requested, deprecated)
    if archive_todo_file and todo_file:
        try:
            archive_todo(todo_file, summary, version)
        except subprocess.CalledProcessError as e:
            print("\n❌ ERROR: Failed to archive TODO file", file=sys.stderr)
            print(f"   Command failed: {e.cmd}", file=sys.stderr)
            print(f"   Return code: {e.returncode}", file=sys.stderr)
            print("\n⚠️  Cleanup aborted - TODO not archived", file=sys.stderr)
            print("   Worktree and branches NOT deleted (safe to retry)", file=sys.stderr)
            sys.exit(1)

    # Step 5: Delete worktree (if exists)
    if worktree_path:
        try:
            delete_worktree(worktree_path)
        except subprocess.CalledProcessError as e:
            print("\n❌ ERROR: Failed to delete worktree", file=sys.stderr)
            print(f"   Path: {worktree_path}", file=sys.stderr)
            print(f"   Command failed: {e.cmd}", file=sys.stderr)
            if archive_todo_file:
                print("\n⚠️  TODO archived but worktree NOT deleted", file=sys.stderr)
            else:
                print("\n⚠️  Worktree NOT deleted", file=sys.stderr)
            print("   You can manually delete: git worktree remove", file=sys.stderr)
            sys.exit(1)

    # Step 6: Delete branches (local + remote)
    try:
        delete_branch(branch_name)
    except subprocess.CalledProcessError as e:
        print("\n❌ ERROR: Failed to delete branch", file=sys.stderr)
        print(f"   Branch: {branch_name}", file=sys.stderr)
        print(f"   Command failed: {e.cmd}", file=sys.stderr)
        if archive_todo_file:
            print("\n⚠️  TODO archived, worktree deleted, but branch NOT deleted", file=sys.stderr)
        else:
            print("\n⚠️  Worktree deleted, but branch NOT deleted", file=sys.stderr)
        print("   You can manually delete: git branch -D", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 70)
    print(f"✅ Feature cleanup complete: {slug}")
    print("=" * 70)
    print("\nCleaned up:")
    if archive_todo_file and todo_file:
        print(f"  ✓ TODO archived: ARCHIVED/{todo_file.name}")
    else:
        print("  - TODO archival: skipped (deprecated)")
    if worktree_path:
        print(f"  ✓ Worktree deleted: {worktree_path}")
    print(f"  ✓ Local branch deleted: {branch_name}")
    print(f"  ✓ Remote branch deleted: origin/{branch_name}")
    print()


def main():
    """Parse arguments and execute cleanup."""
    parser = argparse.ArgumentParser(
        description="Cleanup feature: delete worktree and branches, optionally archive TODO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cleanup feature without TODO archival (default, recommended)
  python cleanup_feature.py auth-system --no-archive

  # Cleanup with TODO archival (deprecated)
  python cleanup_feature.py auth-system \\
    --archive \\
    --summary "Implemented user authentication" \\
    --version "1.5.0"

  # Cleanup feature with project-specific worktree pattern
  python cleanup_feature.py auth-system \\
    --no-archive \\
    --project-name german

Notes:
  - Slug must match the slug used in create_worktree.py
  - TODO file pattern: TODO_feature_*_{slug}.md
  - Worktree pattern: ../feature_{slug}/ or ../{project}_feature_{slug}/
  - Branch pattern: feature/*_{slug}
  - TODO archival is deprecated; use GitHub Issues and specs/*/tasks.md instead
""",
    )

    parser.add_argument("slug", help="Feature slug (e.g., auth-system, issue-243-todo-status)")
    parser.add_argument("--archive", action="store_true", default=False, help="Archive TODO file before cleanup (deprecated, requires --summary and --version)")
    parser.add_argument("--summary", default=None, help="Completion summary for archive (required with --archive)")
    parser.add_argument("--version", default=None, help="Semantic version (e.g., 1.5.0, 1.13.0) (required with --archive)")
    parser.add_argument("--project-name", default=None, help="Project name for worktree pattern (e.g., german). If not provided, uses generic pattern.")

    args = parser.parse_args()

    # Determine if we should archive TODO
    # --archive explicitly enables it, otherwise default is False
    archive_todo = args.archive

    # Validate required args for --archive
    if archive_todo:
        if not args.summary:
            parser.error("--summary is required when using --archive")
        if not args.version:
            parser.error("--version is required when using --archive")

    try:
        cleanup_feature(slug=args.slug, summary=args.summary, version=args.version, project_name=args.project_name, archive_todo_file=archive_todo)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
