#!/usr/bin/env python3
"""
Inspect Internal Database Schema

Discover tables, columns, and schema in the project's internal MotherDuck database.

Usage:
    uv run skills/internal-db/scripts/inspect_internal_db.py
    uv run skills/internal-db/scripts/inspect_internal_db.py --table workflow_state
    uv run skills/internal-db/scripts/inspect_internal_db.py --json

SECURITY: This script only performs read operations (SHOW/DESCRIBE queries).
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def get_connection():
    """Create connection to internal MotherDuck database using environment variables."""
    import duckdb

    token = os.environ.get("FULCRUM_INTERNAL_DB_RW")
    db_name = os.environ.get("FULCRUM_INTERNAL_DB_NAME")

    if not token:
        raise ValueError(
            "FULCRUM_INTERNAL_DB_RW environment variable not set. "
            "Internal DB may not be provisioned yet."
        )
    if not db_name:
        raise ValueError(
            "FULCRUM_INTERNAL_DB_NAME environment variable not set. "
            "Internal DB may not be provisioned yet."
        )

    return duckdb.connect(f"md:{db_name}?motherduck_token={token}")


def list_tables(conn) -> list[str]:
    """Return list of all table names in the database."""
    result = conn.execute("SHOW TABLES").fetchall()
    return [row[0] for row in result]


def validate_table_name(conn, table_name: str) -> str:
    """
    Validate table name against known tables to prevent SQL injection.

    Args:
        conn: Database connection
        table_name: Table name to validate

    Returns:
        Validated table name

    Raises:
        ValueError: If table name is not in the database
    """
    known_tables = list_tables(conn)
    if table_name not in known_tables:
        raise ValueError(
            f"Table '{table_name}' not found. "
            f"Available tables: {', '.join(known_tables) if known_tables else 'none'}"
        )
    return table_name


def get_table_info(conn, table_name: str) -> dict:
    """
    Get detailed information about a table.

    Returns dict with:
        - columns: list of {name, type, nullable, default}
        - primary_key: list of column names
        - row_count: approximate row count
    """
    # SECURITY: Validate table name against known tables to prevent SQL injection
    validated_table = validate_table_name(conn, table_name)

    # Get column information using DESCRIBE
    # Note: DuckDB DESCRIBE doesn't support parameterized table names,
    # so we validate against known tables first
    columns = []
    result = conn.execute(f"DESCRIBE {validated_table}").fetchall()
    for row in result:
        columns.append({
            "name": row[0],
            "type": row[1],
            "nullable": row[2] == "YES" if len(row) > 2 else True,
            "default": row[4] if len(row) > 4 else None,
        })

    # Get primary key info from constraints (if available)
    # Use parameterized query for the WHERE clause
    primary_key = []
    try:
        pk_result = conn.execute("""
            SELECT column_name
            FROM information_schema.key_column_usage
            WHERE table_name = ?
            AND constraint_name LIKE '%pkey%'
            ORDER BY ordinal_position
        """, [validated_table]).fetchall()
        primary_key = [row[0] for row in pk_result]
    except Exception:
        # Primary key detection may not be available in all cases
        pass

    # Get approximate row count
    # Note: FROM clause requires validated table name (can't be parameterized)
    row_count = 0
    try:
        count_result = conn.execute(f"SELECT COUNT(*) FROM {validated_table}").fetchone()
        row_count = count_result[0] if count_result else 0
    except Exception:
        pass

    return {
        "name": validated_table,
        "columns": columns,
        "primary_key": primary_key,
        "row_count": row_count,
    }


def inspect_schema(table: str | None = None) -> dict | list[str]:
    """
    Inspect the internal database schema.

    Args:
        table: If provided, return detailed info for this table.
               If None, return list of all table names.

    Returns:
        List of table names, or dict with table details.
    """
    conn = get_connection()
    try:
        if table:
            return get_table_info(conn, table)
        else:
            return list_tables(conn)
    finally:
        conn.close()


def format_table_info(info: dict) -> str:
    """Format table information for human-readable output."""
    lines = [f"Table: {info['name']}", f"Rows: ~{info['row_count']:,}", "", "Columns:"]

    for col in info["columns"]:
        pk_marker = " [PK]" if col["name"] in info.get("primary_key", []) else ""
        nullable = "" if col["nullable"] else " NOT NULL"
        default = f" DEFAULT {col['default']}" if col["default"] else ""
        lines.append(f"  {col['name']}: {col['type']}{nullable}{default}{pk_marker}")

    if info.get("primary_key"):
        lines.append("")
        lines.append(f"Primary Key: ({', '.join(info['primary_key'])})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Inspect internal database schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                     List all tables
  %(prog)s --table users       Inspect specific table
  %(prog)s --json              Output as JSON
        """,
    )
    parser.add_argument(
        "--table",
        "-t",
        help="Table name to inspect (omit to list all tables)",
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    try:
        result = inspect_schema(args.table)

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        elif args.table:
            print(format_table_info(result))
        else:
            if result:
                print("Tables:")
                for table in result:
                    print(f"  {table}")
            else:
                print("No tables found in database.")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inspecting schema: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
