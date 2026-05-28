#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as _dt
import shutil
import sys
from pathlib import Path

_PLACEHOLDER = "__PROJECT__"


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "projects").is_dir() and (candidate / "skills").is_dir():
            return candidate
    raise FileNotFoundError("Could not locate repo root (missing projects/ and skills/)")


def _templates_root(repo_root: Path) -> Path:
    return repo_root / "skills" / "mxl-project-scaffold" / "assets" / "templates"


def _list_templates(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted([p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")])


def _replace_placeholders(project_dir: Path, replacement: str) -> None:
    suffixes = {".py", ".md", ".json", ".sh", ".txt", ".rst"}
    for path in project_dir.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix.lower() not in suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if _PLACEHOLDER not in text:
            continue
        path.write_text(text.replace(_PLACEHOLDER, replacement), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a new MaxwellLink project under projects/YYYY-MM-DD-NAME/ from a template."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available templates and exit.",
    )
    parser.add_argument(
        "--template",
        type=str,
        help="Template name (directory under skills/mxl-project-scaffold/assets/templates/).",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Project name suffix (the scaffolded folder is YYYY-MM-DD-NAME).",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Override the date prefix (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the destination folder if it already exists.",
    )

    args = parser.parse_args(argv)

    repo_root = _find_repo_root(Path(__file__).resolve())
    templates_root = _templates_root(repo_root)

    if args.list:
        for name in _list_templates(templates_root):
            print(name)
        return 0

    if not args.template or not args.name:
        parser.error("--template and --name are required unless --list is used.")

    template_dir = templates_root / args.template
    if not template_dir.is_dir():
        available = ", ".join(_list_templates(templates_root)) or "<none>"
        raise FileNotFoundError(
            f"Unknown template '{args.template}'. Available templates: {available}"
        )

    date_prefix = args.date or _dt.date.today().isoformat()
    folder_name = f"{date_prefix}-{args.name}"
    dest_dir = repo_root / "projects" / folder_name

    if dest_dir.exists():
        if not args.force:
            raise FileExistsError(f"Destination already exists: {dest_dir}")
        shutil.rmtree(dest_dir)

    ignore = shutil.ignore_patterns(
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".DS_Store",
        ".pytest_cache",
    )
    shutil.copytree(template_dir, dest_dir, ignore=ignore)
    _replace_placeholders(dest_dir, folder_name)

    print(dest_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
