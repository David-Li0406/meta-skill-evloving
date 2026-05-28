#!/usr/bin/env python3
"""
Deal Hunt Script

Modular deal search using Tavily. Claude decides search parameters.
Returns raw results for Claude to analyze.

Usage:
    # Basic search (searches entire web)
    python deal_hunt.py "Sony WH-1000XM5"

    # Multi-query for broader coverage (max 3, runs in parallel, deduplicates)
    python deal_hunt.py "AirPods Pro" --queries "AirPods Pro 2 deal,AirPods Pro coupon,AirPods discount"

    # Search specific retailers only
    python deal_hunt.py "LG C4 OLED" --domains amazon.com,bestbuy.com,walmart.com

    # Fresh deals only (today)
    python deal_hunt.py "PS5" --time-range day

    # Custom query for coupons
    python deal_hunt.py "Nintendo Switch" --query "Nintendo Switch OLED promo code coupon"

    # Fast search with more results
    python deal_hunt.py "Dyson V15" --max-results 15 --search-depth fast
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone

try:
    from tavily import AsyncTavilyClient
except ImportError:
    print("Error: tavily-python not installed. Run: pip install tavily-python")
    sys.exit(1)


async def search(client, query, domains, max_results, time_range, search_depth):
    """Execute a single Tavily search."""
    kwargs = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
    }
    if time_range:
        kwargs["time_range"] = time_range
    if domains:
        kwargs["include_domains"] = domains

    response = await client.search(**kwargs)
    return response.get("results", [])


def deduplicate_by_url(all_results):
    """
    Deduplicate results by URL, keeping highest score and merging content.
    """
    url_data = {}

    for result in all_results:
        url = result.get("url")
        if not url:
            continue

        score = result.get("score", 0)
        content = result.get("content", "")

        if url in url_data:
            existing = url_data[url]
            # Keep higher score
            if score > existing.get("score", 0):
                existing["score"] = score
            # Merge content chunks
            existing_content = existing.get("content", "")
            if content and content not in existing_content:
                existing["content"] = existing_content + " [...] " + content
        else:
            url_data[url] = result.copy()

    # Sort by score descending
    results = list(url_data.values())
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results


async def deal_hunt(
    product,
    query=None,
    queries=None,
    domains=None,
    max_results=10,
    time_range="week",
    search_depth="advanced",
):
    """
    Search for deals on a product.

    Args:
        product: Product name
        query: Single custom search query
        queries: List of queries (max 3) for parallel search with dedup
        domains: List of domains to search (None = search all)
        max_results: Max results per query
        time_range: day, week, month, year, or None
        search_depth: basic, advanced, fast, ultrafast

    Returns raw Tavily results for Claude to analyze.
    """
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not set")

    client = AsyncTavilyClient(api_key=api_key)

    # Determine queries to run
    if queries:
        # Multi-query mode (max 3)
        search_queries = queries[:3]
    elif query:
        # Single custom query
        search_queries = [query]
    else:
        # Default query
        search_queries = [f"{product} deal price"]

    # Run searches in parallel
    tasks = [
        search(client, q, domains, max_results, time_range, search_depth)
        for q in search_queries
    ]
    results_lists = await asyncio.gather(*tasks)

    # Flatten and deduplicate
    all_results = []
    for results in results_lists:
        all_results.extend(results)

    if len(search_queries) > 1:
        # Deduplicate when multiple queries
        final_results = deduplicate_by_url(all_results)
    else:
        final_results = all_results

    return {
        "meta": {
            "product": product,
            "queries": search_queries,
            "domains": domains,
            "time_range": time_range,
            "search_time": datetime.now(timezone.utc).isoformat(),
            "total_results": len(final_results),
        },
        "results": final_results,
    }


def main():
    parser = argparse.ArgumentParser(description="Search for deals")
    parser.add_argument("product", help="Product name")
    parser.add_argument("--query", "-q", help="Single custom search query")
    parser.add_argument("--queries", help="Comma-separated queries (max 3) for parallel search")
    parser.add_argument("--domains", "-d", help="Comma-separated domains to search")
    parser.add_argument("--max-results", "-n", type=int, default=10)
    parser.add_argument("--time-range", "-t", default="week",
                        choices=["day", "week", "month", "year", "none"])
    parser.add_argument("--search-depth", "-s", default="advanced",
                        choices=["basic", "advanced", "fast", "ultrafast"])

    args = parser.parse_args()

    domains = None
    if args.domains:
        domains = [d.strip() for d in args.domains.split(",")]

    queries = None
    if args.queries:
        queries = [q.strip() for q in args.queries.split(",")][:3]

    time_range = args.time_range if args.time_range != "none" else None

    try:
        result = asyncio.run(deal_hunt(
            product=args.product,
            query=args.query,
            queries=queries,
            domains=domains,
            max_results=args.max_results,
            time_range=time_range,
            search_depth=args.search_depth,
        ))
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
