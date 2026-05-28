#!/usr/bin/env python3
"""
Validate that a blog Markdown draft meets the key constraints of this skill.

This is not a language model. It only checks structural / mechanical rules so you
can iterate fast:
  - title format
  - metadata block keys
  - references section
  - banned full-page figures (paper/pages)
  - image links are URLs after Lsky sync (optional)
  - code block count (soft)
  - list density (soft)
  - banned marketing phrases (soft)

Exit codes:
  0 = all hard checks passed
  2 = hard check failed
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


def read_text_guess_encoding(path: Path) -> tuple[str, str]:
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=enc), enc
        except UnicodeDecodeError:
            continue
    raise


TITLE_RE = re.compile(r"^【文献阅读】\|\s*.+[：:].+$")
META_KEYS = [
    "论文标题",
    "作者",
    "期刊/会议",
    "发布时间",
    "影响因子",
    "中科院分区",
    "DOI",
]

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CODE_FENCE_RE = re.compile(r"^```", flags=re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", flags=re.M)
LIST_LINE_RE = re.compile(r"^\s*([-*]|\d+\.)\s+", flags=re.M)

BANNED_HARD = [
    "paper/pages/",
    "\\paper\\pages\\",
]

BANNED_SOFT_WORDS = [
    "颠覆",
    "震撼",
    "史诗级",
    "技术分析文档",
    "技术架构分析文档",
]


@dataclass(frozen=True)
class CheckResult:
    ok: bool
    hard_failures: list[str]
    warnings: list[str]


def parse_link_token(inner: str) -> str:
    # Keep only the first token before optional title/whitespace.
    inner = inner.strip()
    if not inner:
        return inner
    return inner.split()[0]


def is_url(value: str) -> bool:
    value = value.strip()
    return value.startswith("http://") or value.startswith("https://")


def check(
    text: str,
    *,
    require_urls: bool,
    max_code_blocks: int,
    max_list_ratio: float,
) -> CheckResult:
    hard: list[str] = []
    warn: list[str] = []

    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    first_non_empty = next((ln.strip() for ln in lines if ln.strip()), "")
    if not first_non_empty:
        hard.append("Empty file.")
    elif not TITLE_RE.match(first_non_empty):
        hard.append("Title line must match: 【文献阅读】| <name>: <one-line summary>")

    for key in META_KEYS:
        if not any(key in ln for ln in lines[:80]):
            hard.append(f"Missing metadata key near top: {key}")

    if "参考文献" not in text:
        hard.append("Missing '参考文献' section.")

    for bad in BANNED_HARD:
        if bad in text:
            hard.append(f"Forbidden full-page figure reference found: {bad}")

    images = [parse_link_token(m.group(1)) for m in IMAGE_RE.finditer(text)]
    if not images:
        warn.append("No images found (expected at least the front-matter image).")
    if require_urls:
        not_urls = [img for img in images if img and not is_url(img)]
        if not_urls:
            hard.append(
                "Images must be URL links after Lsky sync. Non-URL images: "
                + ", ".join(sorted(set(not_urls))[:10])
            )

    fences = len(CODE_FENCE_RE.findall(text))
    code_blocks = fences // 2 if fences else 0
    if code_blocks > max_code_blocks:
        warn.append(f"Too many code blocks: {code_blocks} (recommended <= {max_code_blocks})")

    non_empty_lines = [ln for ln in lines if ln.strip()]
    list_lines = LIST_LINE_RE.findall(text)
    if non_empty_lines:
        ratio = len(list_lines) / len(non_empty_lines)
        if ratio > max_list_ratio:
            warn.append(f"List density is high: {ratio:.2%} (recommended <= {max_list_ratio:.0%})")

    headings = HEADING_RE.findall(text)
    max_level = max((len(h[0]) for h in headings), default=0)
    if max_level >= 4:
        warn.append(f"Heading depth is deep: max #{max_level} (recommend <= ###)")

    for w in BANNED_SOFT_WORDS:
        if w in text:
            warn.append(f"Contains banned/undesired phrase: {w}")

    return CheckResult(ok=not hard, hard_failures=hard, warnings=warn)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check blog Markdown against dl-paper-code-blog constraints.")
    parser.add_argument("markdown", type=Path, help="Path to blog Markdown (blog.md or *_blog.md).")
    parser.add_argument("--require-urls", action="store_true", help="Require all images to be http(s) URLs.")
    parser.add_argument("--max-code-blocks", type=int, default=2, help="Warn if code blocks exceed this count.")
    parser.add_argument(
        "--max-list-ratio",
        type=float,
        default=0.25,
        help="Warn if list lines exceed this ratio of non-empty lines.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    md_path: Path = args.markdown
    if not md_path.is_file():
        raise SystemExit(f"Markdown not found: {md_path}")

    text, encoding = read_text_guess_encoding(md_path)
    result = check(
        text,
        require_urls=args.require_urls,
        max_code_blocks=args.max_code_blocks,
        max_list_ratio=args.max_list_ratio,
    )

    if result.ok:
        print(f"OK ({encoding}): hard checks passed.")
    else:
        print(f"FAIL ({encoding}): hard checks failed:")
        for msg in result.hard_failures:
            print(f"- {msg}")

    if result.warnings:
        print("Warnings:")
        for msg in result.warnings:
            print(f"- {msg}")

    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

