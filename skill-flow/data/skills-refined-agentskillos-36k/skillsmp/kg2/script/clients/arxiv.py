"""ArXiv API client for fetching paper abstracts."""

from __future__ import annotations

import logging
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from ..constants import DEFAULT_USER_AGENT

logger = logging.getLogger(__name__)

ARXIV_API_URL = "http://export.arxiv.org/api/query"


class ArxivClient:
    """ArXiv API client for fetching abstracts.

    ArXiv API is free and has no authentication required.
    Rate limit: ~3 requests per second recommended.
    """

    def __init__(self):
        pass

    def get_abstract(self, arxiv_id: str) -> str | None:
        """Fetch abstract for a paper from arXiv.

        Args:
            arxiv_id: ArXiv ID (e.g., "1706.03762" or "2301.00001v1")

        Returns:
            Abstract text if found, None otherwise
        """
        # Normalize arxiv_id (remove version suffix for query, keep for matching)
        clean_id = re.sub(r'v\d+$', '', arxiv_id)

        url = f"{ARXIV_API_URL}?id_list={urllib.parse.quote(clean_id)}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                xml_data = resp.read().decode('utf-8')
                return self._parse_abstract(xml_data)
        except urllib.error.HTTPError as e:
            logger.debug("ArXiv HTTP error for %s: %s", arxiv_id, e)
            return None
        except urllib.error.URLError as e:
            logger.debug("ArXiv network error for %s: %s", arxiv_id, e)
            return None
        except ET.ParseError as e:
            logger.debug("ArXiv XML parse error for %s: %s", arxiv_id, e)
            return None

    def _parse_abstract(self, xml_data: str) -> str | None:
        """Parse abstract from arXiv API XML response."""
        # arXiv uses Atom namespace
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
        }

        try:
            root = ET.fromstring(xml_data)

            # Find entry element
            entry = root.find('atom:entry', ns)
            if entry is None:
                return None

            # Find summary (abstract)
            summary = entry.find('atom:summary', ns)
            if summary is None or summary.text is None:
                return None

            # Clean up the abstract (remove extra whitespace)
            abstract = ' '.join(summary.text.split())
            return abstract if abstract else None

        except ET.ParseError:
            return None
