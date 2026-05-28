"""Collector exceptions."""
from __future__ import annotations


class CollectorError(Exception):
    """Base collector exception."""


class NotFoundError(CollectorError):
    """Paper not found."""

    def __init__(self, paper_id: str):
        self.paper_id = paper_id
        super().__init__(f"Paper not found: {paper_id}")


class RateLimitError(CollectorError):
    """API rate limit exceeded."""

    def __init__(self, retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after: {retry_after}s")


class NoAuthorsError(CollectorError):
    """Paper has no authors (cannot insert to kg2)."""

    def __init__(self, paper_id: str):
        self.paper_id = paper_id
        super().__init__(f"Paper has no authors: {paper_id}")


class TemporaryError(CollectorError):
    """Temporary API error (5xx, timeout, etc). Should retry."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class SparqlError(CollectorError):
    """SPARQL query/insert error."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(f"SPARQL error ({status_code}): {message}")


class EnrichmentError(CollectorError):
    """Enrichment failed (LLM extraction error)."""

    def __init__(self, paper_id: str, message: str):
        self.paper_id = paper_id
        super().__init__(f"Enrichment failed for {paper_id}: {message}")
