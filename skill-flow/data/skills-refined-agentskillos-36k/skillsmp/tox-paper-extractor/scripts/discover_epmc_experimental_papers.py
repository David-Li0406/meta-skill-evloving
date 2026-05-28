#!/usr/bin/env python3
"""
Discover Europe PMC Open Access papers likely to contain *extractable experimental data*
in machine-readable tables (JATS XML): peptide/protein sequences + numeric endpoints.

This is a heuristic filter to produce a candidate list for fetch_open_access_papers.py.

Example:
  python scripts/discover_epmc_experimental_papers.py \\
    --query '((hemolysis OR hemolytic) AND peptide AND (HC50 OR IC50 OR CC50))' \\
    --max-results 200 \\
    --out candidates.csv \\
    --ids-out candidate_ids.txt
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
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, Iterable, Optional


AA_ALLOWED = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
AA_ALLOWED_SET = set(AA_ALLOWED)

SEQUENCE_STOPWORDS = {
    "SPECIFICITY",
    "SENSITIVITY",
    "PRECISION",
    "RECALL",
    "ACCURACY",
    "VALIDATION",
    "INDEPENDENT",
    "DEPENDENT",
    "CROSS",
    "TRAIN",
    "TRAINING",
    "TEST",
    "TESTING",
    "PREDICT",
    "PREDICTION",
    "CLASSIFIER",
    "CLASSIFICATION",
    "REGRESSION",
    "FEATURE",
    "FEATURES",
    "SEQUENCE",
    "SEQUENCES",
}

# Include both numeric endpoints and common assay words as hints. Numeric endpoints get higher weight.
ENDPOINT_KEYWORDS = (
    "HC50",
    "CC50",
    "IC50",
    "EC50",
    "LC50",
    "LD50",
    "GI50",
    "MIC",
    "MBC",
)

ENDPOINT_HINT_WORDS = (
    "hemolysis",
    "hemolytic",
    "cytotoxicity",
    "cytotoxic",
    "toxicity",
    "lethal",
)

_NUM_RE = r"(?:\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)"
_UNITS = (
    r"μM|µM|uM|nM|mM|pM|fM|"
    r"mg/kg|mg·kg-1|mg kg-1|"
    r"μg/mL|µg/mL|ug/mL|ng/mL|mg/mL|"
    r"g/L|mg/L|μg/L|µg/L|ug/L|"
    r"%"
)

VALUE_WITH_UNIT_RE = re.compile(rf"{_NUM_RE}\s*(?:{_UNITS})", flags=re.IGNORECASE)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def elem_text(elem: Optional[ET.Element]) -> str:
    if elem is None:
        return ""
    return normalize_whitespace("".join(elem.itertext()))


def extract_aa_tokens(text: str) -> list[str]:
    up = (text or "").upper()
    cleaned = re.sub(rf"[^{AA_ALLOWED}]+", " ", up)
    return [t for t in cleaned.split() if t]


def looks_like_aa_sequence(token: str, *, min_len: int) -> bool:
    if len(token) < min_len:
        return False
    if token in SEQUENCE_STOPWORDS:
        return False
    if any(ch not in AA_ALLOWED_SET for ch in token):
        return False
    unique = set(token)
    if len(token) >= 10 and len(unique) <= 2:
        return False
    return True


def find_sequences(text: str, *, min_len: int = 8) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for tok in extract_aa_tokens(text):
        if not looks_like_aa_sequence(tok, min_len=min_len):
            continue
        if tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


def table_elem_to_matrix(table_el: ET.Element, *, max_rows: int = 2000) -> list[list[str]]:
    rows: list[list[str]] = []
    for tr in table_el.findall(".//{*}tr"):
        cells: list[str] = []
        for child in list(tr):
            if not isinstance(child.tag, str):
                continue
            if child.tag.lower().endswith(("td", "th")):
                cells.append(elem_text(child))
        if cells:
            rows.append(cells)
        if len(rows) >= max_rows:
            break
    return rows


def has_sequence_column(headers: list[str]) -> bool:
    return any(re.search(r"\b(seq|sequence)\b", h or "", flags=re.IGNORECASE) for h in headers)


def count_sequence_cells(rows: list[list[str]], *, min_len: int = 8, max_scan_rows: int = 200) -> int:
    if not rows:
        return 0
    headers = rows[0]
    seq_cols = [i for i, h in enumerate(headers) if re.search(r"\b(seq|sequence)\b", h or "", flags=re.IGNORECASE)]
    if not seq_cols:
        return 0
    cnt = 0
    for r in rows[1 : min(len(rows), 1 + max_scan_rows)]:
        for c in seq_cols:
            if c >= len(r):
                continue
            if find_sequences(r[c], min_len=min_len):
                cnt += 1
                break
    return cnt


def table_endpoint_hints(caption: str, headers: list[str]) -> list[str]:
    text = normalize_whitespace(f"{caption} " + " ".join(headers)).lower()
    hits: list[str] = []
    for kw in ENDPOINT_KEYWORDS:
        if re.search(rf"\b{re.escape(kw.lower())}\b", text):
            hits.append(kw)
    if hits:
        return hits
    # fallback to softer words
    for w in ENDPOINT_HINT_WORDS:
        if w in text:
            hits.append(w.upper())
    return hits


def count_value_cells(rows: list[list[str]], *, max_scan_rows: int = 200) -> int:
    if not rows:
        return 0
    cnt = 0
    for r in rows[1 : min(len(rows), 1 + max_scan_rows)]:
        for cell in r:
            if VALUE_WITH_UNIT_RE.search(cell or ""):
                cnt += 1
                if cnt >= 5:
                    return cnt
    return cnt


def fetch_json(url: str) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_fulltext_xml(pmcid: str) -> Optional[ET.Element]:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    last_err: Optional[Exception] = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                xml_bytes = r.read()
            return ET.fromstring(xml_bytes)
        except Exception as e:
            last_err = e
            time.sleep(0.5)
            continue
    _ = last_err
    return None


def iter_epmc_search(query: str, *, page_size: int = 100, max_results: int = 200) -> Iterable[dict[str, Any]]:
    cursor = "*"
    seen = 0
    while seen < max_results:
        url = (
            "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
            + "?query="
            + urllib.parse.quote(query)
            + "&format=json"
            + f"&pageSize={min(page_size, max_results - seen)}"
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


@dataclass
class Candidate:
    pmcid: str
    doi: str
    pmid: str
    title: str
    pub_year: str
    journal: str
    score: int
    reasons: str
    endpoint_hints: str


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", type=str, required=True, help="Europe PMC query")
    ap.add_argument("--max-results", type=int, default=200, help="Max EPMC search results to scan")
    ap.add_argument("--max-candidates", type=int, default=0, help="Stop after keeping this many candidates (0 disables)")
    ap.add_argument("--out", type=str, default="candidates_experimental.csv", help="Output CSV path")
    ap.add_argument("--ids-out", type=str, default="candidate_ids.txt", help="Output IDs file for fetch_open_access_papers.py")
    ap.add_argument("--min-score", type=int, default=4, help="Minimum score to keep")
    ap.add_argument("--require-oa", action="store_true", help="Require Europe PMC isOpenAccess == Y")
    ap.set_defaults(require_oa=True)
    args = ap.parse_args()

    candidates: list[Candidate] = []
    scanned = 0
    for res in iter_epmc_search(args.query, max_results=max(1, int(args.max_results))):
        scanned += 1
        if scanned % 10 == 0:
            print(f"[progress] scanned={scanned} kept={len(candidates)}", file=sys.stderr)
        pmcid = (res.get("pmcid") or "").strip()
        if not pmcid:
            continue
        if args.require_oa and str(res.get("isOpenAccess") or "").upper() != "Y":
            continue

        root = fetch_fulltext_xml(pmcid)
        if root is None:
            continue

        seq_table_hits = 0
        endpoint_table_hits = 0
        endpoints_found: set[str] = set()
        value_cells_total = 0
        for tw in root.findall(".//{*}table-wrap"):
            caption = elem_text(tw.find("./{*}caption"))
            table_el = tw.find(".//{*}table")
            if table_el is None:
                continue
            rows = table_elem_to_matrix(table_el, max_rows=600)
            if not rows:
                continue
            headers = rows[0]
            seq_cells = count_sequence_cells(rows, min_len=8, max_scan_rows=120) if has_sequence_column(headers) else 0
            if seq_cells >= 2:
                seq_table_hits += 1
            hints = table_endpoint_hints(caption, headers)
            if hints:
                endpoints_found.update(hints)
            value_cells = count_value_cells(rows, max_scan_rows=120)
            value_cells_total += value_cells
            # Endpoint table requires both a hint and some numeric-with-unit cells.
            if hints and value_cells >= 2:
                endpoint_table_hits += 1

        score = 0
        reasons: list[str] = []
        if seq_table_hits:
            score += 3
            reasons.append(f"seq_tables={seq_table_hits}")
        if endpoint_table_hits:
            score += 3
            reasons.append(f"endpoint_tables={endpoint_table_hits}")
        if value_cells_total >= 5:
            score += 1
            reasons.append(f"value_cells>={value_cells_total}")
        if any(e in endpoints_found for e in ENDPOINT_KEYWORDS):
            score += 1
            reasons.append("numeric_endpoint_hint")

        if score < int(args.min_score):
            continue

        candidates.append(
            Candidate(
                pmcid=pmcid,
                doi=str(res.get("doi") or "").strip(),
                pmid=str(res.get("pmid") or "").strip(),
                title=normalize_whitespace(str(res.get("title") or "")),
                pub_year=str(res.get("pubYear") or "").strip(),
                journal=normalize_whitespace(str(res.get("journalTitle") or "")),
                score=score,
                reasons=";".join(reasons),
                endpoint_hints=";".join(sorted(endpoints_found)),
            )
        )
        if int(args.max_candidates) > 0 and len(candidates) >= int(args.max_candidates):
            break

    candidates.sort(key=lambda c: (-c.score, c.pub_year, c.pmcid))

    out_path = args.out
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "pmcid",
                "doi",
                "pmid",
                "pub_year",
                "journal",
                "score",
                "reasons",
                "endpoint_hints",
                "title",
            ]
        )
        for c in candidates:
            w.writerow([c.pmcid, c.doi, c.pmid, c.pub_year, c.journal, c.score, c.reasons, c.endpoint_hints, c.title])

    ids_path = args.ids_out
    with open(ids_path, "w", encoding="utf-8") as f:
        for c in candidates:
            # Prefer DOI when present; otherwise fall back to PMCID.
            f.write((c.doi if c.doi else c.pmcid) + "\n")

    print(f"Scanned: {scanned}", file=sys.stderr)
    print(f"Kept candidates: {len(candidates)}", file=sys.stderr)
    print(f"Candidates CSV: {out_path}", file=sys.stderr)
    print(f"IDs file: {ids_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
