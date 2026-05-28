#!/usr/bin/env python3
"""List all Cloudflare Workers in the account."""

import json
import os
import sys

import httpx


def main() -> int:
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

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/scripts"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    resp = httpx.get(url, headers=headers)
    data = resp.json()

    if not data.get("success"):
        print(f"API Error: {json.dumps(data.get('errors', []))}", file=sys.stderr)
        return 1

    workers = data.get("result", [])
    print(
        json.dumps(
            {
                "workers": [
                    {
                        "name": w["id"],
                        "modified_on": w.get("modified_on"),
                        "created_on": w.get("created_on"),
                    }
                    for w in workers
                ],
                "count": len(workers),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
