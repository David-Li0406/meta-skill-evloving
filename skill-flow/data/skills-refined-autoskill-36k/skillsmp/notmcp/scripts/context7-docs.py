#!/usr/bin/env python3
"""
name: context7-docs
description: Fetch up-to-date API documentation from Context7
credentials:
  - CONTEXT7_API_KEY
input:
  library: string (required) - Library path like "googleapis/gmail" or "vercel/next.js"
  topic: string (optional) - Specific topic to search for like "send" or "authentication"
  tokens: int (optional, default 5000) - Maximum tokens to return
output:
  docs: The documentation content
  library: The library that was queried
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode


def main():
    # Read input
    if sys.stdin.isatty():
        inp = {}
    else:
        try:
            inp = json.load(sys.stdin)
        except json.JSONDecodeError:
            inp = {}

    # Get required parameters
    library = inp.get("library")
    if not library:
        print(json.dumps({"error": "Missing required parameter: library"}))
        sys.exit(1)

    topic = inp.get("topic", "")
    tokens = inp.get("tokens", 5000)

    # Get API key
    api_key = os.environ.get("CONTEXT7_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing CONTEXT7_API_KEY credential"}))
        sys.exit(1)

    # Build URL
    params = {"tokens": tokens}
    if topic:
        params["topic"] = topic
    
    url = f"https://context7.com/api/v1/{library}?{urlencode(params)}"

    try:
        req = Request(url)
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Accept", "text/plain")

        response = urlopen(req, timeout=30)
        docs = response.read().decode("utf-8")

        result = {
            "library": library,
            "topic": topic if topic else "(all)",
            "docs": docs,
            "tokens_requested": tokens,
        }

        print(json.dumps(result, indent=2))

    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(json.dumps({
            "error": f"Context7 API error: HTTP {e.code}",
            "details": error_body[:500]
        }))
        sys.exit(1)

    except URLError as e:
        print(json.dumps({"error": f"Network error: {e.reason}"}))
        sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
