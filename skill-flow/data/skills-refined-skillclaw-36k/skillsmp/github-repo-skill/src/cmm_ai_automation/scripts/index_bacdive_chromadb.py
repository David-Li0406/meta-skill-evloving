#!/usr/bin/env python3
"""Index BacDive strains into ChromaDB for fuzzy/semantic search.

Creates a searchable index of BacDive strain data that can be queried
using natural language or fuzzy matching for strain names, culture
collection IDs, growth conditions, and more.
"""

import contextlib
import logging
import re

import chromadb
import click
from tqdm import tqdm

from cmm_ai_automation.strains.bacdive import get_bacdive_collection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ChromaDB path
CHROMA_PATH = "data/chroma_bacdive"


def normalize_culture_collection_id(raw_id: str) -> list[str]:
    """Generate multiple variants of a culture collection ID for fuzzy matching.

    Input: "DSM 14760" or "DSM:14760" or "DSM-14760"
    Output: ["DSM 14760", "DSM:14760", "DSM-14760", "DSM14760", "DSMZ 14760"]
    """
    # Extract prefix and number
    match = re.match(r"([A-Za-z]+)[\s:\-_]*(\d+)", raw_id.strip())
    if not match:
        return [raw_id.strip()]

    prefix = match.group(1).upper()
    number = match.group(2)

    variants = [
        f"{prefix} {number}",
        f"{prefix}:{number}",
        f"{prefix}-{number}",
        f"{prefix}{number}",
    ]

    # Add common aliases
    aliases = {
        "DSM": ["DSMZ"],
        "ATCC": [],
        "JCM": [],
        "NBRC": ["IFO"],
        "NCIMB": ["NCIB"],
        "CIP": [],
        "LMG": [],
        "NCTC": [],
        "CCM": [],
        "CECT": [],
    }

    for alias in aliases.get(prefix, []):
        variants.extend(
            [
                f"{alias} {number}",
                f"{alias}:{number}",
                f"{alias}-{number}",
            ]
        )

    return variants


def extract_culture_collection_ids(doc: dict) -> list[str]:
    """Extract all culture collection IDs from a BacDive document."""
    ids = []

    # DSM number from General
    dsm_num = doc.get("General", {}).get("DSM-Number")
    if dsm_num:
        ids.extend(normalize_culture_collection_id(f"DSM {dsm_num}"))

    # Culture collection no. from External links
    cc_no = doc.get("External links", {}).get("culture collection no.", "")
    if cc_no:
        for part in re.split(r"[,;]", cc_no):
            part = part.strip()
            if part:
                ids.extend(normalize_culture_collection_id(part))

    return list(set(ids))


def extract_ncbi_taxon_ids(doc: dict) -> list[int]:
    """Extract all NCBI taxon IDs from a BacDive document."""
    taxon_ids = []

    # From General section
    for item in doc.get("General", {}).get("NCBI tax id", []):
        if isinstance(item, dict) and "NCBI tax id" in item:
            taxon_ids.append(item["NCBI tax id"])

    # From Sequence information
    seq_info = doc.get("Sequence information", {})
    if "16S sequences" in seq_info:
        seq = seq_info["16S sequences"]
        if isinstance(seq, dict) and "NCBI tax ID" in seq:
            taxon_ids.append(seq["NCBI tax ID"])

    for genome in seq_info.get("Genome sequences", []):
        if isinstance(genome, dict) and "NCBI tax ID" in genome:
            taxon_ids.append(genome["NCBI tax ID"])

    return list(set(taxon_ids))


def extract_genome_accessions(doc: dict) -> list[str]:
    """Extract genome accessions from a BacDive document."""
    accessions = []

    for genome in doc.get("Sequence information", {}).get("Genome sequences", []):
        if isinstance(genome, dict):
            acc = genome.get("accession", "")
            if acc and (acc.startswith("GCA_") or acc.startswith("GCF_")):
                accessions.append(acc)
            elif acc and acc.startswith("GCA"):
                # Handle GCA without underscore
                accessions.append(acc)

    return accessions


def extract_synonyms(doc: dict) -> list[str]:
    """Extract taxonomic synonyms from LPSN data."""
    synonyms = []

    lpsn = doc.get("Name and taxonomic classification", {}).get("LPSN", {})
    syn_data = lpsn.get("synonyms")

    if isinstance(syn_data, dict):
        if "synonym" in syn_data:
            synonyms.append(syn_data["synonym"])
    elif isinstance(syn_data, list):
        for item in syn_data:
            if isinstance(item, dict) and "synonym" in item:
                synonyms.append(item["synonym"])

    return synonyms


def flatten_bacdive_document(doc: dict) -> tuple[str, dict]:
    """Flatten a BacDive document into searchable text and metadata.

    Focused on strain identification fields only:
    - TEXTUAL: species, genus, full name, strain designation, synonyms,
               description, strain history, culture collection IDs
    - METADATA: bacdive_id, dsm_number, ncbi_taxon_ids, species, genus,
                type_strain, genome_accessions

    Returns:
        tuple: (searchable_text, metadata_dict)
    """
    parts = []
    metadata = {}

    # === General ===
    general = doc.get("General", {})

    bacdive_id = doc.get("_id") or general.get("BacDive-ID")
    metadata["bacdive_id"] = bacdive_id

    dsm_num = general.get("DSM-Number")
    if dsm_num:
        metadata["dsm_number"] = dsm_num

    description = general.get("description", "")
    if description:
        parts.append(f"Description: {description}")

    # Strain history (contains alternative strain names/sources)
    history = general.get("strain history", {})
    if isinstance(history, dict) and "history" in history:
        parts.append(f"Strain history: {history['history']}")

    # === Name and taxonomic classification ===
    tax = doc.get("Name and taxonomic classification", {})

    species = tax.get("species", "")
    if species:
        parts.append(f"Species: {species}")
        metadata["species"] = species

    genus = tax.get("genus", "")
    if genus:
        parts.append(f"Genus: {genus}")
        metadata["genus"] = genus

    full_name = tax.get("full scientific name", "")
    if full_name:
        # Remove HTML tags
        clean_name = re.sub(r"<[^>]+>", "", full_name)
        parts.append(f"Full name: {clean_name}")

    strain_designation = tax.get("strain designation", "")
    if strain_designation:
        parts.append(f"Strain: {strain_designation}")

    type_strain = tax.get("type strain", "")
    if type_strain:
        metadata["type_strain"] = type_strain == "yes"

    # LPSN data (may have different species name and synonyms)
    lpsn = tax.get("LPSN", {})
    if lpsn:
        lpsn_species = lpsn.get("species", "")
        if lpsn_species and lpsn_species != species:
            parts.append(f"LPSN species: {lpsn_species}")

    # LPSN synonyms
    synonyms = extract_synonyms(doc)
    if synonyms:
        parts.append(f"Synonyms: {' | '.join(synonyms)}")

    # === Culture collection IDs (with normalized variants) ===
    cc_ids = extract_culture_collection_ids(doc)
    if cc_ids:
        parts.append(f"Culture collection IDs: {' | '.join(cc_ids)}")

    # === NCBI Taxon IDs (metadata only) ===
    ncbi_ids = extract_ncbi_taxon_ids(doc)
    if ncbi_ids:
        metadata["ncbi_taxon_ids"] = ",".join(map(str, ncbi_ids))

    # === Genome accessions (metadata only) ===
    genomes = extract_genome_accessions(doc)
    if genomes:
        metadata["genome_accessions"] = ",".join(genomes)

    # Combine all parts into searchable text
    searchable_text = "\n".join(parts)

    return searchable_text, metadata


def index_bacdive_to_chromadb(
    limit: int | None = None,
    batch_size: int = 500,
    clear: bool = False,
    database: str | None = None,
    collection: str | None = None,
) -> None:
    """Index BacDive strains into ChromaDB."""

    # Connect to MongoDB
    db_name = database or "bacdive"
    coll_name = collection or "strains"
    logger.info(f"Connecting to MongoDB ({db_name}.{coll_name})...")
    strains = get_bacdive_collection(database=database, collection=collection)

    if strains is None:
        logger.error("Failed to connect to BacDive MongoDB")
        return

    total_count = strains.count_documents({})
    logger.info(f"Found {total_count:,} strains in BacDive")

    if limit:
        total_count = min(total_count, limit)
        logger.info(f"Limiting to {total_count:,} strains")

    # Connect to ChromaDB
    logger.info(f"Connecting to ChromaDB at {CHROMA_PATH}...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection_name = "bacdive_strains"

    if clear:
        logger.info(f"Clearing existing collection '{collection_name}'...")
        # Collection may not exist yet; suppress exception and proceed
        with contextlib.suppress(Exception):
            chroma_client.delete_collection(collection_name)

    collection = chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"description": "BacDive strain data for fuzzy/semantic search"},
    )

    existing_count = collection.count()
    logger.info(f"Collection '{collection_name}' has {existing_count:,} existing documents")

    # Index documents
    logger.info("Indexing documents...")

    cursor = strains.find({}).limit(limit) if limit else strains.find({})

    batch_ids = []
    batch_documents = []
    batch_metadatas = []

    indexed = 0
    skipped = 0
    errors = 0

    for doc in tqdm(cursor, total=total_count, desc="Indexing"):
        try:
            bacdive_id = doc.get("_id") or doc.get("General", {}).get("BacDive-ID")
            if not bacdive_id:
                skipped += 1
                continue

            doc_id = f"bacdive_{bacdive_id}"

            searchable_text, metadata = flatten_bacdive_document(doc)

            if not searchable_text.strip():
                skipped += 1
                continue

            batch_ids.append(doc_id)
            batch_documents.append(searchable_text)
            batch_metadatas.append(metadata)

            if len(batch_ids) >= batch_size:
                collection.upsert(
                    ids=batch_ids,
                    documents=batch_documents,
                    metadatas=batch_metadatas,
                )
                indexed += len(batch_ids)
                batch_ids = []
                batch_documents = []
                batch_metadatas = []

        except Exception as e:
            logger.error(f"Error processing document {doc.get('_id')}: {e}")
            errors += 1

    # Final batch
    if batch_ids:
        collection.upsert(
            ids=batch_ids,
            documents=batch_documents,
            metadatas=batch_metadatas,
        )
        indexed += len(batch_ids)

    logger.info("\nIndexing complete!")
    logger.info(f"  Indexed: {indexed:,}")
    logger.info(f"  Skipped: {skipped:,}")
    logger.info(f"  Errors: {errors:,}")
    logger.info(f"  Total in collection: {collection.count():,}")


def demo_searches(n_results: int = 5) -> None:
    """Demonstrate search capabilities."""

    logger.info("\n" + "=" * 60)
    logger.info("DEMO: BacDive ChromaDB Search Capabilities")
    logger.info("=" * 60)

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_collection("bacdive_strains")

    queries = [
        # Fuzzy strain name matching
        ("Methylobacterium extorquens", "Fuzzy species name search"),
        ("M. extorquens AM1", "Abbreviated genus + strain"),
        ("Methylorubrum extorquens", "Species name synonym"),
        # Culture collection ID variations
        ("DSM 1337", "Culture collection ID (space)"),
        ("DSM:1337", "Culture collection ID (colon)"),
        ("DSM-1337", "Culture collection ID (hyphen)"),
        ("DSMZ 1337", "Culture collection ID (alias)"),
        ("ATCC 14718", "ATCC collection ID"),
        # Strain designation variations
        ("AM1 methylotroph", "Strain designation in context"),
        ("KT2440", "Well-known strain designation"),
        ("DSM 16371", "Methylobacterium aquaticum type strain"),
        # Typos and partial matches
        ("Methylobacteium", "Typo in genus name"),
        ("Pseudomonas putida", "Common model organism"),
    ]

    for query, description in queries:
        logger.info(f"\n{'─' * 50}")
        logger.info(f"Query: '{query}'")
        logger.info(f"Purpose: {description}")
        logger.info("─" * 50)

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
        )

        for i, (doc_id, distance, metadata) in enumerate(
            zip(
                results["ids"][0],
                results["distances"][0],
                results["metadatas"][0],
                strict=False,
            )
        ):
            species = metadata.get("species", "Unknown")
            strain = metadata.get("strain_designation", "")
            dsm = metadata.get("dsm_number", "")

            logger.info(f"  {i + 1}. {species} {strain}")
            logger.info(f"     BacDive: {doc_id} | DSM: {dsm} | Distance: {distance:.4f}")


@click.command()
@click.option("--limit", type=int, default=None, help="Limit number of documents to index")
@click.option("--batch-size", type=int, default=500, help="Batch size for indexing")
@click.option("--clear/--no-clear", default=False, help="Clear existing collection before indexing")
@click.option("--demo/--no-demo", default=False, help="Run demo searches after indexing")
@click.option("--demo-only", is_flag=True, help="Only run demo searches (skip indexing)")
@click.option("--database", type=str, default=None, help="MongoDB database name (default: bacdive)")
@click.option("--collection", type=str, default=None, help="MongoDB collection name (default: strains)")
def main(
    limit: int | None,
    batch_size: int,
    clear: bool,
    demo: bool,
    demo_only: bool,
    database: str | None,
    collection: str | None,
) -> None:
    """Index BacDive strains into ChromaDB for semantic search."""

    if not demo_only:
        index_bacdive_to_chromadb(
            limit=limit,
            batch_size=batch_size,
            clear=clear,
            database=database,
            collection=collection,
        )

    if demo or demo_only:
        demo_searches()


if __name__ == "__main__":
    main()
