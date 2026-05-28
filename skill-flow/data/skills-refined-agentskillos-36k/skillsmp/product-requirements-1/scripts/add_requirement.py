#!/usr/bin/env python3

"""Add a requirement (repo-scoped).

This is a v1 scaffold:

- Writes to product/memory.sqlite (inside the skill folder)
- Regenerates views under product/views/

Question generation and rich view compilation are intentionally minimal in v1.
"""

import argparse
from pathlib import Path

from compile_views import compile_views
from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


def _next_req_id(cur: sqlite3.Cursor) -> str:
    """Allocate the next human-friendly requirement id.

    Uses the last inserted requirement's req_id if present; otherwise starts at 001.
    This avoids collisions if requirements are ever deleted.
    """
    cur.execute("SELECT req_id FROM requirement ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()
    if not row or not row[0]:
        return "R-001"
    last = str(row[0])
    try:
        n = int(last.split("-")[-1])
    except Exception:
        n = 0
    return f"R-{n + 1:03d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a requirement (repo-scoped)")
    parser.add_argument("--description", required=True, help="Requirement idea")
    parser.add_argument("--title", default="", help="Optional short title")
    parser.add_argument(
        "--priority", default="P2", choices=["P0", "P1", "P2"], help="Initial priority"
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    views_dir = skill_root / "product" / "views"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    title = (args.title or args.description).strip()
    title = title.replace("\n", " ")[:60]
    description = args.description.strip()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    req_id = _next_req_id(cur)
    cur.execute(
        "INSERT INTO requirement (req_id, title, description, status, priority) VALUES (?, ?, ?, 'PROPOSED', ?);",
        (req_id, title, description, args.priority),
    )
    conn.commit()
    conn.close()

    compile_views(db_path=db_path, views_dir=views_dir)

    print(f"Added requirement {req_id} (status=PROPOSED, priority={args.priority})")


if __name__ == "__main__":
    main()
