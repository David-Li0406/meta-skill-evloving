#!/usr/bin/env python3
"""
RepoGPS entrypoint finder (standalone).

Usage:
  python find_entrypoints.py --cache .repogps_cache/xai-org__x-algorithm__main
"""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import List, Optional, Tuple

from _github import (
    score_entrypoint_path,
    score_entrypoint_content,
)


def find_downloaded_text(cache_dir: pathlib.Path, original_path: str) -> Optional[str]:
    """Load downloaded file content by original path."""
    slug = original_path.replace("/", "__") + ".txt"
    p = cache_dir / "downloaded" / slug
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8", errors="ignore")


def main():
    ap = argparse.ArgumentParser(description="RepoGPS - Find entrypoints")
    ap.add_argument("--cache", required=True, help="Path to scan_repo output folder")
    args = ap.parse_args()

    cache_dir = pathlib.Path(args.cache)
    tree = json.loads((cache_dir / "repo_tree.json").read_text(encoding="utf-8"))
    paths: List[str] = tree["paths"]

    candidates: List[Tuple[str, float, List[str]]] = []

    for p in paths:
        base = score_entrypoint_path(p)
        if base <= 0:
            continue

        evidence = [f"path_match(base={base:.2f})"]
        content = find_downloaded_text(cache_dir, p)
        score = base

        if content:
            b = score_entrypoint_content(content)
            if b > 0:
                evidence.append(f"content_hints(+{b:.2f})")
            score += b
        else:
            evidence.append("content_unavailable")

        score = min(score, 1.0)
        candidates.append((p, score, evidence))

    candidates.sort(key=lambda x: x[1], reverse=True)

    out = {
        "top_entrypoints": [
            {"path": p, "confidence": round(s, 3), "evidence": ev}
            for (p, s, ev) in candidates[:15]
        ],
        "note": "Confidence is heuristic. Open these files to confirm wiring/entrypoint.",
    }

    (cache_dir / "entrypoints.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(f"[RepoGPS] Wrote: {cache_dir / 'entrypoints.json'}")

    for item in out["top_entrypoints"][:5]:
        print(f"  - {item['path']}  (conf={item['confidence']})")


if __name__ == "__main__":
    main()
