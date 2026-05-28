#!/usr/bin/env python3
"""
Build hierarchical task tree from bd graph --all --json output.

Usage:
    bd graph --all --json | python3 bd-tree.py
    bd graph --all --json | python3 bd-tree.py -s "search term"
    bd graph --all --json | python3 bd-tree.py -n 10
    bd graph --all --json | python3 bd-tree.py --collapse
"""

import argparse
import json
import sys
from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    title: str
    status: str
    priority: int
    issue_type: str
    labels: list[str] = field(default_factory=list)
    description: str = ""
    children: list["Task"] = field(default_factory=list)
    parent_id: str | None = None
    is_blocked: bool = False


TYPE_LETTERS = {
    "epic": "E",
    "feature": "F",
    "task": "T",
    "bug": "B",
    "chore": "C",
}

STATUS_ORDER = {"in_progress": 0, "open": 1, "deferred": 2}
VISIBLE_STATUSES = {"open", "in_progress", "deferred"}


def parse_graphs(data: list[dict]) -> dict[str, Task]:
    """Parse all graphs into a flat dict of tasks."""
    tasks: dict[str, Task] = {}
    parent_map: dict[str, str] = {}  # child_id -> parent_id
    blocked_ids: set[str] = set()

    for graph in data:
        # Parse issues
        for issue in graph.get("Issues") or []:
            task = Task(
                id=issue["id"],
                title=issue["title"],
                status=issue["status"],
                priority=issue.get("priority", 2),
                issue_type=issue.get("issue_type", "task"),
                labels=issue.get("labels", []),
                description=issue.get("description", ""),
            )
            tasks[task.id] = task

        # Parse dependencies
        for dep in graph.get("Dependencies") or []:
            if dep["type"] == "parent-child":
                child_id = dep["issue_id"]
                parent_id = dep["depends_on_id"]
                parent_map[child_id] = parent_id
            elif dep["type"] == "blocks":
                # issue_id is blocked by depends_on_id
                blocked_id = dep["issue_id"]
                blocker_id = dep["depends_on_id"]
                # Only blocked if blocker is not closed
                if blocker_id in tasks and tasks[blocker_id].status != "closed":
                    blocked_ids.add(blocked_id)

    # Build parent-child relationships
    for child_id, parent_id in parent_map.items():
        if child_id in tasks and parent_id in tasks:
            tasks[child_id].parent_id = parent_id
            tasks[parent_id].children.append(tasks[child_id])

    # Mark blocked tasks
    for task_id in blocked_ids:
        if task_id in tasks:
            tasks[task_id].is_blocked = True

    return tasks


def should_show(task: Task, show_blocked: bool = False) -> bool:
    """Check if task should be shown."""
    if task.status == "closed":
        return False
    if task.is_blocked and not show_blocked:
        return False
    return task.status in VISIBLE_STATUSES


def has_visible_descendants(task: Task) -> bool:
    """Check if task has any visible descendants."""
    return any(should_show(child) or has_visible_descendants(child) for child in task.children)


def sort_tasks(tasks: list[Task]) -> list[Task]:
    """Sort tasks by status (in_progress first), then priority."""
    return sorted(
        tasks,
        key=lambda t: (STATUS_ORDER.get(t.status, 99), t.priority),
    )


def filter_by_search(task: Task, search: str) -> bool:
    """Check if task matches search term."""
    search = search.lower()
    return (
        search in task.title.lower()
        or search in task.id.lower()
        or any(search in label.lower() for label in task.labels)
    )


def collect_matching_ids(tasks: dict[str, Task], search: str) -> set[str]:
    """Collect IDs of tasks matching search and their ancestors/descendants."""
    matching: set[str] = set()

    for task in tasks.values():
        if filter_by_search(task, search):
            # Add task and all ancestors
            current: Task | None = task
            while current:
                matching.add(current.id)
                current = tasks[current.parent_id] if current.parent_id and current.parent_id in tasks else None

            # Add all descendants
            def add_descendants(t: Task) -> None:
                for child in t.children:
                    matching.add(child.id)
                    add_descendants(child)

            add_descendants(task)

    return matching


def format_task_line(task: Task, prefix: str, number: str, is_root: bool = False) -> str:
    """Format a single task line."""
    type_letter = TYPE_LETTERS.get(task.issue_type, "T")
    status = task.status
    priority = f"P{task.priority}"
    labels = " ".join(f"#{lbl}" for lbl in task.labels) if task.labels else ""

    # Root items get trailing dot: "1." Children don't: "1.1"
    num_display = f"{number}." if is_root else number
    line = f"{prefix}{num_display} [{type_letter}] {task.title} ({task.id}) | {priority} · {status}"
    if labels:
        line += f" | {labels}"

    return line


def print_tree(  # noqa: PLR0913
    task: Task,
    prefix: str = "",
    connector: str = "",
    number: str = "1",
    is_last: bool = True,
    is_root: bool = False,
    search_ids: set[str] | None = None,
    collapse: bool = False,
) -> list[str]:
    """Recursively build tree lines."""
    lines: list[str] = []

    # Skip if search filter active and task not in matching set
    if search_ids and task.id not in search_ids:
        return lines

    # Skip if not visible (unless has visible descendants for deferred)
    if not should_show(task) and (task.status != "deferred" or not has_visible_descendants(task)):
        return lines

    # Format current task - display prefix includes connector for this line only
    display_prefix = prefix + connector
    lines.append(format_task_line(task, display_prefix, number, is_root=is_root))

    # Handle collapse mode
    visible_children = [c for c in task.children if should_show(c) or has_visible_descendants(c)]
    if collapse and visible_children:
        lines[-1] += f" [+{len(visible_children)}]"
        return lines

    # Sort and filter children
    visible_children = sort_tasks(visible_children)
    if search_ids:
        visible_children = [c for c in visible_children if c.id in search_ids]

    # Continuation prefix for children: add vertical bar or spaces based on is_last
    child_base_prefix = prefix + ("   " if is_last else "│  ") if not is_root else ""

    # Print children
    for i, child in enumerate(visible_children):
        is_child_last = i == len(visible_children) - 1
        child_connector = "└─ " if is_child_last else "├─ "
        child_number = f"{number}.{i + 1}"

        child_lines = print_tree(
            child,
            prefix=child_base_prefix,
            connector=child_connector,
            number=child_number,
            is_last=is_child_last,
            search_ids=search_ids,
            collapse=collapse,
        )
        if child_lines:
            lines.extend(child_lines)

    return lines


def build_tree(
    tasks: dict[str, Task],
    search: str | None = None,
    limit: int | None = None,
    collapse: bool = False,
) -> list[str]:
    """Build the full tree output."""
    # Find root tasks (no parent)
    roots = [t for t in tasks.values() if t.parent_id is None]
    roots = sort_tasks(roots)

    # Apply search filter
    search_ids = None
    search_failed = False
    if search:
        search_ids = collect_matching_ids(tasks, search)
        if not search_ids:
            search_failed = True
            search_ids = None  # Show all tasks instead

    # Apply limit to roots
    if limit:
        roots = roots[:limit]

    # Build output
    lines: list[str] = []
    for i, root in enumerate(roots):
        is_last = i == len(roots) - 1
        number = str(i + 1)
        root_lines = print_tree(
            root,
            prefix="",
            number=number,
            is_last=is_last,
            is_root=True,
            search_ids=search_ids,
            collapse=collapse,
        )
        lines.extend(root_lines)
        if not is_last and root_lines:
            lines.append("")  # Empty line between root trees

    # Prepend search failure message if search found nothing
    if search_failed and lines:
        header = [f'Search "{search}" found no tasks.', "", "All available tasks:", ""]
        lines = header + lines

    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Build task tree from bd graph JSON")
    parser.add_argument("-s", "--search", help="Filter tasks by search term")
    parser.add_argument("-n", "--limit", type=int, help="Limit number of root tasks")
    parser.add_argument("--collapse", action="store_true", help="Collapse children, show count")
    args = parser.parse_args()

    # Read JSON from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not data:
        print("No tasks available.")
        return

    # Parse and build tree
    tasks = parse_graphs(data)

    if not tasks:
        print("No tasks available.")
        return

    lines = build_tree(
        tasks,
        search=args.search,
        limit=args.limit,
        collapse=args.collapse,
    )

    if not lines:
        print("No tasks match the filter criteria.")
        print()
        print("Possible reasons:")
        print("- All tasks are closed")
        print("- All open tasks are blocked")
        print("- All tasks are deferred")
        return

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
