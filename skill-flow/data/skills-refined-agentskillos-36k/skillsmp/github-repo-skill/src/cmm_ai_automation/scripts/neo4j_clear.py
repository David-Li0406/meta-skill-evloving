"""Clear all nodes and edges from Neo4j database."""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()


def main() -> None:
    """Clear all nodes and edges from Neo4j database."""
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "neo4j")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        result = session.run("MATCH (n) DETACH DELETE n")
        summary = result.consume()
        print(
            f"Deleted {summary.counters.nodes_deleted} nodes and {summary.counters.relationships_deleted} relationships"
        )
    driver.close()


if __name__ == "__main__":
    main()
