#!/usr/bin/env python3
"""Export MediaDive data to KGX format.

Exports all MediaDive entities to KGX-formatted TSV files:

Nodes (all prefixed with mediadive.*):
- mediadive.medium:{id} - Growth media (METPO:1004005)
- mediadive.strain:{id} - Microbial strains (biolink:OrganismTaxon)
- mediadive.ingredient:{id} - Chemical ingredients (biolink:ChemicalEntity)
- mediadive.solution:{id} - Stock solutions (biolink:ChemicalMixture)

Edges:
- strain -[METPO:2000517 grows_in]-> medium
- medium -[RO:0001019 contains]-> ingredient (from medium_compositions - flattened)
- solution -[RO:0001019 contains]-> ingredient (from solution_details)

Note: medium -> solution edges are intentionally omitted due to complex nested
structure (up to 5 levels deep, 42% of solutions reference other solutions).
The flattened medium_compositions provides accurate composition without the ~8%
error rate from hierarchical reconstruction. See GitHub issue #111 for details.

Uses KGX NxGraph for idiomatic graph construction and export.
"""

import logging
from pathlib import Path

import click
from kgx.graph.nx_graph import NxGraph
from kgx.sink import TsvSink
from kgx.transformer import Transformer
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Output paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output" / "kgx"

# Categories
MEDIUM_CATEGORY = "METPO:1004005"
STRAIN_CATEGORY = "biolink:OrganismTaxon"
INGREDIENT_CATEGORY = "biolink:ChemicalEntity"
SOLUTION_CATEGORY = "biolink:ChemicalMixture"

# Predicates
GROWS_IN = "METPO:2000517"
CONTAINS = "RO:0001019"

# Provenance
PROVIDED_BY = "mediadive"


def export_mediadive(mongodb_uri: str, output_path: Path) -> dict:
    """Export all MediaDive data to KGX format.

    Args:
        mongodb_uri: MongoDB connection URI
        output_path: Base path for output files

    Returns:
        Dict with counts of nodes and edges by type
    """
    client = MongoClient(mongodb_uri)
    db = client["mediadive"]

    # Create KGX graph
    graph = NxGraph()

    counts = {
        "media": 0,
        "strains": 0,
        "ingredients": 0,
        "solutions": 0,
        "grows_in_edges": 0,
        "contains_edges": 0,
    }

    # --- Export Media ---
    logger.info("Exporting media...")
    for doc in db.media_details.find():
        medium = doc.get("medium", {})
        node_id = f"mediadive.medium:{doc['_id']}"
        graph.add_node(
            node_id,
            name=medium.get("name"),
            category=[MEDIUM_CATEGORY],
            provided_by=[PROVIDED_BY],
            medium_type="complex" if medium.get("complex_medium") else "defined",
            min_ph=medium.get("min_pH"),
            max_ph=medium.get("max_pH"),
            source=medium.get("source"),
            source_reference=medium.get("link"),
            reference=medium.get("reference"),
        )
        counts["media"] += 1

    logger.info(f"  Exported {counts['media']} media")

    # --- Export Strains and Growth Edges ---
    logger.info("Exporting strains...")
    for doc in db.strains.find():
        strain_id = f"mediadive.strain:{doc['id']}"

        # Build xref for BacDive ID if present
        bacdive_id = doc.get("bacdive_id")
        xrefs = [f"bacdive.strain:{bacdive_id}"] if bacdive_id else None

        # Add strain node
        graph.add_node(
            strain_id,
            name=doc.get("species"),
            category=[STRAIN_CATEGORY],
            provided_by=[PROVIDED_BY],
            culture_collection_id=doc.get("ccno"),
            xref=xrefs,
        )
        counts["strains"] += 1

        # Add growth edges for each medium this strain grows on
        for growth in doc.get("media", []):
            medium_id = growth.get("medium_id")
            if medium_id and growth.get("growth"):
                # medium_id can be int or string like "J22"
                medium_curie = f"mediadive.medium:{medium_id}"
                edge_key = f"{strain_id}-grows_in-{medium_curie}"
                graph.add_edge(
                    strain_id,
                    medium_curie,
                    edge_key,
                    predicate=GROWS_IN,
                    relation_label="grows in medium",
                    knowledge_level="knowledge_assertion",
                    agent_type="manual_agent",
                )
                counts["grows_in_edges"] += 1

    logger.info(f"  Exported {counts['strains']} strains")
    logger.info(f"  Created {counts['grows_in_edges']} grows_in edges")

    # --- Export Ingredients ---
    logger.info("Exporting ingredients...")
    for doc in db.ingredient_details.find():
        node_id = f"mediadive.ingredient:{doc['id']}"

        # Build xrefs list from all available identifiers
        xrefs = []
        if doc.get("ChEBI"):
            xrefs.append(f"CHEBI:{doc['ChEBI']}")
        if doc.get("PubChem"):
            xrefs.append(f"PUBCHEM.COMPOUND:{doc['PubChem']}")
        if doc.get("CAS-RN"):
            xrefs.append(f"CAS:{doc['CAS-RN']}")
        if doc.get("KEGG-Compound"):
            xrefs.append(f"KEGG.COMPOUND:{doc['KEGG-Compound']}")
        if doc.get("BRENDA-Ligand"):
            xrefs.append(f"BRENDA:{doc['BRENDA-Ligand']}")
        if doc.get("MetaCyc"):
            xrefs.append(f"MetaCyc:{doc['MetaCyc']}")
        if doc.get("ZVG"):
            xrefs.append(f"ZVG:{doc['ZVG']}")

        # Build synonyms list
        synonyms = doc.get("synonyms", [])

        graph.add_node(
            node_id,
            name=doc.get("name"),
            category=[INGREDIENT_CATEGORY],
            provided_by=[PROVIDED_BY],
            xref=xrefs if xrefs else None,
            synonym=synonyms if synonyms else None,
            chemical_formula=doc.get("formula"),
            molecular_mass=doc.get("mass"),
            density=doc.get("density"),
            is_complex_mixture=doc.get("complex_compound", False),
        )
        counts["ingredients"] += 1

    logger.info(f"  Exported {counts['ingredients']} ingredients")

    # --- Export Solutions and their composition ---
    logger.info("Exporting solutions...")
    for doc in db.solution_details.find():
        solution_id = f"mediadive.solution:{doc['id']}"

        # Serialize steps and equipment as pipe-delimited if present
        steps = doc.get("steps", [])
        equipment = doc.get("equipment", [])

        graph.add_node(
            solution_id,
            name=doc.get("name"),
            category=[SOLUTION_CATEGORY],
            provided_by=[PROVIDED_BY],
            volume_ml=doc.get("volume"),
            preparation_steps=steps if steps else None,
            equipment=equipment if equipment else None,
        )
        counts["solutions"] += 1

        # Add composition edges for solution ingredients
        for item in doc.get("recipe", []):
            ingredient_id = item.get("id")
            if ingredient_id:
                ingredient_curie = f"mediadive.ingredient:{ingredient_id}"
                edge_key = f"{solution_id}-contains-{ingredient_curie}"

                # Build concentration string
                concentration = None
                if item.get("g_l"):
                    concentration = f"{item['g_l']} g/L"
                elif item.get("mmol_l"):
                    concentration = f"{item['mmol_l']} mmol/L"

                graph.add_edge(
                    solution_id,
                    ingredient_curie,
                    edge_key,
                    predicate=CONTAINS,
                    relation_label="contains",
                    knowledge_level="knowledge_assertion",
                    agent_type="manual_agent",
                    concentration=concentration,
                    optional=bool(item.get("optional")),
                )
                counts["contains_edges"] += 1

    logger.info(f"  Exported {counts['solutions']} solutions")

    # --- Export Medium Compositions ---
    logger.info("Exporting medium compositions...")
    for doc in db.medium_compositions.find():
        medium_id = doc["_id"]
        medium_curie = f"mediadive.medium:{medium_id}"

        for item in doc.get("data", []):
            ingredient_id = item.get("id")
            if ingredient_id:
                ingredient_curie = f"mediadive.ingredient:{ingredient_id}"
                edge_key = f"{medium_curie}-contains-{ingredient_curie}"

                concentration = None
                if item.get("g_l"):
                    concentration = f"{item['g_l']} g/L"
                elif item.get("mmol_l"):
                    concentration = f"{item['mmol_l']} mmol/L"

                graph.add_edge(
                    medium_curie,
                    ingredient_curie,
                    edge_key,
                    predicate=CONTAINS,
                    relation_label="contains",
                    knowledge_level="knowledge_assertion",
                    agent_type="manual_agent",
                    concentration=concentration,
                    optional=bool(item.get("optional")),
                )
                counts["contains_edges"] += 1

    logger.info(f"  Total contains edges: {counts['contains_edges']}")

    client.close()

    # Write to TSV using KGX sink
    logger.info(f"Writing to {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Collect all property names from the graph
    node_properties = set()
    for _, node_data in graph.nodes():
        node_properties.update(node_data.keys())
    node_properties.add("id")  # Always include id

    edge_properties = set()
    for _, _, edge_data in graph.edges():
        edge_properties.update(edge_data.keys())
    edge_properties.update(["subject", "object"])  # Always include subject/object

    transformer = Transformer()
    sink = TsvSink(
        owner=transformer,
        filename=str(output_path),
        format="tsv",
        node_properties=list(node_properties),
        edge_properties=list(edge_properties),
    )

    # Write all nodes
    for node_id, node_data in graph.nodes():
        # Clean up None values
        clean_data = {k: v for k, v in node_data.items() if v is not None}
        clean_data["id"] = node_id
        sink.write_node(clean_data)

    # Write all edges
    for subject, obj, edge_data in graph.edges():
        clean_data = {k: v for k, v in edge_data.items() if v is not None}
        clean_data["subject"] = subject
        clean_data["object"] = obj
        sink.write_edge(clean_data)

    sink.finalize()

    return counts


@click.command()
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=OUTPUT_DIR / "mediadive",
    help="Output base path",
)
@click.option(
    "--mongodb-uri",
    default="mongodb://localhost:27017",
    help="MongoDB connection URI",
)
def main(output: Path, mongodb_uri: str) -> None:
    """Export MediaDive data to KGX format."""
    click.echo("=" * 60)
    click.echo("Export MediaDive to KGX")
    click.echo("=" * 60)

    counts = export_mediadive(mongodb_uri, output)

    click.echo()
    click.echo("Summary:")
    click.echo(f"  Media:       {counts['media']:,}")
    click.echo(f"  Strains:     {counts['strains']:,}")
    click.echo(f"  Ingredients: {counts['ingredients']:,}")
    click.echo(f"  Solutions:   {counts['solutions']:,}")
    click.echo(
        f"  Total nodes: {sum([counts['media'], counts['strains'], counts['ingredients'], counts['solutions']]):,}"
    )
    click.echo()
    click.echo(f"  grows_in edges:  {counts['grows_in_edges']:,}")
    click.echo(f"  contains edges:  {counts['contains_edges']:,}")
    click.echo(f"  Total edges:     {counts['grows_in_edges'] + counts['contains_edges']:,}")
    click.echo()
    click.echo(f"Output: {output}_nodes.tsv, {output}_edges.tsv")


if __name__ == "__main__":
    main()
