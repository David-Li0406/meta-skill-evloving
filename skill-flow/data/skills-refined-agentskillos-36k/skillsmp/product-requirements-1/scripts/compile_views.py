#!/usr/bin/env python3

"""Compile human-readable Markdown views from the SQLite database.

Design intent
- The database is the authoritative store.
- Views are derived artifacts for quick human review.
- This script is deterministic and idempotent.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


@dataclass(frozen=True)
class RequirementRow:
    req_id: str
    title: str
    description: str
    status: str
    priority: str


def _load_meta(cur: sqlite3.Cursor) -> Dict[str, str]:
    cur.execute("SELECT key, value FROM meta;")
    return {k: (v or "") for (k, v) in cur.fetchall()}


def _load_requirements(cur: sqlite3.Cursor) -> List[RequirementRow]:
    cur.execute(
        "SELECT req_id, title, description, status, priority FROM requirement ORDER BY id ASC;"
    )
    return [RequirementRow(*row) for row in cur.fetchall()]


def _load_acceptance(cur: sqlite3.Cursor) -> Dict[str, List[str]]:
    # Map req_id -> acceptance list
    cur.execute(
        """
        SELECT r.req_id, a.text
        FROM acceptance a
        JOIN requirement r ON r.id = a.requirement_id
        ORDER BY r.id ASC, a.id ASC;
        """
    )
    out: Dict[str, List[str]] = {}
    for req_id, text in cur.fetchall():
        out.setdefault(req_id, []).append(text)
    return out


def _load_open_questions(cur: sqlite3.Cursor) -> List[Tuple[str, str, str]]:
    # (scope_type, scope_ref, question)
    cur.execute(
        "SELECT scope_type, scope_ref, question FROM open_question WHERE resolved_by_decision_id IS NULL ORDER BY id ASC;"
    )
    return [(a or "", b or "", c or "") for (a, b, c) in cur.fetchall()]


def compile_views(db_path: Path, views_dir: Path) -> None:
    views_dir.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    meta = _load_meta(cur)
    reqs = _load_requirements(cur)
    acc = _load_acceptance(cur)
    openqs = _load_open_questions(cur)
    conn.close()

    title = meta.get("title") or "(Untitled Product)"
    vision = meta.get("vision") or "TBD"
    constraints = meta.get("constraints") or ""

    # PRODUCT.md
    product_md = views_dir / "PRODUCT.md"
    lines: List[str] = [f"# {title}", "", f"**Vision**: {vision}", ""]
    if constraints.strip():
        lines += ["## Constraints", "", constraints.strip(), ""]
    lines += [
        "## Where to edit",
        "",
        "- Add/refine requirements via the skill operations.",
        "- This file is compiled from the SQLite database.",
        "",
    ]
    product_md.write_text("\n".join(lines), encoding="utf-8")

    # BACKLOG.md
    backlog_md = views_dir / "BACKLOG.md"
    lines = ["# Backlog", "", "Summary list:", ""]
    if not reqs:
        lines += ["(No requirements yet)", ""]
    else:
        for r in reqs:
            summary = (r.description or "").strip().replace("\n", " ")
            summary = summary[:120] + ("…" if len(summary) > 120 else "")
            lines.append(
                f"- `{r.req_id}` [{r.status}, {r.priority}] {r.title} — {summary}"
            )
        lines.append("")

        lines.append("## Details")
        lines.append("")
        for r in reqs:
            lines += [
                f"### {r.req_id}: {r.title}",
                "",
                (r.description or "").strip() or "(No description)",
                "",
            ]
            items = acc.get(r.req_id, [])
            lines.append("**Acceptance Criteria**:")
            lines.append("")
            if items:
                lines += [f"- {t}" for t in items]
            else:
                lines.append("- (None yet)")
            lines += [
                "",
                f"**Status**: {r.status}",
                "",
                f"**Priority**: {r.priority}",
                "",
            ]
    backlog_md.write_text("\n".join(lines), encoding="utf-8")

    # OPEN_QUESTIONS.md
    openq_md = views_dir / "OPEN_QUESTIONS.md"
    lines = ["# Open Questions", ""]
    if not openqs:
        lines.append("(No open questions)")
    else:
        prod = [q for q in openqs if q[0] == "product"]
        by_req = [q for q in openqs if q[0] == "requirement"]
        if prod:
            lines += ["## Product", ""]
            for _, _, q in prod:
                lines.append(f"- {q}")
            lines.append("")
        if by_req:
            lines += ["## Requirements", ""]
            # Group by scope_ref
            grouped: Dict[str, List[str]] = {}
            for _, scope_ref, q in by_req:
                grouped.setdefault(scope_ref or "(unknown)", []).append(q)
            for scope_ref in sorted(grouped.keys()):
                lines.append(f"### {scope_ref}")
                lines.append("")
                for q in grouped[scope_ref]:
                    lines.append(f"- {q}")
                lines.append("")
    openq_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Compile Markdown views")
    parser.add_argument(
        "--db", default="", help="Path to SQLite db (default: product/memory.sqlite)"
    )
    parser.add_argument(
        "--views", default="", help="Path to views dir (default: product/views)"
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = Path(args.db) if args.db else (skill_root / "product" / "memory.sqlite")
    views_dir = Path(args.views) if args.views else (skill_root / "product" / "views")
    compile_views(db_path=db_path, views_dir=views_dir)


if __name__ == "__main__":
    main()
