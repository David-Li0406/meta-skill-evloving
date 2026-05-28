#!/usr/bin/env python3
"""Get details about a specific Cloudflare Worker."""

import argparse
import json
import os
import sys

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(description="Get details of a Cloudflare Worker")
    parser.add_argument("script_name", help="The name of the worker script to retrieve")
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

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts/{args.script_name}/settings"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    resp = httpx.get(url, headers=headers)
    data = resp.json()

    if not data.get("success"):
        print(f"API Error: Worker '{args.script_name}' not found", file=sys.stderr)
        return 1

    result = data.get("result", {})
    output = {
        "name": args.script_name,
        "bindings": result.get("bindings", []),
        "compatibility_date": result.get("compatibility_date"),
        "compatibility_flags": result.get("compatibility_flags", []),
        "usage_model": result.get("usage_model"),
        "tags": result.get("tags", []),
        "tail_consumers": result.get("tail_consumers", []),
        "logpush": result.get("logpush"),
        "placement": result.get("placement"),
        "observability": result.get("observability"),
    }
    output = {k: v for k, v in output.items() if v is not None}
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
