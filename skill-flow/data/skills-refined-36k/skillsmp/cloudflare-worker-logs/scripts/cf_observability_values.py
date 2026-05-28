#!/usr/bin/env python3
"""List unique values for a specific key in Workers Observability telemetry data."""

import argparse
from datetime import UTC, datetime, timedelta
import json
import os
import sys
from typing import Any

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find values for a key in Workers Observability data"
    )
    parser.add_argument(
        "key",
        help="The key to get values for (e.g., '$metadata.service', '$metadata.level')",
    )
    parser.add_argument(
        "--key-type",
        choices=["string", "number", "boolean"],
        default="string",
        help="Type of the key (default: string)",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=60,
        help="Time range in minutes (default: 60, max: 10080 for 7 days)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max values to return (default: 50)",
    )
    parser.add_argument(
        "--needle",
        help="Pattern to match values",
    )
    parser.add_argument(
        "--needle-regex",
        action="store_true",
        help="Treat needle as regex",
    )
    parser.add_argument(
        "--filter",
        action="append",
        dest="filters",
        help="Filter in format key:operation:type:value",
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

    now = datetime.now(UTC)
    from_time = now - timedelta(minutes=args.minutes)

    payload: dict[str, Any] = {
        "timeframe": {
            "from": int(from_time.timestamp() * 1000),
            "to": int(now.timestamp() * 1000),
        },
        "datasets": ["cloudflare-workers"],
        "key": args.key,
        "type": args.key_type,
        "limit": args.limit,
    }

    if args.filters:
        parsed_filters: list[dict[str, Any]] = []
        for f in args.filters:
            parts = f.split(":", 3)
            if len(parts) >= 3:
                filter_obj: dict[str, Any] = {
                    "key": parts[0],
                    "operation": parts[1],
                    "type": parts[2],
                }
                if len(parts) == 4:
                    filter_obj["value"] = parts[3]
                parsed_filters.append(filter_obj)
        if parsed_filters:
            payload["filters"] = parsed_filters

    if args.needle:
        payload["needle"] = {
            "value": args.needle,
            "isRegex": args.needle_regex,
            "matchCase": False,
        }

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/observability/telemetry/values"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    resp = httpx.post(url, headers=headers, json=payload)
    data = resp.json()

    if not data.get("success"):
        print(f"API Error: {json.dumps(data.get('errors', []))}", file=sys.stderr)
        return 1

    print(json.dumps(data.get("result", []), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
