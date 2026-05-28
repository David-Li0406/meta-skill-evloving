#!/usr/bin/env python3
"""
Create a per-paper task queue under docs/analysis/ for multi-worker processing.

Design:
  - Each task is a single JSON file: analysis/queue/pending/<paper_id>.json
  - Workers atomically claim tasks by mv -> analysis/queue/in_progress/
  - Outputs are one-paper-per-file: analysis/per_paper/<paper_id>.json + .md
  - Completed tasks are moved to analysis/queue/done/ (or failed/)
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def atomic_write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_worklist(path: Path) -> list[str]:
    ids: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        ids.append(s)
    # Preserve order; de-dup in-order
    seen: set[str] = set()
    out: list[str] = []
    for x in ids:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def task_exists_anywhere(queue_dir: Path, task_name: str) -> bool:
    for sub in ("pending", "in_progress", "done", "failed"):
        if (queue_dir / sub / task_name).exists():
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worklist", type=str, default="analysis/worklist_30.txt", help="Path to worklist txt")
    ap.add_argument("--papers-dir", type=str, required=True, help="Run papers directory, e.g. runs/<run>/papers")
    ap.add_argument("--analysis-dir", type=str, default="analysis", help="Analysis root directory")
    ap.add_argument("--overwrite-pending", action="store_true", help="Overwrite tasks that already exist in pending/")
    args = ap.parse_args()

    worklist_path = Path(args.worklist).resolve()
    if not worklist_path.exists():
        raise SystemExit(f"--worklist not found: {worklist_path}")
    papers_dir = Path(args.papers_dir).resolve()
    if not papers_dir.exists():
        raise SystemExit(f"--papers-dir not found: {papers_dir}")

    analysis_dir = Path(args.analysis_dir).resolve()
    queue_dir = analysis_dir / "queue"
    for sub in ("pending", "in_progress", "done", "failed"):
        (queue_dir / sub).mkdir(parents=True, exist_ok=True)
    (analysis_dir / "per_paper").mkdir(parents=True, exist_ok=True)

    ids = load_worklist(worklist_path)
    if not ids:
        raise SystemExit(f"No IDs found in worklist: {worklist_path}")

    created = 0
    skipped = 0
    overwritten = 0

    for paper_id in ids:
        task_name = f"{paper_id}.json"
        dst = queue_dir / "pending" / task_name

        if dst.exists() and args.overwrite_pending:
            overwritten += 1
        elif task_exists_anywhere(queue_dir, task_name):
            skipped += 1
            continue

        xml_path = papers_dir / f"{paper_id}.xml"
        pdf_path = papers_dir / f"{paper_id}.pdf"
        supp_dir = papers_dir / "supplementary" / paper_id
        oa_pkg = papers_dir / "pmc_oa_packages" / f"{paper_id}.tar.gz"

        task = {
            "paper_id": paper_id,
            "created_at": now_iso(),
            "status": "pending",
            "run_papers_dir": str(papers_dir),
            "materials": {
                "xml_path": str(xml_path) if xml_path.exists() else "",
                "pdf_path": str(pdf_path) if pdf_path.exists() else "",
                "supp_dir": str(supp_dir) if supp_dir.exists() else "",
                "oa_package_path": str(oa_pkg) if oa_pkg.exists() else "",
            },
            "artifacts": {
                "extracted_tables_glob": str(papers_dir / "extracted_tables" / f"{paper_id}_*"),
                "raw_experimental_records_csv": str(papers_dir / "raw_experimental_records.csv"),
                "raw_extractions_csv": str(papers_dir / "raw_extractions.csv"),
                "screened_experimental_records_csv": str(papers_dir / "screened_experimental_records.csv"),
            },
            "outputs": {
                "per_paper_json": str(analysis_dir / "per_paper" / f"{paper_id}.json"),
                "per_paper_md": str(analysis_dir / "per_paper" / f"{paper_id}.md"),
            },
        }

        atomic_write_json(dst, task)
        created += 1

    print(f"[ok] queue: {queue_dir}")
    print(f"[ok] worklist: {worklist_path} ({len(ids)} ids)")
    print(f"[ok] created: {created}, skipped: {skipped}, overwritten_pending: {overwritten}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

