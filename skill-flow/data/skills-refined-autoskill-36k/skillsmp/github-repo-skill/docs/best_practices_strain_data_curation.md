# Best Practices for Bacterial Strain Data Curation

**Project**: Critical Minerals and Materials (CMM)
**Version**: 2.0
**Date**: 2026-01-06

---

## Executive Summary

This document establishes data curation best practices for bacterial strain datasets based on observations from the CMM project's strains.tsv validation and reconciliation efforts. These practices align with established standards from the knowledge graph, semantic web, and culture collection communities while addressing practical data quality issues encountered during curation.

---

## Core Principles

### 1. **FAIR Data Principles**

All strain data should be:
- **Findable**: Use globally unique identifiers (CURIEs/URIs)
- **Accessible**: Link to authoritative databases (BacDive, NCBI, culture collections)
- **Interoperable**: Follow KGX/Biolink standards for knowledge graphs
- **Reusable**: Document provenance and use machine-readable formats

**Authority**: Wilkinson et al. (2016) "The FAIR Guiding Principles for scientific data management and stewardship" - *Scientific Data*

---

## Identifier Best Practices

### 2. **Use CURIEs for All Entities**

**Practice**: All subject, predicate, and object columns in relationship tables must use CURIEs (Compact URIs) with defined prefix expansions registered in the Bioregistry.

**Rationale**: CURIEs provide:
- Global uniqueness without namespace conflicts
- Human-readable prefixes (e.g., `NCBITaxon:408`, `DSM:1337`)
- Compatibility with Linked Data and Semantic Web standards
- Standardized prefix resolution via Bioregistry

**Standards**:
- **W3C CURIE Syntax 1.0** (https://www.w3.org/TR/curie/)
- **Bioregistry** (https://bioregistry.io/) - Central registry for namespace prefixes

**Examples**:
```
✓ GOOD: NCBITaxon:408, BacDive:7143, DSM:1337
✗ BAD:  408, 7143, "DSM 1337" (without prefix)
✗ BAD:  CustomDB:123 (prefix not in Bioregistry)
```

**Note**: URIs (e.g., `http://purl.obolibrary.org/obo/NCBITaxon_408`) are acceptable when the definitive namespace hasn't been established, but KGX requires conversion to CURIEs for final export.

**Bioregistry Compliance**: Before introducing a new prefix, check if it exists in the Bioregistry. If not, consider submitting a prefix registration request or using an existing alternative.

---

### 3. **Reconcile Identifiers Against Authoritative Sources**

**Practice**: Verify all culture collection IDs, NCBI taxon IDs, and species names against authoritative databases (BacDive, NCBI Taxonomy, LPSN).

**Issues Observed**:
- Gross mismatches between binomial names, strain names, and culture collection IDs
- **DSM:1337 is NOT the AM-1 strain** (it's TK 0001; AM-1 is DSM:1338)
- Bad external links (NCBI's AM1 linkouts point to wrong strains)
- Substring search errors causing false matches

**Authority**:
- **WFCC** (World Federation for Culture Collections) Guidelines for the Establishment and Operation of Collections of Microorganisms
- **MIRIAM Guidelines** (Minimum Information Required In the Annotation of Models) - requires unambiguous identifiers

**Implementation**: Use exact matching with word boundaries, not substring searches. Validate cross-references bidirectionally.

---

### 4. **Consistent Identifier Formatting**

**Practice**: Standardize formatting of culture collection IDs, strain designations, and accessions.

**Issues Observed**:
- `AM1` vs `AM-1` vs `AM 1`
- `ORS 2060` vs `ORS2060`
- `DSM:1337` vs `DSM 1337` vs `DSMZ:1337`

**Standard**:
- **BacDive convention**: Space-separated (e.g., `DSM 1337`)
- **CURIE convention**: Colon-separated (e.g., `DSM:1337`)
- **Internal recommendation**: Use CURIE format for data storage, document BacDive's format for reconciliation

**Authority**: Global Genome Biodiversity Network (GGBN) Data Standard - Specimen identifiers should follow institutional conventions consistently.

---

## Data Structure Best Practices

### 5. **Row Integrity: All Columns Must Refer to the Same Entity**

**Practice**: Every column in a row must describe the same biological entity. Auto-populated columns must not introduce identifiers for different organisms.

**Rationale**: Data tables represent assertions about individual entities. When different columns contain identifiers for different organisms, the row loses semantic coherence and becomes unusable for knowledge graph construction.

**Issues Observed**:
- Auto-populated columns (e.g., `kg_microbe_nodes`) violating row integrity when lookups use substring matching or other fuzzy methods
- BacDive ID substring matching (e.g., searching for "1337" matches both BacDive:1337 and BacDive:13378, which are different strains)
- NCBI taxon ID mismatches where auto-lookup retrieves IDs for completely different organisms (Streptomyces, protozoa instead of Methylorubrum)

**Challenge**: Without clear documentation of which columns are hand-entered versus auto-populated, it becomes difficult to determine which values are authoritative when conflicts arise.

**Best Practice**:
1. **Document provenance**: Mark which columns are manually curated vs auto-populated (see §9)
2. **Validate cross-references**: When auto-populating, verify that retrieved identifiers genuinely refer to the same organism described in manually-entered columns
3. **Use exact matching**: Avoid substring searches that can retrieve unrelated identifiers (see §17)
4. **Establish authority hierarchy**: Define which columns are authoritative (typically manually-entered ones) and which are derived

**Standard**: **RDF semantics** - Each row corresponds to an RDF resource; all properties must describe that resource, not multiple different resources.

---

### 6. **Single vs Multi-Valued Columns**

**Practice**: Decide in advance whether each column is single-valued or multi-valued, and document this in the schema.

**Rationale**: Prevents ambiguity in data interpretation and enables proper normalization.

**Standards**:
- **LinkML**: Use `multivalued: true` in schema definitions
- **KGX**: Multi-valued attributes should use list serialization (e.g., `["value1", "value2"]`)

**Examples**:
```yaml
# LinkML Schema
slots:
  culture_collection_ids:
    multivalued: true
    description: All culture collection identifiers for this strain

  species_name:
    multivalued: false
    description: Binomial species name (single value)
```

---

### 7. **Remove Duplicative Columns**

**Practice**: Eliminate redundant columns with overlapping semantics.

**Issues Observed**:
- `name_synonyms` and `alternative_names` columns both contain synonyms
- Multiple "species" columns with slightly different values

**Solution**: Consolidate into a single well-defined column (e.g., `species_synonyms`) with clear documentation of what qualifies as a synonym.

**Authority**: **Darwin Core** (biodiversity data standard) - Avoid term redundancy; use `scientificName`, `acceptedNameUsage`, and `nameAccordingTo` for taxonomic names.

---

### 8. **Deduplicate Rows**

**Practice**: Remove duplicate rows before data integration or KGX export.

**Detection**:
- Identical primary keys (e.g., same `strain_id`)
- Duplicate culture collection IDs mapping to same strain

**Standard**: **OBO Foundry Principle 6**: Textual definitions should be unique within an ontology (extended here: entity definitions should be unique within a dataset).

---

## Provenance and Curation Metadata

### 9. **Document Data Provenance**

**Practice**: Clearly indicate the source and method for every data value:
- **Human expert entry** (manually curated)
- **Computational mapping** (automated lookup from BacDive, NCBI, etc.)
- **AI inference/speculation** (e.g., predicted chemical roles)

**Standard**: **W3C PROV-O** (Provenance Ontology) - provides classes for Entity, Activity, Agent

**Implementation**:
```tsv
# Add provenance columns:
species_name    species_name_source    species_name_method
Methylorubrum extorquens    BacDive:7143    automated_lookup
```

**Authority**:
- **GO Consortium Evidence Codes** - Distinguish between different types of evidence (IEA = Inferred from Electronic Annotation, TAS = Traceable Author Statement, etc.)
- **Gene Ontology Annotation Guidelines** - Require provenance for all annotations

---

### 10. **Mark Auto-Populated/Extended Columns**

**Practice**: Define which columns are manually entered vs auto-populated from lookups, and document this in column headers or schema.

**Suggested Convention**:
```tsv
# Column naming:
strain_id              # Manual entry (PRIMARY KEY)
species_name           # Manual entry
ncbi_taxon_species     # AUTO-POPULATED from NCBI API
bacdive_id             # AUTO-POPULATED from BacDive search
genome_accession       # AUTO-POPULATED from BacDive.Sequence_information
```

**Authority**: **Bioschemas** - Recommends explicit provenance properties for computed vs asserted values.

---

## Relationship Tables (Edge Lists)

### 11. **Name Tables by Their Content**

**Practice**: Relationship tables should be named by the relationship they represent, not vague descriptions.

**Issues Observed**:
- `growth_preferences` table contains "grows in" relationships but also shake speed, temperature, etc.

**Solution**: Either:
1. **Single relationship per table**: `grows_in_media.tsv`, `cultivated_at_temperature.tsv`
2. **Generic edge list**: `strain_relationships.tsv` with explicit `predicate` column

**Authority**: **Biolink Model** - Defines specific relationship types (predicates) like `capable_of`, `has_phenotype`, `located_in`

---

### 12. **Design Decision Needed: Multi-Dimensional Experimental Data**

**Issue**: Experimental datasets often involve multi-dimensional observations where a biological phenomenon is tested across multiple conditions (e.g., strain S grown in medium M at various temperatures, shake speeds, and plate types). Current relationship tables may be underspecified for representing these complex experimental designs.

**Scenario**: When experiments test strain growth across:
- 100 different media formulations
- 5 temperature conditions
- 3 RPM settings
- 2 plate types

...how should this be represented in a knowledge graph?

**Standard Approaches and Their Limitations**:

1. **One edge per combination**: Create individual edges for each permutation
   - **Issue**: 100 × 5 × 3 × 2 = 3,000 edges for a single strain
   - **Authority**: This follows KGX/RDF triple structure but becomes unwieldy

2. **Reification**: Create intermediate "observation" or "experiment" nodes
   - **Example**: Strain → participated_in → Experiment123 → has_medium → M, has_temperature → T
   - **Authority**: RDF reification pattern, also used in SIO (Semantic Science Integrated Ontology)
   - **Issue**: Adds complexity and indirection

3. **Edge properties/qualifiers**: Attach conditions as edge qualifiers
   - **Example**: Strain --[grows_in]--> Medium (temperature: 30C, RPM: 200)
   - **Authority**: Biolink Model supports qualifiers; Wikidata uses this extensively
   - **Issue**: Not all graph databases support rich edge properties

4. **Separate tables for each dimension**: `strain_media.tsv`, `strain_temperature.tsv`
   - **Issue**: Loses the connection between co-varied experimental conditions

**Recommendation**: The team should decide on the semantic model and explicitly document it **before** experimentalists begin populating growth condition data. The choice depends on:
- Query patterns (how will data be retrieved?)
- Graph database capabilities
- Desired granularity of provenance tracking
- Ease of data entry for experimentalists

**Authority**:
- **STATO** (Statistics Ontology) - For representing experimental designs
- **OBI** (Ontology for Biomedical Investigations) - For describing experimental protocols
- **RO** (Relation Ontology) - For qualified relations in biological contexts

**Next Step**: Convene a design discussion to select an approach and document it in the schema before data collection proceeds.

---

### 13. **Relationship Tables Must Have S-P-O Structure**

**Practice**: All relationship/edge tables must contain:
- **Subject**: CURIE for the entity (e.g., `strain_id`)
- **Predicate**: CURIE for the relationship type (e.g., `biolink:capable_of`)
- **Object**: CURIE for the related entity (e.g., `CHEBI:16411`)

**Standard**: **KGX (Knowledge Graph Exchange)** format requires:
```tsv
subject    predicate    object    (optional: qualifiers, evidence, sources)
DSM:1337   biolink:in_taxon   NCBITaxon:408
DSM:1337   grows_in    MediaDive:123
```

**Authority**:
- **RDF (Resource Description Framework)** - Triple structure is fundamental to Linked Data
- **Biolink Model** - Standardized predicates for biomedical knowledge graphs

---

### 14. **Use Real KGX Methods**

**Practice**: Don't reinvent serialization. Use established KGX libraries and methods for export.

**Tools**:
- `kgx` Python package (https://github.com/biolink/kgx)
- Biolink Model Toolkit

**Anti-pattern**: Writing custom CSV-to-KGX converters without following KGX schema validation.

**Authority**: **Monarch Initiative** - Maintains KGX standard and provides reference implementation.

---

## Data Quality Standards

### 15. **Validate Taxonomic Concordance**

**Practice**: Ensure binomial names, strain designations, and culture collection IDs all refer to the same organism.

**Validation Checks**:
1. **Species name ↔ NCBI taxon**: Use `search_species_with_synonyms()` to handle reclassifications
2. **Culture collection ID ↔ BacDive**: Verify strain designation matches
3. **Cross-database consistency**: NCBI Assembly → BacDive → Culture Collections should agree

**Issue**: "Binomial to strain (culture collection ID) usually agree" - This should be **always**, not usually!

**Authority**: **INSDC** (International Nucleotide Sequence Database Collaboration) - Requires taxonomic consistency between sequence records and strain metadata.

---

### 16. **Handle Taxonomic Reclassifications**

**Practice**: Search by both current and historical taxonomic names (synonyms).

**Examples**:
- *Sinorhizobium meliloti* → *Ensifer meliloti*
- *Methylobacterium extorquens* → *Methylorubrum extorquens*

**Implementation**: Use 3-stage search (current name, LPSN name, synonyms array).

**Authority**: **LPSN** (List of Prokaryotic names with Standing in Nomenclature) - Authoritative source for validly published bacterial names and their synonyms.

---

### 17. **Anti-Pattern: Substring Searches for Identifiers**

**Problem**: Substring searches are a primary cause of data quality issues in strain data curation. They lead to false matches that violate row integrity and introduce identifiers for completely unrelated organisms.

**Why Substring Matching Fails**:

1. **Culture collection IDs**: Searching for "DSM 1337" as a substring matches:
   - DSM 1337 (correct)
   - DSM 13378 (wrong strain!)
   - DSM 1337**4** (wrong strain!)
   - Any text containing "DSM 1337" anywhere

2. **Intermediate identifiers**: When a lookup column contains a CURIE as a substring of a longer string, substring searches can match unintended entries:
   - Searching for "BacDive:7143" might match "related_to: BacDive:7143, BacDive:71430"
   - Returns data for BacDive:71430 (wrong organism)

3. **Numeric IDs**: Searching for "408" matches:
   - NCBITaxon:408 (*Methylorubrum extorquens*)
   - NCBITaxon:408004 (*Streptomyces* sp. - wrong genus, wrong phylum!)
   - NCBITaxon:40805 (ciliate protozoa - not even bacteria!)

**Real Impact Observed**:
- During reconciliation, substring searches for NCBI taxon IDs returned Streptomyces and protozoan identifiers instead of Methylorubrum
- Culture collection lookups matched wrong strains (e.g., DSM:13378 when searching for DSM:1337)
- Auto-populated columns violated row integrity due to false matches

**Correct Approach**: Use word-boundary regex or exact matching:

```python
# ✗ WRONG: Substring search
if search_id in full_string:
    return match  # Will match "1337" inside "13378"

# ✓ CORRECT: Word-boundary regex
import re
pattern = rf"(^|,\s*){re.escape(prefix)}[\s:-]*{re.escape(number)}(\s*,|$)"
if re.search(pattern, full_string):
    return match  # Only matches exact "DSM:1337", not "DSM:13378"

# ✓ ALSO CORRECT: Exact matching after normalization
if normalize(search_id) == normalize(database_id):
    return match
```

**Implementation Guidelines**:
1. Always use word boundaries or exact matching for identifier lookups
2. Normalize identifiers before comparison (e.g., strip whitespace, convert to uppercase)
3. Validate that returned identifiers match the expected format (prefix + number)
4. When auto-populating columns, verify that retrieved data refers to the same organism as manually-entered fields

**Authority**:
- **Regular Expression Best Practices** - Use `\b` word boundaries or anchors (`^`, `$`) for identifier matching
- **MIRIAM Guidelines** - Identifiers must be matched exactly against registry patterns

**Testing**: Include test cases with near-matches (e.g., "1337" vs "13378") to ensure substring searches don't cause false positives.

---

### 18. **Detect Spelling Errors**

**Practice**: Implement automated spell-checking against authoritative taxonomic databases.

**Tools**:
- BacDive species list
- NCBI Taxonomy dump
- LPSN validated names

**Example Error Found**: `Methylobrum nodulans` → should be `Methylobacterium nodulans`

**Authority**: **Catalogue of Life** - Global species checklist for spelling validation.

---

### 19. **Quality Assurance via Controlled Error Injection**

**Practice**: Test the robustness of data pipelines, validation scripts, and ML models by intentionally introducing known errors in a controlled, traceable manner. This ensures that quality checks actually detect problems before production use.

**Rationale**: Data quality tools and ML models can give false confidence if they haven't been tested against realistic error scenarios. Controlled error injection (also called "adversarial validation" in ML contexts) verifies that:
- Validation scripts catch common data entry mistakes
- Reconciliation pipelines handle edge cases
- ML models don't overfit to dataset artifacts
- Human reviewers notice anomalies

**Implementation**:

1. **Create a contaminated test dataset**:
   - Copy a subset of production data
   - Inject known errors with tracking metadata
   - Examples: swap species names, introduce typos, duplicate rows, mismatch identifiers

2. **Document injected errors**:
   ```yaml
   # test_data_errors.yml
   - row: 15
     column: species_name
     error_type: taxonomic_synonym
     original: Methylorubrum extorquens
     injected: Methylobacterium extorquens
     expected_behavior: validation should flag or auto-correct
   ```

3. **Run validation pipeline**:
   - Execute data quality checks on contaminated dataset
   - Measure detection rate (recall): did it catch all injected errors?
   - Measure false positive rate: did it flag correct data?

4. **Test ML model robustness**:
   - Train on clean data, test on contaminated data
   - Measure performance degradation
   - Verify that model doesn't learn to exploit systematic errors (e.g., always predicting based on column position rather than content)

**Examples of Errors to Inject**:
- Taxonomic: Use deprecated species names, swap genus/species
- Identifiers: Substring matches (DSM:1337 ↔ DSM:13378), formatting variants (AM1 vs AM-1)
- Duplicates: Exact row duplicates, same strain with different IDs
- Missing data: Strategic NULLs in required fields
- Row integrity violations: Mismatch between species_name and ncbi_taxon_id

**Standards and Authorities**:
- **Adversarial Validation** (Kaggle ML competition practice) - Testing model robustness to train/test distribution shift
- **Google's TensorFlow Data Validation (TFDV)** - Framework for detecting data anomalies
- **Breck et al. (2019)** "Data Validation for Machine Learning" - *SysML Conference* - Describes production ML data validation at scale
- **Chaos Engineering for Data** - Adapting chaos engineering principles (intentional failure injection) to data pipelines

**Benefits**:
- Increases confidence in data quality tools
- Reveals blind spots in validation logic
- Documents expected behavior for edge cases
- Prevents overfitting in ML workflows
- Serves as regression tests when modifying pipelines

**Caution**: Always maintain a clear audit trail of which datasets contain injected errors. Never let contaminated data leak into production knowledge graphs.

---

## Schema and Documentation

### 20. **Define All Columns in Schema**

**Practice**: Use LinkML or similar schema language to formally define:
- Column names
- Data types
- Single vs multi-valued
- Allowed values (enumerations)
- Mappings to ontology terms

**Standard**: **LinkML** (Linked Data Modeling Language) - Schema language designed for knowledge graphs

**Example**:
```yaml
classes:
  Strain:
    slots:
      - strain_id
      - species_name
      - type_strain
      - culture_collection_ids

slots:
  strain_id:
    identifier: true
    required: true
    description: Primary culture collection identifier

  type_strain:
    range: boolean
    description: Whether this is the nomenclatural type strain for the species
```

**Authority**:
- **LinkML** (https://linkml.io/)
- **Biolink Model** - Uses LinkML for schema definition

---

## Where You Align vs Conflict with Standards

### ✓ **Strong Alignment**:

1. **CURIEs for identifiers** - Fully aligned with W3C, Semantic Web, OBO Foundry
2. **Provenance tracking** - Aligned with PROV-O, GO annotation standards
3. **KGX structure** - Following Monarch Initiative standards
4. **Taxonomic validation** - Following LPSN, NCBI Taxonomy best practices
5. **FAIR principles** - Implicit in all recommendations
6. **Error injection testing** - Aligned with ML best practices (TFDV, adversarial validation)

### ⚠️ **Minor Conflicts/Extensions**:

1. **URIs vs CURIEs**: This document suggests "URIs are handy when namespace isn't established" but then requires CURIEs for KGX
   - **Resolution**: This is fine - use URIs during exploration/development, convert to CURIEs for final KGX export
   - **Standard**: KGX allows both but prefers CURIEs with registered prefixes

2. **Relationship table naming**: "Named by what they contain" could conflict with database normalization principles
   - **Resolution**: For KGX, use generic `edges.tsv` with explicit `predicate` column rather than per-predicate tables
   - **Standard**: KGX typically uses unified edge files, not per-relationship tables

3. **"Real KGX methods"**: Clarified to mean both using `kgx` library for transformations AND following Biolink Model predicates

4. **Multi-dimensional experimental data**: Identified as an open design decision requiring team discussion before implementation

---

## Implementation Checklist

- [ ] Adopt LinkML schema for `strains.tsv`
- [ ] Add provenance columns (`_source`, `_method`, `_date`)
- [ ] Implement reconciliation pipeline with BacDive + NCBI
- [ ] Use exact matching (word boundaries) instead of substring searches
- [ ] Audit existing auto-populated columns for row integrity violations
- [ ] Standardize identifier formats (document BacDive vs CURIE conventions)
- [ ] Remove duplicate columns (`name_synonyms` vs `alternative_names`)
- [ ] Deduplicate rows
- [ ] Validate taxonomic concordance across all columns
- [ ] Convert relationship tables to S-P-O format
- [ ] Define single vs multi-valued columns in schema
- [ ] Use `kgx` library for KGX export
- [ ] Register custom prefixes in Bioregistry (or use existing alternatives)
- [ ] Convene design discussion for multi-dimensional experimental data representation
- [ ] Create contaminated test dataset with injected errors for quality assurance testing

---

## References

### Standards and Authorities

1. **FAIR Principles**: Wilkinson et al. (2016) *Scientific Data* 3:160018 - https://doi.org/10.1038/sdata.2016.18

2. **W3C CURIE Syntax**: https://www.w3.org/TR/curie/

3. **Bioregistry**: https://bioregistry.io/

4. **KGX (Knowledge Graph Exchange)**: https://github.com/biolink/kgx

5. **Biolink Model**: https://biolink.github.io/biolink-model/

6. **LinkML**: https://linkml.io/

7. **W3C PROV-O**: https://www.w3.org/TR/prov-o/

8. **LPSN** (List of Prokaryotic names): https://lpsn.dsmz.de/

9. **WFCC Guidelines**: World Federation for Culture Collections - http://www.wfcc.info/

10. **MIRIAM Guidelines**: https://www.nature.com/articles/nbt1156

11. **Darwin Core**: https://dwc.tdwg.org/

12. **OBO Foundry Principles**: http://obofoundry.org/principles/

13. **GO Annotation Guidelines**: http://geneontology.org/docs/go-annotation-policies/

14. **INSDC Standards**: https://www.insdc.org/

15. **Global Genome Biodiversity Network (GGBN)**: https://www.ggbn.org/

16. **Bioschemas**: https://bioschemas.org/

17. **STATO** (Statistics Ontology): http://stato-ontology.org/

18. **OBI** (Ontology for Biomedical Investigations): http://obi-ontology.org/

19. **RO** (Relation Ontology): http://obofoundry.org/ontology/ro.html

20. **SIO** (Semantic Science Integrated Ontology): https://github.com/MaastrichtU-IDS/semanticscience

### Machine Learning and Data Quality

21. **Breck et al. (2019)**: "Data Validation for Machine Learning" - *SysML Conference* - https://mlsys.org/Conferences/2019/doc/2019/167.pdf

22. **TensorFlow Data Validation (TFDV)**: https://www.tensorflow.org/tfx/guide/tfdv

23. **Kaggle Adversarial Validation**: https://www.kaggle.com/code/carlmcbrideellis/what-is-adversarial-validation

24. **Chaos Engineering for Data**: Adapted from Netflix Chaos Engineering principles - https://principlesofchaos.org/

---

## Glossary

- **CURIE**: Compact URI - `prefix:local_id` (e.g., `NCBITaxon:408`)
- **KGX**: Knowledge Graph Exchange format
- **S-P-O**: Subject-Predicate-Object (RDF triple structure)
- **LPSN**: List of Prokaryotic names with Standing in Nomenclature
- **Type Strain**: Nomenclatural type strain used to define a species
- **Provenance**: The origin and history of a data value
- **Row Integrity**: Principle that all columns in a row describe the same entity
- **Bioregistry**: Central registry for standardized namespace prefixes
- **Reification**: Creating intermediate nodes to represent n-ary relationships
- **Adversarial Validation**: Testing robustness by introducing controlled errors

---

## Acknowledgments

These best practices were developed based on observations during reconciliation of the CMM strains dataset against BacDive, NCBI Taxonomy, and culture collection databases. Issues identified include identifier mismatches (DSM:1337/AM-1), formatting inconsistencies (AM1 vs AM-1), taxonomic reclassifications (Sinorhizobium → Ensifer), row integrity violations from substring-based auto-population, and the need for multi-dimensional experimental data representation.

Special thanks to the BBOP team for collaborative development of these practices.

---

**Document Status**: Living document - update as new issues are identified and standards evolve.
