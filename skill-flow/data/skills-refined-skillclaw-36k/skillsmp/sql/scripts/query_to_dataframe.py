#!/usr/bin/env python3
"""
Execute SQL queries and output results as CSV, JSON, or table format.

SECURITY NOTE: This script executes arbitrary SQL queries. It is intended for
trusted administrative use only (CLI, automation scripts). Never expose this
to untrusted user input. For user-facing applications, use predefined query
templates with parameterized values only.

Usage:
    uv run query_to_dataframe.py "SELECT * FROM users LIMIT 10"
    uv run query_to_dataframe.py --file query.sql
    uv run query_to_dataframe.py "SELECT * FROM orders WHERE id = :id" --params '{"id": 123}'
    uv run query_to_dataframe.py "SELECT * FROM sales" --format json --output results.json
    uv run query_to_dataframe.py "SELECT * FROM big_table" --limit 100

Environment:
    DATABASE_URL (or custom via --env) must be set with connection string
"""

import argparse
import json
import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text


def get_engine(env_var: str = "DATABASE_URL"):
    """Create SQLAlchemy engine from environment variable."""
    conn_str = os.environ.get(env_var)
    if not conn_str:
        raise ValueError(f"Environment variable {env_var} not set")
    return create_engine(conn_str)


def query_to_dataframe(
    query: str,
    env_var: str = "DATABASE_URL",
    params: dict | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    """
    Execute SQL query and return results as DataFrame.

    SECURITY: The query parameter must come from trusted sources only (e.g.,
    hardcoded strings, trusted config files, CLI arguments from admins). Never
    pass user-controlled input as the query. Use params for dynamic values.

    Args:
        query: SQL SELECT query (trusted source only - see security note)
        env_var: Environment variable containing connection string
        params: Query parameters for parameterized queries (safe for user input)
        limit: Optional row limit (appended to query if no LIMIT present)

    Returns:
        pandas DataFrame with query results
    """
    engine = get_engine(env_var)
    params = dict(params) if params else {}

    # Add LIMIT if specified and not already in query (using parameterized value)
    if limit and "limit" not in query.lower():
        query = f"{query.rstrip(';')} LIMIT :_limit"
        params["_limit"] = limit

    return pd.read_sql(text(query), engine, params=params)


def main():
    parser = argparse.ArgumentParser(
        description="Execute SQL queries and export results"
    )
    parser.add_argument(
        "query",
        nargs="?",
        help="SQL query to execute (or use --file)",
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to .sql file containing query",
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
        help="Query parameters as JSON string (e.g., '{\"id\": 123}')",
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
        parser.error("Either query or --file is required")

    # Parse parameters
    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON params: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        df = query_to_dataframe(
            query=query,
            env_var=args.env,
            params=params,
            limit=args.limit,
        )

        # Format output
        if args.format == "csv":
            output = df.to_csv(index=False)
        elif args.format == "json":
            output = df.to_json(orient="records", indent=2)
        else:  # table
            output = df.to_string(index=False)

        # Write output
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"Wrote {len(df)} rows to {args.output}", file=sys.stderr)
        else:
            print(output)
            print(f"\n({len(df)} rows)", file=sys.stderr)

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
