#!/usr/bin/env python3
"""Register new workflow in TODO.md master manifest.

This script adds a new workflow to the TODO.md active list when a workflow
is created (e.g., after BMAD planning or worktree creation).

Usage:
    python workflow_registrar.py <todo_file> <workflow_type> <slug> [--title TITLE]

Example:
    python workflow_registrar.py TODO_feature_20251103_auth.md feature auth \\
        --title "User Authentication System"

Constants:
- VALID_WORKFLOW_TYPES: Allowed workflow types
  Rationale: Enforce consistency with workflow system
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
VALID_WORKFLOW_TYPES = ["feature", "release", "hotfix"]
TODO_MD_PATH = Path.cwd() / "TODO.md"


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


def extract_timestamp_from_filename(filename: str) -> str | None:
    """Extract timestamp from TODO filename.

    Args:
        filename: TODO filename like "TODO_feature_20251103T143000Z_auth.md"

    Returns:
        ISO8601 timestamp or None
    """
    match = re.search(r"(\d{8}T\d{6}Z)", filename)
    if match:
        ts = match.group(1)
        # Convert to ISO8601: 20251103T143000Z → 2025-11-03T14:30:00Z
        return f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}T{ts[9:11]}:{ts[11:13]}:{ts[13:15]}Z"
    return None


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


def register_workflow(todo_file: Path, workflow_type: str, slug: str, title: str | None = None) -> None:
    """Register workflow in TODO.md active list.

    Args:
        todo_file: Path to TODO_*.md file
        workflow_type: Type of workflow (feature/release/hotfix)
        slug: Workflow slug
        title: Optional workflow title
    """
    if workflow_type not in VALID_WORKFLOW_TYPES:
        error_exit(f"Invalid workflow type: {workflow_type}. Must be one of: {VALID_WORKFLOW_TYPES}")

    if not todo_file.exists():
        error_exit(f"TODO file not found: {todo_file}")

    info(f"Registering {workflow_type} workflow: {slug}")

    # Load TODO.md
    frontmatter, content = load_todo_md()

    # Extract timestamp from filename
    timestamp = extract_timestamp_from_filename(todo_file.name)
    if not timestamp:
        warning(f"Could not extract timestamp from {todo_file.name}")
        timestamp = datetime.now(UTC).isoformat()

    # Ensure workflows structure exists
    if "workflows" not in frontmatter:
        frontmatter["workflows"] = {}
    if "active" not in frontmatter["workflows"]:
        frontmatter["workflows"]["active"] = []
    if "archived" not in frontmatter["workflows"]:
        frontmatter["workflows"]["archived"] = []

    # Check if already registered
    for workflow in frontmatter["workflows"]["active"]:
        if workflow.get("slug") == slug:
            warning(f"Workflow '{slug}' already registered in active list")
            return

    # Create workflow entry
    workflow_entry = {
        "slug": slug,
        "timestamp": extract_timestamp_from_filename(todo_file.name) or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
        "title": title or f"{workflow_type.title()}: {slug}",
        "status": "in_progress",
        "file": todo_file.name,
    }

    # Add to active list
    frontmatter["workflows"]["active"].append(workflow_entry)

    # Update last_update timestamp
    frontmatter["last_update"] = datetime.now(UTC).isoformat()

    # Save
    save_todo_md(frontmatter, content)

    success(f"Registered workflow in TODO.md: {slug}")
    info(f"  File: {todo_file.name}")
    info(f"  Type: {workflow_type}")
    info(f"  Active workflows: {len(frontmatter['workflows']['active'])}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register workflow in TODO.md master manifest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Register feature workflow
  python workflow_registrar.py TODO_feature_20251103_auth.md feature auth \\
      --title "User Authentication System"

  # Register hotfix workflow
  python workflow_registrar.py TODO_hotfix_20251103_csrf.md hotfix csrf \\
      --title "CSRF Protection Fix"
""",
    )

    parser.add_argument("todo_file", type=Path, help="Path to TODO_*.md file")
    parser.add_argument("workflow_type", choices=VALID_WORKFLOW_TYPES, help="Workflow type")
    parser.add_argument("slug", help="Workflow slug")
    parser.add_argument("--title", help="Workflow title (auto-generated if not provided)")

    args = parser.parse_args()

    try:
        register_workflow(args.todo_file, args.workflow_type, args.slug, args.title)
    except Exception as e:
        error_exit(str(e))


if __name__ == "__main__":
    main()
