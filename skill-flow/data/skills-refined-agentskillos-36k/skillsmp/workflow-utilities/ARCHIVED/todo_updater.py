#!/usr/bin/env python3
"""Update TODO file status, workflow progress, and history."""

import sys
from datetime import datetime
from pathlib import Path


def update_todo_task_status(todo_file, task_id, status, context_usage=None):
    """
    Update task status in TODO file.

    Args:
        todo_file: Path to TODO file
        task_id: Task ID (e.g., 'impl_003')
        status: New status ('pending' | 'complete' | 'blocked')
        context_usage: Optional context usage percentage
    """
    try:
        import yaml
    except ImportError:
        try:
            import ruamel.yaml as yaml
        except ImportError:
            print("Error: PyYAML or ruamel.yaml required. Install: pip install pyyaml", file=sys.stderr)
            sys.exit(1)

    todo_path = Path(todo_file)
    if not todo_path.exists():
        print(f"Error: TODO file not found: {todo_file}", file=sys.stderr)
        sys.exit(1)

    content = todo_path.read_text()

    # Split frontmatter and body
    if not content.startswith("---"):
        print("Error: TODO file missing YAML frontmatter", file=sys.stderr)
        sys.exit(1)

    parts = content.split("---", 2)
    if len(parts) < 3:
        print("Error: Invalid TODO file format", file=sys.stderr)
        sys.exit(1)

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2]

    # Update task status in frontmatter
    task_category = task_id.split("_")[0]  # impl, test, etc.

    if "tasks" in frontmatter and task_category in frontmatter["tasks"]:
        for task in frontmatter["tasks"][task_category]:
            if task["id"] == task_id:
                task["status"] = status
                if status == "complete":
                    task["completed_at"] = datetime.utcnow().isoformat() + "Z"
                print(f"✓ Updated {task_id} status to {status}")
                break
        else:
            print(f"Warning: Task {task_id} not found in category {task_category}", file=sys.stderr)
    else:
        print(f"Warning: Task category {task_category} not found", file=sys.stderr)

    # Update workflow progress
    if "workflow_progress" not in frontmatter:
        frontmatter["workflow_progress"] = {}

    frontmatter["workflow_progress"]["last_task"] = task_id
    frontmatter["workflow_progress"]["last_update"] = datetime.utcnow().isoformat() + "Z"

    if context_usage is not None:
        frontmatter["workflow_progress"]["context_usage"] = f"{context_usage}%"

    # Write back
    try:
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    except TypeError:
        # Fallback for older PyYAML
        yaml_str = yaml.dump(frontmatter, default_flow_style=False)

    new_content = f"---\n{yaml_str}---{body}"
    todo_path.write_text(new_content)

    print(f"✓ Updated TODO file: {todo_file}")


def add_todo_history_entry(todo_file, message):
    """Add entry to TODO status history in body."""

    todo_path = Path(todo_file)
    if not todo_path.exists():
        print(f"Error: TODO file not found: {todo_file}", file=sys.stderr)
        return

    content = todo_path.read_text()
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Find status history section
    history_marker = "## Status History"
    if history_marker in content:
        entry = f"- {timestamp}: {message}"
        content = content.replace(history_marker, f"{history_marker}\n{entry}")
        todo_path.write_text(content)
        print(f"✓ Added history: {message}")
    else:
        print(f"Warning: Status History section not found in {todo_file}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: todo_updater.py <todo_file> <task_id> <status> [context_usage]")
        print("Example: todo_updater.py TODO_feature_xxx.md impl_003 complete 35")
        print("Status: pending, complete, blocked")
        sys.exit(1)

    context_usage = int(sys.argv[4]) if len(sys.argv) > 4 else None
    update_todo_task_status(sys.argv[1], sys.argv[2], sys.argv[3], context_usage)
