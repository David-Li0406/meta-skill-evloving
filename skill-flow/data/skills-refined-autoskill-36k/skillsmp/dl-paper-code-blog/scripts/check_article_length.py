#!/usr/bin/env python3
"""
Check blog article length and provide a section-level breakdown.

This script is a lightweight guardrail to keep output stable within a target
range (default: 5000-7000 chars).

It reports:
  - non-whitespace character count (recommended "字数" proxy)
  - CJK ideograph count (rough "汉字" proxy)
  - per-section counts (based on Markdown headings)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


def read_text_guess_encoding(path: Path) -> tuple[str, str]:
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=enc), enc
        except UnicodeDecodeError:
            continue
    raise


def is_cjk_ideograph(ch: str) -> bool:
    code = ord(ch)
    return (
        0x3400 <= code <= 0x4DBF  # CJK Unified Ideographs Extension A
        or 0x4E00 <= code <= 0x9FFF  # CJK Unified Ideographs
        or 0xF900 <= code <= 0xFAFF  # CJK Compatibility Ideographs
    )


def count_non_ws(text: str) -> int:
    return sum(1 for ch in text if not ch.isspace())


def count_cjk(text: str) -> int:
    return sum(1 for ch in text if is_cjk_ideograph(ch))


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass(frozen=True)
class SectionStat:
    heading: str
    level: int
    non_ws_chars: int
    cjk_chars: int


def section_stats(text: str) -> list[SectionStat]:
    lines = text.splitlines(keepends=True)
    sections: list[tuple[str, int, list[str]]] = []
    current_heading = "(preamble)"
    current_level = 0
    current_buf: list[str] = []

    for line in lines:
        m = HEADING_RE.match(line.rstrip("\n"))
        if m:
            # flush previous
            sections.append((current_heading, current_level, current_buf))
            current_heading = m.group(2).strip()
            current_level = len(m.group(1))
            current_buf = []
            continue
        current_buf.append(line)

    sections.append((current_heading, current_level, current_buf))

    stats: list[SectionStat] = []
    for heading, level, buf in sections:
        body = "".join(buf)
        stats.append(
            SectionStat(
                heading=heading,
                level=level,
                non_ws_chars=count_non_ws(body),
                cjk_chars=count_cjk(body),
            )
        )
    return stats


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check article length for a Markdown blog post.")
    parser.add_argument("markdown", type=Path, help="Path to blog Markdown (blog.md or *_blog.md).")
    parser.add_argument("--min", type=int, default=5000, help="Min target non-whitespace chars.")
    parser.add_argument("--max", type=int, default=7000, help="Max target non-whitespace chars.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    md_path: Path = args.markdown
    if not md_path.is_file():
        raise SystemExit(f"Markdown not found: {md_path}")

    text, encoding = read_text_guess_encoding(md_path)
    total_non_ws = count_non_ws(text)
    total_cjk = count_cjk(text)
    in_range = args.min <= total_non_ws <= args.max

    per_section = section_stats(text)
    payload = {
        "path": str(md_path),
        "encoding": encoding,
        "target": {"min_non_ws": args.min, "max_non_ws": args.max},
        "totals": {"non_ws_chars": total_non_ws, "cjk_chars": total_cjk, "in_range": in_range},
        "sections": [asdict(s) for s in per_section],
    }

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "OK" if in_range else "OUT_OF_RANGE"
        print(f"{status}: non-ws chars = {total_non_ws} (target {args.min}-{args.max}), cjk chars = {total_cjk}")
        # Show top sections by size (excluding preamble)
        sections_sorted = sorted(
            [s for s in per_section if s.heading != "(preamble)"],
            key=lambda s: s.non_ws_chars,
            reverse=True,
        )
        print("Top sections by length:")
        for s in sections_sorted[:10]:
            indent = "  " * max(0, s.level - 1)
            print(f"- {indent}{s.heading}: {s.non_ws_chars} chars ({s.cjk_chars} cjk)")
    return 0 if in_range else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

