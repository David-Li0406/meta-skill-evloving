"""OpenAlex API client for fetching paper abstracts."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from ..constants import DEFAULT_USER_AGENT

logger = logging.getLogger(__name__)

OPENALEX_API_URL = "https://api.openalex.org"


class OpenAlexClient:
    """OpenAlex API client for fetching abstracts.

    OpenAlex is a free, open catalog of scholarly works with good abstract coverage.
    Rate limit: 100,000 requests per day (no auth required).
    Abstracts are stored as inverted index and reconstructed to plaintext.
    """

    def __init__(self, email: str | None = None):
        """Initialize OpenAlex client.

        Args:
            email: Optional email for polite pool (faster rate limits)
        """
        self.email = email

    def get_abstract(self, doi: str | None = None, openalex_id: str | None = None) -> str | None:
        """Fetch abstract for a paper from OpenAlex.

        Args:
            doi: DOI (e.g., "10.1234/example")
            openalex_id: OpenAlex ID (e.g., "W2741809807")

        Returns:
            Abstract text if found, None otherwise
        """
        if not doi and not openalex_id:
            return None

        # Build URL
        if openalex_id:
            url = f"{OPENALEX_API_URL}/works/{openalex_id}"
        else:
            # Normalize DOI - doi is guaranteed non-None here due to early return above
            assert doi is not None
            clean_doi = doi
            if doi.startswith('https://doi.org/'):
                clean_doi = doi[16:]
            elif doi.startswith('http://doi.org/'):
                clean_doi = doi[15:]
            url = f"{OPENALEX_API_URL}/works/doi:{urllib.parse.quote(clean_doi, safe='')}"

        if self.email:
            url += f"?mailto={urllib.parse.quote(self.email)}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', f"{DEFAULT_USER_AGENT} (mailto:{self.email})" if self.email else DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return self._extract_abstract(data)
        except urllib.error.HTTPError as e:
            logger.debug("OpenAlex HTTP error for %s: %s", doi or openalex_id, e)
            return None
        except urllib.error.URLError as e:
            logger.debug("OpenAlex network error for %s: %s", doi or openalex_id, e)
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.debug("OpenAlex parse error for %s: %s", doi or openalex_id, e)
            return None

    def _extract_abstract(self, data: dict) -> str | None:
        """Extract and reconstruct abstract from OpenAlex response.

        OpenAlex stores abstracts as inverted index due to legal constraints.
        Format: {"word": [position1, position2, ...], ...}
        """
        inverted_index = data.get('abstract_inverted_index')
        if not inverted_index:
            return None

        return self._reconstruct_abstract(inverted_index)

    def _reconstruct_abstract(self, inverted_index: dict[str, list[int]]) -> str | None:
        """Reconstruct plaintext abstract from inverted index.

        Args:
            inverted_index: Dict mapping words to their positions

        Returns:
            Reconstructed abstract text
        """
        # Find max position to size the array
        max_pos = 0
        for positions in inverted_index.values():
            if positions:
                max_pos = max(max_pos, max(positions))

        # Build word array
        words = [''] * (max_pos + 1)
        for word, positions in inverted_index.items():
            for pos in positions:
                words[pos] = word

        # Join with spaces
        abstract = ' '.join(words)

        # Clean up whitespace
        abstract = ' '.join(abstract.split())

        return abstract if abstract else None
