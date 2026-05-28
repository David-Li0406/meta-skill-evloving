#!/usr/bin/env python3
"""
Clear DSPy cache and compiled artifacts safely.

This script removes DSPy cache files and compiled artifacts.
Use this after modifying DSPy modules to force recompilation.

Usage:
    python clear-cache.py
    python clear-cache.py --cache-dir .var/cache/dspy --verbose

Options:
    --cache-dir: Cache directory (default: .var/cache/dspy)
    --verbose: Show detailed output
"""

import argparse
import shutil
import sys
from pathlib import Path


def clear_cache(cache_dir: Path, verbose: bool):
    """Clear the DSPy cache directory."""
    print(f"Clearing DSPy cache at: {cache_dir}")

    if not cache_dir.exists():
        print(f"Cache directory does not exist: {cache_dir}")
        print("Nothing to clear.")
        return

    # Count files and directories
    total_files = 0
    total_dirs = 0

    for item in cache_dir.rglob("*"):
        if item.is_file():
            total_files += 1
        elif item.is_dir():
            total_dirs += 1

    print(f"Found {total_files} files and {total_dirs} directories")

    # Confirm deletion
    response = input("Are you sure you want to clear the cache? (y/N): ")
    if response.lower() != "y":
        print("Aborted.")
        return

    # Remove cache directory
    try:
        shutil.rmtree(cache_dir)
        print(f"✓ Removed cache directory: {cache_dir}")
    except Exception as e:
        print(f"❌ Error removing cache directory: {e}")
        sys.exit(1)

    # Also clear compiled artifacts
    logs_dir = Path(".var/logs")
    if logs_dir.exists():
        compiled_files = list(logs_dir.glob("compiled_*.pkl"))
        if compiled_files:
            print(f"\nFound {len(compiled_files)} compiled artifact(s):")
            for file in compiled_files:
                print(f"  - {file}")

            response = input("Remove compiled artifacts? (y/N): ")
            if response.lower() == "y":
                for file in compiled_files:
                    try:
                        file.unlink()
                        print(f"✓ Removed: {file}")
                    except Exception as e:
                        print(f"❌ Error removing {file}: {e}")

    print("\n✓ Cache cleared successfully!")
    print("\nNext steps:")
    print("  1. Recompile your DSPy modules")
    print("  2. Verify compilation artifacts are created")
    print("  3. Test your changes")


def main():
    parser = argparse.ArgumentParser(description="Clear DSPy cache")
    parser.add_argument("--cache-dir", default=".var/cache/dspy", help="Cache directory")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    clear_cache(cache_dir, args.verbose)


if __name__ == "__main__":
    main()
