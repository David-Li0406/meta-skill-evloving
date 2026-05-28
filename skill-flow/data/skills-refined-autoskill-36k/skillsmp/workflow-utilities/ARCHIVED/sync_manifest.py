#!/usr/bin/env python3
"""Synchronize TODO.md manifest with filesystem state.

This script rebuilds TODO.md by scanning for TODO_*.md files in the
current directory (active) and ARCHIVED/ directory (archived). Useful
for recovery if TODO.md gets out of sync with actual files.

Usage:
    python sync_manifest.py [--dry-run]

Example:
    # Preview changes without modifying TODO.md
    python sync_manifest.py --dry-run

    # Sync TODO.md with filesystem
    python sync_manifest.py

Constants:
- TODO_PATTERN: Regex for TODO file names
  Rationale: Extract metadata from standardized file naming
"""

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Error: PyYAML required. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Constants
TODO_MD_PATH = Path.cwd() / "TODO.md"
ARCHIVED_DIR = Path.cwd() / "ARCHIVED"
TODO_PATTERN = re.compile(r"TODO_(\w+)_(\d{8}T\d{6}Z)_(.+)\.md")


# ANSI colors
class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    END = "\033[0m"


def error_exit(msg: str) -> None:
    print(f"{Colors.RED}✗ Error:{Colors.END} {msg}", file=sys.stderr)
    sys.exit(1)


def success(msg: str) -> None:
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")


def info(msg: str) -> None:
    print(f"{Colors.BLUE}ℹ{Colors.END} {msg}")


def warning(msg: str) -> None:
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")


def parse_todo_filename(filename: str) -> dict[str, str] | None:
    """Parse TODO filename to extract metadata.

    Args:
        filename: TODO filename like "TODO_feature_20251103T143000Z_auth.md"

    Returns:
        Dictionary with workflow_type, timestamp, slug or None
    """
    match = TODO_PATTERN.match(filename)
    if not match:
        return None

    workflow_type, timestamp, slug = match.groups()

    # Convert timestamp to ISO8601
    iso_timestamp = f"{timestamp[0:4]}-{timestamp[4:6]}-{timestamp[6:8]}T{timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}Z"

    return {"workflow_type": workflow_type, "timestamp": timestamp, "iso_timestamp": iso_timestamp, "slug": slug}


def load_workflow_metadata(todo_file: Path) -> dict[str, Any] | None:
    """Load workflow file and extract metadata from frontmatter.

    Args:
        todo_file: Path to TODO_*.md file

    Returns:
        Dictionary with metadata or None if invalid
    """
    try:
        content = todo_file.read_text(encoding="utf-8")

        if not content.startswith("---"):
            warning(f"Skipping {todo_file.name}: missing YAML frontmatter")
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            warning(f"Skipping {todo_file.name}: invalid format")
            return None

        frontmatter = yaml.safe_load(parts[1])
        return frontmatter

    except Exception as e:
        warning(f"Error reading {todo_file.name}: {e}")
        return None


def scan_filesystem() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Scan filesystem for TODO files.

    Returns:
        Tuple of (active_workflows, archived_workflows)
    """
    active_workflows = []
    archived_workflows = []

    # Scan current directory for active workflows
    for todo_file in Path.cwd().glob("TODO_*.md"):
        if todo_file.name == "TODO.md":
            continue  # Skip master manifest

        parsed = parse_todo_filename(todo_file.name)
        if not parsed:
            warning(f"Skipping {todo_file.name}: unrecognized format")
            continue

        metadata = load_workflow_metadata(todo_file)

        workflow_entry = {
            "slug": parsed["slug"],
            "timestamp": parsed["timestamp"],
            "title": metadata.get("slug", parsed["slug"]) if metadata else parsed["slug"],
            "status": "in_progress",
            "file": todo_file.name,
        }

        active_workflows.append(workflow_entry)

    # Scan ARCHIVED/ for archived workflows
    if ARCHIVED_DIR.exists():
        for todo_file in ARCHIVED_DIR.glob("TODO_*.md"):
            parsed = parse_todo_filename(todo_file.name)
            if not parsed:
                warning(f"Skipping {todo_file.name}: unrecognized format")
                continue

            metadata = load_workflow_metadata(todo_file)

            workflow_entry = {
                "slug": parsed["slug"],
                "timestamp": parsed["timestamp"],
                "title": metadata.get("slug", parsed["slug"]) if metadata else parsed["slug"],
                "status": "completed",
                "file": f"ARCHIVED/{todo_file.name}",
            }

            # Try to get completion metadata
            if metadata:
                if "completed_at" in metadata:
                    workflow_entry["completed_at"] = metadata["completed_at"]
                if "quality_gates" in metadata and "semantic_version" in metadata["quality_gates"]:
                    workflow_entry["semantic_version"] = metadata["quality_gates"]["semantic_version"]

            archived_workflows.append(workflow_entry)

    return active_workflows, archived_workflows


def load_todo_md() -> tuple[dict[str, Any], str]:
    """Load TODO.md and parse YAML frontmatter.

    Returns:
        Tuple of (frontmatter dict, full content)
    """
    if not TODO_MD_PATH.exists():
        error_exit(f"TODO.md not found: {TODO_MD_PATH}")

    content = TODO_MD_PATH.read_text(encoding="utf-8")

    if not content.startswith("---"):
        error_exit("TODO.md missing YAML frontmatter")

    parts = content.split("---", 2)
    if len(parts) < 3:
        error_exit("Invalid TODO.md format")

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        error_exit(f"Invalid YAML in TODO.md: {e}")

    return frontmatter, content


def save_todo_md(frontmatter: dict[str, Any], content: str) -> None:
    """Save updated TODO.md with new frontmatter.

    Args:
        frontmatter: Updated frontmatter dict
        content: Original full content
    """
    parts = content.split("---", 2)
    new_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{new_yaml}---{parts[2]}"

    TODO_MD_PATH.write_text(new_content, encoding="utf-8")


def sync_manifest(dry_run: bool = False) -> None:
    """Synchronize TODO.md with filesystem state.

    Args:
        dry_run: If True, preview changes without saving
    """
    info("Scanning filesystem for TODO files...")

    # Scan filesystem
    active_workflows, archived_workflows = scan_filesystem()

    info(f"Found {len(active_workflows)} active workflow(s)")
    info(f"Found {len(archived_workflows)} archived workflow(s)")

    # Load current TODO.md
    frontmatter, content = load_todo_md()

    # Update workflows
    if "workflows" not in frontmatter:
        frontmatter["workflows"] = {}

    old_active_count = len(frontmatter.get("workflows", {}).get("active", []))
    old_archived_count = len(frontmatter.get("workflows", {}).get("archived", []))

    frontmatter["workflows"]["active"] = active_workflows
    frontmatter["workflows"]["archived"] = archived_workflows

    # Update statistics
    if "context_stats" not in frontmatter:
        frontmatter["context_stats"] = {}

    frontmatter["context_stats"]["total_workflows_completed"] = len(archived_workflows)
    frontmatter["last_update"] = datetime.now(UTC).isoformat()

    # Display changes
    print(f"\n{Colors.BLUE}Changes to be made:{Colors.END}")
    print(f"  Active workflows: {old_active_count} → {len(active_workflows)}")
    print(f"  Archived workflows: {old_archived_count} → {len(archived_workflows)}")

    if dry_run:
        warning("Dry run mode: not saving changes")
        print(f"\n{Colors.BLUE}Preview of new TODO.md:{Colors.END}")
        new_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        print(new_yaml)
        return

    # Save
    save_todo_md(frontmatter, content)
    success("TODO.md synchronized with filesystem")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Synchronize TODO.md manifest with filesystem state",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview changes without modifying TODO.md
  python sync_manifest.py --dry-run

  # Sync TODO.md with filesystem
  python sync_manifest.py

Usage:
  Run this script if TODO.md becomes out of sync with actual TODO_*.md files.
  It rebuilds the active/archived lists based on files found in the current
  directory and ARCHIVED/ directory.

Warning:
  This script replaces the active/archived lists in TODO.md with what it
  finds on the filesystem. Manual edits to TODO.md metadata may be lost.
""",
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying TODO.md")

    args = parser.parse_args()

    try:
        sync_manifest(args.dry_run)
    except Exception as e:
        error_exit(str(e))


if __name__ == "__main__":
    main()
