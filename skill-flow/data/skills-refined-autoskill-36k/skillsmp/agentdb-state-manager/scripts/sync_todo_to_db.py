#!/usr/bin/env python3
"""Sync TODO_*.md files to AgentDB.

Parses YAML frontmatter from TODO files and converts to immutable append-only
records in AgentDB.

Usage:
    python sync_todo_to_db.py [TODO_FILE]
    python sync_todo_to_db.py --all

If no file specified, syncs all TODO_*.md files in current directory.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


# ANSI colors (simplified)
class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    END = "\033[0m"


def error_exit(msg: str) -> None:
    print(f"{Colors.RED}✗ {msg}{Colors.END}", file=sys.stderr)
    sys.exit(1)


def success(msg: str) -> None:
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def info(msg: str) -> None:
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")


def parse_todo_file(file_path: Path) -> dict[str, Any] | None:
    """Parse TODO file and extract YAML frontmatter.

    Args:
        file_path: Path to TODO_*.md file

    Returns:
        Dictionary with parsed frontmatter or None if invalid
    """
    try:
        content = file_path.read_text(encoding="utf-8")

        # Extract YAML frontmatter between ---
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return None

        frontmatter = yaml.safe_load(match.group(1))
        return frontmatter

    except Exception as e:
        error_exit(f"Failed to parse {file_path.name}: {e}")
        return None


def convert_to_records(frontmatter: dict[str, Any], file_name: str) -> list[dict[str, Any]]:
    """Convert TODO frontmatter to AgentDB records.

    Args:
        frontmatter: Parsed YAML frontmatter
        file_name: Name of source TODO file

    Returns:
        List of records to insert into workflow_records table
    """
    records = []

    # Workflow-level record
    workflow_id = frontmatter.get("slug", "unknown")
    workflow_type = frontmatter.get("workflow_type", "feature")

    workflow_progress = frontmatter.get("workflow_progress", {})
    phase = workflow_progress.get("phase", 0)

    records.append(
        {
            "object_id": f"workflow_{workflow_id}",
            "object_type": "workflow",
            "object_state": f"0{phase}_phase-{phase}",
            "object_metadata": json.dumps(
                {
                    "workflow_type": workflow_type,
                    "slug": frontmatter.get("slug"),
                    "github_user": frontmatter.get("github_user"),
                    "timestamp": frontmatter.get("timestamp"),
                    "current_step": workflow_progress.get("current_step"),
                    "last_task": workflow_progress.get("last_task"),
                    "source_file": file_name,
                }
            ),
        }
    )

    # Task records
    tasks = frontmatter.get("tasks", {})
    for task_group, task_list in tasks.items():
        if not isinstance(task_list, list):
            continue

        for task in task_list:
            task_id = task.get("id", "unknown")
            status = task.get("status", "pending")

            # Map TODO status to workflow-states.json states
            state_map = {"pending": "00_pending", "in_progress": "20_in-progress", "complete": "99_done", "blocked": "30_blocked"}

            records.append(
                {
                    "object_id": f"task_{task_id}",
                    "object_type": "task",
                    "object_state": state_map.get(status, "00_pending"),
                    "object_metadata": json.dumps(
                        {
                            "description": task.get("description"),
                            "group": task_group,
                            "completed_at": task.get("completed_at"),
                            "files": task.get("files", []),
                            "dependencies": task.get("dependencies", []),
                        }
                    ),
                }
            )

    # Quality gate records
    quality_gates = frontmatter.get("quality_gates", {})
    if quality_gates:
        for gate_type, value in quality_gates.items():
            if gate_type == "semantic_version":
                continue  # Skip version field

            passed = value if isinstance(value, bool) else (value >= 80 if isinstance(value, int | float) else False)

            records.append(
                {
                    "object_id": f"quality_{workflow_id}_{gate_type}",
                    "object_type": "quality_gate",
                    "object_state": "20_passed" if passed else "E01_failed",
                    "object_metadata": json.dumps({"gate_type": gate_type, "value": value, "passed": passed}),
                }
            )

    return records


def sync_to_agentdb(records: list[dict[str, Any]], session_id: str) -> bool:
    """Insert records into AgentDB.

    Args:
        records: List of records to insert
        session_id: AgentDB session ID

    Returns:
        True if sync successful

    Note: In actual execution, would use AgentDB tool to execute SQL.
    """
    info(f"Syncing {len(records)} records to AgentDB...")

    # Generate INSERT statements
    for record in records:
        sql = f"""
        INSERT INTO workflow_records (object_id, object_type, object_state, object_metadata)
        VALUES (
            '{record["object_id"]}',
            '{record["object_type"]}',
            '{record["object_state"]}',
            '{record["object_metadata"]}'::JSON
        );
        """
        print(sql.strip())

    success(f"Prepared {len(records)} INSERT statements")
    print("\nNOTE: In actual execution, these would be sent to AgentDB")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync TODO files to AgentDB")
    parser.add_argument("file", nargs="?", help="TODO file to sync")
    parser.add_argument("--all", action="store_true", help="Sync all TODO_*.md files")
    parser.add_argument("--session-id", help="AgentDB session ID")

    args = parser.parse_args()

    # Find TODO files
    if args.all or not args.file:
        todo_files = list(Path.cwd().glob("TODO_*.md"))
        if not todo_files:
            error_exit("No TODO_*.md files found")
    else:
        todo_files = [Path(args.file)]
        if not todo_files[0].exists():
            error_exit(f"File not found: {args.file}")

    info(f"Found {len(todo_files)} TODO file(s)")

    # Parse and sync each file
    for todo_file in todo_files:
        info(f"Processing {todo_file.name}...")

        frontmatter = parse_todo_file(todo_file)
        if not frontmatter:
            print(f"  Skipping {todo_file.name} (no valid frontmatter)")
            continue

        records = convert_to_records(frontmatter, todo_file.name)
        sync_to_agentdb(records, args.session_id or "default")

        success(f"Synced {todo_file.name}")

    print(f"\n{Colors.GREEN}✓ Sync complete{Colors.END}\n")


if __name__ == "__main__":
    main()
