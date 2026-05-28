"""Load KGX TSV files into Neo4j with proper labels and relationship types."""

import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NODES_FILE = Path("output/kgx/mediadive_nodes.tsv")
EDGES_FILE = Path("output/kgx/mediadive_edges.tsv")

# Map categories to Neo4j labels
CATEGORY_TO_LABEL = {
    "METPO:1004005": "GrowthMedium",
    "biolink:OrganismTaxon": "Strain",
    "biolink:ChemicalEntity": "Ingredient",
    "biolink:ChemicalMixture": "Solution",
}

# Map predicates to Neo4j relationship types
PREDICATE_TO_TYPE = {
    "RO:0001019": "CONTAINS",
    "METPO:2000517": "GROWS_IN",
}


def category_to_label(category: str | None) -> str:
    """Convert biolink/ontology category to Neo4j label."""
    if not category or not category.strip():
        return "Unknown"
    return CATEGORY_TO_LABEL.get(category, category.split(":")[-1] if ":" in category else category)


def predicate_to_type(predicate: str) -> str:
    """Convert predicate to Neo4j relationship type."""
    return PREDICATE_TO_TYPE.get(predicate, predicate.split(":")[-1].upper())


def main() -> None:
    """Load KGX files into Neo4j."""
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "neo4j")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    # Load nodes
    print(f"Loading nodes from {NODES_FILE}...")
    with NODES_FILE.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        nodes = list(reader)

    with driver.session() as session:
        # Drop old index if exists, then create constraint
        session.run("DROP INDEX node_id IF EXISTS")
        session.run("CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n:Node) REQUIRE n.id IS UNIQUE")

        for i, row in enumerate(nodes):
            label = category_to_label(row.get("category", "Node"))
            props = {k: v for k, v in row.items() if v}  # Skip empty values

            # Create node with dynamic label
            session.run(f"CREATE (n:Node:{label} $props)", props=props)
            if (i + 1) % 1000 == 0:
                print(f"  Loaded {i + 1:,} / {len(nodes):,} nodes")

        print(f"  Loaded {len(nodes):,} nodes")

    # Load edges
    print(f"Loading edges from {EDGES_FILE}...")
    with EDGES_FILE.open(newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        edges = list(reader)

    loaded = 0
    skipped = 0
    with driver.session() as session:
        for i, row in enumerate(edges):
            rel_type = predicate_to_type(row.get("predicate", "RELATED_TO"))
            props = {k: v for k, v in row.items() if v and k not in ("subject", "object", "predicate")}

            result = session.run(
                f"""
                MATCH (s:Node {{id: $subject}}), (o:Node {{id: $object}})
                CREATE (s)-[r:{rel_type} $props]->(o)
                RETURN count(r) as created
                """,
                subject=row["subject"],
                object=row["object"],
                props=props,
            )
            created = result.single()["created"]
            if created:
                loaded += 1
            else:
                skipped += 1

            if (i + 1) % 10000 == 0:
                print(f"  Processed {i + 1:,} / {len(edges):,} edges ({loaded:,} loaded, {skipped:,} skipped)")

        print(f"  Loaded {loaded:,} edges, skipped {skipped:,} (missing nodes)")

    driver.close()
    print("✓ Upload complete")


if __name__ == "__main__":
    main()
