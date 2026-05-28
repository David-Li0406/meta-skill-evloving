#!/usr/bin/env python3
"""
Fast Europe PMC discovery for OA papers in PMC (PMCID list).

This script is intentionally lightweight: it DOES NOT download full-text XML during discovery.
Instead, it:
  - runs a Europe PMC search query
  - filters results to (pmcid present) AND (isOpenAccess == Y) AND (inPMC == Y)
  - outputs a de-duplicated PMCID list for downstream downloading

Rationale:
  For large-scale runs (e.g., 2000+ papers), downloading fulltext XML twice (discovery + download)
  is wasteful. We do XML/table filtering later in extract_paper_extractions.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable


PMCID_RE = re.compile(r"^PMC\d+$", re.IGNORECASE)

ENDPOINT_TERMS = (
    "mic",
    "mbc",
    "ic50",
    "cc50",
    "ec50",
    "hc10",
    "hc50",
    "mhc",
    "ld50",
    "lc50",
    "hemolysis",
    "hemolytic",
    "cytotoxic",
    "cytotoxicity",
    "toxicity",
    "venom",
    "toxin",
)


def normalize_ws(text: str) -> str:
    return re.sub(r"\\s+", " ", (text or "")).strip()


def fetch_json(url: str, *, max_tries: int = 3, sleep_s: float = 0.6) -> dict[str, Any]:
    last: Exception | None = None
    for _ in range(max_tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e
            time.sleep(max(0.0, float(sleep_s)))
            continue
    raise last or RuntimeError("fetch_json failed")


def iter_epmc_search(
    query: str, *, page_size: int = 100, max_results: int = 1000, request_sleep_s: float = 0.0
) -> Iterable[dict[str, Any]]:
    cursor = "*"
    seen = 0
    while seen < max_results:
        page_size_eff = max(1, min(1000, int(page_size)))
        url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
            + "?query="
            + urllib.parse.quote(query)
            + "&format=json"
            + f"&pageSize={min(page_size_eff, max_results - seen)}"
            + "&cursorMark="
            + urllib.parse.quote(cursor)
        )
        data = fetch_json(url)
        results = data.get("resultList", {}).get("result", []) or []
        if not results:
            return
        for res in results:
            yield res
            seen += 1
            if seen >= max_results:
                return
        cursor = data.get("nextCursorMark") or ""
        if not cursor:
            return
        if request_sleep_s and request_sleep_s > 0:
            time.sleep(float(request_sleep_s))


def score_result(res: dict[str, Any]) -> tuple[int, str]:
    title = normalize_ws(str(res.get("title") or ""))
    t = title.lower()
    hits = [k for k in ENDPOINT_TERMS if k in t]
    score = 2 * len({h for h in hits if h in ("mic", "mbc", "ic50", "cc50", "hc10", "hc50", "mhc", "ld50", "lc50")})
    score += 1 if ("hemolysis" in hits or "hemolytic" in hits) else 0
    score += 1 if ("toxicity" in hits or "cytotoxic" in hits or "cytotoxicity" in hits) else 0
    score += 1 if ("toxin" in hits or "venom" in hits) else 0
    score += 1 if str(res.get("hasSuppl") or "").upper() == "Y" else 0
    score += 1 if str(res.get("hasPDF") or "").upper() == "Y" else 0
    reasons = []
    if hits:
        reasons.append("title_hits=" + ",".join(sorted(set(hits))))
    if str(res.get("hasSuppl") or "").upper() == "Y":
        reasons.append("hasSuppl=Y")
    if str(res.get("hasPDF") or "").upper() == "Y":
        reasons.append("hasPDF=Y")
    return score, ";".join(reasons)


@dataclass
class Candidate:
    pmcid: str
    pmid: str
    title: str
    pub_year: str
    journal: str
    score: int
    reasons: str
    has_pdf: str
    has_suppl: str


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True, help="Europe PMC query string")
    ap.add_argument("--max-results", type=int, default=20000, help="Max Europe PMC results to scan (upper bound)")
    ap.add_argument("--keep", type=int, default=2000, help="Stop after collecting this many PMCIDs")
    ap.add_argument("--min-score", type=int, default=0, help="Only keep results with score >= this value")
    ap.add_argument("--page-size", type=int, default=100, help="Europe PMC pageSize (max 1000)")
    ap.add_argument("--request-sleep", type=float, default=0.0, help="Sleep seconds between page requests")
    ap.add_argument("--out", default="candidates_fast.csv", help="Output CSV path")
    ap.add_argument("--ids-out", default="paper_ids.txt", help="Output PMCID list (one per line)")
    ap.add_argument("--require-oa", action="store_true", help="Require isOpenAccess == Y")
    ap.add_argument("--require-in-pmc", action="store_true", help="Require inPMC == Y")
    ap.set_defaults(require_oa=True, require_in_pmc=True)
    args = ap.parse_args()

    max_results = max(1, int(args.max_results))
    keep = max(1, int(args.keep))

    seen = 0
    kept: list[Candidate] = []
    seen_pmcids: set[str] = set()

    min_score = int(args.min_score)

    for res in iter_epmc_search(
        str(args.query),
        max_results=max_results,
        page_size=int(args.page_size),
        request_sleep_s=float(args.request_sleep),
    ):
        seen += 1
        if seen % 50 == 0:
            print(f"[progress] scanned={seen} kept={len(kept)}", file=sys.stderr)

        pmcid = str(res.get("pmcid") or "").strip()
        if not pmcid or not PMCID_RE.match(pmcid):
            continue
        if args.require_oa and str(res.get("isOpenAccess") or "").upper() != "Y":
            continue
        if args.require_in_pmc and str(res.get("inPMC") or "").upper() != "Y":
            continue
        if pmcid in seen_pmcids:
            continue

        score, reasons = score_result(res)
        if score < min_score:
            seen_pmcids.add(pmcid)
            continue
        kept.append(
            Candidate(
                pmcid=pmcid,
                pmid=str(res.get("pmid") or "").strip(),
                title=normalize_ws(str(res.get("title") or "")),
                pub_year=str(res.get("pubYear") or "").strip(),
                journal=normalize_ws(str(res.get("journalTitle") or "")),
                score=int(score),
                reasons=reasons,
                has_pdf=str(res.get("hasPDF") or "").strip(),
                has_suppl=str(res.get("hasSuppl") or "").strip(),
            )
        )
        seen_pmcids.add(pmcid)
        if len(kept) >= keep:
            break

    kept.sort(key=lambda c: (-c.score, c.pub_year, c.pmcid))

    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pmcid", "pmid", "pub_year", "journal", "score", "reasons", "hasPDF", "hasSuppl", "title"])
        for c in kept:
            w.writerow([c.pmcid, c.pmid, c.pub_year, c.journal, c.score, c.reasons, c.has_pdf, c.has_suppl, c.title])

    with open(args.ids_out, "w", encoding="utf-8") as f:
        for c in kept:
            f.write(c.pmcid + "\n")

    print(f"Scanned: {seen}", file=sys.stderr)
    print(f"Kept PMCIDs: {len(kept)}", file=sys.stderr)
    print(f"Candidates CSV: {args.out}", file=sys.stderr)
    print(f"IDs file: {args.ids_out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
