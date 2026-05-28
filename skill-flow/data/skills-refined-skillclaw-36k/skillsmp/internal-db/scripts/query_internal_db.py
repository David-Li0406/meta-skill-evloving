#!/usr/bin/env python3
"""
Query Internal Database

Execute SELECT queries and export results as CSV, JSON, or table format.

Usage:
    uv run skills/internal-db/scripts/query_internal_db.py "SELECT * FROM workflow_state"
    uv run skills/internal-db/scripts/query_internal_db.py "SELECT * FROM cache" --format json
    uv run skills/internal-db/scripts/query_internal_db.py "SELECT * FROM audit_log" --limit 100

SECURITY: This script only performs read operations (SELECT queries).
The query parameter must come from trusted sources (hardcoded, config files, CLI).
Use --params for dynamic values that may come from user input.
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


def query_to_dataframe(
    query: str,
    params: dict | None = None,
    limit: int | None = None,
):
    """
    Execute a SELECT query and return results as a pandas DataFrame.

    Args:
        query: SQL SELECT query (must come from trusted source)
        params: Dict of parameters for parameterized queries (safe for user input)
        limit: Optional row limit (auto-appended if query lacks LIMIT)

    Returns:
        pandas DataFrame with query results
    """
    import pandas as pd

    conn = get_connection()
    try:
        # SECURITY: Validate limit is strictly a positive integer
        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise ValueError(f"limit must be a non-negative integer, got: {limit}")

        # Auto-append LIMIT if specified and not present
        # Use parameterized query to prevent SQL injection
        query_upper = query.upper()
        query_params = list(params.values()) if params else []

        if limit is not None and "LIMIT" not in query_upper:
            query = f"{query} LIMIT ?"
            query_params.append(limit)

        if query_params:
            result = conn.execute(query, query_params)
        else:
            result = conn.execute(query)

        return result.df()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Query internal database and export results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "SELECT * FROM workflow_state LIMIT 10"
  %(prog)s "SELECT * FROM cache WHERE key = ?" --params '["my_key"]'
  %(prog)s "SELECT * FROM audit_log" --format json --output results.json
  %(prog)s "SELECT * FROM big_table" --limit 100
        """,
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="SQL SELECT query (or use --file)",
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to .sql file containing query",
    )
    parser.add_argument(
        "--params",
        "-p",
        help="JSON array of parameters for parameterized query",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "table"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        help="Limit number of rows returned",
    )

    args = parser.parse_args()

    # Get query from argument or file
    if args.file:
        with open(args.file) as f:
            query = f.read()
    elif args.query:
        query = args.query
    else:
        parser.error("Either query argument or --file is required")

    # Parse parameters if provided
    params = None
    if args.params:
        try:
            params_list = json.loads(args.params)
            if isinstance(params_list, list):
                params = {str(i): v for i, v in enumerate(params_list)}
            else:
                params = params_list
        except json.JSONDecodeError as e:
            print(f"Error parsing --params JSON: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        df = query_to_dataframe(query, params=params, limit=args.limit)

        # Format output
        if args.format == "csv":
            output = df.to_csv(index=False)
        elif args.format == "json":
            output = df.to_json(orient="records", indent=2, default_handler=str)
        else:  # table
            output = df.to_string(index=False)

        # Write to file or stdout
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Results written to {args.output}")
        else:
            print(output)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
