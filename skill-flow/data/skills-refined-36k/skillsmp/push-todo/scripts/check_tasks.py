#!/usr/bin/env python3
"""
Check active Push tasks count for the current project.

This script is called by the session-start hook to show the user
how many active tasks they have in Push. Outputs just the count.

## Unified Hub Architecture (2026-01-16)

Uses the synced-todos endpoint (normalized tables) instead of the legacy
claude-tasks endpoint (pending_claude_tasks table).

Tasks are scoped to the current project (git remote). If not in a git repo,
returns 0 tasks since we can't determine which action's tasks to show.

See: /docs/20260116_unified_hub_action_execution_architecture.md
     /docs/20260116_unified_hub_gap_analysis.md

Usage:
    python check_tasks.py

Environment:
    PUSH_API_KEY: API key for Push authentication (required)

Exit codes:
    0: Success (count printed to stdout)
    1: Error (error message printed to stderr)
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Optional

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


def fetch_tasks(git_remote: str) -> list:
    """
    Fetch active tasks from the synced-todos endpoint.

    Args:
        git_remote: Normalized git remote URL for project filtering.

    Returns:
        List of tasks for this project.
    """
    api_key = get_api_key()

    # Build URL with git_remote parameter
    encoded_remote = urllib.parse.quote(git_remote, safe="")
    url = f"{API_BASE_URL}/synced-todos?git_remote={encoded_remote}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            # Convert synced-todos response format to cache format
            todos = data.get("todos", [])
            return [
                {
                    "id": t.get("id"),
                    "summary": t.get("summary") or t.get("title", "No summary"),
                    "content": t.get("normalizedContent") or t.get("summary") or "",
                    "transcript": t.get("originalTranscript"),
                    "project_hint": None,
                    "git_remote": git_remote,  # Store for reference
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


def main():
    try:
        # Get git remote for project scoping
        git_remote = get_git_remote()

        if not git_remote:
            # Not in a git repo - can't determine which project's tasks to show
            print(0)
            sys.exit(0)

        # Fetch tasks for this project
        tasks = fetch_tasks(git_remote)

        # Output count (for session-start hook)
        print(len(tasks))
        sys.exit(0)

    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
