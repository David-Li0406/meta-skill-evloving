#!/usr/bin/env python3
"""Export growth preferences to KGX format.

Creates KGX-formatted files for strain-medium growth relationships:
- media_nodes: Local cmm:medium/* nodes (METPO:1004005 category)
- grows_in_edges: strain -[METPO:2000517]-> medium edges

Uses strains_nodes.tsv output from export_strains_kgx.py as strain source
to ensure consistent NCBITaxon/BacDive identifiers.

Ontology usage:
- METPO:1004005 = growth medium class
- METPO:2000517 = grows_in predicate
- METPO:2000518 = does_not_grow_in predicate (for negative results)

Uses KGX Transformer and Sink classes for proper serialization.

Usage:
    uv run python -m cmm_ai_automation.scripts.export_growth_kgx
    uv run python -m cmm_ai_automation.scripts.export_growth_kgx --format jsonl
    uv run python -m cmm_ai_automation.scripts.export_growth_kgx --dry-run
"""

from __future__ import annotations

import csv
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import click
from kgx.sink import JsonlSink, TsvSink
from kgx.transformer import Transformer

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "private"
OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx"

# METPO ontology terms with human-readable labels
MEDIUM_CATEGORY = "METPO:1004005"  # growth medium
MEDIUM_CATEGORY_LABEL = "growth medium"
GROWS_IN_PREDICATE = "METPO:2000517"  # grows_in
GROWS_IN_LABEL = "grows in medium"
DOES_NOT_GROW_IN_PREDICATE = "METPO:2000518"  # does_not_grow_in
DOES_NOT_GROW_IN_LABEL = "does not grow in medium"

# CMM namespace for local IDs
# Note: Using underscore instead of slash to comply with CURIE format (slashes
# are only valid in DOIs). See KGX validation requirements.
CMM_MEDIUM_PREFIX = "CMM:medium_"

# Provenance metadata (Biolink enum values)
KNOWLEDGE_LEVEL = "knowledge_assertion"
AGENT_TYPE = "manual_agent"
# infores CURIEs pending registration: see GitHub issues #110, #111
# https://github.com/biolink/information-resource-registry/issues/110
# https://github.com/biolink/information-resource-registry/issues/111


@dataclass
class MediumRecord:
    """Growth medium record for KGX export."""

    id: str  # cmm:medium/local_id
    name: str
    description: str = ""
    media_type: str = ""
    ph: str = ""
    references: str = ""
    source_reference: str = ""

    def to_kgx_node(self) -> dict:
        """Convert to KGX node dict for use with KGX Sink.write_node()."""
        node = {
            "id": self.id,
            "category": [MEDIUM_CATEGORY],  # KGX expects list for category
            "category_label": [MEDIUM_CATEGORY_LABEL],
            "name": self.name,
            "provided_by": ["cmm-ai-automation"],
        }
        if self.description:
            node["description"] = self.description
        return node


@dataclass
class GrowthEdge:
    """Growth preference edge for KGX export."""

    strain_id: str  # NCBITaxon:* or bacdive:*
    medium_id: str  # cmm:medium/*
    grows: bool = True  # True = grows, False = does not grow

    def to_kgx_edge(self) -> dict:
        """Convert to KGX edge dict for use with KGX Sink.write_edge()."""
        if self.grows:
            predicate = GROWS_IN_PREDICATE
            predicate_label = GROWS_IN_LABEL
        else:
            predicate = DOES_NOT_GROW_IN_PREDICATE
            predicate_label = DOES_NOT_GROW_IN_LABEL
        return {
            "subject": self.strain_id,
            "predicate": predicate,
            "relation_label": predicate_label,
            "object": self.medium_id,
            "knowledge_level": KNOWLEDGE_LEVEL,
            "agent_type": AGENT_TYPE,
        }


def normalize_medium_id(name: str) -> str:
    """Convert medium name to a safe local ID.

    Examples:
        >>> normalize_medium_id("MP")
        'mp'
        >>> normalize_medium_id("Hypho medium ")
        'hypho-medium'
        >>> normalize_medium_id("MP-Methanol")
        'mp-methanol'
    """
    # Lowercase, strip, replace spaces with hyphens
    safe = name.lower().strip()
    safe = re.sub(r"\s+", "-", safe)
    # Remove trailing hyphens
    safe = safe.rstrip("-")
    # Remove special characters except hyphen
    safe = re.sub(r"[^a-z0-9-]", "", safe)
    return safe


def load_growth_media(media_file: Path) -> list[MediumRecord]:
    """Load growth media from TSV file.

    Args:
        media_file: Path to growth_media.tsv

    Returns:
        List of MediumRecord objects
    """
    records: list[MediumRecord] = []

    if not media_file.exists():
        logger.warning(f"Media file not found: {media_file}")
        return records

    with media_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            media_id = row.get("media_id", "").strip()
            media_name = row.get("media_name", "").strip()

            # Skip empty rows
            if not media_id and not media_name:
                continue

            # Use media_id if available, otherwise derive from name
            display_name = media_name or media_id
            local_id = normalize_medium_id(media_id or media_name)

            record = MediumRecord(
                id=f"{CMM_MEDIUM_PREFIX}{local_id}",
                name=display_name,
                description=row.get("description", ""),
                media_type=row.get("media_type", ""),
                ph=row.get("ph", ""),
                references=row.get("references", ""),
            )
            records.append(record)

    logger.info(f"Loaded {len(records)} media from {media_file.name}")
    return records


def load_strain_id_mapping(strains_nodes_file: Path) -> dict[str, str]:
    """Load strain name -> canonical ID mapping from strains_nodes.tsv.

    Uses the output from export_strains_kgx.py to ensure consistent IDs.
    Indexes by exact name (case-insensitive) only - reconciliation happens upstream.

    Args:
        strains_nodes_file: Path to strains_nodes.tsv from export_strains_kgx

    Returns:
        Dict mapping strain name (lowercase) -> canonical ID (NCBITaxon/bacdive)
    """
    mapping: dict[str, str] = {}

    if not strains_nodes_file.exists():
        logger.warning(f"Strains nodes file not found: {strains_nodes_file}")
        logger.warning("Run export_strains_kgx.py first to generate strain mappings")
        return mapping

    with strains_nodes_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            canonical_id = row.get("id", "").strip()
            name = row.get("name", "").strip()

            if not canonical_id or not name:
                continue

            # Index by full name (lowercase)
            mapping[name.lower()] = canonical_id

    logger.info(f"Loaded {len(mapping)} strain name mappings from {strains_nodes_file.name}")
    return mapping


def load_growth_preferences(
    prefs_file: Path, strain_mapping: dict[str, str], media_records: list[MediumRecord]
) -> tuple[list[GrowthEdge], int, int]:
    """Load growth preferences and create edges.

    Args:
        prefs_file: Path to growth_preferences.tsv
        strain_mapping: Strain name -> canonical ID mapping
        media_records: List of MediumRecord for medium ID lookup

    Returns:
        Tuple of (edges, matched_count, unmatched_count)
    """
    edges: list[GrowthEdge] = []
    matched = 0
    unmatched_strains: set[str] = set()
    unmatched_media: set[str] = set()

    if not prefs_file.exists():
        logger.warning(f"Growth preferences file not found: {prefs_file}")
        return edges, 0, 0

    # Build medium name -> ID mapping
    medium_map: dict[str, str] = {}
    for m in media_records:
        # Map by normalized local_id
        local_id = m.id.replace(CMM_MEDIUM_PREFIX, "")
        medium_map[local_id] = m.id
        # Also map by original name (case-insensitive)
        medium_map[m.name.lower().strip()] = m.id

    with prefs_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for _row_num, row in enumerate(reader, start=2):
            scientific_name = row.get("scientific name with strain id", "").strip()
            medium_name = row.get("Growth Media", "").strip()
            growth_result = row.get("Growth result binary", "").strip()

            if not scientific_name or not medium_name:
                continue

            # Look up strain ID by exact name match
            strain_id = strain_mapping.get(scientific_name.lower())

            if not strain_id:
                unmatched_strains.add(scientific_name)
                continue

            # Look up medium ID
            medium_key = normalize_medium_id(medium_name)
            medium_id = medium_map.get(medium_key)

            if not medium_id:
                # Try exact name match
                medium_id = medium_map.get(medium_name.lower().strip())

            if not medium_id:
                unmatched_media.add(medium_name)
                continue

            # Determine growth result
            grows = growth_result == "1" if growth_result else True

            edge = GrowthEdge(
                strain_id=strain_id,
                medium_id=medium_id,
                grows=grows,
            )
            edges.append(edge)
            matched += 1

    if unmatched_strains:
        logger.warning(f"Unmatched strains ({len(unmatched_strains)}):")
        for name in sorted(unmatched_strains)[:5]:
            logger.warning(f"  - {name}")
        if len(unmatched_strains) > 5:
            logger.warning(f"  ... and {len(unmatched_strains) - 5} more")

    if unmatched_media:
        logger.warning(f"Unmatched media ({len(unmatched_media)}):")
        for name in sorted(unmatched_media):
            logger.warning(f"  - {name}")

    return edges, matched, len(unmatched_strains) + len(unmatched_media)


def export_kgx(
    nodes: list[MediumRecord],
    edges: list[GrowthEdge],
    output_path: Path,
    output_format: Literal["tsv", "jsonl"] = "tsv",
) -> tuple[int, int]:
    """Export nodes and edges using KGX Sink classes.

    Args:
        nodes: List of MediumRecord
        edges: List of GrowthEdge
        output_path: Base path for output (without extension)
        output_format: Output format - 'tsv' or 'jsonl'

    Returns:
        Tuple of (nodes_count, edges_count)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create KGX transformer and sink
    transformer = Transformer()

    # Specify which properties to include in output
    node_props = {"id", "category", "category_label", "name", "description", "provided_by"}
    edge_props = {"subject", "predicate", "relation_label", "object", "knowledge_level", "agent_type"}

    if output_format == "jsonl":
        sink = JsonlSink(owner=transformer, filename=str(output_path))
    else:
        sink = TsvSink(
            owner=transformer,
            filename=str(output_path),
            format="tsv",
            node_properties=node_props,
            edge_properties=edge_props,
        )

    # Write nodes
    for record in nodes:
        sink.write_node(record.to_kgx_node())

    # Write edges
    for edge in edges:
        sink.write_edge(edge.to_kgx_edge())

    # Finalize to flush and close files
    sink.finalize()

    logger.info(f"Exported {len(nodes)} nodes and {len(edges)} edges to {output_path}")
    return len(nodes), len(edges)


@click.command()
@click.option(
    "--media-tsv",
    type=click.Path(exists=False, path_type=Path),
    default=DATA_DIR / "growth_media.tsv",
    help="Path to growth_media.tsv",
)
@click.option(
    "--prefs-tsv",
    type=click.Path(exists=False, path_type=Path),
    default=DATA_DIR / "growth_preferences.tsv",
    help="Path to growth_preferences.tsv",
)
@click.option(
    "--strains-nodes",
    type=click.Path(exists=False, path_type=Path),
    default=OUTPUT_DIR / "strains_nodes.tsv",
    help="Path to strains_nodes.tsv from export_strains_kgx",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=OUTPUT_DIR / "growth",
    help="Output base path (KGX creates _nodes and _edges files)",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["tsv", "jsonl"]),
    default="tsv",
    help="Output format (use 'kgx transform' for other formats)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Parse data but don't write output",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
def main(
    media_tsv: Path,
    prefs_tsv: Path,
    strains_nodes: Path,
    output: Path,
    format: Literal["tsv", "jsonl"],
    dry_run: bool,
    verbose: bool,
) -> None:
    """Export growth preferences to KGX format using KGX Sink classes.

    Requires strains_nodes.tsv from export_strains_kgx.py to map strain names
    to canonical NCBITaxon/BacDive identifiers.

    For other formats, use 'kgx transform' on the output:
        kgx transform -i tsv -f nt -o output.nt output/kgx/growth_nodes.tsv
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    click.echo("=" * 60)
    click.echo("Export Growth Preferences to KGX")
    click.echo("=" * 60)
    click.echo()

    # Load strain ID mapping from strains_nodes.tsv
    strain_mapping = load_strain_id_mapping(strains_nodes)
    if not strain_mapping:
        click.echo("ERROR: No strain mappings found. Run export_strains_kgx.py first.", err=True)
        raise click.Abort()

    # Load media
    media_records = load_growth_media(media_tsv)
    click.echo(f"Loaded {len(media_records)} media records")

    # Load growth preferences and create edges
    edges, matched, unmatched = load_growth_preferences(prefs_tsv, strain_mapping, media_records)
    click.echo(f"Created {len(edges)} growth edges ({matched} matched, {unmatched} unmatched)")

    # Summary
    click.echo()
    click.echo("=" * 60)
    click.echo("Summary")
    click.echo("=" * 60)
    click.echo(f"Media nodes:     {len(media_records)} (local {CMM_MEDIUM_PREFIX}* IDs)")
    click.echo(f"Growth edges:    {len(edges)} (using METPO predicates)")
    click.echo()
    click.echo("Ontology usage:")
    click.echo(f"  Medium category: {MEDIUM_CATEGORY}")
    click.echo(f"  Grows predicate: {GROWS_IN_PREDICATE}")
    click.echo(f"  Does not grow:   {DOES_NOT_GROW_IN_PREDICATE}")
    click.echo()

    ext = "jsonl" if format == "jsonl" else "tsv"
    nodes_file = f"{output}_nodes.{ext}"
    edges_file = f"{output}_edges.{ext}"

    if dry_run:
        click.echo("[DRY RUN] Would export:")
        click.echo(f"  - Nodes to: {nodes_file}")
        click.echo(f"  - Edges to: {edges_file}")
        click.echo()
        click.echo("Sample media nodes:")
        for m in media_records[:3]:
            click.echo(f"  {m.id}: {m.name}")
        click.echo()
        click.echo("Sample edges:")
        for e in edges[:5]:
            pred = "grows_in" if e.grows else "does_not_grow_in"
            click.echo(f"  {e.strain_id} --[{pred}]--> {e.medium_id}")
    else:
        export_kgx(media_records, edges, output, format)
        click.echo()
        click.echo(f"Output files: {nodes_file}, {edges_file}")
        click.echo()
        click.echo("To convert to other formats:")
        click.echo(f"  kgx transform -i {format} -f nt -o output.nt {nodes_file} {edges_file}")
        click.echo()
        click.echo("To validate:")
        click.echo(f"  kgx validate {nodes_file} {edges_file}")

    click.echo()
    click.echo("Done!")


if __name__ == "__main__":
    main()
