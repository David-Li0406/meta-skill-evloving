#!/usr/bin/env python3
"""
Archive a feature plan document to the archived folder.

Usage:
    python archive_plan.py <feature_name>

Examples:
    python archive_plan.py loop-detection
    python archive_plan.py registry
    python archive_plan.py llm-provider
"""

import os
import re
import sys
from pathlib import Path


def find_plan_file(plan_dir: Path, feature: str) -> Path | None:
    """
    Search for a plan file matching the feature name.

    Patterns checked (case-insensitive):
    - {feature}-plan.*
    - {feature}-implement-plan.*
    - {feature}-implement.*
    - {feature}-design.*
    - {feature}_plan.*
    - {feature}_implement_plan.*
    - {feature}_implement.*
    - {feature}_design.*
    - *{feature}*plan*
    - *{feature}*design*
    - *{feature}*implement*
    """
    if not plan_dir.exists():
        return None

    feature_lower = feature.lower()
    feature_pattern = feature_lower.replace("-", "[-_]?").replace("_", "[-_]?")

    # Priority patterns (most specific first)
    patterns = [
        rf"^{feature_pattern}[-_]plan\.",
        rf"^{feature_pattern}[-_]implement[-_]plan\.",
        rf"^{feature_pattern}[-_]implement\.",
        rf"^{feature_pattern}[-_]design\.",
        rf"^{feature_pattern}[-_]implementation\.",
        rf".*{feature_pattern}.*plan.*",
        rf".*{feature_pattern}.*design.*",
        rf".*{feature_pattern}.*implement.*",
    ]

    # Get all files in plan_dir (not in subdirs)
    files = [f for f in plan_dir.iterdir() if f.is_file()]

    for pattern in patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        for file in files:
            if regex.match(file.name):
                return file

    return None


def list_plan_files(plan_dir: Path) -> list[str]:
    """List all files in the plan directory."""
    if not plan_dir.exists():
        return []

    files = []
    for f in plan_dir.iterdir():
        if f.is_file():
            files.append(f.name)
        elif f.is_dir():
            files.append(f"{f.name}/")

    return sorted(files)


def archive_plan(feature: str, base_dir: Path | None = None) -> bool:
    """
    Find and archive a plan file for the given feature.

    Returns True if successful, False otherwise.
    """
    if base_dir is None:
        # Default to ./doc/plan relative to script location or cwd
        base_dir = Path.cwd() / "doc" / "plan"

    plan_dir = base_dir
    archived_dir = plan_dir / "archived"

    # Find the plan file
    plan_file = find_plan_file(plan_dir, feature)

    if plan_file is None:
        print(f"Error: No plan file found for feature '{feature}'")
        print()
        print("Available files in doc/plan:")
        files = list_plan_files(plan_dir)
        if files:
            for f in files:
                print(f"  - {f}")
        else:
            print("  (no files found)")
        print()
        print("Tip: Try a different feature name or check the file naming.")
        return False

    # Create archived directory if needed
    archived_dir.mkdir(parents=True, exist_ok=True)

    # Move the file
    dest = archived_dir / plan_file.name

    if dest.exists():
        print(f"Warning: {dest} already exists, will be overwritten")

    plan_file.rename(dest)
    print(f"Archived: {plan_file.name} -> archived/{plan_file.name}")
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("Error: Feature name required")
        sys.exit(1)

    feature = sys.argv[1]

    # Support optional base directory as second argument
    base_dir = None
    if len(sys.argv) >= 3:
        base_dir = Path(sys.argv[2])

    success = archive_plan(feature, base_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
