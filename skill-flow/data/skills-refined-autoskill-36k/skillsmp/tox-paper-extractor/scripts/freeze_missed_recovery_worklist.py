#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class SelectionConfig:
    max_sequence_extractions: int
    sort: list[dict]
    n_run1: int
    n_run2: int
    skipped_paper_stems: list[str]


def _read_missed_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "paper_stem",
        "sequence_extractions",
        "endpoint_value_extractions",
        "experimental_records",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns: {sorted(missing)}")
    return df


def _select(
    df: pd.DataFrame,
    *,
    n: int,
    max_sequence_extractions: int,
    skipped_paper_stems: set[str],
) -> tuple[pd.DataFrame, dict]:
    df = df.copy()

    total_rows = int(df.shape[0])
    df = df[df["experimental_records"].fillna(0).astype(int) == 0]
    rows_exp0 = int(df.shape[0])

    df = df[~df["paper_stem"].astype(str).isin(skipped_paper_stems)]
    rows_not_skipped = int(df.shape[0])

    df = df[df["sequence_extractions"].fillna(0).astype(int) <= max_sequence_extractions]
    rows_after_seq_filter = int(df.shape[0])

    sort_cols = ["endpoint_value_extractions", "sequence_extractions", "paper_stem"]
    ascending = [False, True, True]
    if "endpoint_value_extractions_kw_unit" in df.columns:
        sort_cols = ["endpoint_value_extractions_kw_unit", *sort_cols]
        ascending = [False, *ascending]
    df = df.sort_values(sort_cols, ascending=ascending, kind="mergesort")
    selected = df.head(n).copy()
    if selected.empty:
        raise ValueError("No papers selected; check filters/inputs.")

    stats = {
        "rows_total": total_rows,
        "rows_experimental_records_eq_0": rows_exp0,
        "rows_not_skipped": rows_not_skipped,
        "rows_after_sequence_extractions_filter": rows_after_seq_filter,
        "selected_n": int(selected.shape[0]),
    }
    return selected, stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Freeze a reproducible worklist for 'sequence_present_but_no_records' missed-paper recovery.",
    )
    parser.add_argument("--run1-id", default="run1")
    parser.add_argument("--run2-id", default="run2")
    parser.add_argument("--missed-csv-run1", type=Path, required=True)
    parser.add_argument("--missed-csv-run2", type=Path, required=True)
    parser.add_argument("--n-run1", type=int, default=8)
    parser.add_argument("--n-run2", type=int, default=8)
    parser.add_argument("--max-sequence-extractions", type=int, default=5000)
    parser.add_argument("--skip-paper-stem", action="append", default=[])
    parser.add_argument("--out-dir", type=Path, required=True)

    args = parser.parse_args()
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=False)

    skipped = {str(x).strip() for x in args.skip_paper_stem if str(x).strip()}

    df1 = _read_missed_csv(args.missed_csv_run1)
    df2 = _read_missed_csv(args.missed_csv_run2)

    sel1, stats1 = _select(
        df1,
        n=args.n_run1,
        max_sequence_extractions=args.max_sequence_extractions,
        skipped_paper_stems=skipped,
    )
    sel2, stats2 = _select(
        df2,
        n=args.n_run2,
        max_sequence_extractions=args.max_sequence_extractions,
        skipped_paper_stems=skipped,
    )

    worklist1 = out_dir / "worklist_run1.txt"
    worklist2 = out_dir / "worklist_run2.txt"
    worklist1.write_text("\n".join(sel1["paper_stem"].astype(str).tolist()) + "\n", encoding="utf-8")
    worklist2.write_text("\n".join(sel2["paper_stem"].astype(str).tolist()) + "\n", encoding="utf-8")

    cfg = SelectionConfig(
        max_sequence_extractions=int(args.max_sequence_extractions),
        sort=[
            *(
                [{"key": "endpoint_value_extractions_kw_unit", "order": "desc"}]
                if "endpoint_value_extractions_kw_unit" in df1.columns and "endpoint_value_extractions_kw_unit" in df2.columns
                else []
            ),
            {"key": "endpoint_value_extractions", "order": "desc"},
            {"key": "sequence_extractions", "order": "asc"},
            {"key": "paper_stem", "order": "asc"},
        ],
        n_run1=int(args.n_run1),
        n_run2=int(args.n_run2),
        skipped_paper_stems=sorted(skipped),
    )

    now = datetime.now(timezone.utc).astimezone()
    meta = {
        "kind": "missed_recovery_worklist",
        "version": 1,
        "created_at": now.isoformat(timespec="seconds"),
        "inputs": {
            args.run1_id: str(args.missed_csv_run1),
            args.run2_id: str(args.missed_csv_run2),
        },
        "config": asdict(cfg),
        "stats": {args.run1_id: stats1, args.run2_id: stats2},
        "selected": {
            args.run1_id: sel1.to_dict(orient="records"),
            args.run2_id: sel2.to_dict(orient="records"),
        },
        "outputs": {
            args.run1_id: str(worklist1),
            args.run2_id: str(worklist2),
        },
    }
    (out_dir / "worklist.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(str(out_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
