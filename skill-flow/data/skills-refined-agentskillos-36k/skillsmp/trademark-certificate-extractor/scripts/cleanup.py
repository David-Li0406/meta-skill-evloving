#!/usr/bin/env python3
"""
Cleanup script for trademark certificate extractor

Removes intermediate files (*_extracted.txt, *_logo.png, *.json) 
created during the extraction process.
"""

import sys
import os
from pathlib import Path

def cleanup(folder_path: Path):
    """
    Delete intermediate files in the specified folder
    """
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Folder not found: {folder_path}", file=sys.stderr)
        return

    patterns = ["*_extracted.txt", "*_logo.png", "batch_extraction_results_*.json", "trademark_data.json"]
    deleted_count = 0

    print(f"Cleaning up folder: {folder_path}")

    for pattern in patterns:
        for file_path in folder_path.glob(pattern):
            try:
                file_path.unlink()
                print(f"  Deleted: {file_path.name}")
                deleted_count += 1
            except Exception as e:
                print(f"  Error deleting {file_path.name}: {e}", file=sys.stderr)

    print(f"\nCleanup completed. Total files removed: {deleted_count}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python cleanup.py <folder_path>")
        sys.exit(1)

    folder_path = Path(sys.argv[1])
    cleanup(folder_path)

if __name__ == "__main__":
    main()
