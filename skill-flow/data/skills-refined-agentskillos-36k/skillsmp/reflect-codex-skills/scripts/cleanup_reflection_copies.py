"""Remove reflection copy session files prefixed for self-reflection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from session_io import discover_session_files, is_reflection_copy, read_lines

DEFAULT_SESSIONS_ROOT = Path.home() / ".codex" / "sessions"
DEFAULT_PREFIX = "[SELF-REFLECTION] "


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed CLI arguments.

    Example:
        args = parse_args()
    """
    parser = argparse.ArgumentParser(
        description="Remove reflection copy session files prefixed for self-reflection."
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=DEFAULT_SESSIONS_ROOT,
        help="Root directory containing Codex session JSONL files.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_PREFIX,
        help="Prefix marking reflection copies.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="-",
        help="Output path for results, or '-' for stdout.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List reflection copies without deleting them.",
    )
    return parser.parse_args()


def cleanup_reflection_copies(
    *, sessions_root: Path, prefix: str, dry_run: bool
) -> list[Path]:
    """Remove reflection copy files under the sessions root.

    Args:
        sessions_root: Root directory containing session files.
        prefix: Prefix marking reflection copies.
        dry_run: Whether to skip deletions.

    Returns:
        List of reflection copy paths that were removed or would be removed.

    Example:
        removed = cleanup_reflection_copies(
            sessions_root=Path("~/.codex/sessions").expanduser(),
            prefix="[SELF-REFLECTION] ",
            dry_run=False,
        )
    """
    removed: list[Path] = []
    for path in discover_session_files(root=sessions_root):
        lines = read_lines(path=path)
        if not is_reflection_copy(lines=lines, prefix=prefix):
            continue
        removed.append(path)
        if not dry_run:
            path.unlink()
    return removed


def build_payload(*, removed: list[Path], dry_run: bool) -> dict[str, Any]:
    """Build the output payload for cleanup results.

    Args:
        removed: Removed or matched paths.
        dry_run: Whether the run was a dry run.

    Returns:
        JSON-serializable payload.
    """
    return {
        "dry_run": dry_run,
        "removed_count": len(removed),
        "removed_paths": [str(path) for path in removed],
    }


def write_output(*, payload: dict[str, Any], output: str) -> None:
    """Write cleanup output to a file or stdout.

    Args:
        payload: Output payload to write.
        output: Output path or '-' for stdout.
    """
    rendered = json.dumps(payload, indent=2, ensure_ascii=True)
    if output == "-":
        print(rendered)
        return
    Path(output).write_text(rendered + "\n")


def main() -> None:
    """Run cleanup for reflection copy files."""
    args = parse_args()
    removed = cleanup_reflection_copies(
        sessions_root=args.sessions_root.expanduser(),
        prefix=args.prefix,
        dry_run=args.dry_run,
    )
    payload = build_payload(removed=removed, dry_run=args.dry_run)
    write_output(payload=payload, output=args.output)


if __name__ == "__main__":
    main()
