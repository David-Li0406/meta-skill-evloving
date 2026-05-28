#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the ios-tuist-bootstrap template files into a destination repo."
    )
    parser.add_argument("--dest", required=True, help="Destination project root.")
    parser.add_argument("--project-name", required=True, help="Project/app name.")
    parser.add_argument(
        "--scheme",
        help="Scheme name (defaults to project name).",
    )
    parser.add_argument(
        "--workspace",
        help="Workspace name (defaults to '<project-name>.xcworkspace').",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files instead of skipping them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dest_root = Path(args.dest).expanduser().resolve()
    project_name = args.project_name
    scheme = args.scheme or project_name
    workspace = args.workspace or f"{project_name}.xcworkspace"

    script_root = Path(__file__).resolve().parent
    template_root = script_root.parent / "assets" / "template"

    if not template_root.exists():
        print(f"Template directory not found: {template_root}", file=sys.stderr)
        return 1

    if not dest_root.exists():
        print(f"Destination does not exist: {dest_root}", file=sys.stderr)
        return 1

    replacements = {
        "{{PROJECT_NAME}}": project_name,
        "{{SCHEME_NAME}}": scheme,
        "{{WORKSPACE_NAME}}": workspace,
    }

    for src in template_root.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(template_root)
        dest = dest_root / rel

        if dest.exists() and not args.force:
            print(f"Skip existing: {dest}")
            continue

        if args.dry_run:
            print(f"Would copy: {src} -> {dest}")
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        data = src.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            shutil.copy2(src, dest)
            continue

        for needle, value in replacements.items():
            text = text.replace(needle, value)

        dest.write_text(text, encoding="utf-8")
        os.chmod(dest, src.stat().st_mode)
        print(f"Copied: {src} -> {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
