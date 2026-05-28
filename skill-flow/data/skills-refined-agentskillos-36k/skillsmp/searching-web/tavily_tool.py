from __future__ import annotations

import json
import logging
import os
from typing import Any

from src.humcp.decorator import tool

try:
    from tavily import TavilyClient
except ImportError as err:
    raise ImportError(
        "tavily-python is required for Tavily search tools. Install with: pip install tavily-python"
    ) from err

logger = logging.getLogger("humcp.tools.tavily")


class TavilySearchTool:
    """
    Helper class to perform web searches using the Tavily API.

    This class wraps the Tavily client and provides a method to search the web
    while trimming the response to a configurable token limit.
    """

    def __init__(
        self, api_key: str, search_depth: str = "basic", max_tokens: int = 8000
    ):
        self.client = TavilyClient(api_key=api_key)
        self.search_depth = search_depth
        self.max_tokens = max_tokens

    def web_search_using_tavily(self, query: str, max_results: int = 5) -> dict:
        """
        Function to search online given a query using the Tavily API. The query can be anything.

        Args:
            query (str): The query to search for.
            max_results (int): The maximum number of results to return (default is 5).

        Returns:
            dict: A dictionary containing the search results.
        """
        logger.info(
            "Tavily search start depth=%s max_results=%s",
            self.search_depth,
            max_results,
        )
        response = self.client.search(
            query=query, search_depth=self.search_depth, max_results=max_results
        )

        clean_response: dict[str, Any] = {"query": query}
        if "answer" in response:
            clean_response["answer"] = response["answer"]

        clean_results = []
        current_token_count = len(json.dumps(clean_response))
        for result in response.get("results", []):
            _result = {
                "title": result["title"],
                "url": result["url"],
                "content": result["content"],
                "score": result["score"],
            }
            current_token_count += len(json.dumps(_result))
            if current_token_count > self.max_tokens:
                break
            clean_results.append(_result)
        clean_response["results"] = clean_results

        logger.info(
            "Tavily search complete results=%d max_tokens=%s",
            len(clean_results),
            self.max_tokens,
        )
        return clean_response if clean_response else {}


@tool()
async def tavily_web_search(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
    max_tokens: int = 8000,
) -> dict:
    """
    Search the web using Tavily and return cleaned results.

    Args:
        query: The query to search for.
        max_results: Maximum number of results to return.
        search_depth: Tavily search depth (e.g., 'basic' or 'advanced').
        max_tokens: Rough limit for response size to avoid oversized payloads.
        api_key: Optional Tavily API key; falls back to TAVILY_API_KEY env var.

    Returns:
        Success flag and search data or error message.
    """
    try:
        resolved_api_key = os.getenv("TAVILY_API_KEY")
        if not resolved_api_key:
            return {
                "success": False,
                "error": "TAVILY_API_KEY is not set. Provide api_key or set the environment variable.",
            }

        if max_results < 1:
            return {"success": False, "error": "max_results must be at least 1"}
        logger.info(
            "Tavily tool invoked query_length=%d depth=%s", len(query), search_depth
        )
        searcher = TavilySearchTool(
            api_key=resolved_api_key,
            search_depth=search_depth,
            max_tokens=max_tokens,
        )
        results = searcher.web_search_using_tavily(query=query, max_results=max_results)

        if not results:
            return {"success": False, "error": "No results found."}

        return {"success": True, "data": results}
    except Exception as e:
        logger.exception("Tavily search failed")
        return {"success": False, "error": f"Tavily search failed: {str(e)}"}
