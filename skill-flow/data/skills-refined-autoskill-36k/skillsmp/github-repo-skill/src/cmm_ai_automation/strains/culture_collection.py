"""Culture collection ID search and reconciliation.

This module provides functions to search for bacterial strains in BacDive MongoDB
by culture collection identifiers (DSM, ATCC, NCIMB, etc.).

The BacDive collection has a quirk: the field "External links" → "culture collection no."
has a trailing period in the field name, which breaks standard MongoDB dot notation queries.
This module handles that using MongoDB aggregation pipelines.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pymongo.collection import Collection

logger = logging.getLogger(__name__)


def parse_culture_collection_id(cc_id: str) -> tuple[str, str] | None:
    """Parse a culture collection ID into prefix and number.

    Handles various formats:
        - "DSM:1337" → ("DSM", "1337")
        - "DSM-1337" → ("DSM", "1337")
        - "DSM 1337" → ("DSM", "1337")
        - "ATCC:43883" → ("ATCC", "43883")
        - "NBRC 15843" → ("NBRC", "15843")

    Args:
        cc_id: Culture collection ID in various formats

    Returns:
        Tuple of (prefix, number) or None if not parseable

    Examples:
        >>> parse_culture_collection_id("DSM:1337")
        ('DSM', '1337')
        >>> parse_culture_collection_id("ATCC-43883")
        ('ATCC', '43883')
        >>> parse_culture_collection_id("NBRC 15843")
        ('NBRC', '15843')
    """
    match = re.match(r"([A-Za-z]+)[:\s-]*(\d+)", cc_id.strip())
    if match:
        prefix = match.group(1).upper()
        number = match.group(2)
        return (prefix, number)
    return None


def format_for_bacdive_search(prefix: str, number: str) -> str:
    """Format culture collection ID for BacDive search.

    BacDive stores culture collection IDs with space separator:
    "DSM 1337", "ATCC 43883", etc.

    Args:
        prefix: Collection prefix (e.g., "DSM", "ATCC")
        number: Collection number (e.g., "1337", "43883")

    Returns:
        Formatted string for BacDive search

    Examples:
        >>> format_for_bacdive_search("DSM", "1337")
        'DSM 1337'
        >>> format_for_bacdive_search("ATCC", "43883")
        'ATCC 43883'
    """
    return f"{prefix.upper()} {number}"


def search_by_dsm_number(collection: Collection[dict[str, Any]], dsm_number: int) -> dict[str, Any] | None:
    """Search for strain by DSM number using the integer field.

    This is the fastest and most reliable method for DSM strains.
    Uses the indexed "General.DSM-Number" integer field.

    Args:
        collection: BacDive MongoDB collection
        dsm_number: DSM number as integer (e.g., 1337)

    Returns:
        BacDive document or None if not found

    Examples:
        >>> from pymongo import MongoClient
        >>> client = MongoClient("mongodb://localhost:27017")
        >>> collection = client["bacdive"]["strains"]
        >>> doc = search_by_dsm_number(collection, 1337)
        >>> doc['General']['DSM-Number']
        1337
    """
    return cast("dict[str, Any] | None", collection.find_one({"General.DSM-Number": dsm_number}))


def search_by_culture_collection_aggregation(
    collection: Collection[dict[str, Any]],
    search_string: str,
    use_word_boundaries: bool = True,
) -> dict[str, Any] | None:
    """Search for strain by culture collection ID using aggregation pipeline.

    Uses aggregation to access the "culture collection no." field which has
    a trailing period in its name (breaks standard dot notation).

    Args:
        collection: BacDive MongoDB collection
        search_string: Formatted search string (e.g., "DSM 1337", "ATCC 43883")
        use_word_boundaries: If True, use word-boundary regex to prevent
            substring matches (recommended)

    Returns:
        BacDive document or None if not found

    Examples:
        >>> doc = search_by_culture_collection_aggregation(collection, "ATCC 43883")
        >>> doc is not None
        True
    """
    # Build regex pattern
    if use_word_boundaries:
        # Match only at start of string or after ", "
        # and followed by ", " or end of string
        # Prevents "DSM 1337" from matching "DSM 13378"
        escaped = re.escape(search_string)
        pattern = rf"(^|,\s*){escaped}(\s*,|$)"
    else:
        # Simple substring match (not recommended - can cause false positives)
        pattern = re.escape(search_string)

    pipeline = [
        # First, filter to documents with External links
        {"$match": {"External links": {"$exists": True}}},
        # Extract the "culture collection no." field using $getField
        # (necessary because field name contains a period)
        {
            "$addFields": {
                "cc_field": {
                    "$getField": {
                        "field": "culture collection no.",
                        "input": "$External links",
                    }
                }
            }
        },
        # Match using regex with word boundaries
        {
            "$match": {
                "$expr": {
                    "$regexMatch": {
                        "input": {"$ifNull": ["$cc_field", ""]},
                        "regex": pattern,
                    }
                }
            }
        },
        # Limit to first result
        {"$limit": 1},
    ]

    results = list(collection.aggregate(pipeline))
    return results[0] if results else None


def search_culture_collection(
    collection: Collection[dict[str, Any]],
    cc_id: str,
) -> dict[str, Any] | None:
    """Search for a strain by culture collection ID.

    This is the main entry point for culture collection searches.
    Uses optimized search strategies:
    - DSM IDs: Use integer field (fast, indexed)
    - Other IDs: Use aggregation with word-boundary regex

    Args:
        collection: BacDive MongoDB collection
        cc_id: Culture collection ID in any format
            (e.g., "DSM:1337", "ATCC-43883", "NBRC 15843")

    Returns:
        BacDive document or None if not found

    Examples:
        >>> doc = search_culture_collection(collection, "DSM:1337")
        >>> doc['General']['BacDive-ID']
        7142
        >>> doc['General']['DSM-Number']
        1337

        >>> doc = search_culture_collection(collection, "ATCC:43883")
        >>> doc is not None
        True

        >>> doc = search_culture_collection(collection, "INVALID:999999")
        >>> doc is None
        True
    """
    # Parse the culture collection ID
    parsed = parse_culture_collection_id(cc_id)
    if not parsed:
        logger.warning(f"Could not parse culture collection ID: {cc_id}")
        return None

    prefix, number = parsed

    # Strategy 1: Fast path for DSM IDs (use integer field)
    if prefix == "DSM" or prefix == "DSMZ":
        try:
            dsm_int = int(number)
            doc = search_by_dsm_number(collection, dsm_int)
            if doc:
                logger.debug(f"Found {cc_id} via General.DSM-Number field")
                return doc
        except ValueError:
            # DSM number is not a valid integer - will try other search methods
            logger.warning(f"Invalid DSM number: {number}")

    # Strategy 2: Search in culture collection string (with word boundaries)
    search_string = format_for_bacdive_search(prefix, number)
    doc = search_by_culture_collection_aggregation(collection, search_string, use_word_boundaries=True)

    if doc:
        logger.debug(f"Found {cc_id} via culture collection field")
        return doc

    logger.debug(f"Culture collection ID not found: {cc_id}")
    return None


def batch_search_culture_collections(
    collection: Collection[dict[str, Any]],
    cc_ids: list[str],
) -> dict[str, dict[str, Any] | None]:
    """Search for multiple culture collection IDs.

    Args:
        collection: BacDive MongoDB collection
        cc_ids: List of culture collection IDs

    Returns:
        Dict mapping input ID to BacDive document (or None if not found)

    Examples:
        >>> cc_ids = ["DSM:1337", "ATCC:43883", "INVALID:999999"]
        >>> results = batch_search_culture_collections(collection, cc_ids)
        >>> len(results)
        3
        >>> results["DSM:1337"] is not None
        True
        >>> results["INVALID:999999"] is None
        True
    """
    results = {}
    for cc_id in cc_ids:
        results[cc_id] = search_culture_collection(collection, cc_id)
    return results


def extract_culture_collection_ids(doc: dict[str, Any]) -> list[str]:
    """Extract all culture collection IDs from a BacDive document.

    Parses the comma-separated "culture collection no." field.

    Args:
        doc: BacDive MongoDB document

    Returns:
        List of culture collection IDs (in BacDive format with spaces)

    Examples:
        >>> doc = search_culture_collection(collection, "DSM:1337")
        >>> cc_ids = extract_culture_collection_ids(doc)
        >>> "DSM 1337" in cc_ids
        True
        >>> "ATCC 43645" in cc_ids
        True
    """
    external_links = doc.get("External links", {})
    cc_string = external_links.get("culture collection no.", "")

    if not cc_string:
        return []

    # Split on comma and strip whitespace
    return [cc_id.strip() for cc_id in cc_string.split(",") if cc_id.strip()]


def reconcile_culture_collection_id(
    collection: Collection[dict[str, Any]],
    cc_id: str,
) -> dict[str, Any]:
    """Reconcile a culture collection ID and return detailed results.

    Provides comprehensive information about the search, including:
    - Whether the strain was found
    - Which search method succeeded
    - All culture collection cross-references

    Args:
        collection: BacDive MongoDB collection
        cc_id: Culture collection ID to reconcile

    Returns:
        Dict with keys:
            - input_id: Original input ID
            - found: Boolean
            - document: BacDive document (or None)
            - search_method: How it was found ("dsm_number", "culture_collection", None)
            - all_culture_collections: List of all CC IDs for this strain
            - bacdive_id: BacDive ID (or None)
            - dsm_number: DSM number (or None)
            - species: Species name (or None)

    Examples:
        >>> result = reconcile_culture_collection_id(collection, "DSM:1337")
        >>> result['found']
        True
        >>> result['search_method']
        'dsm_number'
        >>> result['bacdive_id']
        7142
        >>> "ATCC 43645" in result['all_culture_collections']
        True
    """
    result = {
        "input_id": cc_id,
        "found": False,
        "document": None,
        "search_method": None,
        "all_culture_collections": [],
        "bacdive_id": None,
        "dsm_number": None,
        "species": None,
        "strain_designation": None,
        "ncbi_taxon_id": None,
    }

    # Parse the ID
    parsed = parse_culture_collection_id(cc_id)
    if not parsed:
        logger.warning(f"Could not parse culture collection ID: {cc_id}")
        return result

    prefix, number = parsed

    # Try DSM number first
    if prefix == "DSM" or prefix == "DSMZ":
        try:
            dsm_int = int(number)
            doc = search_by_dsm_number(collection, dsm_int)
            if doc:
                result["found"] = True
                result["document"] = doc
                result["search_method"] = "dsm_number"
        except ValueError:
            pass

    # Try culture collection search if not found
    if not result["found"]:
        search_string = format_for_bacdive_search(prefix, number)
        doc = search_by_culture_collection_aggregation(collection, search_string, use_word_boundaries=True)
        if doc:
            result["found"] = True
            result["document"] = doc
            result["search_method"] = "culture_collection"

    # Extract metadata if found
    if result["found"] and result["document"]:
        doc = cast("dict[str, Any]", result["document"])

        # BacDive ID
        result["bacdive_id"] = doc.get("General", {}).get("BacDive-ID")

        # DSM Number
        result["dsm_number"] = doc.get("General", {}).get("DSM-Number")

        # Species and designation
        taxonomy = doc.get("Name and taxonomic classification", {})
        result["species"] = taxonomy.get("species")
        result["strain_designation"] = taxonomy.get("strain designation")

        # NCBI taxon ID
        ncbi_tax = doc.get("General", {}).get("NCBI tax id", {})
        if isinstance(ncbi_tax, dict):
            result["ncbi_taxon_id"] = ncbi_tax.get("NCBI tax id")

        # All culture collection IDs
        result["all_culture_collections"] = extract_culture_collection_ids(doc)

    return result
