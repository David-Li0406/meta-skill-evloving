#!/usr/bin/env python3
"""
Search Engine Module - DuckDuckGo based web search

Standalone module for deep-research skill.
Supports both new 'ddgs' package and legacy 'duckduckgo-search'.
"""

from typing import List, Dict, Optional
import logging
import warnings

logger = logging.getLogger(__name__)

# Try new package first, then fallback to legacy
DDGS = None
_using_legacy = False

try:
    # New package: ddgs
    from ddgs import DDGS
except ImportError:
    try:
        # Legacy package: duckduckgo-search (deprecated)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            from duckduckgo_search import DDGS
            _using_legacy = True
            logger.debug("Using legacy duckduckgo-search package. Consider: pip install ddgs")
    except ImportError:
        DDGS = None


class SearchEngine:
    """Web search engine wrapper using DuckDuckGo."""

    def __init__(self, max_results: int = 5):
        """Initialize the search engine.

        Args:
            max_results: Default maximum results per query.
        """
        if DDGS is None:
            raise ImportError(
                "Search package not installed. Run: pip install ddgs"
            )
        self.max_results = max_results
        self._ddgs = DDGS()
        
        if _using_legacy:
            logger.warning("Using deprecated duckduckgo-search. Run: pip install ddgs")

    def search(
        self, query: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Perform a web search.

        Args:
            query: Search query string.
            max_results: Optional limit on results.

        Returns:
            List of dicts with 'title', 'href', 'body' keys.
        """
        limit = max_results or self.max_results
        results = []

        try:
            logger.info(f"Searching: '{query}' (limit={limit})")
            search_gen = self._ddgs.text(query, max_results=limit)

            for r in search_gen:
                results.append(
                    {
                        "title": r.get("title", ""),
                        "href": r.get("href", ""),
                        "body": r.get("body", ""),
                    }
                )
        except Exception as e:
            logger.error(f"Search failed for '{query}': {e}")
            return []

        return results
