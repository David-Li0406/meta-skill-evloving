#!/usr/bin/env python3
"""
Extract *raw, traceable* structured information from downloaded OA papers.

Input: a directory produced by fetch_open_access_papers.py, e.g.
  papers_oa_test5/
    download_manifest.jsonl
    <stem>.xml
    <stem>.pdf
    supplementary/<stem>/*

Output:
  - raw_extractions.csv: one row per extracted entity with DOI/PMID/PMCID and source pointers
  - extracted_tables/: reconstructed tables saved as CSV for audit/review

This is intentionally heuristic and "raw": it aims to be high-recall and auditable,
not perfect. Every row contains a source pointer (table id / file name / page).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import tarfile
import tempfile
import zipfile
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

import pandas as pd

try:
    import fitz  # PyMuPDF
except Exception:  # pragma: no cover
    fitz = None  # type: ignore

import xml.etree.ElementTree as ET


AA_ALLOWED = "ACDEFGHIKLMNPQRSTVWYBXZJUO"  # include common ambiguous residues
AA_ALLOWED_SET = set(AA_ALLOWED)

SEQUENCE_MIN_LEN_DEFAULT = 12
SEQUENCE_MIN_LEN_LOOSE = 5

# Common English/ML terms that are composed only of AA letters and can be false positives.
SEQUENCE_STOPWORDS = {
    "SPECIFICITY",
    "SENSITIVITY",
    "PRECISION",
    "RECALL",
    "ACCURACY",
    "VALIDATION",
    "INDEPENDENT",
    "DEPENDENT",
    "CROSS",
    "TRAIN",
    "TRAINING",
    "TEST",
    "TESTING",
    "PREDICT",
    "PREDICTION",
    "CLASSIFIER",
    "CLASSIFICATION",
    "REGRESSION",
    "FEATURE",
    "FEATURES",
    "SEQUENCE",
    "SEQUENCES",
}

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
)

THRESHOLD_KEYWORDS = (
    "threshold",
    "cutoff",
    "cut-off",
    "cut off",
    "labelled as",
    "labeled as",
    "toxic if",
    "non-toxic if",
)


def is_threshold_sentence(sentence: str) -> bool:
    s = normalize_whitespace(sentence).lower()
    if not s:
        return False
    has_digit = any(ch.isdigit() for ch in s)

    if "toxic if" in s or "non-toxic if" in s:
        return True

    if "threshold" in s or "cutoff" in s or "cut-off" in s or "cut off" in s:
        # Usually thresholds are numeric (e.g., 0.8/0.9, E-value 0.001).
        return has_digit

    if "labelled as" in s or "labeled as" in s:
        # Keep label rules that are likely about toxicity / class labels.
        return ("toxic" in s) or ("non-toxic" in s) or ("positive" in s) or ("negative" in s)

    return False


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_stem(text: str, max_len: int = 120) -> str:
    s = text.strip()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[^\w.\-]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = "paper"
    return s[:max_len]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def clip_text(text: Any, *, max_len: int) -> str:
    s = normalize_whitespace("" if text is None else str(text))
    if max_len > 0 and len(s) > max_len:
        return s[:max_len] + "...<truncated>"
    return s


class ClippingDictWriter(csv.DictWriter):
    def __init__(self, *args: Any, max_field_len: int = 2000, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._max_field_len = max_field_len

    def writerow(self, rowdict: dict[str, Any]) -> int:
        row = dict(rowdict)
        for k in ("entity", "snippet", "context"):
            if k in row:
                row[k] = clip_text(row.get(k, ""), max_len=self._max_field_len)
        return super().writerow(row)


def elem_text(elem: Optional[ET.Element]) -> str:
    if elem is None:
        return ""
    return normalize_whitespace("".join(elem.itertext()))


def split_sentences(text: str) -> list[str]:
    t = normalize_whitespace(text)
    if not t:
        return []
    # Rough sentence splitter; keep it simple to avoid heavy deps.
    parts = re.split(r"(?<=[.!?])\s+", t)
    return [p.strip() for p in parts if p.strip()]


def extract_aa_tokens(text: str) -> list[str]:
    # Uppercase, replace non-allowed letters with space, then split.
    up = (text or "").upper()
    cleaned = re.sub(rf"[^{AA_ALLOWED}]+", " ", up)
    tokens = [t for t in cleaned.split() if t]
    return tokens


def looks_like_aa_sequence(token: str, *, min_len: int) -> bool:
    if len(token) < min_len:
        return False
    if token in SEQUENCE_STOPWORDS:
        return False
    if any(ch not in AA_ALLOWED_SET for ch in token):
        return False
    # Avoid pathological low-entropy strings (e.g., AAAAAAAAAA)
    unique = set(token)
    if len(token) >= 10 and len(unique) <= 2:
        return False
    return True


def find_sequences(text: str, *, min_len: int) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for tok in extract_aa_tokens(text):
        if not looks_like_aa_sequence(tok, min_len=min_len):
            continue
        if tok not in seen:
            seen.add(tok)
            out.append(tok)
    return out


def canonical_sequence_from_cell(text: str, *, min_len: int) -> str:
    """
    Extract a single canonical AA sequence from a cell that is *supposed* to contain a sequence.
    This is stricter/cleaner than find_sequences():
    - removes common markers like '*' (e.g., allo-Ile markers)
    - removes inline style artifacts like 'color=...>' seen in some XML conversions
    - tries to drop common terminal modification suffixes like '-NH2'
    """
    s = normalize_whitespace(text or "")
    if not s:
        return ""

    # Handle hyphen-separated 3-letter residue codes (e.g., "Cys-Gly-Phe" -> "CGF").
    # This is common in short oligopeptide tables where sequences are not given as
    # 1-letter AA strings.
    three_letter = {
        "ala": "A",
        "arg": "R",
        "asn": "N",
        "asp": "D",
        "cys": "C",
        "gln": "Q",
        "glu": "E",
        "gly": "G",
        "his": "H",
        "ile": "I",
        "leu": "L",
        "lys": "K",
        "met": "M",
        "phe": "F",
        "pro": "P",
        "ser": "S",
        "thr": "T",
        "trp": "W",
        "tyr": "Y",
        "val": "V",
        # Ambiguous / uncommon but useful.
        "asx": "B",
        "glx": "Z",
        "sec": "U",
        "pyl": "O",
        "xle": "J",
        "unk": "X",
    }
    token_src = normalize_whitespace(text or "")
    if "-" in token_src or "–" in token_src or "—" in token_src:
        token_src = token_src.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
        parts = [p for p in re.split(r"[-/]+", token_src) if normalize_whitespace(p)]
        mapped: list[str] = []
        for p in parts:
            p2 = normalize_whitespace(p)
            p2 = re.sub(r"\([^)]*\)", "", p2).strip()
            p2 = re.sub(r"[^A-Za-z]+", "", p2)
            if not p2:
                mapped = []
                break
            low = p2.casefold()
            # Support "D-Ala"/"L-Ala" style tokens.
            if len(low) == 4 and low[0] in {"d", "l"} and low[1:] in three_letter:
                low = low[1:]
            if low not in three_letter:
                mapped = []
                break
            mapped.append(three_letter[low])
        if mapped:
            seq3 = "".join(mapped)
            if len(seq3) >= max(1, int(min_len)):
                return seq3

    # Remove common artifacts/markers (keep raw in sequence_raw separately).
    s = s.replace("*", "")
    s = re.sub(r"color\s*=\s*[^>]*>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"style\s*=\s*[^>]*>", "", s, flags=re.IGNORECASE)

    s = re.sub(r"\(\s*orn\s*\)", "K", s, flags=re.IGNORECASE)
    s = re.sub(r"\(\s*dab\s*\)", "K", s, flags=re.IGNORECASE)
    s = re.sub(r"\(\s*dap\s*\)", "K", s, flags=re.IGNORECASE)
    s = re.sub(r"[εϵ]\s*K", "K", s, flags=re.IGNORECASE)

    # Drop a few very common terminal modification suffixes.
    s = re.sub(r"[-–—]\s*NH\s*2\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[-–—]?\s*CONH\s*2\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[-–—]\s*COOH\b", "", s, flags=re.IGNORECASE)
    s = re.sub(r"[-–—]\s*OH\b", "", s, flags=re.IGNORECASE)

    s = re.sub(r"[\(\)\[\]\{\}]", "", s)

    # Within-sequence separators (spaces, hyphens) are usually formatting; remove to re-join.
    s = re.sub(r"[\s‐‑–—_\\-]+", "", s)

    candidates: list[str] = []
    for m in re.finditer(r"[A-Za-z]{%d,}" % max(1, int(min_len)), s):
        tok = m.group(0)
        if all(ch.upper() in AA_ALLOWED_SET for ch in tok):
            candidates.append(tok.upper())

    if not candidates:
        # Fall back to the generic tokenizer.
        seqs = find_sequences(s, min_len=min_len)
        if not seqs:
            return ""
        return max(seqs, key=len)

    return max(candidates, key=len)


_NUM_RE = r"(?:\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?)"
_RANGE_RE = rf"(?P<range_lo>{_NUM_RE})\s*(?:-|–|—|to)\s*(?P<range_hi>{_NUM_RE})"
_VAL_RE = rf"(?P<single_val>{_NUM_RE})"
_PLUSMINUS_RE = rf"(?P<pm_val>{_NUM_RE})\s*±\s*(?P<pm_err>{_NUM_RE})"

_UNITS = (
    r"μM|µM|uM|nM|mM|pM|fM|"
    r"mg/kg|mg·kg-1|mg kg-1|"
    r"μg/mL|µg/mL|ug/mL|ng/mL|mg/mL|"
    r"g/L|mg/L|μg/L|µg/L|ug/L|"
    r"%"
)

UNIT_RE = re.compile(rf"(?<![A-Za-z])(?:{_UNITS})(?![A-Za-z])", flags=re.IGNORECASE)

# Ratio-like headers often indicate *derived indices* (e.g., SI = CC50/IC50), not measured endpoints.
_RATIO_HEADER_RE = re.compile(
    rf"\b(?P<a>{'|'.join(re.escape(k) for k in ENDPOINT_KEYWORDS)})\b\s*/\s*\b(?P<b>{'|'.join(re.escape(k) for k in ENDPOINT_KEYWORDS)})\b",
    flags=re.IGNORECASE,
)

# Common "MIC (MBC)" cell form used in antimicrobial peptide tables: "4 (8)" etc.
MIC_MBC_PAIR_RE = re.compile(
    rf"(?P<mic_cmp>[<>≤≥~]?)\s*(?P<mic_val>{_NUM_RE})\s*\(\s*(?P<mbc_cmp>[<>≤≥~]?)\s*(?P<mbc_val>{_NUM_RE})\s*\)",
    flags=re.IGNORECASE,
)

MIC_MBC_SLASH_RE = re.compile(
    rf"(?P<mic_cmp>[<>≤≥~]?)\s*(?P<mic_val>{_NUM_RE})\s*/\s*(?P<mbc_cmp>[<>≤≥~]?)\s*(?P<mbc_val>{_NUM_RE})",
    flags=re.IGNORECASE,
)

MEAS_RE = re.compile(
    rf"(?P<prefix>{'|'.join(ENDPOINT_KEYWORDS)})?\s*"
    rf"(?P<cmp>[<>≤≥~]?)\s*"
    rf"(?:(?:{_PLUSMINUS_RE})|(?:{_RANGE_RE})|(?:{_VAL_RE}))\s*"
    rf"(?P<unit>(?:{_UNITS}))?",
    flags=re.IGNORECASE,
)


def _to_float(s: Optional[str]) -> Optional[float]:
    if s is None:
        return None
    try:
        return float(s)
    except Exception:
        return None


def find_measurements(text: str, *, hint_prefix: str = "", hint_unit: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    src = text or ""
    for m in MEAS_RE.finditer(src):
        # Avoid matching digits embedded in an alphanumeric token, e.g. "AapA1" -> "1".
        if m.start() > 0 and src[m.start() - 1].isalnum():
            continue
        if m.end() < len(src) and src[m.end()].isalnum():
            continue
        raw = m.group(0).strip()
        if not raw:
            continue
        prefix = (m.group("prefix") or "").upper()
        cmp_ = m.group("cmp") or ""
        unit = m.group("unit") or ""
        if not prefix and hint_prefix:
            prefix = hint_prefix.upper()
        if not unit and hint_unit:
            unit = hint_unit
        # Filter out obvious false positives: a naked "1" with no unit/prefix is rarely useful.
        has_context = bool(prefix) or bool(unit)
        if not has_context:
            continue

        lo = _to_float(m.groupdict().get("range_lo"))
        hi = _to_float(m.groupdict().get("range_hi"))
        # NOTE: do not use `or` here; 0.0 is a valid value and is falsy in Python.
        val = _to_float(m.groupdict().get("single_val"))
        if val is None:
            val = _to_float(m.groupdict().get("pm_val"))
        err = _to_float(m.groupdict().get("pm_err"))
        out.append(
            {
                "raw": raw,
                "prefix": prefix,
                "cmp": cmp_,
                "value": val,
                "error": err,
                "range_low": lo,
                "range_high": hi,
                "unit": unit,
            }
        )
    return out


def _is_hemolysis_header(text: str) -> bool:
    """
    Header-level detection for hemolysis-like readouts.

    We support both explicit "hemolysis/hemolytic" and common synonyms used in
    experimental tables (e.g., "erythrocyte lysis").
    """
    s = normalize_whitespace(text or "")
    if not s:
        return False
    low = s.casefold()
    if "hemolysis" in low or "hemolytic" in low:
        return True
    # Common synonyms / variants.
    if "erythrocyte" in low and "lysis" in low:
        return True
    if re.search(r"\brbc\b", low) and "lysis" in low:
        return True
    return False


def _split_hemolysis_percent_vs_dose(
    measurements: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], str]:
    """
    For a hemolysis-% cell like: "37.00 (200 µM or 577.34 µg/mL)",
    `find_measurements()` can return multiple matches. We keep the % value as
    the endpoint, and return the remaining matches as a "dose_info" string.
    """
    if not measurements:
        return [], ""
    pct: list[dict[str, Any]] = []
    other: list[dict[str, Any]] = []
    for m in measurements:
        unit = str(m.get("unit") or "").strip()
        if unit == "%":
            pct.append(m)
        else:
            other.append(m)
    dose_info = "; ".join([str(m.get("raw") or "").strip() for m in other if str(m.get("raw") or "").strip()])
    return (pct or measurements), dose_info


def find_conditions(text: str) -> list[str]:
    t = text or ""
    out: list[str] = []
    patterns = (
        r"\bpH\s*\d+(?:\.\d+)?\b",
        r"\b\d+(?:\.\d+)?\s*(?:°C|C|K)\b",
        r"\b\d+(?:\.\d+)?\s*(?:h|hr|hrs|hour|hours|min|mins|minute|minutes|s|sec|secs|second|seconds)\b",
        # Common cell lines / assay systems (best-effort; intentionally conservative).
        r"\bHEK\s*293T?\b",
        r"\bHCT\s*\d+\b",
        r"\bA\s*\d{3,4}\b",
        r"\bMCF-?\s*7\b",
        r"\bRAW\s*264\.?7\b",
        r"\bCaco-?\s*2\b",
        r"\bHepG2\b|\bHeLa\b|\bVero\b|\bCHO\b",
    )
    seen: set[str] = set()
    for pat in patterns:
        for m in re.finditer(pat, t, flags=re.IGNORECASE):
            s = m.group(0).strip()
            if s and s not in seen:
                seen.add(s)
                out.append(s)
    return out


def uniq_preserve_order(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for x in items:
        if not x:
            continue
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def header_endpoint_hint(header: str) -> tuple[str, str]:
    h = normalize_whitespace(header or "")
    h_low = h.casefold()

    # Exclude index/ratio columns like "SI (CC50/IC50)" or "CC50/IC50" (except MIC/MBC which is often a paired endpoint).
    if re.search(r"\b(selectivity|therapeutic)\s*index\b", h_low) or re.search(r"\b(?:si|ti)\b", h_low):
        return "", ""
    m = _RATIO_HEADER_RE.search(h)
    if m:
        a = (m.group("a") or "").upper()
        b = (m.group("b") or "").upper()
        if {a, b} != {"MIC", "MBC"}:
            return "", ""

    prefix = ""
    for kw in ENDPOINT_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", h, flags=re.IGNORECASE):
            prefix = kw
            break
    unit = ""
    # Use letter-boundaries to avoid false positives like "Number" -> "uM" or "OPM" -> "pM".
    um = UNIT_RE.search(h)
    if um:
        unit = um.group(0)
    return prefix, unit


def table_level_endpoint_hint(*, caption: str, foot: str = "", label: str = "") -> tuple[str, str]:
    # Infer endpoint/unit from caption/footnote when headers only contain conditions (e.g., organisms).
    return header_endpoint_hint(normalize_whitespace(f"{label} {caption} {foot}"))


def normalize_peptide_id(text: str) -> str:
    """
    Normalize a peptide identifier for cross-table joining.
    - Remove parenthetical length like '(40)'
    - Unicode-aware: keeps Greek letters etc (\\w)
    """
    s = normalize_whitespace(text or "")
    if not s:
        return ""
    s = re.sub(r"\([^)]*\)", "", s)  # drop (..)
    # Normalize common hyphen variants.
    s = s.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    s = s.casefold()
    s = re.sub(r"\W+", "", s, flags=re.UNICODE)
    return s


def guess_id_column(headers: list[str]) -> Optional[int]:
    # Prefer explicit "peptide name" then other identifier-like headers.
    candidates: list[tuple[int, int]] = []  # (score, idx)
    for i, h in enumerate(headers):
        hh = normalize_whitespace(h or "")
        if not hh:
            continue
        if re.search(r"\b(seq|sequence|sequences)\b", hh, flags=re.IGNORECASE):
            continue
        score = 0
        if re.search(r"\bno\.", hh, flags=re.IGNORECASE) or re.fullmatch(r"(?:#|index)", hh.strip(), flags=re.IGNORECASE):
            score = 35
        if re.search(r"\bpeptide\s*name\b", hh, flags=re.IGNORECASE):
            score = 50
        elif re.search(r"\bpeptide\b", hh, flags=re.IGNORECASE):
            score = 40
        elif re.search(r"\bacronym\b", hh, flags=re.IGNORECASE):
            score = 40
        elif re.search(r"\bmastoparan\b", hh, flags=re.IGNORECASE):
            score = 40
        elif re.search(r"\bpeptaibol(?:s)?\b", hh, flags=re.IGNORECASE):
            score = 35
        elif re.search(r"\banalog(?:s)?\b", hh, flags=re.IGNORECASE):
            score = 30
        elif re.search(r"\bsample\b", hh, flags=re.IGNORECASE):
            score = 30
        elif re.search(r"\bagents?\b", hh, flags=re.IGNORECASE):
            score = 35
        elif re.search(r"\btreatments?\b", hh, flags=re.IGNORECASE):
            score = 35
        elif re.search(r"\bvariant(?:s)?\b", hh, flags=re.IGNORECASE) or re.search(r"\bvariation\b", hh, flags=re.IGNORECASE):
            score = 25
        elif re.search(r"\babbrev", hh, flags=re.IGNORECASE):
            score = 25
        elif re.search(r"\bcompound\b", hh, flags=re.IGNORECASE):
            score = 30
        elif re.search(r"\bprotein\b", hh, flags=re.IGNORECASE):
            score = 20
        elif re.search(r"\bname\b", hh, flags=re.IGNORECASE):
            score = 20
        elif re.search(r"\bid\b", hh, flags=re.IGNORECASE):
            score = 10
        if score:
            candidates.append((score, i))
    if candidates:
        return sorted(candidates, reverse=True)[0][1]
    return None


def guess_sequence_column(headers: list[str]) -> Optional[int]:
    for i, h in enumerate(headers):
        hh = normalize_whitespace(h or "")
        if not hh:
            continue
        if re.search(r"\b(seq|sequence|sequences)\b", hh, flags=re.IGNORECASE):
            return i
        if re.search(r"\bamino\s*acid\b", hh, flags=re.IGNORECASE) and re.search(r"\bsequence\b", hh, flags=re.IGNORECASE):
            return i
    return None


def guess_sequence_column_by_content(
    headers: list[str],
    rows: list[list[str]],
    *,
    header_row_idx: int,
    max_rows: int = 200,
) -> Optional[int]:
    """
    Some sequence tables label the sequence column as just 'Peptide'/'Variant' and the cells
    contain the AA sequence directly. Fall back to content-based detection.
    """
    if not rows or len(rows) < 2:
        return None

    data_rows = rows[header_row_idx + 1 : header_row_idx + 1 + max_rows]
    if not data_rows:
        return None

    width = max(len(r) for r in rows)
    best_idx: Optional[int] = None
    best_score = 0

    for c_idx in range(width):
        seq_cnt = 0
        uniq: set[str] = set()
        for r in data_rows:
            if c_idx >= len(r):
                continue
            seq = canonical_sequence_from_cell(r[c_idx], min_len=SEQUENCE_MIN_LEN_LOOSE)
            if not seq:
                continue
            seq_cnt += 1
            uniq.add(seq)
        if seq_cnt < 2 or len(uniq) < 2:
            continue

        # Light header preference: 'peptide' increases confidence.
        h = normalize_whitespace(headers[c_idx] if c_idx < len(headers) else "")
        bonus = 2 if re.search(r"\bpeptide\b", h, flags=re.IGNORECASE) else 0
        score = seq_cnt + bonus
        if score > best_score:
            best_score = score
            best_idx = c_idx

    return best_idx


def guess_alias_id_columns(headers: list[str], *, primary_id_idx: int, seq_idx: int) -> list[int]:
    """
    Identify additional identifier columns in a sequence table, such as "Abbreviation/Number",
    so that cross-table joining can work when other tables use the short IDs.
    """
    out: list[int] = []
    for i, h in enumerate(headers):
        if i == seq_idx or i == primary_id_idx:
            continue
        hh = normalize_whitespace(h or "")
        if not hh:
            continue
        low = hh.casefold()
        if re.search(r"\b(molecular|weight|mass|length|charge|hydrophobic|purity|yield|rt|mz|ppm|adduct)\b", low):
            continue
        if re.search(r"\b(abbrev|abbreviation)\b", low):
            out.append(i)
            continue
        if re.search(r"\b(number|no\\.|no|index|code|identifier|id)\\b", low):
            out.append(i)
            continue
    return out


def guess_parameter_column(headers: list[str]) -> Optional[int]:
    """
    Best-effort guess of a column that carries per-row endpoint labels, e.g.:
      - Parameter: MIC/MBC/IC50...
      - Endpoint: CC50/IC50...

    This is used to override a weak table-level endpoint hint (from caption/footnote)
    when numeric columns only contain units (e.g. "µM") and the endpoint is stored
    as a row attribute ("Parameter" column).
    """
    candidates: list[tuple[int, int]] = []  # (score, idx)
    for i, h in enumerate(headers):
        hh = normalize_whitespace(h or "")
        if not hh:
            continue
        score = 0
        if re.search(r"\bparameter\b", hh, flags=re.IGNORECASE):
            score = 50
        elif re.search(r"\bendpoint\b", hh, flags=re.IGNORECASE):
            score = 45
        elif re.search(r"\breadout\b", hh, flags=re.IGNORECASE):
            score = 35
        elif re.search(r"\bassay\b", hh, flags=re.IGNORECASE):
            score = 25
        if score:
            candidates.append((score, i))
    if candidates:
        return sorted(candidates, reverse=True)[0][1]
    return None


def endpoint_override_from_cell(text: str) -> str:
    """
    Extract an endpoint keyword from a per-row label cell, e.g. "MIC", "MBC", "IC50".
    Returns "" when no known endpoint keyword is present.
    """
    s = normalize_whitespace(text or "")
    if not s:
        return ""
    low = s.lower()
    if "hemolysis" in low or "hemolytic" in low:
        return "HEMOLYSIS"
    for kw in ENDPOINT_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", s, flags=re.IGNORECASE):
            return kw
    return ""


def choose_header_row_index(rows: list[list[str]], *, max_candidates: int = 4) -> int:
    """
    Pick the most likely header row index in a (possibly multi-header) table.

    Many publisher XML tables use a super-header row (endpoint/unit) above the actual column names.
    """
    if not rows:
        return 0
    n = min(len(rows), max(1, int(max_candidates)))
    best_idx = 0
    best_score = -10_000
    for i in range(n):
        r = rows[i]
        nonempty = [normalize_whitespace(x) for x in r if normalize_whitespace(x)]
        uniq = len({x.casefold() for x in nonempty})
        score = 0
        if guess_id_column(r) is not None:
            score += 30
        if guess_sequence_column(r) is not None:
            score += 20
        if any(header_endpoint_hint(x)[0] for x in r):
            score += 10
        score += min(20, len(nonempty))
        # Penalize repeated super-headers (e.g., all cells identical).
        if nonempty and uniq <= max(1, len(nonempty) // 4):
            score -= 25
        if score > best_score:
            best_score = score
            best_idx = i
    return best_idx


def combined_headers(rows: list[list[str]], header_row_idx: int) -> list[str]:
    if not rows:
        return []
    h = max(0, min(int(header_row_idx), len(rows) - 1))
    width = len(rows[h])
    # Detect "concentration header rows" like: ["Peptides (µM)", "2", "4", ...]
    # and annotate numeric headers with the concentration unit to keep them auditable.
    conc_unit = ""
    conc_numeric_cols: set[int] = set()
    if h >= 1:
        last_hdr = rows[h]
        first = normalize_whitespace(last_hdr[0] if last_hdr else "")
        first_low = first.casefold()
        if first and re.search(r"\b(peptides?|concentration|dose|conc)\b", first_low):
            um = UNIT_RE.search(first)
            if um:
                conc_unit = um.group(0)
        if conc_unit:
            for c in range(1, len(last_hdr)):
                v = normalize_whitespace(last_hdr[c] if c < len(last_hdr) else "")
                if v and re.fullmatch(r"[<>≤≥~]?\s*\d+(?:\.\d+)?", v):
                    conc_numeric_cols.add(c)
    out: list[str] = []
    for c in range(width):
        parts: list[str] = []
        for r in rows[: h + 1]:
            txt = normalize_whitespace(r[c] if c < len(r) else "")
            if conc_unit and (r is rows[h]) and (c in conc_numeric_cols) and txt and not UNIT_RE.search(txt):
                txt = f"{txt} {conc_unit}"
            if txt:
                parts.append(txt)
        out.append(" ".join(uniq_preserve_order(parts)))
    return out


def is_count_like_header(header: str) -> bool:
    h = normalize_whitespace(header or "").casefold()
    if not h:
        return False
    h2 = re.sub(r"\W+", "", h)
    return h2 in {"n", "no", "num", "number", "count", "replicates", "replicate"}


def is_derived_index_header(header: str) -> bool:
    h = normalize_whitespace(header or "").casefold()
    if not h:
        return False
    if re.search(r"\b(selectivity|therapeutic)\s*index\b", h):
        return True
    if re.search(r"\b(?:si|ti)\b", h):
        return True
    return False


def is_non_endpoint_property_header(header: str) -> bool:
    h = normalize_whitespace(header or "").casefold()
    if not h:
        return False
    # Common physchem/property columns that should never be treated as endpoint readouts.
    if re.search(r"\b(mol(?:\.|\s*)?wt|molecular\s+weight|mw)\b", h):
        return True
    if re.search(r"\b(mass|m\/z|mz|ppm|adduct)\b", h):
        return True
    if re.search(r"\b(length|residues?|aa\s*length)\b", h):
        return True
    if re.search(r"\b(net\s+charge|charge|hydrophobicity|hydrophobi(?:c|city))\b", h):
        return True
    if re.search(r"\b(isoelectric|pI|pi)\b", h):
        return True
    if re.search(r"\b(purity|yield|retention\s*time|rt)\b", h):
        return True
    return False


def column_has_numeric_signal(
    data_rows: list[list[str]],
    col_idx: int,
    *,
    hint_prefix: str,
    hint_unit: str,
    max_scan_rows: int = 200,
) -> bool:
    for r in data_rows[: min(len(data_rows), int(max_scan_rows))]:
        if col_idx >= len(r):
            continue
        cell = r[col_idx] or ""
        if not normalize_whitespace(cell):
            continue
        if MIC_MBC_PAIR_RE.search(cell) or MIC_MBC_SLASH_RE.search(cell):
            return True
        if find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit):
            return True
    return False


def jats_article_title(root: ET.Element) -> str:
    # Try common JATS paths.
    for path in (
        ".//{*}title-group/{*}article-title",
        ".//{*}article-title",
    ):
        el = root.find(path)
        if el is not None:
            title = elem_text(el)
            if title:
                return title
    return ""


def jats_ids(root: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    for el in root.findall(".//{*}article-id"):
        typ = (el.attrib.get("pub-id-type") or "").lower().strip()
        val = elem_text(el).strip()
        if not typ or not val:
            continue
        if typ == "doi":
            out["doi"] = val
        elif typ == "pmid":
            out["pmid"] = val
        elif typ == "pmcid":
            out["pmcid"] = "PMC" + val if val.isdigit() else (val if val.upper().startswith("PMC") else val)
    return out


def iter_jats_tables(root: ET.Element) -> Iterable[dict[str, Any]]:
    for idx, tw in enumerate(root.findall(".//{*}table-wrap")):
        table_id = tw.attrib.get("id") or f"tablewrap_{idx+1}"
        label = elem_text(tw.find("./{*}label"))
        caption = elem_text(tw.find("./{*}caption"))
        foot = elem_text(tw.find("./{*}table-wrap-foot"))
        table_el = tw.find(".//{*}table")
        yield {"id": table_id, "label": label, "caption": caption, "foot": foot, "elem": table_el}


def table_elem_to_matrix(table_el: ET.Element) -> list[list[str]]:
    """
    Convert a JATS <table> element to a rectangular matrix of strings.
    Expands rowspan/colspan by repeating the cell text into the spanned slots.
    """
    raw_rows: list[list[str]] = []
    rowspans: dict[int, tuple[str, int]] = {}  # col_idx -> (text, remaining_rows)

    for tr in table_el.findall(".//{*}tr"):
        row: list[str] = []
        col = 0

        def fill_from_rowspans() -> None:
            nonlocal col
            while col in rowspans:
                txt, remaining = rowspans[col]
                row.append(txt)
                remaining -= 1
                if remaining <= 0:
                    del rowspans[col]
                else:
                    rowspans[col] = (txt, remaining)
                col += 1

        fill_from_rowspans()

        cells = [c for c in list(tr) if isinstance(c.tag, str) and c.tag.lower().endswith(("td", "th"))]
        for cell in cells:
            fill_from_rowspans()
            txt = elem_text(cell)
            try:
                rowspan = int(cell.attrib.get("rowspan") or "1")
            except Exception:
                rowspan = 1
            try:
                colspan = int(cell.attrib.get("colspan") or "1")
            except Exception:
                colspan = 1
            rowspan = max(1, rowspan)
            colspan = max(1, colspan)

            for i in range(colspan):
                row.append(txt)
                if rowspan > 1:
                    rowspans[col + i] = (txt, rowspan - 1)
            col += colspan

        fill_from_rowspans()
        if any(normalize_whitespace(x) for x in row):
            raw_rows.append(row)

    if not raw_rows:
        return []
    width = max(len(r) for r in raw_rows)
    return [r + [""] * (width - len(r)) for r in raw_rows]


@dataclass
class ParsedTable:
    table_id: str
    label: str
    caption: str
    foot: str
    rows: list[list[str]]


def extract_sequence_map_from_tables(tables: list[ParsedTable]) -> dict[str, dict[str, str]]:
    """
    Build a mapping from normalized peptide id -> sequence information using any table that
    has both an id-like column and a sequence-like column.
    """
    def looks_like_nonstandard_sequence_definition(text: str) -> bool:
        """
        Some papers report sequences with non-canonical residues or chemistry tokens (e.g., Aib/Toac/Phol/Ac-...).
        We keep the raw string for audit and allow downstream joins, even if AA-only `sequence` is empty.
        """
        s = normalize_whitespace(text or "")
        if not s:
            return False
        low = s.casefold()
        # Common chemistry / non-canonical residue markers seen in peptide tables.
        if any(tok in low for tok in ("aib", "toac", "phol", "acetyl", "ac-", "nh2", "conh2", "amid", "amido")):
            return True
        # Many such definitions are hyphen-separated token chains.
        if "-" in s and len(s.split("-")) >= 4:
            return True
        return False

    seq_map: dict[str, dict[str, str]] = {}
    for t in tables:
        if not t.rows or len(t.rows) < 2:
            continue
        header_row_idx = choose_header_row_index(t.rows)
        headers = combined_headers(t.rows, header_row_idx)
        id_idx = guess_id_column(headers)
        seq_idx = guess_sequence_column(headers)
        if seq_idx is None:
            seq_idx = guess_sequence_column_by_content(headers, t.rows, header_row_idx=header_row_idx)
        if id_idx is None or seq_idx is None:
            continue
        alias_id_idxs = guess_alias_id_columns(headers, primary_id_idx=id_idx, seq_idx=seq_idx)
        id_idxs = [id_idx, *alias_id_idxs]

        seq_min_len = SEQUENCE_MIN_LEN_LOOSE
        seq_header = normalize_whitespace(headers[seq_idx] if 0 <= seq_idx < len(headers) else "")
        if re.search(r"\b(amino\s*acid|sequence|sequences)\b", seq_header, flags=re.IGNORECASE):
            # In explicit sequence columns, allow short oligopeptides (di-/tri-peptides).
            seq_min_len = 2

        for r_idx, row in enumerate(t.rows[header_row_idx + 1 :], start=header_row_idx + 1):
            if seq_idx >= len(row):
                continue
            seq_cell = normalize_whitespace(row[seq_idx])
            if not seq_cell:
                continue
            seq = canonical_sequence_from_cell(seq_cell, min_len=seq_min_len)
            if not seq and not looks_like_nonstandard_sequence_definition(seq_cell):
                continue
            for ii in id_idxs:
                if ii >= len(row):
                    continue
                peptide_id = normalize_whitespace(row[ii])
                if not peptide_id:
                    continue
                norm_id = normalize_peptide_id(peptide_id)
                if not norm_id:
                    continue
                cur = seq_map.get(norm_id)
                cur_seq = str((cur or {}).get("sequence") or "")
                # Prefer entries with a longer AA-only sequence; otherwise keep the first raw definition.
                if (cur is None) or (len(seq) > len(cur_seq)):
                    seq_map[norm_id] = {
                        "peptide_id": peptide_id,
                        "sequence": seq,
                        "sequence_raw": seq_cell,
                        "sequence_is_standardized": bool(seq),
                        "sequence_source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={seq_idx};header_row_idx={header_row_idx}",
                        "sequence_table_id": t.table_id,
                    }

    # Fallback: extract inline "ID (SEQUENCE ...)" definitions from any table cell/caption.
    # This recovers papers where sequences appear inside a descriptive row/caption rather
    # than a dedicated "Sequence" column (e.g., "TRP1-TINF (GPSGFLGNR – 903 Da)").
    inline_re = re.compile(
        r"(?P<pep>[A-Za-z][A-Za-z0-9._-]{1,80})\s*\(\s*(?P<body>[^)]{3,240})\)",
        flags=re.IGNORECASE,
    )
    for t in tables:
        candidates: list[str] = [t.label, t.caption, t.foot]
        for r in t.rows[: min(len(t.rows), 80)]:
            for c in r[: min(len(r), 30)]:
                candidates.append(str(c or ""))
        for txt in candidates:
            s = normalize_whitespace(txt)
            if not s:
                continue
            for m in inline_re.finditer(s):
                pep = normalize_whitespace(m.group("pep") or "")
                body = normalize_whitespace(m.group("body") or "")
                if not pep or not body:
                    continue
                if pep.casefold() in {"table", "figure"}:
                    continue
                seq = canonical_sequence_from_cell(body, min_len=2)
                if not seq:
                    continue
                norm_id = normalize_peptide_id(pep)
                if not norm_id:
                    continue
                cur = seq_map.get(norm_id)
                cur_seq = str((cur or {}).get("sequence") or "")
                if (cur is None) or (len(seq) > len(cur_seq)):
                    seq_map[norm_id] = {
                        "peptide_id": pep,
                        "sequence": seq,
                        "sequence_raw": body,
                        "sequence_is_standardized": bool(seq),
                        "sequence_source_ref": f"inline_definition;table_id={t.table_id}",
                        "sequence_table_id": t.table_id,
                    }
    return seq_map


def pick_endpoint_columns(
    headers: list[str],
    data_rows: list[list[str]],
    *,
    table_prefix: str,
    table_unit: str,
    id_idx: int,
) -> list[dict[str, Any]]:
    if not headers:
        return []
    cols: list[dict[str, Any]] = []
    explicit_cols: list[dict[str, Any]] = []

    def is_prediction_like_header(header: str) -> bool:
        h = normalize_whitespace(header or "").casefold()
        if not h:
            return False
        if re.search(r"\b(pred|predict|prediction|predicted|in\s*silico|computed|computational|model)\b", h):
            return True
        # Common derived columns in mixed experimental/prediction tables.
        if "pred-exp" in h or "exp-pred" in h:
            return True
        if "Δ" in (header or ""):
            return True
        return False

    for c_idx, h in enumerate(headers):
        if c_idx == id_idx:
            continue
        if is_prediction_like_header(h):
            continue
        prefix, unit = header_endpoint_hint(h)
        if not prefix:
            continue
        if not unit and table_unit:
            unit = table_unit
        cond = normalize_whitespace(h)
        cond = re.sub(rf"\b{re.escape(prefix)}\b", " ", cond, flags=re.IGNORECASE)
        if unit:
            cond = re.sub(re.escape(unit), " ", cond, flags=re.IGNORECASE)
        for kw in ENDPOINT_KEYWORDS:
            cond = re.sub(rf"\b{re.escape(kw)}\b", " ", cond, flags=re.IGNORECASE)
        cond = cond.replace("[", " ").replace("]", " ").replace("(", " ").replace(")", " ")
        cond = normalize_whitespace(cond)
        # Drop common footnote-only tokens ("a", "b", "*") to avoid polluting condition.
        if re.fullmatch(r"[a-z]\*?", cond, flags=re.IGNORECASE):
            cond = ""
        explicit_cols.append({"col": c_idx, "prefix": prefix, "unit": unit, "condition": cond})

    for c_idx, h in enumerate(headers):
        if c_idx == id_idx:
            continue
        h_norm = normalize_whitespace(h)
        if not h_norm:
            continue
        if is_prediction_like_header(h_norm):
            continue
        if _is_hemolysis_header(h_norm):
            cond = h_norm
            # Prefer to keep only the concentration/assay context as `condition`.
            cond_low = cond.casefold()
            cond = re.sub(r"\bhemolysis\b", " ", cond, flags=re.IGNORECASE)
            cond = re.sub(r"\bhemolytic\b", " ", cond, flags=re.IGNORECASE)
            if "erythrocyte" in cond_low and "lysis" in cond_low:
                cond = re.sub(r"\bery(?:thro)?cyte\b", " ", cond, flags=re.IGNORECASE)
                cond = re.sub(r"\blysis\b", " ", cond, flags=re.IGNORECASE)
            cond = re.sub(r"%", " ", cond)
            cond = normalize_whitespace(cond)
            explicit_cols.append({"col": c_idx, "prefix": "HEMOLYSIS", "unit": "%", "condition": cond})

    cols.extend(explicit_cols)

    if table_prefix:
        for c_idx, h in enumerate(headers):
            if c_idx == id_idx:
                continue
            if is_prediction_like_header(h):
                continue
            if is_count_like_header(h) or is_derived_index_header(h) or is_non_endpoint_property_header(h):
                continue
            if re.search(r"\b(seq|sequence|sequences)\b", h or "", flags=re.IGNORECASE):
                continue
            if any(int(ec.get("col") or -1) == c_idx for ec in explicit_cols):
                continue
            header_prefix, header_unit = header_endpoint_hint(h)
            hint_prefix = header_prefix or table_prefix
            hint_unit = header_unit or table_unit
            if not hint_prefix:
                continue
            if not column_has_numeric_signal(data_rows, c_idx, hint_prefix=hint_prefix, hint_unit=hint_unit):
                continue
            cols.append({"col": c_idx, "prefix": hint_prefix, "unit": hint_unit, "condition": normalize_whitespace(h)})

    if not cols:
        return []

    seen: set[tuple[int, str]] = set()
    out: list[dict[str, Any]] = []
    for c in cols:
        key = (int(c.get("col") or -1), str(c.get("prefix") or ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)

    # Drop duplicate columns caused by multi-level header / colspan expansion:
    # if two columns share the same normalized header AND have identical values across rows,
    # keep only the first to avoid duplicate records.
    def norm_header(i: int) -> str:
        return normalize_whitespace(headers[i] if 0 <= i < len(headers) else "").casefold()

    def col_values(i: int, *, max_rows: int = 50) -> list[str]:
        vals: list[str] = []
        for r in data_rows[: min(len(data_rows), int(max_rows))]:
            vals.append(normalize_whitespace(r[i] if i < len(r) else ""))
        return vals

    kept: list[dict[str, Any]] = []
    seen_groups: dict[tuple[str, str, str], tuple[int, list[str]]] = {}
    for c in out:
        ci = int(c.get("col") or -1)
        if ci < 0:
            continue
        hkey = norm_header(ci)
        gkey = (hkey, str(c.get("prefix") or ""), str(c.get("unit") or ""))
        if not hkey:
            kept.append(c)
            continue
        vals = col_values(ci)
        prev = seen_groups.get(gkey)
        if prev is None:
            seen_groups[gkey] = (ci, vals)
            kept.append(c)
            continue
        _prev_i, prev_vals = prev
        if vals == prev_vals:
            continue
        kept.append(c)
    return kept


def endpoint_keywords_in_text(text: str) -> set[str]:
    s = normalize_whitespace(text or "")
    if not s:
        return set()
    found: set[str] = set()
    for kw in ENDPOINT_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", s, flags=re.IGNORECASE):
            found.add(kw)
    return found


def best_id_column_by_seqmap(
    headers: list[str],
    data_rows: list[list[str]],
    seq_map: dict[str, dict[str, str]],
    *,
    max_scan_rows: int = 200,
) -> tuple[Optional[int], int]:
    if not headers or not data_rows or not seq_map:
        return None, 0
    best_idx: Optional[int] = None
    best_cnt = 0
    width = len(headers)
    for c_idx in range(width):
        cnt = 0
        for r in data_rows[: min(len(data_rows), int(max_scan_rows))]:
            if c_idx >= len(r):
                continue
            val = normalize_whitespace(r[c_idx])
            if not val:
                continue
            if normalize_peptide_id(val) in seq_map:
                cnt += 1
                if cnt >= 6:
                    break
        if cnt > best_cnt:
            best_cnt = cnt
            best_idx = c_idx
    return (best_idx, best_cnt) if (best_idx is not None and best_cnt >= 2) else (None, best_cnt)


def detect_transposed_peptide_header(
    rows: list[list[str]],
    seq_map: dict[str, dict[str, str]],
    *,
    max_header_rows: int = 4,
) -> tuple[Optional[int], dict[int, dict[str, Any]]]:
    if not rows or not seq_map:
        return None, {}
    n = min(len(rows), max(1, int(max_header_rows)))
    best_row: Optional[int] = None
    best_cnt = 0
    best_cols: dict[int, dict[str, Any]] = {}
    for r_idx in range(n):
        r = rows[r_idx]
        cols: dict[int, dict[str, Any]] = {}
        for c_idx, cell in enumerate(r):
            cell_txt = normalize_whitespace(cell)
            if not cell_txt:
                continue
            norm = normalize_peptide_id(cell_txt)
            if norm in seq_map:
                cols[c_idx] = {"peptide_id": cell_txt, "norm_id": norm, "seq_info": seq_map[norm]}
        if len(cols) > best_cnt:
            best_cnt = len(cols)
            best_row = r_idx
            best_cols = cols
    if best_row is None:
        return None, {}
    if best_cnt >= 2:
        return best_row, best_cols
    if best_cnt == 1:
        only = next(iter(best_cols.values()))
        pid = normalize_whitespace(str(only.get("peptide_id") or ""))
        # Allow single-hit transposed detection only for "real" peptide IDs (e.g., GW18),
        # to avoid triggering on trivial numeric IDs ("1") that appear in many tables.
        if len(pid) >= 3 and re.search(r"[A-Za-z]", pid):
            return best_row, best_cols
    return None, {}


def detect_transposed_endpoint_header(
    rows: list[list[str]],
    peptide_cols: dict[int, dict[str, Any]],
    *,
    max_header_rows: int = 4,
) -> Optional[int]:
    if not rows or not peptide_cols:
        return None
    n = min(len(rows), max(1, int(max_header_rows)))
    best_row: Optional[int] = None
    best_score = -1
    for r_idx in range(n):
        r = rows[r_idx]
        score = 0
        for c_idx in peptide_cols.keys():
            if c_idx >= len(r):
                continue
            prefix, unit = header_endpoint_hint(r[c_idx] or "")
            if prefix:
                score += 2
            elif unit:
                score += 1
        if score > best_score:
            best_score = score
            best_row = r_idx
    return best_row


def should_skip_transposed_condition(text: str) -> bool:
    s = normalize_whitespace(text or "").casefold()
    if not s:
        return True
    if "confidence interval" in s or "interval" in s:
        return True
    if "therapeutic index" in s:
        return True
    if "geometric mean" in s:
        return True
    if re.fullmatch(r"(?:ti|si)\*?", s):
        return True
    return False


def is_transposed_derived_section_start(text: str) -> bool:
    """
    Identify transposed-table *section headers* that start a derived/summary block
    (e.g., "Therapeutic index (TI)" or "Geometric mean ...").

    This is intentionally narrower than should_skip_transposed_condition(): we do NOT
    want "95% confidence interval" rows to start a skip-section state.
    """
    s = normalize_whitespace(text or "").casefold()
    if not s:
        return False
    if "geometric mean" in s:
        return True
    if "therapeutic index" in s or "selectivity index" in s:
        return True
    if re.fullmatch(r"(?:ti|si)\*?", s):
        return True
    return False


def transposed_section_start_label(row: list[str], *, primary_label: str, peptide_col_idxs: list[int]) -> str:
    """
    Detect a derived/summary section header row in a transposed table.

    Example:
      Therapeutic index (TI), Therapeutic index (TI), Therapeutic index (TI) ...
    """
    label = normalize_whitespace(primary_label or "")
    if not label:
        # Fallback: use the first non-empty peptide cell as label.
        for c in peptide_col_idxs:
            if c < len(row):
                txt = normalize_whitespace(row[c])
                if txt:
                    label = txt
                    break
    if not label:
        return ""
    if not is_transposed_derived_section_start(label):
        return ""

    norm_label = normalize_whitespace(label).casefold()
    total = 0
    match = 0
    for c in peptide_col_idxs:
        if c >= len(row):
            continue
        txt = normalize_whitespace(row[c])
        if not txt:
            continue
        total += 1
        if normalize_whitespace(txt).casefold() == norm_label:
            match += 1
    if total >= 2 and match >= max(2, int(0.6 * total)):
        return label
    return ""


def emit_transposed_experimental_records_from_table(
    t: ParsedTable,
    *,
    paper: PaperRecord,
    exp_writer: csv.DictWriter,
    source_path: str,
    seq_map: dict[str, dict[str, str]],
) -> int:
    """
    Handle common "transposed" layouts where peptide IDs are in columns and conditions in rows,
    with sequences provided elsewhere (seq_map).
    """
    if not t.rows or len(t.rows) < 2:
        return 0
    if not seq_map:
        return 0

    peptide_header_row_idx, peptide_cols = detect_transposed_peptide_header(t.rows, seq_map)
    if peptide_header_row_idx is None or not peptide_cols:
        return 0

    peptide_col_idxs = sorted(peptide_cols.keys())
    endpoint_header_row_idx = detect_transposed_endpoint_header(t.rows, peptide_cols)
    header_rows_end = max(peptide_header_row_idx, endpoint_header_row_idx or peptide_header_row_idx)

    table_prefix, table_unit = table_level_endpoint_hint(caption=t.caption, foot=t.foot, label=t.label)
    table_kw = endpoint_keywords_in_text(f"{t.label} {t.caption} {t.foot}")

    col_meta: dict[int, dict[str, Any]] = {}
    for c_idx in peptide_col_idxs:
        parts: list[str] = []
        for r in range(header_rows_end + 1):
            if r >= len(t.rows):
                break
            if c_idx >= len(t.rows[r]):
                continue
            txt = normalize_whitespace(t.rows[r][c_idx])
            if txt:
                parts.append(txt)
        header_text = " ".join(uniq_preserve_order(parts))
        prefix, unit = header_endpoint_hint(header_text)
        if not prefix:
            prefix = table_prefix
        if not unit:
            unit = table_unit
        col_meta[c_idx] = {
            "header_text": header_text,
            "prefix": prefix,
            "unit": unit,
            "keywords": endpoint_keywords_in_text(header_text),
        }

    cond_col_count = min(peptide_col_idxs) if peptide_col_idxs else 0
    cond_col_idxs = list(range(cond_col_count))
    header_for_ctx = combined_headers(t.rows, header_rows_end)
    cond_headers = [header_for_ctx[i] if i < len(header_for_ctx) else "" for i in cond_col_idxs]

    active_section_label = ""
    in_skip_section = False
    emitted = 0

    for r_idx in range(header_rows_end + 1, len(t.rows)):
        row = t.rows[r_idx]
        cond_vals = [normalize_whitespace(row[i] if i < len(row) else "") for i in cond_col_idxs]
        primary_label = ""
        for v in cond_vals:
            if v:
                primary_label = v
                break

        section_label = transposed_section_start_label(row, primary_label=primary_label, peptide_col_idxs=peptide_col_idxs)
        if section_label:
            active_section_label = section_label
            in_skip_section = True
            continue

        row_endpoint = endpoint_override_from_cell(primary_label) if primary_label else ""
        if row_endpoint:
            active_section_label = ""
            in_skip_section = False

        if in_skip_section:
            continue
        if primary_label and should_skip_transposed_condition(primary_label):
            continue

        condition = ""
        if not row_endpoint:
            condition = normalize_whitespace(" | ".join([v for v in cond_vals if v]))

        conds = uniq_preserve_order(cond for cell in row for cond in find_conditions(cell))
        row_snippet = " | ".join([normalize_whitespace(c) for c in row if normalize_whitespace(c)])

        # Include a short context for condition columns (for audit).
        cond_ctx_pairs: list[str] = []
        for h, v in zip(cond_headers, cond_vals):
            vv = normalize_whitespace(v)
            if not vv:
                continue
            hh = normalize_whitespace(h)
            if hh and not (header_endpoint_hint(hh)[0] or header_endpoint_hint(hh)[1]):
                cond_ctx_pairs.append(f"{hh}={vv}")
            else:
                cond_ctx_pairs.append(vv)
            if len(cond_ctx_pairs) >= 4:
                break

        for c_idx in peptide_col_idxs:
            if c_idx >= len(row):
                continue
            cell = row[c_idx]
            if not normalize_whitespace(cell):
                continue

            col_info = col_meta.get(c_idx) or {}
            header_text = str(col_info.get("header_text") or "")
            hint_prefix = str(col_info.get("prefix") or "")
            hint_unit = str(col_info.get("unit") or "")

            if row_endpoint:
                hint_prefix = row_endpoint
                _, ru = header_endpoint_hint(primary_label)
                hint_unit = ru or hint_unit or table_unit

            kw = set(col_info.get("keywords") or set())
            kw |= table_kw
            pair_mode = (not row_endpoint) and ({"MIC", "MBC"} <= kw)

            seq_info = peptide_cols[c_idx].get("seq_info") or {}
            peptide_id = str(peptide_cols[c_idx].get("peptide_id") or "")

            # MIC/MBC pairs encoded as "4(8)" or "2/2"
            if pair_mode:
                m = MIC_MBC_PAIR_RE.search(cell) or MIC_MBC_SLASH_RE.search(cell)
                if m:
                    for endpoint_key, cmp_key, val_key in (
                        ("MIC", "mic_cmp", "mic_val"),
                        ("MBC", "mbc_cmp", "mbc_val"),
                    ):
                        val = _to_float(m.group(val_key))
                        if val is None:
                            continue
                        exp_writer.writerow(
                            {
                                "extracted_at": utc_now_iso(),
                                "doi": paper.doi,
                                "pmid": paper.pmid,
                                "pmcid": paper.pmcid,
                                "paper_stem": paper.stem,
                                "title": paper.title,
                                "source_kind": "xml_table_transposed_join",
                                "source_path": source_path,
                                "source_ref": (
                                    f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};"
                                    f"peptide_header_row_idx={peptide_header_row_idx};"
                                    f"endpoint_header_row_idx={endpoint_header_row_idx if endpoint_header_row_idx is not None else ''};"
                                    f"header_rows_end={header_rows_end}"
                                ),
                                "peptide_id": peptide_id,
                                "sequence_raw": str(seq_info.get("sequence_raw") or ""),
                                "sequence": str(seq_info.get("sequence") or ""),
                                "endpoint": endpoint_key,
                                "condition": condition,
                                "cmp": str(m.group(cmp_key) or ""),
                                "value": val,
                                "error": "",
                                "range_low": "",
                                "range_high": "",
                                "unit": hint_unit,
                                "conditions": ";".join(conds),
                                "snippet": row_snippet,
                                "context": normalize_whitespace(
                                    ";".join(
                                        [
                                            f"table_label={t.label}",
                                            f"table_caption={t.caption}",
                                            f"seq_source_ref={seq_info.get('sequence_source_ref','')}",
                                            f"val_col_header={header_text}",
                                            f"raw_value={cell}",
                                            f"active_section={active_section_label}" if active_section_label else "",
                                            *cond_ctx_pairs,
                                        ]
                                    )
                                ),
                            }
                        )
                        emitted += 1
                    continue

            measurements = find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit)
            if hint_unit:
                hu = normalize_whitespace(hint_unit)
                with_unit = [m for m in measurements if normalize_whitespace(str(m.get("unit") or ""))]
                if with_unit:
                    matches = [
                        m
                        for m in measurements
                        if normalize_whitespace(str(m.get("unit") or "")).casefold() == hu.casefold()
                    ]
                    if matches:
                        measurements = matches
            dose_info = ""
            if hint_prefix.upper() == "HEMOLYSIS" and hint_unit.strip() == "%":
                measurements, dose_info = _split_hemolysis_percent_vs_dose(measurements)

            for meas in measurements:
                if not (meas.get("prefix") or ""):
                    continue
                extra_ctx = [*cond_ctx_pairs]
                if dose_info:
                    extra_ctx.append(f"dose_info={dose_info}")
                exp_writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": "xml_table_transposed_join",
                        "source_path": source_path,
                        "source_ref": (
                            f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};"
                            f"peptide_header_row_idx={peptide_header_row_idx};"
                            f"endpoint_header_row_idx={endpoint_header_row_idx if endpoint_header_row_idx is not None else ''};"
                            f"header_rows_end={header_rows_end}"
                        ),
                        "peptide_id": peptide_id,
                        "sequence_raw": str(seq_info.get("sequence_raw") or ""),
                        "sequence": str(seq_info.get("sequence") or ""),
                        "endpoint": str(meas.get("prefix") or ""),
                        "condition": condition,
                        "cmp": str(meas.get("cmp") or ""),
                        "value": meas.get("value", "") if meas.get("value") is not None else "",
                        "error": meas.get("error", "") if meas.get("error") is not None else "",
                        "range_low": meas.get("range_low", "") if meas.get("range_low") is not None else "",
                        "range_high": meas.get("range_high", "") if meas.get("range_high") is not None else "",
                        "unit": str(meas.get("unit") or ""),
                        "conditions": ";".join(conds),
                        "snippet": row_snippet,
                        "context": normalize_whitespace(
                            ";".join(
                                [
                                    f"table_label={t.label}",
                                    f"table_caption={t.caption}",
                                    f"seq_source_ref={seq_info.get('sequence_source_ref','')}",
                                    f"val_col_header={header_text}",
                                    f"raw_value={meas.get('raw','')}",
                                    f"active_section={active_section_label}" if active_section_label else "",
                                    *extra_ctx,
                                ]
                            )
                        ),
                    }
                )
                emitted += 1

    return emitted


def emit_joined_experimental_records_from_tables(
    tables: list[ParsedTable],
    *,
    paper: PaperRecord,
    exp_writer: Optional[csv.DictWriter],
    source_path: str,
    include_computational: bool = False,
) -> int:
    if exp_writer is None:
        return 0
    if not tables:
        return 0

    seq_map = extract_sequence_map_from_tables(tables)
    emitted = 0

    computational_hint_res = (
        re.compile(r"\bcomputational\b", flags=re.IGNORECASE),
        re.compile(r"\bin\s*silico\b", flags=re.IGNORECASE),
        re.compile(r"\bpredict(?:ion|ed|ive)?\b", flags=re.IGNORECASE),
        re.compile(r"\bmachine\s+learning\b", flags=re.IGNORECASE),
        re.compile(r"\bdeep\s+learning\b", flags=re.IGNORECASE),
        re.compile(r"\bweb\s*server\b", flags=re.IGNORECASE),
        re.compile(r"\bwebserver\b", flags=re.IGNORECASE),
        re.compile(r"\bsoftware\b", flags=re.IGNORECASE),
        re.compile(r"\btool\b", flags=re.IGNORECASE),
    )

    def filter_measurements_by_hint_unit(measurements: list[dict[str, Any]], hint_unit: str) -> list[dict[str, Any]]:
        """
        Many MIC/MBC tables encode an alternate unit in parentheses, e.g. "128 (0.20)" with
        header "MIC, µM (mg/mL)". Keep the measurements that match the header hint unit
        when present, to avoid duplicating each cell.
        """
        hu = normalize_whitespace(hint_unit or "")
        if not hu:
            return measurements
        with_unit = [m for m in measurements if normalize_whitespace(str(m.get("unit") or ""))]
        if not with_unit:
            return measurements
        matches = [
            m
            for m in measurements
            if normalize_whitespace(str(m.get("unit") or "")).casefold() == hu.casefold()
        ]
        return matches or measurements

    def infer_single_peptide_from_table_text(text: str) -> Optional[str]:
        if not seq_map:
            return None
        norm_text = normalize_peptide_id(text or "")
        if not norm_text:
            return None
        matches: list[str] = []
        for nid in seq_map.keys():
            if len(nid) < 6 or (not re.search(r"[a-z]", nid)):
                continue
            if nid in norm_text:
                matches.append(nid)
                if len(matches) >= 2:
                    break
        return matches[0] if len(matches) == 1 else None

    for t in tables:
        if not t.rows or len(t.rows) < 2:
            continue
        table_emitted = 0

        # ---------- Row-wise layout: peptide id in rows ----------
        header_row_idx = choose_header_row_index(t.rows)
        headers = combined_headers(t.rows, header_row_idx)
        data_rows = t.rows[header_row_idx + 1 :]

        if not include_computational:
            cap = normalize_whitespace(f"{t.caption} {t.foot}").lower()
            if any(rx.search(cap) for rx in computational_hint_res):
                has_experiment_marker = any(
                    re.search(r"\bexperiment(?:al)?\b|\bmeasured\b|\bobserved\b", normalize_whitespace(h), flags=re.IGNORECASE)
                    for h in headers
                )
                if not has_experiment_marker:
                    continue

        table_prefix, table_unit = table_level_endpoint_hint(caption=t.caption, foot=t.foot, label=t.label)
        table_kw = endpoint_keywords_in_text(f"{t.label} {t.caption} {t.foot}")

        id_idx = guess_id_column(headers)
        if id_idx is None:
            best_idx, _ = best_id_column_by_seqmap(headers, data_rows, seq_map)
            id_idx = best_idx
        elif seq_map:
            # If the guessed id column does not match the seq_map well, fall back to the best-matching column.
            cur_cnt = 0
            for r in data_rows[:200]:
                if id_idx >= len(r):
                    continue
                if normalize_peptide_id(r[id_idx]) in seq_map:
                    cur_cnt += 1
            best_idx, best_cnt = best_id_column_by_seqmap(headers, data_rows, seq_map)
            if best_idx is not None and best_idx != id_idx and best_cnt > max(cur_cnt * 2, cur_cnt + 3):
                id_idx = best_idx

        param_idx = guess_parameter_column(headers)

        endpoint_cols: list[dict[str, Any]] = []
        endpoint_cols = pick_endpoint_columns(
            headers,
            data_rows,
            table_prefix=table_prefix,
            table_unit=table_unit,
            id_idx=id_idx if id_idx is not None else -1,
        )

        if id_idx is not None and endpoint_cols:
            for r_idx, row in enumerate(data_rows, start=header_row_idx + 1):
                if id_idx >= len(row):
                    continue
                peptide_id = normalize_whitespace(row[id_idx])
                if not peptide_id:
                    continue
                norm_id = normalize_peptide_id(peptide_id)
                seq_info = seq_map.get(norm_id)
                if not seq_info:
                    # Common layout: the first column itself contains the AA sequence (no separate "Sequence" column).
                    seq_inline = canonical_sequence_from_cell(peptide_id, min_len=SEQUENCE_MIN_LEN_LOOSE)
                    if seq_inline:
                        seq_info = {
                            "sequence_raw": peptide_id,
                            "sequence": seq_inline,
                            "sequence_source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={id_idx};kind=inline_sequence_id",
                        }
                    else:
                        continue  # only emit sequence-linked experimental records

                conds = uniq_preserve_order(cond for cell in row for cond in find_conditions(cell))
                row_snippet = " | ".join([normalize_whitespace(c) for c in row if normalize_whitespace(c)])

                # Extra structured context from non-endpoint columns (best-effort; keep short).
                ctx_pairs: list[str] = []
                for c_idx, cell in enumerate(row):
                    if c_idx == id_idx:
                        continue
                    if any(ec["col"] == c_idx for ec in endpoint_cols):
                        continue
                    key = normalize_whitespace(headers[c_idx] if c_idx < len(headers) else "")
                    val = normalize_whitespace(cell)
                    if not key or not val:
                        continue
                    if len(val) > 120:
                        continue
                    ctx_pairs.append(f"{key}={val}")
                    if len(ctx_pairs) >= 6:
                        break

                for ec in endpoint_cols:
                    c_idx = int(ec["col"])
                    if c_idx >= len(row):
                        continue
                    cell = row[c_idx]
                    if not normalize_whitespace(cell):
                        continue
                    # If the endpoint is stored as a per-row "Parameter/Endpoint" label, prefer it
                    # over a weak table-level hint (e.g., caption contains "MIC/MBC/IC50" and the
                    # numeric columns are just units like "µM").
                    row_endpoint = ""
                    if (param_idx is not None) and (0 <= param_idx < len(row)):
                        row_endpoint = endpoint_override_from_cell(row[param_idx])

                    header_text = headers[c_idx] if c_idx < len(headers) else ""
                    strong_prefix = bool(header_endpoint_hint(header_text)[0])
                    if _is_hemolysis_header(header_text):
                        strong_prefix = True

                    hint_prefix = str(ec.get("prefix") or "")
                    if row_endpoint and not strong_prefix:
                        hint_prefix = row_endpoint
                    hint_unit = str(ec.get("unit") or "")

                    col_kw = endpoint_keywords_in_text(header_text)
                    pair_mode = (not row_endpoint) and ({"MIC", "MBC"} <= col_kw or {"MIC", "MBC"} <= table_kw)

                    if pair_mode:
                        m = MIC_MBC_PAIR_RE.search(cell) or MIC_MBC_SLASH_RE.search(cell)
                        if m:
                            for endpoint_key, cmp_key, val_key in (
                                ("MIC", "mic_cmp", "mic_val"),
                                ("MBC", "mbc_cmp", "mbc_val"),
                            ):
                                val = _to_float(m.group(val_key))
                                if val is None:
                                    continue
                                exp_writer.writerow(
                                    {
                                        "extracted_at": utc_now_iso(),
                                        "doi": paper.doi,
                                        "pmid": paper.pmid,
                                        "pmcid": paper.pmcid,
                                        "paper_stem": paper.stem,
                                        "title": paper.title,
                                        "source_kind": "xml_table_join",
                                        "source_path": source_path,
                                        "source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};header_row_idx={header_row_idx}",
                                        "peptide_id": peptide_id,
                                        "sequence_raw": str(seq_info.get("sequence_raw") or ""),
                                        "sequence": str(seq_info.get("sequence") or ""),
                                        "endpoint": endpoint_key,
                                        "condition": str(ec.get("condition") or ""),
                                        "cmp": str(m.group(cmp_key) or ""),
                                        "value": val,
                                        "error": "",
                                        "range_low": "",
                                        "range_high": "",
                                        "unit": hint_unit,
                                        "conditions": ";".join(conds),
                                        "snippet": row_snippet,
                                        "context": normalize_whitespace(
                                            ";".join(
                                                [
                                                    f"table_label={t.label}",
                                                    f"table_caption={t.caption}",
                                                    f"seq_source_ref={seq_info.get('sequence_source_ref','')}",
                                                    f"val_col_header={header_text}",
                                                    f"raw_value={cell}",
                                                    *ctx_pairs,
                                                ]
                                            )
                                        ),
                                    }
                                )
                                emitted += 1
                                table_emitted += 1
                            continue

                    measurements = find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit)
                    measurements = filter_measurements_by_hint_unit(measurements, hint_unit)
                    dose_info = ""
                    if hint_prefix.upper() == "HEMOLYSIS" and hint_unit.strip() == "%":
                        measurements, dose_info = _split_hemolysis_percent_vs_dose(measurements)

                    for meas in measurements:
                        if not (meas.get("prefix") or ""):
                            continue
                        extra_ctx = [*ctx_pairs]
                        if dose_info:
                            extra_ctx.append(f"dose_info={dose_info}")
                        exp_writer.writerow(
                            {
                                "extracted_at": utc_now_iso(),
                                "doi": paper.doi,
                                "pmid": paper.pmid,
                                "pmcid": paper.pmcid,
                                "paper_stem": paper.stem,
                                "title": paper.title,
                                "source_kind": "xml_table_join",
                                "source_path": source_path,
                                "source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};header_row_idx={header_row_idx}",
                                "peptide_id": peptide_id,
                                "sequence_raw": str(seq_info.get("sequence_raw") or ""),
                                "sequence": str(seq_info.get("sequence") or ""),
                                "endpoint": str(meas.get("prefix") or ""),
                                "condition": str(ec.get("condition") or ""),
                                "cmp": str(meas.get("cmp") or ""),
                                "value": meas.get("value", "") if meas.get("value") is not None else "",
                                "error": meas.get("error", "") if meas.get("error") is not None else "",
                                "range_low": meas.get("range_low", "") if meas.get("range_low") is not None else "",
                                "range_high": meas.get("range_high", "") if meas.get("range_high") is not None else "",
                                "unit": str(meas.get("unit") or ""),
                                "conditions": ";".join(conds),
                                "snippet": row_snippet,
                                "context": normalize_whitespace(
                                    ";".join(
                                        [
                                            f"table_label={t.label}",
                                            f"table_caption={t.caption}",
                                            f"seq_source_ref={seq_info.get('sequence_source_ref','')}",
                                            f"val_col_header={headers[c_idx] if c_idx < len(headers) else ''}",
                                            f"raw_value={meas.get('raw','')}",
                                            *extra_ctx,
                                        ]
                                    )
                                ),
                            }
                        )
                        emitted += 1
                        table_emitted += 1

        # ---------- No explicit peptide-id column: infer a single peptide from caption/foot ----------
        if table_emitted == 0 and id_idx is None and endpoint_cols:
            inferred_norm_id = infer_single_peptide_from_table_text(f"{t.label} {t.caption} {t.foot}")
            inferred_seq_info = seq_map.get(inferred_norm_id or "") if inferred_norm_id else None
            if inferred_seq_info and (inferred_seq_info.get("sequence") or inferred_seq_info.get("sequence_raw")):
                inferred_peptide_id = str(inferred_seq_info.get("peptide_id") or "")
                for r_idx, row in enumerate(data_rows, start=header_row_idx + 1):
                    conds = uniq_preserve_order(cond for cell in row for cond in find_conditions(cell))
                    row_snippet = " | ".join([normalize_whitespace(c) for c in row if normalize_whitespace(c)])

                    # Best-effort compact context from non-endpoint columns (e.g., organism/strain).
                    ctx_pairs: list[str] = []
                    for c_idx, cell in enumerate(row):
                        if any(ec["col"] == c_idx for ec in endpoint_cols):
                            continue
                        val = normalize_whitespace(cell)
                        if not val or len(val) > 160:
                            continue
                        key = normalize_whitespace(headers[c_idx] if c_idx < len(headers) else "")
                        ctx_pairs.append(f"{key}={val}" if key else val)
                        if len(ctx_pairs) >= 6:
                            break

                    for ec in endpoint_cols:
                        c_idx = int(ec["col"])
                        if c_idx >= len(row):
                            continue
                        cell = row[c_idx]
                        if not normalize_whitespace(cell):
                            continue

                        row_endpoint = ""
                        if (param_idx is not None) and (0 <= param_idx < len(row)):
                            row_endpoint = endpoint_override_from_cell(row[param_idx])

                        header_text = headers[c_idx] if c_idx < len(headers) else ""
                        strong_prefix = bool(header_endpoint_hint(header_text)[0])
                        if _is_hemolysis_header(header_text):
                            strong_prefix = True

                        hint_prefix = str(ec.get("prefix") or "")
                        if row_endpoint and not strong_prefix:
                            hint_prefix = row_endpoint
                        hint_unit = str(ec.get("unit") or "")

                        col_kw = endpoint_keywords_in_text(header_text)
                        pair_mode = (not row_endpoint) and ({"MIC", "MBC"} <= col_kw or {"MIC", "MBC"} <= table_kw)
                        if pair_mode:
                            m = MIC_MBC_PAIR_RE.search(cell) or MIC_MBC_SLASH_RE.search(cell)
                            if m:
                                for endpoint_key, cmp_key, val_key in (
                                    ("MIC", "mic_cmp", "mic_val"),
                                    ("MBC", "mbc_cmp", "mbc_val"),
                                ):
                                    val = _to_float(m.group(val_key))
                                    if val is None:
                                        continue
                                    exp_writer.writerow(
                                        {
                                            "extracted_at": utc_now_iso(),
                                            "doi": paper.doi,
                                            "pmid": paper.pmid,
                                            "pmcid": paper.pmcid,
                                            "paper_stem": paper.stem,
                                            "title": paper.title,
                                            "source_kind": "xml_table_join_inferred_peptide",
                                            "source_path": source_path,
                                            "source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};header_row_idx={header_row_idx};inferred_peptide=1",
                                            "peptide_id": inferred_peptide_id,
                                            "sequence_raw": str(inferred_seq_info.get("sequence_raw") or ""),
                                            "sequence": str(inferred_seq_info.get("sequence") or ""),
                                            "endpoint": endpoint_key,
                                            "condition": str(ec.get("condition") or ""),
                                            "cmp": str(m.group(cmp_key) or ""),
                                            "value": val,
                                            "error": "",
                                            "range_low": "",
                                            "range_high": "",
                                            "unit": hint_unit,
                                            "conditions": ";".join(conds),
                                            "snippet": row_snippet,
                                            "context": normalize_whitespace(
                                                ";".join(
                                                    [
                                                        f"table_label={t.label}",
                                                        f"table_caption={t.caption}",
                                                        f"seq_source_ref={inferred_seq_info.get('sequence_source_ref','')}",
                                                        f"val_col_header={header_text}",
                                                        f"raw_value={cell}",
                                                        *ctx_pairs,
                                                    ]
                                                )
                                            ),
                                        }
                                    )
                                    emitted += 1
                                    table_emitted += 1
                                continue

                        measurements = find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit)
                        measurements = filter_measurements_by_hint_unit(measurements, hint_unit)
                        dose_info = ""
                        if hint_prefix.upper() == "HEMOLYSIS" and hint_unit.strip() == "%":
                            measurements, dose_info = _split_hemolysis_percent_vs_dose(measurements)

                        for meas in measurements:
                            if not (meas.get("prefix") or ""):
                                continue
                            extra_ctx = [*ctx_pairs]
                            if dose_info:
                                extra_ctx.append(f"dose_info={dose_info}")
                            exp_writer.writerow(
                                {
                                    "extracted_at": utc_now_iso(),
                                    "doi": paper.doi,
                                    "pmid": paper.pmid,
                                    "pmcid": paper.pmcid,
                                    "paper_stem": paper.stem,
                                    "title": paper.title,
                                    "source_kind": "xml_table_join_inferred_peptide",
                                    "source_path": source_path,
                                    "source_ref": f"table_id={t.table_id};row_idx={r_idx};col_idx={c_idx};header_row_idx={header_row_idx};inferred_peptide=1",
                                    "peptide_id": inferred_peptide_id,
                                    "sequence_raw": str(inferred_seq_info.get("sequence_raw") or ""),
                                    "sequence": str(inferred_seq_info.get("sequence") or ""),
                                    "endpoint": str(meas.get("prefix") or ""),
                                    "condition": str(ec.get("condition") or ""),
                                    "cmp": str(meas.get("cmp") or ""),
                                    "value": meas.get("value", "") if meas.get("value") is not None else "",
                                    "error": meas.get("error", "") if meas.get("error") is not None else "",
                                    "range_low": meas.get("range_low", "") if meas.get("range_low") is not None else "",
                                    "range_high": meas.get("range_high", "") if meas.get("range_high") is not None else "",
                                    "unit": str(meas.get("unit") or ""),
                                    "conditions": ";".join(conds),
                                    "snippet": row_snippet,
                                    "context": normalize_whitespace(
                                        ";".join(
                                            [
                                                f"table_label={t.label}",
                                                f"table_caption={t.caption}",
                                                f"seq_source_ref={inferred_seq_info.get('sequence_source_ref','')}",
                                                f"val_col_header={headers[c_idx] if c_idx < len(headers) else ''}",
                                                f"raw_value={meas.get('raw','')}",
                                                *extra_ctx,
                                            ]
                                        )
                                    ),
                                }
                            )
                            emitted += 1
                            table_emitted += 1

        # ---------- Transposed layout: peptide id in columns ----------
        if table_emitted == 0:
            table_emitted += emit_transposed_experimental_records_from_table(
                t,
                paper=paper,
                exp_writer=exp_writer,
                source_path=source_path,
                seq_map=seq_map,
            )
            emitted += table_emitted

    return emitted



def write_table_csv(rows: list[list[str]], out_path: Path, *, overwrite: bool) -> None:
    if out_path.exists() and not overwrite:
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for r in rows:
            w.writerow(r)


def iter_manifest_records(input_dir: Path) -> list[dict[str, Any]]:
    manifest = input_dir / "download_manifest.jsonl"
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
        key = str(rec.get("normalized") or rec.get("input") or "")
        if not key:
            continue
        latest[key] = rec
    return list(latest.values())


@dataclass
class PaperRecord:
    stem: str
    input_dir: Path
    doi: str = ""
    pmid: str = ""
    pmcid: str = ""
    title: str = ""
    pdf_path: Optional[Path] = None
    xml_path: Optional[Path] = None
    supplementary_dir: Optional[Path] = None


def build_paper_records(input_dir: Path) -> list[PaperRecord]:
    records: list[PaperRecord] = []
    manifest_records = iter_manifest_records(input_dir)
    if not manifest_records:
        # Fallback: infer stems from xml files.
        for xml_path in sorted(input_dir.glob("*.xml")):
            stem = xml_path.stem
            records.append(
                PaperRecord(
                    stem=stem,
                    input_dir=input_dir,
                    xml_path=xml_path,
                    pdf_path=(input_dir / f"{stem}.pdf" if (input_dir / f"{stem}.pdf").exists() else None),
                    supplementary_dir=(input_dir / "supplementary" / stem),
                )
            )
        return records

    for rec in manifest_records:
        normalized = str(rec.get("normalized") or rec.get("input") or "").strip()
        if not normalized:
            continue
        stem = safe_stem(normalized)
        pdf_path = input_dir / f"{stem}.pdf"
        xml_path = input_dir / f"{stem}.xml"
        supp_dir = input_dir / "supplementary" / stem
        pr = PaperRecord(
            stem=stem,
            input_dir=input_dir,
            pdf_path=pdf_path if pdf_path.exists() else None,
            xml_path=xml_path if xml_path.exists() else None,
            supplementary_dir=supp_dir if supp_dir.exists() else None,
        )

        # Try to populate IDs from manifest XML meta when available.
        for a in rec.get("actions") or []:
            if not isinstance(a, dict):
                continue
            if a.get("kind") == "xml":
                meta = a.get("meta") or {}
                if isinstance(meta, dict):
                    pr.doi = str(meta.get("doi") or pr.doi)
                    pr.pmid = str(meta.get("pmid") or pr.pmid)
                    pr.pmcid = str(meta.get("pmcid") or pr.pmcid)
        if (rec.get("id_type") == "doi") and not pr.doi:
            pr.doi = normalized
        records.append(pr)
    return records


def emit_experimental_records_from_rows(
    rows: list[list[str]],
    *,
    paper: PaperRecord,
    exp_writer: Optional[csv.DictWriter],
    source_kind: str,
    source_path: str,
    source_ref_prefix: str,
) -> None:
    if exp_writer is None:
        return
    if not rows:
        return

    headers = rows[0] if rows else []
    for r_idx, row in enumerate(rows[1:], start=1):
        if not row:
            continue

        row_header = row[0] if row else ""

        seq_items: list[dict[str, Any]] = []
        for c_idx, cell in enumerate(row):
            col_header = headers[c_idx] if c_idx < len(headers) else ""
            hint_is_seq = bool(re.search(r"\b(seq|sequence|sequences)\b", (col_header + " " + row_header), flags=re.IGNORECASE))
            if not hint_is_seq:
                continue
            for seq in find_sequences(cell, min_len=SEQUENCE_MIN_LEN_LOOSE):
                seq_items.append({"sequence": seq, "sequence_raw": normalize_whitespace(cell), "col": c_idx, "col_header": col_header})

        if not seq_items:
            continue

        meas_items: list[dict[str, Any]] = []
        for c_idx, cell in enumerate(row):
            col_header = headers[c_idx] if c_idx < len(headers) else ""
            hint_prefix, hint_unit = header_endpoint_hint(col_header)
            for meas in find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit):
                if not (meas.get("prefix") or ""):
                    continue
                meas_items.append(
                    {
                        **meas,
                        "col": c_idx,
                        "col_header": col_header,
                    }
                )

        if not meas_items:
            continue

        conds = uniq_preserve_order(cond for cell in row for cond in find_conditions(cell))
        row_snippet = " | ".join([normalize_whitespace(c) for c in row if normalize_whitespace(c)])

        for s in seq_items:
            seq = str(s.get("sequence") or "")
            if not seq:
                continue
            for meas in meas_items:
                exp_writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": source_kind,
                        "source_path": source_path,
                        "source_ref": f"{source_ref_prefix};row={r_idx};seq_col={s.get('col','')};val_col={meas.get('col','')}",
                        "peptide_id": "",
                        "sequence_raw": str(s.get("sequence_raw") or ""),
                        "sequence": seq,
                        "endpoint": str(meas.get("prefix") or ""),
                        "condition": "",
                        "cmp": str(meas.get("cmp") or ""),
                        "value": meas.get("value", "") if meas.get("value") is not None else "",
                        "error": meas.get("error", "") if meas.get("error") is not None else "",
                        "range_low": meas.get("range_low", "") if meas.get("range_low") is not None else "",
                        "range_high": meas.get("range_high", "") if meas.get("range_high") is not None else "",
                        "unit": str(meas.get("unit") or ""),
                        "conditions": ";".join(conds),
                        "snippet": row_snippet,
                        "context": f"seq_col_header={s.get('col_header','')};val_col_header={meas.get('col_header','')};raw_value={meas.get('raw','')}",
                    }
                )


def extract_from_xml(
    paper: PaperRecord,
    *,
    tables_dir: Path,
    writer: csv.DictWriter,
    exp_writer: Optional[csv.DictWriter],
    overwrite: bool,
    include_computational: bool,
) -> None:
    if not paper.xml_path or not paper.xml_path.exists():
        return
    try:
        root = ET.fromstring(paper.xml_path.read_text(encoding="utf-8", errors="ignore"))
    except Exception as e:
        writer.writerow(
            {
                "extracted_at": utc_now_iso(),
                "doi": paper.doi,
                "pmid": paper.pmid,
                "pmcid": paper.pmcid,
                "paper_stem": paper.stem,
                "title": paper.title,
                "source_kind": "xml",
                "source_path": str(paper.xml_path),
                "source_ref": "parse_error",
                "extraction_type": "error",
                "entity": repr(e),
                "numeric_value": "",
                "unit": "",
                "snippet": "",
                "context": "",
            }
        )
        return

    ids = jats_ids(root)
    paper.doi = paper.doi or ids.get("doi", "")
    paper.pmid = paper.pmid or ids.get("pmid", "")
    paper.pmcid = paper.pmcid or ids.get("pmcid", "")
    paper.title = paper.title or jats_article_title(root)

    parsed_tables: list[ParsedTable] = []

    # Extract tables
    for t in iter_jats_tables(root):
        table_el = t.get("elem")
        if table_el is None:
            continue
        rows = table_elem_to_matrix(table_el)
        if not rows:
            continue

        parsed_tables.append(
            ParsedTable(
                table_id=str(t.get("id") or ""),
                label=str(t.get("label") or ""),
                caption=str(t.get("caption") or ""),
                foot=str(t.get("foot") or ""),
                rows=rows,
            )
        )

        table_name = safe_stem(f"{paper.stem}__xml__{t['id']}")
        table_out = tables_dir / f"{table_name}.csv"
        write_table_csv(rows, table_out, overwrite=overwrite)

        writer.writerow(
            {
                "extracted_at": utc_now_iso(),
                "doi": paper.doi,
                "pmid": paper.pmid,
                "pmcid": paper.pmcid,
                "paper_stem": paper.stem,
                "title": paper.title,
                "source_kind": "xml_table",
                "source_path": str(paper.xml_path),
                "source_ref": f"table_id={t['id']};label={t.get('label','')}",
                "extraction_type": "table",
                "entity": str(table_out),
                "numeric_value": "",
                "unit": "",
                "snippet": t.get("caption", ""),
                "context": t.get("caption", ""),
            }
        )

        # Heuristic headers
        header_row = rows[0] if rows else []
        for r_idx, row in enumerate(rows):
            row_header = row[0] if row else ""
            for c_idx, cell in enumerate(row):
                col_header = header_row[c_idx] if c_idx < len(header_row) else ""
                hint_is_seq = bool(re.search(r"\b(seq|sequence|sequences)\b", (col_header + " " + row_header), flags=re.IGNORECASE))
                if hint_is_seq:
                    seq = canonical_sequence_from_cell(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                    seqs = [seq] if seq else find_sequences(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                    for s in seqs:
                        writer.writerow(
                            {
                                "extracted_at": utc_now_iso(),
                                "doi": paper.doi,
                                "pmid": paper.pmid,
                                "pmcid": paper.pmcid,
                                "paper_stem": paper.stem,
                                "title": paper.title,
                                "source_kind": "xml_table_cell",
                                "source_path": str(paper.xml_path),
                                "source_ref": f"table_id={t['id']};row={r_idx};col={c_idx}",
                                "extraction_type": "sequence",
                                "entity": s,
                                "numeric_value": "",
                                "unit": "",
                                "snippet": cell,
                                "context": f"col_header={col_header};row_header={row_header}",
                            }
                        )

                hint_prefix, hint_unit = header_endpoint_hint(col_header)
                for meas in find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit):
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": "xml_table_cell",
                            "source_path": str(paper.xml_path),
                            "source_ref": f"table_id={t['id']};row={r_idx};col={c_idx}",
                            "extraction_type": "endpoint_value",
                            "entity": meas.get("raw", ""),
                            "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                            "unit": meas.get("unit", ""),
                            "snippet": cell,
                            "context": f"prefix={meas.get('prefix','')};col_header={col_header};row_header={row_header}",
                        }
                    )

                for cond in find_conditions(cell):
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": "xml_table_cell",
                            "source_path": str(paper.xml_path),
                            "source_ref": f"table_id={t['id']};row={r_idx};col={c_idx}",
                            "extraction_type": "condition",
                            "entity": cond,
                            "numeric_value": "",
                            "unit": "",
                            "snippet": cell,
                            "context": f"col_header={col_header};row_header={row_header}",
                        }
                    )

    # Cross-table experimental extraction (sequence table + assay table joins)
    _ = emit_joined_experimental_records_from_tables(
        parsed_tables,
        paper=paper,
        exp_writer=exp_writer,
        source_path=str(paper.xml_path),
        include_computational=include_computational,
    )

    # Threshold-like statements from body text
    body = root.find(".//{*}body")
    if body is not None:
        paragraphs = [elem_text(p) for p in body.findall(".//{*}p")]
        for p in paragraphs:
            low = p.lower()
            if not any(k in low for k in THRESHOLD_KEYWORDS):
                continue
            for sent in split_sentences(p):
                if not is_threshold_sentence(sent):
                    continue
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": "xml_text",
                        "source_path": str(paper.xml_path),
                        "source_ref": "body_sentence",
                        "extraction_type": "threshold_text",
                        "entity": sent,
                        "numeric_value": "",
                        "unit": "",
                        "snippet": sent,
                        "context": "",
                    }
                )


def extract_tables_from_dataframe(
    df: pd.DataFrame,
    *,
    paper: PaperRecord,
    tables_dir: Path,
    writer: csv.DictWriter,
    exp_writer: Optional[csv.DictWriter],
    source_kind: str,
    source_path: str,
    source_ref_prefix: str,
    overwrite: bool,
) -> Optional[ParsedTable]:
    # Normalize df to strings
    df2 = df.copy()
    df2.columns = [str(c) for c in df2.columns]
    for c in df2.columns:
        df2[c] = df2[c].astype(str)

    rows: list[list[str]] = [list(df2.columns)]
    for _, r in df2.iterrows():
        rows.append([str(x) for x in r.tolist()])

    table_out = tables_dir / f"{safe_stem(source_ref_prefix)}.csv"
    write_table_csv(rows, table_out, overwrite=overwrite)
    writer.writerow(
        {
            "extracted_at": utc_now_iso(),
            "doi": paper.doi,
            "pmid": paper.pmid,
            "pmcid": paper.pmcid,
            "paper_stem": paper.stem,
            "title": paper.title,
            "source_kind": source_kind,
            "source_path": source_path,
            "source_ref": source_ref_prefix,
            "extraction_type": "table",
            "entity": str(table_out),
            "numeric_value": "",
            "unit": "",
            "snippet": "",
            "context": "",
        }
    )

    headers = rows[0] if rows else []
    for r_idx, row in enumerate(rows[1:], start=1):
        row_header = row[0] if row else ""
        for c_idx, cell in enumerate(row):
            col_header = headers[c_idx] if c_idx < len(headers) else ""
            hint_is_seq = bool(re.search(r"\b(seq|sequence|sequences)\b", (col_header + " " + row_header), flags=re.IGNORECASE))
            if hint_is_seq:
                seq = canonical_sequence_from_cell(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                seqs = [seq] if seq else find_sequences(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                for s in seqs:
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": source_kind + "_cell",
                            "source_path": source_path,
                            "source_ref": f"{source_ref_prefix};row={r_idx};col={c_idx}",
                            "extraction_type": "sequence",
                            "entity": s,
                            "numeric_value": "",
                            "unit": "",
                            "snippet": cell,
                            "context": f"col_header={col_header};row_header={row_header}",
                        }
                    )

            hint_prefix, hint_unit = header_endpoint_hint(col_header)
            for meas in find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit):
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": source_kind + "_cell",
                        "source_path": source_path,
                        "source_ref": f"{source_ref_prefix};row={r_idx};col={c_idx}",
                        "extraction_type": "endpoint_value",
                        "entity": meas.get("raw", ""),
                        "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                        "unit": meas.get("unit", ""),
                        "snippet": cell,
                        "context": f"prefix={meas.get('prefix','')};col_header={col_header};row_header={row_header}",
                    }
                )

            for cond in find_conditions(cell):
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": source_kind + "_cell",
                        "source_path": source_path,
                        "source_ref": f"{source_ref_prefix};row={r_idx};col={c_idx}",
                        "extraction_type": "condition",
                        "entity": cond,
                        "numeric_value": "",
                        "unit": "",
                        "snippet": cell,
                        "context": f"col_header={col_header};row_header={row_header}",
                    }
                )

    emit_experimental_records_from_rows(
        rows,
        paper=paper,
        exp_writer=exp_writer,
        source_kind=source_kind + "_row",
        source_path=source_path,
        source_ref_prefix=source_ref_prefix,
    )

    # Return a ParsedTable so callers can perform cross-table joins (e.g., a sequence table
    # in one sheet and an assay table in another).
    return ParsedTable(
        table_id=source_ref_prefix,
        label="",
        caption=source_ref_prefix,
        foot="",
        rows=rows,
    )


def extract_from_supplementary(
    paper: PaperRecord,
    *,
    tables_dir: Path,
    writer: csv.DictWriter,
    exp_writer: Optional[csv.DictWriter],
    overwrite: bool,
) -> None:
    supp_dir = paper.supplementary_dir
    if not supp_dir or not supp_dir.exists():
        return

    parsed_tables: list[ParsedTable] = []

    for path in sorted(supp_dir.glob("*")):
        if path.is_dir():
            continue
        suf = path.suffix.lower()
        if suf in (".csv", ".tsv"):
            sep = "," if suf == ".csv" else "\t"
            try:
                df = pd.read_csv(path, sep=sep, dtype=str, keep_default_na=False)
            except Exception:
                continue
            t = extract_tables_from_dataframe(
                df,
                paper=paper,
                tables_dir=tables_dir,
                writer=writer,
                exp_writer=exp_writer,
                source_kind="supp_table",
                source_path=str(path),
                source_ref_prefix=f"supp_file={path.name}",
                overwrite=overwrite,
            )
            if t is not None:
                parsed_tables.append(t)
        elif suf in (".xlsx", ".xls"):
            try:
                xls = pd.ExcelFile(path)
            except Exception:
                continue
            for sheet in xls.sheet_names:
                try:
                    df = xls.parse(sheet_name=sheet, dtype=str, keep_default_na=False)
                except Exception:
                    continue
                t = extract_tables_from_dataframe(
                    df,
                    paper=paper,
                    tables_dir=tables_dir,
                    writer=writer,
                    exp_writer=exp_writer,
                    source_kind="supp_table",
                    source_path=str(path),
                    source_ref_prefix=f"supp_file={path.name};sheet={sheet}",
                    overwrite=overwrite,
                )
                if t is not None:
                    parsed_tables.append(t)
        elif suf in (".fa", ".fasta", ".faa", ".fna", ".txt"):
            # Try FASTA-like extraction
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            seqs = []
            cur = []
            in_fasta = False
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith(">"):
                    in_fasta = True
                    if cur:
                        seqs.append("".join(cur))
                        cur = []
                    continue
                if in_fasta:
                    cur.append(re.sub(r"[^A-Za-z]", "", line).upper())
            if cur:
                seqs.append("".join(cur))
            if seqs:
                for s in seqs:
                    for seq in find_sequences(s, min_len=SEQUENCE_MIN_LEN_LOOSE):
                        writer.writerow(
                            {
                                "extracted_at": utc_now_iso(),
                                "doi": paper.doi,
                                "pmid": paper.pmid,
                                "pmcid": paper.pmcid,
                                "paper_stem": paper.stem,
                                "title": paper.title,
                                "source_kind": "supp_fasta",
                                "source_path": str(path),
                                "source_ref": f"supp_file={path.name}",
                                "extraction_type": "sequence",
                                "entity": seq,
                                "numeric_value": "",
                                "unit": "",
                                "snippet": seq[:200],
                                "context": "",
                            }
                        )
            else:
                # For non-FASTA plain text, only extract threshold/measures (sequence regex is too noisy).
                low = text.lower()
                if any(k in low for k in THRESHOLD_KEYWORDS):
                    for sent in split_sentences(text):
                        if not is_threshold_sentence(sent):
                            continue
                        writer.writerow(
                            {
                                "extracted_at": utc_now_iso(),
                                "doi": paper.doi,
                                "pmid": paper.pmid,
                                "pmcid": paper.pmcid,
                                "paper_stem": paper.stem,
                                "title": paper.title,
                                "source_kind": "supp_text",
                                "source_path": str(path),
                                "source_ref": f"supp_file={path.name}",
                                "extraction_type": "threshold_text",
                                "entity": sent,
                                "numeric_value": "",
                                "unit": "",
                                "snippet": sent,
                                "context": "",
                            }
                        )
                for meas in find_measurements(text):
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": "supp_text",
                            "source_path": str(path),
                            "source_ref": f"supp_file={path.name}",
                            "extraction_type": "endpoint_value",
                            "entity": meas.get("raw", ""),
                            "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                            "unit": meas.get("unit", ""),
                            "snippet": meas.get("raw", ""),
                            "context": f"prefix={meas.get('prefix','')}",
                        }
                    )

        elif suf == ".docx":
            # Extract tables + light text scan from OOXML (WordprocessingML).
            try:
                with zipfile.ZipFile(path) as zf:
                    xml_bytes = zf.read("word/document.xml")
            except Exception:
                continue
            try:
                doc_root = ET.fromstring(xml_bytes)
            except Exception:
                continue

            # 1) Tables (higher signal than free text)
            tbl_elems = doc_root.findall(".//{*}tbl")
            for t_idx, tbl in enumerate(tbl_elems, start=1):
                t_rows: list[list[str]] = []
                for tr in tbl.findall(".//{*}tr"):
                    r: list[str] = []
                    for tc in tr.findall("./{*}tc"):
                        r.append(normalize_whitespace("".join(tc.itertext())))
                    if r:
                        t_rows.append(r)
                if not t_rows:
                    continue

                table_name = safe_stem(f"{paper.stem}__supp__{path.stem}__docx_tbl{t_idx}")
                table_out = tables_dir / f"{table_name}.csv"
                write_table_csv(t_rows, table_out, overwrite=overwrite)
                parsed_tables.append(
                    ParsedTable(
                        table_id=f"supp_file={path.name};docx_table={t_idx}",
                        label="",
                        caption=f"supp_file={path.name};docx_table={t_idx}",
                        foot="",
                        rows=t_rows,
                    )
                )
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": "supp_docx_table",
                        "source_path": str(path),
                        "source_ref": f"supp_file={path.name};docx_table={t_idx}",
                        "extraction_type": "table",
                        "entity": str(table_out),
                        "numeric_value": "",
                        "unit": "",
                        "snippet": "",
                        "context": "",
                    }
                )

                headers = t_rows[0] if t_rows else []
                for r_idx, row in enumerate(t_rows[1:], start=1):
                    row_header = row[0] if row else ""
                    for c_idx, cell in enumerate(row):
                        col_header = headers[c_idx] if c_idx < len(headers) else ""
                        hint_is_seq = bool(
                            re.search(r"\b(seq|sequence|sequences)\b", (col_header + " " + row_header), flags=re.IGNORECASE)
                        )
                        if hint_is_seq:
                            seq = canonical_sequence_from_cell(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                            seqs = [seq] if seq else find_sequences(cell, min_len=SEQUENCE_MIN_LEN_LOOSE)
                            for s in seqs:
                                writer.writerow(
                                    {
                                        "extracted_at": utc_now_iso(),
                                        "doi": paper.doi,
                                        "pmid": paper.pmid,
                                        "pmcid": paper.pmcid,
                                        "paper_stem": paper.stem,
                                        "title": paper.title,
                                        "source_kind": "supp_docx_table_cell",
                                        "source_path": str(path),
                                        "source_ref": f"supp_file={path.name};docx_table={t_idx};row={r_idx};col={c_idx}",
                                        "extraction_type": "sequence",
                                        "entity": s,
                                        "numeric_value": "",
                                        "unit": "",
                                        "snippet": cell,
                                        "context": f"col_header={col_header};row_header={row_header}",
                                    }
                                )

                        hint_prefix, hint_unit = header_endpoint_hint(col_header)
                        for meas in find_measurements(cell, hint_prefix=hint_prefix, hint_unit=hint_unit):
                            writer.writerow(
                                {
                                    "extracted_at": utc_now_iso(),
                                    "doi": paper.doi,
                                    "pmid": paper.pmid,
                                    "pmcid": paper.pmcid,
                                    "paper_stem": paper.stem,
                                    "title": paper.title,
                                    "source_kind": "supp_docx_table_cell",
                                    "source_path": str(path),
                                    "source_ref": f"supp_file={path.name};docx_table={t_idx};row={r_idx};col={c_idx}",
                                    "extraction_type": "endpoint_value",
                                    "entity": meas.get("raw", ""),
                                    "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                                    "unit": meas.get("unit", ""),
                                    "snippet": cell,
                                    "context": f"prefix={meas.get('prefix','')};col_header={col_header};row_header={row_header}",
                                }
                            )

                        for cond in find_conditions(cell):
                            writer.writerow(
                                {
                                    "extracted_at": utc_now_iso(),
                                    "doi": paper.doi,
                                    "pmid": paper.pmid,
                                    "pmcid": paper.pmcid,
                                    "paper_stem": paper.stem,
                                    "title": paper.title,
                                    "source_kind": "supp_docx_table_cell",
                                    "source_path": str(path),
                                    "source_ref": f"supp_file={path.name};docx_table={t_idx};row={r_idx};col={c_idx}",
                                    "extraction_type": "condition",
                                    "entity": cond,
                                    "numeric_value": "",
                                    "unit": "",
                                    "snippet": cond,
                                    "context": f"col_header={col_header};row_header={row_header}",
                                }
                            )

                emit_experimental_records_from_rows(
                    t_rows,
                    paper=paper,
                    exp_writer=exp_writer,
                    source_kind="supp_docx_table_row",
                    source_path=str(path),
                    source_ref_prefix=f"supp_file={path.name};docx_table={t_idx}",
                )

            # 2) Light free-text scan for endpoint mentions (no AA sequence extraction here).
            text = normalize_whitespace("".join(doc_root.itertext()))
            for meas in find_measurements(text):
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": "supp_docx_text",
                        "source_path": str(path),
                        "source_ref": f"supp_file={path.name}",
                        "extraction_type": "endpoint_value",
                        "entity": meas.get("raw", ""),
                        "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                        "unit": meas.get("unit", ""),
                        "snippet": meas.get("raw", ""),
                        "context": f"prefix={meas.get('prefix','')}",
                    }
                )
        elif suf == ".zip":
            # Extract supported tabular/text assets from zip.
            try:
                with zipfile.ZipFile(path) as zf, tempfile.TemporaryDirectory() as td:
                    tmp_dir = Path(td)
                    for info in zf.infolist():
                        if info.is_dir():
                            continue
                        name = Path(info.filename).name
                        if not name:
                            continue
                        # skip huge binary blobs
                        if info.file_size and info.file_size > 200 * 1024 * 1024:
                            continue
                        out = tmp_dir / name
                        try:
                            out.write_bytes(zf.read(info))
                        except Exception:
                            continue
                        # Process extracted file as if it were a normal supplementary file.
                        # Recurse only one level to avoid zip bombs.
                        sub_paper = PaperRecord(
                            stem=paper.stem,
                            input_dir=paper.input_dir,
                            doi=paper.doi,
                            pmid=paper.pmid,
                            pmcid=paper.pmcid,
                            title=paper.title,
                            supplementary_dir=tmp_dir,
                        )
                        # Limit to this one file by calling helpers directly.
                        suf2 = out.suffix.lower()
                        if suf2 in (".csv", ".tsv"):
                            sep = "," if suf2 == ".csv" else "\t"
                            try:
                                df = pd.read_csv(out, sep=sep, dtype=str, keep_default_na=False)
                            except Exception:
                                continue
                            t = extract_tables_from_dataframe(
                                df,
                                paper=sub_paper,
                                tables_dir=tables_dir,
                                writer=writer,
                                exp_writer=exp_writer,
                                source_kind="supp_zip_table",
                                source_path=str(path),
                                source_ref_prefix=f"supp_file={path.name};zip_member={name}",
                                overwrite=overwrite,
                            )
                            if t is not None:
                                parsed_tables.append(t)
                        elif suf2 in (".xlsx", ".xls"):
                            try:
                                xls = pd.ExcelFile(out)
                            except Exception:
                                continue
                            for sheet in xls.sheet_names:
                                try:
                                    df = xls.parse(sheet_name=sheet, dtype=str, keep_default_na=False)
                                except Exception:
                                    continue
                                t = extract_tables_from_dataframe(
                                    df,
                                    paper=sub_paper,
                                    tables_dir=tables_dir,
                                    writer=writer,
                                    exp_writer=exp_writer,
                                    source_kind="supp_zip_table",
                                    source_path=str(path),
                                    source_ref_prefix=f"supp_file={path.name};zip_member={name};sheet={sheet}",
                                    overwrite=overwrite,
                                )
                                if t is not None:
                                    parsed_tables.append(t)
                        elif suf2 in (".fa", ".fasta", ".txt"):
                            try:
                                text = out.read_text(encoding="utf-8", errors="ignore")
                            except Exception:
                                continue
                            # Only treat as FASTA if it contains FASTA headers.
                            if ">" in text:
                                for seq in find_sequences(text, min_len=SEQUENCE_MIN_LEN_DEFAULT):
                                    writer.writerow(
                                        {
                                            "extracted_at": utc_now_iso(),
                                            "doi": paper.doi,
                                            "pmid": paper.pmid,
                                            "pmcid": paper.pmcid,
                                            "paper_stem": paper.stem,
                                            "title": paper.title,
                                            "source_kind": "supp_zip_fasta",
                                            "source_path": str(path),
                                            "source_ref": f"supp_file={path.name};zip_member={name}",
                                            "extraction_type": "sequence",
                                            "entity": seq,
                                            "numeric_value": "",
                                            "unit": "",
                                            "snippet": seq,
                                            "context": "",
                                        }
                                    )
                        else:
                            continue
            except Exception:
                continue
        elif suf == ".pdf":
            # Supplementary PDF (e.g., mmc1.pdf) can contain tables; do page-level text scan.
            if fitz is None:
                continue
            try:
                doc = fitz.open(str(path))
            except Exception:
                continue
            for page_idx in range(min(doc.page_count, 80)):
                try:
                    txt = doc.load_page(page_idx).get_text("text")
                except Exception:
                    continue
                for cond in find_conditions(txt):
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": "supp_pdf_text",
                            "source_path": str(path),
                            "source_ref": f"supp_file={path.name};page={page_idx+1}",
                            "extraction_type": "condition",
                            "entity": cond,
                            "numeric_value": "",
                            "unit": "",
                            "snippet": cond,
                            "context": "",
                        }
                    )
                for meas in find_measurements(txt):
                    writer.writerow(
                        {
                            "extracted_at": utc_now_iso(),
                            "doi": paper.doi,
                            "pmid": paper.pmid,
                            "pmcid": paper.pmcid,
                            "paper_stem": paper.stem,
                            "title": paper.title,
                            "source_kind": "supp_pdf_text",
                            "source_path": str(path),
                            "source_ref": f"supp_file={path.name};page={page_idx+1}",
                            "extraction_type": "endpoint_value",
                            "entity": meas.get("raw", ""),
                            "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                            "unit": meas.get("unit", ""),
                            "snippet": meas.get("raw", ""),
                            "context": f"prefix={meas.get('prefix','')}",
                        }
                    )
            try:
                doc.close()
            except Exception:
                pass

    # Cross-file experimental extraction (sequence table + assay table joins across supplementary assets)
    _ = emit_joined_experimental_records_from_tables(
        parsed_tables,
        paper=paper,
        exp_writer=exp_writer,
        source_path=str(supp_dir),
        include_computational=False,
    )


def extract_from_pdf(
    paper: PaperRecord,
    *,
    writer: csv.DictWriter,
    max_pages: int,
) -> None:
    if not paper.pdf_path or not paper.pdf_path.exists():
        return
    if fitz is None:
        return
    try:
        doc = fitz.open(str(paper.pdf_path))
    except Exception:
        return
    for page_idx in range(min(doc.page_count, max_pages)):
        try:
            txt = doc.load_page(page_idx).get_text("text")
        except Exception:
            continue

        for cond in find_conditions(txt):
            writer.writerow(
                {
                    "extracted_at": utc_now_iso(),
                    "doi": paper.doi,
                    "pmid": paper.pmid,
                    "pmcid": paper.pmcid,
                    "paper_stem": paper.stem,
                    "title": paper.title,
                    "source_kind": "pdf_text",
                    "source_path": str(paper.pdf_path),
                    "source_ref": f"page={page_idx+1}",
                    "extraction_type": "condition",
                    "entity": cond,
                    "numeric_value": "",
                    "unit": "",
                    "snippet": cond,
                    "context": "",
                }
            )

        for meas in find_measurements(txt):
            writer.writerow(
                {
                    "extracted_at": utc_now_iso(),
                    "doi": paper.doi,
                    "pmid": paper.pmid,
                    "pmcid": paper.pmcid,
                    "paper_stem": paper.stem,
                    "title": paper.title,
                    "source_kind": "pdf_text",
                    "source_path": str(paper.pdf_path),
                    "source_ref": f"page={page_idx+1}",
                    "extraction_type": "endpoint_value",
                    "entity": meas.get("raw", ""),
                    "numeric_value": meas.get("value", "") if meas.get("value") is not None else "",
                    "unit": meas.get("unit", ""),
                    "snippet": meas.get("raw", ""),
                    "context": f"prefix={meas.get('prefix','')}",
                }
            )

        low = (txt or "").lower()
        if any(k in low for k in THRESHOLD_KEYWORDS):
            for sent in split_sentences(txt):
                if not is_threshold_sentence(sent):
                    continue
                writer.writerow(
                    {
                        "extracted_at": utc_now_iso(),
                        "doi": paper.doi,
                        "pmid": paper.pmid,
                        "pmcid": paper.pmcid,
                        "paper_stem": paper.stem,
                        "title": paper.title,
                        "source_kind": "pdf_text",
                        "source_path": str(paper.pdf_path),
                        "source_ref": f"page={page_idx+1}",
                        "extraction_type": "threshold_text",
                        "entity": sent,
                        "numeric_value": "",
                        "unit": "",
                        "snippet": sent,
                        "context": "",
                    }
                )

    try:
        doc.close()
    except Exception:
        pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=str, required=True, help="Directory produced by fetch_open_access_papers.py")
    ap.add_argument("--out", type=str, default="", help="Output CSV path (default: <input-dir>/raw_extractions.csv)")
    ap.add_argument("--tables-dir", type=str, default="", help="Directory to write extracted tables (default: <input-dir>/extracted_tables)")
    ap.add_argument(
        "--experimental-out",
        type=str,
        default="",
        help="Output experimental records CSV path (default: <input-dir>/raw_experimental_records.csv)",
    )
    ap.add_argument("--max-field-len", type=int, default=2000, help="Max length for entity/snippet/context fields (0 disables)")
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs")
    ap.add_argument("--no-xml", dest="xml", action="store_false", help="Disable JATS XML extraction")
    ap.add_argument("--no-supp", dest="supp", action="store_false", help="Disable supplementary extraction")
    ap.add_argument("--no-pdf", dest="pdf", action="store_false", help="Disable PDF page-level scan")
    ap.add_argument("--no-experimental", dest="experimental", action="store_false", help="Disable row-level experimental record extraction")
    ap.add_argument(
        "--include-computational",
        action="store_true",
        help="Include tables that appear to be computational/prediction-only (default: excluded)",
    )
    ap.add_argument("--max-pdf-pages", type=int, default=25, help="Max pages to scan per main PDF")
    ap.set_defaults(xml=True, supp=True, pdf=True, experimental=True)
    args = ap.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"Input dir not found: {input_dir}", file=sys.stderr)
        return 2

    out_csv = Path(args.out) if args.out else (input_dir / "raw_extractions.csv")
    tables_dir = Path(args.tables_dir) if args.tables_dir else (input_dir / "extracted_tables")
    exp_csv = Path(args.experimental_out) if args.experimental_out else (input_dir / "raw_experimental_records.csv")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "extracted_at",
        "doi",
        "pmid",
        "pmcid",
        "paper_stem",
        "title",
        "source_kind",
        "source_path",
        "source_ref",
        "extraction_type",
        "entity",
        "numeric_value",
        "unit",
        "snippet",
        "context",
    ]

    exp_fieldnames = [
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
    ]

    mode = "w" if (args.overwrite or not out_csv.exists()) else "a"
    write_header = mode == "w"
    exp_mode = "w" if (args.overwrite or not exp_csv.exists()) else "a"
    exp_write_header = exp_mode == "w"

    papers = build_paper_records(input_dir)
    if not papers:
        print("No papers found (missing manifest and no *.xml files).", file=sys.stderr)
        return 1

    with ExitStack() as stack:
        f = stack.enter_context(out_csv.open(mode, encoding="utf-8", newline=""))
        writer = ClippingDictWriter(f, fieldnames=fieldnames, max_field_len=max(0, int(args.max_field_len)))
        if write_header:
            writer.writeheader()

        exp_writer: Optional[csv.DictWriter] = None
        if args.experimental:
            exp_f = stack.enter_context(exp_csv.open(exp_mode, encoding="utf-8", newline=""))
            exp_writer = ClippingDictWriter(exp_f, fieldnames=exp_fieldnames, max_field_len=max(0, int(args.max_field_len)))
            if exp_write_header:
                exp_writer.writeheader()

        for paper in papers:
            # Best-effort fill title/ids from XML early, because supplementary parsing benefits from it.
            if args.xml:
                extract_from_xml(
                    paper,
                    tables_dir=tables_dir,
                    writer=writer,
                    exp_writer=exp_writer,
                    overwrite=args.overwrite,
                    include_computational=bool(args.include_computational),
                )
            if args.supp:
                extract_from_supplementary(paper, tables_dir=tables_dir, writer=writer, exp_writer=exp_writer, overwrite=args.overwrite)
            if args.pdf:
                extract_from_pdf(paper, writer=writer, max_pages=max(1, int(args.max_pdf_pages)))

    print(f"Done. CSV: {out_csv}", file=sys.stderr)
    print(f"Tables: {tables_dir}", file=sys.stderr)
    if args.experimental:
        print(f"Experimental: {exp_csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
