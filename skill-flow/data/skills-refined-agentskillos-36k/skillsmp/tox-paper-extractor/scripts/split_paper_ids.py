#!/usr/bin/env python3
"""
Split a paper ID list into multiple non-overlapping parts (deterministic).

Designed for running multiple Codex windows without overlap:
  - Discover once (e.g., with discover_epmc_pmcids_fast.py) to get N candidates
  - Split into k parts (e.g., 2×500) with a fixed seed
  - Each worker/run consumes one part in its own run directory

Input:
  - A text file with one ID per line (PMCID/PMID/DOI; mixed ok)
  - Optional exclude files (one id per line) to avoid re-processing

Output:
  - part_01.txt ... part_k.txt
  - split.meta.json (audit: inputs, filters, seed, selected ids, sha-like counts)
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_ids(path: Path) -> list[str]:
    ids: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        ids.append(s)
    return ids


def dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in items:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


@dataclass(frozen=True)
class SplitConfig:
    seed: int
    parts: int
    per_part: int
    shuffle: bool


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Input ids file (one per line)")
    ap.add_argument("--exclude", action="append", default=[], help="Exclude ids file (repeatable)")
    ap.add_argument("--out-dir", required=True, help="Output directory for part files")
    ap.add_argument("--parts", type=int, default=2, help="Number of parts")
    ap.add_argument("--per-part", type=int, default=500, help="IDs per part")
    ap.add_argument("--seed", type=int, default=20260122, help="Deterministic RNG seed")
    ap.add_argument("--no-shuffle", action="store_true", help="Do not shuffle before splitting")
    args = ap.parse_args()

    inp = Path(args.input).resolve()
    if not inp.exists():
        raise SystemExit(f"--input not found: {inp}")

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = dedupe_preserve_order(load_ids(inp))

    excluded: set[str] = set()
    exclude_paths: list[str] = []
    for p in args.exclude or []:
        path = Path(p).resolve()
        exclude_paths.append(str(path))
        if path.exists():
            excluded.update(load_ids(path))

    filtered = [x for x in raw if x not in excluded]

    parts = max(1, int(args.parts))
    per_part = max(1, int(args.per_part))
    needed = parts * per_part

    cfg = SplitConfig(seed=int(args.seed), parts=parts, per_part=per_part, shuffle=not bool(args.no_shuffle))

    order = list(filtered)
    if cfg.shuffle:
        rng = random.Random(cfg.seed)
        rng.shuffle(order)

    selected = order[:needed]
    if len(selected) < needed:
        raise SystemExit(
            f"Not enough IDs after exclusion: need {needed} (=parts*per_part) but got {len(selected)}. "
            f"input={len(raw)} excluded={len(excluded)} filtered={len(filtered)}"
        )

    part_paths: list[str] = []
    for i in range(parts):
        part_ids = selected[i * per_part : (i + 1) * per_part]
        part_path = out_dir / f"paper_ids_part_{i+1:02d}.txt"
        part_path.write_text("\n".join(part_ids) + "\n", encoding="utf-8")
        part_paths.append(str(part_path))

    meta = {
        "kind": "split_paper_ids",
        "version": 1,
        "created_at": now_iso(),
        "inputs": {
            "input": str(inp),
            "exclude": exclude_paths,
        },
        "config": {
            "seed": cfg.seed,
            "parts": cfg.parts,
            "per_part": cfg.per_part,
            "shuffle": cfg.shuffle,
        },
        "stats": {
            "input_raw": len(load_ids(inp)),
            "input_unique": len(raw),
            "excluded_unique": len(excluded),
            "available_after_exclude": len(filtered),
            "selected_total": len(selected),
        },
        "outputs": {
            "out_dir": str(out_dir),
            "parts": part_paths,
        },
    }
    (out_dir / "split.meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] out_dir: {out_dir}")
    print(f"[ok] parts: {parts} x {per_part} = {needed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

