#!/usr/bin/env python3
"""
Task tracker for LLM context preservation.

Stores tasks as markdown files in .claude/tasks/ directory.
All output is JSON for machine consumption.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path

from task_fs import (
    TASKS_DIR,
    INDEX_FILE,
    VALID_STATUSES,
    Task,
    Note,
    TaskError,
    find_tasks_root,
    require_tasks_root,
    slugify,
    next_prefix,
    get_task_path,
    get_task_id,
    is_leaf,
    parse_task,
    render_task,
    walk_tasks,
    promote_to_parent,
    demote_to_leaf,
    deps_satisfied,
    now_iso,
)


# =============================================================================
# Output Helpers
# =============================================================================


def output_success(data: dict) -> None:
    """Print success response and exit 0."""
    print(json.dumps({"ok": True, **data}, default=str))
    sys.exit(0)


def output_error(message: str) -> None:
    """Print error response and exit 1."""
    print(json.dumps({"ok": False, "error": message}))
    sys.exit(1)


def task_to_dict(task: Task) -> dict:
    """Convert Task to JSON-serializable dict."""
    d = asdict(task)
    # Convert Note objects to dicts
    d["notes"] = [asdict(n) if hasattr(n, "__dataclass_fields__") else n for n in task.notes]
    return d


# =============================================================================
# Commands
# =============================================================================


def cmd_init(args: argparse.Namespace) -> None:
    """Initialize a new tasks directory."""
    tasks_dir = Path.cwd() / TASKS_DIR
    if tasks_dir.exists():
        output_error(f"{tasks_dir} already exists")

    tasks_dir.mkdir(parents=True)
    output_success({"message": f"Created {tasks_dir}", "path": str(tasks_dir)})


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new task or subtask."""
    root = require_tasks_root()

    # Determine target directory
    if args.parent:
        parent_id = args.parent
        parent_file = root / f"{parent_id}.md"
        parent_dir = root / parent_id

        # Promote leaf to directory if needed
        if parent_file.exists() and not parent_dir.exists():
            promote_to_parent(parent_id, root)

        if not parent_dir.exists():
            output_error(f"Parent task not found: {parent_id}")

        target_dir = parent_dir
        task_id_prefix = f"{parent_id}/"
    else:
        target_dir = root
        task_id_prefix = ""

    # Create task
    slug = slugify(args.title)
    prefix = next_prefix(target_dir)
    task_name = f"{prefix}-{slug}"
    task_path = target_dir / f"{task_name}.md"
    task_id = f"{task_id_prefix}{task_name}"

    task = Task(
        id=task_id,
        title=args.title,
        status="pending",
        description=args.description or "",
        approach=args.approach or "",
        criteria=args.criteria or [],
        files=args.files or [],
    )

    # Handle dependencies
    if args.deps:
        dep_ids = []
        for dep in args.deps:
            try:
                get_task_path(dep, root)  # Validate exists
                dep_ids.append(dep)
            except TaskError:
                output_error(f"Dependency not found: {dep}")
        task.deps = dep_ids

    task_path.write_text(render_task(task))
    output_success({"task": task_to_dict(task), "id": task_id})


def cmd_remove(args: argparse.Namespace) -> None:
    """Remove a task or subtask."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)
    task_id = task.id

    if task_path.name == INDEX_FILE:
        # Parent task - remove entire directory
        shutil.rmtree(task_path.parent)
    else:
        # Leaf task - just unlink
        task_path.unlink()

        # Check if parent should demote
        parent_dir = task_path.parent
        if parent_dir != root:
            children = [f for f in parent_dir.iterdir() if f.name != INDEX_FILE]
            if not children:
                parent_id = str(parent_dir.relative_to(root))
                try:
                    demote_to_leaf(parent_id, root)
                except TaskError:
                    pass  # If demotion fails, leave as empty parent

    output_success({"removed": task_id, "task": task_to_dict(task)})


def cmd_update(args: argparse.Namespace) -> None:
    """Update a task's fields."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)

    if args.title:
        task.title = args.title
    if args.description:
        task.description = args.description
    if args.approach:
        task.approach = args.approach
    if args.criteria is not None:
        task.criteria = args.criteria
    if args.files is not None:
        task.files = args.files
    if args.status:
        if args.status not in VALID_STATUSES:
            output_error(f"Invalid status: {args.status}. Valid: {', '.join(VALID_STATUSES)}")
        task.status = args.status
    if args.deps is not None:
        dep_ids = []
        for dep in args.deps:
            try:
                get_task_path(dep, root)
                dep_ids.append(dep)
            except TaskError:
                output_error(f"Dependency not found: {dep}")
        task.deps = dep_ids

    task.updated = now_iso()
    task_path.write_text(render_task(task))
    output_success({"task": task_to_dict(task), "id": task.id})


def cmd_list(args: argparse.Namespace) -> None:
    """List all tasks."""
    root = require_tasks_root()

    tasks = []
    for task_id, task in walk_tasks(root):
        if args.status and task.status != args.status:
            continue
        tasks.append({"id": task_id, **task_to_dict(task)})

    output_success({"tasks": tasks, "count": len(tasks)})


def cmd_show(args: argparse.Namespace) -> None:
    """Show a single task."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)
    satisfied, incomplete = deps_satisfied(task, root)

    result = {
        "task": task_to_dict(task),
        "id": task.id,
        "deps_satisfied": satisfied,
    }
    if not satisfied:
        result["incomplete_deps"] = incomplete

    output_success(result)


def cmd_next(args: argparse.Namespace) -> None:
    """Get the next task to work on (depth-first, deps satisfied)."""
    root = require_tasks_root()

    # First, find in_progress tasks and check for pending children
    for task_id, task in walk_tasks(root, depth_first=True):
        if task.status == "in_progress" and task.children:
            # Check children for pending tasks
            for child_id in task.children:
                try:
                    child_path = get_task_path(child_id, root)
                    child = parse_task(child_path, root)
                    if child.status == "pending":
                        satisfied, _ = deps_satisfied(child, root)
                        if satisfied:
                            output_success({
                                "task": task_to_dict(child),
                                "id": child_id,
                                "reason": "pending child of in_progress task",
                            })
                except TaskError:
                    continue

    # No in_progress with pending children - find first pending with satisfied deps
    for task_id, task in walk_tasks(root, depth_first=True):
        if task.status == "pending":
            satisfied, _ = deps_satisfied(task, root)
            if satisfied:
                output_success({
                    "task": task_to_dict(task),
                    "id": task_id,
                    "reason": "first pending task with satisfied dependencies",
                })

    output_success({"task": None, "reason": "no available tasks"})


def cmd_start(args: argparse.Namespace) -> None:
    """Start working on a task (set to in_progress)."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)

    # Check dependencies (soft blocking - warn but allow)
    satisfied, incomplete = deps_satisfied(task, root)
    warnings = []
    if not satisfied:
        warnings.append(f"Starting with incomplete dependencies: {', '.join(incomplete)}")

    task.status = "in_progress"
    task.updated = now_iso()
    if not task.started:
        task.started = now_iso()

    task_path.write_text(render_task(task))

    result = {"task": task_to_dict(task), "id": task.id}
    if warnings:
        result["warnings"] = warnings
    output_success(result)


def cmd_done(args: argparse.Namespace) -> None:
    """Mark a task complete."""
    root = require_tasks_root()

    if args.id:
        try:
            task_path = get_task_path(args.id, root)
        except TaskError as e:
            output_error(str(e))
    else:
        # Find current in_progress task (deepest first)
        task_path = None
        for task_id, task in walk_tasks(root, depth_first=True):
            if task.status == "in_progress":
                task_path = get_task_path(task_id, root)
                break

        if not task_path:
            output_error("No in_progress task found. Specify an ID.")

    task = parse_task(task_path, root)
    task.status = "complete"
    task.completed = now_iso()
    task.updated = now_iso()

    task_path.write_text(render_task(task))
    output_success({"task": task_to_dict(task), "id": task.id})


def cmd_block(args: argparse.Namespace) -> None:
    """Block a task with optional reason."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)
    task.status = "blocked"
    task.updated = now_iso()
    if args.reason:
        task.blocked_reason = args.reason

    task_path.write_text(render_task(task))
    output_success({"task": task_to_dict(task), "id": task.id})


def cmd_unblock(args: argparse.Namespace) -> None:
    """Unblock a task (set back to pending)."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)
    task.status = "pending"
    task.blocked_reason = ""
    task.updated = now_iso()

    task_path.write_text(render_task(task))
    output_success({"task": task_to_dict(task), "id": task.id})


def cmd_note(args: argparse.Namespace) -> None:
    """Add a note to a task."""
    root = require_tasks_root()

    try:
        task_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(task_path, root)

    note = Note(text=args.text, created=now_iso())
    task.notes.append(note)
    task.updated = now_iso()

    task_path.write_text(render_task(task))

    output_success({
        "task_id": task.id,
        "note": asdict(note),
        "note_count": len(task.notes),
    })


def cmd_notes(args: argparse.Namespace) -> None:
    """List all notes chronologically."""
    root = require_tasks_root()

    all_notes = []
    for task_id, task in walk_tasks(root):
        for note in task.notes:
            all_notes.append({
                "task_id": task_id,
                "task_title": task.title,
                "text": note.text,
                "created": note.created,
            })

    all_notes.sort(key=lambda n: n["created"])
    output_success({"notes": all_notes, "count": len(all_notes)})


def cmd_move(args: argparse.Namespace) -> None:
    """Move a task to a new location."""
    root = require_tasks_root()

    try:
        src_path = get_task_path(args.id, root)
    except TaskError as e:
        output_error(str(e))

    task = parse_task(src_path, root)
    old_id = task.id

    # Determine destination
    if args.parent:
        dest_parent = args.parent
        dest_parent_file = root / f"{dest_parent}.md"
        dest_parent_dir = root / dest_parent

        # Promote destination parent if needed
        if dest_parent_file.exists() and not dest_parent_dir.exists():
            promote_to_parent(dest_parent, root)

        if not dest_parent_dir.exists():
            output_error(f"Destination parent not found: {dest_parent}")

        dest_dir = dest_parent_dir
        new_id_prefix = f"{dest_parent}/"
    else:
        dest_dir = root
        new_id_prefix = ""

    # Calculate new name
    old_name = Path(old_id).name
    # Extract slug from old name (remove prefix)
    if "-" in old_name:
        old_slug = old_name.split("-", 1)[1]
    else:
        old_slug = old_name

    new_prefix = next_prefix(dest_dir)
    new_name = f"{new_prefix}-{old_slug}"
    new_id = f"{new_id_prefix}{new_name}"

    # Move file or directory
    if src_path.name == INDEX_FILE:
        # Moving a parent task
        src_dir = src_path.parent
        dest_path = dest_dir / new_name
        shutil.move(str(src_dir), str(dest_path))
    else:
        # Moving a leaf task
        dest_path = dest_dir / f"{new_name}.md"
        shutil.move(str(src_path), str(dest_path))

        # Check if old parent should demote
        old_parent_dir = src_path.parent
        if old_parent_dir != root:
            children = [f for f in old_parent_dir.iterdir() if f.name != INDEX_FILE]
            if not children:
                old_parent_id = str(old_parent_dir.relative_to(root))
                try:
                    demote_to_leaf(old_parent_id, root)
                except TaskError:
                    pass

    # Update task ID in the moved file
    new_task_path = get_task_path(new_id, root)
    task = parse_task(new_task_path, root)
    task.id = new_id
    task.updated = now_iso()
    new_task_path.write_text(render_task(task))

    # Update dep references in all tasks
    for other_id, other_task in walk_tasks(root):
        if old_id in other_task.deps:
            other_path = get_task_path(other_id, root)
            other_task.deps = [new_id if d == old_id else d for d in other_task.deps]
            other_task.updated = now_iso()
            other_path.write_text(render_task(other_task))

    output_success({"old_id": old_id, "new_id": new_id, "task": task_to_dict(task)})


# =============================================================================
# Main
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Task tracker for LLM context preservation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    subparsers.add_parser("init", help="Create .claude/tasks/ directory")

    # add
    add_parser = subparsers.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--parent", "-p", help="Parent task ID (for subtasks)")
    add_parser.add_argument("--description", "-d", help="Task description")
    add_parser.add_argument("--approach", "-a", help="Implementation approach")
    add_parser.add_argument("--criteria", "-c", nargs="*", help="Acceptance criteria")
    add_parser.add_argument("--files", "-f", nargs="*", help="Relevant file paths")
    add_parser.add_argument("--deps", nargs="*", help="Dependency task IDs")

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove a task")
    remove_parser.add_argument("id", help="Task ID (path-based)")

    # update
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument("--description", "-d", help="New description")
    update_parser.add_argument("--approach", "-a", help="Implementation approach")
    update_parser.add_argument("--criteria", "-c", nargs="*", help="Acceptance criteria")
    update_parser.add_argument("--files", "-f", nargs="*", help="Relevant file paths")
    update_parser.add_argument("--status", "-s", choices=VALID_STATUSES, help="New status")
    update_parser.add_argument("--deps", nargs="*", help="Dependency task IDs")

    # list
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", "-s", choices=VALID_STATUSES, help="Filter by status")

    # show
    show_parser = subparsers.add_parser("show", help="Show a task")
    show_parser.add_argument("id", help="Task ID")

    # next
    subparsers.add_parser("next", help="Get next available task")

    # start
    start_parser = subparsers.add_parser("start", help="Start a task")
    start_parser.add_argument("id", help="Task ID")

    # done
    done_parser = subparsers.add_parser("done", help="Mark task complete")
    done_parser.add_argument("id", nargs="?", help="Task ID (default: current in_progress)")

    # block
    block_parser = subparsers.add_parser("block", help="Block a task")
    block_parser.add_argument("id", help="Task ID")
    block_parser.add_argument("--reason", "-r", help="Reason for blocking")

    # unblock
    unblock_parser = subparsers.add_parser("unblock", help="Unblock a task")
    unblock_parser.add_argument("id", help="Task ID")

    # note
    note_parser = subparsers.add_parser("note", help="Add a note to a task")
    note_parser.add_argument("id", help="Task ID")
    note_parser.add_argument("text", help="Note text")

    # notes
    subparsers.add_parser("notes", help="List all notes chronologically")

    # move
    move_parser = subparsers.add_parser("move", help="Move a task")
    move_parser.add_argument("id", help="Task ID to move")
    move_parser.add_argument("--parent", "-p", help="New parent task ID (omit for top-level)")

    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "remove": cmd_remove,
        "update": cmd_update,
        "list": cmd_list,
        "show": cmd_show,
        "next": cmd_next,
        "start": cmd_start,
        "done": cmd_done,
        "block": cmd_block,
        "unblock": cmd_unblock,
        "note": cmd_note,
        "notes": cmd_notes,
        "move": cmd_move,
    }

    try:
        commands[args.command](args)
    except TaskError as e:
        output_error(str(e))


if __name__ == "__main__":
    main()
