#!/usr/bin/env python3

"""Record a design decision (repo-scoped).

Decisions are durable memory. The Skill (Claude) should write decisions whenever a
key ambiguity is resolved or a trade-off is chosen.

This script records the decision in SQLite. Views do not currently render decisions
to keep the compiled artifacts short, but they remain queryable via SQL.
"""

import argparse
from pathlib import Path

from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a design decision")
    parser.add_argument(
        "--scope",
        default="product",
        choices=["product", "requirement"],
        help="Decision scope",
    )
    parser.add_argument(
        "--ref", default="product", help="Scope ref: 'product' or a req id like R-001"
    )
    parser.add_argument("--question", required=True, help="The question being answered")
    parser.add_argument("--choice", required=True, help="The chosen answer")
    parser.add_argument("--rationale", default="", help="Why this choice was made")
    parser.add_argument(
        "--confidence", type=float, default=0.7, help="0..1 confidence (default 0.7)"
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    scope_ref = args.ref.strip() or ("product" if args.scope == "product" else "")
    q = args.question.strip()
    c = args.choice.strip()
    r = args.rationale.strip()
    conf = float(args.confidence)
    if conf < 0.0:
        conf = 0.0
    if conf > 1.0:
        conf = 1.0

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO decision (scope_type, scope_ref, question, choice, rationale, confidence) VALUES (?, ?, ?, ?, ?, ?);",
        (args.scope, scope_ref, q, c, r, conf),
    )
    conn.commit()
    conn.close()

    print("Recorded decision.")


if __name__ == "__main__":
    main()
