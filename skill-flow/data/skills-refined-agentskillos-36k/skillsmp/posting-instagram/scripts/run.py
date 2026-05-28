#!/usr/bin/env python3
"""
Instagram Posting - Run Script

Executes Instagram posting operations via MCP server.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.mcp_servers.meta_social_connector import post_to_instagram, get_instagram_insights


def main():
    parser = argparse.ArgumentParser(description="Instagram Posting")
    parser.add_argument("--post", help="Post caption to Instagram")
    parser.add_argument("--image", required="--post" in sys.argv, help="Image URL (required for posting)")
    parser.add_argument("--hashtags", help="Comma-separated hashtags (without #)")
    parser.add_argument("--insights", action="store_true", help="Get Instagram insights")
    parser.add_argument("--days", type=int, default=7, help="Days for insights (default: 7)")
    parser.add_argument("--no-approval", action="store_true", help="Skip approval workflow")

    args = parser.parse_args()

    if args.post:
        hashtags = args.hashtags.split(",") if args.hashtags else None
        result = post_to_instagram(
            content=args.post,
            image_url=args.image,
            hashtags=hashtags,
            requires_approval=not args.no_approval
        )
        print(result)

    elif args.insights:
        result = get_instagram_insights(days=args.days)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
