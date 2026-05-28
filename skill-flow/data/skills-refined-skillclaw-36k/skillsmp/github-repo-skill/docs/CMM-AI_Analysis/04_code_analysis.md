# Chapter 4: Code Analysis

[<- Back to Index](00_index.md) | [Previous: Data Quality Issues](03_data_quality_issues.md) | [Next: API and LLM ->](05_api_and_llm.md)

---

## Automation Files Present

| File | Purpose | Lines |
|------|---------|-------|
| `Makefile` | Main pipeline automation | 975 lines |
| `ai.just` | AI assistant setup (symlinks, GitHub secrets) | 47 lines |

**Note**: `ai.just` only handles AI assistant configuration (creating CLAUDE.md symlink, setting GitHub topics/secrets). It does NOT automate any data pipeline tasks.

---

## Python Script Inventory

**Total: 57 Python files**
- `src/`: 51 files
- `src/kg_analysis/`: 6 files

---

## BROKEN: Makefile Targets with Wrong Paths

**These 7 Makefile targets will FAIL because the scripts are missing the `src/` prefix:**

| Makefile Line | Wrong Path | Correct Path |
|---------------|------------|--------------|
| Line 111 | `python extend_pathways.py` | `python src/extend_pathways.py` |
| Line 119 | `python extend_datasets.py` | `python src/extend_datasets.py` |
| Line 152 | `python extend_genes.py` | `python src/extend_genes.py` |
| Line 160 | `python extend_structures.py` | `python src/extend_structures.py` |
| Line 168 | `python extend_publications.py` | `python src/extend_publications.py` |
| Line 307 | `python add_annotation_urls.py` | `python src/add_annotation_urls.py` |
| Line 313 | `python test_annotation_urls.py` | `python src/test_annotation_urls.py` |

**Impact**: The following `make` targets are broken:
- `make update-pathways`
- `make update-datasets`
- `make update-genes`
- `make update-structures`
- `make update-publications`
- `make add-annotations`
- `make test`

### Recommended Fix

```makefile
# Line 111: Fix update-pathways
-	uv run python extend_pathways.py
+	uv run python src/extend_pathways.py

# Line 119: Fix update-datasets
-	uv run python extend_datasets.py
+	uv run python src/extend_datasets.py

# Line 152: Fix update-genes
-	uv run python extend_genes.py
+	uv run python src/extend_genes.py

# Line 160: Fix update-structures
-	uv run python extend_structures.py
+	uv run python src/extend_structures.py

# Line 168: Fix update-publications
-	uv run python extend_publications.py
+	uv run python src/extend_publications.py

# Line 307: Fix add-annotations
-	uv run python add_annotation_urls.py
+	uv run python src/add_annotation_urls.py

# Line 313: Fix test
-	uv run python test_annotation_urls.py
+	uv run python src/test_annotation_urls.py
```

---

## Scripts Referenced in Makefile (40 scripts)

The Makefile references these scripts through various targets:

| Script | Makefile Target(s) |
|--------|-------------------|
| `src/extend_lanthanide_data.py` | `update-genomes`, `update-biosamples` |
| `src/add_annotation_urls.py` | `update-genomes`, `add-annotations` |
| `src/extend_pathways.py` | `update-pathways` |
| `src/extend_genes.py` | `update-genes` |
| `src/extend_structures.py` | `update-structures` |
| `src/extend_publications.py` | `update-publications` |
| `src/extend_datasets.py` | `update-datasets` |
| `src/extend_transcriptomics.py` | `update-transcriptomics` |
| `src/extend_strains.py` | `update-strains` |
| `src/extend_media.py` | `update-media` |
| `src/chemical_search.py` | `update-chemicals`, `extend2` |
| `src/assay_search.py` | `update-assays`, `extend2` |
| `src/download_pdfs_from_publications.py` | `download-pdfs` |
| `src/pdf_to_markdown.py` | `convert-pdfs-to-markdown` |
| `src/extract_from_documents.py` | `extract-from-documents` |
| `src/extend_api.py` | `extend-api` |
| `src/kg_update_genes.py` | `kg-update-genes` |
| `src/kg_update_pathways.py` | `kg-update-pathways` |
| `src/kg_update_chemicals.py` | `kg-update-chemicals` |
| `src/kg_update_genomes.py` | `kg-update-genomes` |
| `src/run_kg_update.py` | `kg-update` |
| `src/annotate_kg_identifiers.py` | `annotate-kg` |
| `src/crosslink_sheets.py` | `crosslink` |
| `src/extend_by_publication.py` | `extendbypub` |
| `src/compare_excel_files.py` | `compare-excel` |
| `src/compare_excel_tsv.py` | `compare-excel-tsv` |
| `src/generate_missing_pdfs_report.py` | `report-missing-pdfs` |
| `src/merge_excel_updates.py` | `merge-excel` |
| `src/convert_sheets.py` | `convert-excel` |
| `src/tsv_to_linkml.py` | `validate-schema` |
| `src/validate_consistency.py` | `validate-consistency` |
| `src/fix_validation_issues.py` | `fix-validation` |
| `src/check_publication_pdfs.py` | `convert-pdfs-to-markdown` |
| `src/extend_from_lanm.py` | `extend-from-lanm` |
| `src/mine_extended_proteins.py` | `mine-proteins` |
| `src/kg_database.py` | `create-kg-db` |
| `src/parsers.py` | `test` (doctest) |
| `src/ncbi_search.py` | `test` (doctest) |
| `src/extend_uniprot` | `update-uniprot` (as module) |
| `examples/query_knowledge_graph.py` | `query-kg-db` |

---

## Scripts NOT in Makefile (17 orphaned)

These scripts exist in `src/` but have no Makefile target:

### Utility Scripts (should probably have targets)

| Script | Purpose | Recommendation |
|--------|---------|----------------|
| `src/add_missing_organisms.py` | Add organisms from genes table to genomes | Add target |
| `src/add_source_column.py` | Add source column to tables | Add target |
| `src/cli.py` | Command-line interface | Optional (alternative to make) |

### Library Modules (used by other scripts - OK to not have targets)

| Script | Used By |
|--------|---------|
| `src/dataset_search.py` | `extend_datasets.py` |
| `src/gene_search.py` | `extend_genes.py` |
| `src/media_search.py` | `extend_media.py` |
| `src/pathway_search.py` | `extend_pathways.py` |
| `src/publication_search.py` | `extend_publications.py` |
| `src/structure_search.py` | `extend_structures.py` |
| `src/strain_search.py` | `extend_strains.py` |
| `src/transcriptomics_search.py` | `extend_transcriptomics.py` |
| `src/uniprot_functions.py` | Multiple extend scripts |
| `src/kg_mining_utils.py` | KG update scripts |

### Auto-generated / Examples (OK to not have targets)

| Script | Reason |
|--------|--------|
| `src/linkml_models.py` | Auto-generated by `gen-linkml-models` target |
| `src/linkml_example.py` | Example code only |
| `src/__init__.py` | Package init |

---

## kg_analysis/ Scripts NOT in Makefile (5 orphaned)

**These analysis scripts have no automation:**

| Script | Purpose | Recommendation |
|--------|---------|----------------|
| `src/kg_analysis/analyze_genome_taxa.py` | Phenotypic characterization analysis | Add `analyze-phenotypes` target |
| `src/kg_analysis/comparative_functions.py` | Comparative functional genomics | Add `analyze-functions` target |
| `src/kg_analysis/find_critical_minerals.py` | Critical mineral relationships | Add `analyze-minerals` target |
| `src/kg_analysis/kg_database.py` | Phenotypic KG interface | Library (OK) |
| `src/kg_analysis/kg_function_database.py` | Function KG interface | Library (OK) |

---

## Hardcoded Data and Configuration in Python Scripts

### Summary

**Extensive hardcoding exists across 51 Python files in `src/`.** This includes complete data records, search terms, API configuration, and some fabricated placeholder data.

### Inventory of Hardcoded Data

| Category | File | Hardcoded Data | Lines | Impact |
|----------|------|----------------|-------|--------|
| **Media formulations** | `media_search.py` | `CURATED_MEDIA` dict - 7 complete media with ~50 ingredients | 135-274 | High - primary source of media/ingredient data |
| **Publications** | `publication_search.py` | `get_curated_lanthanide_publications()` - 8 papers | 96-161 | Medium - seed publications |
| **Publications** | `publication_search.py` | `search_arxiv_preprints()` - 2 fake preprints | 164-187 | **FAKE DATA** - URLs don't exist |
| **Publications** | `publication_search.py` | `search_biorxiv_preprints()` - 2 fake preprints | 190-213 | **FAKE DATA** - URLs don't exist |
| **Gene database** | `gene_search.py` | `get_lanthanide_genes_database()` - 15+ genes | 25-120 | High - seed genes with KEGG IDs |
| **Assay protocols** | `assay_search.py` | `self.curated_assays` - 7 assay protocols | 26-132 | High - all assay data |
| **Target genera** | `kg_analysis/comparative_functions.py` | `TARGET_GENERA` - 4 genera | 14-19 | Low - filtering only |
| **Lanthanides list** | `kg_analysis/find_critical_minerals.py` | `LANTHANIDES` - 17 elements | 15-20 | Low - search terms |
| **Critical minerals** | `kg_analysis/find_critical_minerals.py` | `CRITICAL_MINERALS` - 14 terms | 22-27 | Low - search terms |
| **Search terms** | `publication_search.py` | `search_terms` list | 27-33 | Medium - API query terms |
| **Search terms** | `chemical_search.py` | `self.search_terms` | 45-55 | Medium - PubChem queries |
| **Search terms** | `extend_from_lanm.py` | `self.search_terms` | 38-45 | Medium - UniProt queries |
| **Default organisms** | `publication_search.py` | `organisms` default list | 256-265 | Medium - API filtering |

---

## Makefile Target Categories

For reference, the Makefile organizes targets into these categories:

| Category | Targets | Count |
|----------|---------|-------|
| Data Updates | `update-genomes`, `update-biosamples`, etc. | 15 |
| Experimental Data | `update-chemicals`, `update-assays`, etc. | 5 |
| Utilities | `install`, `test`, `validate-*`, `convert-*` | 12 |
| KG Updates | `kg-update-*`, `annotate-kg` | 6 |
| Cross-Linking | `crosslink`, `extendbypub` | 2 |
| Excel Management | `compare-excel`, `merge-excel`, etc. | 4 |
| Workflows | `extend2`, `extend-api`, `update-all` | 3 |
| Cleanup | `clean`, `clean-extended` | 2 |
| Status | `status`, `help` | 2 |

**Total: ~51 targets defined**

---

## Summary of Issues

| Issue | Count | Severity |
|-------|-------|----------|
| Makefile targets with wrong paths (will fail) | 7 | **Critical** |
| Scripts without Makefile targets | 17 | Medium |
| kg_analysis scripts without targets | 3 | Low |
| Library modules (intentionally no target) | 12 | OK |

---

[<- Back to Index](00_index.md) | [Previous: Data Quality Issues](03_data_quality_issues.md) | [Next: API and LLM ->](05_api_and_llm.md)
