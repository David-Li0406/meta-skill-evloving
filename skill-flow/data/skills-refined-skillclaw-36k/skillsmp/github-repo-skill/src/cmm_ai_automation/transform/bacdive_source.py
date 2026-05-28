"""
BacDive MongoDB source for KGX transformation.

This module provides functions to read bacterial strain data from BacDive MongoDB
and transform it into KGX format.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, cast

from cmm_ai_automation.transform.kgx import KGXEdge, KGXNode, normalize_curie

if TYPE_CHECKING:
    from pymongo.collection import Collection

logger = logging.getLogger(__name__)


def safe_get_list(obj: dict[str, Any] | Any, *keys: str) -> list[Any]:
    """
    Safely get a value that could be dict, list, or scalar.

    Handles BacDive's heterogeneous JSON structure where the same path
    can return different types (dict, list of dicts, or scalar).

    Always returns a list for uniform iteration.

    Parameters
    ----------
    obj : dict or any
        The object to traverse
    *keys : str
        Path components to traverse (e.g., "General", "NCBI tax id")

    Returns
    -------
    list
        List of values found at the path, empty list if not found

    Examples
    --------
    >>> doc = {"General": {"NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"}}}
    >>> safe_get_list(doc, "General", "NCBI tax id")
    [{'NCBI tax id': 408, 'Matching level': 'species'}]

    >>> doc = {"General": {"NCBI tax id": [{"NCBI tax id": 408}, {"NCBI tax id": 426355}]}}
    >>> result = safe_get_list(doc, "General", "NCBI tax id")
    >>> len(result)
    2

    >>> doc = {"General": {"NCBI tax id": 408}}
    >>> safe_get_list(doc, "General", "NCBI tax id")
    [408]

    >>> safe_get_list({}, "Missing", "Path")
    []
    """
    value: Any = obj

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return []

        if value is None:
            return []

    # Normalize to list
    if isinstance(value, list):
        return value
    else:
        return [value]


def extract_ncbi_taxon_ids(doc: dict[str, Any]) -> tuple[set[str], set[str]]:
    """
    Extract NCBI taxonomy IDs from a BacDive document.

    BacDive records may contain both species-level and strain-level NCBI
    taxon IDs. This function extracts both, distinguishing them by the
    "Matching level" field when present.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    tuple[set[str], set[str]]
        Tuple of (species_ids, strain_ids)

    Examples
    --------
    >>> doc = {
    ...     "General": {
    ...         "NCBI tax id": {
    ...             "NCBI tax id": 408,
    ...             "Matching level": "species"
    ...         }
    ...     }
    ... }
    >>> species, strain = extract_ncbi_taxon_ids(doc)
    >>> species
    {'408'}
    >>> strain
    set()

    >>> # Multiple IDs with different levels
    >>> doc = {
    ...     "General": {
    ...         "NCBI tax id": [
    ...             {"NCBI tax id": 31998, "Matching level": "species"},
    ...             {"NCBI tax id": 426355, "Matching level": "strain"}
    ...         ]
    ...     }
    ... }
    >>> species, strain = extract_ncbi_taxon_ids(doc)
    >>> '31998' in species
    True
    >>> '426355' in strain
    True
    """
    species_ids: set[str] = set()
    strain_ids: set[str] = set()

    # Use safe_get_list to handle heterogeneous structure
    ncbi_tax_entries = safe_get_list(doc, "General", "NCBI tax id")

    for entry in ncbi_tax_entries:
        if isinstance(entry, dict):
            tax_id = entry.get("NCBI tax id")
            level = entry.get("Matching level", "").lower()

            if tax_id:
                tax_id_str = str(tax_id)
                if "species" in level:
                    species_ids.add(tax_id_str)
                elif "strain" in level:
                    strain_ids.add(tax_id_str)
                else:
                    # Default to species if no level specified
                    species_ids.add(tax_id_str)
        elif isinstance(entry, int | str):
            # Scalar case - assume species level
            species_ids.add(str(entry))

    return species_ids, strain_ids


def extract_scientific_name(doc: dict[str, Any]) -> str | None:
    """
    Extract scientific name from BacDive document.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    str or None
        Binomial species name or None if not found

    Examples
    --------
    >>> doc = {
    ...     "Name and taxonomic classification": {
    ...         "species": "Methylorubrum extorquens"
    ...     }
    ... }
    >>> extract_scientific_name(doc)
    'Methylorubrum extorquens'

    >>> extract_scientific_name({})
    """
    taxonomy = doc.get("Name and taxonomic classification", {})
    return cast("str | None", taxonomy.get("species"))


def extract_type_strain(doc: dict[str, Any]) -> str | None:
    """
    Extract type strain status from BacDive document.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    str or None
        "yes", "no", or None if not present

    Examples
    --------
    >>> doc = {"Name and taxonomic classification": {"type strain": "yes"}}
    >>> extract_type_strain(doc)
    'yes'

    >>> doc = {"Name and taxonomic classification": {"type strain": True}}
    >>> extract_type_strain(doc)
    'yes'

    >>> extract_type_strain({})
    """
    taxonomy = doc.get("Name and taxonomic classification", {})
    type_strain = taxonomy.get("type strain")

    if type_strain is None:
        return None

    # Handle boolean or string
    if isinstance(type_strain, bool):
        return "yes" if type_strain else "no"

    return cast("str", str(type_strain).lower())


def extract_culture_collection_ids(doc: dict[str, Any]) -> set[str]:
    """
    Extract culture collection IDs from BacDive document.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    set[str]
        Set of normalized CURIEs (e.g., "DSM:1337", "ATCC:43645")

    Examples
    --------
    >>> doc = {
    ...     "External links": {
    ...         "culture collection no.": "DSM 1337, ATCC 43645, JCM 2802"
    ...     }
    ... }
    >>> ids = extract_culture_collection_ids(doc)
    >>> "DSM:1337" in ids
    True
    >>> "ATCC:43645" in ids
    True
    """
    external = doc.get("External links", {})
    cc_string = external.get("culture collection no.", "")

    if not cc_string:
        return set()

    ids = set()
    for cc_id in cc_string.split(","):
        cc_id = cc_id.strip()
        if not cc_id:
            continue

        # Normalize "DSM 1337" -> "DSM:1337"
        if " " in cc_id and ":" not in cc_id:
            parts = cc_id.split(None, 1)  # Split on first whitespace
            if len(parts) == 2:
                cc_id = f"{parts[0]}:{parts[1]}"

        ids.add(cc_id)

    return ids


def extract_alternative_names(doc: dict[str, Any]) -> set[str]:
    """
    Extract alternative/synonym names from BacDive document.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    set[str]
        Set of synonym names

    Examples
    --------
    >>> doc = {
    ...     "Name and taxonomic classification": {
    ...         "LPSN": {
    ...             "synonyms": [
    ...                 {"synonym": "Methylobacterium extorquens"},
    ...                 {"synonym": "Protomonas extorquens"}
    ...             ]
    ...         }
    ...     }
    ... }
    >>> names = extract_alternative_names(doc)
    >>> "Methylobacterium extorquens" in names
    True
    """
    taxonomy = doc.get("Name and taxonomic classification", {})
    lpsn = taxonomy.get("LPSN", {})

    if not isinstance(lpsn, dict):
        return set()

    synonyms = set()
    lpsn_synonyms = lpsn.get("synonyms", [])

    # Could be list, single dict, or string
    if isinstance(lpsn_synonyms, dict):
        lpsn_synonyms = [lpsn_synonyms]
    elif isinstance(lpsn_synonyms, str):
        # Single string synonym - add directly and return
        return {lpsn_synonyms}

    for syn_entry in lpsn_synonyms:
        if isinstance(syn_entry, dict):
            synonym = syn_entry.get("synonym")
            if synonym:
                synonyms.add(synonym)
        elif isinstance(syn_entry, str):
            synonyms.add(syn_entry)

    return synonyms


def extract_strain_designations(doc: dict[str, Any]) -> list[str]:
    """
    Extract strain designations from BacDive document.

    Strain designations can be comma-separated (e.g., "PG 8, PG8").
    Returns a list of individual designations.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    list[str]
        List of strain designations

    Examples
    --------
    >>> doc = {
    ...     "Name and taxonomic classification": {
    ...         "strain designation": "TK 0001"
    ...     }
    ... }
    >>> extract_strain_designations(doc)
    ['TK 0001']

    >>> # Comma-separated designations
    >>> doc = {
    ...     "Name and taxonomic classification": {
    ...         "strain designation": "PG 8, PG8"
    ...     }
    ... }
    >>> extract_strain_designations(doc)
    ['PG 8', 'PG8']

    >>> extract_strain_designations({})
    []
    """
    taxonomy = doc.get("Name and taxonomic classification", {})
    designation = taxonomy.get("strain designation")

    if not designation:
        return []

    # Split on comma and clean whitespace
    designations = [d.strip() for d in designation.split(",") if d.strip()]
    return designations


def extract_genome_accessions(doc: dict[str, Any]) -> list[str]:
    """
    Extract genome sequence accessions from BacDive document.

    Handles BacDive's heterogeneous structure where "Genome sequences"
    can be a dict, list of dicts, or missing.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    list[str]
        List of genome accessions (e.g., GCA IDs, PATRIC IDs)

    Examples
    --------
    >>> doc = {
    ...     "Sequence information": {
    ...         "Genome sequences": {
    ...             "accession": "408.23",
    ...             "database": "patric"
    ...         }
    ...     }
    ... }
    >>> extract_genome_accessions(doc)
    ['408.23']

    >>> # Multiple genomes
    >>> doc = {
    ...     "Sequence information": {
    ...         "Genome sequences": [
    ...             {"accession": "GCA_000022685.1"},
    ...             {"accession": "GCA_000983655.1"}
    ...         ]
    ...     }
    ... }
    >>> extract_genome_accessions(doc)
    ['GCA_000022685.1', 'GCA_000983655.1']

    >>> # Scalar accession (edge case)
    >>> doc = {
    ...     "Sequence information": {
    ...         "Genome sequences": "GCA_000022685.1"
    ...     }
    ... }
    >>> extract_genome_accessions(doc)
    ['GCA_000022685.1']

    >>> extract_genome_accessions({})
    []
    """
    # Use safe_get_list to handle heterogeneous structure
    genome_seqs = safe_get_list(doc, "Sequence information", "Genome sequences")

    accessions = []
    for genome in genome_seqs:
        if isinstance(genome, dict):
            accession = genome.get("accession")
            if accession:
                accessions.append(str(accession))
        elif isinstance(genome, str):
            # Handle scalar string accession (edge case)
            accessions.append(genome)

    return accessions


def extract_biosafety_level(doc: dict[str, Any]) -> str | None:
    """
    Extract biosafety level from BacDive document.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    str or None
        Biosafety level (e.g., "1", "2") or None

    Examples
    --------
    >>> doc = {
    ...     "Safety information": {
    ...         "risk assessment": {
    ...             "biosafety level": "1"
    ...         }
    ...     }
    ... }
    >>> extract_biosafety_level(doc)
    '1'

    >>> # Multiple risk assessments - take first
    >>> doc = {
    ...     "Safety information": {
    ...         "risk assessment": [
    ...             {"biosafety level": "1"},
    ...             {"biosafety level": "2"}
    ...         ]
    ...     }
    ... }
    >>> extract_biosafety_level(doc)
    '1'
    """
    safety = doc.get("Safety information", {})
    risk_assessment = safety.get("risk assessment")

    if not risk_assessment:
        return None

    # Normalize to list
    if isinstance(risk_assessment, dict):
        risk_assessment = [risk_assessment]

    # Take first level found
    for item in risk_assessment:
        if isinstance(item, dict):
            level = item.get("biosafety level")
            if level:
                return str(level).strip()

    return None


def transform_bacdive_doc(doc: dict[str, Any]) -> tuple[list[KGXNode], list[KGXEdge]]:
    """
    Transform a BacDive MongoDB document into KGX nodes and edges.

    Parameters
    ----------
    doc : dict
        BacDive MongoDB document

    Returns
    -------
    tuple[list[KGXNode], list[KGXEdge]]
        Tuple of (nodes, edges) created from this document

    Examples
    --------
    >>> doc = {
    ...     "General": {
    ...         "BacDive-ID": 7142,
    ...         "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"}
    ...     },
    ...     "Name and taxonomic classification": {
    ...         "species": "Methylorubrum extorquens",
    ...         "type strain": "yes"
    ...     },
    ...     "External links": {
    ...         "culture collection no.": "DSM 1337, ATCC 43645"
    ...     }
    ... }
    >>> nodes, edges = transform_bacdive_doc(doc)
    >>> len(nodes)
    2
    >>> nodes[0].id
    'bacdive:7142'
    >>> len(edges)
    1
    """
    nodes: list[KGXNode] = []
    edges: list[KGXEdge] = []

    # Extract BacDive ID (required)
    bacdive_id = doc.get("General", {}).get("BacDive-ID")
    if not bacdive_id:
        # Skip documents without BacDive ID
        return nodes, edges

    # Create strain CURIE
    strain_curie = normalize_curie("bacdive", str(bacdive_id))

    # Extract data from BacDive doc
    scientific_name = extract_scientific_name(doc)
    species_taxon_ids, strain_taxon_ids = extract_ncbi_taxon_ids(doc)
    type_strain = extract_type_strain(doc)
    culture_collections = extract_culture_collection_ids(doc)
    alternative_names = extract_alternative_names(doc)
    biosafety_level = extract_biosafety_level(doc)
    strain_designations = extract_strain_designations(doc)
    genome_accessions = extract_genome_accessions(doc)

    # Build strain node
    strain_node_data: dict[str, Any] = {
        "id": strain_curie,
        "category": ["biolink:OrganismTaxon"],
        "name": scientific_name or strain_curie,
        "provided_by": ["infores:bacdive"],
    }

    # Add species taxonomy as property if available
    if species_taxon_ids:
        # Use first species ID if multiple
        species_id = next(iter(species_taxon_ids))
        taxon_curie = normalize_curie("NCBITaxon", species_id)
        strain_node_data["in_taxon"] = [taxon_curie]
        if scientific_name:
            strain_node_data["in_taxon_label"] = scientific_name

    # Add culture collections as xrefs
    if culture_collections:
        strain_node_data["xref"] = sorted(culture_collections)

    # Add alternative names as synonyms
    if alternative_names:
        strain_node_data["synonym"] = sorted(alternative_names)

    # Add custom properties
    if type_strain:
        strain_node_data["type_strain"] = type_strain

    if biosafety_level:
        strain_node_data["biosafety_level"] = biosafety_level

    if strain_designations:
        strain_node_data["strain_designation"] = strain_designations

    if genome_accessions:
        strain_node_data["has_genome"] = genome_accessions

    strain_node = KGXNode(**strain_node_data)
    nodes.append(strain_node)

    # Create species taxonomy node and edge if species taxon exists
    if species_taxon_ids:
        species_id = next(iter(species_taxon_ids))
        taxon_curie = normalize_curie("NCBITaxon", species_id)

        taxon_node = KGXNode(
            id=taxon_curie,
            category=["biolink:OrganismTaxon"],
            name=scientific_name or f"NCBITaxon:{species_id}",
            provided_by=["infores:ncbi"],
        )
        nodes.append(taxon_node)

        # Create strain -> species edge
        edge = KGXEdge(
            subject=strain_curie,
            predicate="biolink:in_taxon",
            object=taxon_curie,
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
            primary_knowledge_source=["infores:bacdive"],
        )
        edges.append(edge)

    return nodes, edges


def query_bacdive_by_ids(
    collection: Collection[dict[str, Any]], bacdive_ids: list[int]
) -> list[tuple[list[KGXNode], list[KGXEdge]]]:
    """
    Query BacDive MongoDB for multiple BacDive IDs and transform to KGX.

    Parameters
    ----------
    collection : Collection
        BacDive MongoDB collection
    bacdive_ids : list[int]
        List of BacDive IDs to query

    Returns
    -------
    list[tuple[list[KGXNode], list[KGXEdge]]]
        List of (nodes, edges) tuples, one per document found

    Examples
    --------
    >>> from cmm_ai_automation.strains import get_bacdive_collection
    >>> collection = get_bacdive_collection()  # doctest: +SKIP
    >>> if collection:  # doctest: +SKIP
    ...     results = query_bacdive_by_ids(collection, [7142, 7143])
    ...     print(f"Found {len(results)} strains")
    """
    results: list[tuple[list[KGXNode], list[KGXEdge]]] = []

    # Query all documents with BacDive IDs in the list
    query = {"General.BacDive-ID": {"$in": bacdive_ids}}
    docs = collection.find(query)

    for doc in docs:
        nodes, edges = transform_bacdive_doc(doc)
        if nodes:  # Only include if we got nodes
            results.append((nodes, edges))

    logger.info(f"Queried {len(bacdive_ids)} BacDive IDs, found {len(results)} documents")

    return results


def query_all_strains(
    collection: Collection[dict[str, Any]], limit: int | None = None
) -> list[tuple[list[KGXNode], list[KGXEdge]]]:
    """
    Query all strain documents from BacDive and transform to KGX.

    Parameters
    ----------
    collection : Collection
        BacDive MongoDB collection
    limit : int, optional
        Maximum number of documents to process, None for all

    Returns
    -------
    list[tuple[list[KGXNode], list[KGXEdge]]]
        List of (nodes, edges) tuples, one per document

    Examples
    --------
    >>> from cmm_ai_automation.strains import get_bacdive_collection
    >>> collection = get_bacdive_collection()  # doctest: +SKIP
    >>> if collection:  # doctest: +SKIP
    ...     # Get first 10 strains
    ...     results = query_all_strains(collection, limit=10)
    ...     print(f"Transformed {len(results)} strains")
    """
    results: list[tuple[list[KGXNode], list[KGXEdge]]] = []

    # Query all documents
    cursor = collection.find()
    if limit:
        cursor = cursor.limit(limit)

    for doc in cursor:
        nodes, edges = transform_bacdive_doc(doc)
        if nodes:
            results.append((nodes, edges))

    logger.info(f"Transformed {len(results)} BacDive documents to KGX")

    return results


def query_random_sample(
    collection: Collection[dict[str, Any]], sample_size: int
) -> list[tuple[list[KGXNode], list[KGXEdge]]]:
    """
    Query a random sample of strain documents from BacDive and transform to KGX.

    Uses MongoDB's $sample aggregation for efficient random sampling.

    Parameters
    ----------
    collection : Collection
        BacDive MongoDB collection
    sample_size : int
        Number of random documents to sample

    Returns
    -------
    list[tuple[list[KGXNode], list[KGXEdge]]]
        List of (nodes, edges) tuples, one per document

    Examples
    --------
    >>> from cmm_ai_automation.strains import get_bacdive_collection
    >>> collection = get_bacdive_collection()  # doctest: +SKIP
    >>> if collection:  # doctest: +SKIP
    ...     # Get random sample of 50 strains
    ...     results = query_random_sample(collection, sample_size=50)
    ...     print(f"Sampled {len(results)} random strains")
    """
    results: list[tuple[list[KGXNode], list[KGXEdge]]] = []

    # Use MongoDB $sample aggregation for efficient random sampling
    pipeline = [{"$sample": {"size": sample_size}}]
    docs = collection.aggregate(pipeline)

    for doc in docs:
        nodes, edges = transform_bacdive_doc(doc)
        if nodes:
            results.append((nodes, edges))

    logger.info(f"Sampled and transformed {len(results)} random BacDive documents to KGX")

    return results
