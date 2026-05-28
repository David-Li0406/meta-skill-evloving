#!/usr/bin/env python3
"""Full-text search across product requirements, decisions, and open questions.

Uses SQLite FTS5 for fast semantic-like queries. Supports searching across
multiple scopes (requirement, decision, question) or a specific one.

For better multilingual search (e.g., CJK languages), queries are automatically
converted to prefix matching (e.g., "pay" -> "pay*").

Usage examples:
    python scripts/search.py --query "payment"
    python scripts/search.py --query "payment" --scope requirement
    python scripts/search.py --query "why change" --scope decision
"""

import argparse
import os
import sqlite3 as sqlite3_types
from pathlib import Path
from typing import List, Tuple

from sqlite_support import load_sqlite_with_fts

MODE_CHOICES = ("auto", "fts", "like")

sqlite_env = load_sqlite_with_fts()
runtime_sqlite = sqlite_env.sqlite


def _prepare_fts_query(query: str) -> str:
    """Prepare FTS5 query by adding prefix wildcard for better Chinese matching."""
    tokens = query.split()
    processed = []
    for token in tokens:
        if token.startswith('"') or token in ("AND", "OR", "NOT"):
            processed.append(token)
        elif token.endswith("*"):
            processed.append(token)
        else:
            processed.append(f"{token}*")
    return " ".join(processed)


def _like_pattern(query: str) -> str:
    stripped = query.strip()
    return f"%{stripped}%" if stripped else "%"


def _search_requirements(
    cur: sqlite3_types.Cursor, query: str, fts_enabled: bool
) -> List[Tuple[str, str, str, str, str]]:
    """Search requirements using FTS5 or LIKE fallback."""
    if fts_enabled:
        prepared_query = _prepare_fts_query(query)
        sql = """
            SELECT r.req_id, r.title, r.description, r.status, r.priority
            FROM requirement_fts
            JOIN requirement r ON r.id = requirement_fts.rowid
            WHERE requirement_fts MATCH ?;
        """
        cur.execute(sql, (prepared_query,))
        rows = cur.fetchall()
        if rows:
            return rows

    pattern = _like_pattern(query)
    sql = """
        SELECT req_id, title, description, status, priority
        FROM requirement
        WHERE LOWER(title) LIKE LOWER(?)
           OR LOWER(description) LIKE LOWER(?)
        ORDER BY req_id;
    """
    cur.execute(sql, (pattern, pattern))
    return cur.fetchall()


def _search_decisions(
    cur: sqlite3_types.Cursor, query: str, fts_enabled: bool
) -> List[Tuple[str, str, str, str, str, float]]:
    """Search decisions using FTS5 or LIKE fallback."""
    if fts_enabled:
        prepared_query = _prepare_fts_query(query)
        sql = """
            SELECT d.scope_type, d.scope_ref, d.question, d.choice, d.rationale, d.confidence
            FROM decision_fts
            JOIN decision d ON d.id = decision_fts.rowid
            WHERE decision_fts MATCH ?;
        """
        cur.execute(sql, (prepared_query,))
        rows = cur.fetchall()
        if rows:
            return rows

    pattern = _like_pattern(query)
    sql = """
        SELECT scope_type, scope_ref, question, choice, rationale, confidence
        FROM decision
        WHERE LOWER(question) LIKE LOWER(?)
           OR LOWER(choice) LIKE LOWER(?)
           OR LOWER(rationale) LIKE LOWER(?)
        ORDER BY created_at DESC;
    """
    cur.execute(sql, (pattern, pattern, pattern))
    return cur.fetchall()


def _search_questions(
    cur: sqlite3_types.Cursor, query: str, fts_enabled: bool
) -> List[Tuple[str, str, str, str]]:
    """Search open questions using FTS5 or LIKE fallback."""
    if fts_enabled:
        prepared_query = _prepare_fts_query(query)
        sql = """
            SELECT q.scope_type, q.scope_ref, q.question, q.severity
            FROM open_question_fts
            JOIN open_question q ON q.id = open_question_fts.rowid
            WHERE open_question_fts MATCH ?;
        """
        cur.execute(sql, (prepared_query,))
        rows = cur.fetchall()
        if rows:
            return rows

    pattern = _like_pattern(query)
    sql = """
        SELECT scope_type, scope_ref, question, severity
        FROM open_question
        WHERE LOWER(question) LIKE LOWER(?)
        ORDER BY created_at DESC;
    """
    cur.execute(sql, (pattern,))
    return cur.fetchall()


def main() -> None:
    parser = argparse.ArgumentParser(description="Full-text search across product data")
    parser.add_argument(
        "--query", required=True, help="Search query (FTS5 MATCH syntax)"
    )
    parser.add_argument(
        "--scope",
        choices=["requirement", "decision", "question", "all"],
        default="all",
        help="Scope to search (default: all)",
    )
    parser.add_argument(
        "--mode",
        choices=MODE_CHOICES,
        default="auto",
        help="Search backend: auto-detect, force FTS5, or force LIKE fallback",
    )
    args = parser.parse_args()

    env_mode = (os.getenv("IDEATE_PM_SEARCH_MODE") or "").strip().lower()
    mode = args.mode
    if env_mode:
        if env_mode in MODE_CHOICES:
            if env_mode != args.mode:
                print(f"[i] IDEATE_PM_SEARCH_MODE forcing search mode '{env_mode}'.")
            mode = env_mode
        else:
            print(
                f"[!] IDEATE_PM_SEARCH_MODE value '{env_mode}' is invalid; "
                f"falling back to CLI mode '{mode}'."
            )

    skill_root = Path(__file__).resolve().parents[1]
    db_path = skill_root / "product" / "memory.sqlite"
    if not db_path.exists():
        raise SystemExit(
            'Repo product is not initialized. Run: python scripts/init_product.py --title "..."'
        )

    conn = runtime_sqlite.connect(db_path)
    cur = conn.cursor()

    fts_available = sqlite_env.has_fts5
    fts_enabled = fts_available

    if mode == "like":
        fts_enabled = False
        print("[i] Search mode forced to LIKE; using fuzzy fallback.\n")
    elif mode == "fts" and not fts_available:
        fts_enabled = False
        print(
            "[!] --mode fts requested but FTS5 is unavailable; falling back to LIKE.\n"
        )

    if not fts_enabled and mode != "like":
        if sqlite_env.fuzzy_mode:
            print(
                "[!] FTS5 unavailable; using fuzzy LIKE fallback. "
                "Install the optional pysqlite3-binary dependency for best results.\n"
            )
        else:
            print("[i] FTS disabled; using LIKE fallback.\n")

    query = args.query
    scope = args.scope
    results_found = False

    if scope in ("requirement", "all"):
        results = _search_requirements(cur, query, fts_enabled)
        if results:
            results_found = True
            print("## Requirements")
            print()
            for req_id, title, desc, status, priority in results:
                print(f"**{req_id}** [{status}] {title}")
                if desc:
                    desc_snippet = desc.replace("\n", " ")[:200]
                    print(f"   {desc_snippet}...")
                print()

    if scope in ("decision", "all"):
        results = _search_decisions(cur, query, fts_enabled)
        if results:
            results_found = True
            print("## Decisions")
            print()
            for (
                scope_type,
                scope_ref,
                question,
                choice,
                rationale,
                confidence,
            ) in results:
                scope_str = scope_type if not scope_ref else f"{scope_type}:{scope_ref}"
                print(f"**[{scope_str}]** Q: {question}")
                print(f"   → Choice: {choice}")
                if rationale:
                    print(f"   → Rationale: {rationale[:150]}...")
                print()

    if scope in ("question", "all"):
        results = _search_questions(cur, query, fts_enabled)
        if results:
            results_found = True
            print("## Open Questions")
            print()
            for scope_type, scope_ref, question, severity in results:
                scope_str = scope_type if not scope_ref else f"{scope_type}:{scope_ref}"
                print(f"**[{scope_str}]** [{severity}] {question}")
                print()

    if not results_found:
        print(f"No results found for query: {query}")

    conn.close()


if __name__ == "__main__":
    main()
