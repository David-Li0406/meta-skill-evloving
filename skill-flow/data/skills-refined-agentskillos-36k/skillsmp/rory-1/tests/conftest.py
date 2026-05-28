"""
Pytest configuration and shared fixtures for CMO Agent tests.
"""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))
sys.path.insert(0, str(TOOLS_DIR.parent))


# ============================================================================
# Environment Fixtures
# ============================================================================

@pytest.fixture
def mock_env_vars():
    """Provide mock environment variables for testing."""
    env_vars = {
        "FIRECRAWL_API_KEY": "fc-test-key-12345",
        "APOLLO_API_KEY": "apollo-test-key-12345",
        "CLEARBIT_API_KEY": "clearbit-test-key-12345",
        "PROXYCURL_API_KEY": "proxycurl-test-key-12345",
        "BUILTWITH_API_KEY": "builtwith-test-key-12345",
        "GOOGLE_ADS_DEVELOPER_TOKEN": "google-ads-dev-token",
        "GOOGLE_ADS_CLIENT_ID": "google-client-id",
        "GOOGLE_ADS_CLIENT_SECRET": "google-client-secret",
        "GOOGLE_ADS_REFRESH_TOKEN": "google-refresh-token",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "1234567890",
        "LINKEDIN_ACCESS_TOKEN": "linkedin-access-token",
        "LINKEDIN_AD_ACCOUNT_ID": "987654321",
    }
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars


@pytest.fixture
def clean_env():
    """Remove all API keys from environment for testing missing credentials."""
    keys_to_remove = [
        "FIRECRAWL_API_KEY", "APOLLO_API_KEY", "CLEARBIT_API_KEY",
        "PROXYCURL_API_KEY", "BUILTWITH_API_KEY",
        "GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CLIENT_ID",
        "GOOGLE_ADS_CLIENT_SECRET", "GOOGLE_ADS_REFRESH_TOKEN",
        "LINKEDIN_ACCESS_TOKEN", "LINKEDIN_AD_ACCOUNT_ID"
    ]
    original = {k: os.environ.pop(k, None) for k in keys_to_remove}
    yield
    # Restore original values
    for k, v in original.items():
        if v is not None:
            os.environ[k] = v


# ============================================================================
# HTTP Response Fixtures
# ============================================================================

@pytest.fixture
def mock_httpx_client():
    """Mock httpx.Client for testing API clients without network calls."""
    with patch("httpx.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value.__enter__ = MagicMock(return_value=mock_instance)
        mock_client.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_instance


@pytest.fixture
def apollo_people_response():
    """Sample Apollo people search response."""
    return {
        "people": [
            {
                "id": "person-123",
                "first_name": "John",
                "last_name": "Doe",
                "title": "VP of Marketing",
                "email": "john.doe@example.com",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "organization": {
                    "id": "org-456",
                    "name": "Example Corp",
                    "website_url": "https://example.com"
                }
            },
            {
                "id": "person-124",
                "first_name": "Jane",
                "last_name": "Smith",
                "title": "CMO",
                "email": "jane.smith@example.com",
                "linkedin_url": "https://linkedin.com/in/janesmith",
                "organization": {
                    "id": "org-456",
                    "name": "Example Corp",
                    "website_url": "https://example.com"
                }
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 25,
            "total_entries": 2,
            "total_pages": 1
        }
    }


@pytest.fixture
def firecrawl_scrape_response():
    """Sample Firecrawl scrape response."""
    return {
        "success": True,
        "data": {
            "markdown": "# Example Page\n\nThis is sample content from the webpage.",
            "metadata": {
                "title": "Example Page Title",
                "description": "A sample page description",
                "sourceURL": "https://example.com"
            }
        }
    }


@pytest.fixture
def clearbit_company_response():
    """Sample Clearbit company enrichment response."""
    return {
        "id": "company-789",
        "name": "Example Corporation",
        "legalName": "Example Corporation, Inc.",
        "domain": "example.com",
        "description": "A leading example company",
        "foundedYear": 2015,
        "location": "San Francisco, CA",
        "metrics": {
            "employees": 150,
            "employeesRange": "51-200",
            "raised": 25000000,
            "annualRevenue": None,
            "estimatedAnnualRevenue": "$10M-$50M"
        },
        "tech": ["React", "AWS", "Stripe", "HubSpot"],
        "techCategories": ["Frontend", "Cloud", "Payment", "Marketing"]
    }


# ============================================================================
# Ads Configuration Fixtures
# ============================================================================

@pytest.fixture
def ads_config_dict():
    """Sample ads configuration for testing."""
    return {
        "safety": {
            "force_draft_mode": True,
            "require_confirmation": True,
            "destructive_actions": [
                "delete_campaign",
                "enable_campaign",
                "increase_budget"
            ]
        },
        "budgets": {
            "google_ads": {
                "max_daily_budget": 100.0,
                "max_total_budget": 1000.0,
                "max_cpc_bid": 5.00
            },
            "linkedin_ads": {
                "max_daily_budget": 100.0,
                "max_total_budget": 1000.0,
                "max_cpc_bid": 10.00
            }
        },
        "defaults": {
            "google_ads": {
                "status": "PAUSED",
                "bidding_strategy": "MAXIMIZE_CLICKS"
            },
            "linkedin_ads": {
                "status": "DRAFT",
                "objective": "WEBSITE_VISITS"
            }
        }
    }


@pytest.fixture
def zero_budget_config():
    """Configuration with zero budgets (testing mode)."""
    return {
        "safety": {
            "force_draft_mode": True,
            "require_confirmation": True
        },
        "budgets": {
            "google_ads": {
                "max_daily_budget": 0,
                "max_total_budget": 0,
                "max_cpc_bid": 5.00
            },
            "linkedin_ads": {
                "max_daily_budget": 0,
                "max_total_budget": 0
            }
        }
    }
