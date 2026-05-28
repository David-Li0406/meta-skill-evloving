# Chapter 7: Recommendations

[<- Back to Index](00_index.md) | [Previous: Setup Guide](06_setup_guide.md) | [Next: Appendices ->](08_appendices.md)

---

## Prioritized Fixes

### Immediate (Critical - Do First)

| Issue | Action | Files Affected |
|-------|--------|----------------|
| **Fake publications** | DELETE lines 172-205 | `src/publication_search.py` |
| **NCBI email placeholder** | Replace with real email or environment variable | `ncbi_search.py`, `transcriptomics_search.py`, `strain_search.py`, `add_missing_organisms.py` |
| **Broken Makefile paths** | Add `src/` prefix to 7 targets | `Makefile` lines 111, 119, 152, 160, 168, 307, 313 |

### Short-term (Documentation)

1. **Document the Google Sheet workflow** - who, what, when, how
2. **Define which TSV set is authoritative** - or document merge strategy
3. **Update AGENTS.md** - fix incorrect paths and references
4. **Document role vocabulary** - add to schema or separate file
5. **Document kg_microbe_nodes prefixes** - what each prefix means

### Medium-term (Process)

1. **Add changelog to Google Sheet** - or use version history
2. **Track LLM usage** - save prompts and outputs if using LLMs
3. **Fix UTF-8 encoding** - either in Google Sheets or during conversion
4. **Add source column discipline** - distinguish manual/LLM/API sources
5. **Validate media formulations against MediaDive**
6. **Verify all publication DOIs resolve**
7. **Check assay protocol URLs exist**
8. **Document sources for all curated data**

### Long-term (Architecture)

1. **Single source of truth** - decide: Google Sheet OR git-tracked TSV
2. **Bidirectional sync** - if keeping both, document merge process
3. **Validation on entry** - validate data before it enters pipeline
4. **Audit trail** - track all data changes with timestamps and authors

---

## Risk Assessment

| Risk Level | Issue | Files Affected |
|------------|-------|----------------|
| **Critical** | Fake publication data with fabricated DOIs | `publication_search.py` |
| **Critical** | NCBI email placeholder will break API calls | 4 files |
| **Critical** | 7 Makefile targets broken | `Makefile` |
| **High** | Media ingredient roles undocumented/unvalidated | `media_search.py` |
| **High** | Assay protocols may reference non-existent resources | `assay_search.py` |
| **Medium** | Search terms control data scope but undocumented | 5+ files |
| **Medium** | Custom gene IDs with no namespace documentation | `gene_search.py` |
| **Low** | Target genera/minerals lists are reasonable | `kg_analysis/` |

---

## Files Requiring Attention

| File | Priority | Action |
|------|----------|--------|
| `publication_search.py` | **Critical** | Remove fake preprints |
| `ncbi_search.py` | **Critical** | Fix email config |
| `Makefile` | **Critical** | Fix 7 broken paths |
| `media_search.py` | High | Externalize CURATED_MEDIA, document sources |
| `assay_search.py` | High | Externalize curated_assays, verify URLs |
| `gene_search.py` | High | Externalize gene database, document custom IDs |
| `chemical_search.py` | Medium | Document search terms |
| `extend_from_lanm.py` | Medium | Document search terms |
| `strain_search.py` | Medium | Fix email config |
| `transcriptomics_search.py` | Medium | Fix email config |
| `add_missing_organisms.py` | Medium | Fix email config |

---

## Recommendations for Data Model

### Immediate (Data Cleanup)

1. **Fix mojibake**: Run character encoding fix on all TSV files
2. **Deduplicate ingredients**: Create canonical ingredient IDs using CHEBI
3. **Remove redundant media_name**: Can be joined from growth_media table

### Short-term (Schema Revision)

1. **Create 3-table structure**:
   ```
   growth_media (media_id, media_name, ph, sterilization, ...)
   ingredients (ingredient_id, name, formula, chebi_id, cas_number, ...)
   media_compositions (media_id, ingredient_id, concentration, unit, role, ...)
   ```

2. **Define role vocabulary** in LinkML schema:
   ```yaml
   enums:
     IngredientRole:
       permissible_values:
         carbon_source:
           description: Primary carbon and energy source
         nitrogen_source:
           description: Primary nitrogen source
         buffer:
           description: pH buffering component
         trace_element:
           description: Essential micronutrient
         mineral:
           description: Essential macromineral cation/anion
         # ... etc
   ```

3. **Allow multiple roles**: Change `role` from string to list

### Medium-term (Process Improvement)

1. **Import MediaDive data**: Use their SPARQL endpoint to bootstrap
2. **Create ingredient lookup tool**: Auto-populate CHEBI/CAS during entry
3. **Validate on entry**: Check CHEBI IDs exist, formulas parse correctly

### Long-term (Integration)

1. **Bidirectional sync with KG-Microbe**: Push CMM-AI ingredients to KG, pull updates back
2. **DBTL loop integration**: When AI recommends a new medium, auto-create the records
3. **Track effectiveness**: Link screening_results -> media_compositions -> experiment outcomes

---

## Recommendations for Hardcoded Data

### Immediate (Critical Fixes)

1. **Remove or clearly mark fake data:**
   ```python
   # DELETE or rename to:
   def get_placeholder_arxiv_preprints() -> List[Dict]:
       """PLACEHOLDER - These are NOT real publications."""
   ```

2. **Fix NCBI email configuration:**
   ```python
   import os
   Entrez.email = os.environ.get("NCBI_EMAIL", "your.email@example.com")
   if Entrez.email == "your.email@example.com":
       raise ValueError("Set NCBI_EMAIL environment variable")
   ```

### Short-term (Externalize Data)

1. **Move hardcoded data to TSV/YAML files:**
   ```
   data/seed/
   +-- curated_media.yaml         # From CURATED_MEDIA dict
   +-- curated_publications.tsv   # From get_curated_lanthanide_publications()
   +-- curated_assays.tsv         # From self.curated_assays
   +-- curated_genes.tsv          # From get_lanthanide_genes_database()
   +-- search_config.yaml         # All search terms and defaults
   ```

2. **Create configuration file:**
   ```yaml
   # config/pipeline.yaml
   ncbi:
     email: ${NCBI_EMAIL}

   search_terms:
     publications:
       - "lanthanide methanol dehydrogenase"
       - "XoxF methylotroph"
     chemicals:
       - "lanthanophore"
       - "methylolanthanin"

   target_organisms:
     - Methylobacterium
     - Methylorubrum
     - Paracoccus
     - Methylosinus
   ```

### Medium-term (Validation)

1. **Validate media formulations against MediaDive**
2. **Verify all publication DOIs resolve**
3. **Check assay protocol URLs exist**
4. **Document sources for all curated data**

---

## Recommended Additional Makefile Targets

```makefile
# Add organisms from genes table
add-organisms: install
	uv run python src/add_missing_organisms.py

# Add source columns
add-source-columns: install
	uv run python src/add_source_column.py

# KG Analysis targets
analyze-phenotypes: install
	uv run python -m src.kg_analysis.analyze_genome_taxa

analyze-functions: install
	uv run python -m src.kg_analysis.comparative_functions

analyze-minerals: install
	uv run python -m src.kg_analysis.find_critical_minerals

analyze-all: analyze-phenotypes analyze-functions analyze-minerals
```

---

## Policy Recommendations

1. **Establish guidelines for LLM-assisted code** in this project
2. **Require citations** for all hardcoded data
3. **Track provenance** with source columns
4. **Review LLM outputs** before committing
5. **Test all URLs** in curated data

---

[<- Back to Index](00_index.md) | [Previous: Setup Guide](06_setup_guide.md) | [Next: Appendices ->](08_appendices.md)
