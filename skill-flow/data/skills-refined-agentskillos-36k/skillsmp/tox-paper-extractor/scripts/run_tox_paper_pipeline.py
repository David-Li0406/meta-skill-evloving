#!/usr/bin/env python3
"""
End-to-end OA pipeline:
  Europe PMC discovery -> OA download (PDF/XML/supp) -> raw extraction -> Markdown report.

This is a thin orchestration wrapper around:
  - scripts/discover_epmc_experimental_papers.py
  - scripts/fetch_open_access_papers.py
  - scripts/extract_paper_extractions.py
  - scripts/make_extraction_report.py

It is intentionally OA-only and does not bypass paywalls.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


def safe_slug(text: str, max_len: int = 60) -> str:
    s = (text or "").strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "run"
    return s[:max_len]


def now_local_stamp() -> str:
    return datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")


def run_cmd(cmd: list[str], *, cwd: Path) -> None:
    print(f"[cmd] {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=str(cwd), check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", type=str, default="", help="Europe PMC query string (required unless --paper-ids provided)")
    ap.add_argument(
        "--paper-ids",
        type=str,
        default="",
        help="Path to an existing ids file (one DOI/PMID/PMCID per line). If set, discovery is skipped.",
    )
    ap.add_argument("--out-root", type=str, default="runs", help="Root directory to create a run folder under")
    ap.add_argument("--run-name", type=str, default="", help="Optional run folder name (default: timestamp + query slug)")
    ap.add_argument("--max-results", type=int, default=50, help="Discovery: max Europe PMC results to scan")
    ap.add_argument("--min-score", type=int, default=5, help="Discovery: minimum heuristic score to keep candidate")
    ap.add_argument("--download-timeout", type=int, default=45, help="Download: HTTP timeout seconds")
    ap.add_argument("--download-delay", type=float, default=0.5, help="Download: delay between items (seconds)")
    ap.add_argument("--max-file-mb", type=int, default=600, help="Download: max size per file in MB (0 disables)")
    ap.add_argument("--max-file-seconds", type=int, default=300, help="Download: max wall time per file in seconds (0 disables)")
    ap.add_argument("--unpaywall-email", type=str, default="", help="Optional Unpaywall email (improves OA PDF resolution)")
    ap.add_argument("--max-pdf-pages", type=int, default=10, help="Extraction: max PDF pages to scan per paper")
    ap.add_argument(
        "--include-computational",
        action="store_true",
        help="Extraction: include computational/prediction-only tables in raw_experimental_records.csv",
    )
    ap.add_argument(
        "--screen",
        action="store_true",
        help="Postprocess: run screen_experimental_records.py to add train-ready QC flags",
    )
    ap.add_argument(
        "--screen-min-seq-len",
        type=int,
        default=5,
        help="Postprocess: when --screen, pass --min-seq-len to screen_experimental_records.py (affects train_ready_* flags)",
    )
    ap.add_argument(
        "--augment-methods",
        action="store_true",
        help="Postprocess: run augment_records_with_methods.py to attach auditable method_* fields to records",
    )
    ap.add_argument(
        "--methods-taxonomy",
        action="store_true",
        help="Postprocess: run summarize_methods_taxonomy.py (requires --augment-methods outputs)",
    )
    ap.add_argument(
        "--summarize",
        action="store_true",
        help="Postprocess: run summarize_sample_run.py to write sample_metrics.{json,md} under papers/",
    )
    ap.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs inside the run directory")
    args = ap.parse_args()

    cwd = Path.cwd()
    out_root = (cwd / args.out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    ids_path: Path
    query = str(args.query or "").strip()
    if args.paper_ids:
        ids_path = Path(args.paper_ids).resolve()
        if not ids_path.exists():
            raise SystemExit(f"--paper-ids not found: {ids_path}")
        run_label = args.run_name.strip() or f"{now_local_stamp()}_from_ids"
    else:
        if not query:
            raise SystemExit("Either --query or --paper-ids is required.")
        run_label = args.run_name.strip() or f"{now_local_stamp()}_{safe_slug(query)}"
        ids_path = out_root / run_label / "paper_ids.txt"

    run_dir = out_root / run_label
    run_dir.mkdir(parents=True, exist_ok=True)

    # 1) Discover
    if not args.paper_ids:
        cand_csv = run_dir / "experimental_candidates.csv"
        ids_out = run_dir / "paper_ids.txt"
        run_cmd(
            [
                "python",
                "scripts/discover_epmc_experimental_papers.py",
                "--query",
                query,
                "--max-results",
                str(int(args.max_results)),
                "--min-score",
                str(int(args.min_score)),
                "--out",
                str(cand_csv),
                "--ids-out",
                str(ids_out),
            ],
            cwd=cwd,
        )
        ids_path = ids_out

    if not ids_path.exists() or not ids_path.read_text(encoding="utf-8", errors="ignore").strip():
        raise SystemExit(f"No ids found at: {ids_path}")

    # 2) Download OA artifacts
    papers_dir = run_dir / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)

    unpaywall_email = args.unpaywall_email.strip() or os.environ.get("UNPAYWALL_EMAIL", "").strip()
    fetch_cmd = [
        "python",
        "scripts/fetch_open_access_papers.py",
        "--input",
        str(ids_path),
        "--out",
        str(papers_dir),
        "--format",
        "both",
        "--supplementary",
        "--timeout",
        str(int(args.download_timeout)),
        "--delay",
        str(float(args.download_delay)),
        "--max-file-mb",
        str(int(args.max_file_mb)),
        "--max-file-seconds",
        str(int(args.max_file_seconds)),
    ]
    if unpaywall_email:
        fetch_cmd.extend(["--unpaywall-email", unpaywall_email])
    if args.overwrite:
        fetch_cmd.append("--overwrite")
    run_cmd(fetch_cmd, cwd=cwd)

    # 3) Extract
    extract_cmd = [
        "python",
        "scripts/extract_paper_extractions.py",
        "--input-dir",
        str(papers_dir),
        "--max-pdf-pages",
        str(int(args.max_pdf_pages)),
    ]
    if args.overwrite:
        extract_cmd.append("--overwrite")
    if args.include_computational:
        extract_cmd.append("--include-computational")
    run_cmd(extract_cmd, cwd=cwd)

    # 4) Report
    report_cmd = [
        "python",
        "scripts/make_extraction_report.py",
        "--input-dir",
        str(papers_dir),
    ]
    if args.overwrite:
        report_cmd.extend(["--out", str(papers_dir / "extraction_report.md")])
    run_cmd(report_cmd, cwd=cwd)

    # 5) Screening (optional)
    if args.screen:
        run_cmd(
            [
                "python",
                "scripts/screen_experimental_records.py",
                "--input-dir",
                str(papers_dir),
                "--min-seq-len",
                str(int(args.screen_min_seq_len)),
            ],
            cwd=cwd,
        )

    # 6) Method augmentation + taxonomy (optional)
    if args.augment_methods:
        run_cmd(["python", "scripts/augment_records_with_methods.py", "--papers-dir", str(papers_dir)], cwd=cwd)
        if args.methods_taxonomy:
            run_cmd(["python", "scripts/summarize_methods_taxonomy.py", "--papers-dir", str(papers_dir)], cwd=cwd)

    # 7) Sample metrics summary (optional)
    if args.summarize:
        run_cmd(["python", "scripts/summarize_sample_run.py", "--papers-dir", str(papers_dir)], cwd=cwd)

    print("")
    print("[done] run_dir:", run_dir)
    print("[done] papers_dir:", papers_dir)
    print("[done] experimental_records:", papers_dir / "raw_experimental_records.csv")
    print("[done] report:", papers_dir / "extraction_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
