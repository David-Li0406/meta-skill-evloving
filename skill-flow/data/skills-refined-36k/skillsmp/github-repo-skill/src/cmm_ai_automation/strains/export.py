"""KGX node and edge export for strain records.

This module provides functions to export strain records to KGX
(Knowledge Graph Exchange) format TSV files.
"""

from __future__ import annotations

import csv
import logging
from pathlib import Path  # noqa: TC003 - Path is used at runtime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cmm_ai_automation.strains.models import StrainRecord

from cmm_ai_automation.strains.models import RANK_TO_TAXRANK, TAXRANK_LABELS

logger = logging.getLogger(__name__)

# Biolink predicate and category for taxonomic hierarchy edges
SUBCLASS_OF_PREDICATE = "biolink:subclass_of"
TAXON_ASSOCIATION_CATEGORY = "biolink:TaxonToTaxonAssociation"

# Biolink category for TaxonomicRank nodes
TAXONOMIC_RANK_CATEGORY = "biolink:OntologyClass"


def export_kgx_nodes(records: list[StrainRecord], output_path: Path) -> None:
    """Export strain records to KGX nodes.tsv format.

    Args:
        records: List of consolidated strain records
        output_path: Path to output TSV file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id",
        "category",
        "name",
        "strain_designation",
        "ncbi_taxon_id",
        "species_taxon_id",
        "parent_taxon_id",
        "has_taxonomic_rank",
        "bacdive_id",
        "genome_accession",
        "xrefs",
        "synonyms",
        "source_sheet",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for record in records:
            row = record.to_kgx_node()
            writer.writerow(row)

    logger.info(f"Exported {len(records)} strain nodes to {output_path}")


def export_kgx_edges(records: list[StrainRecord], output_path: Path) -> int:
    """Export taxonomic hierarchy edges to KGX edges.tsv format.

    Generates subclass_of edges connecting strains to their parent species taxon.
    Only produces edges when a strain has both:
    - An NCBI taxon ID (or other canonical ID)
    - A species_taxon_id that differs from its primary ID

    Args:
        records: List of consolidated strain records
        output_path: Path to output TSV file

    Returns:
        Number of edges exported
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id",
        "subject",
        "predicate",
        "object",
        "category",
    ]

    edge_count = 0
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for record in records:
            # Get the canonical ID for this strain
            node = record.to_kgx_node()
            subject_id = node["id"]

            # Only create edge if we have a species taxon and it's different
            if record.species_taxon_id:
                species_curie = record.species_taxon_id
                if not species_curie.startswith("NCBITaxon:"):
                    species_curie = f"NCBITaxon:{species_curie}"

                # Don't create self-loops
                if species_curie != subject_id:
                    edge_id = f"{subject_id}--{SUBCLASS_OF_PREDICATE}--{species_curie}"
                    writer.writerow(
                        {
                            "id": edge_id,
                            "subject": subject_id,
                            "predicate": SUBCLASS_OF_PREDICATE,
                            "object": species_curie,
                            "category": TAXON_ASSOCIATION_CATEGORY,
                        }
                    )
                    edge_count += 1

    logger.info(f"Exported {edge_count} taxonomic hierarchy edges to {output_path}")
    return edge_count


def export_taxrank_nodes(records: list[StrainRecord], output_path: Path) -> int:
    """Export TaxonomicRank nodes to provide CURIE→label mapping.

    Creates nodes for each TAXRANK term used by the strain records,
    enabling lookup of rank labels by CURIE in the knowledge graph.

    Args:
        records: List of strain records (to determine which ranks are used)
        output_path: Path to output TSV file

    Returns:
        Number of rank nodes exported
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Collect unique ranks used
    used_ranks: set[str] = set()
    for record in records:
        if record.has_taxonomic_rank:
            taxrank_curie = RANK_TO_TAXRANK.get(record.has_taxonomic_rank, "")
            if taxrank_curie:
                used_ranks.add(taxrank_curie)

    fieldnames = ["id", "category", "name"]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for taxrank_curie in sorted(used_ranks):
            label = TAXRANK_LABELS.get(taxrank_curie, "")
            writer.writerow(
                {
                    "id": taxrank_curie,
                    "category": TAXONOMIC_RANK_CATEGORY,
                    "name": label,
                }
            )

    logger.info(f"Exported {len(used_ranks)} TaxonomicRank nodes to {output_path}")
    return len(used_ranks)
