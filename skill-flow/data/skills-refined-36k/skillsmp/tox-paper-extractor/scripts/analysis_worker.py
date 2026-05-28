#!/usr/bin/env python3
"""
Multi-worker per-paper analysis loop:
  - Claim a task via atomic mv (pending -> in_progress)
  - Run `codex exec` with a fixed prompt template + per-paper context
  - Write one-paper-per-file outputs (JSON + MD)
  - Mark task done/failed (mv -> done/failed)
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import shutil
import time
import zipfile
import html
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from string import Template

import xml.etree.ElementTree as ET

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None  # type: ignore

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None  # type: ignore


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def atomic_write_json(path: Path, obj: object) -> None:
    atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def safe_rel(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except Exception:
        return str(path)


def list_files_block(root: Path, *, max_files: int = 200, base: Path | None = None) -> str:
    if not root.exists() or not root.is_dir():
        return "(none)"
    files = [p for p in root.rglob("*") if p.is_file()]
    files_sorted = sorted(files, key=lambda p: str(p).lower())
    lines: list[str] = []
    for p in files_sorted[:max_files]:
        rel = safe_rel(p, base) if base else str(p)
        try:
            size = p.stat().st_size
            lines.append(f"- {rel} ({size} bytes)")
        except Exception:
            lines.append(f"- {rel}")
    if len(files_sorted) > max_files:
        lines.append(f"... ({len(files_sorted) - max_files} more files)")
    return "\n".join(lines) if lines else "(none)"


def list_extracted_tables_block(papers_dir: Path, paper_id: str, *, max_tables: int = 200, base: Path | None = None) -> str:
    tables_dir = papers_dir / "extracted_tables"
    if not tables_dir.exists():
        return "(missing extracted_tables/)"
    files = sorted(tables_dir.glob(f"{paper_id}_*.csv"))
    if not files:
        return "(none)"
    lines: list[str] = []
    for p in files[:max_tables]:
        rel = safe_rel(p, base) if base else str(p)
        lines.append(f"- {rel}")
    if len(files) > max_tables:
        lines.append(f"... ({len(files) - max_tables} more tables)")
    return "\n".join(lines)


@dataclass(frozen=True)
class RecordsSummary:
    total_rows: int
    unique_sequences: int
    endpoint_counts: dict[str, int]
    sample_lines: list[str]


def summarize_raw_records(papers_dir: Path, paper_id: str, *, max_sample_rows: int = 40) -> RecordsSummary:
    path = papers_dir / "raw_experimental_records.csv"
    if not path.exists():
        return RecordsSummary(total_rows=0, unique_sequences=0, endpoint_counts={}, sample_lines=["(missing raw_experimental_records.csv)"])

    total = 0
    seqs: set[str] = set()
    endpoint_counts: dict[str, int] = {}
    sample: list[str] = []

    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pmcid = (row.get("pmcid") or "").strip()
            stem = (row.get("paper_stem") or "").strip()
            if pmcid != paper_id and stem != paper_id:
                continue
            total += 1
            seq = (row.get("sequence") or "").strip()
            if seq:
                seqs.add(seq)
            endpoint = (row.get("endpoint") or "").strip() or "(missing)"
            endpoint_counts[endpoint] = endpoint_counts.get(endpoint, 0) + 1

            if len(sample) < max_sample_rows:
                sample.append(
                    " | ".join(
                        [
                            f"peptide_id={row.get('peptide_id','')}",
                            f"sequence={seq[:60]}{'…' if len(seq)>60 else ''}",
                            f"endpoint={endpoint}",
                            f"cmp={row.get('cmp','')}",
                            f"value={row.get('value','')}",
                            f"unit={row.get('unit','')}",
                            f"condition={row.get('condition','')}",
                            f"source_ref={row.get('source_ref','')}",
                        ]
                    )
                )

    counts_sorted = dict(sorted(endpoint_counts.items(), key=lambda kv: (-kv[1], kv[0])))
    return RecordsSummary(total_rows=total, unique_sequences=len(seqs), endpoint_counts=counts_sorted, sample_lines=sample or ["(no rows found for this paper_id)"])


def format_records_summary_block(summary: RecordsSummary) -> str:
    lines: list[str] = []
    lines.append(f"total_rows={summary.total_rows}")
    lines.append(f"unique_sequences={summary.unique_sequences}")
    if summary.endpoint_counts:
        lines.append("endpoint_counts:")
        for k, v in list(summary.endpoint_counts.items())[:30]:
            lines.append(f"- {k}: {v}")
        if len(summary.endpoint_counts) > 30:
            lines.append(f"... ({len(summary.endpoint_counts) - 30} more endpoints)")
    lines.append("sample_rows:")
    for s in summary.sample_lines:
        lines.append(f"- {s}")
    return "\n".join(lines)


AA_ALLOWED = "ACDEFGHIKLMNPQRSTVWYBXZJUO"
AA_ALLOWED_SET = set(AA_ALLOWED)

ENDPOINT_KEYWORDS = (
    "LD50",
    "LC50",
    "IC50",
    "EC50",
    "CC50",
    "HC50",
    "HC10",
    "MHC10",
    "MHC",
    "MIC",
    "MBC",
    "GI50",
    "KI",
    "KD",
    "HEMOLYSIS",
)


def truncate_line(line: str, *, max_chars: int = 240) -> str:
    s = (line or "").rstrip("\n")
    if len(s) <= max_chars:
        return s
    if max_chars <= 1:
        return "…"
    return s[: max_chars - 1] + "…"


def read_text_preview_lines(path: Path, *, max_lines: int = 18, max_chars: int = 240) -> list[str]:
    lines: list[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(truncate_line(line, max_chars=max_chars))
    except Exception as e:
        return [f"(preview_error: {e})"]
    return lines or ["(empty)"]


def endpoint_hit_score(text: str) -> int:
    t = (text or "").lower()
    score = 0
    for ep in ENDPOINT_KEYWORDS:
        if ep.lower() in t:
            score += 2
    # Sequence hints help prioritize tables that actually contain AA strings.
    if "sequence" in t or "aa sequence" in t or "amino acid" in t or "primary structure" in t:
        score += 1
    if "peptide" in t or "peptides" in t:
        score += 1
    return score


def build_csv_table_previews_block(
    *, papers_dir: Path, paper_id: str, docs_root: Path, max_tables: int = 5, max_lines: int = 18
) -> str:
    tables_dir = papers_dir / "extracted_tables"
    if not tables_dir.exists():
        return "(missing extracted_tables/)"
    files = sorted(tables_dir.glob(f"{paper_id}_*.csv"))
    if not files:
        return "(none)"

    scored: list[tuple[int, int, str, Path, list[str]]] = []
    for p in files:
        preview = read_text_preview_lines(p, max_lines=max_lines, max_chars=240)
        joined = " ".join(preview)
        score = endpoint_hit_score(joined)
        try:
            size = int(p.stat().st_size)
        except Exception:
            size = 0
        scored.append((score, size, str(p).lower(), p, preview))

    scored.sort(key=lambda x: (-x[0], -x[1], x[2]))
    picked = scored[: max(0, int(max_tables))]

    lines: list[str] = []
    for score, size, _k, p, preview in picked:
        rel = safe_rel(p, docs_root)
        lines.append(f"- {rel} (score={score}, size={size} bytes)")
        lines.append("```")
        for i, ln in enumerate(preview, 1):
            lines.append(f"{i:02d}: {ln}")
        lines.append("```")
    if len(scored) > len(picked):
        lines.append(f"... ({len(scored) - len(picked)} more tables not previewed)")
    return "\n".join(lines) if lines else "(none)"


def docx_text_preview(path: Path, *, max_chars: int = 3500) -> str:
    """
    Extract a short, best-effort text preview from a .docx (zip) without extra deps.
    """
    try:
        with zipfile.ZipFile(path, "r") as z:
            data = z.read("word/document.xml")
        xml_text = data.decode("utf-8", errors="ignore")
        parts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml_text)
        joined = " ".join(html.unescape(p) for p in parts)
        joined = re.sub(r"\s+", " ", joined).strip()
        if not joined:
            return "(empty docx text)"
        if len(joined) > max_chars:
            joined = joined[: max_chars - 1] + "…"
        return joined
    except Exception as e:
        return f"(docx preview error: {e})"


def excel_preview(path: Path, *, max_rows: int = 12, max_chars: int = 3500) -> str:
    if pd is None:
        return "(xlsx preview unavailable: pandas not installed)"
    try:
        xls = pd.ExcelFile(path)
        sheets = list(xls.sheet_names or [])
        out_lines: list[str] = []
        if sheets:
            show = sheets[:5]
            out_lines.append("sheets: " + ", ".join(show) + (" ..." if len(sheets) > len(show) else ""))
            df = pd.read_excel(path, sheet_name=show[0], nrows=max_rows)
        else:
            df = pd.read_excel(path, nrows=max_rows)
        csv_text = df.to_csv(index=False)
        csv_text = re.sub(r"\r\n?", "\n", csv_text).strip()
        if len(csv_text) > max_chars:
            csv_text = csv_text[: max_chars - 1] + "…"
        out_lines.append(csv_text or "(empty sheet)")
        return "\n".join(out_lines).strip()
    except Exception as e:
        return f"(xlsx preview error: {e})"


def build_supp_previews_block(*, supp_dir: Path, docs_root: Path, max_files: int = 6) -> str:
    if not supp_dir.exists() or not supp_dir.is_dir():
        return "(none)"

    files = [p for p in supp_dir.rglob("*") if p.is_file()]
    if not files:
        return "(none)"

    def ext_priority(p: Path) -> int:
        ext = p.suffix.lower()
        if ext in (".xlsx", ".xls"):
            return 100
        if ext in (".csv", ".tsv"):
            return 90
        if ext in (".fa", ".fasta", ".faa", ".fna"):
            return 80
        if ext in (".txt",):
            return 70
        if ext in (".docx",):
            return 60
        return 10

    ranked: list[tuple[int, int, str, Path]] = []
    for p in files:
        try:
            size = int(p.stat().st_size)
        except Exception:
            size = 0
        ranked.append((ext_priority(p), size, str(p).lower(), p))
    ranked.sort(key=lambda x: (-x[0], -x[1], x[2]))

    picked = [p for _pri, _sz, _k, p in ranked[: max(0, int(max_files))]]

    lines: list[str] = []
    for p in picked:
        rel = safe_rel(p, docs_root)
        ext = p.suffix.lower()
        try:
            size = int(p.stat().st_size)
        except Exception:
            size = 0
        lines.append(f"- {rel} (size={size} bytes)")
        lines.append("```")
        if ext in (".csv", ".tsv", ".txt", ".fa", ".fasta", ".faa", ".fna"):
            for i, ln in enumerate(read_text_preview_lines(p, max_lines=18, max_chars=240), 1):
                lines.append(f"{i:02d}: {ln}")
        elif ext in (".xlsx", ".xls"):
            preview = excel_preview(p, max_rows=12, max_chars=3500)
            for i, ln in enumerate(preview.splitlines()[:40], 1):
                lines.append(f"{i:02d}: {truncate_line(ln, max_chars=240)}")
        elif ext in (".docx",):
            preview = docx_text_preview(p, max_chars=3500)
            for i, ln in enumerate(preview.splitlines()[:40], 1):
                lines.append(f"{i:02d}: {truncate_line(ln, max_chars=240)}")
        else:
            lines.append("(binary/unknown format: no preview)")
        lines.append("```")

    if len(files) > len(picked):
        lines.append(f"... ({len(files) - len(picked)} more supplementary files not previewed)")
    return "\n".join(lines) if lines else "(none)"


def normalize_whitespace(text: str) -> str:
    t = (text or "").replace("＞", ">").replace("＜", "<")
    return re.sub(r"\s+", " ", t).strip()


def standardize_aa_sequence(seq: str) -> str:
    """
    Best-effort peptide AA standardization.

    Goals:
    - Keep raw extraction auditable (we still store `value_text` etc), but for `sequence`
      we prefer a clean AA-only string.
    - Avoid common chemistry prefixes/suffixes (e.g., `CH3-(CH2)n-CONH-...`, `H2N-...`,
      `...-NH2`) being interpreted as AA letters.
    """
    if not seq:
        return ""

    raw = normalize_whitespace(seq).upper()

    # Guardrail: some extractions capture biological descriptions (cell lines/controls/oils)
    # that are made entirely of AA letters. Drop these instead of hallucinating a sequence.
    # This keeps `sequence` conservative while `value_text` remains fully auditable.
    non_seq_markers = (
        "HUMAN",
        "MOUSE",
        "RAT",
        "CELL",
        "CELLS",
        "CANCER",
        "CONTROL",
        "GROUP",
        "OIL",
    )
    if any(m in raw for m in non_seq_markers):
        return ""

    # Fast path: looks like a plain 1-letter AA sequence with separators/spaces.
    if re.fullmatch(r"[A-Z\s\-–—_]+", raw) and not re.search(r"\b(NH2|H2N|PEG)\b", raw):
        tokens = [t for t in re.split(r"[-–—_\s]+", raw) if t]
        # Drop common chemistry tokens when they are separated by delimiters (e.g., "CONH-PEPTIDE").
        while tokens and tokens[0] in {"CONH"}:
            tokens = tokens[1:]
        while tokens and tokens[-1] in {"CONH"}:
            tokens = tokens[:-1]
        s = re.sub(r"[^A-Z]", "", "".join(tokens))
        cleaned = "".join(ch for ch in s if ch in AA_ALLOWED_SET)
        # Handle cases where chemistry got concatenated (no delimiter survived).
        if cleaned.startswith("CONH") and len(cleaned) > len("CONH"):
            cleaned = cleaned[len("CONH") :]
        return cleaned

    # General path: split on non-letters first, then choose the longest AA-like run.
    # This avoids concatenating chemistry tokens like `CONH` into the peptide sequence.
    letter_runs = [m.group(0) for m in re.finditer(r"[A-Z]+", raw)]
    candidates: list[str] = []
    for run in letter_runs:
        cand = "".join(ch for ch in run if ch in AA_ALLOWED_SET)
        if cand:
            candidates.append(cand)
    if not candidates:
        return ""

    best = max(candidates, key=len)
    # Avoid returning tiny fragments like 'NH' from '-NH2' suffixes.
    if len(best) < 4:
        return ""
    if best.startswith("CONH") and len(best) > len("CONH"):
        best = best[len("CONH") :]
    return best


def looks_numeric_like(text: str) -> bool:
    # Column-scoring helper; keep it conservative to avoid treating IDs (e.g., 'L-6')
    # or strain IDs as numeric measurements.
    s = normalize_whitespace(text)
    if not s:
        return False
    s_low = s.lower()
    if s_low in {"nd", "n.d.", "na", "n/a", "-", "—"}:
        return False
    # If it contains letters, it's usually an identifier (peptide label, organism, etc.).
    # Most measurement cells in our extracted tables are digit/punct-only.
    if re.search(r"[A-Za-z]", s):
        return False
    # Ignore long integer IDs as measurements (e.g., isolate IDs).
    if re.fullmatch(r"\d{7,}", s):
        return False
    return bool(re.search(r"\d", s))


def looks_numeric_value(text: str) -> bool:
    """
    Stricter numeric detector for *data* cells (avoid headers like 'IC50 (μM)').
    """
    s = normalize_whitespace(text)
    if not s:
        return False
    s_low = s.lower()
    if s_low in {"nd", "n.d.", "na", "n/a", "-", "—"}:
        return False
    # Strip common footnote markers.
    s = re.sub(r"[\*\u2020\u2021\u00a7\u00b6]+", "", s).strip()
    # Avoid misclassifying peptide IDs like 'L-6' / 'CM1' as numeric.
    if re.search(r"[A-Za-z]", s):
        return False
    # Avoid long isolate IDs as measurements.
    if re.fullmatch(r"\d{7,}", s):
        return False
    return bool(re.search(r"\d", s))


def parse_unit_from_text(text: str) -> str:
    s = normalize_whitespace(text)
    if not s:
        return ""
    s = s.replace("ug", "μg").replace("µg", "μg").replace("uM", "μM").replace("µM", "μM")

    # Prefer explicit parentheses, but also capture outer unit tokens if present.
    unit_re = r"(μg/mL|μg/ml|mg/mL|mg/ml|mg/L|g/L|μM|nM|mM|μg/g)"
    outer_units = re.findall(unit_re, s, flags=re.IGNORECASE)
    # Only treat '%' as a unit when it is not part of a media composition like "100% MHB".
    if re.search(r"(?<!\d)%", s):
        outer_units.append("%")
    outer_units_norm: list[str] = []
    for u in outer_units:
        u2 = u.replace("μg/ml", "μg/mL").replace("mg/ml", "mg/mL")
        if u2.lower() == "nm":
            u2 = "nM"
        if u2.lower() == "mm":
            u2 = "mM"
        outer_units_norm.append(u2)
    outer_units_norm = list(dict.fromkeys(outer_units_norm))

    m = re.search(r"\(([^()]{1,40})\)", s)
    if m:
        inner = normalize_whitespace(m.group(1))
        inner = inner.replace("μg/ml", "μg/mL").replace("mg/ml", "mg/mL")
        inner_units = re.findall(unit_re, inner, flags=re.IGNORECASE)
        if re.search(r"(?<!\d)%", inner):
            inner_units.append("%")
        inner_units_norm: list[str] = []
        for u in inner_units:
            u2 = u.replace("μg/ml", "μg/mL").replace("mg/ml", "mg/mL")
            if u2.lower() == "nm":
                u2 = "nM"
            if u2.lower() == "mm":
                u2 = "mM"
            inner_units_norm.append(u2)
        inner_units_norm = list(dict.fromkeys(inner_units_norm))
        if outer_units_norm:
            outer = outer_units_norm[0]
            # Only keep inner text if it also contains a recognized unit token.
            if inner_units_norm:
                inner_u = inner_units_norm[0]
                if inner_u and inner_u not in outer:
                    return f"{outer} ({inner_u})"
            return outer
        if inner_units_norm:
            return inner_units_norm[0]
        return ""

    if outer_units_norm:
        return outer_units_norm[0]
    return ""


def extract_endpoints_from_text(text: str) -> list[str]:
    s = normalize_whitespace(text)
    if not s:
        return []
    up = s.upper()
    up = up.replace("IC 50", "IC50").replace("EC 50", "EC50").replace("CC 50", "CC50").replace("HC 50", "HC50")
    up = up.replace("LD 50", "LD50").replace("LC 50", "LC50").replace("GI 50", "GI50")

    found: list[str] = []
    # Avoid substring false positives (e.g., antiMICrobial) by using word boundaries for short tokens.
    for ep in ENDPOINT_KEYWORDS:
        if ep in {"MIC", "MBC"}:
            if re.search(rf"\b{ep}S?\b", up):
                found.append(ep)
            continue
        if ep == "HEMOLYSIS":
            if re.search(r"\bHEMOLYSIS\b", up) or re.search(r"\bHEMOLYT", up):
                found.append("HEMOLYSIS")
                continue
            # Common experimental synonym: "erythrocyte lysis" / "RBC lysis".
            if ("ERYTHROCYTE" in up and "LYSIS" in up) or ("RBC" in up and "LYSIS" in up):
                found.append("HEMOLYSIS")
            continue
        if re.search(rf"\b{re.escape(ep)}\b", up):
            found.append(ep)
    return found


def is_derived_endpoint_label(label: str) -> bool:
    s = normalize_whitespace(label).lower()
    if not s:
        return False
    if "selectivity" in s or "therapeutic" in s:
        return True
    if re.search(r"\b(si|ti)\b", s):
        return True
    if "inhibition" in s and "%" in s:
        return True
    if "inhibition rate" in s:
        return True
    # Ratios/indices derived from primary endpoints (do not treat as standalone endpoints).
    if re.search(r"\b(index|ratio)\b", s) and re.search(r"\b(mic|mbc|mfc|mhc|ic50|ec50|hc50|ld50|cc50)\b", s):
        return True
    if re.search(r"\b(mic|mbc|mfc|mhc)\s*/\s*(mic|mbc|mfc|mhc)\b", s):
        return True
    return False


def parse_value_fields(value_text: str) -> dict:
    s = normalize_whitespace(value_text)
    if not s:
        return {"value_text": "", "value": None, "error": "", "cmp": "", "range_low": None, "range_high": None}

    s_norm = s.replace("≥", ">=").replace("≤", "<=")
    # Normalize Unicode minus/dash so numeric parsing is stable across publishers.
    s_norm = s_norm.replace("−", "-").replace("–", "-").replace("—", "-")
    cmp_ = ""
    m = re.match(r"^(>=|<=|>|<)\s*(.+)$", s_norm)
    if m:
        cmp_ = m.group(1)
        s_norm = m.group(2).strip()

    range_low = None
    range_high = None
    m = re.match(r"^(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)$", s_norm)
    if m:
        try:
            range_low = float(m.group(1))
            range_high = float(m.group(2))
        except Exception:
            range_low = None
            range_high = None

    err = ""
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(?:±|\+/-|\+\-)\s*(\d+(?:\.\d+)?)$", s_norm)
    if m:
        try:
            v = float(m.group(1))
            err = m.group(2)
            return {"value_text": s, "value": v, "error": err, "cmp": cmp_, "range_low": None, "range_high": None}
        except Exception:
            pass

    value = None
    m = re.search(r"(-?\d+(?:\.\d+)?)", s_norm)
    if m:
        try:
            value = float(m.group(1))
        except Exception:
            value = None

    return {"value_text": s, "value": value, "error": err, "cmp": cmp_, "range_low": range_low, "range_high": range_high}


def parse_jats_citation(xml_path: Path) -> dict:
    if not xml_path.exists():
        return {}
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        title_elem = root.find(".//{*}article-title")
        doi_elem = root.find(".//{*}article-id[@pub-id-type='doi']")
        pmid_elem = root.find(".//{*}article-id[@pub-id-type='pmid']")
        pmcid_elem = root.find(".//{*}article-id[@pub-id-type='pmcid']")
        return {
            "title": normalize_whitespace("".join(title_elem.itertext())) if title_elem is not None else "",
            "doi": normalize_whitespace("".join(doi_elem.itertext())) if doi_elem is not None else "",
            "pmid": normalize_whitespace("".join(pmid_elem.itertext())) if pmid_elem is not None else "",
            "pmcid": normalize_whitespace("".join(pmcid_elem.itertext())) if pmcid_elem is not None else "",
        }
    except Exception:
        return {}


def parse_jats_table_meta(xml_path: Path) -> dict[str, dict]:
    meta: dict[str, dict] = {}
    if not xml_path.exists():
        return meta
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        for tw in root.findall(".//{*}table-wrap"):
            tid = (tw.get("id") or "").strip()
            if not tid:
                continue
            label_elem = tw.find("{*}label")
            cap_elem = tw.find("{*}caption")
            foot_elem = tw.find("{*}table-wrap-foot")
            meta[tid] = {
                "table_id": tid,
                "label": normalize_whitespace("".join(label_elem.itertext())) if label_elem is not None else "",
                "caption": normalize_whitespace("".join(cap_elem.itertext())) if cap_elem is not None else "",
                "footnotes": normalize_whitespace("".join(foot_elem.itertext())) if foot_elem is not None else "",
            }
    except Exception:
        return meta
    return meta


def guess_header_rows(rows: list[list[str]], *, max_header_rows: int = 3) -> int:
    if not rows:
        return 1
    max_header_rows = max(1, min(max_header_rows, len(rows)))

    def build_headers(n: int) -> list[str]:
        n_cols = max(len(r) for r in rows[:n])
        headers: list[str] = []
        for c in range(n_cols):
            parts: list[str] = []
            for r in rows[:n]:
                if c < len(r):
                    v = normalize_whitespace(r[c])
                    if v:
                        parts.append(v)
            headers.append(" | ".join(parts))
        return headers

    def looks_like_data_row(row: list[str]) -> bool:
        if not row:
            return False
        first = normalize_whitespace(row[0] if row else "")
        if not first:
            return False
        first_low = first.lower()
        if re.search(r"\b(table|supplementary|note|footnote)\b", first_low):
            return False
        # Many tables repeat a label like "Tested microorganisms" across header rows.
        if re.search(r"\b(microorganism|microorganisms|organism|organisms|strain|strains|cells|cell line)\b", first_low):
            return False
        # Special-case: concentration/dose header rows, e.g. "Peptides (μM), 2, 4, 8, ..."
        # These often look numeric and can be misclassified as data rows.
        if re.search(r"\b(peptides?|concentration|dose|conc)\b", first_low) and parse_unit_from_text(first):
            return False
        # If it has multiple numeric-like cells, it's almost certainly a data row even if
        # some cells are 'ND'/'NA' (which would otherwise reduce numeric ratio).
        numeric_like = 0
        for v in row[1:]:
            vv = normalize_whitespace(v)
            if not vv:
                continue
            if vv.lower() in {"nd", "n.d.", "na", "n/a", "-", "—"}:
                continue
            if looks_numeric_value(vv) or re.match(r"^[<>≤≥]?\s*\d", vv):
                numeric_like += 1
        return numeric_like >= 2

    best_n = 1
    best_score = -1
    for n in range(1, max_header_rows + 1):
        if n > 1:
            last = rows[n - 1]
            non_empty = sum(1 for v in last if normalize_whitespace(v))
            numeric_vals = sum(1 for v in last if looks_numeric_value(v))
            first = normalize_whitespace(last[0] if last else "")
            first_low = first.lower()
            is_conc_header_row = bool(re.search(r"\b(peptides?|concentration|dose|conc)\b", first_low) and parse_unit_from_text(first))
            if looks_like_data_row(last):
                continue
            # Concentration header rows are often mostly numeric by design; keep them as header rows.
            if (not is_conc_header_row) and non_empty and (numeric_vals / max(1, non_empty)) >= 0.5:
                # Likely a data row; don't treat it as part of the header.
                continue
        headers = build_headers(n)
        endpoint_cols = sum(1 for h in headers if extract_endpoints_from_text(h))
        sample = rows[n : n + 10]
        n_cols = len(headers)
        meas_cols = 0
        for c in range(n_cols):
            non_empty = 0
            numeric_like = 0
            for r in sample:
                if c >= len(r):
                    continue
                cell = normalize_whitespace(r[c])
                if not cell:
                    continue
                if cell.lower() in {"nd", "n.d.", "na", "n/a", "-", "—"}:
                    continue
                non_empty += 1
                if looks_numeric_like(cell):
                    numeric_like += 1
            if non_empty and (numeric_like / max(1, non_empty)) >= 0.5:
                meas_cols += 1
        score = endpoint_cols * 10 + meas_cols
        if score > best_score or (score == best_score and n > best_n):
            best_score = score
            best_n = n
    return best_n


def extract_sequences_from_extracted_tables(
    table_paths: list[Path],
    *,
    docs_root: Path,
) -> tuple[dict[str, str], list[dict]]:
    seq_map: dict[str, str] = {}
    sources: list[dict] = []
    for p in table_paths:
        try:
            with p.open("r", encoding="utf-8", errors="ignore", newline="") as f:
                rows = list(csv.reader(f))
        except Exception:
            continue
        if not rows:
            continue
        header_n = guess_header_rows(rows, max_header_rows=3)
        header_rows = rows[:header_n]
        data_rows = rows[header_n:]

        n_cols = max(len(r) for r in header_rows) if header_rows else max(len(r) for r in rows)
        col_headers: list[str] = []
        for c in range(n_cols):
            parts: list[str] = []
            for r in header_rows:
                if c < len(r):
                    v = normalize_whitespace(r[c])
                    if v:
                        parts.append(v)
            col_headers.append(" | ".join(parts))

        def find_col(keys: tuple[str, ...]) -> int:
            for i, h in enumerate(col_headers):
                h_low = h.lower()
                for k in keys:
                    if k in h_low:
                        return i
            return -1

        seq_col = find_col(("sequence", "aa sequence", "amino acid", "primary structure", "primary sequence"))
        if seq_col < 0:
            continue

        peptide_col = find_col(("peptide", "name", "label", "compound", "id"))
        if peptide_col < 0:
            # Heuristic: if first column is non-empty identifiers, treat it as peptide id.
            if data_rows:
                sample = [normalize_whitespace(r[0]) for r in data_rows[:20] if r and normalize_whitespace(r[0])]
                if sample and sum(1 for x in sample if not looks_numeric_like(x)) / len(sample) >= 0.7:
                    peptide_col = 0

        for ridx0, row in enumerate(data_rows, start=header_n + 1):
            peptide_id = normalize_whitespace(row[peptide_col]) if (peptide_col >= 0 and peptide_col < len(row)) else ""
            seq_raw = normalize_whitespace(row[seq_col]) if seq_col < len(row) else ""
            seq = standardize_aa_sequence(seq_raw)
            if not peptide_id or not seq:
                continue
            if peptide_id not in seq_map:
                seq_map[peptide_id] = seq
                sources.append(
                    {
                        "peptide_id": peptide_id,
                        "sequence": seq,
                        "source": {
                            "kind": "xml_table",
                            "file": safe_rel(p, docs_root),
                            "ref": f"{p.name} row {ridx0} col {col_headers[seq_col] or f'col_{seq_col+1}'}",
                        },
                    }
                )
    return seq_map, sources


def extract_sequences_from_xml_text(xml_path: Path, known_peptide_ids: list[str], *, docs_root: Path) -> tuple[dict[str, str], list[dict]]:
    if not xml_path.exists():
        return {}, []
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        text = normalize_whitespace(" ".join(root.itertext()))
    except Exception:
        text = normalize_whitespace(xml_path.read_text(encoding="utf-8", errors="ignore"))

    found_map: dict[str, str] = {}
    sources: list[dict] = []

    for pid in known_peptide_ids:
        if not pid:
            continue
        patterns = [
            # Prefer explicit delimiters to avoid false positives like "sequence accessible in the database..."
            re.compile(
                re.escape(pid)
                + r".{0,500}?"
                + r"(?:amino\s+acid\s+sequence|aa\s+sequence|sequence|seq\.?)\s*(?::|=)\s*"
                + r"([ACDEFGHIKLMNPQRSTVWYBXZJUO\-\s]{10,180})",
                flags=re.IGNORECASE | re.DOTALL,
            ),
            # Prose without explicit ':'/'=' (e.g., "with aminoacidic sequence GLLR...").
            re.compile(
                re.escape(pid)
                + r".{0,500}?"
                + r"(?:amino\s*acidic\s+sequence|aminoacidic\s+sequence|amino\s+acid\s+sequence|aa\s+sequence)\s+"
                + r"([ACDEFGHIKLMNPQRSTVWYBXZJUO\-\s]{10,180}?)"
                + r"(?=\s+(?:and|of|the|with|degree|purity|was|is|are)\b|$)",
                flags=re.IGNORECASE | re.DOTALL,
            ),
            # Common prose: "... with a sequence of KRFK...".
            # Keep the capture strict (single AA token) to avoid matching normal English phrases.
            re.compile(
                re.escape(pid) + r".{0,500}?\bsequence\s+of\s+([ACDEFGHIKLMNPQRSTVWYBXZJUO]{10,120})\b",
                flags=re.IGNORECASE | re.DOTALL,
            ),
            # Common "PeptideName (SEQUENCE)" pattern.
            re.compile(
                re.escape(pid) + r"\s*\(\s*([ACDEFGHIKLMNPQRSTVWYBXZJUO\-\s]{10,180})\s*\)",
                flags=re.IGNORECASE | re.DOTALL,
            ),
        ]

        m = None
        for pat in patterns:
            m = pat.search(text)
            if m:
                break
        if not m:
            continue

        seq = standardize_aa_sequence(m.group(1))
        if not seq:
            continue

        found_map[pid] = seq
        excerpt = normalize_whitespace(text[max(0, m.start() - 120) : m.end() + 40])
        sources.append(
            {
                "peptide_id": pid,
                "sequence": seq,
                "source": {
                    "kind": "text",
                    "file": safe_rel(xml_path, docs_root),
                    "ref": f"XML text excerpt: {excerpt[:240]}{'…' if len(excerpt)>240 else ''}",
                },
            }
        )

    # NOTE: Do not auto-assign a single free-floating AA-like token to a peptide_id.
    # Many English words can be composed solely of AA letters; keep this strict/traceable.

    return found_map, sources


def clean_peptide_id(text: str) -> str:
    s = normalize_whitespace(text)
    if not s:
        return ""
    s = re.sub(r"(?i)^peptide\s*", "", s)
    s = re.sub(r"\s*\*+$", "", s)
    return s.strip()


def extract_records_from_extracted_table(
    csv_path: Path,
    *,
    table_meta: dict[str, dict],
    sequences: dict[str, str],
    default_peptide_id: str,
    docs_root: Path,
) -> tuple[list[dict], dict]:
    qc: dict = {"tables_parsed": 0, "tables_skipped_derived": 0, "tables_skipped_no_endpoint": 0}
    try:
        with csv_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
            rows = list(csv.reader(f))
    except Exception:
        return [], qc
    if not rows:
        return [], qc

    table_id = ""
    m = re.match(r"^[^_]+_xml_(.+)\.csv$", csv_path.name)
    if m:
        table_id = m.group(1)
    meta = table_meta.get(table_id, {})
    label = meta.get("label") or ""
    caption = meta.get("caption") or ""
    footnotes = meta.get("footnotes") or ""

    header_n = guess_header_rows(rows, max_header_rows=3)
    header_rows = rows[:header_n]
    data_rows = rows[header_n:]

    n_cols = max(len(r) for r in header_rows)
    col_headers: list[str] = []
    for c in range(n_cols):
        parts: list[str] = []
        for r in header_rows:
            if c < len(r):
                v = normalize_whitespace(r[c])
                if v:
                    parts.append(v)
        col_headers.append(" | ".join(parts))

    table_endpoints = extract_endpoints_from_text(" ".join([label, caption, footnotes]))
    table_unit = parse_unit_from_text(" ".join([caption, footnotes]))

    peptide_col = -1
    seq_col = -1
    organism_col = -1
    for i, h in enumerate(col_headers):
        h_low = h.lower()
        if organism_col < 0 and any(k in h_low for k in ("microorganism", "organism", "bacteria", "strain", "cells", "cell line", "erythro")):
            # Avoid misclassifying "erythrocyte lysis"/hemolysis endpoint columns as organism columns.
            if ("erythro" in h_low and "lysis" in h_low) or ("hemolysis" in h_low) or ("hemolytic" in h_low):
                pass
            else:
                organism_col = i
        if peptide_col < 0 and any(k in h_low for k in ("peptide", "compound", "name", "label", "id")) and not extract_endpoints_from_text(h):
            peptide_col = i
        if seq_col < 0 and any(k in h_low for k in ("sequence", "aa sequence", "amino acid", "primary structure", "primary sequence")):
            seq_col = i

    measurement_cols: list[int] = []
    for c in range(n_cols):
        non_empty = 0
        numeric_like = 0
        for r in data_rows[:30]:
            if c >= len(r):
                continue
            cell = normalize_whitespace(r[c])
            if not cell:
                continue
            if cell.lower() in {"nd", "n.d.", "na", "n/a", "-", "—"}:
                continue
            non_empty += 1
            if looks_numeric_like(cell):
                numeric_like += 1
        if non_empty and (numeric_like / max(1, non_empty)) >= 0.5:
            measurement_cols.append(c)

    # Skip obvious non-experimental ML metric tables (common in toxin/hemolysis prediction papers).
    hdr_join = " ".join(col_headers).lower()
    if re.search(r"\broc\b|\bauc\b", hdr_join) and re.search(r"\baccuracy\b|\bprecision\b|\brecall\b|\bf1\b", hdr_join):
        qc["tables_skipped_no_endpoint"] += 1
        return [], qc

    def looks_like_peptide_label(token: str) -> bool:
        t = clean_peptide_id(token)
        if not t:
            return False
        t_low = t.lower()
        if t_low in {"nd", "n.d.", "na", "n/a"}:
            return False
        if t_low in {"unmodified", "glycosylated", "modified"}:
            return False
        if looks_numeric_like(t) or looks_numeric_value(t) or re.match(r"^[<>≤≥]\s*\\d", t):
            return False
        if extract_endpoints_from_text(t) or is_derived_endpoint_label(t):
            return False
        # Media/conditions are not peptides.
        if "%" in t:
            return False
        if re.search(r"(?i)\bMHB\b|\bMHB\s*II\b|\bTSB\b|\bPBS\b|mueller|hinton|broth|medium|media|buffer|tris", t):
            return False
        # Likely organism/strain labels, not peptides.
        if re.search(r"(?i)ATCC\s*\d+|\bMRSA\b|\bMSSA\b|\bESBL\b", t):
            return False
        # Common genus/species formatting ("E. coli", "Staphylococcus aureus", etc.).
        if re.search(r"(?i)^[A-Z]\.\s*[a-z]{3,}", t):
            return False
        if re.search(r"(?i)^[A-Z][a-z]{2,}\s+[a-z]{3,}", t):
            # Avoid filtering 2-word drug salt forms (e.g., "Kanamycin sulfate").
            parts = t.split()
            if len(parts) >= 2:
                second = parts[1].lower()
                if second not in {"sulfate", "chloride", "hydrochloride", "acetate", "phosphate", "nitrate", "sodium", "potassium"}:
                    return False
        # Common non-peptide column labels in MIC tables.
        if re.fullmatch(r"(?i)(od|o\.d\.|lum|rlu|abs|absorbance)", t):
            return False
        if re.fullmatch(r"(?i)(bacterial|mammalial|mammalian|gram\s*\+|gram\s*\-|g\+|g\-)", t):
            return False
        return True

    def guess_peptide_from_col_header(col_h: str) -> str:
        parts = [clean_peptide_id(p) for p in (col_h or "").split("|")]
        parts = [p for p in parts if p]
        for p in reversed(parts):
            if extract_endpoints_from_text(p) or is_derived_endpoint_label(p):
                continue
            if looks_like_peptide_label(p):
                return p
        return ""

    peptides_in_columns = False
    header_pep_hits = 0
    header_pep_total = 0
    for c in measurement_cols:
        col_h = col_headers[c] if c < len(col_headers) else ""
        cand = guess_peptide_from_col_header(col_h)
        header_pep_total += 1
        if cand:
            header_pep_hits += 1
    if header_pep_total and (header_pep_hits / header_pep_total) >= 0.6:
        peptides_in_columns = True

    # Fallback: unlabeled first column often holds peptide IDs (especially in MIC/MBC tables),
    # unless peptides clearly live in column headers.
    if peptide_col < 0 and not peptides_in_columns and n_cols and 0 not in measurement_cols and organism_col != 0 and seq_col != 0:
        sample = [normalize_whitespace(r[0]) for r in data_rows[:20] if r and normalize_whitespace(r[0])]
        if sample and sum(1 for x in sample if not looks_numeric_like(x)) / len(sample) >= 0.7:
            peptide_col = 0

    subject_col = organism_col if organism_col >= 0 else -1
    if peptides_in_columns:
        row_mode = False
        if subject_col < 0:
            if peptide_col >= 0:
                subject_col = peptide_col
            elif n_cols and 0 not in measurement_cols:
                subject_col = 0
    else:
        row_mode = False
        if peptide_col >= 0:
            for c in measurement_cols:
                if c in {peptide_col, seq_col}:
                    continue
                if extract_endpoints_from_text(col_headers[c]) or table_endpoints:
                    row_mode = True
                    break

    if not table_endpoints:
        if re.search(r"minimum\s+inhibitory\s+concentrations?", caption, flags=re.IGNORECASE):
            table_endpoints = ["MIC"]
        elif re.search(r"minimum\s+bactericidal\s+concentrations?", caption, flags=re.IGNORECASE):
            table_endpoints = ["MBC"]

    # Do not skip entire tables just because they contain derived metrics (e.g., SI/TI).
    # We skip derived *columns* later, and keep primary endpoints when present.

    if not measurement_cols or (not table_endpoints and not any(extract_endpoints_from_text(h) for h in col_headers)):
        qc["tables_skipped_no_endpoint"] += 1
        return [], qc

    qc["tables_parsed"] += 1

    records: list[dict] = []

    # Column-level condition row support (multi-row headers).
    # Pattern: last header row has a unit in col0, and numeric values in other columns.
    # Example:
    #   header_rows[-1][0] = "Peptides (μM)"
    #   header_rows[-1][c] = "2", "4", ...
    col_conditions: dict[int, str] = {}
    if header_rows and len(header_rows) >= 2:
        last_hdr = header_rows[-1]
        first = normalize_whitespace(last_hdr[0] if last_hdr else "")
        first_low = first.lower()
        conc_unit = parse_unit_from_text(first) if (re.search(r"\b(peptides?|concentration|dose|conc)\b", first_low) and first) else ""
        if conc_unit:
            for c in range(1, min(len(last_hdr), n_cols)):
                v = normalize_whitespace(last_hdr[c] if c < len(last_hdr) else "")
                if v and looks_numeric_like(v):
                    col_conditions[c] = f"{v} {conc_unit}"

    def is_group_row(row: list[str]) -> str:
        cells = [normalize_whitespace(x) for x in row if normalize_whitespace(x)]
        if len(cells) < 3:
            return ""
        # If most non-empty cells are identical (e.g., 'S. aureus' repeated), treat as a group header row.
        counts: dict[str, int] = {}
        for v in cells:
            counts[v] = counts.get(v, 0) + 1
        best = max(counts.items(), key=lambda kv: kv[1])[0]
        if (counts.get(best, 0) / len(cells)) >= 0.8 and not looks_numeric_like(best) and len(best) <= 40:
            return best
        return ""

    def guess_organism_from_col_header(col_h: str) -> str:
        parts = [normalize_whitespace(p) for p in (col_h or "").split("|")]
        for p in parts:
            if not p:
                continue
            if extract_endpoints_from_text(p) or is_derived_endpoint_label(p):
                continue
            # Skip pure unit fragments.
            if parse_unit_from_text(p):
                continue
            # Skip concentration tokens like "2" / "4" from multi-header concentration rows.
            if looks_numeric_like(p) or looks_numeric_value(p) or re.match(r"^[<>≤≥]\s*\d", p):
                continue
            return p
        return ""

    def source_ref_for_cell(row_idx_1b: int, col_idx_1b: int, *, row_label: str, col_label: str) -> str:
        bits: list[str] = []
        if label:
            bits.append(label)
        if table_id:
            bits.append(f"id={table_id}")
        bits.append(f"csv={csv_path.name}")
        if row_label:
            bits.append(f"row={row_label}")
        bits.append(f"row_idx={row_idx_1b}")
        if col_label:
            bits.append(f"col={col_label}")
        bits.append(f"col_idx={col_idx_1b}")
        return ";".join(bits)

    current_group = ""
    if header_rows:
        hdr_group = is_group_row(header_rows[-1])
        if hdr_group:
            current_group = hdr_group
    for ridx0, row in enumerate(data_rows, start=header_n + 1):
        group = is_group_row(row)
        if group:
            current_group = group
            continue

        organism = normalize_whitespace(row[organism_col]) if (organism_col >= 0 and organism_col < len(row)) else ""
        subject = normalize_whitespace(row[subject_col]) if (subject_col >= 0 and subject_col < len(row)) else ""
        peptide_id_row = normalize_whitespace(row[peptide_col]) if (row_mode and peptide_col >= 0 and peptide_col < len(row)) else ""
        seq_row_raw = normalize_whitespace(row[seq_col]) if (row_mode and seq_col >= 0 and seq_col < len(row)) else ""
        seq_row = standardize_aa_sequence(seq_row_raw)

        cond_parts: list[str] = []
        for c in range(n_cols):
            if c in measurement_cols:
                continue
            if c in {organism_col, peptide_col, seq_col, subject_col}:
                continue
            if c >= len(row):
                continue
            v = normalize_whitespace(row[c])
            if v:
                cond_parts.append(v)
        row_condition = " | ".join(cond_parts)

        for c in measurement_cols:
            if c in {organism_col, peptide_col, seq_col}:
                continue
            if c >= len(row):
                continue
            cell = normalize_whitespace(row[c])
            if not cell or cell.lower() in {"nd", "n.d.", "na", "n/a", "-", "—"}:
                continue

            col_h = col_headers[c] if c < len(col_headers) else f"col_{c+1}"
            if is_derived_endpoint_label(col_h):
                continue
            col_endpoints = extract_endpoints_from_text(col_h) or list(table_endpoints)
            if not col_endpoints:
                continue
            if any(is_derived_endpoint_label(ep) for ep in col_endpoints):
                continue

            unit = parse_unit_from_text(col_h) or table_unit or ""

            if row_mode:
                peptide_id = clean_peptide_id(peptide_id_row)
                sequence = seq_row or sequences.get(peptide_id, "")
            else:
                peptide_id = guess_peptide_from_col_header(col_h) or default_peptide_id
                sequence = sequences.get(peptide_id, "")

            organism_cell = organism or current_group
            if not row_mode and not organism_cell:
                organism_cell = subject
            if row_mode and not organism_cell and organism_col < 0:
                organism_cell = guess_organism_from_col_header(col_h)

            if ("MIC" in col_endpoints and "MBC" in col_endpoints) and "/" in cell:
                parts = [normalize_whitespace(x) for x in re.split(r"/", cell)]
                pairs = [("MIC", parts[0])] + ([("MBC", parts[1])] if len(parts) > 1 else [])
            else:
                pairs = [(col_endpoints[0], cell)]

            for ep, vtxt in pairs:
                value_fields = parse_value_fields(vtxt)
                if not value_fields.get("value_text"):
                    continue
                cond_final = " | ".join([x for x in [row_condition, col_conditions.get(c, "")] if x])
                records.append(
                    {
                        "peptide_id": peptide_id,
                        "sequence": sequence,
                        "endpoint": ep,
                        "value_text": value_fields["value_text"],
                        "value": value_fields["value"],
                        "cmp": value_fields.get("cmp") or "",
                        "error": value_fields.get("error") or "",
                        "range_low": value_fields.get("range_low"),
                        "range_high": value_fields.get("range_high"),
                        "unit": unit,
                        "organism_or_cell": organism_cell,
                        "condition": cond_final,
                        "conditions": cond_final,
                        "source": {
                            "kind": "xml_table",
                            "file": safe_rel(csv_path, docs_root),
                            "ref": source_ref_for_cell(
                                ridx0,
                                c + 1,
                                row_label=organism_cell or row_condition or peptide_id_row or f"row_{ridx0}",
                                col_label=col_h,
                            ),
                        },
                        "notes": normalize_whitespace(caption)[:300],
                    }
                )

    return records, qc


def extract_records_from_supp_pdf_text(
    *,
    pdf_text: str,
    source_file: str,
    sequences: dict[str, str],
) -> list[dict]:
    if not pdf_text.strip():
        return []
    lines = [normalize_whitespace(x) for x in pdf_text.splitlines()]
    lines = [x for x in lines if x]
    if not lines:
        return []

    records: list[dict] = []
    table_starts: list[int] = [i for i, ln in enumerate(lines) if re.match(r"^Table\s+\S+", ln, flags=re.IGNORECASE)]
    if not table_starts:
        table_starts = [0]
    table_starts.append(len(lines))

    for si in range(len(table_starts) - 1):
        start = table_starts[si]
        end = table_starts[si + 1]
        block = lines[start:end]
        if not block:
            continue
        table_heading = block[0] if re.match(r"^Table\s+\S+", block[0], flags=re.IGNORECASE) else ""

        organism = ""
        heading_join = " ".join(block[:3])
        m_org = re.search(r"\b(in|against)\s+([A-Za-z][A-Za-z0-9. _-]{1,40})\b", heading_join, flags=re.IGNORECASE)
        if m_org:
            organism = normalize_whitespace(m_org.group(2))

        for i, ln in enumerate(block):
            eps = extract_endpoints_from_text(ln)
            if not eps:
                continue
            ep = eps[0]
            unit = parse_unit_from_text(ln) or ""
            descriptor = block[i - 1] if i - 1 >= 0 else ""

            for n in range(1, 7):
                if i + 1 + n >= len(block):
                    break
                peptides = block[i + 1 : i + 1 + n]
                j = i + 1 + n
                if j + n >= len(block):
                    continue
                cond = block[j]
                vals = block[j + 1 : j + 1 + n]
                if not cond or not all(re.match(r"^[<>≤≥]?[0-9]+(\\.[0-9]+)?$", v) for v in vals):
                    continue

                row_idx = 0
                jj = j
                while jj + 1 + n <= len(block):
                    cond2 = block[jj]
                    vals2 = block[jj + 1 : jj + 1 + n]
                    if not cond2 or not all(re.match(r"^[<>≤≥]?[0-9]+(\\.[0-9]+)?$", v) for v in vals2):
                        break
                    for pep, vtxt in zip(peptides, vals2, strict=False):
                        peptide_id = clean_peptide_id(pep)
                        value_fields = parse_value_fields(vtxt)
                        records.append(
                            {
                                "peptide_id": peptide_id,
                                "sequence": sequences.get(peptide_id, ""),
                                "endpoint": ep,
                                "value_text": value_fields["value_text"],
                                "value": value_fields["value"],
                                "error": value_fields.get("error") or "",
                                "range_low": value_fields.get("range_low"),
                                "range_high": value_fields.get("range_high"),
                                "unit": unit,
                                "organism_or_cell": organism,
                                "condition": f"{descriptor}: {cond2}" if descriptor else cond2,
                                "conditions": f"{descriptor}: {cond2}" if descriptor else cond2,
                                "source": {
                                    "kind": "supplementary",
                                    "file": source_file,
                                    "ref": ";".join(
                                        [
                                            table_heading or "Supplementary PDF",
                                            f"endpoint_line={ln}",
                                            f"row={cond2}",
                                            f"col={peptide_id}",
                                            f"row_idx={row_idx+1}",
                                        ]
                                    ),
                                },
                                "notes": "",
                            }
                        )
                    row_idx += 1
                    jj += 1 + n
                break

    return records


def extract_records_from_supplementary(
    supp_dir: Path,
    *,
    sequences: dict[str, str],
    docs_root: Path,
) -> tuple[list[dict], dict]:
    qc: dict = {"supp_files_parsed": 0, "supp_files_skipped": 0}
    if not supp_dir.exists() or not supp_dir.is_dir():
        return [], qc

    records: list[dict] = []
    files = [p for p in supp_dir.rglob("*") if p.is_file()]
    for p in sorted(files, key=lambda x: str(x).lower()):
        ext = p.suffix.lower()
        try:
            if ext == ".zip":
                with zipfile.ZipFile(p, "r") as zf:
                    for name in zf.namelist():
                        data = zf.read(name)
                        if name.lower().endswith(".pdf") and fitz is not None:
                            doc = fitz.open(stream=data, filetype="pdf")
                            text = "\n".join(doc.load_page(i).get_text("text") for i in range(doc.page_count))
                            source_file = safe_rel(p, docs_root)
                            recs = extract_records_from_supp_pdf_text(pdf_text=text, source_file=source_file, sequences=sequences)
                            if recs:
                                for r in recs:
                                    r["source"]["ref"] = f"inner={name};" + str(r["source"]["ref"])
                                records.extend(recs)
                                qc["supp_files_parsed"] += 1
                            else:
                                qc["supp_files_skipped"] += 1
                        else:
                            qc["supp_files_skipped"] += 1
                continue

            if ext == ".pdf" and fitz is not None:
                doc = fitz.open(p)
                text = "\n".join(doc.load_page(i).get_text("text") for i in range(doc.page_count))
                source_file = safe_rel(p, docs_root)
                recs = extract_records_from_supp_pdf_text(pdf_text=text, source_file=source_file, sequences=sequences)
                if recs:
                    records.extend(recs)
                    qc["supp_files_parsed"] += 1
                else:
                    qc["supp_files_skipped"] += 1
                continue

            if ext in {".xlsx", ".xls"} and pd is not None:
                qc["supp_files_skipped"] += 1
                continue

            qc["supp_files_skipped"] += 1
        except Exception:
            qc["supp_files_skipped"] += 1
            continue

    return records, qc


def build_local_result(*, papers_dir: Path, paper_id: str, docs_root: Path) -> dict:
    """
    Local-only fallback: build a per-paper JSON result from existing pipeline outputs
    (raw_experimental_records.csv + extracted_tables + supplementary listing).
    """
    raw_path = papers_dir / "raw_experimental_records.csv"
    records: list[dict] = []
    citation: dict = {"pmcid": paper_id}
    excluded_derived = 0

    xml_path = papers_dir / f"{paper_id}.xml"
    citation_xml = parse_jats_citation(xml_path)
    if citation_xml:
        for k, v in citation_xml.items():
            if v:
                citation[k] = v

    table_meta = parse_jats_table_meta(xml_path) if xml_path.exists() else {}

    tables_list = sorted((papers_dir / "extracted_tables").glob(f"{paper_id}_*.csv"))
    supp_dir = papers_dir / "supplementary" / paper_id
    supp_files = sorted([p for p in supp_dir.rglob("*") if p.is_file()], key=lambda p: str(p).lower()) if supp_dir.exists() else []
    supp_files_count = len(supp_files)

    seq_map_from_tables, seq_sources_tables = extract_sequences_from_extracted_tables(tables_list, docs_root=docs_root)
    known_peptide_ids = sorted(seq_map_from_tables.keys(), key=lambda s: s.lower())
    seq_map: dict[str, str] = dict(seq_map_from_tables)

    def guess_default_peptide_id_from_title(title: str) -> str:
        t = normalize_whitespace(title)
        if not t:
            return ""
        # Prefer explicit "peptide X" patterns.
        m = re.search(r"(?i)\bpeptide\s+([A-Za-z][A-Za-z0-9-]{1,40})\b", t)
        if m:
            return m.group(1)
        # Fallback: common peptide naming like "Dadapin-1", "LL-37", etc.
        m = re.search(r"\b([A-Za-z]{2,}[A-Za-z0-9]*-\d{1,3})\b", t)
        if m:
            return m.group(1)
        return ""

    default_peptide_id = known_peptide_ids[0] if len(known_peptide_ids) == 1 else ""
    if not default_peptide_id and not known_peptide_ids and citation.get("title"):
        default_peptide_id = guess_default_peptide_id_from_title(str(citation.get("title") or ""))

    # 1) From pipeline joined experimental records (already auditable)
    if raw_path.exists():
        with raw_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pmcid = (row.get("pmcid") or "").strip()
                stem = (row.get("paper_stem") or "").strip()
                if pmcid != paper_id and stem != paper_id:
                    continue

                endpoint = (row.get("endpoint") or "").strip()
                if is_derived_endpoint_label(endpoint):
                    excluded_derived += 1
                    continue

                peptide_id = (row.get("peptide_id") or "").strip()
                seq = standardize_aa_sequence((row.get("sequence") or "").strip()) or seq_map.get(peptide_id, "")
                unit = (row.get("unit") or "").strip()

                value = (row.get("value") or "").strip()
                cmp_ = (row.get("cmp") or "").strip()
                err = (row.get("error") or "").strip()
                snippet = (row.get("snippet") or "").strip()
                value_text = snippet or (f"{cmp_}{value}" + (f" ± {err}" if err else ""))

                source_path = (row.get("source_path") or "").strip()
                source_file = safe_rel(Path(source_path), docs_root) if source_path else safe_rel(xml_path, docs_root)

                records.append(
                    {
                        "peptide_id": peptide_id,
                        "sequence": seq,
                        "endpoint": endpoint,
                        "value_text": value_text,
                        "value": float(value) if value and value.replace(".", "", 1).isdigit() else None,
                        "cmp": cmp_,
                        "error": err,
                        "range_low": float(row["range_low"]) if (row.get("range_low") or "").strip().replace(".", "", 1).isdigit() else None,
                        "range_high": float(row["range_high"]) if (row.get("range_high") or "").strip().replace(".", "", 1).isdigit() else None,
                        "unit": unit,
                        "organism_or_cell": (row.get("condition") or "").strip(),
                        "condition": (row.get("condition") or "").strip(),
                        "conditions": (row.get("conditions") or "").strip(),
                        "source": {
                            "kind": (row.get("source_kind") or "").strip() or "other",
                            "ref": (row.get("source_ref") or "").strip(),
                            "file": source_file,
                        },
                        "notes": (row.get("context") or "").strip(),
                    }
                )

    # 2) Parse extracted_tables CSVs to recover missed endpoints
    table_qc_agg: dict = {"tables_parsed": 0, "tables_skipped_derived": 0, "tables_skipped_no_endpoint": 0}
    for t in tables_list:
        recs, tqc = extract_records_from_extracted_table(
            t,
            table_meta=table_meta,
            sequences=seq_map,
            default_peptide_id=default_peptide_id,
            docs_root=docs_root,
        )
        for k in table_qc_agg:
            table_qc_agg[k] += int(tqc.get(k) or 0)
        records.extend(recs)

    # 3) Best-effort supplementary PDF parsing (incl. PDFs inside zips)
    supp_records, supp_qc = extract_records_from_supplementary(supp_dir, sequences=seq_map, docs_root=docs_root)
    records.extend(supp_records)

    # De-dup by key including source pointer
    deduped: list[dict] = []
    seen: set[tuple] = set()
    for r in records:
        src = r.get("source") or {}
        key = (
            r.get("endpoint") or "",
            r.get("peptide_id") or "",
            r.get("sequence") or "",
            r.get("value_text") or "",
            r.get("unit") or "",
            r.get("organism_or_cell") or "",
            r.get("condition") or "",
            src.get("file") or "",
            src.get("ref") or "",
        )
        if key in seen:
            continue
        seen.add(key)
        if not (src.get("file") or ""):
            src["file"] = safe_rel(xml_path, docs_root) if xml_path.exists() else ""
            r["source"] = src
        deduped.append(r)
    records = deduped

    # Fill peptide sequences from XML text when tables didn't include them.
    if xml_path.exists():
        seen_peptide_ids = sorted({(r.get("peptide_id") or "").strip() for r in records if (r.get("peptide_id") or "").strip()}, key=str.lower)
        missing_seq_peptide_ids = [pid for pid in seen_peptide_ids if pid and pid not in seq_map]
        seq_map_from_text, seq_sources_text = extract_sequences_from_xml_text(xml_path, missing_seq_peptide_ids, docs_root=docs_root)
        for k, v in seq_map_from_text.items():
            if v and k not in seq_map:
                seq_map[k] = v
        for r in records:
            if (r.get("sequence") or "").strip():
                continue
            pid = (r.get("peptide_id") or "").strip()
            if pid and pid in seq_map:
                r["sequence"] = seq_map[pid]
    else:
        seq_sources_text = []

    missing_unit = sum(1 for r in records if not (r.get("unit") or "").strip())
    missing_sequence = sum(1 for r in records if not (r.get("sequence") or "").strip())

    coverage = {
        "mode": "local",
        "records_total": len(records),
        "extracted_tables_count": len(tables_list),
        "supp_files_count": supp_files_count,
        "tables": [safe_rel(p, docs_root) for p in tables_list],
        "supp_files": [safe_rel(p, docs_root) for p in supp_files],
        "sequence_sources": seq_sources_tables + seq_sources_text,
        "notes": "Offline local extraction from extracted_tables CSVs + XML text (sequence mapping) + best-effort supplementary PDF parsing; all records include source.kind/ref/file.",
    }
    qc = {
        "missing_unit_rows": missing_unit,
        "missing_sequence_rows": missing_sequence,
        "excluded_derived_endpoint_rows": excluded_derived,
        "tables_qc": table_qc_agg,
        "supp_qc": supp_qc,
    }

    # Simple markdown
    endpoint_counts: dict[str, int] = {}
    seqs: set[str] = set()
    for r in records:
        endpoint_counts[r.get("endpoint") or "(missing)"] = endpoint_counts.get(r.get("endpoint") or "(missing)", 0) + 1
        if r.get("sequence"):
            seqs.add(r["sequence"])
    endpoint_counts = dict(sorted(endpoint_counts.items(), key=lambda kv: (-kv[1], kv[0])))

    md_lines: list[str] = []
    md_lines.append(f"- paper_id: {paper_id}")
    if citation.get("doi"):
        md_lines.append(f"- doi: {citation.get('doi')}")
    md_lines.append(f"- records: {len(records)}")
    md_lines.append(f"- unique_sequences: {len(seqs)}")
    md_lines.append(f"- extracted_tables: {len(tables_list)}")
    md_lines.append(f"- supplementary_files: {supp_files_count}")
    if endpoint_counts:
        md_lines.append("\n**Endpoints**")
        for k, v in list(endpoint_counts.items())[:25]:
            md_lines.append(f"- {k}: {v}")
    if tables_list:
        md_lines.append("\n**Tables Scanned**")
        for p in tables_list[:25]:
            md_lines.append(f"- {safe_rel(p, docs_root)}")
        if len(tables_list) > 25:
            md_lines.append(f"- ... ({len(tables_list) - 25} more)")
    if supp_files:
        md_lines.append("\n**Supplementary Files**")
        for p in supp_files[:25]:
            md_lines.append(f"- {safe_rel(p, docs_root)}")
        if len(supp_files) > 25:
            md_lines.append(f"- ... ({len(supp_files) - 25} more)")
    if records:
        md_lines.append("\n**Sample Records**")
        for r in records[:10]:
            md_lines.append(
                f"- {r.get('peptide_id','')} | {r.get('endpoint','')} | {r.get('value_text','')} {r.get('unit','')} | {r.get('sequence','')[:30]}"
            )
    md_lines.append("\n**QC**")
    md_lines.append(f"- missing_unit_rows: {missing_unit}")
    md_lines.append(f"- missing_sequence_rows: {missing_sequence}")
    md_lines.append(f"- excluded_derived_endpoint_rows: {excluded_derived}")
    md_lines.append(
        f"- tables_parsed: {table_qc_agg.get('tables_parsed', 0)} (skipped_derived={table_qc_agg.get('tables_skipped_derived', 0)}, skipped_no_endpoint={table_qc_agg.get('tables_skipped_no_endpoint', 0)})"
    )
    md_lines.append(f"- supp_files_parsed: {supp_qc.get('supp_files_parsed', 0)} (skipped={supp_qc.get('supp_files_skipped', 0)})")
    if not records:
        md_lines.append("- note: no extractable endpoint rows found in scanned tables/supp (may be figures-only or non-endpoint tables).")

    return {
        "paper_id": paper_id,
        "citation": citation,
        "records": records,
        "coverage": coverage,
        "qc": qc,
        "markdown": "\n".join(md_lines).strip() + "\n",
    }


def claim_task(queue_dir: Path) -> Path | None:
    pending = queue_dir / "pending"
    in_progress = queue_dir / "in_progress"
    in_progress.mkdir(parents=True, exist_ok=True)

    for src in sorted(pending.glob("*.json")):
        dst = in_progress / src.name
        try:
            # Some distributed filesystems may refuse cross-directory rename() with EXDEV.
            # To keep de-duplication safe across multiple workers, we use an atomic
            # claim marker, then fall back to shutil.move() (copy+unlink if needed).
            claim = in_progress / (src.name + ".claim")
            try:
                with claim.open("x", encoding="utf-8") as f:
                    f.write(f"{now_iso()} {os.getpid()}\n")
            except FileExistsError:
                continue

            try:
                shutil.move(str(src), str(dst))
            except Exception:
                try:
                    claim.unlink(missing_ok=True)
                except Exception:
                    pass
                continue

            try:
                claim.unlink(missing_ok=True)
            except Exception:
                pass
            return dst
        except Exception:
            continue
    return None


def safe_move(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        src.replace(dst)
        return
    except OSError as e:
        if getattr(e, "errno", None) == 18:  # EXDEV
            shutil.move(str(src), str(dst))
            return
        raise


def run_codex_exec(
    *,
    docs_root: Path,
    prompt_text: str,
    schema_path: Path,
    out_json_path: Path,
    log_path: Path,
    model: str,
    sandbox_mode: str,
    codex_home: Path | None,
    timeout_seconds: float | None,
) -> int:
    cmd = [
        "codex",
        "-a",
        "never",
        "exec",
        "--skip-git-repo-check",
        "-C",
        str(docs_root),
        "--sandbox",
        sandbox_mode,
        "--output-schema",
        str(schema_path),
        "-o",
        str(out_json_path),
    ]
    if model:
        cmd.extend(["-m", model])
    cmd.append("-")  # read prompt from stdin

    env = os.environ.copy()
    if codex_home is not None:
        env["CODEX_HOME"] = str(codex_home)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab") as log_f:
        log_f.write(f"\n\n===== {now_iso()} RUN =====\n".encode("utf-8"))
        log_f.write(("CMD: " + " ".join(cmd) + "\n").encode("utf-8"))
        try:
            proc = subprocess.run(
                cmd,
                input=prompt_text.encode("utf-8"),
                stdout=log_f,
                stderr=log_f,
                env=env,
                check=False,
                timeout=timeout_seconds,
            )
            log_f.write(f"\nEXIT_CODE: {proc.returncode}\n".encode("utf-8"))
            return int(proc.returncode)
        except subprocess.TimeoutExpired:
            log_f.write(f"\nEXIT_CODE: timeout_after_seconds={timeout_seconds}\n".encode("utf-8"))
            return 124


def strip_json_code_fences(text: str) -> str:
    """
    Codex outputs should be pure JSON (because we pass --output-schema), but in practice
    models occasionally wrap the JSON in markdown fences like:
      ```json
      {...}
      ```
    This helper strips a single outer code-fence block if present.
    """
    s = (text or "").strip()
    if not s.startswith("```"):
        return s
    lines = s.splitlines()
    if not lines:
        return s
    if not lines[0].lstrip().startswith("```"):
        return s
    # Drop opening fence line (``` or ```json)
    lines = lines[1:]
    # Drop trailing closing fence line if present
    while lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis-dir", type=str, default="analysis", help="Analysis root directory")
    ap.add_argument("--worker-name", type=str, default="", help="Worker name for logging/attribution")
    ap.add_argument("--poll-seconds", type=float, default=2.0, help="Sleep when no tasks are available")
    ap.add_argument("--max-tasks", type=int, default=0, help="Stop after N tasks (0 = infinite)")
    ap.add_argument("--model", type=str, default="", help="Optional Codex model override (e.g., o3, gpt-5)")
    ap.add_argument("--sandbox", type=str, default="read-only", help="Codex sandbox mode (read-only/workspace-write/danger-full-access)")
    ap.add_argument("--preview-tables", type=int, default=5, help="How many extracted_tables/*.csv files to preview in the prompt")
    ap.add_argument("--preview-supp-files", type=int, default=6, help="How many supplementary files to preview in the prompt")
    ap.add_argument("--preview-lines", type=int, default=18, help="How many lines to preview per text/CSV file")
    ap.add_argument(
        "--codex-home",
        type=str,
        default="",
        help="Optional CODEX_HOME override (must be writable). If unset, uses $CODEX_HOME or <analysis-dir>/_codex_home.",
    )
    ap.add_argument(
        "--prompt-template",
        type=str,
        default="analysis/prompts/per_paper_prompt.txt",
        help="Prompt template path (Template placeholders).",
    )
    ap.add_argument(
        "--schema",
        type=str,
        default="analysis/schemas/per_paper_output.schema.json",
        help="Output JSON schema path (for codex exec --output-schema).",
    )
    ap.add_argument(
        "--mode",
        type=str,
        default="codex",
        choices=["codex", "local"],
        help="Processing mode: codex (LLM proofreading) or local (no-network fallback from existing CSV outputs).",
    )
    ap.add_argument(
        "--codex-timeout-seconds",
        type=float,
        default=1800.0,
        help="Hard timeout for each `codex exec` call; prevents stuck runs (0/negative disables).",
    )
    args = ap.parse_args()

    docs_root = Path.cwd().resolve()
    analysis_dir = Path(args.analysis_dir).resolve()
    queue_dir = analysis_dir / "queue"
    prompt_path = Path(args.prompt_template).resolve()
    schema_path = Path(args.schema).resolve()

    for sub in ("pending", "in_progress", "done", "failed"):
        (queue_dir / sub).mkdir(parents=True, exist_ok=True)
    (analysis_dir / "per_paper").mkdir(parents=True, exist_ok=True)
    (analysis_dir / "logs").mkdir(parents=True, exist_ok=True)

    worker_name = args.worker_name.strip() or f"worker-{os.getpid()}"
    prompt_template = Template(prompt_path.read_text(encoding="utf-8"))

    codex_home: Path | None = None
    if str(args.codex_home or "").strip():
        codex_home = Path(str(args.codex_home)).expanduser().resolve()
    elif os.environ.get("CODEX_HOME"):
        codex_home = Path(os.environ["CODEX_HOME"]).expanduser().resolve()

    tasks_attempted = 0
    while True:
        if args.max_tasks and tasks_attempted >= int(args.max_tasks):
            print(f"[ok] reached --max-tasks={args.max_tasks}; exiting")
            return 0

        task_path = claim_task(queue_dir)
        if task_path is None:
            time.sleep(float(args.poll_seconds))
            continue

        started = time.time()
        try:
            task = json.loads(task_path.read_text(encoding="utf-8"))
        except Exception as e:
            failed_path = queue_dir / "failed" / task_path.name
            safe_move(task_path, failed_path)
            atomic_write_text(analysis_dir / "logs" / f"bad_task_{task_path.name}.log", f"Failed to parse task JSON: {e}\n")
            tasks_attempted += 1
            continue

        paper_id = str(task.get("paper_id") or "").strip() or task_path.stem
        papers_dir = Path(str(task.get("run_papers_dir") or "")).resolve()

        task["status"] = "in_progress"
        task["started_at"] = now_iso()
        task["worker"] = worker_name
        atomic_write_json(task_path, task)

        materials = task.get("materials") or {}
        xml_path = Path(str(materials.get("xml_path") or "")).resolve() if materials.get("xml_path") else Path()
        pdf_path = Path(str(materials.get("pdf_path") or "")).resolve() if materials.get("pdf_path") else Path()
        supp_dir = Path(str(materials.get("supp_dir") or "")).resolve() if materials.get("supp_dir") else Path()
        oa_pkg = Path(str(materials.get("oa_package_path") or "")).resolve() if materials.get("oa_package_path") else Path()

        # Build per-paper context blocks
        supp_files = list_files_block(supp_dir, max_files=200, base=docs_root)
        tables = list_extracted_tables_block(papers_dir, paper_id, max_tables=200, base=docs_root)
        table_previews = build_csv_table_previews_block(
            papers_dir=papers_dir,
            paper_id=paper_id,
            docs_root=docs_root,
            max_tables=max(0, int(args.preview_tables)),
            max_lines=max(1, int(args.preview_lines)),
        )
        supp_previews = build_supp_previews_block(
            supp_dir=supp_dir,
            docs_root=docs_root,
            max_files=max(0, int(args.preview_supp_files)),
        )
        summary = summarize_raw_records(papers_dir, paper_id, max_sample_rows=40)
        records_summary = format_records_summary_block(summary)

        prompt_text = prompt_template.safe_substitute(
            paper_id=paper_id,
            xml_path=safe_rel(xml_path, docs_root) if xml_path and xml_path.exists() else "(missing)",
            pdf_path=safe_rel(pdf_path, docs_root) if pdf_path and pdf_path.exists() else "(missing)",
            supp_dir=safe_rel(supp_dir, docs_root) if supp_dir and supp_dir.exists() else "(missing)",
            oa_package_path=safe_rel(oa_pkg, docs_root) if oa_pkg and oa_pkg.exists() else "(missing)",
            supp_files=supp_files,
            tables=tables,
            table_previews=table_previews,
            supp_previews=supp_previews,
            records_summary=records_summary,
        )

        prompt_dump = analysis_dir / "logs" / f"{paper_id}.prompt.txt"
        atomic_write_text(prompt_dump, prompt_text)

        tmp_out = analysis_dir / "logs" / f"{paper_id}.codex_output.json"
        log_path = analysis_dir / "logs" / f"{paper_id}.codex_exec.log"

        rc = 0
        if args.mode == "codex":
            timeout_seconds = float(getattr(args, "codex_timeout_seconds", 0.0))
            if timeout_seconds <= 0:
                timeout_seconds = None
            rc = run_codex_exec(
                docs_root=docs_root,
                prompt_text=prompt_text,
                schema_path=schema_path,
                out_json_path=tmp_out,
                log_path=log_path,
                model=str(args.model or "").strip(),
                sandbox_mode=str(args.sandbox or "read-only"),
                codex_home=codex_home,
                timeout_seconds=timeout_seconds,
            )

        elapsed = time.time() - started

        outputs = task.get("outputs") or {}
        per_paper_json = Path(str(outputs.get("per_paper_json") or (analysis_dir / "per_paper" / f"{paper_id}.json"))).resolve()
        per_paper_md = Path(str(outputs.get("per_paper_md") or (analysis_dir / "per_paper" / f"{paper_id}.md"))).resolve()

        if args.mode == "local":
            result = build_local_result(papers_dir=papers_dir, paper_id=paper_id, docs_root=docs_root)
        else:
            if rc != 0 or not tmp_out.exists() or not tmp_out.read_text(encoding="utf-8", errors="ignore").strip():
                task["status"] = "failed"
                task["finished_at"] = now_iso()
                task["elapsed_seconds"] = round(elapsed, 3)
                task["error"] = f"codex exec failed (rc={rc}); see log: {safe_rel(log_path, docs_root)}"
                atomic_write_json(task_path, task)
                failed_path = queue_dir / "failed" / task_path.name
                safe_move(task_path, failed_path)
                tasks_attempted += 1
                continue

            try:
                raw = tmp_out.read_text(encoding="utf-8", errors="ignore")
                result = json.loads(strip_json_code_fences(raw))
            except Exception as e:
                task["status"] = "failed"
                task["finished_at"] = now_iso()
                task["elapsed_seconds"] = round(elapsed, 3)
                task["error"] = f"failed to parse codex output json: {e}"
                atomic_write_json(task_path, task)
                failed_path = queue_dir / "failed" / task_path.name
                safe_move(task_path, failed_path)
                tasks_attempted += 1
                continue

        # Ensure paper_id is present/consistent
        if not isinstance(result, dict):
            result = {"paper_id": paper_id, "records": [], "coverage": {}, "qc": {}, "markdown": str(result)}
        result["paper_id"] = str(result.get("paper_id") or paper_id)

        atomic_write_json(per_paper_json, result)
        md_text = str(result.get("markdown") or "").strip() + "\n"
        atomic_write_text(per_paper_md, md_text)

        task["status"] = "done"
        task["finished_at"] = now_iso()
        task["elapsed_seconds"] = round(elapsed, 3)
        task["outputs_written"] = {"json": str(per_paper_json), "md": str(per_paper_md)}
        atomic_write_json(task_path, task)

        done_path = queue_dir / "done" / task_path.name
        safe_move(task_path, done_path)
        tasks_attempted += 1


if __name__ == "__main__":
    raise SystemExit(main())
