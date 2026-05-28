"""Bridge between PydanticAI reconciliation and KGX clique merge.

This module converts PydanticAI ReconciliationResults into KGX-compatible
`biolink:same_as` edges that can be consumed by KGX clique merge.

Example workflow:
    1. PydanticAI compares strain candidates and produces ReconciliationResults
    2. This bridge converts matches to same_as edges
    3. KGX clique merge consolidates the graph using those edges
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path  # noqa: TC003 - used at runtime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.reconcile.agent import MatchConfidence, ReconciliationResult

logger = logging.getLogger(__name__)

# Biolink predicate for equivalence
SAME_AS_PREDICATE = "biolink:same_as"
ASSOCIATION_CATEGORY = "biolink:Association"

# Prefix priority for KGX leader election
# Higher in list = higher priority for being the canonical ID
PREFIX_PRIORITY = [
    "NCBITaxon",  # Authoritative taxonomy
    "bacdive",  # Culture collection database
    "dsmz",  # DSMZ culture collection
    "atcc",  # ATCC culture collection
    "jcm",  # JCM culture collection
    "nbrc",  # NBRC culture collection
    "cip",  # CIP culture collection
    "cmm",  # Our local IDs (lowest priority)
]


def reconciliation_to_same_as_edge(
    subject_id: str,
    object_id: str,
    result: ReconciliationResult,
) -> dict[str, str]:
    """Convert a ReconciliationResult to a KGX same_as edge.

    Args:
        subject_id: ID of the first entity
        object_id: ID of the second entity
        result: PydanticAI reconciliation result

    Returns:
        KGX edge dictionary with same_as relationship
    """
    edge_id = f"{subject_id}--{SAME_AS_PREDICATE}--{object_id}"

    return {
        "id": edge_id,
        "subject": subject_id,
        "predicate": SAME_AS_PREDICATE,
        "object": object_id,
        "category": ASSOCIATION_CATEGORY,
        # Store reconciliation metadata as edge properties
        "reconciliation_confidence": result.confidence.value,
        "reconciliation_reasoning": result.reasoning[:500],  # Truncate long reasoning
        "matched_fields": "|".join(result.matched_fields),
    }


def filter_high_confidence_matches(
    results: list[tuple[str, str, ReconciliationResult]],
    min_confidence: MatchConfidence,
) -> list[tuple[str, str, ReconciliationResult]]:
    """Filter reconciliation results by minimum confidence.

    Args:
        results: List of (subject_id, object_id, result) tuples
        min_confidence: Minimum confidence level to include

    Returns:
        Filtered list of results meeting confidence threshold
    """
    from cmm_ai_automation.reconcile.agent import MatchConfidence

    confidence_order = [MatchConfidence.HIGH, MatchConfidence.MEDIUM, MatchConfidence.LOW, MatchConfidence.NONE]
    min_index = confidence_order.index(min_confidence)

    filtered = []
    for subject_id, object_id, result in results:
        if result.is_match:
            conf_index = confidence_order.index(result.confidence)
            if conf_index <= min_index:
                filtered.append((subject_id, object_id, result))

    return filtered


def export_same_as_edges(
    results: list[tuple[str, str, ReconciliationResult]],
    output_path: Path,
    min_confidence: MatchConfidence | None = None,
) -> int:
    """Export reconciliation results as KGX same_as edges TSV.

    Args:
        results: List of (subject_id, object_id, result) tuples
        output_path: Path to output TSV file
        min_confidence: Optional minimum confidence filter

    Returns:
        Number of edges exported
    """

    # Filter if requested
    if min_confidence:
        results = filter_high_confidence_matches(results, min_confidence)
    else:
        # Default: only export matches
        results = [(s, o, r) for s, o, r in results if r.is_match]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id",
        "subject",
        "predicate",
        "object",
        "category",
        "reconciliation_confidence",
        "reconciliation_reasoning",
        "matched_fields",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for subject_id, object_id, result in results:
            edge = reconciliation_to_same_as_edge(subject_id, object_id, result)
            writer.writerow(edge)

    logger.info(f"Exported {len(results)} same_as edges to {output_path}")
    return len(results)


def generate_kgx_merge_config(
    nodes_files: list[Path],
    edges_files: list[Path],
    same_as_file: Path,
    output_dir: Path,
) -> dict:
    """Generate KGX merge configuration YAML content.

    This creates a configuration that KGX CLI can use to:
    1. Load strain nodes and edges
    2. Load same_as edges from reconciliation
    3. Run clique merge with prefix prioritization
    4. Output merged graph

    Args:
        nodes_files: List of node TSV files
        edges_files: List of edge TSV files (including same_as)
        same_as_file: Path to same_as edges from reconciliation
        output_dir: Output directory for merged graph

    Returns:
        Dictionary representing KGX merge config
    """
    config = {
        "configuration": {
            "output_directory": str(output_dir),
            "checkpoint": False,
        },
        "target": {
            "filename": [str(f) for f in nodes_files],
            "format": "tsv",
        },
        "source": [
            {
                "name": "strain_edges",
                "filename": [str(f) for f in edges_files],
                "format": "tsv",
            },
            {
                "name": "reconciliation_same_as",
                "filename": [str(same_as_file)],
                "format": "tsv",
            },
        ],
        "operations": [
            {
                "name": "clique_merge",
                "args": {
                    "prefix_prioritization_map": {prefix: i for i, prefix in enumerate(PREFIX_PRIORITY)},
                },
            },
        ],
    }

    return config


# Example usage documentation
__doc__ += """

## Example Workflow

```python
from cmm_ai_automation.reconcile.agent import StrainReconciler, StrainCandidate, MatchConfidence
from cmm_ai_automation.reconcile.kgx_bridge import export_same_as_edges, generate_kgx_merge_config

# 1. Run PydanticAI reconciliation
reconciler = StrainReconciler()
results = []

for input_strain in input_strains:
    for bacdive_candidate in bacdive_candidates:
        result = await reconciler.compare_strains(input_strain, bacdive_candidate)
        if result.is_match:
            results.append((input_strain.identifier, bacdive_candidate.identifier, result))

# 2. Export same_as edges
export_same_as_edges(
    results,
    Path("output/kgx/same_as_edges.tsv"),
    min_confidence=MatchConfidence.MEDIUM,
)

# 3. Generate KGX config for clique merge
config = generate_kgx_merge_config(
    nodes_files=[Path("output/kgx/strains_nodes.tsv")],
    edges_files=[Path("output/kgx/strains_edges.tsv")],
    same_as_file=Path("output/kgx/same_as_edges.tsv"),
    output_dir=Path("output/kgx/merged"),
)

# 4. Run KGX merge (CLI or programmatic)
# kgx merge --config merge_config.yaml
```
"""
