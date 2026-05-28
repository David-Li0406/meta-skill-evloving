"""
Unit tests for API client tools: Apollo, Firecrawl, Clearbit, BuiltWith.

Tests cover:
- Client initialization with credentials
- API request formatting
- Response parsing
- Error handling
- CLI interfaces
"""

import os
import sys
import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))


# ============================================================================
# Apollo Client Tests
# ============================================================================

class TestApolloClient:
    """Test suite for Apollo API client."""

    @pytest.fixture
    def apollo_client(self, mock_env_vars):
        """Create Apollo client with mocked credentials."""
        import base
        base._broker = None

        from apollo import ApolloClient
        return ApolloClient()

    def test_client_initialization(self, apollo_client):
        """Test Apollo client initializes correctly."""
        assert apollo_client is not None
        assert apollo_client.BASE_URL == "https://api.apollo.io/v1"

    def test_headers_include_api_key(self, apollo_client, mock_env_vars):
        """Test that headers include X-Api-Key."""
        headers = apollo_client._get_headers()

        assert "X-Api-Key" in headers
        assert headers["X-Api-Key"] == "apollo-test-key-12345"
        assert headers["Content-Type"] == "application/json"

    def test_people_search_payload_construction(self, apollo_client):
        """Test people_search builds correct payload."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"people": [], "pagination": {}}

            apollo_client.people_search(
                titles=["VP Marketing", "CMO"],
                company_size=["50-200"],
                limit=25
            )

            call_args = mock_post.call_args
            assert call_args[0][0] == "/mixed_people/search"

            payload = call_args[1]["json"]
            assert payload["person_titles"] == ["VP Marketing", "CMO"]
            assert payload["organization_num_employees_ranges"] == ["50-200"]
            assert payload["per_page"] == 25

    def test_people_search_respects_max_limit(self, apollo_client):
        """Test people_search caps limit at 100."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"people": [], "pagination": {}}

            apollo_client.people_search(limit=500)

            payload = mock_post.call_args[1]["json"]
            assert payload["per_page"] == 100  # Capped at max

    def test_enrich_person_with_email(self, apollo_client):
        """Test enrich_person with email."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"person": {}}

            apollo_client.enrich_person(email="test@example.com")

            payload = mock_post.call_args[1]["json"]
            assert payload["email"] == "test@example.com"

    def test_enrich_person_with_linkedin(self, apollo_client):
        """Test enrich_person with LinkedIn URL."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"person": {}}

            apollo_client.enrich_person(linkedin_url="https://linkedin.com/in/test")

            payload = mock_post.call_args[1]["json"]
            assert payload["linkedin_url"] == "https://linkedin.com/in/test"

    def test_enrich_person_with_name_and_domain(self, apollo_client):
        """Test enrich_person with name + company domain."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"person": {}}

            apollo_client.enrich_person(
                first_name="John",
                last_name="Doe",
                company_domain="example.com"
            )

            payload = mock_post.call_args[1]["json"]
            assert payload["first_name"] == "John"
            assert payload["last_name"] == "Doe"
            assert payload["domain"] == "example.com"

    def test_enrich_person_raises_on_invalid_input(self, apollo_client):
        """Test enrich_person raises ValueError with insufficient data."""
        with pytest.raises(ValueError) as exc_info:
            apollo_client.enrich_person()

        assert "email" in str(exc_info.value).lower() or "linkedin" in str(exc_info.value).lower()

    def test_company_search_with_domain(self, apollo_client):
        """Test company_search with domain filter."""
        with patch.object(apollo_client, 'post') as mock_post:
            mock_post.return_value = {"organizations": []}

            apollo_client.company_search(domain="https://example.com")

            payload = mock_post.call_args[1]["json"]
            assert "organization_domains" in payload
            assert "example.com" in payload["organization_domains"]

    def test_find_contacts_at_company_by_domain(self, apollo_client, apollo_people_response):
        """Test find_contacts_at_company with domain."""
        with patch.object(apollo_client, 'people_search') as mock_search:
            mock_search.return_value = apollo_people_response

            contacts = apollo_client.find_contacts_at_company(
                company="example.com",
                titles=["VP Marketing"]
            )

            assert len(contacts) == 2
            mock_search.assert_called_once()
            call_args = mock_search.call_args
            assert call_args[1]["company_domains"] == ["example.com"]

    def test_find_contacts_at_company_by_name(self, apollo_client, apollo_people_response):
        """Test find_contacts_at_company with company name."""
        with patch.object(apollo_client, 'people_search') as mock_search:
            mock_search.return_value = apollo_people_response

            contacts = apollo_client.find_contacts_at_company(
                company="Example Corp",
                titles=["CMO"]
            )

            call_args = mock_search.call_args
            assert call_args[1]["company"] == "Example Corp"


# ============================================================================
# Firecrawl Client Tests
# ============================================================================

class TestFirecrawlClient:
    """Test suite for Firecrawl API client."""

    @pytest.fixture
    def firecrawl_client(self, mock_env_vars):
        """Create Firecrawl client with mocked credentials."""
        import base
        base._broker = None

        from firecrawl import FirecrawlClient
        return FirecrawlClient()

    def test_client_initialization(self, firecrawl_client):
        """Test Firecrawl client initializes correctly."""
        assert firecrawl_client.BASE_URL == "https://api.firecrawl.dev/v1"

    def test_headers_include_bearer_token(self, firecrawl_client, mock_env_vars):
        """Test headers include Bearer authorization."""
        headers = firecrawl_client._get_headers()

        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer fc-test-key-12345"

    def test_scrape_builds_correct_payload(self, firecrawl_client):
        """Test scrape method builds correct payload."""
        with patch.object(firecrawl_client, 'post') as mock_post:
            mock_post.return_value = {"success": True, "data": {}}

            firecrawl_client.scrape(
                url="example.com",
                formats=["markdown", "html"],
                only_main_content=True
            )

            payload = mock_post.call_args[1]["json"]
            assert payload["url"] == "https://example.com"
            assert payload["formats"] == ["markdown", "html"]
            assert payload["onlyMainContent"] is True

    def test_scrape_cleans_url(self, firecrawl_client):
        """Test scrape adds https:// and removes trailing slash."""
        with patch.object(firecrawl_client, 'post') as mock_post:
            mock_post.return_value = {"success": True, "data": {}}

            firecrawl_client.scrape(url="example.com/")

            payload = mock_post.call_args[1]["json"]
            assert payload["url"] == "https://example.com"

    def test_screenshot_payload(self, firecrawl_client):
        """Test screenshot builds correct payload."""
        with patch.object(firecrawl_client, 'post') as mock_post:
            mock_post.return_value = {"success": True, "data": {"screenshot": "base64..."}}

            firecrawl_client.screenshot(url="example.com", full_page=True)

            payload = mock_post.call_args[1]["json"]
            assert payload["formats"] == ["screenshot"]
            assert payload["screenshot"]["fullPage"] is True

    def test_extract_links(self, firecrawl_client):
        """Test extract_links calls scrape with links format."""
        with patch.object(firecrawl_client, 'scrape') as mock_scrape:
            mock_scrape.return_value = {
                "success": True,
                "data": {"links": ["https://example.com/page1", "https://example.com/page2"]}
            }

            links = firecrawl_client.extract_links("example.com")

            assert len(links) == 2
            mock_scrape.assert_called_once()
            assert mock_scrape.call_args[1]["formats"] == ["links"]

    def test_crawl_builds_correct_payload(self, firecrawl_client):
        """Test crawl method builds correct payload."""
        with patch.object(firecrawl_client, 'post') as mock_post:
            mock_post.return_value = {"success": True, "id": "crawl-123"}

            firecrawl_client.crawl(
                url="example.com",
                max_pages=20,
                include_patterns=["*/blog/*"]
            )

            payload = mock_post.call_args[1]["json"]
            assert payload["url"] == "https://example.com"
            assert payload["limit"] == 20
            assert payload["includePaths"] == ["*/blog/*"]


# ============================================================================
# Clearbit Client Tests
# ============================================================================

class TestClearbitClient:
    """Test suite for Clearbit API client."""

    @pytest.fixture
    def clearbit_client(self, mock_env_vars):
        """Create Clearbit client with mocked credentials."""
        import base
        base._broker = None

        from clearbit import ClearbitClient
        return ClearbitClient()

    def test_client_initialization(self, clearbit_client):
        """Test Clearbit client initializes correctly."""
        assert clearbit_client.BASE_URL == "https://company.clearbit.com/v2"

    def test_headers_include_bearer_token(self, clearbit_client, mock_env_vars):
        """Test headers include Bearer authorization."""
        headers = clearbit_client._get_headers()

        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer clearbit-test-key-12345"

    def test_enrich_company_extracts_domain(self, clearbit_client):
        """Test enrich_company extracts domain from URL."""
        with patch.object(clearbit_client, 'get') as mock_get:
            mock_get.return_value = {"name": "Example Corp"}

            clearbit_client.enrich_company("https://www.example.com/path")

            call_url = mock_get.call_args[0][0]
            assert "domain=example.com" in call_url

    def test_find_company_by_domain(self, clearbit_client):
        """Test find_company with domain calls enrich_company."""
        with patch.object(clearbit_client, 'enrich_company') as mock_enrich:
            mock_enrich.return_value = {"name": "Test"}

            clearbit_client.find_company(domain="example.com")

            mock_enrich.assert_called_once_with("example.com")

    def test_find_company_by_name(self, clearbit_client):
        """Test find_company with name uses name lookup."""
        with patch.object(clearbit_client, 'get') as mock_get:
            mock_get.return_value = {"name": "Test Corp"}

            clearbit_client.find_company(name="Test Corp")

            call_url = mock_get.call_args[0][0]
            assert "name=Test Corp" in call_url

    def test_find_company_raises_without_input(self, clearbit_client):
        """Test find_company raises ValueError without name or domain."""
        with pytest.raises(ValueError):
            clearbit_client.find_company()

    def test_get_company_tech_stack(self, clearbit_client, clearbit_company_response):
        """Test get_company_tech_stack returns tech list."""
        with patch.object(clearbit_client, 'enrich_company') as mock_enrich:
            mock_enrich.return_value = clearbit_company_response

            tech = clearbit_client.get_company_tech_stack("example.com")

            assert tech == ["React", "AWS", "Stripe", "HubSpot"]

    def test_get_company_metrics(self, clearbit_client, clearbit_company_response):
        """Test get_company_metrics returns metrics dict."""
        with patch.object(clearbit_client, 'enrich_company') as mock_enrich:
            mock_enrich.return_value = clearbit_company_response

            metrics = clearbit_client.get_company_metrics("example.com")

            assert metrics["employees"] == 150
            assert metrics["employeesRange"] == "51-200"


# ============================================================================
# BuiltWith Client Tests
# ============================================================================

class TestBuiltWithClient:
    """Test suite for BuiltWith API client."""

    @pytest.fixture
    def builtwith_client_with_key(self, mock_env_vars):
        """Create BuiltWith client with API key."""
        import base
        base._broker = None

        from builtwith import BuiltWithClient
        return BuiltWithClient()

    @pytest.fixture
    def builtwith_client_scraping(self, clean_env):
        """Create BuiltWith client without API key (uses scraping)."""
        import base
        base._broker = None

        # Mock Firecrawl client to avoid credential requirement
        with patch("builtwith.FirecrawlClient"):
            from builtwith import BuiltWithClient
            return BuiltWithClient()

    def test_client_uses_api_when_key_available(self, mock_env_vars):
        """Test client uses API when key is available."""
        import base
        base._broker = None

        from builtwith import BuiltWithClient
        client = BuiltWithClient()

        assert client._use_scraping is False

    def test_client_falls_back_to_scraping(self, clean_env):
        """Test client falls back to scraping without API key."""
        import base
        base._broker = None

        with patch("builtwith.FirecrawlClient"):
            from builtwith import BuiltWithClient
            client = BuiltWithClient()

            assert client._use_scraping is True

    def test_compare_tech_stacks(self, builtwith_client_with_key):
        """Test compare_tech_stacks returns comparison dict."""
        with patch.object(builtwith_client_with_key, 'lookup') as mock_lookup:
            mock_lookup.side_effect = [
                {"technologies": [{"name": "React"}, {"name": "AWS"}]},
                {"technologies": [{"name": "Vue.js"}, {"name": "AWS"}]}
            ]

            result = builtwith_client_with_key.compare_tech_stacks("site1.com", "site2.com")

            assert "shared" in result
            assert "only_domain1" in result
            assert "only_domain2" in result
            assert "aws" in result["shared"]


# ============================================================================
# TechDetector Tests
# ============================================================================

class TestTechDetector:
    """Test suite for TechDetector (free tech detection)."""

    @pytest.fixture
    def tech_detector(self, mock_env_vars):
        """Create TechDetector with mocked Firecrawl."""
        import base
        base._broker = None

        with patch("builtwith.FirecrawlClient") as mock_firecrawl:
            from builtwith import TechDetector
            detector = TechDetector()
            detector.firecrawl = MagicMock()
            return detector

    def test_detect_finds_google_analytics(self, tech_detector):
        """Test detection of Google Analytics signature."""
        tech_detector.firecrawl.scrape.return_value = {
            "success": True,
            "data": {"html": "<script src='https://google-analytics.com/ga.js'></script>"}
        }

        result = tech_detector.detect("example.com")

        tech_names = [t["name"] for t in result["technologies"]]
        assert "Google Analytics" in tech_names

    def test_detect_finds_multiple_technologies(self, tech_detector):
        """Test detection of multiple technologies."""
        html = """
        <html>
            <script src='https://www.google-analytics.com/analytics.js'></script>
            <script src='https://cdn.hubspot.com/hs-scripts.js'></script>
            <div class='wp-content'></div>
        </html>
        """
        tech_detector.firecrawl.scrape.return_value = {
            "success": True,
            "data": {"html": html}
        }

        result = tech_detector.detect("example.com")

        tech_names = [t["name"] for t in result["technologies"]]
        assert "Google Analytics" in tech_names
        assert "HubSpot" in tech_names
        assert "WordPress" in tech_names

    def test_detect_handles_scrape_failure(self, tech_detector):
        """Test graceful handling of scrape failure."""
        tech_detector.firecrawl.scrape.return_value = {"success": False}

        result = tech_detector.detect("example.com")

        assert "error" in result
        assert result["technologies"] == []


# ============================================================================
# Response Parsing Tests
# ============================================================================

class TestResponseParsing:
    """Test response parsing and data extraction."""

    def test_apollo_people_response_parsing(self, apollo_people_response):
        """Test parsing of Apollo people search response."""
        people = apollo_people_response["people"]

        assert len(people) == 2
        assert people[0]["first_name"] == "John"
        assert people[0]["organization"]["name"] == "Example Corp"

    def test_firecrawl_scrape_response_parsing(self, firecrawl_scrape_response):
        """Test parsing of Firecrawl scrape response."""
        assert firecrawl_scrape_response["success"] is True
        assert "markdown" in firecrawl_scrape_response["data"]
        assert firecrawl_scrape_response["data"]["metadata"]["title"] == "Example Page Title"

    def test_clearbit_company_response_parsing(self, clearbit_company_response):
        """Test parsing of Clearbit company response."""
        assert clearbit_company_response["name"] == "Example Corporation"
        assert clearbit_company_response["metrics"]["employees"] == 150
        assert "React" in clearbit_company_response["tech"]
