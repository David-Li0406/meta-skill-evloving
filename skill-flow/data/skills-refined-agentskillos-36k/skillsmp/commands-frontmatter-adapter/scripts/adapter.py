#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "pyyaml",
# ]
# ///
"""Extract Claude Code command frontmatter + body for Codex CLI prompts."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Dict, Optional, Tuple


def split_frontmatter(text: str) -> Tuple[Optional[str], str]:
    """Return (frontmatter, body). Frontmatter is None if absent."""
    # Match first pair of --- at the beginning of the file
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, flags=re.DOTALL)
    if not match:
        return None, text
    return match.group(1), match.group(2)


def _fallback_parse(raw: str) -> Dict[str, object]:
    data: Dict[str, object] = {}
    current_key: Optional[str] = None
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("- ") and current_key:
            data.setdefault(current_key, []).append(line[2:].strip())
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if not val:
                data[key] = ""
            else:
                # Comma-separated list is stored as list
                if "," in val:
                    parts = [p.strip() for p in val.split(",") if p.strip()]
                    data[key] = parts if len(parts) > 1 else val
                else:
                    data[key] = val
            current_key = key
    return data


def parse_frontmatter(raw: str) -> Dict[str, object]:
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(raw)
        if loaded is None:
            return {}
        if isinstance(loaded, dict):
            return loaded
        return {"_": loaded}
    except Exception:
        return _fallback_parse(raw)


def build_output(
    file_path: pathlib.Path, fm_raw: Optional[str], body: str
) -> Dict[str, object]:
    return {
        "file": str(file_path),
        "frontmatter": parse_frontmatter(fm_raw) if fm_raw else None,
        "frontmatter_raw": fm_raw,
        "body": body,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--command", help="Command name (without .md) under src/.claude/commands"
    )
    parser.add_argument("--file", help="Explicit path to command file")
    parser.add_argument("--body-only", action="store_true", help="Print only body text")
    parser.add_argument(
        "--frontmatter-only",
        action="store_true",
        help="Print parsed frontmatter as JSON",
    )
    parser.add_argument(
        "--raw-frontmatter", action="store_true", help="Print raw frontmatter block"
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    if not args.command and not args.file:
        parser.error("Specify --command or --file")

    # Resolve commands directory relative to this skill so symlinked installs work.
    skill_root = pathlib.Path(__file__).resolve().parents[3] / "commands"
    base = skill_root if skill_root.exists() else pathlib.Path("src/.claude/commands")

    file_path = pathlib.Path(args.file) if args.file else base / f"{args.command}.md"
    if not file_path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        return 1

    text = file_path.read_text(encoding="utf-8")
    fm_raw, body = split_frontmatter(text)
    payload = build_output(file_path, fm_raw, body)

    if args.body_only:
        print(body.rstrip())
        return 0
    if args.frontmatter_only:
        print(
            json.dumps(
                payload["frontmatter"],
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0
    if args.raw_frontmatter:
        print(fm_raw or "")
        return 0

    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
