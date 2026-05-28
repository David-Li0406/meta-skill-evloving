#!/usr/bin/env python3

"""Query current product design state (repo-scoped).

Reads product/memory.sqlite (inside the skill folder) and prints a compact summary suitable for
copying into a conversation.
"""

import argparse
from pathlib import Path

from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


def _meta(cur: sqlite3.Cursor) -> dict:
    cur.execute("SELECT key, value FROM meta;")
    return {k: v for (k, v) in cur.fetchall()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Query product state (repo-scoped)")
    parser.add_argument("--full", action="store_true", help="Include open questions")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    meta = _meta(cur)
    title = meta.get("title") or "(Untitled Product)"
    vision = meta.get("vision") or "TBD"

    print(f"# {title}")
    print(f"Vision: {vision}")
    print("\n## Requirements")

    cur.execute(
        "SELECT req_id, title, status, priority FROM requirement ORDER BY req_id;"
    )
    rows = cur.fetchall()
    if not rows:
        print("No requirements recorded.")
    else:
        for req_id, rtitle, status, priority in rows:
            print(f"- {req_id}: {rtitle} ({status}, {priority})")

    if args.full:
        print("\n## Open questions")
        cur.execute(
            "SELECT scope_type, scope_ref, severity, question FROM open_question ORDER BY created_at;"
        )
        qs = cur.fetchall()
        if not qs:
            print("No open questions.")
        else:
            for scope_type, scope_ref, severity, q in qs:
                scope = (
                    scope_type
                    if scope_ref in ("", None)
                    else f"{scope_type}:{scope_ref}"
                )
                print(f"- [{severity}] {scope}: {q}")

    conn.close()


if __name__ == "__main__":
    main()
