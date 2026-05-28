#!/usr/bin/env python3
"""
Deterministically merge analysis/per_paper/*.md into a single summary markdown.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis-dir", type=str, default="analysis", help="Analysis root directory")
    ap.add_argument("--out", type=str, default="analysis/summary.md", help="Output summary markdown path")
    args = ap.parse_args()

    analysis_dir = Path(args.analysis_dir).resolve()
    per_paper = analysis_dir / "per_paper"
    if not per_paper.exists():
        raise SystemExit(f"per_paper dir not found: {per_paper}")

    md_files = sorted(per_paper.glob("*.md"), key=lambda p: p.name.lower())
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = []
    parts.append(f"# Per-paper extraction review summary\n\nGenerated at: {now_iso()}\n\nCount: {len(md_files)}\n")

    for p in md_files:
        paper_id = p.stem
        parts.append(f"\n\n---\n\n## {paper_id}\n")
        parts.append(p.read_text(encoding="utf-8", errors="ignore").rstrip() + "\n")

    out_path.write_text("".join(parts), encoding="utf-8")
    print(f"[ok] wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

