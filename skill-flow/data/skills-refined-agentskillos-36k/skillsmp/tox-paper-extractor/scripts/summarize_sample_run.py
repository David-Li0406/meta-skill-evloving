#!/usr/bin/env python3
"""
Summarize a download+extraction run directory into simple hit/effective metrics.

Input directory should be produced by:
  - scripts/fetch_open_access_papers.py
  - scripts/extract_paper_extractions.py
  - (optional) scripts/screen_experimental_records.py

Outputs:
  - JSON metrics (machine-readable)
  - Markdown metrics (human-readable)
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


def now_local_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def read_manifest_records(papers_dir: Path) -> list[dict[str, Any]]:
    manifest = papers_dir / "download_manifest.jsonl"
    if not manifest.exists():
        return []
    latest: dict[str, dict[str, Any]] = {}
    for line in manifest.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        key = str(rec.get("normalized") or rec.get("input") or "").strip()
        if not key:
            continue
        latest[key] = rec
    return list(latest.values())


def action_download_status(action: dict[str, Any]) -> str:
    if "download" in action and isinstance(action.get("download"), dict):
        return str(action["download"].get("status") or "")
    return str(action.get("status") or "")


def has_ok_download(action: dict[str, Any]) -> bool:
    s = action_download_status(action)
    return s in ("downloaded", "skipped_exists")


@dataclass(frozen=True)
class RecordsStats:
    rows: int
    unique_sequences: int
    endpoint_counts: dict[str, int]
    papers_with_rows: int
    papers: set[str]


def summarize_records(csv_path: Path) -> RecordsStats:
    if not csv_path.exists():
        return RecordsStats(rows=0, unique_sequences=0, endpoint_counts={}, papers_with_rows=0, papers=set())

    seqs: set[str] = set()
    endpoints = Counter()
    papers: set[str] = set()
    rows = 0

    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows += 1
            paper = str(row.get("paper_stem") or "").strip()
            if paper:
                papers.add(paper)
            seq = str(row.get("sequence") or "").strip()
            if seq:
                seqs.add(seq)
            ep = str(row.get("endpoint") or "").strip()
            if ep:
                endpoints[ep] += 1

    return RecordsStats(
        rows=rows,
        unique_sequences=len(seqs),
        endpoint_counts=dict(endpoints.most_common()),
        papers_with_rows=len(papers),
        papers=papers,
    )


def summarize_screened(csv_path: Path) -> dict[str, Any]:
    if not csv_path.exists():
        return {
            "rows": 0,
            "papers_with_rows": 0,
            "train_ready_strict_rows": 0,
            "train_ready_relaxed_rows": 0,
            "papers_with_train_ready_strict": 0,
            "papers_with_train_ready_relaxed": 0,
        }

    rows = 0
    strict_rows = 0
    relaxed_rows = 0
    papers_strict: set[str] = set()
    papers_relaxed: set[str] = set()
    papers_any: set[str] = set()

    def truthy(raw: str) -> bool:
        return str(raw or "").strip().lower() in ("1", "true", "t", "yes", "y")

    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows += 1
            paper = str(row.get("paper_stem") or "").strip()
            if paper:
                papers_any.add(paper)
            if truthy(row.get("train_ready_strict")):
                strict_rows += 1
                if paper:
                    papers_strict.add(paper)
            if truthy(row.get("train_ready_relaxed")):
                relaxed_rows += 1
                if paper:
                    papers_relaxed.add(paper)

    return {
        "rows": rows,
        "papers_with_rows": len(papers_any),
        "train_ready_strict_rows": strict_rows,
        "train_ready_relaxed_rows": relaxed_rows,
        "papers_with_train_ready_strict": len(papers_strict),
        "papers_with_train_ready_relaxed": len(papers_relaxed),
    }


def safe_div(num: int, den: int) -> float:
    if den <= 0:
        return 0.0
    return float(num) / float(den)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers-dir", required=True, help="Directory produced by fetch_open_access_papers.py")
    ap.add_argument("--out-json", default="", help="Write metrics JSON here (default: <papers-dir>/sample_metrics.json)")
    ap.add_argument("--out-md", default="", help="Write metrics Markdown here (default: <papers-dir>/sample_metrics.md)")
    args = ap.parse_args()

    papers_dir = Path(args.papers_dir).resolve()
    if not papers_dir.exists():
        raise SystemExit(f"--papers-dir not found: {papers_dir}")

    manifest_recs = read_manifest_records(papers_dir)
    attempted = len(manifest_recs)

    xml_ok = 0
    pdf_ok = 0
    supp_any = 0
    pmc_pkg_ok = 0

    for rec in manifest_recs:
        actions = rec.get("actions") or []
        if not isinstance(actions, list):
            continue
        ok_by_kind: dict[str, bool] = defaultdict(bool)
        for a in actions:
            if not isinstance(a, dict):
                continue
            kind = str(a.get("kind") or "").strip()
            if not kind:
                continue
            if kind == "supplementary":
                # Treat either "downloaded/skipped_exists" supplementary actions OR extracted files from PMC package as "has supp".
                if has_ok_download(a):
                    ok_by_kind["supplementary"] = True
            elif kind in ("xml", "pdf", "pmc_oa_package"):
                if has_ok_download(a):
                    ok_by_kind[kind] = True
                if kind == "pmc_oa_package":
                    extract = a.get("extract") or {}
                    if isinstance(extract, dict):
                        if bool(extract.get("extracted_pdf")):
                            ok_by_kind["pdf"] = True
                        try:
                            if int(extract.get("extracted_supp_files") or 0) > 0:
                                ok_by_kind["supplementary"] = True
                        except Exception:
                            pass

        if ok_by_kind.get("xml"):
            xml_ok += 1
        if ok_by_kind.get("pdf"):
            pdf_ok += 1
        if ok_by_kind.get("pmc_oa_package"):
            pmc_pkg_ok += 1
        # If any supplementary directory exists for this record, count it.
        # This is a coarse indicator; actual file count should be inspected in extraction_report.md.
        stem = str(rec.get("normalized") or rec.get("input") or "").strip()
        if stem and (papers_dir / "supplementary" / stem).exists():
            supp_any += 1

    raw_records = summarize_records(papers_dir / "raw_experimental_records.csv")
    screened = summarize_screened(papers_dir / "screened_experimental_records.csv")

    metrics: dict[str, Any] = {
        "generated_at": now_local_str(),
        "papers_dir": str(papers_dir),
        "attempted_papers": attempted,
        "download_ok": {
            "xml_ok_papers": xml_ok,
            "pdf_ok_papers": pdf_ok,
            "supp_dir_present_papers": supp_any,
            "pmc_oa_package_ok_papers": pmc_pkg_ok,
        },
        "extraction": {
            "papers_with_experimental_rows": raw_records.papers_with_rows,
            "experimental_rows": raw_records.rows,
            "unique_sequences": raw_records.unique_sequences,
            "endpoint_counts": raw_records.endpoint_counts,
        },
        "screening": screened,
    }

    # Derived ratios
    n_hit = int(raw_records.papers_with_rows)
    n_effective_strict = int(screened.get("papers_with_train_ready_strict") or 0)
    n_effective_relaxed = int(screened.get("papers_with_train_ready_relaxed") or 0)

    metrics["rates"] = {
        "hit_rate_attempted": safe_div(n_hit, attempted),
        "hit_rate_given_xml_ok": safe_div(n_hit, xml_ok),
        "effective_rate_strict_attempted": safe_div(n_effective_strict, attempted),
        "effective_rate_relaxed_attempted": safe_div(n_effective_relaxed, attempted),
        "effective_rate_strict_given_hit": safe_div(n_effective_strict, n_hit),
        "effective_rate_relaxed_given_hit": safe_div(n_effective_relaxed, n_hit),
        "train_ready_strict_row_rate": safe_div(int(screened.get("train_ready_strict_rows") or 0), int(screened.get("rows") or 0)),
        "train_ready_relaxed_row_rate": safe_div(int(screened.get("train_ready_relaxed_rows") or 0), int(screened.get("rows") or 0)),
    }

    out_json = Path(args.out_json).resolve() if args.out_json else (papers_dir / "sample_metrics.json")
    out_md = Path(args.out_md).resolve() if args.out_md else (papers_dir / "sample_metrics.md")

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Markdown
    lines: list[str] = []
    lines.append("# Sample Run Metrics")
    lines.append("")
    lines.append(f"Generated at: {metrics['generated_at']}")
    lines.append(f"Papers dir: `{papers_dir}`")
    lines.append("")
    lines.append("## Download")
    lines.append(f"- attempted_papers: {attempted}")
    lines.append(f"- xml_ok_papers: {xml_ok}")
    lines.append(f"- pdf_ok_papers: {pdf_ok}")
    lines.append(f"- supp_dir_present_papers: {supp_any}")
    lines.append(f"- pmc_oa_package_ok_papers: {pmc_pkg_ok}")
    lines.append("")
    lines.append("## Extraction")
    lines.append(f"- papers_with_experimental_rows: {raw_records.papers_with_rows}")
    lines.append(f"- experimental_rows: {raw_records.rows}")
    lines.append(f"- unique_sequences: {raw_records.unique_sequences}")
    lines.append("")
    lines.append("## Screening")
    lines.append(f"- train_ready_strict_rows: {screened.get('train_ready_strict_rows', 0)}")
    lines.append(f"- train_ready_relaxed_rows: {screened.get('train_ready_relaxed_rows', 0)}")
    lines.append(f"- papers_with_train_ready_strict: {screened.get('papers_with_train_ready_strict', 0)}")
    lines.append(f"- papers_with_train_ready_relaxed: {screened.get('papers_with_train_ready_relaxed', 0)}")
    lines.append("")
    lines.append("## Rates")
    for k, v in metrics["rates"].items():
        lines.append(f"- {k}: {v:.4f}")
    lines.append("")
    lines.append("## Top Endpoints (by rows)")
    for ep, cnt in list(raw_records.endpoint_counts.items())[:30]:
        lines.append(f"- {ep}: {cnt}")
    lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[ok] wrote: {out_json}")
    print(f"[ok] wrote: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
