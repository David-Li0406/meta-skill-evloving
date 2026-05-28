#!/usr/bin/env python3
"""
Freeze a small, deterministic worklist of papers for downstream per-paper analysis.

Selection priority (highest first):
  1) Has supplementary files (papers/supplementary/<ID>/**)
  2) Has main PDF (papers/<ID>.pdf)
  3) Has PMC OA package (papers/pmc_oa_packages/<ID>.tar.gz)
  4) Otherwise: has XML only (papers/<ID>.xml)

This is designed for PMCID-centric runs (IDs like PMC1234567), but will work for any
ID that follows the same naming convention in the papers directory.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class PaperMaterial:
    paper_id: str
    has_xml: bool
    has_pdf: bool
    supp_file_count: int
    has_oa_package: bool

    @property
    def score(self) -> int:
        # Prefer supplementary (often holds extra tables/FASTA/XLSX), then main PDF.
        return (100 if self.supp_file_count > 0 else 0) + (10 if self.has_pdf else 0) + (1 if self.has_oa_package else 0)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def count_files_recursively(root: Path) -> int:
    if not root.exists() or not root.is_dir():
        return 0
    return sum(1 for p in root.rglob("*") if p.is_file())


def detect_papers(papers_dir: Path) -> dict[str, PaperMaterial]:
    materials: dict[str, PaperMaterial] = {}

    # Start from XMLs (authoritative list for PMCID runs)
    for xml_path in sorted(papers_dir.glob("*.xml")):
        paper_id = xml_path.stem
        materials[paper_id] = PaperMaterial(
            paper_id=paper_id,
            has_xml=True,
            has_pdf=(papers_dir / f"{paper_id}.pdf").exists(),
            supp_file_count=count_files_recursively(papers_dir / "supplementary" / paper_id),
            has_oa_package=(papers_dir / "pmc_oa_packages" / f"{paper_id}.tar.gz").exists(),
        )

    # Include any PDFs that exist without XML (rare, but handle it)
    for pdf_path in sorted(papers_dir.glob("*.pdf")):
        paper_id = pdf_path.stem
        if paper_id in materials:
            continue
        materials[paper_id] = PaperMaterial(
            paper_id=paper_id,
            has_xml=(papers_dir / f"{paper_id}.xml").exists(),
            has_pdf=True,
            supp_file_count=count_files_recursively(papers_dir / "supplementary" / paper_id),
            has_oa_package=(papers_dir / "pmc_oa_packages" / f"{paper_id}.tar.gz").exists(),
        )

    return materials


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers-dir", type=str, required=True, help="Run papers directory, e.g. runs/<run>/papers")
    ap.add_argument("--n", type=int, default=30, help="How many paper IDs to freeze")
    ap.add_argument("--out", type=str, default="analysis/worklist_30.txt", help="Output worklist path")
    ap.add_argument(
        "--meta-out",
        type=str,
        default="analysis/worklist_30.meta.json",
        help="Output metadata path (JSON)",
    )
    args = ap.parse_args()

    papers_dir = Path(args.papers_dir).resolve()
    if not papers_dir.exists():
        raise SystemExit(f"--papers-dir not found: {papers_dir}")

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    meta_out = Path(args.meta_out).resolve()
    meta_out.parent.mkdir(parents=True, exist_ok=True)

    materials = detect_papers(papers_dir)
    if not materials:
        raise SystemExit(f"No papers detected under: {papers_dir}")

    ranked = sorted(materials.values(), key=lambda m: (-m.score, m.paper_id))
    selected = ranked[: max(0, int(args.n))]

    out_path.write_text("\n".join(m.paper_id for m in selected) + "\n", encoding="utf-8")

    meta = {
        "generated_at": now_iso(),
        "papers_dir": str(papers_dir),
        "requested_n": int(args.n),
        "selected_n": len(selected),
        "selected_with_pdf": sum(1 for m in selected if m.has_pdf),
        "selected_with_supp_files": sum(1 for m in selected if m.supp_file_count > 0),
        "selected_with_oa_package": sum(1 for m in selected if m.has_oa_package),
        "note": (
            "If selected_with_pdf+selected_with_supp_files is low, PDF/supplementary downloads may still be running. "
            "Re-run this script later to refresh a new snapshot."
        ),
        "items": [asdict(m) | {"score": m.score} for m in selected],
    }
    meta_out.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ok] wrote: {out_path}")
    print(f"[ok] wrote: {meta_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

