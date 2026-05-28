#!/usr/bin/env python3
"""
Build a reproducible union dataset from two sample200 runs (400 papers total),
produce strict/relaxed subsets, generate leakage-safe splits, and write audit reports.

Inputs (read-only; do NOT modify):
  - runs/<run>/papers/screened_experimental_records_with_methods.csv
  - runs/<run>/papers/screened_experimental_records.csv
  - runs/<run>/papers/raw_experimental_records.csv
  - runs/<run>/papers/download_manifest.jsonl
  - runs/<run>/sample200_metrics.json/.md
  - runs/<run>/sequence_present_but_no_records.csv

Outputs (under --out-dir):
  - records_union.csv.gz / records_union.parquet
  - dataset_strict.parquet / dataset_relaxed.parquet
  - splits/{split_by_paper,split_by_sequence}/...
  - reports/metrics_recompute_vs_official.md
  - reports/dataset_profile.md
  - TASK_PLAN.md
  - config.json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


def now_iso8601_local() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def truthy(raw: Any) -> bool:
    if raw is None:
        return False
    s = str(raw).strip().lower()
    return s in ("1", "true", "t", "yes", "y")


def norm_str(x: Any) -> str | None:
    if x is None:
        return None
    if isinstance(x, float) and np.isnan(x):
        return None
    s = str(x).strip()
    return s if s else None


def norm_optional_int_str(x: Any) -> str | None:
    s = norm_str(x)
    if s is None:
        return None
    try:
        # Handles "123.0" from CSV float parsing
        f = float(s)
        if np.isfinite(f) and abs(f - int(f)) < 1e-9:
            return str(int(f))
    except Exception:
        pass
    return s


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


BOOL_COLS = [
    "seq_is_canonical20",
    "seq_ok_minlen",
    "unit_missing",
    "value_missing",
    "cmp_missing",
    "is_censored",
    "is_aggregate",
    "is_aggregate_stat",
    "is_aggregate_group",
    "train_ready_strict",
    "train_ready_relaxed",
]

ID_COLS = [
    "doi",
    "pmid",
    "pmcid",
    "paper_stem",
    "source_kind",
    "source_path",
    "source_ref",
    "peptide_id",
    "sequence_raw",
    "sequence",
    "endpoint",
    "condition",
    "unit",
    "cmp",
    "conditions",
    "snippet",
    "context",
]

NUM_COLS = [
    "value",
    "error",
    "range_low",
    "range_high",
    "seq_len",
]


def normalize_screened_df(df: pd.DataFrame, *, run_id: str) -> pd.DataFrame:
    df = df.copy()
    df.insert(0, "run_id", run_id)

    # Ensure all expected columns exist (union schema).
    for c in BOOL_COLS + ID_COLS + NUM_COLS + ["extracted_at", "title", "val_col_header"] + [
        "method_sec_titles",
        "method_evidence",
        "method_source_ref",
        "method_guideline",
        "method_assay_method",
        "method_medium",
        "method_inoculum",
        "method_incubation",
        "method_plate",
        "method_volume",
        "method_readout",
        "method_rbc_source",
        "method_rbc_conc",
    ]:
        if c not in df.columns:
            df[c] = pd.NA

    # IDs as strings (nullable)
    for c in ID_COLS + ["title", "extracted_at", "val_col_header", "run_id"]:
        if c in df.columns:
            df[c] = df[c].map(norm_str).astype("string")

    if "pmid" in df.columns:
        df["pmid"] = df["pmid"].map(norm_optional_int_str).astype("string")

    # Numerics
    for c in NUM_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Booleans
    for c in BOOL_COLS:
        if c in df.columns:
            df[c] = df[c].map(truthy).astype("boolean")

    # Keep a consistent column order (stable across runs)
    preferred = [
        "run_id",
        "extracted_at",
        "doi",
        "pmid",
        "pmcid",
        "paper_stem",
        "title",
        "source_kind",
        "source_path",
        "source_ref",
        "peptide_id",
        "sequence_raw",
        "sequence",
        "endpoint",
        "condition",
        "cmp",
        "value",
        "error",
        "range_low",
        "range_high",
        "unit",
        "conditions",
        "snippet",
        "context",
        "val_col_header",
        "seq_len",
        "seq_is_canonical20",
        "seq_ok_minlen",
        "unit_missing",
        "value_missing",
        "cmp_missing",
        "is_censored",
        "is_aggregate",
        "is_aggregate_stat",
        "is_aggregate_group",
        "train_ready_strict",
        "train_ready_relaxed",
        "method_sec_titles",
        "method_evidence",
        "method_source_ref",
        "method_guideline",
        "method_assay_method",
        "method_medium",
        "method_inoculum",
        "method_incubation",
        "method_plate",
        "method_volume",
        "method_readout",
        "method_rbc_source",
        "method_rbc_conc",
    ]
    cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
    return df[cols]


def build_primary_key(df: pd.DataFrame) -> pd.Series:
    strong_cols = ["source_kind", "source_path", "source_ref", "endpoint"]
    weak_cols = ["pmcid", "peptide_id", "sequence", "endpoint", "condition", "value", "unit", "cmp"]

    strong_ok = pd.Series(True, index=df.index)
    for c in strong_cols:
        strong_ok &= df[c].notna() & (df[c].astype("string").str.strip() != "")

    def join_cols(cols: list[str]) -> pd.Series:
        parts: list[pd.Series] = []
        for c in cols:
            if c in ("value",):
                # Stable text key for floats
                v = pd.to_numeric(df[c], errors="coerce")
                parts.append(v.map(lambda x: "" if pd.isna(x) else f"{float(x):.12g}").astype("string"))
            else:
                parts.append(df[c].fillna("").astype("string").str.strip())
        out = parts[0]
        for p in parts[1:]:
            out = out + "||" + p
        return out

    pk = pd.Series("", index=df.index, dtype="string")
    pk.loc[strong_ok] = "strong||" + join_cols(strong_cols).loc[strong_ok]
    pk.loc[~strong_ok] = "weak||" + join_cols(weak_cols).loc[~strong_ok]
    return pk


def dedupe_records(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    df = df.copy()
    df["_primary_key"] = build_primary_key(df)
    before = len(df)
    df = df.drop_duplicates(subset=["_primary_key"], keep="first").drop(columns=["_primary_key"])
    after = len(df)
    return df, {"rows_before": before, "rows_after": after, "dropped": before - after}


def paper_group_id(df: pd.DataFrame) -> pd.Series:
    # Prefer PMCID; then paper_stem; then DOI/PMID; finally a deterministic fallback.
    pmcid = df.get("pmcid", pd.Series([pd.NA] * len(df), index=df.index)).astype("string")
    paper_stem = df.get("paper_stem", pd.Series([pd.NA] * len(df), index=df.index)).astype("string")
    doi = df.get("doi", pd.Series([pd.NA] * len(df), index=df.index)).astype("string")
    pmid = df.get("pmid", pd.Series([pd.NA] * len(df), index=df.index)).astype("string")

    out = pmcid.copy()
    out = out.fillna(paper_stem)
    out = out.fillna(doi)
    out = out.fillna(pmid)
    out = out.fillna("UNKNOWN_PAPER")
    return out.astype("string")


def sequence_group_id(df: pd.DataFrame, *, paper_ids: pd.Series) -> tuple[pd.Series, dict[str, Any]]:
    seq = df.get("sequence", pd.Series([pd.NA] * len(df), index=df.index)).astype("string")
    seq_clean = seq.fillna("").str.strip()
    missing = seq_clean == ""
    group = seq_clean.mask(missing, other=paper_ids)
    info = {
        "rows_total": int(len(df)),
        "rows_sequence_missing": int(missing.sum()),
        "rows_sequence_missing_ratio": float(missing.mean()) if len(df) else 0.0,
    }
    return group.astype("string"), info


@dataclass(frozen=True)
class SplitIds:
    train: list[str]
    valid: list[str]
    test: list[str]


def split_group_ids(group_ids: Iterable[str], *, seed: int, ratios: tuple[float, float, float]) -> SplitIds:
    gids = [g for g in group_ids if g is not None and str(g).strip()]
    gids = sorted(set(map(str, gids)))
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(gids))
    gids_shuf = [gids[i] for i in perm]

    n = len(gids_shuf)
    train_ratio, valid_ratio, test_ratio = ratios
    if abs((train_ratio + valid_ratio + test_ratio) - 1.0) > 1e-9:
        raise ValueError(f"ratios must sum to 1.0, got {ratios}")

    n_train = int(n * train_ratio)
    n_valid = int(n * valid_ratio)
    n_test = n - n_train - n_valid
    if n_train <= 0 or n_valid <= 0 or n_test <= 0:
        raise ValueError(f"split too small: n={n}, counts={(n_train, n_valid, n_test)}")

    train = gids_shuf[:n_train]
    valid = gids_shuf[n_train : n_train + n_valid]
    test = gids_shuf[n_train + n_valid :]
    return SplitIds(train=train, valid=valid, test=test)


def write_ids(out_dir: Path, ids: SplitIds) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    def w_txt(name: str, rows: list[str]) -> None:
        (out_dir / f"{name}.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")

    def w_json(name: str, rows: list[str]) -> None:
        (out_dir / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    w_txt("train_ids", ids.train)
    w_txt("valid_ids", ids.valid)
    w_txt("test_ids", ids.test)
    w_json("train_ids", ids.train)
    w_json("valid_ids", ids.valid)
    w_json("test_ids", ids.test)


def filter_by_groups(df: pd.DataFrame, group_col: str, keep: set[str]) -> pd.DataFrame:
    return df[df[group_col].astype("string").isin(pd.Series(sorted(keep), dtype="string"))].copy()


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    ensure_parent(path)
    df.to_parquet(path, index=False)

def cleanup_legacy_split_files(scheme_dir: Path) -> None:
    # Earlier drafts used a flat file layout directly under scheme_dir.
    # Keep the directory self-contained by removing those known legacy files.
    for name in [
        "train_ids.txt",
        "valid_ids.txt",
        "test_ids.txt",
        "train_ids.json",
        "valid_ids.json",
        "test_ids.json",
        "union_train.parquet",
        "union_valid.parquet",
        "union_test.parquet",
        "strict_train.parquet",
        "strict_valid.parquet",
        "strict_test.parquet",
        "relaxed_train.parquet",
        "relaxed_valid.parquet",
        "relaxed_test.parquet",
    ]:
        p = scheme_dir / name
        try:
            p.unlink()
        except FileNotFoundError:
            pass


def write_union_outputs(
    union_df: pd.DataFrame,
    *,
    out_dir: Path,
) -> dict[str, Any]:
    out_union_csv = out_dir / "records_union.csv.gz"
    out_union_parquet = out_dir / "records_union.parquet"

    ensure_parent(out_union_csv)
    union_df.to_csv(out_union_csv, index=False, compression="gzip")
    write_parquet(union_df, out_union_parquet)
    return {"records_union_csv_gz": str(out_union_csv), "records_union_parquet": str(out_union_parquet)}


def subset_and_write(union_df: pd.DataFrame, *, out_dir: Path) -> dict[str, Any]:
    strict = union_df[union_df["train_ready_strict"].fillna(False)].copy()
    relaxed = union_df[union_df["train_ready_relaxed"].fillna(False)].copy()

    out_strict = out_dir / "dataset_strict.parquet"
    out_relaxed = out_dir / "dataset_relaxed.parquet"
    write_parquet(strict, out_strict)
    write_parquet(relaxed, out_relaxed)

    return {
        "strict_rows": int(len(strict)),
        "relaxed_rows": int(len(relaxed)),
        "dataset_strict_parquet": str(out_strict),
        "dataset_relaxed_parquet": str(out_relaxed),
    }

def make_split_artifacts_for_df(
    *,
    df: pd.DataFrame,
    scheme_dir: Path,
    dataset_name: str,
    scheme: str,
    seed: int,
    ratios: tuple[float, float, float],
) -> dict[str, Any]:
    dataset_dir = scheme_dir / dataset_name
    dataset_dir.mkdir(parents=True, exist_ok=True)

    df1 = df.copy()
    df1["paper_group_id"] = paper_group_id(df1)
    if scheme == "split_by_paper":
        group_col = "paper_group_id"
        extra: dict[str, Any] = {"definition": "group by pmcid (fallback: paper_stem/doi/pmid)"}
    elif scheme == "split_by_sequence":
        group_col = "sequence_group_id"
        gids, seq_info = sequence_group_id(df1, paper_ids=df1["paper_group_id"])
        df1[group_col] = gids
        extra = {"definition": "group by sequence; if sequence missing -> fallback to paper_group_id", **seq_info}
    else:
        raise ValueError(f"unknown scheme: {scheme}")

    ids = split_group_ids(df1[group_col].dropna().astype("string").tolist(), seed=seed, ratios=ratios)
    write_ids(dataset_dir, ids)

    for split_name, keep_ids in [("train", set(ids.train)), ("valid", set(ids.valid)), ("test", set(ids.test))]:
        out_p = dataset_dir / f"{split_name}.parquet"
        write_parquet(filter_by_groups(df1, group_col, keep=set(keep_ids)), out_p)

    return {
        "dataset": dataset_name,
        "group_col": group_col,
        "group_counts": {"train": len(ids.train), "valid": len(ids.valid), "test": len(ids.test), "total": len(set(ids.train + ids.valid + ids.test))},
        "extra_info": extra,
        "rows": int(len(df)),
    }


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


def summarize_records_papers(csv_path: Path) -> set[str]:
    if not csv_path.exists():
        return set()
    papers: set[str] = set()
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            paper = str(row.get("paper_stem") or "").strip()
            if paper:
                papers.add(paper)
    return papers


def summarize_screened_papers(csv_path: Path) -> tuple[set[str], set[str]]:
    if not csv_path.exists():
        return set(), set()
    strict: set[str] = set()
    relaxed: set[str] = set()
    with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            paper = str(row.get("paper_stem") or "").strip()
            if not paper:
                continue
            if truthy(row.get("train_ready_strict")):
                strict.add(paper)
            if truthy(row.get("train_ready_relaxed")):
                relaxed.add(paper)
    return strict, relaxed


def recompute_run_metrics(run_dir: Path) -> dict[str, Any]:
    papers_dir = run_dir / "papers"
    manifest_recs = read_manifest_records(papers_dir)
    attempted = int(len(manifest_recs))

    xml_ok = 0
    for rec in manifest_recs:
        actions = rec.get("actions") or []
        if not isinstance(actions, list):
            continue
        ok_xml = False
        for a in actions:
            if not isinstance(a, dict):
                continue
            kind = str(a.get("kind") or "").strip()
            if kind != "xml":
                continue
            if has_ok_download(a):
                ok_xml = True
                break
        if ok_xml:
            xml_ok += 1

    hit_papers = summarize_records_papers(papers_dir / "raw_experimental_records.csv")
    strict_papers, relaxed_papers = summarize_screened_papers(papers_dir / "screened_experimental_records.csv")

    n_hit = int(len(hit_papers))
    n_effective_strict = int(len(strict_papers))
    n_effective_relaxed = int(len(relaxed_papers))

    def safe_div(num: int, den: int) -> float:
        return float(num) / float(den) if den > 0 else 0.0

    return {
        "N": attempted,
        "N_xml_ok": int(xml_ok),
        "N_hit": n_hit,
        "N_effective_strict": n_effective_strict,
        "N_effective_relaxed": n_effective_relaxed,
        "hit_rate_attempted": safe_div(n_hit, attempted),
        "hit_rate_given_xml_ok": safe_div(n_hit, int(xml_ok)),
        "effective_rate_strict_attempted": safe_div(n_effective_strict, attempted),
        "effective_rate_relaxed_attempted": safe_div(n_effective_relaxed, attempted),
    }


def load_official_metrics(run_dir: Path) -> dict[str, Any] | None:
    p = run_dir / "sample200_metrics.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def compare_metrics(recomputed: dict[str, Any], official: dict[str, Any] | None) -> dict[str, Any]:
    if official is None:
        return {"official_present": False, "diff": {}}
    # Official schema matches scripts/summarize_sample_run.py
    official_flat = {
        "N": int(official.get("attempted_papers") or 0),
        "N_xml_ok": int(((official.get("download_ok") or {}) or {}).get("xml_ok_papers") or 0),
        "N_hit": int(((official.get("extraction") or {}) or {}).get("papers_with_experimental_rows") or 0),
        "N_effective_strict": int(((official.get("screening") or {}) or {}).get("papers_with_train_ready_strict") or 0),
        "N_effective_relaxed": int(((official.get("screening") or {}) or {}).get("papers_with_train_ready_relaxed") or 0),
        "hit_rate_attempted": float(((official.get("rates") or {}) or {}).get("hit_rate_attempted") or 0.0),
        "hit_rate_given_xml_ok": float(((official.get("rates") or {}) or {}).get("hit_rate_given_xml_ok") or 0.0),
        "effective_rate_strict_attempted": float(((official.get("rates") or {}) or {}).get("effective_rate_strict_attempted") or 0.0),
        "effective_rate_relaxed_attempted": float(((official.get("rates") or {}) or {}).get("effective_rate_relaxed_attempted") or 0.0),
    }
    diff: dict[str, Any] = {}
    for k in recomputed.keys():
        a = recomputed.get(k)
        b = official_flat.get(k)
        if isinstance(a, float) or isinstance(b, float):
            ok = abs(float(a) - float(b)) <= 1e-9
        else:
            ok = a == b
        if not ok:
            diff[k] = {"recomputed": a, "official": b}
    return {"official_present": True, "diff": diff, "official_flat": official_flat}


def write_metrics_reconcile_report(
    *,
    out_path: Path,
    runs: list[tuple[str, Path]],
    generated_at: str,
    notes: list[str],
) -> dict[str, Any]:
    ensure_parent(out_path)

    rows = []
    diffs: dict[str, Any] = {}
    for run_id, run_dir in runs:
        rec = recompute_run_metrics(run_dir)
        off = load_official_metrics(run_dir)
        cmp = compare_metrics(rec, off)
        diffs[run_id] = cmp
        row = {"run_id": run_id, **rec}
        if cmp.get("official_present"):
            for k, v in (cmp.get("official_flat") or {}).items():
                row[f"official_{k}"] = v
        rows.append(row)

    df = pd.DataFrame(rows)
    # Keep a stable column order for the report table
    cols = [
        "run_id",
        "N",
        "official_N",
        "N_xml_ok",
        "official_N_xml_ok",
        "N_hit",
        "official_N_hit",
        "N_effective_strict",
        "official_N_effective_strict",
        "N_effective_relaxed",
        "official_N_effective_relaxed",
        "hit_rate_attempted",
        "official_hit_rate_attempted",
        "hit_rate_given_xml_ok",
        "official_hit_rate_given_xml_ok",
        "effective_rate_strict_attempted",
        "official_effective_rate_strict_attempted",
        "effective_rate_relaxed_attempted",
        "official_effective_rate_relaxed_attempted",
    ]
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    lines: list[str] = []
    lines.append("# Metrics Recompute vs Official (口径一致性对账)")
    lines.append("")
    lines.append(f"- generated_at: {generated_at}")
    for n in notes:
        lines.append(f"- note: {n}")
    lines.append("")
    lines.append("## Definition (论文数据收集.md:10.9.3)")
    lines.append("- N: attempted_papers")
    lines.append("- N_xml_ok: xml_ok_papers (manifest xml downloaded/skipped_exists)")
    lines.append("- N_hit: papers_with_experimental_rows (>=1 raw_experimental_records row)")
    lines.append("- N_effective_strict/relaxed: papers with >=1 train_ready_* row")
    lines.append("")
    lines.append("## Per-run comparison table")
    lines.append(df.to_markdown(index=False))
    lines.append("")
    lines.append("## Differences (if any)")
    any_diff = False
    for run_id, info in diffs.items():
        d = info.get("diff") or {}
        if not d:
            continue
        any_diff = True
        lines.append(f"### {run_id}")
        for k, v in d.items():
            lines.append(f"- {k}: recomputed={v.get('recomputed')} vs official={v.get('official')}")
        lines.append("")
    if not any_diff:
        lines.append("- All compared fields match the official `sample200_metrics.json` exactly.")
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"diffs": diffs}


def value_counts_md(series: pd.Series, *, top_k: int = 30) -> str:
    vc = series.fillna("MISSING").astype("string").str.strip()
    vc = vc.replace("", "MISSING")
    counts = vc.value_counts(dropna=False).head(top_k)
    df = counts.rename_axis("value").reset_index(name="count")
    return df.to_markdown(index=False)


def method_missing_table(df: pd.DataFrame) -> str:
    method_cols = [c for c in df.columns if c.startswith("method_")]
    rows = []
    for c in method_cols:
        s = df[c].astype("string")
        total = len(s)
        if total == 0:
            continue
        s_clean = s.fillna("").str.strip()
        missing = (s_clean == "")
        unknown = s_clean.str.lower().eq("unknown")
        rows.append(
            {
                "field": c,
                "missing_ratio": float(missing.mean()),
                "unknown_ratio": float(unknown.mean()),
                "nonempty_ratio": float((~missing).mean()),
            }
        )
    if not rows:
        return "_No method_* fields found._"
    out = pd.DataFrame(rows).sort_values(by=["missing_ratio", "unknown_ratio"], ascending=False)
    return out.to_markdown(index=False, floatfmt=".4f")


def endpoint_unit_crosstab_md(df: pd.DataFrame, *, max_units: int = 20) -> str:
    ep = df["endpoint"].fillna("MISSING").astype("string").str.strip().replace("", "MISSING")
    unit = df["unit"].fillna("MISSING").astype("string").str.strip().replace("", "MISSING")
    tab = pd.crosstab(ep, unit)
    # Keep the most frequent units to avoid extremely wide tables
    unit_totals = tab.sum(axis=0).sort_values(ascending=False)
    keep_units = list(unit_totals.head(max_units).index)
    tab = tab[keep_units]
    tab = tab.sort_index(axis=0)
    return tab.to_markdown()


def write_dataset_profile_report(
    *,
    out_path: Path,
    union_df: pd.DataFrame,
    strict_df: pd.DataFrame,
    relaxed_df: pd.DataFrame,
    generated_at: str,
    split_stats: dict[str, Any],
) -> None:
    ensure_parent(out_path)

    def basics(df: pd.DataFrame) -> dict[str, Any]:
        return {
            "rows": int(len(df)),
            "papers": int(df["pmcid"].nunique(dropna=True)) if "pmcid" in df.columns else 0,
            "sequences": int(df["sequence"].nunique(dropna=True)) if "sequence" in df.columns else 0,
            "endpoints": int(df["endpoint"].nunique(dropna=True)) if "endpoint" in df.columns else 0,
        }

    b_union = basics(union_df)
    b_strict = basics(strict_df)
    b_relaxed = basics(relaxed_df)

    def censored_stats(df: pd.DataFrame) -> dict[str, Any]:
        s = df.get("is_censored", pd.Series([False] * len(df))).fillna(False).astype(bool)
        cmp = df.get("cmp", pd.Series([pd.NA] * len(df))).astype("string").fillna("").str.strip()
        return {
            "is_censored_ratio": float(s.mean()) if len(df) else 0.0,
            "cmp_present_ratio": float((cmp != "").mean()) if len(df) else 0.0,
        }

    c_strict = censored_stats(strict_df)
    c_relaxed = censored_stats(relaxed_df)

    lines: list[str] = []
    lines.append("# Dataset Profile (训练视角画像)")
    lines.append("")
    lines.append(f"- generated_at: {generated_at}")
    lines.append("")
    lines.append("## Key notes: what `unknown` means (and what it does NOT mean)")
    lines.append("- `unknown` **≠** “no experimental data”; it means the pipeline extracted some evidence but **method taxonomy / normalization did not match** a known category/value.")
    lines.append("- Empty/NaN method fields usually mean **no method snippet could be attached** for that record (or the endpoint has no corresponding method schema).")
    lines.append("- Training impact: `unknown` inflates heterogeneity; for cross-paper comparability, prefer strict subsets + method-filtered benchmarks.")
    lines.append("")
    lines.append("## Dataset sizes")
    size_df = pd.DataFrame(
        [
            {"dataset": "union (records_union)", **b_union},
            {"dataset": "strict (train_ready_strict==True)", **b_strict},
            {"dataset": "relaxed (train_ready_relaxed==True)", **b_relaxed},
        ]
    )
    lines.append(size_df.to_markdown(index=False))
    lines.append("")
    lines.append("## Endpoint distribution (strict)")
    lines.append(value_counts_md(strict_df["endpoint"], top_k=30) if len(strict_df) else "_empty_")
    lines.append("")
    lines.append("## Unit distribution (strict)")
    lines.append(value_counts_md(strict_df["unit"], top_k=30) if len(strict_df) else "_empty_")
    lines.append("")
    lines.append("## Censoring / cmp (strict vs relaxed)")
    cr = pd.DataFrame(
        [
            {"dataset": "strict", **c_strict},
            {"dataset": "relaxed", **c_relaxed},
        ]
    )
    lines.append(cr.to_markdown(index=False, floatfmt=".4f"))
    lines.append("")
    lines.append("## Method field missingness (strict)")
    lines.append(method_missing_table(strict_df) if len(strict_df) else "_empty_")
    lines.append("")
    lines.append("## Endpoint × Unit crosstab (strict; top units)")
    lines.append(endpoint_unit_crosstab_md(strict_df, max_units=20) if len(strict_df) else "_empty_")
    lines.append("")
    lines.append("## Endpoint × Unit crosstab (relaxed; top units)")
    lines.append(endpoint_unit_crosstab_md(relaxed_df, max_units=20) if len(relaxed_df) else "_empty_")
    lines.append("")
    lines.append("## Recommended comparable baselines")
    lines.append("- strict: recommended for leakage-safe cross-paper benchmarks (highest comparability; excludes censored/aggregate/missing-unit records).")
    lines.append("- relaxed: recommended for larger-scale training, but requires explicit handling of `cmp/is_censored/range_low/range_high` (censored/interval regression or label encoding).")
    lines.append("")
    lines.append("## Split stats (summary)")
    lines.append("```json")
    lines.append(json.dumps(split_stats, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_task_plan(
    out_path: Path,
    *,
    generated_at: str,
    runs: list[tuple[str, Path]],
) -> None:
    ensure_parent(out_path)

    missed_paths = [str((run_dir / "sequence_present_but_no_records.csv").resolve()) for _, run_dir in runs]

    lines: list[str] = []
    lines.append("# TASK_PLAN (Next Steps)")
    lines.append("")
    lines.append(f"- generated_at: {generated_at}")
    lines.append("")
    lines.append("## Level 1: Extraction improvements (coverage)")
    lines.append("- Improve cross-table join recall (sequence table ↔ endpoint table) for supplementary XLSX/PDF-derived tables.")
    lines.append("- Add conservative PDF table/OCR fallback for “sequence present but no machine-readable table” cases (keep auditable source pointers).")
    lines.append("- Expand endpoint patterns (e.g., LC50/EC50 variants) and reduce acronym ambiguity via context filters.")
    lines.append("")
    lines.append("## Level 2: Method normalization improvements (comparability)")
    lines.append("- Expand method taxonomy + normalization dictionaries for medium/inoculum/incubation/readout/RBC parameters; keep evidence snippets.")
    lines.append("- Separate “no method evidence found” vs “evidence found but normalization=unknown” as two explicit flags for downstream filtering.")
    lines.append("- Add endpoint-aware method requirements for benchmark tracks (e.g., MIC broth microdilution + standardized medium).")
    lines.append("")
    lines.append("## Level 3: Model training & evaluation")
    lines.append("- Define benchmark tasks by endpoint/unit with strict splits: regression for numeric, censored/interval regression for relaxed.")
    lines.append("- Baselines: simple sequence models (k-mer + ridge), protein LM pooling + MLP, and uncertainty-aware heads for censored labels.")
    lines.append("- Evaluate leakage risk with both `split_by_paper` and `split_by_sequence`; report both to prevent over-optimistic results.")
    lines.append("")
    lines.append("## LLM deep-read queue regression (high-signal missed list → feedback loop)")
    lines.append("- Inputs (do not edit):")
    for p in missed_paths:
        lines.append(f"  - `{p}`")
    lines.append("- Procedure (no deep-read executed in this task):")
    lines.append("  1) Freeze a deterministic worklist of PMCID from the missed CSVs (dedupe, stable sort).")
    lines.append("  2) Build an analysis queue with `python scripts/build_analysis_queue.py --worklist <worklist> --papers-dir <run>/papers --analysis-dir analysis_llm_*`.")
    lines.append("  3) Run N workers (tmux) using `scripts/start_analysis_workers_tmux.sh` in read-only sandbox.")
    lines.append("  4) Merge results with `python scripts/merge_per_paper_md.py --analysis-dir ...`.")
    lines.append("  5) Feed back: add new extraction heuristics or manual per-paper patches as auditable overlays (never overwrite raw tables).")
    lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--run-dir",
        action="append",
        default=[],
        help="Run dir to include (repeatable; contains papers/). If provided, overrides --run1-dir/--run2-dir.",
    )
    ap.add_argument("--run1-dir", default="runs/oa_seq_peptide_fast_20260121_214200", help="First run dir (contains papers/)")
    ap.add_argument("--run2-dir", default="runs/oa_seq_peptide_fast_oa_inpmc_20260121_220445", help="Second run dir (contains papers/)")
    ap.add_argument("--out-dir", required=True, help="Output directory under docs/analysis/")
    ap.add_argument("--seed", type=int, default=20260122, help="Fixed RNG seed for reproducible splits")
    ap.add_argument("--train-ratio", type=float, default=0.8)
    ap.add_argument("--valid-ratio", type=float, default=0.1)
    ap.add_argument("--test-ratio", type=float, default=0.1)
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "splits").mkdir(parents=True, exist_ok=True)
    (out_dir / "reports").mkdir(parents=True, exist_ok=True)

    generated_at = now_iso8601_local()

    run_dirs: list[Path] = [Path(p).resolve() for p in (args.run_dir or []) if str(p).strip()]
    if run_dirs:
        runs = [(p.name, p) for p in run_dirs]
    else:
        run1_dir = Path(args.run1_dir).resolve()
        run2_dir = Path(args.run2_dir).resolve()
        runs = [(run1_dir.name, run1_dir), (run2_dir.name, run2_dir)]

    ratios = (float(args.train_ratio), float(args.valid_ratio), float(args.test_ratio))

    # Load + normalize
    dfs = []
    for run_id, run_dir in runs:
        p = run_dir / "papers" / "screened_experimental_records_with_methods.csv"
        if not p.exists():
            raise SystemExit(f"missing input: {p}")
        df = read_csv(p)
        df = normalize_screened_df(df, run_id=run_id)
        dfs.append(df)

    union_df = pd.concat(dfs, ignore_index=True)

    # Deterministic sort before dedupe/output
    sort_cols = [c for c in ["run_id", "pmcid", "source_path", "source_ref", "endpoint", "peptide_id", "condition", "value", "unit", "cmp"] if c in union_df.columns]
    if sort_cols:
        union_df = union_df.sort_values(by=sort_cols, kind="mergesort", na_position="last").reset_index(drop=True)

    union_df, dedupe_info = dedupe_records(union_df)

    # Write union + strict/relaxed
    union_paths = write_union_outputs(union_df, out_dir=out_dir)
    subsets_info = subset_and_write(union_df, out_dir=out_dir)

    strict_df = union_df[union_df["train_ready_strict"].fillna(False)].copy()
    relaxed_df = union_df[union_df["train_ready_relaxed"].fillna(False)].copy()

    # Splits: generate per-dataset artifacts (union/strict/relaxed), always grouped to prevent leakage.
    split_stats: dict[str, Any] = {"seed": int(args.seed), "ratios": {"train": ratios[0], "valid": ratios[1], "test": ratios[2]}}

    for scheme in ["split_by_paper", "split_by_sequence"]:
        scheme_dir = out_dir / "splits" / scheme
        scheme_dir.mkdir(parents=True, exist_ok=True)
        cleanup_legacy_split_files(scheme_dir)

        per_ds = []
        for ds_name, ds_df in [("union", union_df), ("strict", strict_df), ("relaxed", relaxed_df)]:
            per_ds.append(
                make_split_artifacts_for_df(
                    df=ds_df,
                    scheme_dir=scheme_dir,
                    dataset_name=ds_name,
                    scheme=scheme,
                    seed=int(args.seed),
                    ratios=ratios,
                )
            )

        cfg = {
            "generated_at": generated_at,
            "scheme": scheme,
            "seed": int(args.seed),
            "ratios": {"train": ratios[0], "valid": ratios[1], "test": ratios[2]},
            "per_dataset": per_ds,
        }
        (scheme_dir / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        split_stats[scheme] = {
            d["dataset"]: d["group_counts"]
            | ({"sequence_missing_ratio": d["extra_info"]["rows_sequence_missing_ratio"]} if scheme == "split_by_sequence" else {})
            for d in per_ds
        }

    # Reports
    reconcile = write_metrics_reconcile_report(
        out_path=out_dir / "reports" / "metrics_recompute_vs_official.md",
        runs=runs,
        generated_at=generated_at,
        notes=[
            "Recompute uses run-local download_manifest + raw_experimental_records + screened_experimental_records (same as scripts/summarize_sample_run.py).",
            "unknown != no data: method normalization miss does not imply missing experimental records.",
        ],
    )

    write_dataset_profile_report(
        out_path=out_dir / "reports" / "dataset_profile.md",
        union_df=union_df,
        strict_df=strict_df,
        relaxed_df=relaxed_df,
        generated_at=generated_at,
        split_stats=split_stats,
    )

    write_task_plan(out_dir / "TASK_PLAN.md", generated_at=generated_at, runs=runs)

    # Root config for reproducibility
    run_inputs = []
    for run_id, run_dir in runs:
        run_inputs.append(
            {
                "run_id": run_id,
                "run_dir": str(run_dir),
                "records_csv": str(run_dir / "papers" / "screened_experimental_records_with_methods.csv"),
                "metrics_official": str(run_dir / "sample200_metrics.json"),
                "high_signal_missed": str(run_dir / "sequence_present_but_no_records.csv"),
            }
        )
    config = {
        "generated_at": generated_at,
        "inputs": {"runs": run_inputs},
        "outputs": {
            **union_paths,
            **subsets_info,
            "splits_dir": str((out_dir / "splits").resolve()),
            "reports_dir": str((out_dir / "reports").resolve()),
        },
        "dedupe": {
            "primary_key": "strong=source_kind+source_path+source_ref+endpoint else weak=pmcid+peptide_id+sequence+endpoint+condition+value+unit+cmp",
            **dedupe_info,
        },
        "split": split_stats,
        "metrics_reconcile": reconcile,
        "dataset_sizes": {
            "union_rows": int(len(union_df)),
            "strict_rows": int(len(strict_df)),
            "relaxed_rows": int(len(relaxed_df)),
            "union_unique_papers": int(union_df["pmcid"].nunique(dropna=True)),
            "union_unique_sequences": int(union_df["sequence"].nunique(dropna=True)),
        },
    }
    (out_dir / "config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] out_dir: {out_dir}")
    print(f"[ok] union rows: {len(union_df)} (dedupe dropped {dedupe_info['dropped']})")
    print(f"[ok] strict rows: {len(strict_df)}")
    print(f"[ok] relaxed rows: {len(relaxed_df)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
