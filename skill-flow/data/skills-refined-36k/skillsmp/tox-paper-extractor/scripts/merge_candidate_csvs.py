#!/usr/bin/env python3
"""
Merge multiple candidate CSVs (from discover_epmc_pmcids_fast.py) into a de-duplicated list.

De-dup key: pmcid
Tie-break: higher score, then hasSuppl=Y, then hasPDF=Y, then newer pub_year, then longer title.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Candidate:
    pmcid: str
    pmid: str
    pub_year: int
    journal: str
    score: int
    reasons: str
    has_pdf: str
    has_suppl: str
    title: str


def parse_int(raw: str) -> int:
    try:
        return int(str(raw or "").strip())
    except Exception:
        return 0


def yn(raw: str) -> int:
    return 1 if str(raw or "").strip().upper() == "Y" else 0


def better(a: Candidate, b: Candidate) -> Candidate:
    if a.score != b.score:
        return a if a.score > b.score else b
    if yn(a.has_suppl) != yn(b.has_suppl):
        return a if yn(a.has_suppl) > yn(b.has_suppl) else b
    if yn(a.has_pdf) != yn(b.has_pdf):
        return a if yn(a.has_pdf) > yn(b.has_pdf) else b
    if a.pub_year != b.pub_year:
        return a if a.pub_year > b.pub_year else b
    if len(a.title) != len(b.title):
        return a if len(a.title) > len(b.title) else b
    return a if a.pmcid <= b.pmcid else b


def load_csv(path: Path) -> list[Candidate]:
    out: list[Candidate] = []
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            pmcid = str(row.get("pmcid") or "").strip()
            if not pmcid:
                continue
            out.append(
                Candidate(
                    pmcid=pmcid,
                    pmid=str(row.get("pmid") or "").strip(),
                    pub_year=parse_int(row.get("pub_year") or ""),
                    journal=str(row.get("journal") or "").strip(),
                    score=parse_int(row.get("score") or ""),
                    reasons=str(row.get("reasons") or "").strip(),
                    has_pdf=str(row.get("hasPDF") or "").strip(),
                    has_suppl=str(row.get("hasSuppl") or "").strip(),
                    title=str(row.get("title") or "").strip(),
                )
            )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True, help="One or more candidates.csv paths")
    ap.add_argument("--out", required=True, help="Output merged candidates CSV")
    ap.add_argument("--ids-out", required=True, help="Output PMCID list (one per line)")
    ap.add_argument("--max-rows", type=int, default=0, help="Optional cap for output size (0 disables)")
    args = ap.parse_args()

    merged: dict[str, Candidate] = {}
    for raw in args.inputs:
        p = Path(raw).resolve()
        if not p.exists():
            raise SystemExit(f"Input not found: {p}")
        for c in load_csv(p):
            prev = merged.get(c.pmcid)
            merged[c.pmcid] = c if prev is None else better(prev, c)

    items = list(merged.values())
    items.sort(key=lambda c: (-c.score, -c.pub_year, c.pmcid))

    max_rows = int(args.max_rows)
    if max_rows > 0:
        items = items[:max_rows]

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pmcid", "pmid", "pub_year", "journal", "score", "reasons", "hasPDF", "hasSuppl", "title"])
        for c in items:
            w.writerow([c.pmcid, c.pmid, c.pub_year or "", c.journal, c.score, c.reasons, c.has_pdf, c.has_suppl, c.title])

    ids_path = Path(args.ids_out).resolve()
    ids_path.parent.mkdir(parents=True, exist_ok=True)
    with ids_path.open("w", encoding="utf-8") as f:
        for c in items:
            f.write(c.pmcid + "\n")

    print(f"[ok] inputs={len(args.inputs)} merged={len(merged)} wrote={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

