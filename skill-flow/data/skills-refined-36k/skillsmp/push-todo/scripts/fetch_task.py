#!/usr/bin/env python3
"""
Fetch and display active Push tasks.
Version: 4.2.0 (completion comment support)

This script retrieves active tasks from the Push iOS app and outputs them
in a format suitable for Claude Code to process.

## Unified Hub Architecture (v3.0 - 2026-01-16)

Uses the synced-todos endpoint ONLY (normalized tables: todos + todo_actions).
The legacy claude-tasks endpoint has been removed.

Tasks become visible when:
1. User assigns a Claude Code action to a todo in Push
2. Action has completionBehavior = .automatic (auto-sync enabled)
3. Todo syncs to Supabase via sync-push with sync_enabled = true
4. CLI queries synced-todos which filters by sync_enabled

## Project Scoping (Default)
By default, only tasks for the CURRENT PROJECT are shown (based on git remote).
Use --all-projects to see tasks from all projects.

Usage:
    python fetch_task.py [TASK_NUMBER] [--all-projects] [--pinned] [--mark-completed TASK_ID]

Arguments:
    TASK_NUMBER        Optional task number to fetch directly (e.g., 5 or #5)

Options:
    --all-projects     Fetch tasks from ALL projects (not just current)
    --pinned           Only show pinned (focused) tasks, or prioritize them at the top
    --mark-completed ID Mark a task as completed (syncs back to Push)
    --completion-comment TEXT  Comment to include when marking completed (appears in Push timeline)
    --json             Output raw JSON

Environment:
    PUSH_API_KEY: API key for Push authentication (required)

Output format (JSON):
    {
        "tasks": [
            {
                "id": "uuid",
                "display_number": "Human-readable number (#1, #2, #3...)",
                "summary": "Task summary",
                "content": "Full task content",
                "transcript": "Optional voice transcript",
                "project_hint": "Optional project hint",
                "git_remote": "Optional git remote for project scoping",
                "is_focused": "Boolean indicating if task is pinned",
                "created_at": "ISO timestamp"
            }
        ]
    }

See: /docs/20260116_unified_hub_action_execution_architecture.md
     /docs/20260116_unified_hub_gap_analysis.md
"""

import os
import sys
import json
import argparse
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List

# Configuration
API_BASE_URL = "https://jxuzqcbqhiaxmfitzxlo.supabase.co/functions/v1"


def get_git_remote() -> Optional[str]:
    """
    Get the normalized git remote URL for the current directory.

    Returns:
        Normalized git remote (e.g., "github.com/user/repo") or None if not a git repo.
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode != 0:
            return None

        url = result.stdout.strip()
        if not url:
            return None

        # Normalize: remove protocol, convert : to /, remove .git
        # git@github.com:user/repo.git → github.com/user/repo
        # https://github.com/user/repo.git → github.com/user/repo

        # Remove protocol prefixes
        for prefix in ["https://", "http://", "git@", "ssh://git@"]:
            if url.startswith(prefix):
                url = url[len(prefix):]
                break

        # Convert : to / (for git@ style)
        if ":" in url and "://" not in url:
            url = url.replace(":", "/", 1)

        # Remove .git suffix
        if url.endswith(".git"):
            url = url[:-4]

        return url
    except Exception:
        return None


def get_api_key() -> str:
    """
    Get API key from config file or environment.

    Priority:
    1. Environment variable (for CI/testing)
    2. Config file at ~/.config/push/config (production)
    3. Error with helpful message

    Returns:
        The API key string.

    Raises:
        ValueError: If API key is not found in either location.
    """
    # 1. Try environment first (for CI/testing, backward compatibility)
    key = os.environ.get("PUSH_API_KEY")
    if key:
        return key

    # 2. Read from config file (production - more reliable)
    config_path = Path.home() / ".config" / "push" / "config"
    if config_path.exists():
        try:
            # Parse bash-style config (export VAR="value")
            for line in config_path.read_text().splitlines():
                line = line.strip()
                if line.startswith("export PUSH_API_KEY="):
                    # Extract value after = and remove quotes
                    value = line.split("=", 1)[1].strip()
                    # Remove surrounding quotes if present
                    key = value.strip('"').strip("'")
                    if key:
                        return key
        except Exception:
            # Config file exists but couldn't parse - fall through to error
            pass

    # 3. Not found - provide helpful error message
    raise ValueError(
        "PUSH_API_KEY not configured.\n"
        "Run: /push-todo connect\n"
        "Or manually add to ~/.config/push/config:\n"
        '  export PUSH_API_KEY="your-key-here"'
    )


def fetch_tasks_from_api(git_remote: Optional[str] = None) -> List:
    """
    Fetch active tasks from the synced-todos endpoint.

    Uses the unified hub architecture - all tasks come from the normalized
    tables (todos + todo_actions with sync_enabled=true).

    Args:
        git_remote: If provided, only fetch tasks for this project.
                   The endpoint looks up the action_id from cli_action_registrations.
                   If None, fetches ALL synced tasks across all projects.

    Returns:
        List of tasks for this project, or all synced tasks if no git_remote.
    """
    api_key = get_api_key()

    # Build URL - with git_remote for project-scoped, without for all projects
    if git_remote:
        encoded_remote = urllib.parse.quote(git_remote, safe="")
        url = f"{API_BASE_URL}/synced-todos?git_remote={encoded_remote}"
    else:
        # No git_remote = fetch ALL synced tasks (for --all-projects)
        url = f"{API_BASE_URL}/synced-todos"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            # Convert synced-todos response format to match expected format
            todos = data.get("todos", [])
            return [
                {
                    "id": t.get("id"),
                    "display_number": t.get("displayNumber"),  # Human-readable #1, #2, #3...
                    "summary": t.get("summary") or t.get("title", "No summary"),
                    "content": t.get("normalizedContent") or t.get("summary") or "",
                    "transcript": t.get("originalTranscript"),
                    "project_hint": None,  # Not included in synced-todos response
                    "git_remote": git_remote,  # Store for reference (may be None for all-projects)
                    "is_focused": t.get("isFocused", False),  # Pinned status
                    "created_at": t.get("createdAt"),
                }
                for t in todos
            ]
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise ValueError("Invalid API key. Run '/push-todo connect' to configure.")
        if e.code == 404:
            # No action registered for this project
            return []
        raise
    except urllib.error.URLError as e:
        raise ValueError(f"Network error: {e.reason}")


def get_tasks(git_remote: Optional[str] = None) -> List:
    """
    Get tasks - always fetches fresh from API.

    Args:
        git_remote: If provided, fetch tasks for this project only.
                   If None, fetch ALL synced tasks across all projects.

    Returns:
        List of tasks from the synced-todos endpoint.

    Version 4.0: Removed caching - always returns fresh data from Supabase.
    """
    return fetch_tasks_from_api(git_remote)


def fetch_task_by_number(display_number: int) -> Optional[dict]:
    """
    Fetch a specific task by its display number (direct lookup).

    This is the fast path - goes directly to the API with display_number
    query param, bypassing project filtering.

    Args:
        display_number: The global task number (e.g., 427)

    Returns:
        Task dict if found, None if not found.
    """
    api_key = get_api_key()
    url = f"{API_BASE_URL}/synced-todos?display_number={display_number}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            todos = data.get("todos", [])
            if not todos:
                return None
            t = todos[0]
            return {
                "id": t.get("id"),
                "display_number": t.get("displayNumber"),
                "summary": t.get("summary") or t.get("title", "No summary"),
                "content": t.get("normalizedContent") or t.get("summary") or "",
                "transcript": t.get("originalTranscript"),
                "project_hint": None,
                "git_remote": None,
                "is_focused": t.get("isFocused", False),
                "created_at": t.get("createdAt"),
            }
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise ValueError("Invalid API key. Run '/push-todo connect' to configure.")
        if e.code == 404:
            return None
        raise
    except urllib.error.URLError as e:
        raise ValueError(f"Network error: {e.reason}")


def mark_task_completed(task_id: str, comment: Optional[str] = None) -> bool:
    """
    Mark a task as completed using the todo-status endpoint.

    This syncs the completion back to the Push iOS app via the unified hub.
    Optionally includes a completion comment that appears in the task's timeline.

    Args:
        task_id: The UUID of the todo to mark as completed.
        comment: Optional completion comment (summary of work done).

    Returns:
        True if successful, False otherwise.
    """
    api_key = get_api_key()
    url = f"{API_BASE_URL}/todo-status"

    payload = {
        "todoId": task_id,
        "isCompleted": True,
        "completedAt": datetime.now(timezone.utc).isoformat()
    }

    # Add completion comment if provided (appears in Push app timeline)
    if comment:
        payload["completionComment"] = comment

    body = json.dumps(payload).encode()

    req = urllib.request.Request(url, data=body, method="PATCH")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status == 200
    except urllib.error.HTTPError:
        return False
    except urllib.error.URLError:
        return False


def format_task_for_display(task: dict) -> str:
    """Format a task for human-readable display."""
    lines = []

    # Build task header with display number and pinned indicator
    display_num = task.get("display_number")
    pinned_prefix = "📌 " if task.get("is_focused") else ""
    num_prefix = f"#{display_num} " if display_num else ""
    lines.append(f"## Task: {num_prefix}{pinned_prefix}{task.get('summary', 'No summary')}")
    lines.append("")

    if task.get("project_hint"):
        lines.append(f"**Project:** {task['project_hint']}")
        lines.append("")

    lines.append("### Content")
    lines.append(task.get("content", "No content"))
    lines.append("")

    if task.get("transcript"):
        lines.append("### Original Voice Transcript")
        lines.append(f"> {task['transcript']}")
        lines.append("")

    lines.append(f"**Task ID:** `{task.get('id', 'unknown')}`")
    if display_num:
        lines.append(f"**Display Number:** #{display_num}")
    lines.append(f"**Created:** {task.get('created_at', 'unknown')}")

    return "\n".join(lines)


def parse_task_number(value: str) -> Optional[int]:
    """
    Parse task number from string, handling both '5' and '#5' formats.

    Returns:
        The integer task number, or None if not a valid format.
    """
    if not value:
        return None
    # Strip leading '#' if present
    cleaned = value.lstrip("#")
    try:
        num = int(cleaned)
        return num if num > 0 else None
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Fetch active Push tasks")
    parser.add_argument("task_number", nargs="?", default=None, help="Task number to fetch directly (e.g., 5 or #5)")
    parser.add_argument("--all-projects", action="store_true", help="Fetch tasks from ALL projects (not just current)")
    parser.add_argument("--pinned", action="store_true", help="Only show pinned tasks, or prioritize them at the top")
    parser.add_argument("--mark-completed", metavar="ID", help="Mark a task as completed")
    parser.add_argument("--completion-comment", metavar="TEXT", help="Comment to include when marking task completed (appears in Push app timeline)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    try:
        # Handle mark-completed
        if args.mark_completed:
            success = mark_task_completed(args.mark_completed, args.completion_comment)
            if success:
                print(f"Task {args.mark_completed} marked as completed")
                if args.completion_comment:
                    print(f"Completion note: {args.completion_comment[:100]}{'...' if len(args.completion_comment) > 100 else ''}")
            else:
                print(f"Failed to mark task {args.mark_completed} as completed", file=sys.stderr)
                sys.exit(1)
            return

        # Handle direct task number lookup (fast path)
        if args.task_number:
            display_num = parse_task_number(args.task_number)
            if display_num is None:
                print(f"Invalid task number: {args.task_number}", file=sys.stderr)
                sys.exit(1)

            task = fetch_task_by_number(display_num)
            if not task:
                print(f"Task #{display_num} not found (may be completed or deleted).")
                sys.exit(0)

            if args.json:
                print(json.dumps({"tasks": [task]}, indent=2))
            else:
                print(f"# Task #{display_num} from Push\n")
                print(format_task_for_display(task))
            sys.exit(0)

        # Determine project filter
        # By default, scope to current project (git remote)
        # Use --all-projects to disable project filtering
        git_remote = None if args.all_projects else get_git_remote()

        # Fetch tasks (always fresh from API)
        tasks = get_tasks(git_remote=git_remote)

        # Handle --pinned flag: filter to only pinned tasks, or sort pinned first
        if args.pinned:
            pinned_tasks = [t for t in tasks if t.get("is_focused")]
            if pinned_tasks:
                # If there are pinned tasks, show only those
                tasks = pinned_tasks
            # If no pinned tasks, fall through to show all (with pinned sorted first)
            else:
                # Sort to put any pinned tasks first (in case of future additions)
                tasks = sorted(tasks, key=lambda t: (not t.get("is_focused", False)))
        else:
            # Always sort pinned tasks first, even without --pinned flag
            tasks = sorted(tasks, key=lambda t: (not t.get("is_focused", False)))

        # Filter out tasks without display_number (required for predictable identification)
        valid_tasks = [t for t in tasks if t.get("display_number")]
        invalid_count = len(tasks) - len(valid_tasks)
        if invalid_count > 0:
            print(f"Warning: {invalid_count} task(s) missing display_number (skipped)", file=sys.stderr)
        tasks = valid_tasks

        if not tasks:
            if args.pinned:
                print("No pinned tasks found.")
            elif git_remote:
                print(f"No active tasks for this project.")
            else:
                print("No active tasks from Push.")
            sys.exit(0)

        # Output - always use global display_number (#N format)
        if args.json:
            print(json.dumps({"tasks": tasks}, indent=2))
        else:
            # Show all tasks for current project (default behavior)
            scope = "this project" if git_remote else "all projects"
            pinned_suffix = ", pinned only" if args.pinned else ""
            print(f"# {len(tasks)} Active Tasks ({scope}{pinned_suffix})\n")
            for task in tasks:
                display_num = task.get("display_number")
                print(f"---\n### #{display_num}\n")
                print(format_task_for_display(task))
                print()

        sys.exit(0)

    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
