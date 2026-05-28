#!/usr/bin/env python3
"""
Augment extracted experimental records with paper-local, auditable method conditions.

Reads an extracted records CSV (typically screened_experimental_records.csv), parses each
hit paper's JATS XML, extracts method-condition snippets + key fields, and merges them
back into the records (endpoint-aware).

Outputs (defaults under --papers-dir):
  - methods_conditions_by_paper.csv
  - screened_experimental_records_with_methods.csv
  - methods_conditions_report.md
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def now_local_str() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def safe_str(x: Any) -> str:
    if x is None:
        return ""
    try:
        if pd.isna(x):
            return ""
    except Exception:
        pass
    return str(x).strip()


TABLE_ID_RE = re.compile(r"(?:^|;)\s*table_id=([^;]+)")


def extract_table_ids(source_ref: str) -> list[str]:
    if not source_ref:
        return []
    out: list[str] = []
    for m in TABLE_ID_RE.finditer(source_ref):
        tid = (m.group(1) or "").strip()
        if tid and tid not in out:
            out.append(tid)
    return out


@dataclass
class SectionText:
    title: str
    text: str
    sec_type: str = ""


def parse_xml(path: Path) -> ET.Element:
    xml_text = path.read_text(encoding="utf-8", errors="ignore")
    return ET.fromstring(xml_text)


def iter_sections(root: ET.Element) -> list[SectionText]:
    out: list[SectionText] = []
    for sec in root.iter():
        if not str(sec.tag).endswith("sec"):
            continue
        title = ""
        for child in list(sec):
            if str(child.tag).endswith("title"):
                title = normalize_ws("".join(child.itertext()))
                break
        if not title:
            continue
        sec_type = safe_str(sec.attrib.get("sec-type"))
        text = normalize_ws("".join(sec.itertext()))
        out.append(SectionText(title=title, text=text, sec_type=sec_type))
    return out


def table_wrap_text(root: ET.Element, table_id: str) -> str:
    if not table_id:
        return ""
    texts: list[str] = []
    for tw in root.iter():
        if not str(tw.tag).endswith("table-wrap"):
            continue
        if safe_str(tw.attrib.get("id")) != table_id:
            continue
        for child in tw.iter():
            if str(child.tag).endswith(("caption", "table-wrap-foot")):
                t = normalize_ws("".join(child.itertext()))
                if t:
                    texts.append(t)
    return normalize_ws(" ".join(texts))


def pick_relevant_text(
    sections: list[SectionText],
    *,
    title_keywords: list[str],
    fallback_keywords: list[str],
    extra_texts: list[str],
) -> tuple[str, list[str]]:
    title_kw = [k.lower() for k in title_keywords if k]
    fallback_kw = [k.lower() for k in fallback_keywords if k]

    picked: list[SectionText] = []
    for s in sections:
        low = s.title.lower()
        if any(k in low for k in title_kw):
            picked.append(s)

    if not picked:
        for s in sections:
            low = s.title.lower()
            if any(k in low for k in fallback_kw):
                picked.append(s)

    if not picked:
        for s in sections:
            low = s.title.lower()
            if any(k in low for k in ("materials and methods", "materials & methods", "methods", "experimental")):
                picked.append(s)
                break

    titles = [s.title for s in picked]
    text_parts = [s.text for s in picked if s.text]
    text_parts.extend([t for t in extra_texts if normalize_ws(t)])
    return (normalize_ws(" ".join(text_parts)), titles)


def unique_join(values: list[str]) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for v in values:
        v = normalize_ws(v)
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return " | ".join(out)


METHOD_PATTERNS: dict[str, re.Pattern[str]] = {
    "guideline": re.compile(r"\b(CLSI|EUCAST)\b", flags=re.IGNORECASE),
    "assay_method": re.compile(
        r"\b("
        r"broth\s+microdilution|microdilution|broth\s+dilution|agar\s+dilution|disk\s+diffusion"
        r"|MTT(?:\s+assay)?|WST-?1|CCK-?8|alamar\s*blue|resazurin"
        r"|cell\s+viability\s+assay|cytotoxicity\s+assay|LDH\s+release"
        r")\b",
        flags=re.IGNORECASE,
    ),
    "medium": re.compile(
        r"\b(Mueller[\u2013\u2014-]?Hinton(?:\s+Broth)?|MHB|MH\s+broth|RPMI[\u2013\u2014-]?1640|LB\s+broth|TSB|BHI)\b",
        flags=re.IGNORECASE,
    ),
    "inoculum": re.compile(
        r"\b(\d+(?:\.\d+)?)\s*(?:[x\u00d7]\s*)?10\^?\s*(\d+)\s*CFU\s*/\s*mL\b|\b\d+(?:\.\d+)?\s*CFU\s*/\s*mL\b",
        flags=re.IGNORECASE,
    ),
    "incubation": re.compile(
        r"\bincubat\w*[^.]{0,120}\b(?:"
        r"(?:for\s+\d+(?:\.\d+)?\s*(?:h|hours)|\d+(?:\.\d+)?\s*(?:h|hours))[^.]{0,60}\b(?:at\s+\d+(?:\.\d+)?\s*°?\s*C|\d+(?:\.\d+)?\s*°?\s*C)"
        r"|(?:at\s+\d+(?:\.\d+)?\s*°?\s*C|\d+(?:\.\d+)?\s*°?\s*C)[^.]{0,60}\b(?:for\s+\d+(?:\.\d+)?\s*(?:h|hours)|\d+(?:\.\d+)?\s*(?:h|hours))"
        r")\b",
        flags=re.IGNORECASE,
    ),
    "plate": re.compile(r"\b(96[-\s]*well|384[-\s]*well|microtiter\s+plate|microplate)\b", flags=re.IGNORECASE),
    "volume": re.compile(r"\b(final\s+volume[^.]{0,40}\b\d+(?:\.\d+)?\s*(?:\u00b5l|ul|mL|ml)\b)", flags=re.IGNORECASE),
    "readout": re.compile(
        r"\b("
        r"OD\s*\d+"
        r"|absorbance\s+at\s+\d+\s*nm(?:\d+)?"
        r"|wavelengths?\s+of\s+\d+\s*nm(?:\d+)?"
        r"|measur(?:e|ed)\s+(?:at|using)\s+\d+\s*nm(?:\d+)?"
        r"|(?:supernatant|hemoglobin|spectrophot|optical\s+density)[^.]{0,80}\bat\s+\d+\s*nm(?:\d+)?"
        r")\b",
        flags=re.IGNORECASE,
    ),
    "rbc_source": re.compile(
        r"\b(human|sheep|rabbit|mouse|rat)\b[^.]{0,120}\b(?:red\s+blood\s+cells|RBCs?|erythrocytes|blood)\b|\b(?:red\s+blood\s+cells|RBCs?|erythrocytes|blood)\b[^.]{0,120}\b(human|sheep|rabbit|mouse|rat)\b",
        flags=re.IGNORECASE,
    ),
    "rbc_conc": re.compile(
        r"\b(\d+(?:\.\d+)?)\s*%\s+(?:concentration\s+of\s+)?(?:erythrocytes|RBCs?|cell\s+suspension)\b",
        flags=re.IGNORECASE,
    ),
}


def extract_method_fields(text: str) -> dict[str, str]:
    text = normalize_ws(text)
    if not text:
        return {}
    out: dict[str, str] = {}
    for key, pat in METHOD_PATTERNS.items():
        matches: list[str] = []
        for m in pat.finditer(text):
            s = normalize_ws(m.group(0))
            if s:
                matches.append(s)
        if matches:
            out[key] = unique_join(matches)
    return out


def extract_evidence_sentences(text: str) -> str:
    text = normalize_ws(text)
    if not text:
        return ""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    evidence: list[str] = []
    for s in sents:
        if any(p.search(s) for p in METHOD_PATTERNS.values()):
            evidence.append(s)
    if len(evidence) > 20:
        evidence = evidence[:20]
    return unique_join(evidence)


def endpoint_group(endpoint: str) -> str:
    e = (endpoint or "").strip().upper()
    if e in ("MIC", "MBC"):
        return "antimicrobial"
    if e in ("HEMOLYSIS", "HC50", "IC50", "CC50", "EC50", "GI50", "LC50", "LD50"):
        return "hemolysis"
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers-dir", required=True, help="Run papers dir containing *.xml and *_experimental_records.csv")
    ap.add_argument(
        "--records-in",
        default="",
        help="Input records CSV (default: <papers-dir>/screened_experimental_records.csv; fallback raw_experimental_records.csv)",
    )
    ap.add_argument("--out-methods-csv", default="", help="Output per-paper methods CSV path")
    ap.add_argument("--out-csv", default="", help="Output augmented records CSV path")
    ap.add_argument("--out-md", default="", help="Output Markdown report path")
    args = ap.parse_args()

    papers_dir = Path(args.papers_dir)
    if not papers_dir.exists():
        raise SystemExit(f"Not found: {papers_dir}")

    in_csv = Path(args.records_in) if args.records_in else (papers_dir / "screened_experimental_records.csv")
    if not in_csv.exists():
        in_csv = papers_dir / "raw_experimental_records.csv"
    if not in_csv.exists():
        raise SystemExit(f"Missing input records: {in_csv}")

    out_methods_csv = Path(args.out_methods_csv) if args.out_methods_csv else (papers_dir / "methods_conditions_by_paper.csv")
    out_csv = Path(args.out_csv) if args.out_csv else (papers_dir / "screened_experimental_records_with_methods.csv")
    out_md = Path(args.out_md) if args.out_md else (papers_dir / "methods_conditions_report.md")

    df = pd.read_csv(in_csv)
    for c in ("paper_stem", "endpoint", "source_path", "source_ref"):
        if c in df.columns:
            df[c] = df[c].astype("string")

    hit_papers = sorted({safe_str(x) for x in df.get("paper_stem", pd.Series([], dtype="string")).tolist() if safe_str(x)})
    if not hit_papers:
        raise SystemExit("No paper_stem found in input records.")

    paper_table_ids: dict[str, list[str]] = {}
    if "source_ref" in df.columns:
        for paper, sub in df.groupby("paper_stem"):
            tids: list[str] = []
            for sr in sub["source_ref"].dropna().astype(str).tolist():
                for tid in extract_table_ids(sr):
                    if tid not in tids:
                        tids.append(tid)
            paper_table_ids[safe_str(paper)] = tids

    paper_endpoints: dict[str, list[str]] = {}
    if "endpoint" in df.columns:
        for paper, sub in df.groupby("paper_stem"):
            eps: list[str] = []
            for e in sub["endpoint"].dropna().astype(str).tolist():
                e = e.strip()
                if e and e not in eps:
                    eps.append(e)
            paper_endpoints[safe_str(paper)] = eps

    methods_rows: list[dict[str, Any]] = []

    for paper in hit_papers:
        xml_path = papers_dir / f"{paper}.xml"
        if not xml_path.exists() and "source_path" in df.columns:
            sp = df.loc[df["paper_stem"].astype(str) == paper, "source_path"].dropna().astype(str).head(1)
            if len(sp) > 0:
                xml_path = Path(sp.iloc[0])

        rec: dict[str, Any] = {
            "paper_stem": paper,
            "xml_path": str(xml_path) if xml_path else "",
            "endpoints_in_records": ",".join(paper_endpoints.get(paper, [])),
        }

        if not xml_path or not xml_path.exists():
            rec["status"] = "missing_xml"
            methods_rows.append(rec)
            continue

        try:
            root = parse_xml(xml_path)
        except Exception as e:
            rec["status"] = f"xml_parse_error:{type(e).__name__}"
            methods_rows.append(rec)
            continue

        sections = iter_sections(root)
        rec["status"] = "ok"

        table_ids = paper_table_ids.get(paper, [])
        table_texts = [table_wrap_text(root, tid) for tid in table_ids]

        abx_text, abx_titles = pick_relevant_text(
            sections,
            title_keywords=["mic", "mbc", "antibacterial", "antimicrobial", "antimicrobial assay", "antibacterial assays"],
            fallback_keywords=["organisms", "culture condition", "assay"],
            extra_texts=table_texts,
        )
        abx_fields = extract_method_fields(abx_text)
        rec["abx_sec_titles"] = " | ".join(abx_titles)
        rec["abx_evidence"] = extract_evidence_sentences(abx_text)
        for k, v in abx_fields.items():
            rec[f"abx_{k}"] = v

        hem_text, hem_titles = pick_relevant_text(
            sections,
            title_keywords=["hemolysis", "hemolytic", "erythro", "red blood", "rbc", "selectivity index", "hc50"],
            fallback_keywords=["hemolysis", "safety", "cytotoxic", "cell"],
            extra_texts=table_texts,
        )
        hem_fields = extract_method_fields(hem_text)
        rec["hem_sec_titles"] = " | ".join(hem_titles)
        rec["hem_evidence"] = extract_evidence_sentences(hem_text)
        for k, v in hem_fields.items():
            rec[f"hem_{k}"] = v

        rec["table_ids_used"] = " | ".join(table_ids)
        methods_rows.append(rec)

    methods_df = pd.DataFrame(methods_rows)
    methods_df.to_csv(out_methods_csv, index=False)

    methods_map = {safe_str(r.get("paper_stem")): r for r in methods_rows}

    def pick_method_value(row: pd.Series, key: str) -> str:
        paper = safe_str(row.get("paper_stem"))
        endpoint = safe_str(row.get("endpoint"))
        grp = endpoint_group(endpoint)
        r = methods_map.get(paper) or {}
        if grp == "antimicrobial":
            return safe_str(r.get(f"abx_{key}"))
        if grp == "hemolysis":
            return safe_str(r.get(f"hem_{key}"))
        return ""

    def pick_method_titles(row: pd.Series) -> str:
        paper = safe_str(row.get("paper_stem"))
        endpoint = safe_str(row.get("endpoint"))
        grp = endpoint_group(endpoint)
        r = methods_map.get(paper) or {}
        if grp == "antimicrobial":
            return safe_str(r.get("abx_sec_titles"))
        if grp == "hemolysis":
            return safe_str(r.get("hem_sec_titles"))
        return ""

    def pick_method_evidence(row: pd.Series) -> str:
        paper = safe_str(row.get("paper_stem"))
        endpoint = safe_str(row.get("endpoint"))
        grp = endpoint_group(endpoint)
        r = methods_map.get(paper) or {}
        if grp == "antimicrobial":
            return safe_str(r.get("abx_evidence"))
        if grp == "hemolysis":
            return safe_str(r.get("hem_evidence"))
        return ""

    def pick_method_source_ref(row: pd.Series) -> str:
        paper = safe_str(row.get("paper_stem"))
        r = methods_map.get(paper) or {}
        xml_path = safe_str(r.get("xml_path"))
        table_ids = safe_str(r.get("table_ids_used"))
        titles = pick_method_titles(row)
        parts: list[str] = []
        if xml_path:
            parts.append(f"source_path={xml_path}")
        if titles:
            parts.append(f"sec_titles={titles}")
        if table_ids:
            parts.append(f"table_ids={table_ids}")
        return ";".join(parts)

    df["method_sec_titles"] = df.apply(pick_method_titles, axis=1)
    df["method_evidence"] = df.apply(pick_method_evidence, axis=1)
    df["method_source_ref"] = df.apply(pick_method_source_ref, axis=1)

    for k in ("guideline", "assay_method", "medium", "inoculum", "incubation", "plate", "volume", "readout", "rbc_source", "rbc_conc"):
        df[f"method_{k}"] = df.apply(lambda r: pick_method_value(r, k), axis=1)

    df.to_csv(out_csv, index=False)

    ok_papers = [r for r in methods_rows if r.get("status") == "ok"]
    missing_xml = [r for r in methods_rows if str(r.get("status") or "") == "missing_xml"]
    parse_err = [r for r in methods_rows if str(r.get("status") or "").startswith("xml_parse_error")]

    def count_nonempty(col: str) -> int:
        return int(sum(1 for r in ok_papers if safe_str(r.get(col))))

    report_lines = [
        "# Methods Conditions Augmentation Report",
        "",
        f"Generated at: {now_local_str()}",
        f"Input records: `{in_csv}`",
        f"Papers dir: `{papers_dir}`",
        "",
        "## Coverage",
        f"- hit_papers: {len(hit_papers)}",
        f"- xml_ok: {len(ok_papers)}",
        f"- missing_xml: {len(missing_xml)}",
        f"- xml_parse_error: {len(parse_err)}",
        "",
        "## Field Coverage (papers with non-empty)",
        f"- antimicrobial.guideline: {count_nonempty('abx_guideline')}",
        f"- antimicrobial.assay_method: {count_nonempty('abx_assay_method')}",
        f"- antimicrobial.medium: {count_nonempty('abx_medium')}",
        f"- antimicrobial.inoculum: {count_nonempty('abx_inoculum')}",
        f"- antimicrobial.incubation: {count_nonempty('abx_incubation')}",
        f"- hemolysis.rbc_source: {count_nonempty('hem_rbc_source')}",
        f"- hemolysis.rbc_conc: {count_nonempty('hem_rbc_conc')}",
        f"- hemolysis.incubation: {count_nonempty('hem_incubation')}",
        "",
        "## Outputs",
        f"- Per-paper: `{out_methods_csv}`",
        f"- Augmented records: `{out_csv}`",
        f"- Report: `{out_md}`",
        "",
    ]

    if missing_xml:
        report_lines.append("## Missing XML")
        for r in missing_xml:
            report_lines.append(f"- {r.get('paper_stem')}")
        report_lines.append("")

    if parse_err:
        report_lines.append("## XML Parse Errors")
        for r in parse_err:
            report_lines.append(f"- {r.get('paper_stem')}: {r.get('status')}")
        report_lines.append("")

    out_md.write_text("\n".join(report_lines), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
