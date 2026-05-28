#!/usr/bin/env python3
"""Archive completed workflow and update TODO.md manifest.

This script moves a TODO_*.md file to ARCHIVED/ and updates the TODO.md
master manifest (active → archived list). Use at Phase 4.3 after PR merge.

Usage:
    python workflow_archiver.py <todo_file> [--summary SUMMARY] [--version VERSION]

Example:
    python workflow_archiver.py TODO_feature_20251103_auth.md \\
        --summary "Implemented OAuth2 authentication" \\
        --version "1.5.0"

Constants:
- ARCHIVED_DIR: Path to ARCHIVED directory
  Rationale: Standardized location for archived files
"""

import argparse
import re
import shutil
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


def extract_slug_from_filename(filename: str) -> str | None:
    """Extract slug from TODO filename.

    Args:
        filename: TODO filename like "TODO_feature_20251103T143000Z_auth.md"

    Returns:
        Slug (e.g., "auth") or None
    """
    match = re.search(r"TODO_\w+_\d{8}T\d{6}Z_(.+)\.md", filename)
    return match.group(1) if match else None


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


def load_workflow_file(todo_file: Path) -> dict[str, Any]:
    """Load workflow TODO file and extract metadata.

    Args:
        todo_file: Path to TODO_*.md file

    Returns:
        Dictionary with workflow metadata
    """
    content = todo_file.read_text(encoding="utf-8")

    if not content.startswith("---"):
        error_exit(f"{todo_file.name} missing YAML frontmatter")

    parts = content.split("---", 2)
    if len(parts) < 3:
        error_exit(f"Invalid format in {todo_file.name}")

    try:
        frontmatter = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        error_exit(f"Invalid YAML in {todo_file.name}: {e}")

    return frontmatter


def archive_workflow(todo_file: Path, summary: str | None = None, version: str | None = None) -> None:
    """Archive workflow: move file and update TODO.md.

    Args:
        todo_file: Path to TODO_*.md file to archive
        summary: Optional summary of what was completed
        version: Optional semantic version for this workflow
    """
    if not todo_file.exists():
        error_exit(f"TODO file not found: {todo_file}")

    slug = extract_slug_from_filename(todo_file.name)
    if not slug:
        error_exit(f"Could not extract slug from filename: {todo_file.name}")

    info(f"Archiving workflow: {slug}")

    # Load workflow file to get metadata
    workflow_data = load_workflow_file(todo_file)

    # Ensure ARCHIVED directory exists
    if not ARCHIVED_DIR.exists():
        error_exit(f"ARCHIVED directory not found: {ARCHIVED_DIR}")

    # Move file to ARCHIVED/
    archived_path = ARCHIVED_DIR / todo_file.name
    if archived_path.exists():
        warning(f"File already exists in ARCHIVED/: {archived_path.name}")
        response = input("Overwrite? (y/N): ")
        if response.lower() != "y":
            error_exit("Archival cancelled")

    shutil.move(str(todo_file), str(archived_path))
    success(f"Moved {todo_file.name} → ARCHIVED/{todo_file.name}")

    # Load TODO.md
    frontmatter, content = load_todo_md()

    # Ensure workflows structure exists
    if "workflows" not in frontmatter:
        frontmatter["workflows"] = {"active": [], "archived": []}
    if "active" not in frontmatter["workflows"]:
        frontmatter["workflows"]["active"] = []
    if "archived" not in frontmatter["workflows"]:
        frontmatter["workflows"]["archived"] = []

    # Find workflow in active list
    workflow_entry = None
    for i, workflow in enumerate(frontmatter["workflows"]["active"]):
        if workflow.get("slug") == slug:
            workflow_entry = frontmatter["workflows"]["active"].pop(i)
            break

    if not workflow_entry:
        warning(f"Workflow '{slug}' not found in active list (creating new entry)")
        workflow_entry = {"slug": slug, "timestamp": workflow_data.get("timestamp", "unknown"), "title": workflow_data.get("slug", slug), "file": todo_file.name}

    # Update workflow entry for archival
    workflow_entry["status"] = "completed"
    workflow_entry["completed_at"] = datetime.now(UTC).isoformat()
    workflow_entry["file"] = f"ARCHIVED/{todo_file.name}"

    if summary:
        workflow_entry["summary"] = summary

    if version:
        workflow_entry["semantic_version"] = version
    elif "quality_gates" in workflow_data and "semantic_version" in workflow_data["quality_gates"]:
        workflow_entry["semantic_version"] = workflow_data["quality_gates"]["semantic_version"]

    # Add to archived list
    frontmatter["workflows"]["archived"].append(workflow_entry)

    # Update statistics
    if "context_stats" not in frontmatter:
        frontmatter["context_stats"] = {}

    total_completed = frontmatter["context_stats"].get("total_workflows_completed", 0)
    frontmatter["context_stats"]["total_workflows_completed"] = total_completed + 1
    frontmatter["context_stats"]["last_checkpoint"] = datetime.now(UTC).isoformat()

    # Update last_update timestamp
    frontmatter["last_update"] = datetime.now(UTC).isoformat()

    # Save
    save_todo_md(frontmatter, content)

    success(f"Updated TODO.md: moved '{slug}' to archived list")
    info(f"  Active workflows: {len(frontmatter['workflows']['active'])}")
    info(f"  Archived workflows: {len(frontmatter['workflows']['archived'])}")
    info(f"  Total completed: {frontmatter['context_stats']['total_workflows_completed']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Archive workflow and update TODO.md manifest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Archive feature workflow
  python workflow_archiver.py TODO_feature_20251103_auth.md \\
      --summary "Implemented OAuth2 authentication with Google and GitHub" \\
      --version "1.5.0"

  # Archive with minimal info (extracts from TODO file)
  python workflow_archiver.py TODO_feature_20251103_auth.md

Usage at Phase 4.3:
  After PR merged to contrib branch, archive the workflow before
  creating the next PR to develop.
""",
    )

    parser.add_argument("todo_file", type=Path, help="Path to TODO_*.md file to archive")
    parser.add_argument("--summary", help="Summary of what was completed")
    parser.add_argument("--version", help="Semantic version for this workflow (e.g., 1.5.0)")

    args = parser.parse_args()

    try:
        archive_workflow(args.todo_file, args.summary, args.version)
    except Exception as e:
        error_exit(str(e))


if __name__ == "__main__":
    main()
