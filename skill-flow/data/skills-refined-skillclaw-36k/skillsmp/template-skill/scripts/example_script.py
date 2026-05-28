#!/usr/bin/env python3
"""
Example helper script for new skills.
Generates a simple markdown header block you can prepend to outputs.
"""
from __future__ import annotations

import argparse


def build_header(title: str, summary: str, notes: str | None = None) -> str:
    lines = ["## " + title, "", summary.strip()]
    if notes:
        lines.extend(["", "Notes:", "- " + notes.strip()])
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a markdown header block")
    parser.add_argument("--title", required=True, help="Short title for the output")
    parser.add_argument("--summary", required=True, help="One-line summary of what changed")
    parser.add_argument("--notes", help="Optional extra note (bullet will be added)")
    args = parser.parse_args()

    header = build_header(args.title, args.summary, args.notes)
    print(header)


if __name__ == "__main__":
    main()
