#!/usr/bin/env python3
"""
Quick Search - Standalone DuckDuckGo Web Search

이 스크립트는 독립적으로 실행 가능하며, 외부 프로젝트 의존성이 없습니다.

Usage:
    python run.py "search query" [max_results]

Example:
    python run.py "Python best practices" 10
"""

import sys
from typing import List, Dict

try:
    from duckduckgo_search import DDGS
except ImportError:
    print("❌ Error: duckduckgo-search not installed")
    print("   Install with: pip install duckduckgo-search>=3.0.0")
    sys.exit(1)


def search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Perform a quick web search using DuckDuckGo.

    Args:
        query: Search query string.
        max_results: Maximum number of results to return.

    Returns:
        List of search result dictionaries with keys: title, url, snippet
    """
    print(f"🔍 Searching for: {query}")
    results = []

    try:
        with DDGS() as ddgs:
            # backend='html' 사용 (더 안정적)
            search_results = list(
                ddgs.text(query, max_results=max_results, backend="html")
            )
            if not search_results:
                print("No results with backend='html'. Trying default...")
                search_results = list(ddgs.text(query, max_results=max_results))

            for r in search_results:
                result = {
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                }
                results.append(result)
                print(f"Title: {result['title']}")
                print(f"URL: {result['url']}")
                print(f"Snippet: {result['snippet']}")
                print("-" * 40)

    except Exception as e:
        print(f"❌ Error during search: {e}")

    return results


def main():
    if len(sys.argv) < 2:
        print('Usage: python run.py "search query" [max_results]')
        print('Example: python run.py "Python best practices" 10')
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    results = search(query, max_results)
    print(f"\n✅ Found {len(results)} results")
    return results


if __name__ == "__main__":
    main()
