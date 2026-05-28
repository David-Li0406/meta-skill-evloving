#!/usr/bin/env python3
"""
Export media-ingredient relationships to KGX format.

Creates edges: CMM:medium_* -[has_part]-> CHEBI:*

Input: data/private/media_ingredients.tsv
Output: output/kgx/media_ingredients_nodes.tsv, output/kgx/media_ingredients_edges.tsv
"""

import csv
from dataclasses import dataclass
from pathlib import Path

import click
from kgx.sink import TsvSink
from kgx.transformer import Transformer

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "private"
OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx"

# Biolink predicate for composition
HAS_PART_PREDICATE = "biolink:has_part"
HAS_PART_LABEL = "has part"

# Category for chemical ingredients
INGREDIENT_CATEGORY = "biolink:ChemicalEntity"
INGREDIENT_CATEGORY_LABEL = "chemical entity"

# CMM medium prefix (must match export_growth_kgx.py)
CMM_MEDIUM_PREFIX = "CMM:medium_"

# Provenance
KNOWLEDGE_LEVEL = "knowledge_assertion"
AGENT_TYPE = "manual_agent"


def normalize_medium_id(media_id: str) -> str:
    """Convert media_id to CMM CURIE format."""
    # Lowercase and replace spaces/special chars
    local_id = media_id.lower().strip()
    local_id = local_id.replace(" ", "-").replace("_", "-")
    return f"{CMM_MEDIUM_PREFIX}{local_id}"


@dataclass
class IngredientNode:
    """Ingredient node for KGX."""

    id: str  # CHEBI:*
    name: str

    def to_kgx_node(self) -> dict:
        return {
            "id": self.id,
            "category": [INGREDIENT_CATEGORY],
            "category_label": [INGREDIENT_CATEGORY_LABEL],
            "name": self.name,
            "provided_by": ["cmm-ai-automation"],
        }


@dataclass
class MediaIngredientEdge:
    """Media contains ingredient edge."""

    medium_id: str  # CMM:medium_*
    ingredient_id: str  # CHEBI:*
    concentration: str = ""
    unit: str = ""
    role: str = ""

    def to_kgx_edge(self) -> dict:
        edge = {
            "subject": self.medium_id,
            "predicate": HAS_PART_PREDICATE,
            "relation_label": HAS_PART_LABEL,
            "object": self.ingredient_id,
            "knowledge_level": KNOWLEDGE_LEVEL,
            "agent_type": AGENT_TYPE,
        }
        # Add concentration as edge property if available
        if self.concentration and self.unit:
            edge["concentration"] = f"{self.concentration} {self.unit}"
        if self.role:
            edge["role"] = self.role
        return edge


def load_media_ingredients(filepath: Path) -> tuple[dict[str, IngredientNode], list[MediaIngredientEdge]]:
    """Load media-ingredient relationships from TSV."""
    ingredients = {}  # id -> IngredientNode
    edges = []

    with filepath.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            ontology_id = row.get("ontology_id", "").strip()
            if not ontology_id or not ontology_id.startswith("CHEBI:"):
                # Skip rows without CHEBI ID
                continue

            # Handle multiple IDs (e.g., "CHEBI:31206; solution:6306")
            chebi_id = ontology_id.split(";")[0].strip()

            media_id = row.get("media_id", "").strip()
            if not media_id:
                continue

            # Create ingredient node
            ingredient_name = row.get("ingredient_name", "").strip()
            ontology_label = row.get("ontology_label", "").strip()
            name = ontology_label if ontology_label else ingredient_name

            if chebi_id not in ingredients:
                ingredients[chebi_id] = IngredientNode(id=chebi_id, name=name)

            # Create edge
            medium_curie = normalize_medium_id(media_id)
            edge = MediaIngredientEdge(
                medium_id=medium_curie,
                ingredient_id=chebi_id,
                concentration=row.get("concentration", ""),
                unit=row.get("unit", ""),
                role=row.get("role", ""),
            )
            edges.append(edge)

    return ingredients, edges


def export_kgx(nodes: list[dict], edges: list[dict], output_path: Path) -> None:
    """Export nodes and edges to KGX TSV format."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    transformer = Transformer()

    node_props = {"id", "category", "category_label", "name", "provided_by"}
    edge_props = {
        "subject",
        "predicate",
        "relation_label",
        "object",
        "knowledge_level",
        "agent_type",
        "concentration",
        "role",
    }

    sink = TsvSink(
        owner=transformer,
        filename=str(output_path),
        format="tsv",
        node_properties=node_props,
        edge_properties=edge_props,
    )

    for node in nodes:
        sink.write_node(node)
    for edge in edges:
        sink.write_edge(edge)

    sink.finalize()
    click.echo(f"INFO: Exported {len(nodes)} nodes and {len(edges)} edges to {output_path}")


@click.command()
@click.option(
    "--input",
    "input_file",
    type=click.Path(exists=True, path_type=Path),
    default=DATA_DIR / "media_ingredients.tsv",
    help="Input media ingredients TSV file",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    default=OUTPUT_DIR / "media_ingredients",
    help="Output path prefix for KGX files",
)
def main(input_file: Path, output_path: Path) -> None:
    """Export media-ingredient relationships to KGX format."""
    click.echo("=" * 60)
    click.echo("Export Media Ingredients to KGX")
    click.echo("=" * 60)
    click.echo()

    # Load data
    ingredients, edges = load_media_ingredients(input_file)
    click.echo(f"Loaded {len(ingredients)} unique ingredients")
    click.echo(f"Loaded {len(edges)} media-ingredient relationships")

    # Convert to KGX format
    ingredient_nodes = [ing.to_kgx_node() for ing in ingredients.values()]
    ingredient_edges = [e.to_kgx_edge() for e in edges]

    # Export
    export_kgx(ingredient_nodes, ingredient_edges, output_path)

    click.echo()
    click.echo("=" * 60)
    click.echo("Summary")
    click.echo("=" * 60)
    click.echo(f"Ingredient nodes: {len(ingredient_nodes)}")
    click.echo(f"Contains edges:   {len(ingredient_edges)}")
    click.echo(f"Predicate:        {HAS_PART_PREDICATE} ({HAS_PART_LABEL})")
    click.echo()
    click.echo(f"Output: {output_path}_nodes.tsv, {output_path}_edges.tsv")
    click.echo()
    click.echo("Done!")


if __name__ == "__main__":
    main()
