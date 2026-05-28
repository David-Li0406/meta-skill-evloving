#!/usr/bin/env python3
"""Deprecate files by archiving them with timestamp."""

import sys
import zipfile
from datetime import datetime
from pathlib import Path


def deprecate_files(todo_file, description, *files):
    """
    Archive deprecated files with timestamp.

    Args:
        todo_file: Path to TODO file (for timestamp extraction)
        description: Short description (e.g., 'old-auth-flow')
        *files: File paths to deprecate

    Creates:
        ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip
    """
    # Extract timestamp from TODO file name
    todo_path = Path(todo_file)
    todo_name = todo_path.stem  # TODO_feature_20251022T143022Z_slug
    parts = todo_name.split("_")
    timestamp = parts[2] if len(parts) > 2 else datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Create ARCHIVED directory if needed
    archived_dir = Path("ARCHIVED")
    archived_dir.mkdir(exist_ok=True)

    # Ensure ARCHIVED has standard files (if not already an ARCHIVED dir)
    archived_claude = archived_dir / "CLAUDE.md"
    if not archived_claude.exists():
        archived_claude.write_text(
            """# Claude Code Context: Archived Content

## Purpose

Archive of deprecated files.

## Contents

Zip files containing deprecated code and resources.

## Restoration

Use archive_manager.py to list and extract archived files.
"""
        )

    archived_readme = archived_dir / "README.md"
    if not archived_readme.exists():
        archived_readme.write_text(
            """# Archived Files

This directory contains archived (deprecated) files that are no longer in active use.

Files are stored in timestamped zip archives for potential recovery.
"""
        )

    # Create zip archive
    zip_name = f"{timestamp}_{description}.zip"
    zip_path = archived_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            file_path = Path(file)
            if file_path.exists():
                zipf.write(file_path, file_path.name)
                print(f"  Archived: {file}")
                file_path.unlink()  # Delete original
            else:
                print(f"  Warning: {file} not found", file=sys.stderr)

    print(f"✓ Created archive: {zip_path}")
    return str(zip_path)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: deprecate_files.py <todo_file> <description> <file1> [file2 ...]")
        print("Example: deprecate_files.py TODO_feature_xxx.md old-impl src/old.py")
        sys.exit(1)

    deprecate_files(sys.argv[1], sys.argv[2], *sys.argv[3:])
