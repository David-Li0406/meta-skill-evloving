#!/usr/bin/env python3
"""Manage scribe log entries — write entries with automatic ID generation.

Requires Python 3.9+ (uses built-in generic types).
"""

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from common import ENTRY_ID_PATTERN, ENTRY_ID_COMMENT_PATTERN, require_scribe_dir

# Pre-compiled regex patterns for performance
HEADER_WITH_TIME_PATTERN = re.compile(r"^## (\d{2}:\d{2}) — .+$", re.MULTILINE)
HEADER_SIMPLE_PATTERN = re.compile(r"^## (.+)$", re.MULTILINE)
LOG_FILE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
TIME_FORMAT_PATTERN = re.compile(r"^\d{2}:\d{2}$")


def get_existing_ids(log_file: Path) -> set[str]:
    """Extract all entry IDs from a log file."""
    if not log_file.exists():
        return set()
    content = log_file.read_text()
    return set(ENTRY_ID_COMMENT_PATTERN.findall(content))


def generate_entry_id(log_file: Path, time_str: str) -> str:
    """Generate a unique entry ID for the given time."""
    today = datetime.now().strftime("%Y-%m-%d")
    base_id = f"{today}-{time_str.replace(':', '-')}"

    existing_ids = get_existing_ids(log_file)

    if base_id not in existing_ids:
        return base_id

    # Handle collisions with zero-padded suffix
    suffix = 2
    while f"{base_id}-{suffix:02d}" in existing_ids:
        suffix += 1

    return f"{base_id}-{suffix:02d}"


def inject_entry_id(entry: str, entry_id: str) -> str:
    """Inject the entry ID comment after the header line."""
    lines = entry.split("\n")
    result = []
    id_injected = False

    for line in lines:
        result.append(line)
        if not id_injected and HEADER_WITH_TIME_PATTERN.match(line):
            result.append(f"<!-- id: {entry_id} -->")
            id_injected = True

    if not id_injected:
        result.insert(0, f"<!-- id: {entry_id} -->")

    return "\n".join(result)


def find_latest_entry(scribe_dir: Path) -> tuple[Path, str | None, str, int, int] | None:
    """Find the latest entry across all log files.

    Returns (log_file, entry_id, entry_content, start_pos, end_pos) or None.
    """
    log_files = sorted(
        [f for f in scribe_dir.iterdir() if LOG_FILE_PATTERN.match(f.name)],
        reverse=True
    )

    if not log_files:
        return None

    for log_file in log_files:
        content = log_file.read_text()
        matches = list(HEADER_WITH_TIME_PATTERN.finditer(content))

        if not matches:
            continue

        last_match = matches[-1]
        start_pos = last_match.start()
        end_pos = len(content)
        entry_content = content[start_pos:end_pos]

        id_match = ENTRY_ID_COMMENT_PATTERN.search(entry_content)
        entry_id = id_match.group(1) if id_match else None

        return (log_file, entry_id, entry_content, start_pos, end_pos)

    return None


def delete_assets_for_entry(scribe_dir: Path, entry_id: str) -> list[str]:
    """Delete all assets associated with an entry ID."""
    assets_dir = scribe_dir / "assets"
    if not assets_dir.exists():
        return []

    deleted = []
    for asset in assets_dir.iterdir():
        if asset.name.startswith(f"{entry_id}-"):
            asset.unlink()
            deleted.append(asset.name)

    return deleted


def quick_validate(scribe_dir: Path, entry_id: str) -> list[str]:
    """Quick validation for a single entry. Returns list of errors."""
    errors = []

    # Validate ID format
    if not ENTRY_ID_PATTERN.match(entry_id):
        errors.append(f"Invalid entry ID format: {entry_id}")

    return errors


def cmd_write(args):
    """Write an entry to today's log file."""
    scribe_dir = require_scribe_dir()

    # Read entry from file or stdin
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        entry = file_path.read_text().strip()
        # Remove the temp file so next write doesn't show a diff
        file_path.unlink()
    else:
        entry = sys.stdin.read().strip()

    if not entry:
        print("Error: No entry provided (use --file or pipe via stdin)", file=sys.stderr)
        sys.exit(1)

    # Get current time
    time_str = datetime.now().strftime("%H:%M")

    # Check if entry already has time in header (legacy format)
    legacy_match = HEADER_WITH_TIME_PATTERN.search(entry)
    if legacy_match:
        time_str = legacy_match.group(1)
    else:
        header_match = HEADER_SIMPLE_PATTERN.search(entry)
        if not header_match:
            print("Error: Entry must start with '## Title'", file=sys.stderr)
            sys.exit(1)

        title = header_match.group(1)
        entry = re.sub(r"^## .+$", f"## {time_str} — {title}", entry, count=1, flags=re.MULTILINE)

    # Determine log file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = scribe_dir / f"{today}.md"

    # Generate unique entry ID
    entry_id = generate_entry_id(log_file, time_str)

    # Inject ID into entry
    entry_with_id = inject_entry_id(entry, entry_id)

    # Create log file if needed
    if not log_file.exists():
        log_file.write_text(f"# {today}\n\n---\n\n")

    # Append entry
    with open(log_file, "a") as f:
        f.write(entry_with_id)
        if not entry_with_id.endswith("\n"):
            f.write("\n")

    print(f"Entry written: {entry_id}")

    # Quick validation unless skipped
    if not args.no_validate:
        errors = quick_validate(scribe_dir, entry_id)
        if errors:
            for error in errors:
                print(f"Warning: {error}", file=sys.stderr)


def cmd_new_id(args):
    """Generate a new entry ID for the current time (or specified time)."""
    scribe_dir = require_scribe_dir()

    time_str = args.time or datetime.now().strftime("%H:%M")

    if not TIME_FORMAT_PATTERN.match(time_str):
        print(f"Error: Invalid time format: {time_str} (expected HH:MM)", file=sys.stderr)
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = scribe_dir / f"{today}.md"

    entry_id = generate_entry_id(log_file, time_str)
    print(entry_id)


def cmd_last(args):
    """Show the last entry ID from today's log."""
    scribe_dir = require_scribe_dir()

    today = datetime.now().strftime("%Y-%m-%d")
    log_file = scribe_dir / f"{today}.md"

    existing_ids = get_existing_ids(log_file)
    if not existing_ids:
        print("No entries today")
        return

    last_id = sorted(existing_ids)[-1]

    if args.with_title:
        content = log_file.read_text()
        pattern = re.compile(rf"^## (\d{{2}}:\d{{2}}) — (.+)$\n<!-- id: {re.escape(last_id)} -->", re.MULTILINE)
        match = pattern.search(content)
        if match:
            print(f"{last_id} — {match.group(2)}")
        else:
            print(last_id)
    else:
        print(last_id)


def cmd_edit_latest_show(args):
    """Display the latest entry."""
    scribe_dir = require_scribe_dir()

    result = find_latest_entry(scribe_dir)
    if not result:
        print("No entries found")
        return

    log_file, entry_id, entry_content, _, _ = result
    print(f"Latest entry from {log_file.name} (ID: {entry_id}):\n")
    print(entry_content)


def cmd_edit_latest_delete(args):
    """Delete the latest entry and its associated assets."""
    scribe_dir = require_scribe_dir()

    result = find_latest_entry(scribe_dir)
    if not result:
        print("No entries found")
        return

    log_file, entry_id, _, start_pos, _ = result

    if entry_id:
        deleted_assets = delete_assets_for_entry(scribe_dir, entry_id)
        for asset in deleted_assets:
            print(f"Deleted asset: {asset}")

    content = log_file.read_text()
    new_content = content[:start_pos].rstrip()

    if new_content and not new_content.endswith("\n"):
        new_content += "\n"

    log_file.write_text(new_content)
    print(f"Deleted entry: {entry_id}")


def cmd_edit_latest_replace(args):
    """Replace the latest entry with new content from file or stdin."""
    scribe_dir = require_scribe_dir()

    result = find_latest_entry(scribe_dir)
    if not result:
        print("No entries found")
        return

    log_file, old_entry_id, _, start_pos, _ = result

    if not old_entry_id:
        print("Error: Latest entry has no ID, cannot replace", file=sys.stderr)
        sys.exit(1)

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        new_entry = file_path.read_text().strip()
    else:
        new_entry = sys.stdin.read().strip()

    if not new_entry:
        print("Error: No entry provided (use --file or pipe via stdin)", file=sys.stderr)
        sys.exit(1)

    time_str = datetime.now().strftime("%H:%M")

    legacy_match = HEADER_WITH_TIME_PATTERN.search(new_entry)
    if legacy_match:
        time_str = legacy_match.group(1)
    else:
        header_match = HEADER_SIMPLE_PATTERN.search(new_entry)
        if not header_match:
            print("Error: Entry must start with '## Title'", file=sys.stderr)
            sys.exit(1)

        title = header_match.group(1)
        new_entry = re.sub(r"^## .+$", f"## {time_str} — {title}", new_entry, count=1, flags=re.MULTILINE)

    new_entry_with_id = inject_entry_id(new_entry, old_entry_id)

    content = log_file.read_text()
    new_content = content[:start_pos] + new_entry_with_id
    if not new_content.endswith("\n"):
        new_content += "\n"

    log_file.write_text(new_content)
    print(f"Replaced entry: {old_entry_id}")


def cmd_edit_latest_rearchive(args):
    """Re-archive a file using the latest entry's ID."""
    scribe_dir = require_scribe_dir()

    result = find_latest_entry(scribe_dir)
    if not result:
        print("No entries found")
        return

    _, entry_id, _, _, _ = result
    if not entry_id:
        print("Error: Latest entry has no ID", file=sys.stderr)
        sys.exit(1)

    src = Path(args.file)
    if not src.exists():
        print(f"Error: {args.file} not found", file=sys.stderr)
        sys.exit(1)

    assets_dir = scribe_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    dest_name = f"{entry_id}-{src.name}"
    dest = assets_dir / dest_name

    if dest.exists():
        print(f"Error: {dest_name} already exists", file=sys.stderr)
        sys.exit(1)

    shutil.copy(src, dest)
    print(f"Archived: {dest_name}")


def cmd_edit_latest_unarchive(args):
    """Delete all assets associated with the latest entry (but keep the entry)."""
    scribe_dir = require_scribe_dir()

    result = find_latest_entry(scribe_dir)
    if not result:
        print("No entries found")
        return

    _, entry_id, _, _, _ = result
    if not entry_id:
        print("Error: Latest entry has no ID", file=sys.stderr)
        sys.exit(1)

    deleted_assets = delete_assets_for_entry(scribe_dir, entry_id)

    if deleted_assets:
        for asset in deleted_assets:
            print(f"Deleted asset: {asset}")
    else:
        print(f"No assets found for entry {entry_id}")


def main():
    parser = argparse.ArgumentParser(description="Manage scribe log entries")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # write command
    write_parser = subparsers.add_parser("write", help="Write an entry (from file or stdin)")
    write_parser.add_argument("--file", help="Read entry from file instead of stdin")
    write_parser.add_argument("--no-validate", action="store_true", help="Skip validation after write")
    write_parser.set_defaults(func=cmd_write)

    # new-id command
    new_id_parser = subparsers.add_parser("new-id", help="Generate a new entry ID")
    new_id_parser.add_argument("--time", help="Time for the entry (HH:MM), defaults to now")
    new_id_parser.set_defaults(func=cmd_new_id)

    # last command
    last_parser = subparsers.add_parser("last", help="Show the last entry ID from today")
    last_parser.add_argument("--with-title", action="store_true", help="Include entry title in output")
    last_parser.set_defaults(func=cmd_last)

    # edit-latest command with subcommands
    edit_parser = subparsers.add_parser("edit-latest", help="Edit the latest entry")
    edit_subparsers = edit_parser.add_subparsers(dest="edit_command", required=True)

    edit_show = edit_subparsers.add_parser("show", help="Display the latest entry")
    edit_show.set_defaults(func=cmd_edit_latest_show)

    edit_delete = edit_subparsers.add_parser("delete", help="Delete the latest entry and its assets")
    edit_delete.set_defaults(func=cmd_edit_latest_delete)

    edit_replace = edit_subparsers.add_parser("replace", help="Replace the latest entry (from file or stdin)")
    edit_replace.add_argument("--file", help="Read entry from file instead of stdin")
    edit_replace.set_defaults(func=cmd_edit_latest_replace)

    edit_rearchive = edit_subparsers.add_parser("rearchive", help="Re-archive a file for the latest entry")
    edit_rearchive.add_argument("file", help="File to archive")
    edit_rearchive.set_defaults(func=cmd_edit_latest_rearchive)

    edit_unarchive = edit_subparsers.add_parser("unarchive", help="Delete assets for the latest entry")
    edit_unarchive.set_defaults(func=cmd_edit_latest_unarchive)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
