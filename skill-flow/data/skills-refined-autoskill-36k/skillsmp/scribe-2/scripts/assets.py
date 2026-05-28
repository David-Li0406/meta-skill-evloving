#!/usr/bin/env python3
"""Manage scribe assets — archive and restore files.

Requires Python 3.9+ (uses built-in generic types).
"""

import argparse
import shutil
import sys
from pathlib import Path

from common import ENTRY_ID_PATTERN, require_scribe_dir


def cmd_save(args):
    """Archive files to .scribe/assets/"""
    if not ENTRY_ID_PATTERN.match(args.entry_id):
        print(f"Error: Invalid entry ID format: {args.entry_id}", file=sys.stderr)
        print("Expected format: YYYY-MM-DD-HH-MM (e.g., 2026-01-23-14-35)", file=sys.stderr)
        sys.exit(1)

    scribe_dir = require_scribe_dir()

    assets_dir = scribe_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    for filepath in args.files:
        src = Path(filepath)
        if not src.exists():
            print(f"Error: {filepath} not found", file=sys.stderr)
            sys.exit(1)

        dest_name = f"{args.entry_id}-{src.name}"
        dest = assets_dir / dest_name
        
        if dest.exists():
            print(f"Error: {dest_name} already exists, not overwriting", file=sys.stderr)
            sys.exit(1)
        
        shutil.copy(src, dest)
        print(f"Archived: {dest_name}")


def cmd_get(args):
    """Restore an archived file to the project directory."""
    scribe_dir = require_scribe_dir()

    assets_dir = scribe_dir / "assets"
    src = assets_dir / args.asset

    if not src.exists():
        print(f"Error: {args.asset} not found in assets", file=sys.stderr)
        sys.exit(1)

    dest_dir = Path(args.dest)
    dest_name = f"_{args.asset}"
    dest = dest_dir / dest_name

    if dest.exists():
        print(f"Error: {dest} already exists, not overwriting", file=sys.stderr)
        sys.exit(1)

    shutil.copy(src, dest)
    print(f"Restored: {dest}")


def cmd_list(args):
    """List archived assets."""
    scribe_dir = require_scribe_dir()

    assets_dir = scribe_dir / "assets"
    if not assets_dir.exists():
        print("No assets directory")
        return

    assets = sorted(assets_dir.iterdir())
    if not assets:
        print("No assets archived")
        return

    matched = False
    for asset in assets:
        # Apply filter if provided
        if args.filter and args.filter.lower() not in asset.name.lower():
            continue
        print(asset.name)
        matched = True
    
    if args.filter and not matched:
        print(f"No assets matching '{args.filter}'")


def main():
    parser = argparse.ArgumentParser(description="Manage scribe assets")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # save command
    save_parser = subparsers.add_parser("save", help="Archive files to assets")
    save_parser.add_argument("entry_id", help="Entry ID (e.g., 2026-01-23-14-35)")
    save_parser.add_argument("files", nargs="+", help="Files to archive")
    save_parser.set_defaults(func=cmd_save)

    # get command
    get_parser = subparsers.add_parser("get", help="Restore an archived file")
    get_parser.add_argument("asset", help="Asset filename")
    get_parser.add_argument("--dest", default=".", help="Destination directory")
    get_parser.set_defaults(func=cmd_get)

    # list command
    list_parser = subparsers.add_parser("list", help="List archived assets")
    list_parser.add_argument("filter", nargs="?", help="Filter by filename or date (e.g., '2026-01-23' or 'etl')")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
