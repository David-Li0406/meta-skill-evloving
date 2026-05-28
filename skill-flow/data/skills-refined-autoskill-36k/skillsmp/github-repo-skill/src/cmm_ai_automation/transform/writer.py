"""
KGX file writer for nodes and edges.

This module provides functions to write KGX nodes and edges to JSON Lines
format, which is the least lossy serialization format for KGX.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.transform.kgx import KGXEdge, KGXNode

logger = logging.getLogger(__name__)


def deduplicate_nodes(nodes: list[KGXNode]) -> list[KGXNode]:
    """
    Deduplicate nodes by ID, merging properties.

    When multiple nodes have the same ID, this function merges their properties:
    - List fields are combined and deduplicated
    - Scalar fields prefer non-None values
    - Later nodes override earlier ones for conflicting scalars

    Parameters
    ----------
    nodes : list[KGXNode]
        List of nodes that may contain duplicates

    Returns
    -------
    list[KGXNode]
        Deduplicated list of nodes

    Examples
    --------
    >>> from cmm_ai_automation.transform.kgx import KGXNode
    >>> nodes = [
    ...     KGXNode(
    ...         id="NCBITaxon:408",
    ...         category=["biolink:OrganismTaxon"],
    ...         name="Methylorubrum extorquens",
    ...         provided_by=["infores:ncbi"]
    ...     ),
    ...     KGXNode(
    ...         id="NCBITaxon:408",
    ...         category=["biolink:OrganismTaxon"],
    ...         name="Methylorubrum extorquens",
    ...         provided_by=["infores:bacdive"]
    ...     ),
    ... ]
    >>> deduped = deduplicate_nodes(nodes)
    >>> len(deduped)
    1
    >>> sorted(deduped[0].provided_by)
    ['infores:bacdive', 'infores:ncbi']
    """
    node_map: dict[str, dict] = {}

    for node in nodes:
        node_id = node.id
        node_dict = node.model_dump(exclude_none=True)

        if node_id not in node_map:
            # First occurrence - add as-is
            node_map[node_id] = node_dict
        else:
            # Merge with existing
            existing = node_map[node_id]

            # Merge each field
            for key, value in node_dict.items():
                if key not in existing:
                    # New field - add it
                    existing[key] = value
                elif isinstance(value, list) and isinstance(existing[key], list):
                    # Both are lists - combine and deduplicate
                    combined = existing[key] + value
                    # Deduplicate while preserving order
                    seen = set()
                    deduped = []
                    for item in combined:
                        # Use JSON string for hashability
                        item_key = json.dumps(item, sort_keys=True) if isinstance(item, dict) else item
                        if item_key not in seen:
                            seen.add(item_key)
                            deduped.append(item)
                    existing[key] = deduped
                # For scalar fields, later values override earlier ones
                # (current behavior - could also prefer non-None values)

    # Reconstruct KGXNode objects
    from cmm_ai_automation.transform.kgx import KGXNode

    deduplicated = [KGXNode(**node_dict) for node_dict in node_map.values()]

    logger.info(f"Deduplicated {len(nodes)} nodes to {len(deduplicated)} unique nodes")

    return deduplicated


def generate_edge_id(edge: KGXEdge) -> str:
    """
    Generate a deterministic edge ID from edge properties.

    Uses SHA256 hash of subject, predicate, and object to create a
    deterministic, collision-resistant edge ID.

    Parameters
    ----------
    edge : KGXEdge
        The edge to generate an ID for

    Returns
    -------
    str
        Deterministic edge ID

    Examples
    --------
    >>> from cmm_ai_automation.transform.kgx import KGXEdge
    >>> edge = KGXEdge(
    ...     subject="bacdive:7142",
    ...     predicate="biolink:in_taxon",
    ...     object="NCBITaxon:408",
    ...     knowledge_level="knowledge_assertion",
    ...     agent_type="manual_agent"
    ... )
    >>> edge_id = generate_edge_id(edge)
    >>> edge_id.startswith("edge_")
    True
    >>> len(edge_id)
    69

    >>> # Same edge should produce same ID
    >>> edge2 = KGXEdge(
    ...     subject="bacdive:7142",
    ...     predicate="biolink:in_taxon",
    ...     object="NCBITaxon:408",
    ...     knowledge_level="knowledge_assertion",
    ...     agent_type="manual_agent"
    ... )
    >>> generate_edge_id(edge2) == edge_id
    True
    """
    # Create deterministic string from subject, predicate, object
    key = f"{edge.subject}|{edge.predicate}|{edge.object}"
    # SHA256 hash for collision resistance
    hash_digest = hashlib.sha256(key.encode()).hexdigest()
    return f"edge_{hash_digest}"


def write_kgx_jsonl(
    nodes: list[KGXNode],
    edges: list[KGXEdge],
    output_dir: str | Path,
    basename: str,
    *,
    deduplicate: bool = True,
    generate_ids: bool = True,
) -> tuple[Path, Path]:
    """
    Write KGX nodes and edges to JSON Lines files.

    Creates two files:
    - {basename}_nodes.jsonl - One node per line
    - {basename}_edges.jsonl - One edge per line

    JSON Lines format is the least lossy format for KGX serialization,
    preserving all fields and maintaining compatibility with KGX tools.

    Parameters
    ----------
    nodes : list[KGXNode]
        List of nodes to write
    edges : list[KGXEdge]
        List of edges to write
    output_dir : str or Path
        Directory to write output files
    basename : str
        Base name for output files (without extension)
    deduplicate : bool, optional
        Whether to deduplicate nodes before writing, by default True
    generate_ids : bool, optional
        Whether to generate deterministic edge IDs, by default True

    Returns
    -------
    tuple[Path, Path]
        Paths to (nodes_file, edges_file)

    Examples
    --------
    >>> from cmm_ai_automation.transform.kgx import KGXNode, KGXEdge
    >>> import tempfile
    >>> nodes = [
    ...     KGXNode(
    ...         id="bacdive:7142",
    ...         category=["biolink:OrganismTaxon"],
    ...         name="Methylorubrum extorquens DSM:1337"
    ...     )
    ... ]
    >>> edges = [
    ...     KGXEdge(
    ...         subject="bacdive:7142",
    ...         predicate="biolink:in_taxon",
    ...         object="NCBITaxon:408",
    ...         knowledge_level="knowledge_assertion",
    ...         agent_type="manual_agent"
    ...     )
    ... ]
    >>> with tempfile.TemporaryDirectory() as tmpdir:
    ...     nodes_file, edges_file = write_kgx_jsonl(
    ...         nodes, edges, tmpdir, "test"
    ...     )
    ...     print(f"Wrote {nodes_file.name} and {edges_file.name}")
    Wrote test_nodes.jsonl and test_edges.jsonl
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Deduplicate nodes if requested
    if deduplicate:
        nodes = deduplicate_nodes(nodes)

    # Generate edge IDs if requested
    if generate_ids:
        for edge in edges:
            if edge.id is None:
                edge.id = generate_edge_id(edge)

    # Write nodes
    nodes_file = output_dir / f"{basename}_nodes.jsonl"
    with nodes_file.open("w") as f:
        for node in nodes:
            # Serialize with all fields, exclude None values
            node_dict = node.model_dump(exclude_none=True, mode="json")
            f.write(json.dumps(node_dict, sort_keys=True))
            f.write("\n")

    logger.info(f"Wrote {len(nodes)} nodes to {nodes_file}")

    # Write edges
    edges_file = output_dir / f"{basename}_edges.jsonl"
    with edges_file.open("w") as f:
        for edge in edges:
            # Serialize with all fields, exclude None values
            edge_dict = edge.model_dump(exclude_none=True, mode="json")
            f.write(json.dumps(edge_dict, sort_keys=True))
            f.write("\n")

    logger.info(f"Wrote {len(edges)} edges to {edges_file}")

    return nodes_file, edges_file


def flatten_results(
    results: list[tuple[list[KGXNode], list[KGXEdge]]],
) -> tuple[list[KGXNode], list[KGXEdge]]:
    """
    Flatten a list of (nodes, edges) tuples into separate node and edge lists.

    Useful for collecting results from multiple document transformations
    before writing to files.

    Parameters
    ----------
    results : list[tuple[list[KGXNode], list[KGXEdge]]]
        List of (nodes, edges) tuples from transformations

    Returns
    -------
    tuple[list[KGXNode], list[KGXEdge]]
        Tuple of (all_nodes, all_edges)

    Examples
    --------
    >>> from cmm_ai_automation.transform.kgx import KGXNode, KGXEdge
    >>> results = [
    ...     (
    ...         [KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"])],
    ...         [KGXEdge(
    ...             subject="bacdive:1",
    ...             predicate="biolink:in_taxon",
    ...             object="NCBITaxon:1",
    ...             knowledge_level="knowledge_assertion",
    ...             agent_type="manual_agent"
    ...         )]
    ...     ),
    ...     (
    ...         [KGXNode(id="bacdive:2", category=["biolink:OrganismTaxon"])],
    ...         [KGXEdge(
    ...             subject="bacdive:2",
    ...             predicate="biolink:in_taxon",
    ...             object="NCBITaxon:2",
    ...             knowledge_level="knowledge_assertion",
    ...             agent_type="manual_agent"
    ...         )]
    ...     ),
    ... ]
    >>> nodes, edges = flatten_results(results)
    >>> len(nodes)
    2
    >>> len(edges)
    2
    """
    all_nodes: list[KGXNode] = []
    all_edges: list[KGXEdge] = []

    for nodes, edges in results:
        all_nodes.extend(nodes)
        all_edges.extend(edges)

    return all_nodes, all_edges
