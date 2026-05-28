#!/usr/bin/env python3
"""
Multi-source search online tool with AI summarization.
Aggregates results from Tavily, WebSearchAPI, and Gemini Search, then summarizes with Gemini.
"""

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# Load .env file if it exists
def load_dotenv():
    """Load environment variables from .env file in script directory."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value.strip()

load_dotenv()


def retry_on_failure(max_retries: int = 3, delay: float = 3.0):
    """Decorator for retrying failed API calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                result = func(*args, **kwargs)
                if result and result.get("success"):
                    return result
                if attempt < max_retries:
                    print(f"  Retry {attempt}/{max_retries - 1} for {result.get('source', 'unknown')}...", file=sys.stderr)
                    time.sleep(delay)
            return result
        return wrapper
    return decorator


class WebSearch:
    """Multi-source search online aggregator."""

    def __init__(self, max_results: int = 5):
        """
        Initialize with API keys from environment variables.

        Args:
            max_results: Maximum number of results per search source (1-10). Default is 5.
        """
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        self.websearchapi_key = os.getenv("WEBSEARCHAPI_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.max_results = max(1, min(10, max_results))  # Clamp between 1-10
        self.gemini_models = ["gemini-3-flash-preview", "gemini-flash-latest", "gemini-2.5-flash-lite"]
        self.available_gemini_models = list(self.gemini_models)

        if not self.gemini_key:
            print("Warning: GEMINI_API_KEY not found. Summarization will be skipped.", file=sys.stderr)

    @retry_on_failure(max_retries=3, delay=3.0)
    def search_tavily(self, query: str) -> Optional[Dict[str, Any]]:
        """Search using Tavily API."""
        if not self.tavily_key:
            return {"error": "TAVILY_API_KEY not set", "source": "tavily", "success": False}

        try:
            response = requests.post(
                "https://api.tavily.com/search",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.tavily_key}"
                },
                json={
                    "query": query,
                    "search_depth": "advanced",
                    "max_results": self.max_results
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return {
                "source": "tavily",
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "source": "tavily",
                "success": False,
                "error": str(e)
            }

    @retry_on_failure(max_retries=3, delay=3.0)
    def search_websearchapi(self, query: str) -> Optional[Dict[str, Any]]:
        """Search using WebSearchAPI."""
        if not self.websearchapi_key:
            return {"error": "WEBSEARCHAPI_KEY not set", "source": "websearchapi", "success": False}

        try:
            response = requests.post(
                "https://api.websearchapi.ai/ai-search",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.websearchapi_key}"
                },
                json={
                    "query": query,
                    "maxResults": self.max_results,
                    "includeContent": False,
                    "country": "us",
                    "language": "en"
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return {
                "source": "websearchapi",
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "source": "websearchapi",
                "success": False,
                "error": str(e)
            }

    def search_gemini(self, query: str) -> Optional[Dict[str, Any]]:
        """Search using Gemini with grounding (Google Search)."""
        if not self.gemini_key:
            return {"error": "GEMINI_API_KEY not set", "source": "gemini_search", "success": False}

        last_error = "Unknown error"
        trial_models = list(self.available_gemini_models)
        
        while trial_models:
            model = trial_models[0]
            
            # Try each model up to 3 times
            for attempt in range(1, 4):
                try:
                    response = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                        headers={
                            "x-goog-api-key": self.gemini_key,
                            "Content-Type": "application/json"
                        },
                        json={
                            "contents": [{
                                "parts": [{
                                    "text": f"Search the web and provide comprehensive information about: {query}. Include recent developments, key facts, and relevant sources."
                                }]
                            }],
                            "tools": [{
                                "googleSearch": {}
                            }]
                        },
                        timeout=45
                    )
                    
                    if response.status_code == 429:
                        last_error = "api rate limit!"
                        print(f"  Rate limit hit for {model}, removing from available models...", file=sys.stderr)
                        if model in self.available_gemini_models:
                            self.available_gemini_models.remove(model)
                        break  # Exit retry loop immediately for 429
                    
                    response.raise_for_status()
                    data = response.json()
                    return {
                        "source": "gemini_search",
                        "success": True,
                        "data": data
                    }
                except Exception as e:
                    last_error = str(e)
                    print(f"  Error with {model} (attempt {attempt}/3): {e}", file=sys.stderr)
                    if attempt < 3:
                        time.sleep(3.0)  # Wait before retry
                    else:
                        # All 3 attempts failed for this model
                        print(f"  All attempts failed for {model}, moving to next model...", file=sys.stderr)
            
            # Remove current model from trial list
            trial_models.pop(0)
                
        return {
            "source": "gemini_search",
            "success": False,
            "error": last_error
        }

    def summarize_with_gemini(self, search_results: List[Dict[str, Any]], original_query: str) -> str:
        """Summarize aggregated search results using Gemini."""
        if not self.gemini_key:
            return self._format_raw_results(search_results)

        # Prepare context from all successful searches
        context_parts = []
        for result in search_results:
            if result.get("success"):
                source = result.get("source", "unknown")
                data = result.get("data", {})
                context_parts.append(f"## Results from {source}:\n{json.dumps(data, indent=2)}\n")

        if not context_parts:
            return "# Search Failed\n\nNo successful results from any search source."

        context = "\n".join(context_parts)

        # Create summarization prompt
        prompt = f"""You are a research assistant helping an AI agent. I've gathered search results from multiple sources about this query:

**Query:** {original_query}

**Aggregated Search Results:**
{context}

Please provide a well-structured summary in Markdown format following these guidelines:

**Output Length Strategy:**
- For simple factual queries (weather, time, definitions): 2-4 concise sentences
- For "what is" or "how to" questions: 1-2 short paragraphs with key points
- For lists (trending repos, top tools, comparisons): Table or bullet list with name + brief description (1 line each)
- For research topics: 3-5 paragraphs covering main aspects, avoid excessive detail
- For news/events: Key facts, dates, and outcomes only

**Content Requirements:**
1. Synthesize information from all sources - remove duplicates
2. Preserve factual accuracy (numbers, dates, names, URLs)
3. For projects/tools: Include name, one-line description, and URL if available
4. Organize logically with clear headings if needed
5. Be concise but informative - optimize for an AI agent to quickly understand and act

**Critical:** Do NOT write lengthy introductions or conclusions. Get straight to the facts. Prioritize actionable, structured information over narrative prose."""

        trial_models = list(self.available_gemini_models)
        
        while trial_models:
            model = trial_models[0]
            
            # Try each model up to 3 times
            for attempt in range(1, 4):
                try:
                    response = requests.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                        headers={
                            "x-goog-api-key": self.gemini_key,
                            "Content-Type": "application/json"
                        },
                        json={
                            "contents": [{
                                "parts": [{
                                    "text": prompt
                                }]
                            }]
                        },
                        timeout=60
                    )
                    
                    if response.status_code == 429:
                        print(f"  Rate limit hit for {model} (summarization), removing from available models...", file=sys.stderr)
                        if model in self.available_gemini_models:
                            self.available_gemini_models.remove(model)
                        break  # Exit retry loop immediately for 429
                    
                    response.raise_for_status()
                    data = response.json()

                    # Extract text from Gemini response
                    if "candidates" in data and len(data["candidates"]) > 0:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            if len(parts) > 0 and "text" in parts[0]:
                                return parts[0]["text"]
                except Exception as e:
                    print(f"Warning: Gemini summarization with {model} failed (attempt {attempt}/3): {e}", file=sys.stderr)
                    if attempt < 3:
                        time.sleep(3.0)  # Wait before retry
            
            # Remove current model from trial list after all attempts
            trial_models.pop(0)

        # If we reach here, all models failed or were rate limited
        raw_results = self._format_raw_results(search_results)
        return f"{raw_results}\n\n---\n**Note:** All Gemini models reached rate limits or failed. Showing raw search results instead."

    def _format_raw_results(self, search_results: List[Dict[str, Any]]) -> str:
        """Fallback: Format raw results as markdown."""
        output = ["# Search Online Results\n"]

        for result in search_results:
            source = result.get("source", "unknown")
            output.append(f"## {source.title()}\n")

            if result.get("success"):
                output.append("**Status:** Success\n")
                output.append(f"```json\n{json.dumps(result.get('data', {}), indent=2)}\n```\n")
            else:
                output.append("**Status:** Failed\n")
                output.append(f"**Error:** {result.get('error', 'Unknown error')}\n")

        return "\n".join(output)

    def search(self, query: str) -> str:
        """
        Perform multi-source search and return summarized results.

        Args:
            query: Search query string

        Returns:
            Markdown-formatted summary of search results
        """
        print(f"Searching for: {query}", file=sys.stderr)

        # Execute all searches concurrently
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self.search_tavily, query): "tavily",
                executor.submit(self.search_websearchapi, query): "websearchapi",
                executor.submit(self.search_gemini, query): "gemini_search"
            }

            for future in as_completed(futures):
                source_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        status = "✓" if result.get("success") else "✗"
                        print(f"{status} {source_name}", file=sys.stderr)
                except Exception as e:
                    print(f"✗ {source_name}: {e}", file=sys.stderr)
                    results.append({
                        "source": source_name,
                        "success": False,
                        "error": str(e)
                    })

        # Check if at least one search succeeded
        successful_results = [r for r in results if r.get("success")]
        if not successful_results:
            return "# Search Failed\n\nAll search sources failed. Please check your API keys and internet connection."

        print(f"\nSummarizing {len(successful_results)} successful results...", file=sys.stderr)

        # Summarize results with Gemini
        summary = self.summarize_with_gemini(results, query)
        return summary


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python search_online.py <search query> [max_results]", file=sys.stderr)
        print("\nArguments:", file=sys.stderr)
        print("  search query: Your search query (required)", file=sys.stderr)
        print("  max_results: Maximum results per source, 1-10 (default: 5)", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  GEMINI_API_KEY (required for summarization)", file=sys.stderr)
        print("  TAVILY_API_KEY (optional)", file=sys.stderr)
        print("  WEBSEARCHAPI_KEY (optional)", file=sys.stderr)
        sys.exit(1)

    # Parse max_results if provided
    max_results = 5
    if len(sys.argv) > 2 and sys.argv[-1].isdigit():
        max_results = int(sys.argv[-1])
        query = " ".join(sys.argv[1:-1])
    else:
        query = " ".join(sys.argv[1:])

    searcher = WebSearch(max_results=max_results)
    result = searcher.search(query)
    print(result)


if __name__ == "__main__":
    main()
