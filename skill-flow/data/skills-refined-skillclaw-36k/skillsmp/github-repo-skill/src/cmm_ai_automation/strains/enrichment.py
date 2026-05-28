"""Enrichment pipeline orchestration for strain records.

This module provides the iterative enrichment pipeline that coordinates
BacDive and NCBI enrichment across multiple rounds.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path  # noqa: TC003 - Path is used at runtime
from typing import TYPE_CHECKING, Any

import click

if TYPE_CHECKING:
    from pymongo.collection import Collection

    from cmm_ai_automation.strains.models import StrainRecord

logger = logging.getLogger(__name__)


def generate_query_variants(
    scientific_name: str | None,
    strain_designation: str | None,
    culture_collection_ids: list[str],
) -> list[str]:
    """Generate multiple query variants for fuzzy matching.

    Args:
        scientific_name: Binomial name (e.g., "Methylobacterium aquaticum")
        strain_designation: Strain name (e.g., "DSM 16371", "AM1")
        culture_collection_ids: List of culture collection IDs

    Returns:
        List of query strings to try for matching
    """
    queries = []

    # Full name + strain designation
    if scientific_name and strain_designation:
        queries.append(f"{scientific_name} {strain_designation}")

    # Scientific name only
    if scientific_name:
        queries.append(scientific_name)

    # Strain designation only
    if strain_designation:
        queries.append(strain_designation)

    # Culture collection ID variants
    for cc_id in culture_collection_ids:
        if ":" in cc_id:
            prefix, local_id = cc_id.split(":", 1)
            # Various formats
            queries.extend(
                [
                    f"{prefix} {local_id}",  # DSM 16371
                    f"{prefix}-{local_id}",  # DSM-16371
                    f"{prefix}{local_id}",  # DSM16371
                ]
            )
            # With scientific name
            if scientific_name:
                queries.append(f"{scientific_name} {prefix} {local_id}")

    # Deduplicate while preserving order
    seen_queries: set[str] = set()
    unique_queries: list[str] = []
    for q in queries:
        if q and q not in seen_queries:
            seen_queries.add(q)
            unique_queries.append(q)
    return unique_queries


def enrich_strains_with_ncbi(records: list[StrainRecord]) -> tuple[int, int, int, int, int]:
    """Enrich strain records with NCBI Taxonomy data using batch API.

    Fetches synonyms, lineage (species/parent taxon), rank, and external linkouts
    from NCBI Entrez for strains that have NCBITaxon IDs.

    Args:
        records: List of strain records to enrich

    Returns:
        Tuple of (synonym_enriched, species_enriched, parent_enriched, linkout_enriched, total_with_taxon)
    """
    from cmm_ai_automation.strains.ncbi import (
        extract_xrefs_from_linkouts,
        fetch_ncbi_batch,
        fetch_ncbi_linkouts,
    )

    # Collect taxon IDs for batch fetch
    taxon_id_to_records: dict[str, list[StrainRecord]] = {}
    for record in records:
        if record.ncbi_taxon_id:
            taxid = record.ncbi_taxon_id.replace("NCBITaxon:", "")
            if taxid not in taxon_id_to_records:
                taxon_id_to_records[taxid] = []
            taxon_id_to_records[taxid].append(record)

    taxon_ids = list(taxon_id_to_records.keys())
    with_taxon = len(taxon_ids)

    if not taxon_ids:
        return 0, 0, 0, 0, 0

    # Batch fetch taxonomy data
    logger.info(f"Fetching NCBI taxonomy data for {len(taxon_ids)} taxa in batches...")
    ncbi_data_map = fetch_ncbi_batch(taxon_ids)

    # Batch fetch linkouts
    logger.info(f"Fetching NCBI linkouts for {len(taxon_ids)} taxa...")
    linkouts_map = fetch_ncbi_linkouts(taxon_ids)

    # Apply enrichment
    synonym_enriched = 0
    species_enriched = 0
    parent_enriched = 0
    linkout_enriched = 0

    for taxid, record_list in taxon_id_to_records.items():
        ncbi_data = ncbi_data_map.get(taxid)
        linkouts = linkouts_map.get(taxid, [])

        for record in record_list:
            if ncbi_data:
                # Set taxonomic rank - NCBI is authoritative, always overwrite
                ncbi_rank = ncbi_data.get("rank", "")
                if isinstance(ncbi_rank, str) and ncbi_rank:
                    record.has_taxonomic_rank = ncbi_rank

                # Set species_taxon_id from lineage
                if not record.species_taxon_id and ncbi_data["species_taxon_id"]:
                    record.species_taxon_id = ncbi_data["species_taxon_id"]
                    species_enriched += 1

                # Set parent_taxon_id from lineage
                if not record.parent_taxon_id and ncbi_data["parent_taxon_id"]:
                    record.parent_taxon_id = ncbi_data["parent_taxon_id"]
                    parent_enriched += 1

                # Add synonyms
                added_syn = False
                for synonym in ncbi_data["synonyms"]:
                    if synonym not in record.synonyms:
                        record.synonyms.append(synonym)
                        added_syn = True
                for equiv in ncbi_data["equivalent_names"]:
                    if equiv not in record.synonyms:
                        record.synonyms.append(equiv)
                        added_syn = True
                for misspelling in ncbi_data["misspellings"]:
                    if misspelling not in record.synonyms:
                        record.synonyms.append(misspelling)
                        added_syn = True
                for includes in ncbi_data["includes"]:
                    if includes not in record.synonyms:
                        record.synonyms.append(includes)
                        added_syn = True
                if added_syn:
                    synonym_enriched += 1

            # Extract xrefs from linkouts
            if linkouts:
                xrefs = extract_xrefs_from_linkouts(linkouts)
                added_xref = False
                for xref in xrefs:
                    if xref not in record.xrefs:
                        record.xrefs.append(xref)
                        added_xref = True
                    # Also extract BacDive ID if not set
                    if xref.startswith("bacdive:") and not record.bacdive_id:
                        record.bacdive_id = xref.replace("bacdive:", "")
                if added_xref:
                    linkout_enriched += 1

    return synonym_enriched, species_enriched, parent_enriched, linkout_enriched, with_taxon


@dataclass
class EnrichmentStats:
    """Statistics from an enrichment round."""

    records_processed: int = 0
    records_enriched: int = 0
    new_ncbi_ids: int = 0
    new_bacdive_ids: int = 0
    new_species_ids: int = 0
    new_parent_ids: int = 0
    new_synonyms: int = 0
    new_xrefs: int = 0

    def __str__(self) -> str:
        return (
            f"processed={self.records_processed}, enriched={self.records_enriched}, "
            f"ncbi+={self.new_ncbi_ids}, bacdive+={self.new_bacdive_ids}"
        )


@dataclass
class IterativeEnrichmentPipeline:
    """Iterative enrichment pipeline for strain records.

    Runs multiple rounds of enrichment, using results from each round
    to discover new data sources for subsequent rounds.

    Workflow:
        Round 1: Parse input sheets, consolidate duplicates
        Round 2: BacDive enrichment (first pass) - match by name
        Round 3: NCBI enrichment - get lineage, synonyms, external linkouts
        Round 4: BacDive enrichment (second pass) - use NCBI linkouts
        Round 5: PydanticAI reconciliation for ambiguous matches (optional)
        Round 6: Final consolidation and export
    """

    strains_tsv: Path
    taxa_genomes_tsv: Path
    growth_prefs_tsv: Path
    bacdive_collection: Collection[dict[str, Any]] | None = None
    use_pydanticai: bool = False
    skip_ncbi: bool = False
    verbose: bool = False

    records: list[StrainRecord] = field(default_factory=list)
    round_stats: list[tuple[str, EnrichmentStats]] = field(default_factory=list)
    _discovered_bacdive_ids: set[str] = field(default_factory=set)

    def run(self) -> list[StrainRecord]:
        """Execute the full iterative enrichment pipeline.

        Returns:
            List of fully enriched StrainRecord objects
        """
        click.echo("=== Iterative Strain Enrichment Pipeline ===\n")

        # Round 1: Parse and consolidate
        self._round_1_parse()

        # Round 2: BacDive first pass
        if self.bacdive_collection is not None:
            self._round_2_bacdive_first_pass()

        # Round 3: NCBI enrichment with linkouts
        if not self.skip_ncbi:
            self._round_3_ncbi_enrichment()
        else:
            click.echo("Round 3: NCBI enrichment skipped (--no-ncbi)\n")

        # Round 4: BacDive second pass using NCBI linkouts
        if self.bacdive_collection is not None and not self.skip_ncbi:
            self._round_4_bacdive_from_linkouts()

        # Round 5: PydanticAI reconciliation (optional)
        if self.use_pydanticai:
            self._round_5_pydanticai_reconciliation()

        # Round 6: Final inference and deduplication
        self._round_6_finalize()

        # Print summary
        self._print_pipeline_summary()

        return self.records

    def _round_1_parse(self) -> None:
        """Round 1: Parse input sheets and consolidate duplicates."""
        from cmm_ai_automation.strains.consolidation import consolidate_strains
        from cmm_ai_automation.strains.parsing import (
            parse_growth_preferences_tsv,
            parse_strains_tsv,
            parse_taxa_and_genomes_tsv,
        )

        click.echo("Round 1: Parsing input sheets")
        stats = EnrichmentStats()

        all_records: list[StrainRecord] = []

        records = parse_strains_tsv(self.strains_tsv)
        all_records.extend(records)
        click.echo(f"  - {self.strains_tsv.name}: {len(records)} records")

        records = parse_taxa_and_genomes_tsv(self.taxa_genomes_tsv)
        all_records.extend(records)
        click.echo(f"  - {self.taxa_genomes_tsv.name}: {len(records)} records")

        records = parse_growth_preferences_tsv(self.growth_prefs_tsv)
        all_records.extend(records)
        click.echo(f"  - {self.growth_prefs_tsv.name}: {len(records)} records")

        stats.records_processed = len(all_records)

        # Consolidate
        self.records = consolidate_strains(all_records)
        stats.records_enriched = len(self.records)

        click.echo(f"  Consolidated: {stats.records_processed} -> {len(self.records)} unique strains\n")
        self.round_stats.append(("Parse & Consolidate", stats))

    def _round_2_bacdive_first_pass(self) -> None:
        """Round 2: BacDive enrichment by name matching."""
        from cmm_ai_automation.strains.bacdive import enrich_strains_with_bacdive

        if self.bacdive_collection is None:
            raise RuntimeError("BacDive collection required for Round 2")
        click.echo("Round 2: BacDive enrichment (first pass - name matching)")
        stats = EnrichmentStats()

        before_bacdive = sum(1 for r in self.records if r.bacdive_id)
        before_ncbi = sum(1 for r in self.records if r.ncbi_taxon_id)

        enriched, total = enrich_strains_with_bacdive(self.records, self.bacdive_collection)

        stats.records_processed = total
        stats.records_enriched = enriched
        stats.new_bacdive_ids = sum(1 for r in self.records if r.bacdive_id) - before_bacdive
        stats.new_ncbi_ids = sum(1 for r in self.records if r.ncbi_taxon_id) - before_ncbi

        # Track discovered BacDive IDs
        for r in self.records:
            if r.bacdive_id:
                self._discovered_bacdive_ids.add(r.bacdive_id)

        click.echo(f"  Enriched: {enriched}/{total} strains")
        click.echo(f"  New BacDive IDs: +{stats.new_bacdive_ids}")
        click.echo(f"  New NCBI IDs: +{stats.new_ncbi_ids}\n")
        self.round_stats.append(("BacDive (name match)", stats))

    def _round_3_ncbi_enrichment(self) -> None:
        """Round 3: NCBI batch enrichment with linkouts."""
        click.echo("Round 3: NCBI Taxonomy enrichment (batch mode)")
        stats = EnrichmentStats()

        before_species = sum(1 for r in self.records if r.species_taxon_id)
        before_parent = sum(1 for r in self.records if r.parent_taxon_id)
        before_synonyms = sum(len(r.synonyms) for r in self.records)
        before_xrefs = sum(len(r.xrefs) for r in self.records)

        syn, species, parent, linkout, total = enrich_strains_with_ncbi(self.records)

        stats.records_processed = total
        stats.records_enriched = syn + species + parent + linkout
        stats.new_species_ids = sum(1 for r in self.records if r.species_taxon_id) - before_species
        stats.new_parent_ids = sum(1 for r in self.records if r.parent_taxon_id) - before_parent
        stats.new_synonyms = sum(len(r.synonyms) for r in self.records) - before_synonyms
        stats.new_xrefs = sum(len(r.xrefs) for r in self.records) - before_xrefs

        # Track any new BacDive IDs discovered via linkouts
        new_bacdive_from_linkouts = 0
        for r in self.records:
            if r.bacdive_id and r.bacdive_id not in self._discovered_bacdive_ids:
                self._discovered_bacdive_ids.add(r.bacdive_id)
                new_bacdive_from_linkouts += 1
        stats.new_bacdive_ids = new_bacdive_from_linkouts

        click.echo(f"  Processed: {total} taxa")
        click.echo(f"  New species_taxon_id: +{stats.new_species_ids}")
        click.echo(f"  New parent_taxon_id: +{stats.new_parent_ids}")
        click.echo(f"  New synonyms: +{stats.new_synonyms}")
        click.echo(f"  New xrefs (from linkouts): +{stats.new_xrefs}")
        click.echo(f"  New BacDive IDs (from linkouts): +{stats.new_bacdive_ids}\n")
        self.round_stats.append(("NCBI Taxonomy", stats))

    def _round_4_bacdive_from_linkouts(self) -> None:
        """Round 4: BacDive second pass using IDs from NCBI linkouts."""
        click.echo("Round 4: BacDive enrichment (second pass - from NCBI linkouts)")
        stats = EnrichmentStats()

        # Find records that got BacDive IDs from linkouts but weren't enriched
        records_needing_enrichment = [
            r
            for r in self.records
            if r.bacdive_id and not r.xrefs  # Has BacDive ID but no xrefs yet
        ]

        if not records_needing_enrichment:
            click.echo("  No new BacDive IDs to enrich\n")
            self.round_stats.append(("BacDive (linkout)", stats))
            return

        before_xrefs = sum(len(r.xrefs) for r in self.records)

        # Enrich these specific records by BacDive ID
        enriched_count = 0
        for record in records_needing_enrichment:
            if self._enrich_single_by_bacdive_id(record):
                enriched_count += 1

        stats.records_processed = len(records_needing_enrichment)
        stats.records_enriched = enriched_count
        stats.new_xrefs = sum(len(r.xrefs) for r in self.records) - before_xrefs

        click.echo(f"  Enriched: {enriched_count}/{len(records_needing_enrichment)} strains")
        click.echo(f"  New xrefs: +{stats.new_xrefs}\n")
        self.round_stats.append(("BacDive (linkout)", stats))

    def _enrich_single_by_bacdive_id(self, record: StrainRecord) -> bool:
        """Enrich a single record by its BacDive ID."""
        if not record.bacdive_id or self.bacdive_collection is None:
            return False

        try:
            bacdive_id = int(record.bacdive_id)
        except ValueError:
            return False

        # Try standard paths for BacDive ID
        doc = self.bacdive_collection.find_one({"General.BacDive-ID": bacdive_id})
        if not doc:
            doc = self.bacdive_collection.find_one({"_id": bacdive_id})

        if not doc:
            return False

        # Extract culture collection IDs
        cc_ids = doc.get("culture_collection_ids", [])
        for cc_id in cc_ids:
            if cc_id not in record.culture_collection_ids:
                record.culture_collection_ids.append(cc_id)
            # Also add as xref (culture collection IDs are already in CURIE-like format)
            if cc_id and cc_id not in record.xrefs:
                record.xrefs.append(cc_id)

        return True

    def _round_5_pydanticai_reconciliation(self) -> None:
        """Round 5: PydanticAI reconciliation for ambiguous matches."""
        click.echo("Round 5: PydanticAI reconciliation")
        stats = EnrichmentStats()

        # Find candidates for reconciliation:
        # - Records without BacDive ID (might have matches we missed)
        # - Records with genus synonymy issues (Sinorhizobium/Ensifer)
        candidates = [r for r in self.records if not r.bacdive_id]

        if not candidates:
            click.echo("  No candidates for LLM reconciliation\n")
            self.round_stats.append(("PydanticAI", stats))
            return

        click.echo(f"  Found {len(candidates)} candidates for reconciliation")
        click.echo("  (PydanticAI reconciliation not yet implemented - see issue #74)\n")

        # TODO: Implement PydanticAI reconciliation
        # 1. For each candidate, search BacDive by scientific name
        # 2. Use StrainReconciler to compare candidates
        # 3. If high-confidence match, add bacdive_id
        # 4. Generate same_as edges for KGX clique merge

        self.round_stats.append(("PydanticAI", stats))

    def _round_6_finalize(self) -> None:
        """Round 6: Final inference and deduplication."""
        from cmm_ai_automation.strains.consolidation import deduplicate_by_canonical_id
        from cmm_ai_automation.strains.inference import (
            infer_species_from_bacdive,
            infer_species_from_self,
            infer_taxonomic_rank,
        )

        click.echo("Round 6: Finalizing")
        stats = EnrichmentStats()

        # Infer taxonomic ranks only for records without NCBI rank
        rank_inferred = infer_taxonomic_rank(self.records)
        click.echo(f"  Ranks inferred (no NCBI data): {rank_inferred}")

        # Infer species from BacDive for strains
        species_bacdive = infer_species_from_bacdive(self.records)
        click.echo(f"  Species from BacDive: {species_bacdive}")

        # Infer species from self for species-level records
        species_self = infer_species_from_self(self.records)
        click.echo(f"  Species from self: {species_self}")

        # Final deduplication
        pre_dedup = len(self.records)
        self.records = deduplicate_by_canonical_id(self.records)

        stats.records_processed = pre_dedup
        stats.records_enriched = len(self.records)

        if len(self.records) < pre_dedup:
            click.echo(f"  Deduplication: {pre_dedup} -> {len(self.records)}")

        click.echo()
        self.round_stats.append(("Finalize", stats))

    def _print_pipeline_summary(self) -> None:
        """Print summary of all enrichment rounds."""
        print_validation_summary(self.records)


def compute_validation_summary(records: list[StrainRecord]) -> dict[str, dict[str, int | float]]:
    """Compute field completeness statistics for validation.

    Args:
        records: List of strain records

    Returns:
        Dictionary with field names and their completeness counts
    """
    total = len(records)
    summary: dict[str, dict[str, int | float]] = {}

    # Define fields to check
    fields = [
        ("ncbi_taxon_id", lambda r: bool(r.ncbi_taxon_id)),
        ("species_taxon_id", lambda r: bool(r.species_taxon_id)),
        ("parent_taxon_id", lambda r: bool(r.parent_taxon_id)),
        ("has_taxonomic_rank", lambda r: bool(r.has_taxonomic_rank)),
        ("bacdive_id", lambda r: bool(r.bacdive_id)),
        ("strain_designation", lambda r: bool(r.strain_designation)),
        ("genome_accession", lambda r: bool(r.genome_accession)),
        ("synonyms", lambda r: len(r.synonyms) > 0),
        ("xrefs", lambda r: len(r.xrefs) > 0 or len(r.culture_collection_ids) > 0),
    ]

    for field_name, check_fn in fields:
        present = sum(1 for r in records if check_fn(r))
        summary[field_name] = {
            "present": present,
            "missing": total - present,
            "total": total,
            "percent": round(100 * present / total, 1) if total > 0 else 0,
        }

    return summary


def print_validation_summary(records: list[StrainRecord]) -> None:
    """Print a validation summary showing field completeness.

    Args:
        records: List of strain records
    """
    summary = compute_validation_summary(records)
    total = len(records)

    click.echo("=" * 60)
    click.echo("DATA COMPLETENESS VALIDATION")
    click.echo("=" * 60)
    click.echo(f"Total records: {total}\n")

    click.echo(f"{'Field':<20} {'Present':>8} {'Missing':>8} {'Percent':>8}")
    click.echo("-" * 48)

    for field_name, stats in summary.items():
        pct = stats["percent"]
        status = "OK" if pct == 100 else ("WARN" if pct >= 80 else "LOW")
        click.echo(f"{field_name:<20} {stats['present']:>8} {stats['missing']:>8} {pct:>7.1f}%  [{status}]")

    click.echo("-" * 48)

    # Show records missing critical fields
    missing_ncbi = [r for r in records if not r.ncbi_taxon_id]
    missing_species = [r for r in records if not r.species_taxon_id]
    missing_parent = [r for r in records if not r.parent_taxon_id]

    if missing_ncbi:
        click.echo(f"\nRecords missing ncbi_taxon_id ({len(missing_ncbi)}):")
        for r in missing_ncbi[:5]:
            click.echo(f"  - {r.name or r.strain_designation or 'Unknown'}")
        if len(missing_ncbi) > 5:
            click.echo(f"  ... and {len(missing_ncbi) - 5} more")

    if missing_species:
        click.echo(f"\nRecords missing species_taxon_id ({len(missing_species)}):")
        for r in missing_species[:5]:
            click.echo(f"  - {r.name or r.strain_designation or 'Unknown'} (ncbi: {r.ncbi_taxon_id or 'N/A'})")
        if len(missing_species) > 5:
            click.echo(f"  ... and {len(missing_species) - 5} more")

    if missing_parent:
        click.echo(f"\nRecords missing parent_taxon_id ({len(missing_parent)}):")
        for r in missing_parent[:5]:
            click.echo(f"  - {r.name or r.strain_designation or 'Unknown'} (ncbi: {r.ncbi_taxon_id or 'N/A'})")
        if len(missing_parent) > 5:
            click.echo(f"  ... and {len(missing_parent) - 5} more")

    click.echo("=" * 60 + "\n")
