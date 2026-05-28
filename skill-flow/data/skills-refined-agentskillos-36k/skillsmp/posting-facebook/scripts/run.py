#!/usr/bin/env python3
"""
Facebook Posting - Run Script

Executes Facebook posting operations via MCP server.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.mcp_servers.meta_social_connector import post_to_facebook, get_facebook_insights


def main():
    parser = argparse.ArgumentParser(description="Facebook Posting")
    parser.add_argument("--post", help="Post content to Facebook")
    parser.add_argument("--link", help="Optional link to include")
    parser.add_argument("--insights", action="store_true", help="Get Facebook insights")
    parser.add_argument("--days", type=int, default=7, help="Days for insights (default: 7)")
    parser.add_argument("--no-approval", action="store_true", help="Skip approval workflow")

    args = parser.parse_args()

    if args.post:
        result = post_to_facebook(
            content=args.post,
            link=args.link,
            requires_approval=not args.no_approval
        )
        print(result)

    elif args.insights:
        result = get_facebook_insights(days=args.days)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
