#!/usr/bin/env python3
"""
Summarize and classify (taxonomy) paper-level experimental methods extracted by
scripts/augment_records_with_methods.py.

Inputs:
  - methods_conditions_by_paper.csv (under a run's papers/ directory)

Outputs:
  - methods_taxonomy.csv
  - methods_taxonomy.md
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def now_local_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def s(x: Any) -> str:
    if x is None:
        return ""
    try:
        if pd.isna(x):
            return ""
    except Exception:
        pass
    return str(x).strip()


def norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def norm_guideline(text: str) -> str:
    t = s(text).upper()
    if "CLSI" in t:
        return "CLSI"
    if "EUCAST" in t:
        return "EUCAST"
    return ""


def norm_abx_method(text: str) -> str:
    t = s(text).lower()
    if "broth microdilution" in t or "microdilution" in t:
        return "broth_microdilution"
    if "agar dilution" in t:
        return "agar_dilution"
    if "disk diffusion" in t:
        return "disk_diffusion"
    if t:
        return "other"
    return "unknown"


def norm_medium(text: str) -> str:
    t = s(text)
    low = t.lower()
    mediums: list[str] = []
    if any(k in low for k in ("mueller", "muller", "mhb", "mh broth", "mueller–hinton", "mueller-hinton")):
        mediums.append("mueller_hinton")
    if "rpmi" in low:
        mediums.append("rpmi_1640")
    if "lb" in low:
        mediums.append("lb")
    if "tsb" in low:
        mediums.append("tsb")
    if "bhi" in low:
        mediums.append("bhi")
    return "|".join(mediums) if mediums else ""


TEMP_RE = re.compile(r"(\d+(?:\.\d+)?)\s*°\s*C|\b(\d+(?:\.\d+)?)\s*C\b", flags=re.IGNORECASE)
HOURS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:h|hours)\b", flags=re.IGNORECASE)


def norm_incubation(text: str) -> str:
    t = s(text)
    low = t.lower()
    temps = []
    for m in TEMP_RE.finditer(t):
        val = m.group(1) or m.group(2)
        if val:
            temps.append(val)
    hours = []
    for m in HOURS_RE.finditer(t):
        val = m.group(1)
        if val:
            hours.append(val)
    # Prefer the first pair as a compact signature.
    if temps and hours:
        return f"{hours[0]}h_{temps[0]}C"
    if temps:
        return f"{temps[0]}C"
    if hours:
        return f"{hours[0]}h"
    if "co2" in low:
        return "co2_incubation"
    return ""


def norm_inoculum(text: str) -> str:
    t = s(text)
    if not t:
        return ""
    # Common: "5 × 10^5 CFU/mL" (or without caret).
    m = re.search(
        r"(\d+(?:\.\d+)?)\s*[x×]\s*10\s*\^?\s*(\d+)\s*CFU\s*/\s*mL",
        t,
        flags=re.IGNORECASE,
    )
    if m:
        coef, exp = m.group(1), m.group(2)
        return f"{coef}x10^{exp}_cfu_ml"

    # Variant: "5 × 105 CFU/mL" meaning 5 × 10^5 (common when superscripts are flattened).
    m = re.search(r"(\d+(?:\.\d+)?)\s*[x×]\s*10(\d{1,2})\s*CFU\s*/\s*mL", t, flags=re.IGNORECASE)
    if m:
        coef, exp = m.group(1), m.group(2)
        return f"{coef}x10^{exp}_cfu_ml"

    # Direct: "1e6 CFU/mL" not handled; keep plain numeric if present.
    m = re.search(r"\b(\d+(?:\.\d+)?)\s*CFU\s*/\s*mL\b", t, flags=re.IGNORECASE)
    if m:
        return f"{m.group(1)}_cfu_ml"
    return ""


def norm_rbc_source(text: str) -> str:
    low = s(text).lower()
    has_human = "human" in low
    has_sheep = "sheep" in low
    if has_human and has_sheep:
        return "mixed_human_sheep"
    if has_human:
        return "human"
    if has_sheep:
        return "sheep"
    if low:
        return "other"
    return "unknown"


def norm_readout_nm(text: str) -> str:
    t = s(text)
    # Extract first wavelength mention.
    m = re.search(r"(\d{3})\s*nm", t, flags=re.IGNORECASE)
    return f"{m.group(1)}nm" if m else ""


def hem_class(rbc_source_norm: str, readout_nm: str) -> str:
    if rbc_source_norm in ("human", "sheep", "mixed_human_sheep"):
        if readout_nm in ("540nm", "550nm", "535nm", "450nm"):
            return "rbc_hemoglobin_release_spectro"
        return "rbc_assay_other_readout"
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers-dir", required=True, help="Run papers dir (contains methods_conditions_by_paper.csv)")
    ap.add_argument("--in-csv", default="", help="Override input CSV path")
    ap.add_argument("--out-csv", default="", help="Output taxonomy CSV path")
    ap.add_argument("--out-md", default="", help="Output taxonomy Markdown path")
    args = ap.parse_args()

    papers_dir = Path(args.papers_dir)
    in_csv = Path(args.in_csv) if args.in_csv else (papers_dir / "methods_conditions_by_paper.csv")
    if not in_csv.exists():
        raise SystemExit(f"Missing: {in_csv}")

    out_csv = Path(args.out_csv) if args.out_csv else (papers_dir / "methods_taxonomy.csv")
    out_md = Path(args.out_md) if args.out_md else (papers_dir / "methods_taxonomy.md")

    df = pd.read_csv(in_csv).fillna("")
    if "paper_stem" not in df.columns:
        raise SystemExit("Input missing paper_stem column.")

    tax = pd.DataFrame()
    tax["paper_stem"] = df["paper_stem"].astype(str)
    tax["endpoints_in_records"] = df.get("endpoints_in_records", "").astype(str)

    tax["abx_guideline_norm"] = df.get("abx_guideline", "").map(norm_guideline)
    tax["abx_method_class"] = df.get("abx_assay_method", "").map(norm_abx_method)
    tax["abx_medium_norm"] = df.get("abx_medium", "").map(norm_medium)
    tax["abx_inoculum_norm"] = df.get("abx_inoculum", "").map(norm_inoculum)
    tax["abx_incubation_norm"] = df.get("abx_incubation", "").map(norm_incubation)

    tax["hem_rbc_source_norm"] = df.get("hem_rbc_source", "").map(norm_rbc_source)
    tax["hem_readout_nm"] = df.get("hem_readout", "").map(norm_readout_nm)
    tax["hem_incubation_norm"] = df.get("hem_incubation", "").map(norm_incubation)
    tax["hem_method_class"] = [hem_class(r, n) for r, n in zip(tax["hem_rbc_source_norm"], tax["hem_readout_nm"])]

    tax.to_csv(out_csv, index=False)

    # Markdown summary
    def md_list(papers: list[str]) -> str:
        return ", ".join(papers) if papers else "-"

    lines = [
        "# Methods Taxonomy Summary",
        "",
        f"Generated at: {now_local_str()}",
        f"Input: `{in_csv}`",
        "",
        "## Antimicrobial Assay Classes",
    ]
    for cls, sub in tax.groupby("abx_method_class", dropna=False):
        papers = sorted(sub["paper_stem"].tolist())
        lines.append(f"- {cls}: {len(papers)} papers ({md_list(papers)})")

    lines.extend(["", "## Hemolysis / Cytotoxicity Classes"])
    for cls, sub in tax.groupby("hem_method_class", dropna=False):
        papers = sorted(sub["paper_stem"].tolist())
        lines.append(f"- {cls}: {len(papers)} papers ({md_list(papers)})")

    lines.extend(["", "## Key Parameter Variants (counts)"])
    for col in ("abx_guideline_norm", "abx_medium_norm", "abx_inoculum_norm", "abx_incubation_norm", "hem_rbc_source_norm", "hem_readout_nm", "hem_incubation_norm"):
        vc = tax[col].fillna("").astype(str).value_counts()
        lines.append(f"- {col}:")
        for k, v in vc.items():
            key = k if k else "(empty)"
            lines.append(f"  - {key}: {int(v)}")

    lines.extend(["", "## Per-Paper Map", ""])
    # Compact table
    view = tax[
        [
            "paper_stem",
            "endpoints_in_records",
            "abx_method_class",
            "abx_guideline_norm",
            "abx_medium_norm",
            "abx_inoculum_norm",
            "abx_incubation_norm",
            "hem_method_class",
            "hem_rbc_source_norm",
            "hem_readout_nm",
            "hem_incubation_norm",
        ]
    ].copy()
    # Render as markdown table
    lines.append("| " + " | ".join(view.columns) + " |")
    lines.append("|" + "|".join(["---"] * len(view.columns)) + "|")
    for _, row in view.iterrows():
        vals = [norm_ws(s(row[c])).replace("|", "\\|") for c in view.columns]
        lines.append("| " + " | ".join(vals) + " |")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
