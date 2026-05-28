#!/usr/bin/env python3
"""
Batch update task statuses in progress file YAML frontmatter.

This script surgically updates multiple tasks' statuses in a single file operation,
preserving all formatting and content while recalculating metrics only once.

Usage:
    python update-batch.py --file .claude/progress/prd/phase-1-progress.md --updates "TASK-1.1:completed,TASK-1.2:completed,TASK-1.3:in_progress"
    python update-batch.py --file .claude/progress/prd/phase-1-progress.md --updates-json '[{"id":"TASK-1.1","status":"completed"},{"id":"TASK-1.2","status":"completed"}]'
"""

import argparse
import json
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


def parse_updates_string(updates: str) -> List[Dict[str, str]]:
    """
    Parse comma-separated updates string.

    Args:
        updates: String like "TASK-1.1:completed,TASK-1.2:in_progress"

    Returns:
        List of update dictionaries

    Raises:
        ValueError: If format is invalid
    """
    result = []
    parts = updates.split(',')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if ':' not in part:
            raise ValueError(f"Invalid update format '{part}'. Expected 'TASK-ID:status'")

        task_id, status = part.split(':', 1)
        result.append({
            'id': task_id.strip(),
            'status': status.strip()
        })

    return result


def update_batch_statuses(
    filepath: Path,
    updates: List[Dict[str, str]]
) -> Tuple[int, int, int]:
    """
    Update statuses of multiple tasks in progress file.

    Args:
        filepath: Path to progress file
        updates: List of update dictionaries with 'id' and 'status' keys

    Returns:
        Tuple of (old_progress, new_progress, updated_count)

    Raises:
        ValueError: If task not found or invalid status
        FileNotFoundError: If file doesn't exist
    """
    # Validate all statuses first
    valid_statuses = ['pending', 'in_progress', 'completed', 'blocked', 'at_risk']
    for update in updates:
        status = update.get('status', '')
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
            )

    # Check file exists
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Extract frontmatter and body
    frontmatter, body = extract_frontmatter_and_body(filepath)
    if frontmatter is None:
        raise ValueError("Could not extract frontmatter from file")

    # Get current progress
    old_progress = frontmatter.get('progress', 0)

    # Build task lookup
    tasks = frontmatter.get('tasks', [])
    task_map = {task.get('id'): task for task in tasks}

    # Apply all updates
    updated_count = 0
    not_found = []

    for update in updates:
        task_id = update.get('id')
        status = update.get('status')
        note = update.get('note')

        task = task_map.get(task_id)
        if not task:
            not_found.append(task_id)
            continue

        task['status'] = status
        if note:
            task['note'] = note
        updated_count += 1

    # Report tasks not found (but don't fail)
    if not_found:
        print(f"Warning: Tasks not found: {', '.join(not_found)}", file=sys.stderr)

    # Recalculate metrics once after all updates
    frontmatter = recalculate_metrics(frontmatter)
    new_progress = frontmatter.get('progress', 0)

    # Write back to file
    write_frontmatter_and_body(filepath, frontmatter, body)

    return old_progress, new_progress, updated_count


def main():
    """Main entry point for update-batch script."""
    parser = argparse.ArgumentParser(
        description="Batch update task statuses in progress file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update multiple tasks with comma-separated format
  python update-batch.py --file .claude/progress/prd/phase-1-progress.md --updates "TASK-1.1:completed,TASK-1.2:completed,TASK-1.3:in_progress"

  # Update with JSON array
  python update-batch.py --file .claude/progress/prd/phase-1-progress.md --updates-json '[{"id":"TASK-1.1","status":"completed"},{"id":"TASK-1.2","status":"completed"}]'

  # Update with notes in JSON
  python update-batch.py --file .claude/progress/prd/phase-1-progress.md --updates-json '[{"id":"TASK-1.3","status":"blocked","note":"Waiting on API"}]'

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

    # Mutually exclusive update formats
    update_group = parser.add_mutually_exclusive_group(required=True)

    update_group.add_argument(
        '--updates',
        '-u',
        help='Comma-separated updates: "TASK-1.1:completed,TASK-1.2:in_progress"'
    )

    update_group.add_argument(
        '--updates-json',
        '-j',
        help='JSON array of updates: [{"id":"TASK-1.1","status":"completed"}]'
    )

    args = parser.parse_args()

    try:
        # Parse updates
        if args.updates:
            updates = parse_updates_string(args.updates)
        else:  # args.updates_json
            try:
                updates = json.loads(args.updates_json)
                if not isinstance(updates, list):
                    raise ValueError("JSON must be an array")
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON: {e}", file=sys.stderr)
                sys.exit(1)

        # Validate update structure
        for update in updates:
            if not isinstance(update, dict):
                raise ValueError("Each update must be a dictionary")
            if 'id' not in update or 'status' not in update:
                raise ValueError("Each update must have 'id' and 'status' keys")

        # Update batch statuses
        old_progress, new_progress, updated_count = update_batch_statuses(
            args.file,
            updates
        )

        # Print success message
        print(f"✓ Updated {updated_count} task(s)")
        print(f"  Progress: {old_progress}% → {new_progress}%")

        # Show updated tasks
        for update in updates:
            status = update['status']
            task_id = update['id']
            print(f"  - {task_id}: {status}")

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
