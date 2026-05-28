"""Enrichment store module for CMM AI Automation.

Provides linkml-store backed data management with entity resolution
using (InChIKey, CAS-RN) composite keys.
"""

from cmm_ai_automation.store.enrichment_store import (
    AUTHORITATIVE_SOURCES,
    EnrichmentStore,
    generate_composite_key,
    parse_composite_key,
)

__all__ = [
    "AUTHORITATIVE_SOURCES",
    "EnrichmentStore",
    "generate_composite_key",
    "parse_composite_key",
]
