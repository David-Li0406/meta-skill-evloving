#!/usr/bin/env python3
"""Archive completed specifications.

Moves completed spec directories to docs/archived/specs/ with timestamp.
Updates specs/STATUS.md to reflect the archival.

Usage:
    python archive_spec.py <spec-id>

Example:
    python archive_spec.py 001-users-stharrold-documents

Constants:
    ARCHIVE_DIR: docs/archived/specs/
    Rationale: Keeps archived specs with other archived documents
"""

import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path


def get_repo_root() -> Path:
    """Get repository root directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def archive_spec(spec_id: str, dry_run: bool = False) -> bool:
    """Archive a completed specification.

    Args:
        spec_id: Spec directory name (e.g., "001-users-stharrold-documents")
        dry_run: If True, only print what would be done

    Returns:
        True if archival succeeded, False otherwise
    """
    repo_root = get_repo_root()
    spec_dir = repo_root / "specs" / spec_id

    if not spec_dir.exists():
        print(f"\u2717 Spec not found: {spec_id}", file=sys.stderr)
        return False

    # Create archive directory
    archive_base = repo_root / "docs" / "archived" / "specs"
    archive_base.mkdir(parents=True, exist_ok=True)

    # Generate timestamped archive name
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    archive_name = f"{timestamp}_{spec_id}"
    archive_path = archive_base / archive_name

    if archive_path.exists():
        print(f"\u2717 Archive already exists: {archive_path}", file=sys.stderr)
        return False

    if dry_run:
        print(f"\u2192 Would move: {spec_dir}")
        print(f"\u2192 To: {archive_path}")
        return True

    # Move spec to archive
    try:
        shutil.move(str(spec_dir), str(archive_path))
        print(f"\u2713 Archived {spec_id} to {archive_path.relative_to(repo_root)}")

        # Update STATUS.md if it exists
        status_file = repo_root / "specs" / "STATUS.md"
        if status_file.exists():
            content = status_file.read_text()
            # Note: More sophisticated STATUS.md update would require parsing
            if spec_id in content:
                print(f"\u2192 Review specs/STATUS.md to update {spec_id} status")

        return True

    except Exception as e:
        print(f"\u2717 Failed to archive: {e}", file=sys.stderr)
        return False


def list_archivable_specs() -> list[str]:
    """List specs that could be archived."""
    repo_root = get_repo_root()
    specs_dir = repo_root / "specs"

    if not specs_dir.exists():
        return []

    return [d.name for d in specs_dir.iterdir() if d.is_dir() and d.name[0].isdigit()]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archive_spec.py <spec-id> [--dry-run]")
        print("\nAvailable specs:")
        for spec in list_archivable_specs():
            print(f"  - {spec}")
        sys.exit(1)

    spec_id = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    success = archive_spec(spec_id, dry_run=dry_run)
    sys.exit(0 if success else 1)
