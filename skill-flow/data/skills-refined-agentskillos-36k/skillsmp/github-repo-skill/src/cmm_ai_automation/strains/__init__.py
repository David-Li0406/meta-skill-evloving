"""Strain data processing subpackage.

This subpackage provides modular components for processing strain data.

Submodules:
    - models: Domain models (StrainRecord)
    - parsing: TSV parsing for strain data
    - inference: Taxonomic rank inference
    - consolidation: Deduplication and merging
    - ncbi: NCBI Entrez API functions
    - bacdive: BacDive MongoDB lookup functions
    - enrichment: Enrichment pipeline orchestration
    - export: KGX node/edge generation
"""

from cmm_ai_automation.strains.bacdive import (
    enrich_strain_from_bacdive,
    enrich_strains_with_bacdive,
    get_bacdive_collection,
    search_species_with_synonyms,
)
from cmm_ai_automation.strains.consolidation import (
    consolidate_strains,
    deduplicate_by_canonical_id,
    merge_records,
)
from cmm_ai_automation.strains.culture_collection import (
    batch_search_culture_collections,
    parse_culture_collection_id,
    reconcile_culture_collection_id,
    search_culture_collection,
)
from cmm_ai_automation.strains.enrichment import (
    EnrichmentStats,
    IterativeEnrichmentPipeline,
    enrich_strains_with_ncbi,
    generate_query_variants,
)
from cmm_ai_automation.strains.export import (
    export_kgx_edges,
    export_kgx_nodes,
    export_taxrank_nodes,
)
from cmm_ai_automation.strains.inference import (
    infer_species_from_bacdive,
    infer_species_from_self,
    infer_taxonomic_rank,
    run_inference_pipeline,
)
from cmm_ai_automation.strains.models import StrainRecord
from cmm_ai_automation.strains.parsing import (
    parse_all_strain_sources,
    parse_growth_preferences_tsv,
    parse_strains_tsv,
    parse_taxa_and_genomes_tsv,
)

__all__ = [
    "EnrichmentStats",
    "IterativeEnrichmentPipeline",
    "StrainRecord",
    "batch_search_culture_collections",
    "consolidate_strains",
    "deduplicate_by_canonical_id",
    "enrich_strain_from_bacdive",
    "enrich_strains_with_bacdive",
    "enrich_strains_with_ncbi",
    "export_kgx_edges",
    "export_kgx_nodes",
    "export_taxrank_nodes",
    "generate_query_variants",
    "get_bacdive_collection",
    "infer_species_from_bacdive",
    "infer_species_from_self",
    "infer_taxonomic_rank",
    "merge_records",
    "parse_all_strain_sources",
    "parse_culture_collection_id",
    "parse_growth_preferences_tsv",
    "parse_strains_tsv",
    "parse_taxa_and_genomes_tsv",
    "reconcile_culture_collection_id",
    "run_inference_pipeline",
    "search_culture_collection",
    "search_species_with_synonyms",
]
