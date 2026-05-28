#!/usr/bin/env python3
"""
Sync AI Configuration Utility

Consolidates all AI config sync operations into a single utility.
Used by:
- Pre-commit hook (sync on every commit)
- PR workflow (step 3: sync-agents)
- Quality gates (gate 5: AI config sync)

Syncs:
- CLAUDE.md → AGENTS.md
- CLAUDE.md → .github/copilot-instructions.md
- .claude/skills/ → .agents/

Usage:
    # Sync all files (for pre-commit or manual)
    python sync_ai_config.py sync

    # Verify files are in sync (for quality gate)
    python sync_ai_config.py verify

    # Check if sync is needed (for conditional execution)
    python sync_ai_config.py check

Exit codes:
    0 - Success (sync complete or files already in sync)
    1 - Files were modified (for pre-commit to signal re-stage)
    2 - Verification failed (files out of sync)
    3 - Error during sync
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

# Safe cross-platform output
try:
    from .safe_output import format_arrow, format_check, format_cross, format_warning, safe_print
except ImportError:
    from safe_output import format_arrow, format_check, format_cross, format_warning, safe_print


def sync_claude_md_to_agents() -> tuple[bool, bool]:
    """
    Sync CLAUDE.md to AGENTS.md.

    Returns:
        (success: bool, modified: bool)
    """
    source = Path("CLAUDE.md")
    dest = Path("AGENTS.md")

    if not source.exists():
        safe_print("  " + format_warning("CLAUDE.md not found, skipping AGENTS.md sync"))
        return True, False

    # Check if already in sync
    if dest.exists() and filecmp.cmp(source, dest, shallow=False):
        return True, False

    try:
        shutil.copy(source, dest)
        safe_print("  " + format_arrow("CLAUDE.md", "AGENTS.md"))
        return True, True
    except Exception as e:
        safe_print("  " + format_cross(f"Failed to sync AGENTS.md: {e}"))
        return False, False


def sync_claude_md_to_copilot() -> tuple[bool, bool]:
    """
    Sync CLAUDE.md to .github/copilot-instructions.md.

    Returns:
        (success: bool, modified: bool)
    """
    source = Path("CLAUDE.md")
    dest = Path(".github/copilot-instructions.md")

    if not source.exists():
        safe_print("  " + format_warning("CLAUDE.md not found, skipping copilot-instructions.md sync"))
        return True, False

    # Ensure .github directory exists
    dest.parent.mkdir(exist_ok=True)

    # Check if already in sync
    if dest.exists() and filecmp.cmp(source, dest, shallow=False):
        return True, False

    try:
        shutil.copy(source, dest)
        safe_print("  " + format_arrow("CLAUDE.md", ".github/copilot-instructions.md"))
        return True, True
    except Exception as e:
        safe_print("  " + format_cross(f"Failed to sync copilot-instructions.md: {e}"))
        return False, False


def sync_skills_to_agents_dir() -> tuple[bool, bool]:
    """
    Sync .claude/skills/ to .agents/.

    Returns:
        (success: bool, modified: bool)
    """
    source_dir = Path(".claude/skills")
    dest_dir = Path(".agents")

    if not source_dir.exists():
        safe_print("  " + format_warning(".claude/skills/ not found, skipping .agents/ sync"))
        return True, False

    # Ensure .agents directory exists
    dest_dir.mkdir(exist_ok=True)

    modified = False
    try:
        for skill_dir in source_dir.iterdir():
            if skill_dir.is_dir():
                dest = dest_dir / skill_dir.name

                # Check if directory needs sync using dircmp
                if dest.exists():
                    comparison = filecmp.dircmp(skill_dir, dest)
                    if not _dirs_differ(comparison):
                        continue  # Already in sync

                # Remove existing and copy fresh
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(skill_dir, dest)
                modified = True

        if modified:
            safe_print("  " + format_arrow(".claude/skills/", ".agents/"))
        return True, modified
    except Exception as e:
        safe_print("  " + format_cross(f"Failed to sync .agents/: {e}"))
        return False, False


def _dirs_differ(dcmp: filecmp.dircmp) -> bool:
    """
    Recursively check if directories differ.

    Returns:
        True if directories have any differences
    """
    if dcmp.diff_files or dcmp.left_only or dcmp.right_only:
        return True
    for sub_dcmp in dcmp.subdirs.values():
        if _dirs_differ(sub_dcmp):
            return True
    return False


def sync_all() -> tuple[bool, bool]:
    """
    Perform all sync operations.

    Returns:
        (all_success: bool, any_modified: bool)
    """
    safe_print("Syncing AI configuration files...")

    all_success = True
    any_modified = False

    # Sync CLAUDE.md → AGENTS.md
    success, modified = sync_claude_md_to_agents()
    all_success &= success
    any_modified |= modified

    # Sync CLAUDE.md → .github/copilot-instructions.md
    success, modified = sync_claude_md_to_copilot()
    all_success &= success
    any_modified |= modified

    # Sync .claude/skills/ → .agents/
    success, modified = sync_skills_to_agents_dir()
    all_success &= success
    any_modified |= modified

    if all_success and not any_modified:
        safe_print(format_check("All files already in sync"))
    elif all_success and any_modified:
        safe_print(format_check("Sync complete (files modified)"))
    else:
        safe_print(format_cross("Sync completed with errors"))

    return all_success, any_modified


def verify_sync() -> bool:
    """
    Verify all files are in sync without modifying them.

    Returns:
        True if all files are in sync
    """
    safe_print("Verifying AI configuration sync...")
    all_synced = True

    # Verify CLAUDE.md → AGENTS.md
    source = Path("CLAUDE.md")
    dest = Path("AGENTS.md")
    if source.exists():
        if not dest.exists():
            safe_print("  " + format_cross("AGENTS.md missing"))
            all_synced = False
        elif not filecmp.cmp(source, dest, shallow=False):
            safe_print("  " + format_cross("AGENTS.md differs from CLAUDE.md"))
            all_synced = False
        else:
            safe_print("  " + format_check("AGENTS.md in sync"))

    # Verify CLAUDE.md → .github/copilot-instructions.md
    dest = Path(".github/copilot-instructions.md")
    if source.exists():
        if not dest.exists():
            safe_print("  " + format_cross(".github/copilot-instructions.md missing"))
            all_synced = False
        elif not filecmp.cmp(source, dest, shallow=False):
            safe_print("  " + format_cross(".github/copilot-instructions.md differs from CLAUDE.md"))
            all_synced = False
        else:
            safe_print("  " + format_check(".github/copilot-instructions.md in sync"))

    # Verify .claude/skills/ → .agents/
    source_dir = Path(".claude/skills")
    dest_dir = Path(".agents")
    if source_dir.exists():
        if not dest_dir.exists():
            safe_print("  " + format_cross(".agents/ directory missing"))
            all_synced = False
        else:
            skills_synced = True
            for skill_dir in source_dir.iterdir():
                if skill_dir.is_dir():
                    dest = dest_dir / skill_dir.name
                    if not dest.exists():
                        safe_print("  " + format_cross(f".agents/{skill_dir.name}/ missing"))
                        skills_synced = False
                    else:
                        comparison = filecmp.dircmp(skill_dir, dest)
                        if _dirs_differ(comparison):
                            safe_print("  " + format_cross(f".agents/{skill_dir.name}/ differs from .claude/skills/{skill_dir.name}/"))
                            skills_synced = False
            if skills_synced:
                safe_print("  " + format_check(".agents/ in sync with .claude/skills/"))
            else:
                all_synced = False

    if all_synced:
        safe_print(format_check("All AI configuration files in sync"))
    else:
        safe_print(format_cross("AI configuration files out of sync - run 'sync_ai_config.py sync'"))

    return all_synced


def check_needs_sync() -> bool:
    """
    Check if any files need syncing (quick check without modifying).

    Returns:
        True if files need syncing
    """
    # Check CLAUDE.md → AGENTS.md
    source = Path("CLAUDE.md")
    if source.exists():
        dest = Path("AGENTS.md")
        if not dest.exists() or not filecmp.cmp(source, dest, shallow=False):
            return True

        dest = Path(".github/copilot-instructions.md")
        if not dest.exists() or not filecmp.cmp(source, dest, shallow=False):
            return True

    # Check .claude/skills/ → .agents/
    source_dir = Path(".claude/skills")
    dest_dir = Path(".agents")
    if source_dir.exists():
        if not dest_dir.exists():
            return True
        for skill_dir in source_dir.iterdir():
            if skill_dir.is_dir():
                dest = dest_dir / skill_dir.name
                if not dest.exists():
                    return True
                comparison = filecmp.dircmp(skill_dir, dest)
                if _dirs_differ(comparison):
                    return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync AI configuration files for model-agnostic support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "action",
        choices=["sync", "verify", "check"],
        help="Action to perform: sync (copy files), verify (check without modifying), check (quick needs-sync check)",
    )

    args = parser.parse_args()

    if args.action == "sync":
        success, modified = sync_all()
        if not success:
            sys.exit(3)  # Error during sync
        elif modified:
            sys.exit(1)  # Files modified (pre-commit should re-stage)
        else:
            sys.exit(0)  # Already in sync

    elif args.action == "verify":
        if verify_sync():
            sys.exit(0)  # All in sync
        else:
            sys.exit(2)  # Verification failed

    elif args.action == "check":
        if check_needs_sync():
            print("Files need syncing")
            sys.exit(1)
        else:
            print("Files in sync")
            sys.exit(0)


if __name__ == "__main__":
    main()
