#!/usr/bin/env python3
"""
Execute SQL write operations (INSERT, UPDATE, DELETE, DDL) with transaction safety.

⚠️  CAUTION: Write operations cannot be undone. ALWAYS use --dry-run first to
preview changes before committing. Verify your WHERE clause carefully - a missing
or incorrect WHERE clause can affect all rows in a table.

SECURITY NOTE: This script executes arbitrary SQL statements. It is intended for
trusted administrative use only (CLI, automation scripts). Never expose this
to untrusted user input. For user-facing applications, use predefined statement
templates with parameterized values only.

Usage:
    uv run execute_sql.py "UPDATE users SET active = true WHERE id = 1"
    uv run execute_sql.py "UPDATE users SET active = true" --dry-run
    uv run execute_sql.py --file migrations/add_column.sql
    uv run execute_sql.py "INSERT INTO logs (msg) VALUES (:msg)" --params '{"msg": "test"}'

Environment:
    DATABASE_URL (or custom via --env) must be set with connection string
"""

import argparse
import json
import os
import sys

from sqlalchemy import create_engine, text


def get_engine(env_var: str = "DATABASE_URL"):
    """Create SQLAlchemy engine from environment variable."""
    conn_str = os.environ.get(env_var)
    if not conn_str:
        raise ValueError(f"Environment variable {env_var} not set")
    return create_engine(conn_str)


def execute_sql(
    statement: str,
    env_var: str = "DATABASE_URL",
    params: dict | None = None,
    dry_run: bool = False,
) -> dict:
    """
    Execute SQL statement within a transaction.

    SECURITY: The statement parameter must come from trusted sources only (e.g.,
    hardcoded strings, trusted config files, CLI arguments from admins). Never
    pass user-controlled input as the statement. Use params for dynamic values.

    Args:
        statement: SQL statement to execute (trusted source only - see security note)
        env_var: Environment variable containing connection string
        params: Statement parameters for parameterized queries (safe for user input)
        dry_run: If True, rollback instead of commit

    Returns:
        Dict with rowcount and any returned values
    """
    engine = get_engine(env_var)

    with engine.begin() as conn:
        result = conn.execute(text(statement), params or {})

        response = {
            "rowcount": result.rowcount,
            "dry_run": dry_run,
        }

        # Capture RETURNING results if any
        if result.returns_rows:
            rows = [dict(row._mapping) for row in result.fetchall()]
            response["returned"] = rows

        if dry_run:
            conn.rollback()
            response["status"] = "rolled_back"
        else:
            response["status"] = "committed"

        return response


def main():
    parser = argparse.ArgumentParser(
        description="Execute SQL write operations with transaction safety"
    )
    parser.add_argument(
        "statement",
        nargs="?",
        help="SQL statement to execute (or use --file)",
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to .sql file containing statement(s)",
    )
    parser.add_argument(
        "--env",
        "-e",
        default="DATABASE_URL",
        help="Environment variable with connection string (default: DATABASE_URL)",
    )
    parser.add_argument(
        "--params",
        "-p",
        help="Statement parameters as JSON string (e.g., '{\"id\": 123}')",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Execute but rollback (preview changes without committing)",
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    # Get statement from argument or file
    if args.file:
        with open(args.file) as f:
            statement = f.read()
    elif args.statement:
        statement = args.statement
    else:
        parser.error("Either statement or --file is required")

    # Parse parameters
    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON params: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        result = execute_sql(
            statement=statement,
            env_var=args.env,
            params=params,
            dry_run=args.dry_run,
        )

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            status = "DRY RUN - changes rolled back" if result["dry_run"] else "Committed"
            print(f"Status: {status}")
            print(f"Rows affected: {result['rowcount']}")

            if result.get("returned"):
                print(f"\nReturned {len(result['returned'])} row(s):")
                for row in result["returned"]:
                    print(f"  {row}")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
