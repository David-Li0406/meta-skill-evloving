#!/usr/bin/env python3
"""
Filesystem-based task storage utilities.

Tasks are stored as markdown files with YAML frontmatter.
Directory structure represents hierarchy:
- Leaf tasks: NN-slug.md
- Parent tasks: NN-slug/00-index.md + children

No external dependencies - uses simple custom frontmatter parser.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

# Constants
TASKS_DIR = ".claude/tasks"
INDEX_FILE = "00-index.md"
VALID_STATUSES = ("pending", "in_progress", "blocked", "complete", "wont_do")


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class Note:
    """A timestamped note attached to a task."""

    text: str
    created: str = ""

    def __post_init__(self):
        if not self.created:
            self.created = now_iso()


@dataclass
class Task:
    """A task with metadata and optional children."""

    id: str  # Path-based: "01-auth/02-session"
    title: str
    status: str = "pending"
    description: str = ""
    deps: list[str] = field(default_factory=list)
    approach: str = ""
    criteria: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    created: str = ""
    updated: str = ""
    started: str = ""
    completed: str = ""
    blocked_reason: str = ""
    children: list[str] = field(default_factory=list)  # Populated when walking

    def __post_init__(self):
        if not self.created:
            self.created = now_iso()
        if not self.updated:
            self.updated = now_iso()


# =============================================================================
# Time Utilities
# =============================================================================


def now_iso() -> str:
    """Return current time as ISO8601 string."""
    return datetime.now(timezone.utc).isoformat()


# =============================================================================
# Simple Frontmatter Parser (no PyYAML dependency)
# =============================================================================


def parse_frontmatter(text: str) -> dict:
    """
    Parse simple YAML-like frontmatter.

    Supports:
    - key: value (strings)
    - key: (followed by indented list items starting with -)
    """
    result = {}
    lines = text.strip().split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Match key: value or key:
        match = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if not match:
            i += 1
            continue

        key = match.group(1)
        value = match.group(2).strip()

        if value:
            # Single-line value - strip quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            result[key] = value
        else:
            # Check for list on following lines
            items = []
            i += 1
            while i < len(lines):
                next_line = lines[i]
                list_match = re.match(r'^  - (.+)$', next_line)
                if list_match:
                    items.append(list_match.group(1).strip())
                    i += 1
                elif next_line.strip() == "" or re.match(r'^[a-z_]+:', next_line):
                    break
                else:
                    i += 1
            result[key] = items
            continue

        i += 1

    return result


def render_frontmatter(data: dict) -> str:
    """
    Render dict to simple YAML-like frontmatter.
    """
    lines = []

    for key, value in data.items():
        if isinstance(value, list):
            if value:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            # Skip empty lists
        elif value:  # Skip empty strings
            # Quote if contains special chars
            if ":" in str(value) or "\n" in str(value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")

    return "\n".join(lines)


# =============================================================================
# Directory Utilities
# =============================================================================


def find_tasks_root() -> Path | None:
    """Walk up directories to find .claude/tasks/."""
    current = Path.cwd()
    while current != current.parent:
        candidate = current / TASKS_DIR
        if candidate.is_dir():
            return candidate
        current = current.parent
    # Check root
    candidate = current / TASKS_DIR
    if candidate.is_dir():
        return candidate
    return None


def require_tasks_root() -> Path:
    """Find tasks root or exit with error."""
    root = find_tasks_root()
    if not root:
        raise TaskError(f"No {TASKS_DIR} found. Run 'task.py init' first.")
    return root


def slugify(title: str) -> str:
    """Convert title to filesystem-safe slug."""
    # Lowercase
    slug = title.lower()
    # Replace spaces and underscores with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")
    # Limit length
    return slug[:50] if slug else "task"


def next_prefix(directory: Path) -> str:
    """Return next NN- prefix for a directory."""
    if not directory.exists():
        return "01"

    existing = []
    for item in directory.iterdir():
        name = item.name
        if name == INDEX_FILE:
            continue
        match = re.match(r"^(\d+)-", name)
        if match:
            existing.append(int(match.group(1)))

    if not existing:
        return "01"
    return f"{max(existing) + 1:02d}"


def get_task_path(task_id: str, root: Path | None = None) -> Path:
    """Resolve task ID to file path."""
    if root is None:
        root = require_tasks_root()

    # Check if it's a directory (parent task)
    dir_path = root / task_id
    if dir_path.is_dir():
        return dir_path / INDEX_FILE

    # Check if it's a file
    file_path = root / f"{task_id}.md"
    if file_path.exists():
        return file_path

    # Maybe they included .md extension
    if task_id.endswith(".md"):
        file_path = root / task_id
        if file_path.exists():
            return file_path

    raise TaskError(f"Task not found: {task_id}")


def get_task_id(path: Path, root: Path) -> str:
    """Get task ID from file path."""
    rel = path.relative_to(root)
    if path.name == INDEX_FILE:
        # Parent task - ID is the directory
        return str(rel.parent)
    else:
        # Leaf task - ID is path without .md
        return str(rel).removesuffix(".md")


def is_leaf(task_id: str, root: Path | None = None) -> bool:
    """Check if task is a leaf (file) vs parent (directory)."""
    if root is None:
        root = require_tasks_root()
    file_path = root / f"{task_id}.md"
    return file_path.exists()


# =============================================================================
# Markdown Parser
# =============================================================================


def parse_task(path: Path, root: Path | None = None) -> Task:
    """Parse markdown file into Task object."""
    if root is None:
        root = require_tasks_root()

    content = path.read_text()

    # Split frontmatter and body
    match = re.match(r"^---\n(.+?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise TaskError(f"Invalid task format (no frontmatter): {path}")

    frontmatter = parse_frontmatter(match.group(1))
    body = match.group(2).strip()

    # Parse title from H1
    title_match = re.match(r"^# (.+)$", body, re.MULTILINE)
    title = title_match.group(1) if title_match else path.stem

    # Parse description (everything between title and ## Notes or ## sections)
    desc_match = re.search(r"^# .+\n\n(.+?)(?=\n## |\Z)", body, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Parse notes from ## Notes section
    notes = []
    notes_match = re.search(r"## Notes\n(.+)$", body, re.DOTALL)
    if notes_match:
        # Find all ### timestamp headers followed by content
        note_pattern = r"### (\d{4}-\d{2}-\d{2}T[^\n]+)\n\n(.*?)(?=\n### |\Z)"
        note_blocks = re.findall(note_pattern, notes_match.group(1), re.DOTALL)
        for timestamp, text in note_blocks:
            notes.append(Note(text=text.strip(), created=timestamp))

    return Task(
        id=get_task_id(path, root),
        title=title,
        status=frontmatter.get("status", "pending"),
        description=description,
        deps=frontmatter.get("deps", []),
        approach=frontmatter.get("approach", ""),
        criteria=frontmatter.get("criteria", []),
        files=frontmatter.get("files", []),
        notes=notes,
        created=frontmatter.get("created", ""),
        updated=frontmatter.get("updated", ""),
        started=frontmatter.get("started", ""),
        completed=frontmatter.get("completed", ""),
        blocked_reason=frontmatter.get("blocked_reason", ""),
    )


# =============================================================================
# Markdown Renderer
# =============================================================================


def render_task(task: Task) -> str:
    """Render Task object to markdown string."""
    # Build frontmatter dict - order matters for readability
    frontmatter: dict = {
        "status": task.status,
        "created": task.created or now_iso(),
        "updated": task.updated or now_iso(),
    }

    if task.started:
        frontmatter["started"] = task.started
    if task.completed:
        frontmatter["completed"] = task.completed
    if task.blocked_reason:
        frontmatter["blocked_reason"] = task.blocked_reason
    if task.deps:
        frontmatter["deps"] = task.deps
    if task.approach:
        frontmatter["approach"] = task.approach
    if task.criteria:
        frontmatter["criteria"] = task.criteria
    if task.files:
        frontmatter["files"] = task.files

    lines = [
        "---",
        render_frontmatter(frontmatter),
        "---",
        "",
        f"# {task.title}",
    ]

    if task.description:
        lines.extend(["", task.description])

    if task.notes:
        lines.extend(["", "## Notes"])
        for note in task.notes:
            lines.extend(["", f"### {note.created}", "", note.text])

    return "\n".join(lines) + "\n"


# =============================================================================
# Task Walking
# =============================================================================


def walk_tasks(
    root: Path | None = None, depth_first: bool = True
) -> Iterator[tuple[str, Task]]:
    """
    Walk directory tree, yielding (id, Task) tuples.

    Args:
        root: Tasks root directory. If None, finds it automatically.
        depth_first: If True, yield children before siblings.
    """
    if root is None:
        root = require_tasks_root()

    def walk_dir(directory: Path, prefix: str = "") -> Iterator[tuple[str, Task]]:
        """Recursively walk a directory."""
        items = sorted(directory.iterdir(), key=lambda p: p.name)

        for item in items:
            if item.name == INDEX_FILE:
                continue  # Handle index separately

            if item.is_dir():
                # Parent task - yield index first, then children
                index_path = item / INDEX_FILE
                task_id = f"{prefix}{item.name}" if prefix else item.name

                if index_path.exists():
                    task = parse_task(index_path, root)
                    # Populate children
                    task.children = [
                        f"{task_id}/{child.name}".removesuffix(".md")
                        for child in sorted(item.iterdir())
                        if child.name != INDEX_FILE
                    ]
                    yield task_id, task

                # Recurse into children
                if depth_first:
                    yield from walk_dir(item, f"{task_id}/")

            elif item.suffix == ".md":
                # Leaf task
                task_id = f"{prefix}{item.stem}" if prefix else item.stem
                task = parse_task(item, root)
                yield task_id, task

    yield from walk_dir(root)


# =============================================================================
# Promote / Demote
# =============================================================================


def promote_to_parent(task_id: str, root: Path | None = None) -> None:
    """
    Convert a leaf task to a parent task.

    Moves NN-slug.md to NN-slug/00-index.md
    """
    if root is None:
        root = require_tasks_root()

    file_path = root / f"{task_id}.md"
    if not file_path.exists():
        raise TaskError(f"Cannot promote: {task_id} is not a leaf task")

    dir_path = root / task_id
    if dir_path.exists():
        raise TaskError(f"Cannot promote: directory {task_id} already exists")

    # Create directory and move file
    dir_path.mkdir(parents=True)
    file_path.rename(dir_path / INDEX_FILE)


def demote_to_leaf(task_id: str, root: Path | None = None) -> None:
    """
    Convert a parent task with no children to a leaf task.

    Moves NN-slug/00-index.md to NN-slug.md and removes directory.
    """
    if root is None:
        root = require_tasks_root()

    dir_path = root / task_id
    if not dir_path.is_dir():
        raise TaskError(f"Cannot demote: {task_id} is not a parent task")

    index_path = dir_path / INDEX_FILE
    if not index_path.exists():
        raise TaskError(f"Cannot demote: {task_id} has no index file")

    # Check for children
    children = [f for f in dir_path.iterdir() if f.name != INDEX_FILE]
    if children:
        raise TaskError(f"Cannot demote: {task_id} still has children")

    # Move index to file and remove directory
    file_path = root / f"{task_id}.md"
    index_path.rename(file_path)
    dir_path.rmdir()


# =============================================================================
# Dependency Checking
# =============================================================================


def deps_satisfied(task: Task, root: Path | None = None) -> tuple[bool, list[str]]:
    """
    Check if all dependencies are complete.

    Returns (satisfied, list of incomplete dep IDs).
    """
    if root is None:
        root = require_tasks_root()

    incomplete = []
    for dep_id in task.deps:
        try:
            dep_path = get_task_path(dep_id, root)
            dep_task = parse_task(dep_path, root)
            if dep_task.status != "complete":
                incomplete.append(dep_id)
        except TaskError:
            # Dependency doesn't exist - treat as incomplete
            incomplete.append(dep_id)

    return len(incomplete) == 0, incomplete


# =============================================================================
# Error Handling
# =============================================================================


class TaskError(Exception):
    """Raised for task operations that fail."""

    pass
