"""Semantic Scholar API client."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import NoReturn

from ..constants import DEFAULT_USER_AGENT, SEMANTIC_SCHOLAR_API_URL, SPARQL_TIMEOUT_SECONDS
from ..exceptions import NotFoundError, RateLimitError, TemporaryError
from ..models import Author, Paper, Venue
from .rate_limiter import RateLimiter


def _handle_http_error(e: urllib.error.HTTPError, paper_id: str) -> NoReturn:
    """Handle HTTP errors from Semantic Scholar API."""
    if e.code == 404:
        raise NotFoundError(paper_id) from e
    if e.code == 429:
        retry_after = e.headers.get('Retry-After')
        raise RateLimitError(int(retry_after) if retry_after else 60) from e
    if e.code >= 500:
        raise TemporaryError(f"HTTP {e.code}: {e.reason}", e.code) from e
    raise


class SemanticScholarClient:
    """Semantic Scholar API client.

    Rate limit: 100 requests / 5 minutes (without API key)
    """

    BASE_URL = SEMANTIC_SCHOLAR_API_URL
    FIELDS = ",".join([
        "paperId", "externalIds", "title",
        "authors.authorId", "authors.name", "authors.externalIds",
        "year", "abstract",
        "publicationVenue", "citationCount",
        "references.paperId",
        "citations.paperId"
    ])

    # 100 requests per 5 minutes (300 seconds), minimum 3 seconds between requests
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 300
    MIN_INTERVAL = 3.0

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.rate_limiter = RateLimiter(
            self.RATE_LIMIT_REQUESTS,
            self.RATE_LIMIT_WINDOW,
            self.MIN_INTERVAL
        )

    def get_paper(self, paper_id: str) -> Paper:
        """Fetch paper metadata.

        Args:
            paper_id: Semantic Scholar ID, DOI:xxx, ARXIV:xxx, CorpusId:xxx

        Raises:
            NotFoundError: Paper not found
            RateLimitError: Rate limit exceeded
        """
        # Wait for rate limit
        self.rate_limiter.wait()

        url = f"{self.BASE_URL}/paper/{urllib.parse.quote(paper_id, safe='')}"
        url += f"?fields={self.FIELDS}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', DEFAULT_USER_AGENT)
        if self.api_key:
            req.add_header('x-api-key', self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return self._parse_paper(data)
        except urllib.error.HTTPError as e:
            _handle_http_error(e, paper_id)
        except urllib.error.URLError as e:
            raise TemporaryError(f"Network error: {e.reason}") from e

    def get_citation_contexts(self, paper_id: str) -> list[dict]:
        """Fetch citation contexts for a paper's references.

        Returns list of dicts with:
        - cited_id: S2 paper ID of cited paper
        - intents: list of citation intents (background, methodology, result)
        - contexts: list of text snippets where citation occurs

        Args:
            paper_id: Semantic Scholar paper ID

        Raises:
            NotFoundError: Paper not found
            RateLimitError: Rate limit exceeded
        """
        self.rate_limiter.wait()

        url = f"{self.BASE_URL}/paper/{urllib.parse.quote(paper_id, safe='')}/references"
        url += "?fields=intents,contexts,citedPaper.paperId&limit=100"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', DEFAULT_USER_AGENT)
        if self.api_key:
            req.add_header('x-api-key', self.api_key)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return self._parse_citation_contexts(data)
        except urllib.error.HTTPError as e:
            _handle_http_error(e, paper_id)
        except urllib.error.URLError as e:
            raise TemporaryError(f"Network error: {e.reason}") from e

    def _parse_citation_contexts(self, data: dict) -> list[dict]:
        """Parse citation contexts from API response."""
        results = []
        for item in data.get('data', []):
            cited_paper = item.get('citedPaper') or {}
            cited_id = cited_paper.get('paperId')
            if cited_id:
                results.append({
                    'cited_id': cited_id,
                    'intents': item.get('intents') or [],
                    'contexts': item.get('contexts') or [],
                })
        return results

    def _parse_paper(self, data: dict) -> Paper:
        """Parse API response into Paper object."""
        paper_id = data.get('paperId')
        title = data.get('title')
        if not paper_id or not title:
            raise ValueError("Missing required field: paperId or title")

        # External IDs
        external_ids = data.get('externalIds') or {}
        doi = external_ids.get('DOI')
        arxiv_id = external_ids.get('ArXiv')

        # Authors
        authors = []
        for author_data in (data.get('authors') or []):
            name = author_data.get('name')
            if not name:
                continue
            author_ext_ids = author_data.get('externalIds') or {}
            authors.append(Author(
                name=name,
                author_id=author_data.get('authorId'),
                orcid=author_ext_ids.get('ORCID'),
            ))

        # Venue
        venue = None
        venue_data = data.get('publicationVenue')
        if venue_data and venue_data.get('name'):
            venue = Venue(
                name=venue_data['name'],
                venue_id=venue_data.get('id'),
                venue_type=venue_data.get('type'),
            )

        # References/Citations
        references = [
            ref['paperId'] for ref in (data.get('references') or [])
            if ref and ref.get('paperId')
        ]
        citations = [
            cit['paperId'] for cit in (data.get('citations') or [])
            if cit and cit.get('paperId')
        ]

        return Paper(
            id=paper_id,
            title=title,
            year=data.get('year'),
            abstract=data.get('abstract'),
            doi=doi,
            arxiv_id=arxiv_id,
            citation_count=data.get('citationCount') or 0,
            authors=authors,
            venue=venue,
            references=references,
            citations=citations,
        )
