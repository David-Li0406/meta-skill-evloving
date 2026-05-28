#!/usr/bin/env python3
"""
Database schema inspection using SQLAlchemy.

Usage:
    uv run inspect_schema.py                      # List all tables
    uv run inspect_schema.py --table users        # Inspect specific table
    uv run inspect_schema.py --table users --json # JSON output
    uv run inspect_schema.py --env ANALYTICS_DB   # Use different env var

Environment:
    DATABASE_URL (or custom via --env) must be set with connection string
"""

import argparse
import json
import os
import sys

from sqlalchemy import create_engine, inspect


def get_engine(env_var: str = "DATABASE_URL"):
    """Create SQLAlchemy engine from environment variable."""
    conn_str = os.environ.get(env_var)
    if not conn_str:
        raise ValueError(f"Environment variable {env_var} not set")
    return create_engine(conn_str)


def list_tables(engine) -> list[str]:
    """Get list of all table names in the database."""
    inspector = inspect(engine)
    return inspector.get_table_names()


def get_table_info(engine, table_name: str) -> dict:
    """
    Get detailed information about a table.

    Returns:
        Dict with columns, primary_keys, foreign_keys, and indexes
    """
    inspector = inspect(engine)

    columns = []
    for col in inspector.get_columns(table_name):
        columns.append({
            "name": col["name"],
            "type": str(col["type"]),
            "nullable": col.get("nullable", True),
            "default": str(col.get("default")) if col.get("default") else None,
        })

    pk = inspector.get_pk_constraint(table_name)
    primary_keys = pk.get("constrained_columns", []) if pk else []

    foreign_keys = []
    for fk in inspector.get_foreign_keys(table_name):
        foreign_keys.append({
            "columns": fk.get("constrained_columns", []),
            "referred_table": fk.get("referred_table"),
            "referred_columns": fk.get("referred_columns", []),
        })

    indexes = []
    for idx in inspector.get_indexes(table_name):
        indexes.append({
            "name": idx.get("name"),
            "columns": idx.get("column_names", []),
            "unique": idx.get("unique", False),
        })

    return {
        "table": table_name,
        "columns": columns,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys,
        "indexes": indexes,
    }


def inspect_schema(
    env_var: str = "DATABASE_URL",
    table: str | None = None,
) -> dict:
    """
    Inspect database schema.

    Args:
        env_var: Environment variable containing connection string
        table: Specific table to inspect (None for all tables)

    Returns:
        Dict with tables list or single table info
    """
    engine = get_engine(env_var)

    if table:
        return get_table_info(engine, table)
    else:
        tables = list_tables(engine)
        return {"tables": tables, "count": len(tables)}


def format_table_info(info: dict) -> str:
    """Format table info for human-readable output."""
    lines = [f"Table: {info['table']}", ""]

    lines.append("Columns:")
    for col in info["columns"]:
        nullable = "NULL" if col["nullable"] else "NOT NULL"
        default = f" DEFAULT {col['default']}" if col["default"] else ""
        pk_marker = " [PK]" if col["name"] in info["primary_keys"] else ""
        lines.append(f"  {col['name']}: {col['type']} {nullable}{default}{pk_marker}")

    if info["primary_keys"]:
        lines.append(f"\nPrimary Key: {', '.join(info['primary_keys'])}")

    if info["foreign_keys"]:
        lines.append("\nForeign Keys:")
        for fk in info["foreign_keys"]:
            cols = ", ".join(fk["columns"])
            ref_cols = ", ".join(fk["referred_columns"])
            lines.append(f"  ({cols}) -> {fk['referred_table']}({ref_cols})")

    if info["indexes"]:
        lines.append("\nIndexes:")
        for idx in info["indexes"]:
            unique = "UNIQUE " if idx["unique"] else ""
            cols = ", ".join(idx["columns"])
            lines.append(f"  {idx['name']}: {unique}({cols})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Inspect database schema - tables, columns, keys, and indexes"
    )
    parser.add_argument(
        "--table",
        "-t",
        help="Specific table to inspect (omit for table list)",
    )
    parser.add_argument(
        "--env",
        "-e",
        default="DATABASE_URL",
        help="Environment variable with connection string (default: DATABASE_URL)",
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output as JSON",
    )

    args = parser.parse_args()

    try:
        result = inspect_schema(env_var=args.env, table=args.table)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if args.table:
                print(format_table_info(result))
            else:
                print(f"Found {result['count']} tables:\n")
                for table in result["tables"]:
                    print(f"  {table}")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
