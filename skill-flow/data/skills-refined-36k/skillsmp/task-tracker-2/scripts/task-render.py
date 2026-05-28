#!/usr/bin/env python3
"""
Render tasks to human-readable markdown.

Reads .claude/tasks/ directory and outputs formatted markdown
grouped by status.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from task_fs import (
    find_tasks_root,
    walk_tasks,
    Task,
)


def format_deps(task: Task) -> str:
    """Format dependency list for display."""
    if not task.deps:
        return ""
    return f" _(depends on: {', '.join(task.deps)})_"


def render_task_line(task_id: str, task: Task, indent: int = 0) -> list[str]:
    """Render a single task to markdown lines."""
    lines = []
    prefix = "  " * indent
    deps = format_deps(task)

    # Task line with checkbox based on status
    if task.status == "complete":
        lines.append(f"{prefix}- [x] **{task_id}** {task.title}{deps}")
    elif task.status == "wont_do":
        lines.append(f"{prefix}- [~] **{task_id}** ~~{task.title}~~{deps}")
    elif task.status == "blocked":
        reason = f" ({task.blocked_reason})" if task.blocked_reason else ""
        lines.append(f"{prefix}- [ ] **{task_id}** {task.title} [BLOCKED]{reason}{deps}")
    else:
        lines.append(f"{prefix}- **{task_id}** {task.title}{deps}")

    # Planning fields
    if task.approach:
        lines.append(f"{prefix}  _Approach: {task.approach}_")
    if task.criteria:
        lines.append(f"{prefix}  _Done when:_")
        for criterion in task.criteria:
            lines.append(f"{prefix}    - {criterion}")
    if task.files:
        files = ", ".join(f"`{f}`" for f in task.files)
        lines.append(f"{prefix}  _Files: {files}_")

    # Notes
    for note in task.notes:
        lines.append(f"{prefix}  > {note.text}")

    return lines


def main():
    root = find_tasks_root()
    if not root:
        print("No .claude/tasks/ found.", file=sys.stderr)
        sys.exit(1)

    # Collect all tasks
    all_tasks: list[tuple[str, Task]] = list(walk_tasks(root))

    if not all_tasks:
        print("# Tasks\n\n_No tasks._")
        return

    # Group by status
    by_status: dict[str, list[tuple[str, Task]]] = defaultdict(list)
    for task_id, task in all_tasks:
        by_status[task.status].append((task_id, task))

    lines = ["# Tasks", ""]

    # Render in priority order
    status_order = ["in_progress", "pending", "blocked", "complete", "wont_do"]
    status_titles = {
        "in_progress": "In Progress",
        "pending": "Pending",
        "blocked": "Blocked",
        "complete": "Completed",
        "wont_do": "Won't Do",
    }

    for status in status_order:
        tasks = by_status.get(status, [])
        if tasks:
            lines.append(f"## {status_titles[status]}")
            for task_id, task in tasks:
                # Calculate indent based on path depth
                depth = task_id.count("/")
                lines.extend(render_task_line(task_id, task, indent=depth))
            lines.append("")

    print("\n".join(lines).rstrip())


if __name__ == "__main__":
    main()
