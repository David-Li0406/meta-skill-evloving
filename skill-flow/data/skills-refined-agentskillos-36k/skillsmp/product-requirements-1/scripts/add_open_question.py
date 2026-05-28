#!/usr/bin/env python3

"""Record an open question (repo-scoped).

The Skill (Claude) should use this to persist uncertainties instead of losing them in chat.
Open questions appear in product/views/OPEN_QUESTIONS.md after view compilation.
"""

import argparse
from pathlib import Path

from compile_views import compile_views
from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


def main() -> None:
    parser = argparse.ArgumentParser(description="Add an open question")
    parser.add_argument(
        "--scope",
        default="product",
        choices=["product", "requirement"],
        help="Question scope",
    )
    parser.add_argument(
        "--ref", default="product", help="Scope ref: 'product' or a req id like R-001"
    )
    parser.add_argument("--question", required=True, help="The unresolved question")
    parser.add_argument(
        "--severity",
        default="medium",
        choices=["low", "medium", "high"],
        help="Severity",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    views_dir = skill_root / "product" / "views"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    scope_ref = args.ref.strip() or ("product" if args.scope == "product" else "")
    q = args.question.strip()
    if not q:
        raise SystemExit("--question cannot be empty")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO open_question (scope_type, scope_ref, question, severity) VALUES (?, ?, ?, ?);",
        (args.scope, scope_ref, q, args.severity),
    )
    conn.commit()
    conn.close()

    compile_views(db_path=db_path, views_dir=views_dir)
    print("Recorded open question.")


if __name__ == "__main__":
    main()
