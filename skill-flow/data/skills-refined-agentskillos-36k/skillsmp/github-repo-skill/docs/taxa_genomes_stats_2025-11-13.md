# Taxa & Genomes Sheet Statistics - 2025-11-13

**Sheet:** `BER CMM Data for AI - for editing` → `taxa_and_genomes`  
**Date:** 2025-11-13  
**Total Rows:** 211 (up from 197 in git)  
**Overall Grade:** B (90/100) - Good with minor normalization issues

---

## Summary Statistics

| Column Name                          | Blank | Populated | Unique | Duplicated | Notes |
|--------------------------------------|-------|-----------|--------|------------|-----------------------------------------------------|
| Scientific name                      |     0 |       211 |    211 |          0 | Perfect primary key; mostly consistent 'sp.' usage |
| NCBITaxon id                         |     1 |       210 |    208 |          2 | ⚠ 2 duplicates: 270351, 157278 |
| Genome identifier (GenBank, IMG etc) |    19 |       192 |    190 |          2 | GCF:158 RefSeq, GCA:34 GenBank; 2 dups |
| source                               |    12 |       199 |     65 |          2 | ⚠ INCONSISTENT: 63 URLs mixed with 136 labels |
| kg_node_ids                          |    31 |       180 |    178 |          2 | 180 linked to both KGs; 2 dups |
| Annotation download URL              |    19 |       192 |    190 |          2 | All FTP; 2 dups (match genome dups) |

---

## Data Quality Scores

### Completeness: 93.6/100
- **100%** Scientific names (211/211)
- **99.5%** NCBITaxon IDs (210/211)
- **91.0%** Genome identifiers (192/211)
- **91.0%** Annotation download URLs (192/211)
- **94.3%** Source labels (199/211, but 63 are incorrect)
- **85.3%** KG linkage (180/211)

### Actionability: 91.0/100
- **192/211 (91%)** have complete data (taxon + genome + URL)
- Can immediately download 192 genome annotations
- Can query phenotypes for 180 organisms via KG
- **19 records** need data completion

### Knowledge Integration: 85.3/100
- **180/211 (85%)** linked to kg-microbe (phenotypes) AND kg-microbe-function (proteins)
- **132/211 (62.6%)** found via lanthanide protein searches (xoxF, lanM, etc.)
- **31/211 (14.7%)** too new for KG (no experimental data yet)

---

## Critical Issues

### ❌ Issue 1: Source Field Pollution (HIGH PRIORITY)

**Problem:** 63 records (30%) have FTP URLs in the `source` field

**Expected:**
```
source: "UniProt API search: lanM, xoxF, mxaF..."
source: "extend1"
source: "fix_validation"
```

**Actual (wrong):**
```
source: "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/333/655/..."
```

**Root Cause:**
- Early implementation used `source` for FTP URLs (no separate column existed)
- `Annotation download URL` column was added later via `add_annotation_urls.py`
- Old URLs in `source` field were never cleaned up
- **This is a migration artifact**

**Impact:**
- Source provenance is lost/unclear
- Can't track which pipeline generated the data
- URLs duplicate the `Annotation download URL` column

**Distribution:**
- 132 proper labels: "UniProt API search..."
- 63 legacy URLs: `ftp://...` ❌
- 12 blank: No tracking
- 4 proper labels: "fix_validation"

---

### ❌ Issue 2: Duplicate Taxon IDs (MEDIUM PRIORITY)

**Problem:** 2 taxon IDs appear multiple times with different organism names

**Case 1: NCBITaxon:270351**
- Row A: "Methylobacterium aquaticum CCM : 7218 , CECT : 5998 , CIP : 108333 , DSM : 16371 , personal : GR16" (no genome)
- Row B: "Methylobacterium aquaticum" (has genome GCF_050408745.1)
- **Analysis:** Same species, different strain designations
- **Decision needed:** Merge or keep separate?

**Case 2: NCBITaxon:157278**
- Row A: "uncultured Methylobacterium sp." (with period)
- Row B: "uncultured Methylobacterium sp" (no period)
- **Same genome:** GCA_965531505.1
- **Analysis:** TRUE DUPLICATE (typo in name)
- **Action:** Merge rows

**Impact:**
- Duplicate entry inflates row count
- Inconsistent organism naming
- May cause join/merge issues in downstream analysis

---

### ⚠ Issue 3: Inconsistent "sp." Formatting (LOW PRIORITY)

**Problem:** Mixed usage of "sp." (59) vs "sp" (2)

**Examples:**
- "Methylobacterium sp. MB200" ✓ (with period - correct scientific notation)
- "Paracoccus sp NSM" ✗ (without period)

**Impact:** Minor - won't break analysis but reduces polish

**Fix:** Standardize to "sp." (with period, per scientific convention)

---

## Data Provenance & Maintenance

### How the Sheet is Populated (5 Methods)

| Method | Count | Script | Names From | Source Label |
|--------|-------|--------|------------|--------------|
| 1. Manual Seed | 2 | Hand-entered | Researchers | (blank) |
| 2. NCBI Assembly Search | ~60 | `ncbi_search.py` → `extend_lanthanide_data.py` | NCBI Assembly metadata | FTP URLs ❌ (should be "extend1") |
| 3. UniProt API Protein Search | 132 | `extend_from_lanm.py` | UniProt organism field | "UniProt API search: lanM, xoxF..." ⭐ |
| 4. Validation Fixes | 4 | `add_missing_organisms.py` | genes/proteins table → NCBI Taxonomy | "fix_validation" |
| 5. Recent Manual Additions | 12 | Direct Google Sheet edits | Researchers | (blank) |

**Key Insight:** The majority (132/211 = 62.6%) of organisms were discovered via **UniProt protein searches**, not genome searches. These organisms have lanthanide-relevant proteins (xoxF, lanM, mxaF, exaF) but may not have sequenced genomes.

### Automated Maintenance Workflows

```bash
# Core extension scripts (run periodically)
make update-genomes                 # NCBI Assembly search
src/extend_from_lanm.py             # UniProt protein search (majority method)
src/add_missing_organisms.py        # Validation fixes
src/annotate_kg_identifiers.py     # Adds KG linkage
src/add_annotation_urls.py         # Generates download URLs
```

### Deduplication Strategy

Current approach:
```python
df.drop_duplicates(subset=["Scientific name"], keep="first")
```

**Gap:** Doesn't catch duplicate taxon IDs with different names (NCBITaxon:270351, 157278)

**Proposed:**
```python
# Check for duplicate taxon IDs
df.groupby('NCBITaxon id').filter(lambda x: len(x) > 1)
```

---

## kg_node_ids Column Structure

### Format Specification

```
NCBITaxon:270351|kg-microbe; NCBITaxon:270351|kg-microbe-function
```

**Components:**
- `NCBITaxon:XXXXX` - Organism's NCBI Taxonomy ID
- `|` - Pipe delimiter separates ID from KG name
- `kg-microbe` - Phenotypic knowledge graph (BacDive-derived: growth conditions, traits)
- `; ` - Semicolon-space delimiter between multiple KGs
- `kg-microbe-function` - Functional knowledge graph (UniProt-derived: proteins, pathways)

### Coverage Pattern

- **All 180** organisms with KG data are in **BOTH** graphs (100%)
- **0** organisms in only kg-microbe
- **0** organisms in only kg-microbe-function
- Script: `src/annotate_kg_identifiers.py` queries both KGs simultaneously

**What this means:**
- If an organism has `kg_node_ids`, you can query BOTH phenotypes AND protein functions
- Missing `kg_node_ids` (31 organisms) = too new for KG databases (no experimental data yet)

---

## Data Validation Results

### ✓ No Mismatches Found

1. **Genome ID ↔ Download URL:** All genome IDs match their download URLs ✓
2. **Taxon ID ↔ KG Node IDs:** All taxon IDs match their KG node entries ✓
3. **Data Structure:** Internally consistent ✓

### Incomplete Records (19 rows)

**Pattern:** Have taxon ID but no genome ID

**Organisms affected:**
- Methylobacterium aquaticum Strain 22A (no taxon OR genome)
- Methylobacterium aquaticum CCM:7218... (no genome)
- Bradyrhizobium sp. SM-2017B (no genome)
- Bradyrhizobium sp. MAFF 211645 (no genome)
- Rhizobium sp. SM-2017B (no genome)
- ... (14 more)

**Likely reasons:**
- Organisms known to NCBI but no sequenced genome yet
- Culture collection strains not yet deposited in GenBank
- Pending genome assembly submissions

---

## Recommendations

### Quick Wins (Can implement immediately)

1. **Clean source field pollution**
   - Remove 63 FTP URLs from `source` column
   - Add proper provenance labels (e.g., "extend1")
   - Script: Simple find/replace based on pattern matching

2. **Merge NCBITaxon:157278 duplicate**
   - Same genome (GCA_965531505.1)
   - Typo in organism name (sp. vs sp)
   - Keep row with period: "uncultured Methylobacterium sp."

3. **Standardize "sp." formatting**
   - Global find/replace: " sp " → " sp. "
   - Ensure space before and period after

4. **Add source labels to 12 blank rows**
   - Likely manual additions
   - Label as "manual_addition_2025-11"

### Requires Investigation

1. **NCBITaxon:270351 duplication**
   - Are these different strains of the same species?
   - Should we keep both or merge with strain info in parentheses?
   - Decision needed from domain expert

2. **19 incomplete records**
   - Search NCBI for newly available genomes
   - Contact culture collections for deposition status
   - Consider removing if permanently unavailable

3. **Validate FTP URLs**
   - Check if all 192 download links are still live
   - NCBI periodically reorganizes FTP structure
   - Script: `src/test_annotation_urls.py` exists but needs run

### Long-term Improvements

1. **Automate Google Sheet sync**
   - Current: Manual export/import
   - Proposed: Scheduled sync or webhook-based updates
   - Prevents drift between Google Sheet and git

2. **Enhanced deduplication**
   - Check taxon IDs, not just names
   - Flag potential duplicates for manual review
   - Add to `validate_consistency.py`

3. **Source field schema enforcement**
   - Validate that `source` contains only provenance labels
   - Reject FTP URLs at write time
   - Add to `validate_consistency.py`

4. **Complete KG coverage**
   - 31 organisms lack KG linkage
   - Monitor kg-microbe updates for new taxa
   - Re-run `annotate_kg_identifiers.py` periodically

---

## Action Items

### High Priority
- [ ] Clean 63 URLs from source field
- [ ] Merge NCBITaxon:157278 duplicate
- [ ] Decide on NCBITaxon:270351 (strain vs species)

### Medium Priority
- [ ] Add source labels to 12 blank rows
- [ ] Standardize "sp." formatting
- [ ] Search for genomes for 19 incomplete records

### Low Priority
- [ ] Validate all 192 FTP URLs
- [ ] Document 5 data sources in schema/README.md
- [ ] Enhance deduplication checks
- [ ] Automate Google Sheet sync

---

## Files Generated

Analysis scripts used:
- `/tmp/summary_stats.py` - Column statistics
- `/tmp/check_mismatches.py` - Data validation
- `/tmp/investigate_data.py` - Provenance analysis
- `/tmp/enhanced_table.py` - Final table generation

Repository scripts relevant to this sheet:
- `src/annotate_kg_identifiers.py` - Populates kg_node_ids
- `src/add_annotation_urls.py` - Populates Annotation download URL
- `src/add_missing_organisms.py` - Adds organisms from genes table
- `src/extend_from_lanm.py` - UniProt protein search (majority method)
- `src/ncbi_search.py` - NCBI Assembly search
- `src/validate_consistency.py` - Cross-sheet validation

---

**Generated:** 2025-11-13  
**Analyst:** Data quality assessment via Claude Code  
**Next Review:** After implementing Quick Wins
