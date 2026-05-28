#!/usr/bin/env python3
"""Index BacDive media compositions into ChromaDB for semantic search.

Creates embeddings of media name + composition text for fuzzy matching
against ungrounded media from the growth_media sheet.

Usage:
    uv run python -m cmm_ai_automation.scripts.index_bacdive_media_compositions
    uv run python -m cmm_ai_automation.scripts.index_bacdive_media_compositions --search "PIPES buffered methylotroph minimal medium"
"""

import csv
import logging
from pathlib import Path

import chromadb
import click

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

CHROMA_PATH = "data/chroma_bacdive_media"
BACDIVE_TSV = "data/bacdive_strain_medium_edges.tsv"

# Ungrounded media from growth_media sheet (from media_grounding_analysis.yaml)
UNGROUNDED_MEDIA = {
    "MPYG": {
        "name": "MPYG medium (Methanol-Peptone-Yeast extract-Glucose)",
        "ingredients": [
            "Methanol",
            "Peptone",
            "Yeast extract",
            "Glucose",
            "Dipotassium phosphate",
            "Agar",
        ],
    },
    "MP": {
        "name": "MP medium (PIPES-buffered methylotroph minimal medium)",
        "ingredients": [
            "PIPES buffer (30 mM)",
            "Dipotassium phosphate trihydrate",
            "Sodium phosphate monobasic",
            "Magnesium chloride hexahydrate",
            "Ammonium sulfate",
            "Calcium chloride dihydrate",
            "Trace elements (Zn, Mn, Fe, Mo, Cu, Co, W)",
            "Disodium succinate hexahydrate",
        ],
    },
    "MP-Methanol": {
        "name": "MP medium with methanol carbon source",
        "ingredients": [
            "Methanol",
            "PIPES buffer (30 mM)",
            "Dipotassium phosphate trihydrate",
            "Sodium phosphate monobasic",
            "Magnesium chloride hexahydrate",
            "Ammonium sulfate",
            "Calcium chloride dihydrate",
            "Trace elements",
        ],
    },
    "Hypho-Methanol": {
        "name": "Hypho medium with methanol",
        "ingredients": [
            "Methanol",
            "Dipotassium phosphate",
            "Sodium phosphate",
            "Magnesium sulfate",
            "Ammonium sulfate",
            "Iron(II) sulfate heptahydrate",
            "Disodium EDTA",
            "Trace elements (Ca, Mn, Mo, Cu, Co, Zn)",
        ],
    },
}


def load_unique_media(tsv_path: str) -> list[dict]:
    """Load unique media from BacDive TSV, dedupe by (medium_id, composition).

    This captures media variants (same ID but different compositions due to
    strain-specific modifications). Drops all strain attributes and growth info.

    Returns list of {medium_id, name, composition, link}.
    """
    seen = set()  # (medium_id, composition) pairs
    media = []
    tsv_file = Path(tsv_path)

    if not tsv_file.exists():
        logger.error(f"TSV file not found: {tsv_path}")
        return media

    with tsv_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            medium_id = row.get("medium_id", "").strip()
            if not medium_id:
                continue

            name = row.get("medium_name", "").strip()
            composition = row.get("composition", "").strip()
            link = row.get("medium_link", "").strip()

            # Dedupe by (medium_id, composition) to capture variants
            key = (medium_id, composition)
            if key in seen:
                continue
            seen.add(key)

            if name or composition:
                media.append(
                    {
                        "medium_id": medium_id,
                        "name": name,
                        "composition": composition,
                        "link": link,
                    }
                )

    return media


def create_searchable_text(name: str, composition: str) -> str:
    """Create searchable text from media name and composition."""
    parts = []

    if name:
        parts.append(f"Medium: {name}")

    if composition:
        # Unescape newlines in composition
        comp_text = composition.replace("\\n", "\n")
        parts.append(f"Composition:\n{comp_text}")

    return "\n".join(parts)


def index_media(chroma_client, media: list[dict], clear: bool = False) -> int:
    """Index media into ChromaDB."""
    collection_name = "bacdive_media_compositions"

    if clear:
        try:
            chroma_client.delete_collection(collection_name)
            logger.info(f"Cleared existing collection '{collection_name}'")
        except Exception:
            # Collection may not exist yet; proceed with indexing
            pass

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "BacDive media compositions for semantic search"},
    )

    batch_ids = []
    batch_docs = []
    batch_metas = []
    batch_size = 500
    indexed = 0

    for i, data in enumerate(media):
        medium_id = data["medium_id"]
        searchable_text = create_searchable_text(data["name"], data["composition"])
        if not searchable_text.strip():
            continue

        # Use index to make IDs unique (same medium_id can have variants)
        batch_ids.append(f"BacDive_Medium_{medium_id}_{i}")
        batch_docs.append(searchable_text)
        batch_metas.append(
            {
                "mediadive_id": medium_id,
                "name": data["name"],
                "link": data["link"],
                "is_variant": "strain-specific" in data["composition"].lower(),
            }
        )
        indexed += 1

        if len(batch_ids) >= batch_size:
            collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
            batch_ids, batch_docs, batch_metas = [], [], []

    # Final batch
    if batch_ids:
        collection.upsert(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)

    logger.info(f"Indexed {indexed} unique media (including variants)")
    logger.info(f"Collection count: {collection.count()}")
    return indexed


def search_ungrounded_media(chroma_client, n_results: int = 5) -> dict:
    """Search ungrounded media against indexed BacDive compositions."""
    collection = chroma_client.get_collection("bacdive_media_compositions")
    results = {}

    for media_id, data in UNGROUNDED_MEDIA.items():
        # Create query text from name + ingredients
        ingredients_text = ", ".join(data["ingredients"])
        query = f"{data['name']}\nIngredients: {ingredients_text}"

        logger.info(f"\n--- Searching for: {media_id} ---")
        logger.info(f"Query: {data['name']}")

        search_results = collection.query(query_texts=[query], n_results=n_results)

        results[media_id] = []
        for i, (_doc_id, dist, meta) in enumerate(
            zip(
                search_results["ids"][0],
                search_results["distances"][0],
                search_results["metadatas"][0],
                strict=False,
            )
        ):
            result = {
                "rank": i + 1,
                "mediadive_id": meta.get("mediadive_id"),
                "name": meta.get("name"),
                "distance": dist,
                "link": meta.get("link"),
            }
            results[media_id].append(result)
            logger.info(f"  {i + 1}. [{meta.get('mediadive_id')}] {meta.get('name')[:60]}... (dist: {dist:.3f})")

    return results


def search_custom(chroma_client, query: str, n_results: int = 5) -> None:
    """Search with custom query."""
    collection = chroma_client.get_collection("bacdive_media_compositions")

    logger.info(f"\n--- Custom search: '{query}' ---")
    search_results = collection.query(query_texts=[query], n_results=n_results)

    for i, (_doc_id, dist, meta, doc) in enumerate(
        zip(
            search_results["ids"][0],
            search_results["distances"][0],
            search_results["metadatas"][0],
            search_results["documents"][0],
            strict=False,
        )
    ):
        logger.info(f"\n{i + 1}. [{meta.get('mediadive_id')}] {meta.get('name')}")
        logger.info(f"   Distance: {dist:.3f}")
        logger.info(f"   Link: {meta.get('link')}")
        # Show first few lines of composition
        lines = doc.split("\n")[:5]
        for line in lines:
            logger.info(f"   {line[:80]}")


@click.command()
@click.option("--clear/--no-clear", default=True, help="Clear existing collection")
@click.option("--index/--no-index", default=True, help="Run indexing")
@click.option(
    "--search-ungrounded/--no-search-ungrounded",
    default=False,
    help="Search ungrounded media from sheet",
)
@click.option("--search", default=None, help="Custom search query")
@click.option("--n-results", default=5, help="Number of results to return")
def main(
    clear: bool,
    index: bool,
    search_ungrounded: bool,
    search: str | None,
    n_results: int,
) -> None:
    """Index BacDive media compositions into ChromaDB."""
    logger.info("=" * 60)
    logger.info("BacDive Media Compositions ChromaDB Indexer")
    logger.info("=" * 60)

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    if index:
        media = load_unique_media(BACDIVE_TSV)
        logger.info(f"Loaded {len(media)} unique media from TSV")
        index_media(chroma_client, media, clear=clear)

    if search_ungrounded:
        search_ungrounded_media(chroma_client, n_results=n_results)

    if search:
        search_custom(chroma_client, search, n_results=n_results)

    logger.info("\nDone!")


if __name__ == "__main__":
    main()
