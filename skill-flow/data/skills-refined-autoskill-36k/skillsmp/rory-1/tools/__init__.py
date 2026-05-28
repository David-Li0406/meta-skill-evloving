"""
CMO Agent - Research Tools

Unified interface for all research and data gathering tools.

Usage:
    from tools import (
        FirecrawlClient,
        ApolloClient,
        ClearbitClient,
        ProxycurlClient,
        ReviewScraper,
        RedditClient,
        BuiltWithClient,
        CrunchbaseClient,
    )
    
    # Or import specific functions
    from tools.base import get_credential, has_credential
    from tools.research import research_company, research_competitor
"""

# Base utilities
from tools.base import (
    CredentialBroker,
    get_credential,
    has_credential,
    get_broker,
    BaseAPIClient,
    clean_url,
    extract_domain,
)

# Web scraping
from tools.firecrawl import FirecrawlClient

# Company & contact data
from tools.apollo import ApolloClient
from tools.clearbit import ClearbitClient
from tools.proxycurl import ProxycurlClient

# Review sites
from tools.reviews import ReviewScraper

# Social media
from tools.social import RedditClient, TwitterClient

# Tech detection
from tools.builtwith import BuiltWithClient, TechDetector

# Funding data
from tools.crunchbase import CrunchbaseClient

# High-level research functions
from tools.research import (
    research_company,
    research_competitor,
    research_people,
    research_topic,
)

__all__ = [
    # Base
    "CredentialBroker",
    "get_credential",
    "has_credential",
    "get_broker",
    "BaseAPIClient",
    "clean_url",
    "extract_domain",
    
    # Clients
    "FirecrawlClient",
    "ApolloClient",
    "ClearbitClient",
    "ProxycurlClient",
    "ReviewScraper",
    "RedditClient",
    "TwitterClient",
    "BuiltWithClient",
    "TechDetector",
    "CrunchbaseClient",
    
    # Research functions
    "research_company",
    "research_competitor",
    "research_people",
    "research_topic",
]

__version__ = "0.2.0"
