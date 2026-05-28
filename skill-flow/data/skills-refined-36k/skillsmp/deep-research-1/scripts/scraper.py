#!/usr/bin/env python3
"""
Web Scraper Module - Extract clean text from URLs

Standalone module for deep-research skill.
"""

import logging

logger = logging.getLogger(__name__)

# Optional imports with fallback
_requests_available = False
_bs4_available = False

try:
    import requests

    _requests_available = True
except ImportError:
    requests = None

try:
    from bs4 import BeautifulSoup

    _bs4_available = True
except ImportError:
    BeautifulSoup = None


class WebScraper:
    """Fetches and extracts clean text from URLs."""

    def __init__(self, timeout: int = 10):
        """Initialize the scraper.

        Args:
            timeout: Request timeout in seconds.
        """
        if not _requests_available:
            raise ImportError("requests not installed. Run: pip install requests")
        if not _bs4_available:
            raise ImportError(
                "beautifulsoup4 not installed. Run: pip install beautifulsoup4"
            )

        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_content(self, url: str) -> str:
        """Fetch URL and return clean text content.

        Args:
            url: Target URL.

        Returns:
            Cleaned text string. Empty string on failure.
        """
        if requests is None or BeautifulSoup is None:
            return ""

        try:
            logger.info(f"Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted elements
            for tag in soup(
                ["script", "style", "nav", "footer", "header", "iframe", "noscript"]
            ):
                tag.decompose()

            # Extract text
            text = soup.get_text(separator="\n\n")

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return ""
