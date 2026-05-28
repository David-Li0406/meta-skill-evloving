#!/usr/bin/env python3
"""Build a ChromaDB collection for NCBITaxon embeddings.

Extracts NCBITaxon embeddings from the OLS embeddings database and creates
a ChromaDB collection for efficient semantic search of taxonomic terms.

Usage:
    uv run python -m cmm_ai_automation.scripts.build_ncbitaxon_chromadb

Options:
    --source-db PATH      Source SQLite embeddings database
    --chroma-path PATH    Output ChromaDB directory
    --collection-name     ChromaDB collection name
    --dry-run            Show stats without creating database
"""

import argparse
import json
import logging
import sqlite3
from pathlib import Path

import chromadb
from chromadb.config import Settings
from tqdm import tqdm  # type: ignore[import-untyped]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_SOURCE_DB = "/home/mark/work/large/ontologies/embeddings.db"
DEFAULT_CHROMA_PATH = "./data/chroma_ncbitaxon"
DEFAULT_COLLECTION_NAME = "ncbitaxon_embeddings"
BATCH_SIZE = 5000


def get_ncbitaxon_count(cursor: sqlite3.Cursor) -> int:
    """Get count of NCBITaxon embeddings."""
    cursor.execute("SELECT COUNT(*) FROM embeddings WHERE ontologyId = 'ncbitaxon'")
    result = cursor.fetchone()
    count: int = int(result[0]) if result else 0
    return count


def build_chromadb(
    source_db: str,
    chroma_path: str,
    collection_name: str,
    dry_run: bool = False,
) -> None:
    """Build ChromaDB collection from NCBITaxon embeddings.

    Args:
        source_db: Path to source SQLite embeddings database
        chroma_path: Output ChromaDB directory
        collection_name: Name for the ChromaDB collection
        dry_run: If True, show stats without creating database
    """
    logger.info(f"Connecting to source: {source_db}")
    conn = sqlite3.connect(source_db)
    cursor = conn.cursor()

    # Get count
    total_count = get_ncbitaxon_count(cursor)
    logger.info(f"Found {total_count:,} NCBITaxon embeddings")

    if dry_run:
        logger.info("[DRY RUN] Not creating ChromaDB.")
        conn.close()
        return

    # Create output directory
    chroma_dir = Path(chroma_path)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    # Create ChromaDB
    logger.info(f"Creating ChromaDB at: {chroma_path}")
    client = chromadb.PersistentClient(
        path=chroma_path,
        settings=Settings(anonymized_telemetry=False),
    )

    # Delete existing collection if present
    try:
        client.delete_collection(name=collection_name)
        logger.info(f"Deleted existing collection '{collection_name}'")
    except Exception:
        pass  # Collection doesn't exist, that's fine

    collection = client.create_collection(
        name=collection_name,
        metadata={
            "description": f"NCBITaxon embeddings ({total_count:,} terms)",
            "source": "OLS embeddings database",
        },
    )

    # Query NCBITaxon embeddings
    logger.info(f"Migrating {total_count:,} embeddings...")
    cursor.execute(
        """
        SELECT ontologyId, iri, document, embeddings
        FROM embeddings
        WHERE ontologyId = 'ncbitaxon'
        """
    )

    batch_ids: list[str] = []
    batch_embeddings: list[list[float]] = []
    batch_documents: list[str] = []
    batch_metadatas: list[dict[str, str]] = []

    with tqdm(total=total_count, desc="Migrating") as pbar:
        for row in cursor:
            ontology_id, iri, document, emb_str = row

            try:
                emb_data = json.loads(emb_str)
                # Handle nested format: {"object":"embedding","embedding":[...]}
                if isinstance(emb_data, dict) and "embedding" in emb_data:
                    embedding = emb_data["embedding"]
                else:
                    embedding = emb_data

                # Create unique ID
                doc_id = f"{ontology_id}_{iri}".replace("/", "_").replace(":", "_")

                batch_ids.append(doc_id)
                batch_embeddings.append(embedding)
                batch_documents.append(document)
                batch_metadatas.append({"ontologyId": ontology_id, "iri": iri})

                if len(batch_ids) >= BATCH_SIZE:
                    collection.add(
                        ids=batch_ids,
                        embeddings=batch_embeddings,  # type: ignore[arg-type]
                        documents=batch_documents,
                        metadatas=batch_metadatas,  # type: ignore[arg-type]
                    )
                    pbar.update(len(batch_ids))
                    batch_ids = []
                    batch_embeddings = []
                    batch_documents = []
                    batch_metadatas = []

            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Error processing {ontology_id} {iri}: {e}")
                continue

        # Add remaining batch
        if batch_ids:
            collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,  # type: ignore[arg-type]
                documents=batch_documents,
                metadatas=batch_metadatas,  # type: ignore[arg-type]
            )
            pbar.update(len(batch_ids))

    conn.close()

    # Verify
    final_count = collection.count()
    logger.info("Migration complete!")
    logger.info(f"  Final count: {final_count:,}")
    logger.info(f"  Expected: {total_count:,}")
    logger.info(f"  Match: {'Yes' if final_count == total_count else 'No'}")


def main() -> None:
    """Build NCBITaxon ChromaDB collection."""
    parser = argparse.ArgumentParser(description="Build ChromaDB collection for NCBITaxon embeddings")
    parser.add_argument(
        "--source-db",
        default=DEFAULT_SOURCE_DB,
        help="Source SQLite embeddings database",
    )
    parser.add_argument(
        "--chroma-path",
        default=DEFAULT_CHROMA_PATH,
        help="Output ChromaDB directory",
    )
    parser.add_argument(
        "--collection-name",
        default=DEFAULT_COLLECTION_NAME,
        help="ChromaDB collection name",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show stats without creating database",
    )
    args = parser.parse_args()

    build_chromadb(
        source_db=args.source_db,
        chroma_path=args.chroma_path,
        collection_name=args.collection_name,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
