"""API clients for external services.

This package provides clients for:
- Semantic Scholar API (paper metadata)
- GraphDB SPARQL endpoint (knowledge graph)
- OpenAI API (LLM structured outputs)
- ArXiv API (paper abstracts)
- CrossRef API (paper abstracts)
- OpenAlex API (paper abstracts)
- DOI scraper (publisher page abstracts)
"""

from __future__ import annotations

from .arxiv import ArxivClient
from .crossref import CrossRefClient
from .doi_scraper import DOIScraperClient
from .openai import OpenAIClient
from .openalex import OpenAlexClient
from .rate_limiter import RateLimiter
from .semantic_scholar import SemanticScholarClient
from .sparql import SparqlClient, escape_sparql

__all__ = [
    "ArxivClient",
    "CrossRefClient",
    "DOIScraperClient",
    "OpenAIClient",
    "OpenAlexClient",
    "RateLimiter",
    "SemanticScholarClient",
    "SparqlClient",
    "escape_sparql",
]
