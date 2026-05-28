#!/usr/bin/env python3
"""
Archive + summarize per-paper experimental method conditions into a few families.

Input: methods_conditions_by_paper*.csv produced by scripts/augment_records_with_methods.py
Output (defaults under --papers-dir):
  - methods_archive_by_paper.csv   (one row per paper per method family)
  - methods_archive_summary.md     (human-readable grouped summary)
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


def now_local_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def safe_str(x: object) -> str:
    if x is None:
        return ""
    try:
        if pd.isna(x):
            return ""
    except Exception:
        pass
    return str(x).strip()


def split_endpoints(s: str) -> list[str]:
    out: list[str] = []
    for part in (s or "").split(","):
        p = part.strip().upper()
        if p and p not in out:
            out.append(p)
    return out


ANTIMICROBIAL_ENDPOINTS = {"MIC", "MBC"}
HEMOLYSIS_ENDPOINTS = {"HEMOLYSIS"}
CYTOTOX_ENDPOINTS = {"IC50", "HC50", "CC50", "EC50", "GI50", "LC50", "LD50"}


@dataclass(frozen=True)
class Family:
    key: str
    title: str
    endpoints: set[str]
    prefix: str  # abx_ or hem_


FAMILIES = [
    Family(key="antimicrobial", title="Antimicrobial Susceptibility (MIC/MBC)", endpoints=ANTIMICROBIAL_ENDPOINTS, prefix="abx_"),
    Family(key="hemolysis", title="Hemolysis (RBC lysis)", endpoints=HEMOLYSIS_ENDPOINTS, prefix="hem_"),
    Family(key="cytotoxicity", title="Cytotoxicity / Anti-proliferation (IC50/HC50/…)", endpoints=CYTOTOX_ENDPOINTS, prefix="hem_"),
]


def pick_row_fields(row: pd.Series, family: Family) -> dict[str, str]:
    p = family.prefix
    fields = {
        "guideline": safe_str(row.get(f"{p}guideline")),
        "assay_method": safe_str(row.get(f"{p}assay_method")),
        "medium": safe_str(row.get(f"{p}medium")),
        "inoculum": safe_str(row.get(f"{p}inoculum")),
        "incubation": safe_str(row.get(f"{p}incubation")),
        "plate": safe_str(row.get(f"{p}plate")),
        "readout": safe_str(row.get(f"{p}readout")),
        "rbc_source": safe_str(row.get(f"{p}rbc_source")) if family.key in {"hemolysis"} else "",
        "sec_titles": safe_str(row.get(f"{p}sec_titles")),
        "evidence": safe_str(row.get(f"{p}evidence")),
    }
    return fields


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers-dir", required=True, help="Run papers dir (contains methods_conditions_by_paper*.csv)")
    ap.add_argument(
        "--methods-csv",
        default="",
        help="Input methods CSV (default: <papers-dir>/methods_conditions_by_paper_from_raw.csv then methods_conditions_by_paper.csv)",
    )
    ap.add_argument("--out-csv", default="", help="Output archive CSV path")
    ap.add_argument("--out-md", default="", help="Output Markdown summary path")
    args = ap.parse_args()

    papers_dir = Path(args.papers_dir)
    if not papers_dir.exists():
        raise SystemExit(f"Not found: {papers_dir}")

    if args.methods_csv:
        in_path = Path(args.methods_csv)
    else:
        cand1 = papers_dir / "methods_conditions_by_paper_from_raw.csv"
        cand2 = papers_dir / "methods_conditions_by_paper.csv"
        in_path = cand1 if cand1.exists() else cand2
    if not in_path.exists():
        raise SystemExit(f"Missing methods CSV: {in_path}")

    out_csv = Path(args.out_csv) if args.out_csv else (papers_dir / "methods_archive_by_paper.csv")
    out_md = Path(args.out_md) if args.out_md else (papers_dir / "methods_archive_summary.md")

    df = pd.read_csv(in_path).fillna("")
    if "paper_stem" not in df.columns or "endpoints_in_records" not in df.columns:
        raise SystemExit(f"Unexpected columns in methods CSV: {in_path}")

    df["paper_stem"] = df["paper_stem"].astype("string")
    df["endpoints_in_records"] = df["endpoints_in_records"].astype("string")

    ok = df[df.get("status", "").astype(str).eq("ok")].copy()
    ok["endpoints_list"] = ok["endpoints_in_records"].astype(str).map(split_endpoints)
    hit_papers = ok["paper_stem"].dropna().astype(str).str.strip()
    hit_papers = hit_papers[hit_papers.ne("")]
    hit_papers_unique = sorted(set(hit_papers.tolist()))

    rows: list[dict[str, str]] = []
    for _, r in ok.iterrows():
        paper = safe_str(r.get("paper_stem"))
        if not paper:
            continue
        endpoints = set(r.get("endpoints_list") or [])
        for fam in FAMILIES:
            eps = sorted(endpoints.intersection(fam.endpoints))
            if not eps:
                continue
            fields = pick_row_fields(r, fam)
            rows.append(
                {
                    "paper_stem": paper,
                    "family": fam.key,
                    "family_title": fam.title,
                    "endpoints": ",".join(eps),
                    "xml_path": safe_str(r.get("xml_path")),
                    **fields,
                }
            )

    out_df = pd.DataFrame(rows)
    if len(out_df) == 0:
        out_df = pd.DataFrame(
            columns=[
                "paper_stem",
                "family",
                "family_title",
                "endpoints",
                "xml_path",
                "guideline",
                "assay_method",
                "medium",
                "inoculum",
                "incubation",
                "plate",
                "readout",
                "rbc_source",
                "sec_titles",
                "evidence",
            ]
        )

    out_df.to_csv(out_csv, index=False)

    lines: list[str] = []
    lines.append("# Methods Archive Summary")
    lines.append("")
    lines.append(f"Generated at: {now_local_str()}")
    lines.append(f"Input: `{in_path}`")
    lines.append(f"Papers dir: `{papers_dir}`")
    lines.append("")
    lines.append("## Coverage")
    lines.append(f"- hit_papers_in_methods_csv: {len(hit_papers_unique)}")
    lines.append(f"- archive_rows (paper × family): {len(out_df)}")
    lines.append("")

    if len(out_df) == 0:
        lines.append("No archive rows produced (no endpoints matched configured families).")
        out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return 0

    lines.append("## Families")
    fam_counts = out_df.groupby("family")["paper_stem"].nunique().to_dict()
    for fam in FAMILIES:
        lines.append(f"- {fam.title}: {int(fam_counts.get(fam.key, 0))} papers")
    lines.append("")

    for fam in FAMILIES:
        sub = out_df[out_df["family"] == fam.key].copy()
        if len(sub) == 0:
            continue
        lines.append(f"## {fam.title}")
        lines.append(f"- papers: {sub['paper_stem'].nunique()}")
        lines.append("")

        def add_group(title: str, col: str) -> None:
            vals = sub[col].fillna("").astype(str).str.strip()
            sub2 = sub.copy()
            sub2[col] = vals
            vc = sub2[sub2[col].ne("")].groupby(col)["paper_stem"].nunique().sort_values(ascending=False)
            lines.append(f"**{title}**")
            if vc.empty:
                lines.append("- (none)")
                lines.append("")
                return
            for v, n in vc.items():
                papers = sorted(sub2[sub2[col].eq(v)]["paper_stem"].unique().tolist())
                lines.append(f"- {v}: {int(n)} papers ({', '.join(papers)})")
            lines.append("")

        add_group("Guideline", "guideline")
        add_group("Assay Method", "assay_method")
        add_group("Medium", "medium")
        add_group("Inoculum", "inoculum")
        add_group("Incubation", "incubation")
        add_group("Readout", "readout")
        if fam.key == "hemolysis":
            add_group("RBC Source", "rbc_source")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

