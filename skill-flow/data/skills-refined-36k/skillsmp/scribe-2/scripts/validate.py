#!/usr/bin/env python3
"""Validate scribe entries for consistency.

Requires Python 3.9+ (uses built-in generic types).
"""

import argparse
import re
import sys
from pathlib import Path

from common import ENTRY_ID_PATTERN, find_scribe_dir

# Pre-compiled regex patterns for performance
HEADER_PATTERN = re.compile(r"^## (\d{2}:\d{2}) — (.+)$", re.MULTILINE)
ID_PATTERN = re.compile(r"<!-- id: ([\d-]+) -->")
ARCHIVE_PATTERN = re.compile(r"\[`([^`]+)`\]\(assets/([^)]+)\)")
RELATED_SECTION_PATTERN = re.compile(r"\*\*Related:\*\*(.+?)(?=\n\n|\n\*\*|\n---|\Z)", re.DOTALL)
RELATED_ID_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}(?:-\d{2,})?)")
LOG_FILE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


def extract_entries(log_file: Path) -> list[dict]:
    """Extract entries from a daily log file."""
    content = log_file.read_text()
    entries = []

    parts = HEADER_PATTERN.split(content)

    for i in range(1, len(parts), 3):
        if i + 2 >= len(parts):
            break
        time = parts[i]
        title = parts[i + 1]
        body = parts[i + 2] if i + 2 < len(parts) else ""

        id_match = ID_PATTERN.search(body)
        entry_id = id_match.group(1) if id_match else None

        archived = ARCHIVE_PATTERN.findall(body)

        related = []
        related_section_match = RELATED_SECTION_PATTERN.search(body)
        if related_section_match:
            related_text = related_section_match.group(1)
            related = RELATED_ID_PATTERN.findall(related_text)

        entries.append({
            "file": log_file.name,
            "time": time,
            "title": title,
            "id": entry_id,
            "archived": archived,
            "related": related,
        })

    return entries


def validate(scribe_dir: Path, since_id: str | None = None) -> tuple[list[str], int]:
    """Validate entries and return (errors, entry_count).

    If since_id is provided, only validate entries after that ID (incremental).
    """
    errors = []
    assets_dir = scribe_dir / "assets"

    log_files = [f for f in scribe_dir.iterdir() if LOG_FILE_PATTERN.match(f.name)]

    # For incremental validation, filter to relevant files
    if since_id:
        since_date = since_id[:10]  # YYYY-MM-DD portion
        log_files = [f for f in log_files if f.stem >= since_date]

    all_entries = []

    for log_file in sorted(log_files):
        entries = extract_entries(log_file)

        # For incremental, filter entries
        if since_id:
            entries = [e for e in entries if e["id"] and e["id"] > since_id]

        all_entries.extend(entries)

        for entry in entries:
            if not entry["id"]:
                errors.append(
                    f"✗ {log_file.name} [{entry['time']}] \"{entry['title']}\" — missing entry ID"
                )
            elif not ENTRY_ID_PATTERN.match(entry["id"]):
                errors.append(
                    f"✗ {log_file.name} [{entry['time']}] — invalid entry ID format: {entry['id']}"
                )

            for _, asset_path in entry["archived"]:
                asset_file = assets_dir / asset_path
                if not asset_file.exists():
                    errors.append(
                        f"✗ {log_file.name} [{entry['time']}] — references {asset_path} but file not found"
                    )

    # For full validation, also check Related references and orphaned assets
    if not since_id:
        all_entry_ids = {entry["id"] for entry in all_entries if entry["id"]}

        for entry in all_entries:
            for related_id in entry.get("related", []):
                if related_id not in all_entry_ids:
                    errors.append(
                        f"✗ {entry['file']} [{entry['time']}] — Related references {related_id} but entry not found"
                    )

        if assets_dir.exists():
            referenced_assets = set()
            for entry in all_entries:
                for _, asset_path in entry["archived"]:
                    referenced_assets.add(asset_path)

            for asset_file in assets_dir.iterdir():
                if asset_file.name not in referenced_assets:
                    errors.append(
                        f"✗ Orphaned asset: {asset_file.name} — no entry references it"
                    )

    return errors, len(all_entries)


def main():
    parser = argparse.ArgumentParser(description="Validate scribe entries")
    parser.add_argument("--since", help="Only validate entries after this ID (incremental)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Only output errors")
    args = parser.parse_args()

    scribe_dir = find_scribe_dir()

    if not scribe_dir or not scribe_dir.exists():
        print("Error: .scribe directory not found", file=sys.stderr)
        sys.exit(1)

    errors, entry_count = validate(scribe_dir, since_id=args.since)

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    elif not args.quiet:
        if args.since:
            print(f"✓ {entry_count} new entries validated (since {args.since})")
        else:
            print(f"✓ {entry_count} entries validated")
    sys.exit(0)


if __name__ == "__main__":
    main()
