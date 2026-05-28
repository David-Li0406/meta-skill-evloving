"""Citation Network Paper Collector package.

Public API:
    Collector - Main coordinator for paper collection and enrichment
    Database - SQLite database operations
    Config, Paper, Author, Venue - Data models

Example:
    from script import Collector, Config

    collector = Collector("./papers.db")
    collector.initialize(["DOI:10.1234/example"])
    collector.run()
"""

# Main classes
# Clients (for dependency injection / testing)
from .clients import (
    OpenAIClient,
    SemanticScholarClient,
    SparqlClient,
    escape_sparql,
)
from .collector import Collector
from .db import Database

# Exceptions
from .exceptions import (
    CollectorError,
    NoAuthorsError,
    NotFoundError,
    RateLimitError,
    SparqlError,
    TemporaryError,
)

# Data models
from .models import (
    Author,
    Config,
    DbStats,
    EnrichedRef,
    Paper,
    PaperRow,
    QueueCandidate,
    Venue,
)

# Schemas (for LLM responses)
from .schemas import (
    ClaimRelationsResponse,
    ExtractionResponse,
)

__all__ = [
    # Main
    'Collector',
    'Database',
    # Models
    'Paper', 'Author', 'Venue', 'Config',
    'QueueCandidate', 'PaperRow', 'EnrichedRef', 'DbStats',
    # Clients
    'SparqlClient', 'SemanticScholarClient', 'OpenAIClient',
    'escape_sparql',
    # Exceptions
    'CollectorError', 'NotFoundError', 'RateLimitError', 'TemporaryError',
    'NoAuthorsError', 'SparqlError',
    # Schemas
    'ClaimRelationsResponse', 'ExtractionResponse',
]
