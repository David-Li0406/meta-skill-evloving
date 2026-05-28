#!/usr/bin/env python3
"""
Update task status in progress file YAML frontmatter.

This script surgically updates a single task's status in a progress file without
loading the full markdown body, preserving all formatting and content.

Usage:
    python update-status.py --file .claude/progress/prd/phase-1-progress.md --task TASK-1.3 --status complete
    python update-status.py --file .claude/progress/prd/phase-1-progress.md --task TASK-1.3 --status blocked --note "Waiting on API"
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


def extract_frontmatter_and_body(filepath: Path) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Extract YAML frontmatter and markdown body separately.

    Args:
        filepath: Path to progress file

    Returns:
        Tuple of (frontmatter dict, markdown body string)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if content starts with frontmatter delimiter
        if not content.strip().startswith('---'):
            print(f"Error: File does not contain YAML frontmatter", file=sys.stderr)
            return None, ""

        # Find the closing delimiter (second ---)
        match = re.match(r'^---\n(.*?\n)---\n(.*)$', content, re.DOTALL)
        if not match:
            print(f"Error: Could not parse YAML frontmatter", file=sys.stderr)
            return None, ""

        frontmatter_str = match.group(1)
        body = match.group(2)

        frontmatter = yaml.safe_load(frontmatter_str)
        return frontmatter, body

    except Exception as e:
        print(f"Error: Could not read {filepath}: {e}", file=sys.stderr)
        return None, ""


def write_frontmatter_and_body(
    filepath: Path,
    frontmatter: Dict[str, Any],
    body: str
) -> None:
    """
    Write updated frontmatter and preserved body back to file.

    Args:
        filepath: Path to progress file
        frontmatter: Updated frontmatter dictionary
        body: Preserved markdown body
    """
    try:
        # Dump frontmatter to YAML string
        frontmatter_yaml = yaml.dump(
            frontmatter,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )

        # Write file with frontmatter delimiters
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(frontmatter_yaml)
            f.write('---\n')
            f.write(body)

    except Exception as e:
        print(f"Error: Could not write to {filepath}: {e}", file=sys.stderr)
        raise


def recalculate_metrics(frontmatter: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recalculate progress metrics based on task statuses.

    Args:
        frontmatter: Progress file frontmatter dictionary

    Returns:
        Updated frontmatter with recalculated metrics
    """
    tasks = frontmatter.get('tasks', [])
    if not tasks:
        return frontmatter

    # Count tasks by status
    completed = sum(1 for t in tasks if t.get('status') == 'completed')
    in_progress = sum(1 for t in tasks if t.get('status') == 'in_progress')
    blocked = sum(1 for t in tasks if t.get('status') == 'blocked')
    at_risk = sum(1 for t in tasks if t.get('status') == 'at_risk')
    pending = sum(1 for t in tasks if t.get('status') == 'pending')

    total = len(tasks)

    # Calculate overall progress percentage
    progress = int((completed / total) * 100) if total > 0 else 0

    # Update frontmatter metrics
    frontmatter['total_tasks'] = total
    frontmatter['completed_tasks'] = completed
    frontmatter['in_progress_tasks'] = in_progress
    frontmatter['blocked_tasks'] = blocked
    frontmatter['progress'] = progress

    # Update phase status based on progress
    if progress == 100:
        frontmatter['status'] = 'completed'
    elif blocked > 0 or at_risk > 0:
        frontmatter['status'] = 'at_risk'
    elif in_progress > 0:
        frontmatter['status'] = 'in_progress'
    else:
        frontmatter['status'] = 'pending'

    # Update timestamp
    frontmatter['updated'] = datetime.now().strftime('%Y-%m-%d')

    return frontmatter


def update_task_status(
    filepath: Path,
    task_id: str,
    status: str,
    note: Optional[str] = None
) -> Tuple[int, int]:
    """
    Update status of a single task in progress file.

    Args:
        filepath: Path to progress file
        task_id: Task identifier (e.g., "TASK-1.3")
        status: New status value (pending, in_progress, completed, blocked, at_risk)
        note: Optional note to add to task

    Returns:
        Tuple of (old_progress, new_progress) percentages

    Raises:
        ValueError: If task not found or invalid status
        FileNotFoundError: If file doesn't exist
    """
    # Validate status
    valid_statuses = ['pending', 'in_progress', 'completed', 'blocked', 'at_risk']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}")

    # Check file exists
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Extract frontmatter and body
    frontmatter, body = extract_frontmatter_and_body(filepath)
    if frontmatter is None:
        raise ValueError("Could not extract frontmatter from file")

    # Get current progress
    old_progress = frontmatter.get('progress', 0)

    # Find and update task
    tasks = frontmatter.get('tasks', [])
    task_found = False

    for task in tasks:
        if task.get('id') == task_id:
            task['status'] = status
            if note:
                task['note'] = note
            task_found = True
            break

    if not task_found:
        raise ValueError(f"Task '{task_id}' not found in {filepath}")

    # Recalculate metrics
    frontmatter = recalculate_metrics(frontmatter)
    new_progress = frontmatter.get('progress', 0)

    # Write back to file
    write_frontmatter_and_body(filepath, frontmatter, body)

    return old_progress, new_progress


def main():
    """Main entry point for update-status script."""
    parser = argparse.ArgumentParser(
        description="Update task status in progress file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mark task as complete
  python update-status.py --file .claude/progress/prd/phase-1-progress.md --task TASK-1.3 --status completed

  # Mark task as blocked with note
  python update-status.py --file .claude/progress/prd/phase-1-progress.md --task TASK-1.3 --status blocked --note "Waiting on API"

  # Start working on task
  python update-status.py --file .claude/progress/prd/phase-1-progress.md --task TASK-1.3 --status in_progress

Valid statuses: pending, in_progress, completed, blocked, at_risk
        """
    )

    parser.add_argument(
        '--file',
        '-f',
        type=Path,
        required=True,
        help='Path to progress file'
    )

    parser.add_argument(
        '--task',
        '-t',
        required=True,
        help='Task ID to update (e.g., TASK-1.3)'
    )

    parser.add_argument(
        '--status',
        '-s',
        required=True,
        choices=['pending', 'in_progress', 'completed', 'blocked', 'at_risk'],
        help='New status for the task'
    )

    parser.add_argument(
        '--note',
        '-n',
        help='Optional note to add to the task'
    )

    args = parser.parse_args()

    try:
        # Update task status
        old_progress, new_progress = update_task_status(
            args.file,
            args.task,
            args.status,
            args.note
        )

        # Print success message
        print(f"✓ Updated {args.task} to '{args.status}'")
        if args.note:
            print(f"  Note: {args.note}")
        print(f"  Progress: {old_progress}% → {new_progress}%")
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
