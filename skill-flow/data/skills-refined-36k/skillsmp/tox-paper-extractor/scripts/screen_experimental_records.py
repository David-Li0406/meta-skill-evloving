#!/usr/bin/env python3
"""
Screen extracted experimental records for training readiness & audit gaps.

This is a lightweight post-processing step on top of:
  - scripts/fetch_open_access_papers.py
  - scripts/extract_paper_extractions.py

Inputs (inside --input-dir):
  - raw_experimental_records.csv
  - download_manifest.jsonl (optional, for paper listing)

Outputs (default written under --input-dir):
  - screened_experimental_records.csv (adds QC flags/fields)
  - screening_report.md (per-paper + overall summary)
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


CANONICAL_AA20 = set("ACDEFGHIKLMNPQRSTVWY")


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


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|")


def read_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Normalize key columns to strings (preserve NaN for missing values).
    for c in ("doi", "pmid", "pmcid", "paper_stem", "title", "source_kind", "peptide_id", "sequence", "endpoint", "condition", "unit"):
        if c in df.columns:
            df[c] = df[c].astype("string")
    return df


def get_context_kv(context: Any, key: str) -> str:
    s = "" if context is None else str(context)
    if not s:
        return ""
    # Context is semicolon-joined "k=v" pairs (best-effort).
    for part in s.split(";"):
        part = part.strip()
        if not part:
            continue
        if part.startswith(key + "="):
            return part[len(key) + 1 :].strip()
    return ""


AGG_STAT_RE = re.compile(r"\b(?:gm|gmm|geometric\s+mean|mean|median|average)\b", flags=re.IGNORECASE)
AGG_GROUP_RE = re.compile(
    r"\b(?:gram[-\s]*positive|gram[-\s]*negative|g\s*\+|g\s*-\b|all\b|overall\b)\b",
    flags=re.IGNORECASE,
)


def is_missing(val: Any) -> bool:
    if val is None:
        return True
    try:
        if pd.isna(val):
            return True
    except Exception:
        pass
    s = str(val)
    if s.strip() == "":
        return True
    if s.strip().lower() == "nan":
        return True
    return False


def seq_is_canonical20(seq: Any) -> bool:
    if is_missing(seq):
        return False
    s = str(seq).strip().upper()
    if not s:
        return False
    return all(ch in CANONICAL_AA20 for ch in s)


def seq_len(seq: Any) -> int:
    if is_missing(seq):
        return 0
    return len(str(seq).strip())


def detect_aggregate(condition: str, val_col_header: str) -> tuple[bool, bool, bool]:
    text = normalize_whitespace(f"{condition} {val_col_header}")
    stat = bool(AGG_STAT_RE.search(text))
    group = bool(AGG_GROUP_RE.search(text))
    return (stat or group), stat, group


@dataclass
class ManifestEntry:
    normalized: str
    stem: str
    doi: str = ""
    pmcid: str = ""
    pdf_ok: bool = False
    xml_ok: bool = False
    supp_files: int = 0


def load_manifest(run_dir: Path) -> list[ManifestEntry]:
    manifest_path = run_dir / "download_manifest.jsonl"
    if not manifest_path.exists():
        return []
    latest: dict[str, dict[str, Any]] = {}
    for line in manifest_path.read_text(encoding="utf-8", errors="ignore").splitlines():
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

    out: list[ManifestEntry] = []
    for rec in latest.values():
        normalized = str(rec.get("normalized") or rec.get("input") or "").strip()
        if not normalized:
            continue
        stem = safe_stem(normalized)
        me = ManifestEntry(normalized=normalized, stem=stem)
        actions = rec.get("actions") or []
        if isinstance(actions, list):
            for a in actions:
                if not isinstance(a, dict):
                    continue
                meta = a.get("meta") or {}
                if isinstance(meta, dict):
                    me.doi = me.doi or str(meta.get("doi") or "")
                    me.pmcid = me.pmcid or str(meta.get("pmcid") or "")
                kind = str(a.get("kind") or "")
                if kind == "pdf":
                    dl = a.get("download") or {}
                    if isinstance(dl, dict) and dl.get("status") in ("downloaded", "skipped_exists"):
                        me.pdf_ok = True
                elif kind == "xml":
                    dl = a.get("download") or {}
                    if isinstance(dl, dict) and dl.get("status") in ("downloaded", "skipped_exists"):
                        me.xml_ok = True
                elif kind == "pmc_oa_package":
                    dl = a.get("download") or {}
                    if isinstance(dl, dict) and dl.get("status") in ("downloaded", "skipped_exists"):
                        me.xml_ok = True
                        extract = a.get("extract") or {}
                        if isinstance(extract, dict):
                            me.pdf_ok = me.pdf_ok or bool(extract.get("extracted_pdf"))
                            try:
                                me.supp_files = max(me.supp_files, int(extract.get("extracted_supp_files") or 0))
                            except Exception:
                                pass

        # Ground-truth supp count from filesystem.
        supp_dir = run_dir / "supplementary" / stem
        if supp_dir.exists():
            try:
                me.supp_files = max(me.supp_files, len([p for p in supp_dir.iterdir() if p.is_file()]))
            except Exception:
                pass
        out.append(me)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, help="Directory produced by fetch_open_access_papers.py + extract_paper_extractions.py")
    ap.add_argument("--out-csv", default="", help="Output screened CSV path (default: <input-dir>/screened_experimental_records.csv)")
    ap.add_argument("--out-md", default="", help="Output screening Markdown path (default: <input-dir>/screening_report.md)")
    ap.add_argument("--min-seq-len", type=int, default=5, help="Minimum sequence length for training readiness flags")
    ap.add_argument(
        "--zero-papers-out",
        default="",
        help="Optional output txt for papers with 0 extracted experimental records (default: <input-dir>/papers_with_zero_experimental_records.txt)",
    )
    args = ap.parse_args()

    run_dir = Path(args.input_dir)
    if not run_dir.exists():
        raise SystemExit(f"Input dir not found: {run_dir}")

    in_csv = run_dir / "raw_experimental_records.csv"
    if not in_csv.exists():
        raise SystemExit(f"Missing: {in_csv}")

    out_csv = Path(args.out_csv) if args.out_csv else (run_dir / "screened_experimental_records.csv")
    out_md = Path(args.out_md) if args.out_md else (run_dir / "screening_report.md")
    out_zero = Path(args.zero_papers_out) if args.zero_papers_out else (run_dir / "papers_with_zero_experimental_records.txt")

    df = read_csv(in_csv)
    if "context" not in df.columns:
        df["context"] = ""
    if "cmp" not in df.columns:
        df["cmp"] = ""
    if "value" not in df.columns:
        df["value"] = ""

    df["val_col_header"] = df["context"].apply(lambda x: get_context_kv(x, "val_col_header"))

    df["seq_len"] = df["sequence"].apply(seq_len).astype(int)
    df["seq_is_canonical20"] = df["sequence"].apply(seq_is_canonical20).astype(bool)
    df["seq_ok_minlen"] = df["seq_len"] >= int(args.min_seq_len)

    df["unit_missing"] = df["unit"].apply(is_missing).astype(bool)
    df["value_missing"] = df["value"].apply(is_missing).astype(bool)
    df["cmp_missing"] = df["cmp"].apply(is_missing).astype(bool)
    df["is_censored"] = (~df["cmp_missing"]).astype(bool)

    def _cond_val(r: pd.Series, key: str) -> str:
        v = r.get(key)
        return "" if is_missing(v) else str(v)

    agg = df.apply(lambda r: detect_aggregate(_cond_val(r, "condition"), _cond_val(r, "val_col_header")), axis=1)
    df["is_aggregate"] = agg.apply(lambda x: bool(x[0]))
    df["is_aggregate_stat"] = agg.apply(lambda x: bool(x[1]))
    df["is_aggregate_group"] = agg.apply(lambda x: bool(x[2]))

    # Strict training readiness: numeric, unit, canonical sequence, non-aggregate, non-censored.
    df["train_ready_strict"] = (
        df["seq_ok_minlen"]
        & df["seq_is_canonical20"]
        & (~df["value_missing"])
        & (~df["unit_missing"])
        & (~df["is_aggregate"])
        & (~df["is_censored"])
    )

    # Relaxed: allow censored values, but still require unit + non-aggregate.
    df["train_ready_relaxed"] = (
        df["seq_ok_minlen"]
        & df["seq_is_canonical20"]
        & (~df["value_missing"])
        & (~df["unit_missing"])
        & (~df["is_aggregate"])
    )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    # ---- Markdown report ----
    manifest = load_manifest(run_dir)
    manifest_by_stem = {m.stem: m for m in manifest}

    lines: list[str] = []
    lines.append("# Experimental Data Screening Report")
    lines.append("")
    lines.append(f"Generated at: {now_local_str()}")
    lines.append(f"Run directory: `{run_dir}`")
    lines.append(f"Input: `{in_csv}`")
    lines.append(f"Output: `{out_csv}`")
    lines.append("")

    lines.append("## Overall")
    lines.append(f"- Records: {len(df)}")
    if "sequence" in df.columns:
        try:
            lines.append(f"- Unique sequences: {int(df['sequence'].nunique())}")
        except Exception:
            pass
    if "endpoint" in df.columns:
        vc = df["endpoint"].value_counts().head(50)
        lines.append("- Endpoints:")
        for k, v in vc.items():
            lines.append(f"  - {md_escape(str(k))}: {int(v)}")
    lines.append("")

    lines.append("## QC Flags (Counts)")
    for name in (
        "unit_missing",
        "value_missing",
        "is_censored",
        "is_aggregate",
        "seq_is_canonical20",
        "train_ready_strict",
        "train_ready_relaxed",
    ):
        if name not in df.columns:
            continue
        try:
            cnt = int(df[name].sum())
        except Exception:
            continue
        lines.append(f"- {name}: {cnt}")
    lines.append("")

    # Per-paper summary table
    lines.append("## Per-Paper Summary (Top 40 by records)")
    group_key = "paper_stem" if "paper_stem" in df.columns else None
    if not group_key:
        lines.append("- Missing `paper_stem` column; cannot group by paper.")
    else:
        g = df.groupby(group_key, dropna=False)
        summary = pd.DataFrame(
            {
                "records": g.size(),
                "unique_sequences": g["sequence"].nunique() if "sequence" in df.columns else g.size(),
                "train_ready_strict": g["train_ready_strict"].sum(),
                "train_ready_relaxed": g["train_ready_relaxed"].sum(),
                "unit_missing": g["unit_missing"].sum(),
                "censored": g["is_censored"].sum(),
                "aggregate": g["is_aggregate"].sum(),
            }
        ).sort_values("records", ascending=False)

        top = summary.head(40)
        lines.append("")
        lines.append("| paper_stem | records | uniq_seq | strict | relaxed | unit_missing | censored | aggregate | pdf | xml | supp_files |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for stem, r in top.iterrows():
            m = manifest_by_stem.get(str(stem))
            lines.append(
                "| "
                + " | ".join(
                    [
                        md_escape(str(stem)),
                        str(int(r["records"])),
                        str(int(r["unique_sequences"])),
                        str(int(r["train_ready_strict"])),
                        str(int(r["train_ready_relaxed"])),
                        str(int(r["unit_missing"])),
                        str(int(r["censored"])),
                        str(int(r["aggregate"])),
                        "1" if (m and m.pdf_ok) else "0",
                        "1" if (m and m.xml_ok) else "0",
                        str(int(m.supp_files)) if m else "0",
                    ]
                )
                + " |"
            )

        # Papers with 0 experimental records (if we have manifest)
        if manifest:
            stems_with_records = set(str(s) for s in df[group_key].dropna().unique().tolist())
            missing = [m.normalized for m in manifest if m.stem not in stems_with_records]
            if missing:
                lines.append("")
                lines.append("## Papers With 0 Extracted Experimental Records")
                lines.append(f"- total: {len(missing)}")
                lines.append(f"- full_list: `{out_zero}`")
                lines.append(f"- listed_below: first {min(200, len(missing))}")
                # Write full list for automation / follow-up worklists.
                out_zero.write_text("\n".join(missing) + "\n", encoding="utf-8")
                for x in missing[:200]:
                    lines.append(f"- {md_escape(x)}")
                if len(missing) > 200:
                    lines.append(f"- ... ({len(missing) - 200} more)")

    lines.append("")
    lines.append("## Notes")
    lines.append("- `train_ready_strict`: canonical AA20 + has unit + not aggregate + not censored; conservative for cross-paper benchmarking.")
    lines.append("- `train_ready_relaxed`: allows censored values (e.g., `> 128`) but still requires unit + non-aggregate; suitable if you model censoring explicitly.")
    lines.append("- Aggregate examples: `GM MIC`, `geometric mean`, `Gram-positive/negative` group summaries; keep separately if you want a multi-granularity benchmark.")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
