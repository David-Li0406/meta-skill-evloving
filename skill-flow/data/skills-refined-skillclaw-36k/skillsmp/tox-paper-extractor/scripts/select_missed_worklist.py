#!/usr/bin/env python3
"""
Select a deterministic "high-signal missed" worklist from sequence_present_but_no_records.csv.

Input CSV schema (expected columns):
  - paper_stem
  - sequence_extractions
  - endpoint_value_extractions
  - experimental_records

Typical usage:
  python scripts/select_missed_worklist.py \
    --missed-csv runs/<run>/sequence_present_but_no_records.csv \
    --n 10 \
    --max-sequence-extractions 5000 \
    --out-worklist analysis/missed_round1/worklist_run1.txt \
    --out-meta analysis/missed_round1/worklist_run1.meta.json
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def safe_int(raw: object) -> int:
    s = str(raw or "").strip()
    if not s:
        return 0
    try:
        return int(float(s))
    except Exception:
        return 0


@dataclass(frozen=True)
class Row:
    paper_stem: str
    sequence_extractions: int
    endpoint_value_extractions: int
    experimental_records: int


def load_rows(path: Path) -> list[Row]:
    rows: list[Row] = []
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for d in r:
            paper = str((d.get("paper_stem") or "")).strip()
            if not paper:
                continue
            rows.append(
                Row(
                    paper_stem=paper,
                    sequence_extractions=safe_int(d.get("sequence_extractions")),
                    endpoint_value_extractions=safe_int(d.get("endpoint_value_extractions")),
                    experimental_records=safe_int(d.get("experimental_records")),
                )
            )
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--missed-csv", required=True, help="Path to sequence_present_but_no_records.csv")
    ap.add_argument("--n", type=int, default=10, help="How many papers to select")
    ap.add_argument("--max-sequence-extractions", type=int, default=5000, help="Filter out extreme sequence_extractions noise")
    ap.add_argument(
        "--require-experimental-records-eq-0",
        action="store_true",
        help="Only keep rows where experimental_records==0 (recommended).",
    )
    ap.add_argument("--skip", action="append", default=[], help="Paper stem to skip (repeatable), e.g., --skip PMC11452708")
    ap.add_argument("--out-worklist", required=True, help="Output txt worklist path (one PMCID per line)")
    ap.add_argument("--out-meta", required=True, help="Output meta JSON path (selection audit)")
    args = ap.parse_args()

    missed_csv = Path(args.missed_csv).resolve()
    if not missed_csv.exists():
        raise SystemExit(f"--missed-csv not found: {missed_csv}")

    out_worklist = Path(args.out_worklist).resolve()
    out_meta = Path(args.out_meta).resolve()
    out_worklist.parent.mkdir(parents=True, exist_ok=True)
    out_meta.parent.mkdir(parents=True, exist_ok=True)

    rows = load_rows(missed_csv)
    skipped = {str(s).strip() for s in (args.skip or []) if str(s).strip()}

    filtered = []
    for row in rows:
        if row.paper_stem in skipped:
            continue
        if args.require_experimental_records_eq_0 and row.experimental_records != 0:
            continue
        if row.sequence_extractions > int(args.max_sequence_extractions):
            continue
        filtered.append(row)

    # High-signal heuristic: prioritize endpoint_value_extractions, prefer fewer sequence_extractions noise.
    filtered.sort(
        key=lambda r: (-r.endpoint_value_extractions, r.sequence_extractions, r.paper_stem),
    )

    selected = filtered[: max(0, int(args.n))]
    out_worklist.write_text("\n".join(r.paper_stem for r in selected) + "\n", encoding="utf-8")

    meta = {
        "kind": "missed_recovery_worklist_single",
        "version": 1,
        "created_at": now_iso(),
        "inputs": {"missed_csv": str(missed_csv)},
        "config": {
            "n": int(args.n),
            "max_sequence_extractions": int(args.max_sequence_extractions),
            "require_experimental_records_eq_0": bool(args.require_experimental_records_eq_0),
            "skip": sorted(skipped),
            "sort": [
                {"key": "endpoint_value_extractions", "order": "desc"},
                {"key": "sequence_extractions", "order": "asc"},
                {"key": "paper_stem", "order": "asc"},
            ],
        },
        "stats": {
            "rows_total": len(rows),
            "rows_after_filters": len(filtered),
            "selected_n": len(selected),
        },
        "selected": [
            {
                "paper_stem": r.paper_stem,
                "sequence_extractions": r.sequence_extractions,
                "endpoint_value_extractions": r.endpoint_value_extractions,
                "experimental_records": r.experimental_records,
            }
            for r in selected
        ],
        "outputs": {"worklist": str(out_worklist)},
    }
    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] missed_csv: {missed_csv}")
    print(f"[ok] selected: {len(selected)} (of {len(filtered)} after filters)")
    print(f"[ok] out_worklist: {out_worklist}")
    print(f"[ok] out_meta: {out_meta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

