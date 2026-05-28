#!/usr/bin/env python3
"""
Query and manage session history.

Usage:
    python session-history.py list [--limit N]
    python session-history.py show <session_id>
    python session-history.py stats
    python session-history.py clean [--keep N]
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_history(project_root="."):
    """Load session history from file."""
    history_file = Path(project_root) / ".claude" / ".session-history.json"

    if not history_file.exists():
        return []

    try:
        with open(history_file) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Session history file is corrupted: {e}", file=sys.stderr)
        return []


def save_history(history, project_root="."):
    """Save session history to file."""
    history_file = Path(project_root) / ".claude" / ".session-history.json"
    history_file.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing file
    if history_file.exists():
        backup_file = history_file.with_suffix(".json.bak")
        history_file.rename(backup_file)

    # Write new history
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)


def format_duration(minutes):
    """Format duration in human-readable format."""
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def format_timestamp(iso_timestamp):
    """Format ISO timestamp for display."""
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    return dt.strftime("%Y-%m-%d %H:%M")


def calculate_age(iso_timestamp):
    """Calculate age of session from timestamp."""
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    now = datetime.now(dt.tzinfo)
    delta = now - dt

    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if days > 0:
        return f"{days}d ago"
    elif hours > 0:
        return f"{hours}h ago"
    else:
        return f"{minutes}m ago"


def cmd_list(history, limit=None):
    """List recent sessions."""
    if not history:
        print("No session history found.")
        return

    # Apply limit
    sessions = history[-limit:] if limit else history
    sessions.reverse()  # Most recent first

    print("═══════════════════════════════════════════════")
    print("  Session History")
    print("═══════════════════════════════════════════════")
    print("")

    for session in sessions:
        session_id = session.get("session_id", "unknown")
        timestamp = session.get("timestamp", "")
        duration = session.get("duration_minutes", 0)
        phase = session.get("phase", "Unknown")
        progress = session.get("phase_progress", 0)
        files = session.get("edited_files_count", 0)
        todos = session.get("todos_completed", 0)

        age = calculate_age(timestamp) if timestamp else "unknown"
        time_str = format_timestamp(timestamp) if timestamp else "unknown"

        print(f"Session: {session_id}")
        print(f"  Time: {time_str} ({age})")
        print(f"  Duration: {format_duration(duration)}")
        print(f"  Phase: {phase} ({progress}% complete)")
        print(f"  Activity: {files} files edited, {todos} todos completed")
        print("")


def cmd_show(history, session_id):
    """Show detailed information for a specific session."""
    # Find session
    session = next((s for s in history if s.get("session_id") == session_id), None)

    if not session:
        print(f"Error: Session {session_id} not found.", file=sys.stderr)
        return 1

    print("═══════════════════════════════════════════════")
    print(f"  Session Details: {session_id}")
    print("═══════════════════════════════════════════════")
    print("")

    # Display all fields
    timestamp = session.get("timestamp", "")
    print(f"Timestamp: {format_timestamp(timestamp)} ({calculate_age(timestamp)})")
    print(f"Duration: {format_duration(session.get('duration_minutes', 0))}")
    print("")

    phase = session.get("phase", "Unknown")
    progress = session.get("phase_progress", 0)
    print(f"Phase: {phase}")
    print(f"Progress: {progress}%")
    print("")

    files = session.get("edited_files_count", 0)
    todos = session.get("todos_completed", 0)
    print(f"Files edited: {files}")
    print(f"Todos completed: {todos}")
    print("")

    reason = session.get("checkpoint_reason", "unknown")
    print(f"Checkpoint reason: {reason}")

    git_branch = session.get("git_branch")
    if git_branch:
        commits = session.get("commits_made", 0)
        print(f"Git branch: {git_branch}")
        print(f"Commits: {commits}")

    return 0


def cmd_stats(history):
    """Display statistics across all sessions."""
    if not history:
        print("No session history found.")
        return

    print("═══════════════════════════════════════════════")
    print("  Session Statistics")
    print("═══════════════════════════════════════════════")
    print("")

    # Calculate statistics
    total_sessions = len(history)
    total_duration = sum(s.get("duration_minutes", 0) for s in history)
    total_files = sum(s.get("edited_files_count", 0) for s in history)
    total_todos = sum(s.get("todos_completed", 0) for s in history)
    total_commits = sum(s.get("commits_made", 0) for s in history)

    avg_duration = total_duration / total_sessions if total_sessions > 0 else 0
    avg_files = total_files / total_sessions if total_sessions > 0 else 0

    print(f"Total sessions: {total_sessions}")
    print(f"Total time: {format_duration(total_duration)}")
    print(f"Average session: {format_duration(int(avg_duration))}")
    print("")

    print(f"Files edited: {total_files} ({avg_files:.1f} per session)")
    print(f"Todos completed: {total_todos}")
    print(f"Commits made: {total_commits}")
    print("")

    # Phase breakdown
    phase_counts = defaultdict(int)
    for session in history:
        phase = session.get("phase", "Unknown")
        phase_counts[phase] += 1

    print("Sessions by phase:")
    for phase, count in sorted(phase_counts.items(), key=lambda x: -x[1]):
        print(f"  • {phase}: {count}")
    print("")

    # Checkpoint reasons
    reason_counts = defaultdict(int)
    for session in history:
        reason = session.get("checkpoint_reason", "unknown")
        reason_counts[reason] += 1

    print("Checkpoint reasons:")
    for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1]):
        print(f"  • {reason}: {count}")


def cmd_clean(history, keep=30):
    """Clean old sessions, keeping only the most recent N."""
    if not history:
        print("No session history to clean.")
        return 0

    original_count = len(history)

    if original_count <= keep:
        print(f"Session history has {original_count} entries. Nothing to clean.")
        return 0

    # Keep only most recent N
    cleaned_history = history[-keep:]

    # Save cleaned history
    save_history(cleaned_history)

    removed = original_count - len(cleaned_history)
    print(f"Removed {removed} old sessions. Kept {len(cleaned_history)} most recent.")
    return 0


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: session-history.py <command> [options]")
        print("")
        print("Commands:")
        print("  list [--limit N]     List recent sessions")
        print("  show <session_id>    Show detailed session info")
        print("  stats                Display statistics")
        print("  clean [--keep N]     Remove old sessions (default: keep 30)")
        sys.exit(1)

    command = sys.argv[1]

    # Load history
    history = load_history()

    # Execute command
    if command == "list":
        limit = None
        if len(sys.argv) > 2 and sys.argv[2] == "--limit":
            limit = int(sys.argv[3])
        cmd_list(history, limit)

    elif command == "show":
        if len(sys.argv) < 3:
            print("Error: session_id required", file=sys.stderr)
            sys.exit(1)
        session_id = sys.argv[2]
        sys.exit(cmd_show(history, session_id))

    elif command == "stats":
        cmd_stats(history)

    elif command == "clean":
        keep = 30
        if len(sys.argv) > 2 and sys.argv[2] == "--keep":
            keep = int(sys.argv[3])
        sys.exit(cmd_clean(history, keep))

    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
