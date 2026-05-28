#!/usr/bin/env python3
"""
Rename a skill across the entire marketplace.

Usage:
    python rename-skill.py <old-name> <new-name> [--dry-run]

Examples:
    python rename-skill.py skill-creator-pro skill-creator
    python rename-skill.py julien-dev-tools-skill-creator-pro julien-dev-tools-skill-creator
"""

import os
import re
import sys
import shutil
from pathlib import Path

def find_marketplace_root():
    """Find the marketplace root by looking for .claude-plugin/"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".claude-plugin").exists():
            return current
        current = current.parent
    # Fallback to cwd
    return Path.cwd()

def rename_skill(old_name: str, new_name: str, dry_run: bool = False):
    root = find_marketplace_root()
    skills_dir = root / "skills"

    # Find the actual folder (could be with prefix)
    old_folder = None
    for folder in skills_dir.iterdir():
        if folder.is_dir() and (folder.name == old_name or folder.name.endswith(f"-{old_name}")):
            old_folder = folder
            break

    if not old_folder:
        print(f"Error: Could not find skill folder matching '{old_name}'")
        sys.exit(1)

    # Determine new folder name
    old_folder_name = old_folder.name

    # Check if new_name is already a full name (contains common prefixes)
    full_name_prefixes = ['julien-', 'anthropic-']
    new_is_full_name = any(new_name.startswith(prefix) for prefix in full_name_prefixes)

    if new_is_full_name:
        # User provided complete new name, use it directly
        new_folder_name = new_name
    elif "-" in old_folder_name and old_name in old_folder_name:
        # Has prefix like julien-dev-tools-skill-creator-pro, preserve it
        new_folder_name = old_folder_name.replace(old_name, new_name)
    else:
        new_folder_name = new_name

    new_folder = skills_dir / new_folder_name

    print(f"Marketplace root: {root}")
    print(f"Old folder: {old_folder_name}")
    print(f"New folder: {new_folder_name}")
    print()

    # Patterns to replace (both short and full names)
    replacements = [
        (old_folder_name, new_folder_name),  # Full name with prefix
        (old_name, new_name),  # Short name
    ]
    # Remove duplicates
    replacements = list(dict.fromkeys(replacements))

    # Files to update
    extensions = {'.md', '.json', '.py', '.sh', '.yaml', '.yml'}
    dirs_to_scan = [
        root / "skills",
        root / "configs",
        root / ".claude-plugin",
        root / "scripts",
    ]

    files_modified = []

    # Scan and replace in files
    for scan_dir in dirs_to_scan:
        if not scan_dir.exists():
            continue
        for file_path in scan_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix not in extensions:
                continue
            # Skip the old folder we're about to rename
            if old_folder in file_path.parents or file_path == old_folder:
                continue

            try:
                content = file_path.read_text(encoding='utf-8')
                original = content

                for old_pattern, new_pattern in replacements:
                    content = content.replace(old_pattern, new_pattern)

                if content != original:
                    files_modified.append(file_path)
                    if not dry_run:
                        file_path.write_text(content, encoding='utf-8')
                    print(f"  Modified: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"  Warning: Could not process {file_path}: {e}")

    # Also update files inside the skill folder itself
    if old_folder.exists():
        for file_path in old_folder.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix not in extensions:
                continue
            try:
                content = file_path.read_text(encoding='utf-8')
                original = content

                for old_pattern, new_pattern in replacements:
                    content = content.replace(old_pattern, new_pattern)

                if content != original:
                    files_modified.append(file_path)
                    if not dry_run:
                        file_path.write_text(content, encoding='utf-8')
                    print(f"  Modified: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"  Warning: Could not process {file_path}: {e}")

    # Rename folder
    if old_folder.exists() and old_folder != new_folder:
        print(f"\nRenaming folder: {old_folder_name} -> {new_folder_name}")
        if not dry_run:
            shutil.move(str(old_folder), str(new_folder))

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Files modified: {len(files_modified)}")
    print(f"  Folder renamed: {old_folder_name} -> {new_folder_name}")

    if not dry_run:
        print(f"\nDone! Run 'git status' to review changes.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    old_name = sys.argv[1]
    new_name = sys.argv[2]
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("[DRY RUN MODE - No changes will be made]\n")

    rename_skill(old_name, new_name, dry_run)
