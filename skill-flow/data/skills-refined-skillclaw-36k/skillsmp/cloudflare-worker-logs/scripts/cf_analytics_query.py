#!/usr/bin/env python3
"""Query Workers Analytics Engine datasets using the SQL API."""

import argparse
import json
import os
import sys
from typing import Any

import httpx

# Schema mappings for known datasets
# Maps dataset name -> {field_name: semantic_alias}
DATASET_SCHEMAS: dict[str, dict[str, str]] = {
    "llms_usage": {
        "index1": "method",
        "blob1": "path",
        "blob2": "status",
        "blob3": "request_type",  # provider, amp-tab, amp-telemetry, amp-admin, management, oauth, other
        "blob4": "provider",  # anthropic, google, openai, etc.
        "blob5": "model",  # gemini-3-pro-preview, etc.
        "blob6": "client",  # VS Code CLI, VS Code Insiders, Bun, node, etc.
        "double1": "latency_ms",
        "double2": "input_tokens",  # Input/prompt tokens (non-streaming only)
        "double3": "output_tokens",  # Output/completion tokens (non-streaming only)
    },
}


def build_select_clause(
    dataset: str,
    fields: list[str] | None,
    aggregations: list[str] | None,
    group_by: list[str] | None,
) -> str:
    """Build SELECT clause with semantic aliases."""
    schema = DATASET_SCHEMAS.get(dataset, {})

    if aggregations:
        # Aggregation mode - build computed columns
        select_parts: list[str] = []

        # Add group-by fields first
        if group_by:
            for field in group_by:
                alias = schema.get(field, field)
                if field != alias:
                    select_parts.append(f"{field} AS {alias}")
                else:
                    select_parts.append(field)

        # Add aggregations
        for agg in aggregations:
            select_parts.append(agg)

        return ", ".join(select_parts)

    # Raw event mode
    if fields:
        select_parts = []
        for field in fields:
            alias = schema.get(field, field)
            if field != alias:
                select_parts.append(f"{field} AS {alias}")
            else:
                select_parts.append(field)
        return ", ".join(select_parts)

    # Default: select commonly useful fields with aliases
    default_fields = ["timestamp", "index1", "blob1", "blob2", "double1"]
    select_parts = []
    for field in default_fields:
        alias = schema.get(field, field)
        if field != alias:
            select_parts.append(f"{field} AS {alias}")
        else:
            select_parts.append(field)
    return ", ".join(select_parts)


def build_query(
    dataset: str,
    fields: list[str] | None,
    aggregations: list[str] | None,
    group_by: list[str] | None,
    where: list[str] | None,
    minutes: int,
    order_by: str | None,
    order: str,
    limit: int,
) -> str:
    """Build complete SQL query."""
    select_clause = build_select_clause(dataset, fields, aggregations, group_by)

    query_parts = [f"SELECT {select_clause}", f"FROM {dataset}"]

    # Time filter
    where_clauses = [f"timestamp > NOW() - INTERVAL '{minutes}' MINUTE"]

    if where:
        where_clauses.extend(where)

    query_parts.append("WHERE " + " AND ".join(where_clauses))

    if group_by:
        query_parts.append("GROUP BY " + ", ".join(group_by))

    if order_by:
        query_parts.append(f"ORDER BY {order_by} {order.upper()}")
    elif aggregations:
        # Default ordering for aggregations: by first aggregation descending
        query_parts.append("ORDER BY 1 DESC")
    else:
        query_parts.append("ORDER BY timestamp DESC")

    query_parts.append(f"LIMIT {limit}")

    return "\n".join(query_parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query Workers Analytics Engine datasets using the SQL API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show recent events with semantic field names
  uv run scripts/cf_analytics_query.py

  # Custom time range
  uv run scripts/cf_analytics_query.py --minutes 1440

  # Request counts by path and status
  uv run scripts/cf_analytics_query.py --agg 'SUM(_sample_interval) AS request_count' --group-by blob1 --group-by blob2

  # Average latency by method
  uv run scripts/cf_analytics_query.py --agg 'SUM(_sample_interval * double1) / SUM(_sample_interval) AS avg_latency_ms' --group-by index1

  # Filter by status code
  uv run scripts/cf_analytics_query.py --where "blob2 = '401'"

  # Raw SQL query
  uv run scripts/cf_analytics_query.py --raw "SELECT blob1, COUNT() FROM llms_usage GROUP BY blob1 LIMIT 10"
""",
    )
    parser.add_argument(
        "--dataset",
        default="llms_usage",
        help="Analytics Engine dataset name (default: llms_usage)",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=60,
        help="Time range in minutes (default: 60)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max results to return (default: 20)",
    )
    parser.add_argument(
        "--field",
        action="append",
        dest="fields",
        help="Field to select (can be repeated). Omit for default fields with aliases.",
    )
    parser.add_argument(
        "--agg",
        action="append",
        dest="aggregations",
        help="Aggregation expression (e.g., 'SUM(_sample_interval) AS count'). Implies grouping mode.",
    )
    parser.add_argument(
        "--group-by",
        action="append",
        dest="group_by",
        help="Field to group by (can be repeated). Use with --agg.",
    )
    parser.add_argument(
        "--where",
        action="append",
        dest="where_clauses",
        help="WHERE clause condition (can be repeated). E.g., \"blob2 = '401'\"",
    )
    parser.add_argument(
        "--order-by",
        help="Field or alias to order by",
    )
    parser.add_argument(
        "--order",
        choices=["asc", "desc"],
        default="desc",
        help="Sort order (default: desc)",
    )
    parser.add_argument(
        "--raw",
        dest="raw_query",
        help="Execute a raw SQL query (ignores other options except --format)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "jsonl", "tsv"],
        default="json",
        help="Output format: json (default), jsonl (one JSON object per line), tsv (tab-separated)",
    )
    parser.add_argument(
        "--show-query",
        action="store_true",
        help="Print the generated SQL query",
    )
    parser.add_argument(
        "--show-schema",
        action="store_true",
        help="Show the schema mapping for the dataset",
    )
    parser.add_argument(
        "--list-datasets",
        action="store_true",
        help="List available Analytics Engine datasets",
    )
    args = parser.parse_args()

    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")

    if not account_id:
        print(
            "Error: CLOUDFLARE_ACCOUNT_ID environment variable is required",
            file=sys.stderr,
        )
        return 1
    if not api_token:
        print(
            "Error: CLOUDFLARE_API_TOKEN environment variable is required",
            file=sys.stderr,
        )
        return 1

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql"
    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    # Handle --list-datasets
    if args.list_datasets:
        resp = httpx.post(url, headers=headers, content="SHOW TABLES", timeout=30.0)
        data = resp.json()
        if "data" in data:
            datasets = [row.get("dataset") for row in data["data"]]
            print(json.dumps({"datasets": datasets}, indent=2))
        else:
            print(json.dumps(data, indent=2))
        return 0

    # Handle --show-schema
    if args.show_schema:
        schema = DATASET_SCHEMAS.get(args.dataset, {})
        if schema:
            print(f"Schema for {args.dataset}:")
            print(json.dumps(schema, indent=2))
        else:
            print(
                f"No schema defined for {args.dataset}. Raw field names will be used."
            )
            print("Available schemas:", list(DATASET_SCHEMAS.keys()))
        return 0

    # Build or use raw query
    if args.raw_query:
        query = args.raw_query
    else:
        query = build_query(
            dataset=args.dataset,
            fields=args.fields,
            aggregations=args.aggregations,
            group_by=args.group_by,
            where=args.where_clauses,
            minutes=args.minutes,
            order_by=args.order_by,
            order=args.order,
            limit=args.limit,
        )

    if args.show_query:
        print("Generated SQL:", file=sys.stderr)
        print(query, file=sys.stderr)
        print("---", file=sys.stderr)

    # Add format clause if needed
    if args.format == "jsonl":
        query = query.rstrip(";") + " FORMAT JSONEachRow"
    elif args.format == "tsv":
        query = query.rstrip(";") + " FORMAT TabSeparated"

    resp = httpx.post(url, headers=headers, content=query, timeout=30.0)

    if args.format in ["jsonl", "tsv"]:
        # Raw text output
        print(resp.text)
        return 0

    # JSON handling
    if not resp.text:
        print(f"Empty response (status {resp.status_code})", file=sys.stderr)
        return 1

    try:
        data: dict[str, Any] = resp.json()
    except Exception:
        print(f"Invalid JSON response: {resp.text[:500]}", file=sys.stderr)
        return 1

    if data.get("errors"):
        print(f"API Error: {json.dumps(data['errors'])}", file=sys.stderr)
        return 1

    # Format output
    result = {
        "data": data.get("data", []),
        "rows": data.get("rows", 0),
        "meta": data.get("meta", []),
    }

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
