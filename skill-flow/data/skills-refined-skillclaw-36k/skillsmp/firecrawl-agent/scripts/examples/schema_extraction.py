#!/usr/bin/env python3
"""
Example: Extract structured data using custom schemas.

This example demonstrates how to use Pydantic models to define
schemas for structured data extraction with Firecrawl Agent.
"""

import json
import os
import sys
from typing import List, Optional

try:
    from pydantic import BaseModel, Field
    from firecrawl import FirecrawlApp
except ImportError as e:
    print(f"Error: Missing dependency. Run: pip install firecrawl-py pydantic")
    print(f"Details: {e}")
    sys.exit(1)


# ============================================================================
# Example Pydantic Schemas
# ============================================================================

class PricingTier(BaseModel):
    """A single pricing tier/plan."""
    name: str = Field(description="Name of the pricing tier (e.g., 'Free', 'Pro', 'Enterprise')")
    price: str = Field(description="Price (e.g., '$10/month', 'Free', 'Contact sales')")
    billing_cycle: Optional[str] = Field(default=None, description="Billing cycle (monthly, yearly)")
    features: List[str] = Field(default_factory=list, description="List of features included")
    limits: Optional[str] = Field(default=None, description="Any limits or quotas")


class ProductPricing(BaseModel):
    """Complete pricing information for a product."""
    product_name: str = Field(description="Name of the product")
    pricing_model: str = Field(description="Type of pricing (freemium, subscription, usage-based, etc.)")
    tiers: List[PricingTier] = Field(default_factory=list, description="Available pricing tiers")
    free_trial: Optional[str] = Field(default=None, description="Free trial information")
    discounts: Optional[str] = Field(default=None, description="Available discounts (annual, education, etc.)")


class TeamMember(BaseModel):
    """A team member or founder."""
    name: str = Field(description="Full name")
    role: str = Field(description="Job title or role")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    background: Optional[str] = Field(default=None, description="Brief background or previous companies")


class CompanyTeam(BaseModel):
    """Company leadership and team information."""
    company_name: str = Field(description="Name of the company")
    founders: List[TeamMember] = Field(default_factory=list, description="Company founders")
    leadership: List[TeamMember] = Field(default_factory=list, description="Current leadership team")
    team_size: Optional[str] = Field(default=None, description="Total team size")


# ============================================================================
# Extraction Functions
# ============================================================================

def extract_pricing(product_name: str) -> dict:
    """
    Extract pricing information for a product.

    Args:
        product_name: Name of the product to research

    Returns:
        Structured pricing information
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set")

    app = FirecrawlApp(api_key=api_key)

    # Convert Pydantic model to JSON schema
    schema = ProductPricing.model_json_schema()

    prompt = f"""
    Find the complete pricing information for {product_name}.
    Include all pricing tiers, what's included in each tier,
    any free trial offers, and available discounts.
    """

    result = app.agent(
        prompt=prompt,
        schema=schema,
        model="spark-1-mini",
        maxCredits=30
    )

    return result


def extract_team(company_name: str) -> dict:
    """
    Extract team and leadership information for a company.

    Args:
        company_name: Name of the company to research

    Returns:
        Structured team information
    """
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY environment variable not set")

    app = FirecrawlApp(api_key=api_key)

    # Convert Pydantic model to JSON schema
    schema = CompanyTeam.model_json_schema()

    prompt = f"""
    Find information about {company_name}'s team:
    - Who are the founders and their backgrounds
    - Current leadership team (CEO, CTO, etc.)
    - Approximate team size
    """

    result = app.agent(
        prompt=prompt,
        schema=schema,
        model="spark-1-mini",
        maxCredits=30
    )

    return result


def main():
    """Main entry point with example usage."""
    print("Schema Extraction Examples")
    print("=" * 50)

    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python schema_extraction.py pricing <product_name>")
        print("  python schema_extraction.py team <company_name>")
        print("\nExamples:")
        print("  python schema_extraction.py pricing Notion")
        print("  python schema_extraction.py team Anthropic")
        sys.exit(1)

    extraction_type = sys.argv[1].lower()
    target = sys.argv[2]

    try:
        if extraction_type == "pricing":
            print(f"\nExtracting pricing for: {target}")
            result = extract_pricing(target)
        elif extraction_type == "team":
            print(f"\nExtracting team info for: {target}")
            result = extract_team(target)
        else:
            print(f"Unknown extraction type: {extraction_type}")
            print("Valid types: pricing, team")
            sys.exit(1)

        print("\nResult:")
        print(json.dumps(result, indent=2, default=str))

    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
