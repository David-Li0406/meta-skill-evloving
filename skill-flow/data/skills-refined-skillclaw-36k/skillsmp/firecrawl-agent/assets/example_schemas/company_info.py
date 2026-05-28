"""
Company Information Schema

Ready-to-use Pydantic models for extracting company information
using Firecrawl Agent.

Usage:
    from company_info import CompanyInfo
    schema = CompanyInfo.model_json_schema()
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Founder(BaseModel):
    """Information about a company founder."""
    name: str = Field(description="Full name of the founder")
    role: str = Field(description="Current role/title at the company")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    background: Optional[str] = Field(
        default=None,
        description="Brief background (previous companies, education)"
    )


class FundingRound(BaseModel):
    """Details of a single funding round."""
    round_type: str = Field(description="Type of round (Seed, Series A, B, etc.)")
    amount: str = Field(description="Amount raised (e.g., '$50M')")
    date: Optional[str] = Field(default=None, description="Date of the round")
    lead_investors: Optional[List[str]] = Field(
        default=None,
        description="Lead investors in this round"
    )


class FundingInfo(BaseModel):
    """Complete funding information for a company."""
    total_raised: str = Field(description="Total funding raised (e.g., '$200M')")
    latest_round: Optional[str] = Field(default=None, description="Most recent round type")
    latest_round_date: Optional[str] = Field(default=None, description="Date of most recent round")
    rounds: Optional[List[FundingRound]] = Field(
        default=None,
        description="List of funding rounds"
    )
    investors: Optional[List[str]] = Field(
        default=None,
        description="List of notable investors"
    )


class CompanyInfo(BaseModel):
    """
    Comprehensive company information schema.

    This schema extracts detailed information about a company including
    founding details, team, funding, products, and competitive landscape.
    """
    # Basic Information
    name: str = Field(description="Official company name")
    description: str = Field(description="Brief description of what the company does")
    tagline: Optional[str] = Field(default=None, description="Company tagline or slogan")

    # Founding & History
    founded_year: Optional[int] = Field(default=None, description="Year the company was founded")
    founders: Optional[List[Founder]] = Field(default=None, description="Company founders")

    # Location & Size
    headquarters: Optional[str] = Field(default=None, description="HQ location (city, country)")
    employee_count: Optional[str] = Field(
        default=None,
        description="Approximate employee count (e.g., '100-500')"
    )
    offices: Optional[List[str]] = Field(default=None, description="Office locations")

    # Funding
    funding: Optional[FundingInfo] = Field(default=None, description="Funding information")

    # Products & Services
    products: Optional[List[str]] = Field(
        default=None,
        description="Main products or services offered"
    )
    target_market: Optional[str] = Field(
        default=None,
        description="Target market or customer segment"
    )

    # Technology
    tech_stack: Optional[List[str]] = Field(
        default=None,
        description="Known technologies used"
    )

    # Competition
    competitors: Optional[List[str]] = Field(
        default=None,
        description="Main competitors"
    )

    # Online Presence
    website: Optional[str] = Field(default=None, description="Company website URL")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn company page")
    twitter: Optional[str] = Field(default=None, description="Twitter/X handle")


class CompanyInfoBasic(BaseModel):
    """
    Simplified company information schema.

    Use this for quick lookups when you only need basic information.
    """
    name: str = Field(description="Company name")
    description: str = Field(description="What the company does")
    founded_year: Optional[int] = Field(default=None, description="Year founded")
    founders: Optional[List[str]] = Field(default=None, description="Founder names")
    headquarters: Optional[str] = Field(default=None, description="HQ location")
    funding_total: Optional[str] = Field(default=None, description="Total funding raised")


# JSON schema exports for direct use with Firecrawl
COMPANY_INFO_SCHEMA = CompanyInfo.model_json_schema()
COMPANY_INFO_BASIC_SCHEMA = CompanyInfoBasic.model_json_schema()


if __name__ == "__main__":
    import json

    print("Full Company Info Schema:")
    print(json.dumps(COMPANY_INFO_SCHEMA, indent=2))
    print("\n" + "=" * 50 + "\n")
    print("Basic Company Info Schema:")
    print(json.dumps(COMPANY_INFO_BASIC_SCHEMA, indent=2))
