"""
Transformation logic for growth preference (strain-medium) data.

This module provides functions to link strains to grounded media nodes
and generate KGX association edges.
"""

from __future__ import annotations

import logging
import re

from cmm_ai_automation.transform.kgx import KGXEdge

logger = logging.getLogger(__name__)

# METPO Predicates
GROWS_IN = "METPO:2000517"
DOES_NOT_GROW_IN = "METPO:2000518"


def extract_placeholder_id(object_uri: str) -> str | None:
    """
    Extract the 7-digit placeholder ID from the mashed object URI.

    Example: 'http://example.com/ber-cmm/media/0000001Hypho medium' -> '0000001'
    """
    match = re.search(r"/media/(\d{7})", object_uri)
    if match:
        return match.group(1)
    return None


def extract_strain_curie(strain_url: str) -> str | None:
    """
    Convert PURL/URL to CURIE.

    Example: 'http://purl.obolibrary.org/obo/NCBITaxon_1286640' -> 'NCBITaxon:1286640'
    """
    if not strain_url:
        return None

    # Handle OBO PURLs
    if "/NCBITaxon_" in strain_url:
        taxon_id = strain_url.split("_")[-1]
        return f"NCBITaxon:{taxon_id}"

    # Handle BacDive links
    if "bacdive.dsmz.de/strain/" in strain_url:
        bacdive_id = strain_url.rstrip("/").split("/")[-1]
        return f"bacdive:{bacdive_id}"

    return None


def transform_preference_row(row: dict[str, str], media_map: dict[str, str]) -> KGXEdge | None:
    """
    Transform a row from growth_preferences.tsv into a KGX edge.

    Parameters
    ----------
    row : dict[str, str]
        Row from growth_preferences.tsv
    media_map : dict[str, str]
        Mapping from placeholder ID (e.g. '0000001') to grounded ID (e.g. 'BER-CMM-MEDIUM:0000001')

    Returns
    -------
    KGXEdge | None
        The created edge or None if mapping fails
    """
    # 1. Subject (Strain)
    subject_id = extract_strain_curie(row.get("strain_url", ""))
    if not subject_id:
        # Try fallback to strain id if available
        sid = row.get("strain id", "").strip()
        if sid:
            subject_id = sid
        else:
            logger.warning(f"Could not identify strain for row: {row.get('scientific name with strain id')}")
            return None

    # 2. Object (Medium)
    placeholder = extract_placeholder_id(row.get("object", ""))
    if not placeholder:
        logger.warning(f"Could not extract placeholder ID from object: {row.get('object')}")
        return None

    object_id = media_map.get(placeholder)
    if not object_id:
        logger.warning(f"No grounded media found for placeholder: {placeholder}")
        return None

    # 3. Predicate (Growth result)
    binary_result = row.get("Growth result binary", "").strip()
    predicate = GROWS_IN
    if binary_result == "0":
        predicate = DOES_NOT_GROW_IN

    # 4. Create Edge
    edge = KGXEdge(
        subject=subject_id,
        predicate=predicate,
        object=object_id,
        knowledge_level="knowledge_assertion",
        agent_type="manual_agent",
        primary_knowledge_source=["infores:cmm-ai-automation"],
    )

    # Add quantitative metadata if present
    quant = row.get("Growth result quantiative", "").strip()
    if quant:
        edge.model_extra["growth_value"] = quant

    return edge
