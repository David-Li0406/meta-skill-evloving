#!/usr/bin/env python3

"""Refine a requirement (repo-scoped).

This is a v1 helper that applies explicit updates supplied on the CLI.

The Skill (Claude) is expected to do the interactive clarification. After the
user answers, use this script to persist the updated fields and acceptance
criteria.
"""

import argparse
from pathlib import Path

from compile_views import compile_views
from sqlite_support import load_sqlite_with_fts

sqlite_env = load_sqlite_with_fts()
sqlite3 = sqlite_env.sqlite


def main() -> None:
    parser = argparse.ArgumentParser(description="Refine a requirement (repo-scoped)")
    parser.add_argument("--id", required=True, help="Requirement ID, e.g., R-001")
    parser.add_argument("--title", default="", help="New title")
    parser.add_argument("--description", default="", help="New description")
    parser.add_argument(
        "--priority", default="", choices=["", "P0", "P1", "P2"], help="New priority"
    )
    parser.add_argument(
        "--status",
        default="",
        choices=["", "PROPOSED", "READY", "DONE"],
        help="New status",
    )
    parser.add_argument(
        "--add-accept",
        action="append",
        default=[],
        help="Add one acceptance criterion (repeatable)",
    )
    parser.add_argument(
        "--accept-type",
        default="CHECKLIST",
        choices=["CHECKLIST", "GWT"],
        help="Acceptance type",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    views_dir = skill_root / "product" / "views"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM requirement WHERE req_id = ?;", (args.id,))
    row = cur.fetchone()
    if not row:
        raise SystemExit(f"Requirement not found: {args.id}")
    req_db_id = int(row[0])

    updates = []
    params = []
    if args.title:
        updates.append("title = ?")
        params.append(args.title.strip())
    if args.description:
        updates.append("description = ?")
        params.append(args.description.strip())
    if args.priority:
        updates.append("priority = ?")
        params.append(args.priority)
    if args.status:
        updates.append("status = ?")
        params.append(args.status)
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        sql = "UPDATE requirement SET " + ", ".join(updates) + " WHERE id = ?;"
        params.append(req_db_id)
        cur.execute(sql, tuple(params))

    for item in args.add_accept:
        text = item.strip()
        if text:
            cur.execute(
                "INSERT INTO acceptance (requirement_id, text, type) VALUES (?, ?, ?);",
                (req_db_id, text, args.accept_type),
            )

    conn.commit()
    conn.close()

    compile_views(db_path=db_path, views_dir=views_dir)
    print(f"Updated {args.id}. Added acceptance items: {len(args.add_accept)}")


if __name__ == "__main__":
    main()
