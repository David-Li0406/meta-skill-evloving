#!/usr/bin/env python3
"""
Firecrawl Agent - Autonomous web research using Firecrawl's agent API.

This script wraps Firecrawl's /agent endpoint to perform autonomous web research
without requiring URLs upfront. The agent searches, navigates, and extracts data
from websites based on natural language prompts.

Usage:
    python firecrawl_agent.py "Your research query"
    python firecrawl_agent.py "Query" --schema '{"key": "type"}'
    python firecrawl_agent.py "Query" --model spark-1-pro --max-credits 100
"""

import argparse
import json
import os
import sys
import time
from typing import Any, Optional

try:
    from firecrawl import FirecrawlApp
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "firecrawl-py not installed. Run: pip install firecrawl-py"
    }))
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Perform autonomous web research using Firecrawl's agent API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Find the founders of Anthropic"
  %(prog)s "Research Stripe" --schema '{"name": "string", "founders": ["string"]}'
  %(prog)s "Compare Notion and Coda" --model spark-1-pro
  %(prog)s "Extract pricing" --urls "https://example.com/pricing"
        """
    )

    parser.add_argument(
        "prompt",
        help="Natural language research query (max 10,000 characters)"
    )

    parser.add_argument(
        "--schema",
        type=str,
        default=None,
        help="JSON schema for structured output (e.g., '{\"key\": \"string\"}')"
    )

    parser.add_argument(
        "--model",
        type=str,
        choices=["spark-1-mini", "spark-1-pro"],
        default="spark-1-mini",
        help="Model to use (default: spark-1-mini)"
    )

    parser.add_argument(
        "--urls",
        type=str,
        default=None,
        help="Comma-separated starting URLs to focus the search"
    )

    parser.add_argument(
        "--max-credits",
        type=int,
        default=50,
        help="Maximum credits to spend (default: 50)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout in seconds for the agent to complete (default: 300)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print status updates while waiting"
    )

    return parser.parse_args()


def validate_prompt(prompt: str) -> None:
    """Validate the research prompt."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    if len(prompt) > 10000:
        raise ValueError(f"Prompt too long ({len(prompt)} chars). Maximum is 10,000 characters.")


def parse_schema(schema_str: Optional[str]) -> Optional[dict]:
    """Parse JSON schema string into a dictionary."""
    if not schema_str:
        return None

    try:
        schema = json.loads(schema_str)
        if not isinstance(schema, dict):
            raise ValueError("Schema must be a JSON object")
        return schema
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON schema: {e}")


def parse_urls(urls_str: Optional[str]) -> Optional[list]:
    """Parse comma-separated URLs into a list."""
    if not urls_str:
        return None

    urls = [url.strip() for url in urls_str.split(",") if url.strip()]
    if not urls:
        return None

    return urls


def run_agent(
    app: FirecrawlApp,
    prompt: str,
    schema: Optional[dict] = None,
    model: str = "spark-1-mini",
    urls: Optional[list] = None,
    max_credits: int = 50,
    timeout: int = 300,
    verbose: bool = False
) -> dict:
    """
    Run the Firecrawl agent with the given parameters.

    Args:
        app: FirecrawlApp instance
        prompt: Research query
        schema: Optional JSON schema for structured output
        model: Model to use (spark-1-mini or spark-1-pro)
        urls: Optional starting URLs
        max_credits: Maximum credits to spend
        timeout: Timeout in seconds
        verbose: Print status updates

    Returns:
        Dictionary with results or error information
    """
    # Build agent parameters
    params = {
        "prompt": prompt,
        "model": model,
        "maxCredits": max_credits,
    }

    if schema:
        params["schema"] = schema

    if urls:
        params["urls"] = urls

    try:
        if verbose:
            print(f"Starting agent with model: {model}", file=sys.stderr)
            print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}", file=sys.stderr)

        # Call the agent API
        result = app.agent(**params)

        # The firecrawl-py library handles polling internally
        # Return the result directly
        return {
            "success": True,
            "status": "completed",
            "data": result.get("data") if isinstance(result, dict) else result,
            "sources": result.get("sources", []) if isinstance(result, dict) else [],
            "credits_used": result.get("creditsUsed", 0) if isinstance(result, dict) else 0
        }

    except Exception as e:
        error_msg = str(e)

        # Provide helpful error messages for common issues
        if "rate limit" in error_msg.lower():
            return {
                "success": False,
                "error": "Rate limit exceeded. Please wait before retrying.",
                "details": error_msg
            }
        elif "credit" in error_msg.lower():
            return {
                "success": False,
                "error": f"Credit limit reached. Current limit: {max_credits}. Try increasing --max-credits.",
                "details": error_msg
            }
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            return {
                "success": False,
                "error": "Invalid API key. Check your FIRECRAWL_API_KEY.",
                "details": error_msg
            }
        else:
            return {
                "success": False,
                "error": "Agent execution failed",
                "details": error_msg
            }


def main():
    """Main entry point."""
    args = parse_args()

    # Check for API key
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print(json.dumps({
            "success": False,
            "error": "FIRECRAWL_API_KEY environment variable not set",
            "help": "Set it with: export FIRECRAWL_API_KEY=your_key_here"
        }, indent=2))
        sys.exit(1)

    try:
        # Validate inputs
        validate_prompt(args.prompt)
        schema = parse_schema(args.schema)
        urls = parse_urls(args.urls)

        # Initialize Firecrawl
        app = FirecrawlApp(api_key=api_key)

        # Run the agent
        result = run_agent(
            app=app,
            prompt=args.prompt,
            schema=schema,
            model=args.model,
            urls=urls,
            max_credits=args.max_credits,
            timeout=args.timeout,
            verbose=args.verbose
        )

        # Output result as JSON
        print(json.dumps(result, indent=2, default=str))

        # Exit with appropriate code
        sys.exit(0 if result.get("success") else 1)

    except ValueError as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": "Unexpected error",
            "details": str(e)
        }, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
