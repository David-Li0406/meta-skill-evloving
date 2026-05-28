"""
Input Validation Models for CMO Agent Tools

Pydantic models for validating API inputs before making requests.
This prevents malformed requests and provides clear error messages.
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
from urllib.parse import urlparse
import re


# ============================================================================
# Common Validators
# ============================================================================

def validate_email(email: str) -> str:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email}")
    return email.lower()


def validate_url(url: str) -> str:
    """Validate and clean URL."""
    if not url:
        raise ValueError("URL cannot be empty")

    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"

    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    return url.rstrip('/')


def validate_domain(domain: str) -> str:
    """Extract and validate domain from URL or domain string."""
    if not domain:
        raise ValueError("Domain cannot be empty")

    # Clean up the input
    domain = domain.strip().lower()

    # If it's a URL, extract the domain
    if domain.startswith(('http://', 'https://')):
        parsed = urlparse(domain)
        domain = parsed.netloc

    # Remove www prefix
    if domain.startswith('www.'):
        domain = domain[4:]

    # Basic domain validation
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, domain):
        raise ValueError(f"Invalid domain format: {domain}")

    return domain


# ============================================================================
# Apollo Models
# ============================================================================

class PeopleSearchRequest(BaseModel):
    """Validate Apollo people search request."""

    titles: Optional[List[str]] = Field(None, description="Job titles to search")
    company: Optional[str] = Field(None, description="Company name")
    company_domains: Optional[List[str]] = Field(None, description="Company domains")
    company_size: Optional[List[str]] = Field(None, description="Company size ranges")
    industries: Optional[List[str]] = Field(None, description="Industry filters")
    locations: Optional[List[str]] = Field(None, description="Location filters")
    seniority: Optional[List[str]] = Field(None, description="Seniority levels")
    keywords: Optional[str] = Field(None, description="Keyword search")
    page: int = Field(1, ge=1, description="Page number")
    limit: int = Field(25, ge=1, le=100, description="Results per page")

    @field_validator('seniority')
    @classmethod
    def validate_seniority(cls, v):
        if v is None:
            return v
        valid = {'c_suite', 'vp', 'director', 'manager', 'senior', 'entry'}
        for s in v:
            if s.lower() not in valid:
                raise ValueError(f"Invalid seniority: {s}. Valid options: {valid}")
        return [s.lower() for s in v]

    @field_validator('company_domains')
    @classmethod
    def validate_domains(cls, v):
        if v is None:
            return v
        return [validate_domain(d) for d in v]


class PersonEnrichRequest(BaseModel):
    """Validate Apollo person enrichment request."""

    email: Optional[str] = Field(None, description="Person's email")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    company_domain: Optional[str] = Field(None, description="Company domain")

    @field_validator('email')
    @classmethod
    def validate_email_field(cls, v):
        if v is None:
            return v
        return validate_email(v)

    @field_validator('linkedin_url')
    @classmethod
    def validate_linkedin(cls, v):
        if v is None:
            return v
        if 'linkedin.com' not in v.lower():
            raise ValueError("Must be a LinkedIn URL")
        return validate_url(v)

    @model_validator(mode='after')
    def check_required_fields(self):
        has_email = self.email is not None
        has_linkedin = self.linkedin_url is not None
        has_name_combo = all([self.first_name, self.last_name, self.company_domain])

        if not (has_email or has_linkedin or has_name_combo):
            raise ValueError(
                "Provide one of: email, linkedin_url, or (first_name + last_name + company_domain)"
            )
        return self


# ============================================================================
# Firecrawl Models
# ============================================================================

class ScrapeRequest(BaseModel):
    """Validate Firecrawl scrape request."""

    url: str = Field(..., description="URL to scrape")
    formats: List[str] = Field(["markdown"], description="Output formats")
    only_main_content: bool = Field(True, description="Extract main content only")
    wait_for: int = Field(0, ge=0, le=30000, description="Wait time in ms")
    timeout: int = Field(30000, ge=1000, le=120000, description="Timeout in ms")

    @field_validator('url')
    @classmethod
    def validate_url_field(cls, v):
        return validate_url(v)

    @field_validator('formats')
    @classmethod
    def validate_formats(cls, v):
        valid = {'markdown', 'html', 'text', 'links', 'screenshot'}
        for fmt in v:
            if fmt.lower() not in valid:
                raise ValueError(f"Invalid format: {fmt}. Valid options: {valid}")
        return [f.lower() for f in v]


class CrawlRequest(BaseModel):
    """Validate Firecrawl crawl request."""

    url: str = Field(..., description="Starting URL")
    max_pages: int = Field(10, ge=1, le=100, description="Maximum pages to crawl")
    include_patterns: Optional[List[str]] = Field(None, description="URL patterns to include")
    exclude_patterns: Optional[List[str]] = Field(None, description="URL patterns to exclude")
    formats: List[str] = Field(["markdown"], description="Output formats")

    @field_validator('url')
    @classmethod
    def validate_url_field(cls, v):
        return validate_url(v)


# ============================================================================
# Ads Models
# ============================================================================

class CampaignCreateRequest(BaseModel):
    """Validate campaign creation request."""

    name: str = Field(..., min_length=1, max_length=255, description="Campaign name")
    budget: float = Field(0, ge=0, description="Daily budget in USD")
    total_budget: float = Field(0, ge=0, description="Total/lifetime budget in USD")
    campaign_type: str = Field("SEARCH", description="Campaign type")
    objective: str = Field("WEBSITE_VISITS", description="Campaign objective")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        # Remove leading/trailing whitespace
        v = v.strip()
        if not v:
            raise ValueError("Campaign name cannot be empty")
        # Check for disallowed characters
        if any(c in v for c in '<>'):
            raise ValueError("Campaign name cannot contain < or >")
        return v

    @field_validator('campaign_type')
    @classmethod
    def validate_campaign_type(cls, v):
        valid_google = {'SEARCH', 'DISPLAY', 'SHOPPING', 'VIDEO', 'PERFORMANCE_MAX'}
        valid_linkedin = {'SPONSORED_UPDATES', 'SPONSORED_INMAILS', 'TEXT_ADS'}
        valid = valid_google | valid_linkedin
        if v.upper() not in valid:
            raise ValueError(f"Invalid campaign type: {v}. Valid options: {valid}")
        return v.upper()


class CampaignUpdateRequest(BaseModel):
    """Validate campaign update request."""

    campaign_id: str = Field(..., description="Campaign ID to update")
    status: Optional[str] = Field(None, description="New status")
    budget: Optional[float] = Field(None, ge=0, description="New daily budget")
    name: Optional[str] = Field(None, description="New name")

    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        valid = {'ENABLED', 'PAUSED', 'ACTIVE', 'DRAFT', 'ARCHIVED', 'REMOVED'}
        if v.upper() not in valid:
            raise ValueError(f"Invalid status: {v}. Valid options: {valid}")
        return v.upper()

    @model_validator(mode='after')
    def check_has_update(self):
        if self.status is None and self.budget is None and self.name is None:
            raise ValueError("At least one update field must be provided")
        return self


class TargetingCriteria(BaseModel):
    """Validate ad targeting criteria."""

    locations: Optional[List[str]] = Field(None, description="Geographic locations")
    industries: Optional[List[str]] = Field(None, description="Industry targets")
    job_titles: Optional[List[str]] = Field(None, description="Job title targets")
    company_sizes: Optional[List[str]] = Field(None, description="Company size ranges")
    seniorities: Optional[List[str]] = Field(None, description="Seniority levels")

    @field_validator('company_sizes')
    @classmethod
    def validate_company_sizes(cls, v):
        if v is None:
            return v
        valid = {'1-10', '11-50', '51-200', '201-500', '501-1000', '1001-5000', '5001+'}
        for size in v:
            if size not in valid:
                raise ValueError(f"Invalid company size: {size}. Valid options: {valid}")
        return v


# ============================================================================
# Validation Helper Functions
# ============================================================================

def validate_people_search(
    titles: Optional[List[str]] = None,
    company: Optional[str] = None,
    company_domains: Optional[List[str]] = None,
    **kwargs
) -> dict:
    """Validate and return cleaned people search parameters."""
    request = PeopleSearchRequest(
        titles=titles,
        company=company,
        company_domains=company_domains,
        **kwargs
    )
    return request.model_dump(exclude_none=True)


def validate_person_enrich(
    email: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    **kwargs
) -> dict:
    """Validate and return cleaned person enrich parameters."""
    request = PersonEnrichRequest(email=email, linkedin_url=linkedin_url, **kwargs)
    return request.model_dump(exclude_none=True)


def validate_scrape(url: str, **kwargs) -> dict:
    """Validate and return cleaned scrape parameters."""
    request = ScrapeRequest(url=url, **kwargs)
    return request.model_dump()


def validate_campaign_create(name: str, budget: float = 0, **kwargs) -> dict:
    """Validate and return cleaned campaign create parameters."""
    request = CampaignCreateRequest(name=name, budget=budget, **kwargs)
    return request.model_dump()


def validate_campaign_update(campaign_id: str, **kwargs) -> dict:
    """Validate and return cleaned campaign update parameters."""
    request = CampaignUpdateRequest(campaign_id=campaign_id, **kwargs)
    return request.model_dump(exclude_none=True)
