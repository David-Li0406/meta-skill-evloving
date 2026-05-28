"""
Unit tests for tools/validation.py - Input validation models.

Tests cover:
- Email validation
- URL validation and cleaning
- Domain extraction
- Apollo request validation
- Firecrawl request validation
- Ads campaign validation
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from validation import (
    validate_email,
    validate_url,
    validate_domain,
    PeopleSearchRequest,
    PersonEnrichRequest,
    ScrapeRequest,
    CrawlRequest,
    CampaignCreateRequest,
    CampaignUpdateRequest,
    TargetingCriteria,
    validate_people_search,
    validate_person_enrich,
    validate_scrape,
    validate_campaign_create,
    validate_campaign_update
)
from pydantic import ValidationError


# ============================================================================
# Basic Validator Tests
# ============================================================================

class TestEmailValidator:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test valid email addresses."""
        assert validate_email("test@example.com") == "test@example.com"
        assert validate_email("user.name@company.co.uk") == "user.name@company.co.uk"
        assert validate_email("User@Example.COM") == "user@example.com"  # Lowercased

    def test_invalid_email(self):
        """Test invalid email addresses raise ValueError."""
        with pytest.raises(ValueError):
            validate_email("not-an-email")

        with pytest.raises(ValueError):
            validate_email("missing@domain")

        with pytest.raises(ValueError):
            validate_email("@nodomain.com")


class TestURLValidator:
    """Tests for URL validation."""

    def test_adds_https(self):
        """Test that https:// is added to bare domains."""
        assert validate_url("example.com") == "https://example.com"
        assert validate_url("www.example.com") == "https://www.example.com"

    def test_preserves_protocol(self):
        """Test existing protocols are preserved."""
        assert validate_url("https://example.com") == "https://example.com"
        assert validate_url("http://example.com") == "http://example.com"

    def test_removes_trailing_slash(self):
        """Test trailing slashes are removed."""
        assert validate_url("https://example.com/") == "https://example.com"

    def test_empty_url_raises(self):
        """Test empty URL raises ValueError."""
        with pytest.raises(ValueError):
            validate_url("")


class TestDomainValidator:
    """Tests for domain extraction and validation."""

    def test_extracts_from_url(self):
        """Test domain extraction from full URLs."""
        assert validate_domain("https://www.example.com/page") == "example.com"
        assert validate_domain("http://api.example.com") == "api.example.com"

    def test_removes_www(self):
        """Test www prefix is removed."""
        assert validate_domain("www.example.com") == "example.com"
        assert validate_domain("https://www.example.com") == "example.com"

    def test_handles_bare_domain(self):
        """Test bare domain input."""
        assert validate_domain("example.com") == "example.com"

    def test_invalid_domain(self):
        """Test invalid domains raise ValueError."""
        with pytest.raises(ValueError):
            validate_domain("")

        with pytest.raises(ValueError):
            validate_domain("not a domain")


# ============================================================================
# Apollo Model Tests
# ============================================================================

class TestPeopleSearchRequest:
    """Tests for PeopleSearchRequest model."""

    def test_basic_request(self):
        """Test basic people search request."""
        request = PeopleSearchRequest(
            titles=["VP Marketing"],
            limit=25
        )
        assert request.titles == ["VP Marketing"]
        assert request.limit == 25

    def test_limit_capped_at_100(self):
        """Test limit is capped at 100."""
        with pytest.raises(ValidationError):
            PeopleSearchRequest(limit=500)

    def test_seniority_validation(self):
        """Test seniority values are validated."""
        request = PeopleSearchRequest(seniority=["C_Suite", "VP"])
        assert request.seniority == ["c_suite", "vp"]

        with pytest.raises(ValidationError):
            PeopleSearchRequest(seniority=["invalid_level"])

    def test_domain_validation(self):
        """Test company domains are validated."""
        request = PeopleSearchRequest(company_domains=["https://example.com"])
        assert request.company_domains == ["example.com"]


class TestPersonEnrichRequest:
    """Tests for PersonEnrichRequest model."""

    def test_with_email(self):
        """Test enrichment with email."""
        request = PersonEnrichRequest(email="test@example.com")
        assert request.email == "test@example.com"

    def test_with_linkedin(self):
        """Test enrichment with LinkedIn URL."""
        request = PersonEnrichRequest(
            linkedin_url="https://linkedin.com/in/johndoe"
        )
        assert "linkedin.com" in request.linkedin_url

    def test_with_name_combo(self):
        """Test enrichment with name + domain."""
        request = PersonEnrichRequest(
            first_name="John",
            last_name="Doe",
            company_domain="example.com"
        )
        assert request.first_name == "John"

    def test_requires_identifier(self):
        """Test that at least one identifier is required."""
        with pytest.raises(ValidationError):
            PersonEnrichRequest()

        with pytest.raises(ValidationError):
            PersonEnrichRequest(first_name="John")  # Missing last_name and domain


# ============================================================================
# Firecrawl Model Tests
# ============================================================================

class TestScrapeRequest:
    """Tests for ScrapeRequest model."""

    def test_basic_request(self):
        """Test basic scrape request."""
        request = ScrapeRequest(url="example.com")
        assert request.url == "https://example.com"
        assert request.formats == ["markdown"]

    def test_format_validation(self):
        """Test format values are validated."""
        request = ScrapeRequest(url="example.com", formats=["HTML", "Markdown"])
        assert request.formats == ["html", "markdown"]

        with pytest.raises(ValidationError):
            ScrapeRequest(url="example.com", formats=["invalid"])

    def test_timeout_bounds(self):
        """Test timeout has bounds."""
        with pytest.raises(ValidationError):
            ScrapeRequest(url="example.com", timeout=500)  # Too low

        with pytest.raises(ValidationError):
            ScrapeRequest(url="example.com", timeout=500000)  # Too high


class TestCrawlRequest:
    """Tests for CrawlRequest model."""

    def test_basic_request(self):
        """Test basic crawl request."""
        request = CrawlRequest(url="example.com", max_pages=20)
        assert request.url == "https://example.com"
        assert request.max_pages == 20

    def test_max_pages_bounds(self):
        """Test max_pages has bounds."""
        with pytest.raises(ValidationError):
            CrawlRequest(url="example.com", max_pages=0)

        with pytest.raises(ValidationError):
            CrawlRequest(url="example.com", max_pages=500)


# ============================================================================
# Ads Model Tests
# ============================================================================

class TestCampaignCreateRequest:
    """Tests for CampaignCreateRequest model."""

    def test_basic_request(self):
        """Test basic campaign creation."""
        request = CampaignCreateRequest(name="Test Campaign")
        assert request.name == "Test Campaign"
        assert request.budget == 0  # Default

    def test_name_validation(self):
        """Test campaign name validation."""
        # Whitespace trimmed
        request = CampaignCreateRequest(name="  Test  ")
        assert request.name == "Test"

        # Empty name rejected
        with pytest.raises(ValidationError):
            CampaignCreateRequest(name="")

        with pytest.raises(ValidationError):
            CampaignCreateRequest(name="   ")

        # Disallowed characters
        with pytest.raises(ValidationError):
            CampaignCreateRequest(name="<script>bad</script>")

    def test_budget_non_negative(self):
        """Test budget cannot be negative."""
        with pytest.raises(ValidationError):
            CampaignCreateRequest(name="Test", budget=-100)

    def test_campaign_type_validation(self):
        """Test campaign type validation."""
        request = CampaignCreateRequest(name="Test", campaign_type="search")
        assert request.campaign_type == "SEARCH"

        with pytest.raises(ValidationError):
            CampaignCreateRequest(name="Test", campaign_type="invalid")


class TestCampaignUpdateRequest:
    """Tests for CampaignUpdateRequest model."""

    def test_status_update(self):
        """Test status update validation."""
        request = CampaignUpdateRequest(
            campaign_id="123",
            status="paused"
        )
        assert request.status == "PAUSED"

    def test_requires_update_field(self):
        """Test that at least one update field is required."""
        with pytest.raises(ValidationError):
            CampaignUpdateRequest(campaign_id="123")

    def test_invalid_status(self):
        """Test invalid status is rejected."""
        with pytest.raises(ValidationError):
            CampaignUpdateRequest(campaign_id="123", status="invalid")


class TestTargetingCriteria:
    """Tests for TargetingCriteria model."""

    def test_company_size_validation(self):
        """Test company size values are validated."""
        request = TargetingCriteria(company_sizes=["1-10", "51-200"])
        assert request.company_sizes == ["1-10", "51-200"]

        with pytest.raises(ValidationError):
            TargetingCriteria(company_sizes=["1-100"])  # Invalid range


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestHelperFunctions:
    """Tests for validation helper functions."""

    def test_validate_people_search(self):
        """Test validate_people_search helper."""
        result = validate_people_search(
            titles=["CMO"],
            company_domains=["example.com"],
            limit=50
        )
        assert result["titles"] == ["CMO"]
        assert result["limit"] == 50

    def test_validate_person_enrich(self):
        """Test validate_person_enrich helper."""
        result = validate_person_enrich(email="test@example.com")
        assert result["email"] == "test@example.com"

    def test_validate_scrape(self):
        """Test validate_scrape helper."""
        result = validate_scrape("example.com")
        assert result["url"] == "https://example.com"

    def test_validate_campaign_create(self):
        """Test validate_campaign_create helper."""
        result = validate_campaign_create("Test Campaign", budget=100)
        assert result["name"] == "Test Campaign"
        assert result["budget"] == 100

    def test_validate_campaign_update(self):
        """Test validate_campaign_update helper."""
        result = validate_campaign_update("123", status="PAUSED")
        assert result["campaign_id"] == "123"
        assert result["status"] == "PAUSED"
