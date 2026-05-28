"""
Contact Information Schema

Ready-to-use Pydantic models for extracting contact and team information
using Firecrawl Agent.

Usage:
    from contact_info import ContactInfo, TeamInfo
    schema = ContactInfo.model_json_schema()
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    """Physical address information."""
    street: Optional[str] = Field(default=None, description="Street address")
    city: Optional[str] = Field(default=None, description="City")
    state: Optional[str] = Field(default=None, description="State or province")
    country: Optional[str] = Field(default=None, description="Country")
    postal_code: Optional[str] = Field(default=None, description="ZIP or postal code")
    full_address: Optional[str] = Field(
        default=None,
        description="Complete formatted address"
    )


class SocialMedia(BaseModel):
    """Social media profile links."""
    twitter: Optional[str] = Field(default=None, description="Twitter/X URL or handle")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn URL")
    facebook: Optional[str] = Field(default=None, description="Facebook URL")
    instagram: Optional[str] = Field(default=None, description="Instagram URL")
    youtube: Optional[str] = Field(default=None, description="YouTube channel URL")
    github: Optional[str] = Field(default=None, description="GitHub organization URL")


class ContactInfo(BaseModel):
    """
    Comprehensive contact information schema.

    Extracts all contact details including email, phone, address, and social media.
    """
    # Company/Organization
    company_name: str = Field(description="Company or organization name")

    # Email Contacts
    general_email: Optional[str] = Field(default=None, description="General contact email")
    sales_email: Optional[str] = Field(default=None, description="Sales email")
    support_email: Optional[str] = Field(default=None, description="Customer support email")
    press_email: Optional[str] = Field(default=None, description="Press/media email")
    careers_email: Optional[str] = Field(default=None, description="Careers/HR email")

    # Phone
    phone_main: Optional[str] = Field(default=None, description="Main phone number")
    phone_sales: Optional[str] = Field(default=None, description="Sales phone number")
    phone_support: Optional[str] = Field(default=None, description="Support phone number")

    # Address
    headquarters: Optional[Address] = Field(
        default=None,
        description="Headquarters address"
    )
    other_offices: Optional[List[Address]] = Field(
        default=None,
        description="Other office locations"
    )

    # Social Media
    social_media: Optional[SocialMedia] = Field(
        default=None,
        description="Social media profiles"
    )

    # Website
    website: Optional[str] = Field(default=None, description="Main website URL")
    contact_page: Optional[str] = Field(default=None, description="Contact page URL")


class TeamMember(BaseModel):
    """Information about a team member."""
    name: str = Field(description="Full name")
    title: str = Field(description="Job title or role")
    department: Optional[str] = Field(default=None, description="Department")
    email: Optional[str] = Field(default=None, description="Work email")
    phone: Optional[str] = Field(default=None, description="Work phone")
    linkedin: Optional[str] = Field(default=None, description="LinkedIn profile URL")
    twitter: Optional[str] = Field(default=None, description="Twitter/X handle")
    bio: Optional[str] = Field(default=None, description="Brief biography")
    photo_url: Optional[str] = Field(default=None, description="Profile photo URL")


class TeamInfo(BaseModel):
    """
    Company team and leadership information schema.

    Extracts information about the team, leadership, and key personnel.
    """
    company_name: str = Field(description="Company name")

    # Leadership
    ceo: Optional[TeamMember] = Field(default=None, description="CEO information")
    founders: Optional[List[TeamMember]] = Field(
        default=None,
        description="Company founders"
    )
    executives: Optional[List[TeamMember]] = Field(
        default=None,
        description="Executive team (C-suite)"
    )

    # Team
    leadership_team: Optional[List[TeamMember]] = Field(
        default=None,
        description="Leadership/management team"
    )
    team_members: Optional[List[TeamMember]] = Field(
        default=None,
        description="Other notable team members"
    )

    # Team Size
    total_employees: Optional[str] = Field(
        default=None,
        description="Total employee count"
    )
    team_size_by_department: Optional[dict] = Field(
        default=None,
        description="Employee count by department"
    )

    # About Page
    about_page_url: Optional[str] = Field(
        default=None,
        description="Company about/team page URL"
    )


class ContactInfoBasic(BaseModel):
    """
    Simplified contact information schema.

    Use for quick lookups when you only need basic contact details.
    """
    company_name: str = Field(description="Company name")
    email: Optional[str] = Field(default=None, description="Primary email")
    phone: Optional[str] = Field(default=None, description="Primary phone")
    address: Optional[str] = Field(default=None, description="Primary address")
    website: Optional[str] = Field(default=None, description="Website URL")
    social_links: Optional[List[str]] = Field(
        default=None,
        description="Social media profile URLs"
    )


# JSON schema exports for direct use with Firecrawl
CONTACT_INFO_SCHEMA = ContactInfo.model_json_schema()
TEAM_INFO_SCHEMA = TeamInfo.model_json_schema()
CONTACT_INFO_BASIC_SCHEMA = ContactInfoBasic.model_json_schema()


if __name__ == "__main__":
    import json

    print("Contact Info Schema:")
    print(json.dumps(CONTACT_INFO_SCHEMA, indent=2))
    print("\n" + "=" * 50 + "\n")
    print("Team Info Schema:")
    print(json.dumps(TEAM_INFO_SCHEMA, indent=2))
    print("\n" + "=" * 50 + "\n")
    print("Basic Contact Info Schema:")
    print(json.dumps(CONTACT_INFO_BASIC_SCHEMA, indent=2))
