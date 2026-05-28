#!/usr/bin/env python3
"""
Example: Research a company using Firecrawl Agent.

This example demonstrates how to research a company and extract
structured information including founders, funding, and products.
"""

import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from firecrawl import FirecrawlApp
except ImportError:
    print("Error: firecrawl-py not installed. Run: pip install firecrawl-py")
    sys.exit(1)


def research_company(company_name: str) -> dict:
    """
    Research a company and extract structured information.

    Args:
        company_name: Name of the company to research

    Returns:
        Dictionary with company information
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set")

    app = FirecrawlApp(api_key=api_key)

    # Define the schema for structured output
    schema = {
        "company_name": "string",
        "description": "string",
        "founded_year": "number",
        "founders": ["string"],
        "headquarters": "string",
        "employee_count": "string",
        "funding_total": "string",
        "funding_rounds": [
            {
                "round_type": "string",
                "amount": "string",
                "date": "string"
            }
        ],
        "products": ["string"],
        "tech_stack": ["string"],
        "competitors": ["string"]
    }

    prompt = f"""
    Research {company_name} and find comprehensive information including:
    - Company description and what they do
    - When they were founded and by whom
    - Headquarters location
    - Approximate employee count
    - Total funding raised and funding rounds
    - Main products or services
    - Technologies they use
    - Main competitors
    """

    result = app.agent(
        prompt=prompt,
        schema=schema,
        model="spark-1-mini",
        maxCredits=50
    )

    return result


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python company_research.py <company_name>")
        print("Example: python company_research.py Anthropic")
        sys.exit(1)

    company_name = sys.argv[1]
    print(f"Researching {company_name}...")

    try:
        result = research_company(company_name)
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
