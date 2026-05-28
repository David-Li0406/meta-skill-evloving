"""
KGX transformation for bacterial strain data.

This module provides data models and transformation functions to convert
bacterial strain data into Biolink Model-compliant KGX format.

Design follows:
- Biolink Model specification
- KGX format specification (https://github.com/biolink/kgx)
- kg-microbe implementation patterns
"""

from typing import Literal

from pydantic import BaseModel, Field

# Type aliases for clarity
CURIE = str
BiolinkCategory = str
BiolinkPredicate = str
KnowledgeLevel = Literal[
    "knowledge_assertion",
    "logical_entailment",
    "prediction",
    "statistical_association",
    "observation",
    "not_provided",
]
AgentType = Literal[
    "manual_agent",
    "automated_agent",
    "data_analysis_pipeline",
    "computational_model",
    "text_mining_agent",
    "image_processing_agent",
    "manual_validation_of_automated_agent",
    "not_provided",
]


class KGXNode(BaseModel):
    """
    A node in a KGX knowledge graph.

    Represents a Biolink Model NamedThing. Follows KGX specification with
    only `id` and `category` as required fields.

    Examples
    --------
    >>> node = KGXNode(
    ...     id="bacdive:7142",
    ...     category=["biolink:OrganismTaxon"],
    ...     name="Methylorubrum extorquens DSM 1337"
    ... )
    >>> node.id
    'bacdive:7142'
    >>> node.category
    ['biolink:OrganismTaxon']

    >>> # Taxonomy node
    >>> taxon = KGXNode(
    ...     id="NCBITaxon:408",
    ...     category=["biolink:OrganismTaxon"],
    ...     name="Methylorubrum extorquens",
    ...     provided_by=["infores:ncbi"]
    ... )
    >>> taxon.provided_by
    ['infores:ncbi']
    """

    # Required fields
    id: CURIE = Field(..., description="CURIE uniquely identifying this node")
    category: list[BiolinkCategory] = Field(
        ...,
        min_length=1,
        description="Biolink categories from NamedThing hierarchy",
    )

    # Common optional fields
    name: str | None = Field(None, description="Human-readable name")
    description: str | None = Field(None, description="Human-readable description")
    provided_by: list[str] | None = Field(None, description="Information resources that provided this node")
    xref: list[CURIE] | None = Field(None, description="Cross-references as CURIEs")
    synonym: list[str] | None = Field(None, description="Alternative names")
    iri: str | None = Field(None, description="IRI form of identifier")
    in_taxon: list[CURIE] | None = Field(None, description="Taxonomic classification CURIEs")
    in_taxon_label: str | None = Field(None, description="Human-readable taxon name")

    # Allow additional fields (KGX lenient design)
    model_config = {"extra": "allow"}


class KGXEdge(BaseModel):
    """
    An edge in a KGX knowledge graph.

    Represents a Biolink Model Association. Follows KGX specification with
    required fields: subject, predicate, object, knowledge_level, agent_type.

    Examples
    --------
    >>> edge = KGXEdge(
    ...     subject="bacdive:7142",
    ...     predicate="biolink:in_taxon",
    ...     object="NCBITaxon:408",
    ...     knowledge_level="knowledge_assertion",
    ...     agent_type="manual_agent"
    ... )
    >>> edge.subject
    'bacdive:7142'
    >>> edge.predicate
    'biolink:in_taxon'

    >>> # With full provenance
    >>> edge = KGXEdge(
    ...     id="edge_1",
    ...     subject="bacdive:7142",
    ...     predicate="biolink:in_taxon",
    ...     object="NCBITaxon:408",
    ...     knowledge_level="knowledge_assertion",
    ...     agent_type="manual_agent",
    ...     primary_knowledge_source=["infores:bacdive"]
    ... )
    >>> edge.primary_knowledge_source
    ['infores:bacdive']
    """

    # Required fields
    subject: CURIE = Field(..., description="ID of source node")
    predicate: BiolinkPredicate = Field(..., description="Biolink predicate from related_to hierarchy")
    object: CURIE = Field(..., description="ID of target node")
    knowledge_level: KnowledgeLevel = Field(..., description="Level of knowledge representation")
    agent_type: AgentType = Field(..., description="Type of autonomous agent that generated this edge")

    # Optional but recommended
    id: str | None = Field(None, description="Unique edge identifier")
    category: list[BiolinkCategory] | None = Field(None, description="Biolink association categories")
    primary_knowledge_source: list[str] | None = Field(None, description="Most upstream knowledge source")
    aggregator_knowledge_source: list[str] | None = Field(None, description="Intermediate knowledge sources")
    publications: list[CURIE] | None = Field(None, description="Supporting publications")

    # Allow additional fields (KGX lenient design)
    model_config = {"extra": "allow"}


def normalize_curie(prefix: str, local_id: str) -> CURIE:
    """
    Normalize a prefix and local ID into standard CURIE format.

    Parameters
    ----------
    prefix : str
        The CURIE prefix (e.g., "bacdive", "NCBITaxon")
    local_id : str
        The local identifier

    Returns
    -------
    str
        Normalized CURIE in format "prefix:local_id"

    Examples
    --------
    >>> normalize_curie("bacdive", "7142")
    'bacdive:7142'
    >>> normalize_curie("NCBITaxon", "408")
    'NCBITaxon:408'
    >>> normalize_curie("DSM", "1337")
    'DSM:1337'
    """
    return f"{prefix}:{local_id}"


def split_list_field(value: str | None, delimiter: str = ";") -> list[str]:
    """
    Split a delimited string field into a list, cleaning whitespace.

    Parameters
    ----------
    value : str | None
        The delimited string to split
    delimiter : str, optional
        The delimiter character, by default ";"

    Returns
    -------
    list[str]
        List of cleaned values, empty list if input is None or empty

    Examples
    --------
    >>> split_list_field("DSM:1337; ATCC:43645; JCM:2802")
    ['DSM:1337', 'ATCC:43645', 'JCM:2802']
    >>> split_list_field("value1;value2;value3")
    ['value1', 'value2', 'value3']
    >>> split_list_field(None)
    []
    >>> split_list_field("")
    []
    >>> split_list_field("  single  ")
    ['single']
    """
    if not value or not value.strip():
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]


def transform_strain_row(row: dict[str, str]) -> tuple[list[KGXNode], list[KGXEdge]]:
    """
    Transform a single strain data row into KGX nodes and edges.

    Creates:
    1. A strain node (biolink:OrganismTaxon)
    2. A species taxonomy node (biolink:OrganismTaxon) if species taxon ID present
    3. An edge connecting strain to species (biolink:in_taxon)

    Parameters
    ----------
    row : dict[str, str]
        A dictionary representing a strain record with keys from strains_enriched.tsv

    Returns
    -------
    tuple[list[KGXNode], list[KGXEdge]]
        A tuple of (nodes, edges) created from this row

    Examples
    --------
    >>> row = {
    ...     "bacdive_id_mam": "7142",
    ...     "strain_id_sub_or_mpj": "DSM:1337",
    ...     "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
    ...     "ncbi_species_taxon_fresh_lookup": "408",
    ...     "type_strain_fresh_lookup": "yes",
    ...     "biosafety_level_fresh_lookup": "1",
    ... }
    >>> nodes, edges = transform_strain_row(row)
    >>> len(nodes)
    2
    >>> nodes[0].id
    'bacdive:7142'
    >>> nodes[0].category
    ['biolink:OrganismTaxon']
    >>> nodes[1].id
    'NCBITaxon:408'
    >>> len(edges)
    1
    >>> edges[0].predicate
    'biolink:in_taxon'

    >>> # Row without species taxon - only creates strain node
    >>> row_no_taxon = {
    ...     "bacdive_id_mam": "7143",
    ...     "strain_id_sub_or_mpj": "DSM:1338",
    ...     "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
    ... }
    >>> nodes, edges = transform_strain_row(row_no_taxon)
    >>> len(nodes)
    1
    >>> len(edges)
    0
    """
    nodes: list[KGXNode] = []
    edges: list[KGXEdge] = []

    # Extract BacDive ID (required)
    bacdive_id = row.get("bacdive_id_mam", "").strip()
    if not bacdive_id:
        # Skip rows without BacDive ID
        return nodes, edges

    # Create strain CURIE
    strain_curie = normalize_curie("bacdive", bacdive_id)

    # Get strain name (prefer scientific_name, fallback to strain_id)
    scientific_name = row.get("scientific_name_sub_or_mpj", "").strip()
    strain_id = row.get("strain_id_sub_or_mpj", "").strip()

    if scientific_name and strain_id:
        strain_name = f"{scientific_name} {strain_id}"
    elif scientific_name:
        strain_name = scientific_name
    elif strain_id:
        strain_name = strain_id
    else:
        strain_name = strain_curie  # Fallback to CURIE

    # Get species taxonomy (prefer fresh_lookup over sub_or_mpj)
    species_taxon = (
        row.get("ncbi_species_taxon_fresh_lookup", "").strip() or row.get("species_taxon_id_sub_or_mpj", "").strip()
    )

    # Parse culture collection IDs for xref
    culture_collections_str = row.get("culture_collection_ids_sub_or_mpj", "").strip()
    xrefs = split_list_field(culture_collections_str) if culture_collections_str else None

    # Parse alternative names for synonyms
    alt_names_str = row.get("alternative_names_sub_or_mpj", "").strip()
    synonyms = split_list_field(alt_names_str) if alt_names_str else None

    # Create strain node
    strain_node_data: dict = {
        "id": strain_curie,
        "category": ["biolink:OrganismTaxon"],
        "name": strain_name,
        "provided_by": ["infores:bacdive"],
    }

    # Add species taxonomy as property if available
    if species_taxon:
        taxon_curie = normalize_curie("NCBITaxon", species_taxon)
        strain_node_data["in_taxon"] = [taxon_curie]
        if scientific_name:
            strain_node_data["in_taxon_label"] = scientific_name

    # Add optional fields if present
    if xrefs:
        strain_node_data["xref"] = xrefs
    if synonyms:
        strain_node_data["synonym"] = synonyms

    # Add custom properties (KGX allows non-Biolink properties)
    type_strain = row.get("type_strain_fresh_lookup", "").strip() or row.get("type_strain_sub_or_mpj", "").strip()
    if type_strain:
        strain_node_data["type_strain"] = type_strain

    biosafety = row.get("biosafety_level_fresh_lookup", "").strip() or row.get("biosafety_level_sub_or_mpj", "").strip()
    if biosafety:
        strain_node_data["biosafety_level"] = biosafety

    availability = row.get("availability_status_sub_or_mpj", "").strip()
    if availability:
        strain_node_data["availability_status"] = availability

    strain_node = KGXNode(**strain_node_data)
    nodes.append(strain_node)

    # Create species taxonomy node and edge if species taxon exists
    if species_taxon:
        taxon_curie = normalize_curie("NCBITaxon", species_taxon)

        taxon_node = KGXNode(
            id=taxon_curie,
            category=["biolink:OrganismTaxon"],
            name=scientific_name or f"NCBITaxon:{species_taxon}",
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
