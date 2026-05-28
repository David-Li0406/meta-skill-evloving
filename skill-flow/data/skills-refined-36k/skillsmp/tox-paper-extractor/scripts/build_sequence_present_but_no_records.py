#!/usr/bin/env python3
"""
Build a "high-signal missed" list for a run: papers with 0 experimental records but with
extracted sequence + endpoint-value signals in raw_extractions.csv.

This is intended to be regenerated after any extraction rule regression, so you don't keep
deep-reading stale missed lists.

Default output schema is compatible with:
  - scripts/freeze_missed_recovery_worklist.py
  - scripts/select_missed_worklist.py

Output columns (minimum):
  - paper_stem
  - sequence_extractions
  - endpoint_value_extractions
  - experimental_records

Extra columns may be added for audit/triage.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


AA20_RE = re.compile(r"^[ACDEFGHIKLMNPQRSTVWY]+$")


def looks_like_aa_sequence(text: str, *, min_len: int) -> bool:
    s = re.sub(r"[^A-Za-z]", "", (text or "").strip().upper())
    if len(s) < min_len:
        return False
    return bool(AA20_RE.fullmatch(s))


def normalize_unit(raw: str) -> str:
    """
    Normalize units to improve recall across common variants:
      - µ vs μ
      - 'uM'/'ug/mL' micro prefix
      - case variants (mg/L vs mg/l)
      - whitespace variants

    Note: this is used for coarse filtering only (triage), not final dataset QC.
    """
    s = str(raw or "").strip()
    s = s.replace("μ", "µ")
    s = re.sub(r"\s+", "", s)
    if not s:
        return s
    # Normalize micro prefix: uM/ug/mL -> µM/µg/mL (best-effort).
    if s.startswith(("u", "U")) and len(s) > 1 and s[1].isalpha():
        s = "µ" + s[1:]
    return s


@dataclass(frozen=True)
class Config:
    min_seq_len: int
    min_sequence_extractions: int
    min_endpoint_value_extractions: int
    max_sequence_extractions: int
    endpoint_keyword_regex: str
    allowed_units: list[str]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default="", help="Run dir containing papers/ (alternative to --papers-dir)")
    ap.add_argument("--papers-dir", default="", help="Papers dir (alternative to --run-dir), e.g. runs/<run>/papers")
    ap.add_argument(
        "--out",
        default="",
        help="Output CSV path (default: <run-dir>/sequence_present_but_no_records_recomputed.csv)",
    )
    ap.add_argument("--min-seq-len", type=int, default=8, help="Minimum AA20 length for counting a sequence extraction")
    ap.add_argument("--min-sequence-extractions", type=int, default=1, help="Minimum sequence_extractions to include")
    ap.add_argument("--min-endpoint-value-extractions", type=int, default=1, help="Minimum endpoint_value_extractions to include")
    ap.add_argument("--max-sequence-extractions", type=int, default=5000, help="Filter out extreme sequence_extractions noise")
    ap.add_argument(
        "--endpoint-keywords",
        default=r"(?i)\b(MIC|MBC|MHC|IC50|EC50|CC50|HC50|HC10|LC50|LD50|hemolysis|hemolytic|minimum inhibitory concentration|cytotoxic)\b",
        help="Regex used to decide whether an endpoint_value extraction is relevant (applied to snippet+context).",
    )
    ap.add_argument(
        "--allowed-units",
        default="µM,uM,μM,nM,mM,pM,µg/mL,μg/mL,ug/mL,µg/ml,μg/ml,ug/ml,mg/L,mg/l,mg/mL,mg/ml,ng/mL,ng/ml,g/L,g/l,mg/kg,mg/Kg,%,µg/L,μg/L",
        help="Comma-separated units that count toward endpoint_value_extractions (unit is normalized by removing whitespace and using µ; includes common variants).",
    )
    ap.add_argument("--write-meta", action="store_true", help="Also write <out>.meta.json with config + summary stats")
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve() if str(args.run_dir).strip() else None
    papers_dir = Path(args.papers_dir).resolve() if str(args.papers_dir).strip() else None
    if run_dir is None and papers_dir is None:
        raise SystemExit("Either --run-dir or --papers-dir is required.")
    if papers_dir is None:
        papers_dir = run_dir / "papers"  # type: ignore[operator]
    if run_dir is None:
        run_dir = papers_dir.parent

    if not papers_dir.exists():
        raise SystemExit(f"papers dir not found: {papers_dir}")

    raw_extractions_csv = papers_dir / "raw_extractions.csv"
    raw_records_csv = papers_dir / "raw_experimental_records.csv"
    if not raw_extractions_csv.exists():
        raise SystemExit(f"missing: {raw_extractions_csv}")
    if not raw_records_csv.exists():
        raise SystemExit(f"missing: {raw_records_csv}")

    out_path = Path(args.out).resolve() if str(args.out).strip() else (run_dir / "sequence_present_but_no_records_recomputed.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    allowed_units = [normalize_unit(u) for u in str(args.allowed_units).split(",") if str(u).strip()]
    kw_re = re.compile(str(args.endpoint_keywords), flags=0)
    cfg = Config(
        min_seq_len=int(args.min_seq_len),
        min_sequence_extractions=int(args.min_sequence_extractions),
        min_endpoint_value_extractions=int(args.min_endpoint_value_extractions),
        max_sequence_extractions=int(args.max_sequence_extractions),
        endpoint_keyword_regex=str(args.endpoint_keywords),
        allowed_units=allowed_units,
    )

    df = pd.read_csv(raw_extractions_csv)
    required = {"paper_stem", "extraction_type", "entity", "unit", "snippet", "context"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"{raw_extractions_csv}: missing columns: {sorted(missing)}")

    df["paper_stem"] = df["paper_stem"].astype("string").fillna("").str.strip()
    df = df[df["paper_stem"] != ""].copy()

    # Sequence signal: only count strict AA20 sequences of sufficient length.
    seq_df = df[df["extraction_type"].astype("string").str.strip().eq("sequence")].copy()
    seq_df["entity"] = seq_df["entity"].astype("string").fillna("")
    seq_df["seq_ok"] = seq_df["entity"].map(lambda s: looks_like_aa_sequence(str(s), min_len=cfg.min_seq_len))
    seq_counts_all = seq_df.groupby("paper_stem").size().rename("sequence_extractions_raw")
    seq_counts = seq_df[seq_df["seq_ok"]].groupby("paper_stem").size().rename("sequence_extractions")

    # Endpoint-value signal: require both "assay-ish" unit and an endpoint keyword in context/snippet.
    ep_df = df[df["extraction_type"].astype("string").str.strip().eq("endpoint_value")].copy()
    ep_df["unit_norm"] = ep_df["unit"].map(normalize_unit)
    ep_df["text"] = (
        ep_df["entity"].astype("string")
        .fillna("")
        .str.cat(ep_df["snippet"].astype("string").fillna(""), sep=" | ", na_rep="")
        .str.cat(ep_df["context"].astype("string").fillna(""), sep=" | ", na_rep="")
    )
    ep_df["kw_ok"] = ep_df["text"].map(lambda t: bool(kw_re.search(str(t))))
    ep_df["unit_ok"] = ep_df["unit_norm"].isin(set(allowed_units))
    ep_counts_all = ep_df.groupby("paper_stem").size().rename("endpoint_value_extractions_raw")
    # For worklist selection we want enough candidates while still being conservative:
    # - primary signal: unit-filtered endpoint values (concentration-ish units)
    # - auxiliary signals: keyword-matched counts for ranking/triage.
    ep_counts_unit = ep_df[ep_df["unit_ok"]].groupby("paper_stem").size().rename("endpoint_value_extractions")
    ep_counts_kw = ep_df[ep_df["kw_ok"]].groupby("paper_stem").size().rename("endpoint_value_extractions_kw")
    ep_counts_kw_unit = (
        ep_df[ep_df["kw_ok"] & ep_df["unit_ok"]].groupby("paper_stem").size().rename("endpoint_value_extractions_kw_unit")
    )

    # Experimental records ground truth (0 means missed).
    rec = pd.read_csv(raw_records_csv, usecols=["paper_stem"])
    rec["paper_stem"] = rec["paper_stem"].astype("string").fillna("").str.strip()
    rec = rec[rec["paper_stem"] != ""]
    rec_counts = rec.groupby("paper_stem").size().rename("experimental_records")

    # Attempted paper set (best effort): union of stems seen in extractions, records, and local XML/PDF files.
    stems = set(df["paper_stem"].unique().tolist()) | set(rec["paper_stem"].unique().tolist())
    stems |= {p.stem for p in papers_dir.glob("*.xml")}
    stems |= {p.stem for p in papers_dir.glob("*.pdf")}
    stems |= {p.name for p in (papers_dir / "supplementary").iterdir() if p.is_dir()} if (papers_dir / "supplementary").exists() else set()

    out = pd.DataFrame({"paper_stem": sorted(stems)})
    out = out.merge(rec_counts, on="paper_stem", how="left")
    out["experimental_records"] = out["experimental_records"].fillna(0).astype(int)
    out = out.merge(seq_counts, on="paper_stem", how="left").merge(seq_counts_all, on="paper_stem", how="left")
    out = (
        out.merge(ep_counts_unit, on="paper_stem", how="left")
        .merge(ep_counts_kw, on="paper_stem", how="left")
        .merge(ep_counts_kw_unit, on="paper_stem", how="left")
        .merge(ep_counts_all, on="paper_stem", how="left")
    )
    for c in ("sequence_extractions", "sequence_extractions_raw", "endpoint_value_extractions", "endpoint_value_extractions_raw"):
        out[c] = out[c].fillna(0).astype(int)
    for c in ("endpoint_value_extractions_kw", "endpoint_value_extractions_kw_unit"):
        out[c] = out[c].fillna(0).astype(int)

    # Filter to "missed but high-signal".
    missed = out[out["experimental_records"] == 0].copy()
    missed = missed[missed["sequence_extractions"] <= cfg.max_sequence_extractions]
    missed = missed[
        (missed["sequence_extractions"] >= cfg.min_sequence_extractions)
        & (missed["endpoint_value_extractions"] >= cfg.min_endpoint_value_extractions)
    ]
    missed = missed.sort_values(
        by=["endpoint_value_extractions_kw_unit", "endpoint_value_extractions", "sequence_extractions", "paper_stem"],
        ascending=[False, False, True, True],
        kind="mergesort",
    )

    cols = [
        "paper_stem",
        "sequence_extractions",
        "endpoint_value_extractions",
        "endpoint_value_extractions_kw",
        "endpoint_value_extractions_kw_unit",
        "experimental_records",
        "sequence_extractions_raw",
        "endpoint_value_extractions_raw",
    ]
    missed[cols].to_csv(out_path, index=False)

    if args.write_meta:
        meta = {
            "kind": "sequence_present_but_no_records_recomputed",
            "version": 1,
            "generated_at": now_iso(),
            "inputs": {
                "run_dir": str(run_dir),
                "papers_dir": str(papers_dir),
                "raw_extractions_csv": str(raw_extractions_csv),
                "raw_experimental_records_csv": str(raw_records_csv),
            },
            "config": {
                "min_seq_len": cfg.min_seq_len,
                "min_sequence_extractions": cfg.min_sequence_extractions,
                "min_endpoint_value_extractions": cfg.min_endpoint_value_extractions,
                "max_sequence_extractions": cfg.max_sequence_extractions,
                "endpoint_keywords": cfg.endpoint_keyword_regex,
                "allowed_units": cfg.allowed_units,
            },
            "stats": {
                "attempted_stems": int(len(stems)),
                "missed_high_signal_rows": int(missed.shape[0]),
            },
        }
        meta_path = out_path.with_suffix(out_path.suffix + ".meta.json")
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] out: {out_path}")
    print(f"[ok] missed_high_signal_rows: {missed.shape[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
