#!/usr/bin/env python3
"""
Filter NCBI PMC OA file list (oa_file_list.txt / oa_file_list.csv) by a set of IDs.

Primary use:
  - Download oa_file_list.txt (~778MB) once
  - Intersect it with your topic-specific PMCID list (e.g. toxicity/AMP candidate PMCIDs)
  - Produce a small, auditable subset mapping:
      PMCID -> oa_package relative path -> full URL -> license

This avoids per-PMCID oa.fcgi lookups when you already have PMCIDs in bulk.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path


PMCID_RE = re.compile(r"^PMC\d+$", flags=re.IGNORECASE)


def normalize_pmcid(raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        return ""
    s = s.replace("PMCID:", "").strip()
    if s.isdigit():
        s = f"PMC{s}"
    if PMCID_RE.match(s):
        return s.upper()
    return s


def load_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.add(normalize_pmcid(line))
    ids.discard("")
    return ids


def detect_format(path: Path) -> str:
    name = path.name.lower()
    if name.endswith(".csv"):
        return "csv"
    return "txt"


def parse_txt_line(line: str) -> tuple[str, str, str, str, str] | None:
    """
    Returns: (rel_path, citation, pmcid, pmid, license)
    """
    parts = line.rstrip("\n").split("\t")
    if len(parts) < 3:
        return None
    rel_path = parts[0].strip()
    citation = parts[1].strip() if len(parts) > 1 else ""
    pmcid = parts[2].strip() if len(parts) > 2 else ""
    pmid = ""
    license_text = parts[-1].strip() if parts else ""
    for p in parts:
        if p.startswith("PMID:"):
            pmid = p.replace("PMID:", "").strip()
            break
    return rel_path, citation, pmcid, pmid, license_text


def iter_rows(oa_file_list: Path, fmt: str):
    if fmt == "csv":
        with oa_file_list.open("r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rel_path = (row.get("File") or "").strip()
                citation = (row.get("Article Citation") or "").strip()
                pmcid = (row.get("Accession ID") or "").strip()
                pmid = (row.get("PMID") or "").strip()
                license_text = (row.get("License") or "").strip()
                if not rel_path or not pmcid:
                    continue
                yield rel_path, citation, pmcid, pmid, license_text
        return

    # txt: first line is a timestamp, then tab-separated fields
    with oa_file_list.open("r", encoding="utf-8", errors="ignore") as f:
        first = True
        for line in f:
            if first:
                first = False
                # Timestamp line, e.g. "2026-01-17 13:27:38"
                if re.match(r"^\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2}$", line.strip()):
                    continue
            if not line.strip():
                continue
            parsed = parse_txt_line(line)
            if not parsed:
                continue
            yield parsed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oa-file-list", type=str, required=True, help="Path to oa_file_list.txt or oa_file_list.csv")
    ap.add_argument("--ids", type=str, required=True, help="Path to IDs file (one PMCID per line)")
    ap.add_argument("--out", type=str, required=True, help="Output TSV path")
    ap.add_argument("--missing-out", type=str, default="", help="Optional path to write missing PMCIDs")
    ap.add_argument("--base-url", type=str, default="https://ftp.ncbi.nlm.nih.gov/pub/pmc/", help="Base URL for oa_package paths")
    ap.add_argument(
        "--license-allow",
        type=str,
        default="",
        help="Comma-separated allowlist of license labels (e.g., 'CC BY,CC0'). Empty means allow all.",
    )
    args = ap.parse_args()

    oa_path = Path(args.oa_file_list).resolve()
    ids_path = Path(args.ids).resolve()
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not oa_path.exists():
        raise SystemExit(f"--oa-file-list not found: {oa_path}")
    if not ids_path.exists():
        raise SystemExit(f"--ids not found: {ids_path}")

    wanted = load_ids(ids_path)
    if not wanted:
        raise SystemExit(f"No PMCIDs found in: {ids_path}")

    license_allow: set[str] = set()
    if str(args.license_allow or "").strip():
        license_allow = {x.strip() for x in str(args.license_allow).split(",") if x.strip()}

    fmt = detect_format(oa_path)

    found: dict[str, dict] = {}
    lic_counter = Counter()

    for rel_path, citation, pmcid_raw, pmid, lic in iter_rows(oa_path, fmt):
        pmcid = normalize_pmcid(pmcid_raw)
        if pmcid not in wanted:
            continue
        if license_allow and lic not in license_allow:
            continue

        url = args.base_url.rstrip("/") + "/" + rel_path.lstrip("/")
        found[pmcid] = {
            "pmcid": pmcid,
            "pmid": pmid,
            "license": lic,
            "rel_path": rel_path,
            "url": url,
            "citation": citation,
        }
        lic_counter[lic] += 1

    missing = sorted(wanted - set(found.keys()))

    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["pmcid", "pmid", "license", "rel_path", "url", "citation"])
        for pmcid in sorted(found.keys()):
            r = found[pmcid]
            w.writerow([r["pmcid"], r["pmid"], r["license"], r["rel_path"], r["url"], r["citation"]])

    if args.missing_out:
        miss_path = Path(args.missing_out).resolve()
        miss_path.parent.mkdir(parents=True, exist_ok=True)
        miss_path.write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")

    print(f"[ok] wanted={len(wanted)} found={len(found)} missing={len(missing)}")
    print(f"[ok] wrote: {out_path}")
    if args.missing_out:
        print(f"[ok] wrote missing: {Path(args.missing_out).resolve()}")
    if lic_counter:
        print("[info] found license distribution (top 10):")
        for lic, n in lic_counter.most_common(10):
            print(f"  {n}\t{lic}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

