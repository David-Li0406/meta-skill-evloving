#!/usr/bin/env python3
"""
name: http-get
description: Fetch a URL and return the response (useful for APIs and web pages)
credentials:
input:
  url: string (required) - The URL to fetch
  headers: object (optional) - Additional headers to send
output:
  status: HTTP status code
  headers: response headers
  body: response body (parsed as JSON if possible, otherwise string)
  size: response size in bytes
"""

import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError


def main():
    # Read input
    if sys.stdin.isatty():
        inp = {}
    else:
        try:
            inp = json.load(sys.stdin)
        except json.JSONDecodeError:
            inp = {}

    url = inp.get("url")
    if not url:
        print(json.dumps({"error": "Missing required parameter: url"}))
        sys.exit(1)

    custom_headers = inp.get("headers", {})

    try:
        # Build request
        req = Request(url)
        req.add_header("User-Agent", "notmcp/1.0")

        for key, value in custom_headers.items():
            req.add_header(key, value)

        # Make request
        response = urlopen(req, timeout=30)
        body_bytes = response.read()
        body_str = body_bytes.decode("utf-8", errors="replace")

        # Try to parse as JSON
        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            # Truncate large text responses
            if len(body_str) > 10000:
                body = body_str[:10000] + f"\n... (truncated, {len(body_str)} bytes total)"
            else:
                body = body_str

        # Build result
        result = {
            "status": response.status,
            "headers": dict(response.headers),
            "body": body,
            "size": len(body_bytes),
        }

        print(json.dumps(result, indent=2))

    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        result = {
            "error": f"HTTP {e.code}: {e.reason}",
            "status": e.code,
            "body": error_body[:2000] if len(error_body) > 2000 else error_body,
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)

    except URLError as e:
        print(json.dumps({"error": f"URL Error: {e.reason}"}))
        sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
