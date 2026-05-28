#!/usr/bin/env python3
"""List available keys in Workers Observability telemetry data."""

import argparse
from datetime import UTC, datetime, timedelta
import json
import os
import sys
from typing import Any

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find keys in the Workers Observability data"
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
        default=100,
        help="Max keys to return (default: 100, set high like 1000 for comprehensive list)",
    )
    parser.add_argument(
        "--key-needle",
        help="Pattern to match key names",
    )
    parser.add_argument(
        "--key-needle-regex",
        action="store_true",
        help="Treat key-needle as regex",
    )
    parser.add_argument(
        "--needle",
        help="General text search in log content",
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
        help="Filter in format key:operation:type:value (e.g., '$metadata.service:eq:string:llms')",
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

    if args.key_needle:
        payload["keyNeedle"] = {
            "value": args.key_needle,
            "isRegex": args.key_needle_regex,
            "matchCase": False,
        }

    if args.needle:
        payload["needle"] = {
            "value": args.needle,
            "isRegex": args.needle_regex,
            "matchCase": False,
        }

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/observability/telemetry/keys"
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
