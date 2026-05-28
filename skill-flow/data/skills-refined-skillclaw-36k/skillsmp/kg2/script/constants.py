"""Shared constants for the kg2 collector."""

import logging
import time

from .models import ClaimRelation, ConceptRelation

# --- Timeouts (seconds) ---
DB_TIMEOUT_SECONDS = 30.0
DB_BUSY_TIMEOUT_MS = 30000
SPARQL_TIMEOUT_SECONDS = 30
OPENAI_TIMEOUT_SECONDS = 60

# --- HTTP ---
DEFAULT_USER_AGENT = "kg2-collector/1.0"

# --- URI Generation ---
URI_HASH_LENGTH = 8
URI_GENERATION_MAX_RETRIES = 10

# --- Retry/Backoff ---
BACKOFF_MULTIPLIER = 2
BACKOFF_MAX_INIT = 32  # Max backoff during initialization
BACKOFF_MAX_RUN = 64   # Max backoff during run loop

_backoff_logger = logging.getLogger(__name__)


class Backoff:
    """Exponential backoff helper for retry logic."""

    def __init__(
        self,
        initial: int = BACKOFF_MULTIPLIER,
        maximum: int = BACKOFF_MAX_RUN,
        sleep_fn=None,
    ):
        self.initial = initial
        self.maximum = maximum
        self._current = initial
        self._sleep = sleep_fn or time.sleep

    def wait(self, reason: str = "Rate limited") -> None:
        """Sleep with current backoff and increase for next time."""
        _backoff_logger.info("%s. Waiting %ds...", reason, self._current)
        self._sleep(self._current)
        self._current = min(self._current * BACKOFF_MULTIPLIER, self.maximum)

    def reset(self) -> None:
        """Reset backoff to initial value (call on success)."""
        self._current = self.initial

    @property
    def current(self) -> int:
        """Current backoff value in seconds."""
        return self._current

# --- RDF Prefixes ---
PAPER_PREFIX = "https://kg.corca.ai/paper#"
RDFS_PREFIX = "http://www.w3.org/2000/01/rdf-schema#"
XSD_PREFIX = "http://www.w3.org/2001/XMLSchema#"

# Turtle prefix declarations (reusable)
TURTLE_PREFIXES = """@prefix paper: <https://kg.corca.ai/paper#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> ."""

# --- API Endpoints ---
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1"
GRAPHDB_API_URL = "https://kg.corca.ai/repositories"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# --- Model Configuration ---
DEFAULT_OPENAI_MODEL = "gpt-5-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536  # text-embedding-3-small default

# --- Embedding Similarity Thresholds ---
EMBEDDING_THRESHOLD_AUTO_MERGE = 0.95      # Auto-merge without LLM verification
EMBEDDING_THRESHOLD_LLM_VERIFY = 0.88      # LLM verify (conservative: prefer false negatives)
EMBEDDING_THRESHOLD_CLAIM_FILTER = 0.5     # Pre-filter claims for linking

# --- Deduplication Settings ---
DEDUP_MAX_CLUSTER_SIZE = 5  # Clusters larger than this use pairwise verification

# Claim relation definitions for LLM prompts
CLAIM_RELATION_DEFINITIONS = """- extends: This claim builds upon, improves, or generalizes the referenced claim
  Example: "Our method achieves 95% accuracy" extends "The baseline achieves 80% accuracy"
- refutes: This claim contradicts or argues against the referenced claim
  Example: "Attention is not necessary for translation" refutes "Attention is essential for NMT"
- supports: This claim provides additional evidence for the referenced claim
  Example: "We confirm transformers scale well" supports "Large models improve performance\""""

# Concept relation types (derived from Enum for consistency)
CONCEPT_RELATIONS = [r.value for r in ConceptRelation]

# Claim relation types (derived from Enum for consistency)
CLAIM_RELATIONS = [r.value for r in ClaimRelation]
