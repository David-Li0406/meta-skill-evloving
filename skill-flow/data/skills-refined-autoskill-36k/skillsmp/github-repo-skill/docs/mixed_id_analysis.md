# Mixed ID Analysis: NCBI Taxon IDs vs BacDive Strain IDs

**Date**: 2026-01-05
**Status**: Data quality issue identified

## Problem

User provided a mixed list containing both NCBI taxon IDs and BacDive strain IDs from their source data. Analysis reveals these represent **multiple different organisms**, indicating a data quality issue.

## IDs Analyzed

### NCBI Taxon IDs (5 IDs)
```
NCBITaxon:408004
NCBITaxon:408047
NCBITaxon:40805
NCBITaxon:408050
NCBITaxon:408073
```

### BacDive Strain IDs (5 IDs)
```
163427
163431
163437
163426
163440
```

## Findings

### NCBI Taxon IDs: Not Found in BacDive

All 5 NCBI taxon IDs were **not found** anywhere in the BacDive database, including:
- `General.NCBI tax id.NCBI tax id`
- `Sequence information.16S sequences.NCBI tax ID`
- `Sequence information.Genome sequences.NCBI tax ID`

**Initial hypothesis** (INCORRECT): All IDs start with "408", which is the species-level NCBI taxon ID for *Methylorubrum extorquens* (NCBITaxon:408), so they might be strain-level IDs.

**ACTUAL FINDINGS** (via NCBI Taxonomy API):

| NCBI Taxon ID | Scientific Name | Rank | Lineage |
|---------------|-----------------|------|---------|
| 408004 | *Streptomyces sp. 13-32* | species | Actinomycetota; Streptomycetaceae; Streptomyces |
| 408047 | *Streptomyces sp. 1A01510* | species | Actinomycetota; Streptomycetaceae; Streptomyces |
| 40805 | *Dasytricha* | **genus** | **Ciliophora** (ciliate protozoa, NOT bacteria!) |
| 408050 | *Streptomyces sp. 1A01536* | species | Actinomycetota; Streptomycetaceae; Streptomyces |
| 408073 | *Epalxellidae* | **family** | **Ciliophora** (ciliate protozoa, NOT bacteria!) |

**Critical Issue**: These NCBI taxon IDs have **NOTHING to do with** *Methylorubrum*:
- 3 are unclassified *Streptomyces* species (Actinomycetota phylum)
- 2 are **ciliate/protozoa** taxa (not even bacteria!)

This is a **severe data quality error** - the list mixes:
- *Methylorubrum* strain IDs (from BacDive)
- *Streptomyces* taxon IDs (wrong genus, wrong phylum)
- Protozoa taxon IDs (wrong kingdom!)

These appear to be **completely erroneous/unrelated** taxon IDs, not legitimate references for *Methylorubrum* strains.

### BacDive Strain IDs: Found but Multiple Species

All 5 BacDive strain IDs were found, but they represent **3 DIFFERENT SPECIES**:

| BacDive ID | Species | NCBI Taxon | Count |
|------------|---------|------------|-------|
| 163426 | *Methylorubrum extorquens* | 408 (species) | 1 strain |
| 163427 | *Methylorubrum rhodesianum* | 29427 (species) | 2 strains |
| 163431 | *Methylorubrum rhodesianum* | 29427 (species) | ↑ |
| 163437 | *Methylorubrum zatmanii* | 29429 (species) | 2 strains |
| 163440 | *Methylorubrum zatmanii* | 29429 (species) | ↑ |

**Analysis**: The list mixes strains from 3 different species within the *Methylorubrum* genus.

## Data Quality Impact

This finding demonstrates **catastrophic data quality issues** that the reconciliation system must detect:

1. **Mixed identifier types**: NCBI taxon IDs and BacDive strain IDs shouldn't be in the same list
2. **Multiple bacterial species**: BacDive IDs represent 3 different *Methylorubrum* species
3. **Wrong genus**: 3 NCBI taxon IDs are for *Streptomyces* (Actinomycetota), not *Methylorubrum* (Alphaproteobacteria)
4. **Wrong kingdom**: 2 NCBI taxon IDs are for **ciliate protozoa**, not bacteria at all!
5. **Unresolvable IDs**: All 5 NCBI taxon IDs are completely unrelated to the *Methylorubrum* strains in the same list

**Severity**: This is not just a data entry error - it suggests fundamental confusion about organism identity. Someone appears to have randomly selected NCBI taxon IDs that have no relationship to the actual strains.

## Related Issues

This is the third data quality issue identified:

1. **Row 10 of strains.tsv**: Culture collection IDs from 4 different strains
   - DSM:1337 claimed to be "AM-1" but is actually "TK 0001"
   - Mixes BacDive IDs: 7142, 7143, 7146, 154971

2. **Sinorhizobium meliloti**: Historical name requires synonym search
   - Now called *Ensifer meliloti*

3. **This finding**: Mixed NCBI taxon IDs and BacDive strain IDs representing multiple species

## Recommendations

### Critical Validation Rules

1. **Taxonomic Consistency Check**:
   - Query NCBI Taxonomy API to verify taxon IDs belong to expected taxonomic groups
   - **ERROR** if taxon IDs are from different phyla (e.g., Alphaproteobacteria vs Actinomycetota)
   - **CRITICAL ERROR** if taxon IDs are from different kingdoms (e.g., Bacteria vs Protozoa)

2. **Identifier Type Consistency**:
   - Detect mixed identifier types in single field (strain IDs vs taxon IDs)
   - **WARNING** if culture collection IDs resolve to multiple BacDive entries
   - **ERROR** if NCBI taxon IDs can't be found in BacDive and belong to wrong genus

3. **Cross-Reference Validation**:
   - For each NCBI taxon ID, verify it matches the genus/species of associated strain IDs
   - For *Methylorubrum* strains, NCBI taxon should be genus 33011 or species 408/29427/29429
   - **ERROR** if taxon ID is for a different genus

### Reconciliation Report Format

```
CRITICAL ERROR: Taxonomic mismatch detected
  Expected: Methylorubrum (Alphaproteobacteria)

  BacDive IDs (valid):
    - BacDive:163426 → Methylorubrum extorquens (NCBITaxon:408) ✓
    - BacDive:163427 → Methylorubrum rhodesianum (NCBITaxon:29427) ⚠️ DIFFERENT SPECIES
    - BacDive:163437 → Methylorubrum zatmanii (NCBITaxon:29429) ⚠️ DIFFERENT SPECIES

  NCBI Taxon IDs (INVALID):
    - NCBITaxon:408004 → Streptomyces sp. 13-32 ❌ WRONG GENUS (Actinomycetota)
    - NCBITaxon:408047 → Streptomyces sp. 1A01510 ❌ WRONG GENUS (Actinomycetota)
    - NCBITaxon:40805 → Dasytricha ❌ WRONG KINGDOM (Protozoa)
    - NCBITaxon:408050 → Streptomyces sp. 1A01536 ❌ WRONG GENUS (Actinomycetota)
    - NCBITaxon:408073 → Epalxellidae ❌ WRONG KINGDOM (Protozoa)

Action required: Remove invalid NCBI taxon IDs or verify source data for errors.
```

## Test Scripts

### BacDive Analysis

Analysis performed by `/tmp/detailed_analysis.py`:

```bash
uv run python /tmp/detailed_analysis.py
```

The script:
1. Groups BacDive results by species
2. Searches for NCBI taxon IDs in all possible BacDive fields
3. Identifies when multiple species are present
4. Reports unresolvable NCBI taxon IDs

### NCBI Taxonomy Lookup

NCBI Taxonomy API queries performed by `/tmp/lookup_ncbi_with_names.py`:

```bash
uv run python /tmp/lookup_ncbi_with_names.py
```

The script:
1. Queries NCBI Taxonomy API for scientific names, ranks, and lineages
2. Identifies taxonomic mismatches (wrong genus, wrong kingdom)
3. Uses existing `cmm_ai_automation.strains.ncbi` module functions:
   - `fetch_ncbi_batch()` - Batch fetch taxonomy data
   - `fetch_ncbi_linkouts()` - Get external database links
   - `extract_xrefs_from_linkouts()` - Parse BacDive/BioCyc/LPSN references

## Next Steps

When ready to build the full reconciliation validator:

1. Implement `ReconciliationValidator` class
2. Add rules for detecting:
   - Mixed identifier types
   - Multiple species in single field
   - Unresolvable identifiers
3. Generate comprehensive validation reports
4. Apply to entire `strains.tsv` file
5. Create remediation suggestions for each issue type
