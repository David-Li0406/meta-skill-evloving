#!/usr/bin/env python3
"""
Twitter/X Posting - Run Script

Executes Twitter posting operations via MCP server.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.mcp_servers.twitter_connector import (
    post_tweet,
    create_thread,
    search_mentions,
    get_timeline_insights
)


def main():
    parser = argparse.ArgumentParser(description="Twitter/X Posting")
    parser.add_argument("--post", help="Post a tweet")
    parser.add_argument("--reply-to", help="Tweet ID to reply to")
    parser.add_argument("--thread", nargs="+", help="Create a thread (multiple tweets)")
    parser.add_argument("--search", help="Search mentions or query")
    parser.add_argument("--insights", action="store_true", help="Get timeline insights")
    parser.add_argument("--days", type=int, default=7, help="Days for insights (default: 7)")
    parser.add_argument("--no-approval", action="store_true", help="Skip approval workflow")

    args = parser.parse_args()

    if args.post:
        result = post_tweet(
            content=args.post,
            reply_to=args.reply_to,
            requires_approval=not args.no_approval
        )
        print(result)

    elif args.thread:
        result = create_thread(
            tweets=args.thread,
            requires_approval=not args.no_approval
        )
        print(result)

    elif args.search:
        result = search_mentions(query=args.search)
        print(result)

    elif args.insights:
        result = get_timeline_insights(days=args.days)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
