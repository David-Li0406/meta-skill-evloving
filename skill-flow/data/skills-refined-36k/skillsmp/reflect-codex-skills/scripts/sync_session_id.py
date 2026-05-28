"""Copy or sync Codex session JSONL files to align session IDs with filenames.

By default this script creates a new copy with a new UUID in the filename and
updates the internal session_meta id to match. Use --sync-only to update an
existing file in place.

Example:
    python3 sync_session_id.py \
        ~/.codex/sessions/2026/01/12/rollout-2026-01-12T18-05-53-uuid.jsonl
"""

from __future__ import annotations

import argparse
from pathlib import Path

from session_io import (
    create_copy_with_new_id,
    extract_uuid_from_filename,
    sync_session_file,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Copy or sync a session JSONL file so the id matches the filename UUID."
    )
    parser.add_argument("path", type=Path, help="Path to the session JSONL file")
    parser.add_argument(
        "--sync-only",
        action="store_true",
        help="Update the file in place to match its filename UUID.",
    )
    parser.add_argument(
        "--dest-dir",
        type=Path,
        help="Directory to place the copied session file (default: source directory).",
    )
    parser.add_argument(
        "--timestamp",
        type=str,
        help="Override the timestamp portion of the new filename.",
    )
    parser.add_argument(
        "--session-id",
        type=str,
        help="Override the UUID portion of the new filename.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the sync or copy+sync operation."""
    args = parse_args()
    source_path: Path = args.path
    assert source_path.exists(), f"File not found: {source_path}"

    if args.sync_only:
        session_id = extract_uuid_from_filename(path=source_path)
        sync_session_file(path=source_path, session_id=session_id)
        print(session_id)
        return

    dest_dir = args.dest_dir or source_path.parent
    assert dest_dir.exists(), f"Destination directory not found: {dest_dir}"
    assert dest_dir.is_dir(), f"Destination is not a directory: {dest_dir}"
    dest_path = create_copy_with_new_id(
        source=source_path,
        dest_dir=dest_dir,
        timestamp=args.timestamp,
        session_id=args.session_id,
        prefix=None,
    )
    new_id = extract_uuid_from_filename(path=dest_path)
    print(dest_path)
    print(new_id)


if __name__ == "__main__":
    main()
