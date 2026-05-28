"""GraphDB SPARQL client."""

from __future__ import annotations

import json
import logging
import random
import string
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from ..constants import (
    DEFAULT_USER_AGENT,
    GRAPHDB_API_URL,
    SPARQL_TIMEOUT_SECONDS,
    URI_GENERATION_MAX_RETRIES,
    URI_HASH_LENGTH,
)
from ..exceptions import SparqlError

logger = logging.getLogger(__name__)


class SparqlClient:
    """GraphDB SPARQL client.

    Endpoints:
    - Query: {GRAPHDB_API_URL}/{repo}
    - Insert: {GRAPHDB_API_URL}/{repo}/statements
    """

    BASE_URL = GRAPHDB_API_URL

    def __init__(self, repo: str = "kg2"):
        self.repo = repo
        self.query_endpoint = f"{self.BASE_URL}/{repo}"
        self.update_endpoint = f"{self.BASE_URL}/{repo}/statements"

    def query(self, sparql: str) -> list[dict[str, Any]]:
        """Execute SELECT query, return result bindings."""
        url = f"{self.query_endpoint}?query={urllib.parse.quote(sparql)}"
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/sparql-results+json')
        req.add_header('User-Agent', DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('results', {}).get('bindings', [])
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise SparqlError(body, e.code) from e

    def ask(self, sparql: str) -> bool:
        """Execute ASK query."""
        url = f"{self.query_endpoint}?query={urllib.parse.quote(sparql)}"
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/sparql-results+json')
        req.add_header('User-Agent', DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                return data.get('boolean', False)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise SparqlError(body, e.code) from e

    def insert_turtle(self, turtle: str) -> None:
        """Insert Turtle data."""
        data = turtle.encode('utf-8')
        req = urllib.request.Request(self.update_endpoint, data=data, method='POST')
        req.add_header('Content-Type', 'text/turtle')
        req.add_header('User-Agent', DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS):
                pass  # Success
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise SparqlError(body, e.code) from e

    def insert_turtle_silent(self, turtle: str) -> bool:
        """Insert Turtle data, logging but not raising errors.

        Returns:
            True if successful, False if error occurred
        """
        try:
            self.insert_turtle(turtle)
            return True
        except SparqlError as e:
            logger.debug("SPARQL insert failed: %s (turtle: %s...)", e, turtle[:100])
            return False

    def update(self, sparql_update: str) -> None:
        """Execute SPARQL UPDATE query (DELETE/INSERT).

        Args:
            sparql_update: SPARQL UPDATE query string
        """
        data = sparql_update.encode('utf-8')
        req = urllib.request.Request(self.update_endpoint, data=data, method='POST')
        req.add_header('Content-Type', 'application/sparql-update')
        req.add_header('User-Agent', DEFAULT_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=SPARQL_TIMEOUT_SECONDS):
                pass  # Success
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise SparqlError(body, e.code) from e

    def uri_exists(self, uri: str) -> bool:
        """Check if URI exists."""
        return self.ask(f"ASK {{ <{uri}> ?p ?o }}")

    def generate_uri(self, prefix: str) -> str:
        """Generate opaque URI. Retry on collision."""
        from ..turtle_builders import expand_prefixed_uri
        for _ in range(URI_GENERATION_MAX_RETRIES):
            hash_str = ''.join(random.choices(
                string.ascii_lowercase + string.digits, k=URI_HASH_LENGTH
            ))
            uri = f"paper:{prefix}_{hash_str}"
            full_uri = expand_prefixed_uri(uri)
            if not self.uri_exists(full_uri):
                return uri
        raise RuntimeError(
            f"Failed to generate unique URI after {URI_GENERATION_MAX_RETRIES} attempts"
        )


def escape_sparql(s: str | None) -> str:
    """Escape string for SPARQL/Turtle literal."""
    if not s:
        return ""
    return (s
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('\t', '\\t'))
