#!/usr/bin/env python3
"""
Generate a compact, auditable Markdown report for one download+extraction run.

Input directory should be produced by fetch_open_access_papers.py and then processed by
extract_paper_extractions.py, e.g.:

  run_dir/
    download_manifest.jsonl
    raw_extractions.csv
    raw_experimental_records.csv
    extracted_tables/
    supplementary/

This report is designed for "LLM monitoring": it summarizes what was downloaded/extracted,
highlights gaps, and provides clickable pointers (file paths + table ids + row/col indices).
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd


def now_local_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def safe_stem(text: str, max_len: int = 120) -> str:
    s = (text or "").strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[^\w.\-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = "paper"
    return s[:max_len]


@dataclass
class ManifestSummary:
    normalized: str
    input_id: str
    id_type: str
    retrieved_at: str
    doi: str = ""
    pmid: str = ""
    pmcid: str = ""
    pdf_ok: bool = False
    xml_ok: bool = False
    pmc_oa_package_ok: bool = False
    extracted_pdf_from_pmc: bool = False
    extracted_supp_files_from_pmc: int = 0
    supp_any_ok: bool = False
    notes: str = ""


def load_manifest_latest(manifest_path: Path) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for line in manifest_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        key = str(rec.get("normalized") or rec.get("input") or "")
        if not key:
            continue
        latest[key] = rec
    return list(latest.values())


def action_download_ok(action: dict[str, Any]) -> bool:
    dl = action.get("download")
    if isinstance(dl, dict):
        return dl.get("status") in ("downloaded", "skipped_exists")
    return False


def summarize_manifest(run_dir: Path) -> list[ManifestSummary]:
    manifest_path = run_dir / "download_manifest.jsonl"
    if not manifest_path.exists():
        return []

    out: list[ManifestSummary] = []
    for rec in load_manifest_latest(manifest_path):
        normalized = str(rec.get("normalized") or rec.get("input") or "").strip()
        input_id = str(rec.get("input") or "").strip()
        id_type = str(rec.get("id_type") or "").strip()
        retrieved_at = str(rec.get("retrieved_at") or "").strip()

        ms = ManifestSummary(normalized=normalized, input_id=input_id, id_type=id_type, retrieved_at=retrieved_at)

        actions = rec.get("actions") or []
        if isinstance(actions, list):
            for a in actions:
                if not isinstance(a, dict):
                    continue
                kind = str(a.get("kind") or "")
                meta = a.get("meta") or {}
                if isinstance(meta, dict):
                    ms.doi = ms.doi or str(meta.get("doi") or "")
                    ms.pmid = ms.pmid or str(meta.get("pmid") or "")
                    ms.pmcid = ms.pmcid or str(meta.get("pmcid") or "")

                if kind == "pdf":
                    # For PDF we accept either a direct PDF download or later extraction from PMC OA package.
                    if action_download_ok(a):
                        ms.pdf_ok = True
                elif kind == "xml":
                    if action_download_ok(a):
                        ms.xml_ok = True
                elif kind == "supplementary":
                    if action_download_ok(a):
                        ms.supp_any_ok = True
                elif kind == "pmc_oa_package":
                    if action_download_ok(a):
                        ms.pmc_oa_package_ok = True
                        extract = a.get("extract") or {}
                        if isinstance(extract, dict):
                            ms.extracted_pdf_from_pmc = bool(extract.get("extracted_pdf"))
                            try:
                                ms.extracted_supp_files_from_pmc = int(extract.get("extracted_supp_files") or 0)
                            except Exception:
                                ms.extracted_supp_files_from_pmc = 0

        if ms.extracted_pdf_from_pmc:
            ms.pdf_ok = True
        if ms.extracted_supp_files_from_pmc > 0:
            ms.supp_any_ok = True

        # Local FS cross-check for supplementary folder (ground truth).
        stem = safe_stem(normalized)
        supp_dir = run_dir / "supplementary" / stem
        if supp_dir.exists():
            try:
                file_cnt = len([p for p in supp_dir.iterdir() if p.is_file()])
            except Exception:
                file_cnt = 0
            if file_cnt > 0:
                ms.supp_any_ok = True
            if file_cnt > ms.extracted_supp_files_from_pmc:
                ms.extracted_supp_files_from_pmc = file_cnt

        out.append(ms)

    return out


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|")


def read_csv_if_exists(path: Path) -> Optional[pd.DataFrame]:
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, help="Directory containing manifest + extraction outputs")
    ap.add_argument("--out", default="", help="Output Markdown path (default: <input-dir>/extraction_report.md)")
    ap.add_argument("--max-examples", type=int, default=12, help="Max sample rows to include")
    args = ap.parse_args()

    run_dir = Path(args.input_dir)
    if not run_dir.exists():
        raise SystemExit(f"Input dir not found: {run_dir}")

    out_path = Path(args.out) if args.out else (run_dir / "extraction_report.md")

    manifest = summarize_manifest(run_dir)

    raw_extractions = read_csv_if_exists(run_dir / "raw_extractions.csv")
    raw_experimental = read_csv_if_exists(run_dir / "raw_experimental_records.csv")

    extracted_tables_dir = run_dir / "extracted_tables"
    extracted_tables_cnt = len(list(extracted_tables_dir.glob("*.csv"))) if extracted_tables_dir.exists() else 0

    lines: list[str] = []
    lines.append("# Extraction Run Report")
    lines.append("")
    lines.append(f"Generated at: {now_local_str()}")
    lines.append(f"Run directory: `{run_dir}`")
    lines.append("")

    # Download summary
    lines.append("## Download Summary")
    if not manifest:
        lines.append("- Missing `download_manifest.jsonl` (cannot summarize downloads).")
    else:
        total = len(manifest)
        pdf_ok = sum(1 for m in manifest if m.pdf_ok)
        xml_ok = sum(1 for m in manifest if m.xml_ok)
        supp_ok = sum(1 for m in manifest if m.supp_any_ok)
        pmc_pkg = sum(1 for m in manifest if m.pmc_oa_package_ok)
        lines.append(f"- Papers: {total}")
        lines.append(f"- PDF available: {pdf_ok}")
        lines.append(f"- JATS XML available: {xml_ok}")
        lines.append(f"- Supplementary files available: {supp_ok}")
        lines.append(f"- Used PMC OA package fallback: {pmc_pkg}")
        lines.append("")
        lines.append("| normalized | DOI | PMCID | PDF | XML | supp_files |")
        lines.append("|---|---|---|---:|---:|---:|")
        for m in sorted(manifest, key=lambda x: x.normalized):
            lines.append(
                "| "
                + " | ".join(
                    [
                        md_escape(m.normalized),
                        md_escape(m.doi),
                        md_escape(m.pmcid),
                        "1" if m.pdf_ok else "0",
                        "1" if m.xml_ok else "0",
                        str(m.extracted_supp_files_from_pmc or 0),
                    ]
                )
                + " |"
            )

    lines.append("")

    # Extraction summary
    lines.append("## Extraction Summary")
    lines.append(f"- Extracted tables CSV count: {extracted_tables_cnt} (in `{extracted_tables_dir}`)")
    if raw_extractions is None:
        lines.append("- Missing/invalid `raw_extractions.csv`.")
    else:
        lines.append(f"- `raw_extractions.csv` rows: {len(raw_extractions)}")
        if "extraction_type" in raw_extractions.columns:
            ct = raw_extractions["extraction_type"].value_counts().head(12)
            lines.append("- Top extraction types:")
            for k, v in ct.items():
                lines.append(f"  - {md_escape(str(k))}: {int(v)}")

    if raw_experimental is None:
        lines.append("- Missing/invalid `raw_experimental_records.csv`.")
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    lines.append("")
    lines.append("## Experimental Records (Sequence × Endpoint × Value)")
    lines.append(f"- `raw_experimental_records.csv` rows: {len(raw_experimental)}")
    if "sequence" in raw_experimental.columns:
        try:
            lines.append(f"- Unique sequences: {int(raw_experimental['sequence'].nunique())}")
        except Exception:
            pass
    if "endpoint" in raw_experimental.columns:
        vc = raw_experimental["endpoint"].value_counts().head(20)
        lines.append("- Endpoints:")
        for k, v in vc.items():
            lines.append(f"  - {md_escape(str(k))}: {int(v)}")

    if "paper_stem" in raw_experimental.columns:
        per_paper = raw_experimental.groupby("paper_stem").size().sort_values(ascending=False).head(30)
        lines.append("- Top papers by record count:")
        for k, v in per_paper.items():
            lines.append(f"  - {md_escape(str(k))}: {int(v)}")

    # Highlight gaps: downloaded papers with zero experimental rows
    if manifest and "paper_stem" in raw_experimental.columns:
        stems_with_records = set(str(s) for s in raw_experimental["paper_stem"].dropna().unique().tolist())
        missing: list[str] = []
        for m in manifest:
            stem = safe_stem(m.normalized)
            if stem not in stems_with_records:
                missing.append(m.normalized)
        if missing:
            lines.append("- Papers with 0 experimental records (likely figures-only, or endpoints not in tables/supp):")
            for x in missing[:50]:
                lines.append(f"  - {md_escape(x)}")

    # Sample rows for audit
    cols = [c for c in ("doi", "pmcid", "peptide_id", "sequence", "endpoint", "condition", "value", "unit", "source_ref") if c in raw_experimental.columns]
    if cols:
        lines.append("")
        lines.append("## Samples (Audit Pointers)")
        lines.append("Each row points back to a specific table cell via `source_ref`.")
        lines.append("")
        sample = raw_experimental.copy()
        if "endpoint" in sample.columns:
            # Try to cover diverse endpoints.
            parts = []
            for ep, sub in sample.groupby("endpoint"):
                parts.append(sub.head(max(1, int(args.max_examples) // max(1, sample["endpoint"].nunique()))))
            sample = pd.concat(parts, ignore_index=True) if parts else sample
        sample = sample.head(max(1, int(args.max_examples)))
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join(["---"] * len(cols)) + "|")
        for _, r in sample.iterrows():
            row = []
            for c in cols:
                row.append(md_escape(normalize_whitespace(str(r.get(c, "")))))
            lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("## Notes / Known Limits")
    lines.append("- Figure-only numeric data (plots) is not digitized in this pipeline; prefer authors' supplementary source tables when available.")
    lines.append("- If an endpoint is only mentioned in captions/footnotes and values are unitless, manual curation may still be required.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

