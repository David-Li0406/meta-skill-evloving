#!/usr/bin/env python3
"""Manage archived files: list, extract, verify, archive workflows."""

import sys
import zipfile
from datetime import datetime
from pathlib import Path


def list_archives(archived_dir="ARCHIVED"):
    """List all archives with timestamps."""

    archived_path = Path(archived_dir)
    if not archived_path.exists():
        print(f"No {archived_dir} directory found")
        return []

    archives = sorted(archived_path.glob("*.zip"))

    if not archives:
        print(f"No archives found in {archived_dir}/")
        return []

    print(f"Archives in {archived_dir}/:")
    print("-" * 60)

    for archive in archives:
        # Parse timestamp from filename: YYYYMMDDTHHMMSSZ_description.zip
        name = archive.stem
        parts = name.split("_", 1)

        if len(parts) == 2:
            timestamp_str, description = parts
            try:
                # Parse timestamp
                timestamp = datetime.strptime(timestamp_str, "%Y%m%dT%H%M%SZ")
                print(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {description}")
                print(f"  File: {archive.name}")

                # List contents
                with zipfile.ZipFile(archive, "r") as zipf:
                    files = zipf.namelist()
                    print(f"  Contains: {', '.join(files)}")

            except ValueError:
                print(f"  {archive.name} (invalid timestamp format)")
        else:
            print(f"  {archive.name}")

        print()

    return archives


def extract_archive(archive_path, output_dir="."):
    """Extract archive to specified directory."""

    archive = Path(archive_path)
    if not archive.exists():
        print(f"Error: Archive not found: {archive_path}", file=sys.stderr)
        sys.exit(1)

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    print(f"Extracting {archive.name} to {output}/")

    with zipfile.ZipFile(archive, "r") as zipf:
        zipf.extractall(output)
        print("✓ Extracted files:")
        for name in zipf.namelist():
            print(f"  - {name}")

    print("\n✓ Extraction complete")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archive_manager.py <list|extract> [args]")
        print()
        print("Commands:")
        print("  list [directory]           - List archives in directory (default: ARCHIVED)")
        print("  extract <archive> [output] - Extract archive to output directory")
        print()
        print("Examples:")
        print("  archive_manager.py list")
        print("  archive_manager.py list ARCHIVED")
        print("  archive_manager.py extract ARCHIVED/20251022T143022Z_old-impl.zip restored/")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        archived_dir = sys.argv[2] if len(sys.argv) > 2 else "ARCHIVED"
        list_archives(archived_dir)

    elif command == "extract":
        if len(sys.argv) < 3:
            print("Usage: archive_manager.py extract <archive_path> [output_dir]")
            sys.exit(1)

        archive_path = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "."
        extract_archive(archive_path, output_dir)

    else:
        print(f"Unknown command: {command}")
        print("Use 'list' or 'extract'")
        sys.exit(1)
