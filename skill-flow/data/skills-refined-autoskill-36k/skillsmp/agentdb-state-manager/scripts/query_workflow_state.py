#!/usr/bin/env python3
"""Query current workflow phase from AgentDB.

This script queries the AgentDB database to determine the current workflow
phase based on the most recent synchronization record. Useful for the
/workflow/all orchestrator to detect and continue from the current state.

Usage:
    python query_workflow_state.py
    python query_workflow_state.py --format json
    python query_workflow_state.py --worktree /path/to/worktree

Created: 2025-11-23
Feature: 008-workflow-skill-integration
"""

import argparse
import json
import subprocess
from pathlib import Path

# Phase mapping from pattern to phase number and name
PHASE_MAP = {
    "phase_1_specify": (1, "specify", "/2_plan"),
    "phase_2_plan": (2, "plan", "/3_tasks"),
    "phase_3_tasks": (3, "tasks", "/4_implement"),
    "phase_4_implement": (4, "implement", "/5_integrate"),
    "phase_5_integrate": (5, "integrate", "/6_release"),
    "phase_6_release": (6, "release", "/7_backmerge"),
    "phase_7_backmerge": (7, "backmerge", None),
}


def get_worktree_path() -> str | None:
    """Detect current worktree path if in a worktree.

    Returns:
        Worktree path or None if in main repo
    """
    try:
        # Get git toplevel
        toplevel = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE).strip()

        # Get current directory
        cwd = str(Path.cwd())

        # If different, we're in a worktree
        if cwd != toplevel:
            return cwd
        return None
    except subprocess.CalledProcessError:
        return None


def get_database_path() -> Path | None:
    """Get path to AgentDB database.

    Returns:
        Path to agentdb.duckdb or None if not found
    """
    cwd = Path.cwd()

    # Check current directory
    state_dir = cwd / ".claude-state"
    if (state_dir / "agentdb.duckdb").exists():
        return state_dir / "agentdb.duckdb"

    # Check parent (if in worktree)
    parent_state = cwd.parent / ".claude-state"
    if (parent_state / "agentdb.duckdb").exists():
        return parent_state / "agentdb.duckdb"

    return None


def query_latest_sync(db_path: Path, worktree: str | None = None) -> dict | None:
    """Query the latest sync record for a worktree.

    Args:
        db_path: Path to database file
        worktree: Worktree path filter (None for main repo syncs)

    Returns:
        Dict with sync record or None if not found
    """
    # Build WHERE clause
    if worktree:
        where = f"WHERE worktree_path = '{worktree}'"
    else:
        where = "WHERE worktree_path IS NULL"

    sql = f"""
    SELECT
        sync_id,
        worktree_path,
        sync_type,
        pattern,
        status,
        created_at,
        source_location,
        target_location
    FROM agent_synchronizations
    {where}
    ORDER BY created_at DESC
    LIMIT 1;
    """

    try:
        import duckdb

        conn = duckdb.connect(str(db_path), read_only=True)
        result = conn.execute(sql).fetchone()
        conn.close()

        if result:
            return {
                "sync_id": result[0],
                "worktree_path": result[1],
                "sync_type": result[2],
                "pattern": result[3],
                "status": result[4],
                "created_at": result[5].isoformat() if result[5] else None,
                "source_location": result[6],
                "target_location": result[7],
            }
        return None

    except ImportError:
        # Fallback to CLI
        result = subprocess.run(["duckdb", str(db_path), "-json", "-c", sql], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if data:
                return data[0]
        return None
    except Exception:
        return None


def get_workflow_state(worktree: str | None = None) -> dict:
    """Get current workflow state.

    Args:
        worktree: Worktree path (auto-detected if None)

    Returns:
        Dict with workflow state information
    """
    # Auto-detect worktree
    if worktree is None:
        worktree = get_worktree_path()

    # Get database path
    db_path = get_database_path()

    if db_path is None:
        return {
            "error": "No AgentDB found",
            "worktree": worktree,
            "phase": None,
            "phase_name": None,
            "next_command": "/1_specify",
        }

    # Query latest sync
    sync = query_latest_sync(db_path, worktree)

    if sync is None:
        return {
            "worktree": worktree,
            "phase": 0,
            "phase_name": "not_started",
            "last_sync": None,
            "pattern": None,
            "next_command": "/1_specify",
        }

    # Parse phase from pattern
    pattern = sync.get("pattern", "")
    phase_info = PHASE_MAP.get(pattern, (0, "unknown", None))

    return {
        "worktree": worktree,
        "phase": phase_info[0],
        "phase_name": phase_info[1],
        "last_sync": sync.get("created_at"),
        "pattern": pattern,
        "next_command": phase_info[2],
        "sync_id": sync.get("sync_id"),
    }


def format_text(state: dict) -> str:
    """Format state as human-readable text.

    Args:
        state: Workflow state dict

    Returns:
        Formatted string
    """
    lines = ["Current Workflow State:"]

    if state.get("error"):
        lines.append(f"  Error: {state['error']}")
        lines.append("  Suggestion: Run /1_specify to start a new feature")
        return "\n".join(lines)

    if state.get("worktree"):
        lines.append(f"  Worktree: {state['worktree']}")
    else:
        lines.append("  Location: Main repository")

    lines.append(f"  Phase: {state['phase']} ({state['phase_name']})")

    if state.get("last_sync"):
        lines.append(f"  Last Sync: {state['last_sync']}")

    if state.get("pattern"):
        lines.append(f"  Pattern: {state['pattern']}")

    if state.get("next_command"):
        lines.append(f"  Next: {state['next_command']}")
    else:
        lines.append("  Next: Workflow complete")

    return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Query current workflow phase from AgentDB",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query state (auto-detect worktree)
  python query_workflow_state.py

  # Query state as JSON
  python query_workflow_state.py --format json

  # Query specific worktree
  python query_workflow_state.py --worktree /path/to/worktree
""",
    )

    parser.add_argument("--worktree", default=None, help="Worktree path (auto-detected if not provided)")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format (default: text)")

    args = parser.parse_args()

    # Get state
    state = get_workflow_state(args.worktree)

    # Output
    if args.format == "json":
        print(json.dumps(state, indent=2))
    else:
        print(format_text(state))


if __name__ == "__main__":
    main()
