"""CrossRef API client for fetching paper abstracts."""

from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request

from ..constants import DEFAULT_USER_AGENT

logger = logging.getLogger(__name__)

CROSSREF_API_URL = "https://api.crossref.org/works"


class CrossRefClient:
    """CrossRef API client for fetching abstracts.

    CrossRef API is free but requests a polite pool email.
    Rate limit: ~50 requests per second for polite pool.
    """

    def __init__(self, email: str | None = None):
        """Initialize CrossRef client.

        Args:
            email: Optional email for polite pool (higher rate limits)
        """
        self.email = email

    def get_abstract(self, doi: str) -> str | None:
        """Fetch abstract for a paper from CrossRef.

        Args:
            doi: DOI (e.g., "10.1234/example")

        Returns:
            Abstract text if found, None otherwise
        """
        # Normalize DOI (remove URL prefix if present)
        clean_doi = doi
        if doi.startswith('https://doi.org/'):
            clean_doi = doi[16:]
        elif doi.startswith('http://doi.org/'):
            clean_doi = doi[15:]

        url = f"{CROSSREF_API_URL}/{urllib.parse.quote(clean_doi, safe='')}"
        if self.email:
            url += f"?mailto={urllib.parse.quote(self.email)}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', f"{DEFAULT_USER_AGENT} (mailto:{self.email})" if self.email else DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return self._parse_abstract(data)
        except urllib.error.HTTPError as e:
            logger.debug("CrossRef HTTP error for %s: %s", doi, e)
            return None
        except urllib.error.URLError as e:
            logger.debug("CrossRef network error for %s: %s", doi, e)
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.debug("CrossRef parse error for %s: %s", doi, e)
            return None

    def _parse_abstract(self, data: dict) -> str | None:
        """Parse abstract from CrossRef API JSON response."""
        try:
            message = data.get('message', {})
            abstract = message.get('abstract')

            if not abstract:
                return None

            # CrossRef abstracts often contain JATS XML tags - strip them
            abstract = self._strip_jats_tags(abstract)

            # Clean up whitespace
            abstract = ' '.join(abstract.split())

            return abstract if abstract else None

        except (KeyError, TypeError):
            return None

    def _strip_jats_tags(self, text: str) -> str:
        """Strip JATS XML tags from CrossRef abstract."""
        # Remove common JATS tags like <jats:p>, <jats:italic>, etc.
        text = re.sub(r'<jats:[^>]+>', '', text)
        text = re.sub(r'</jats:[^>]+>', '', text)
        # Also handle generic XML tags
        text = re.sub(r'<[^>]+>', '', text)
        return text
