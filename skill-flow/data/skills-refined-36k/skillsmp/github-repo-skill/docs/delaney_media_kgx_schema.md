# Delaney Media KGX Schema Specification

## Overview

This document specifies the standardized KGX/Biolink schema for Delaney media data files, ensuring full compliance with KGX format while preserving complete scientific provenance without reification.

## Design Principles

1. **Standards Compliance**: Use standard Biolink Model properties wherever possible
2. **Provenance Preservation**: Maintain full audit trail to source publications via PROV-O aligned columns
3. **Flat Structure**: Avoid reification - use direct columns for quantitative measurements
4. **Semantic Precision**: Use Units Ontology (UO) CURIEs for all units
5. **Traceability**: Enable deterministic, unambiguous mapping back to source data

## Node Schema

### Required Columns

| Column | Description | Example | Standard |
|--------|-------------|---------|----------|
| `id` | CURIE identifier | `CHEBI:114249`, `doi:10.1371/journal.pone.0062957.s005` | KGX required |
| `name` | Human-readable name | `sodium dihydrogenphosphate monohydrate` | Biolink standard |
| `category` | Biolink Model category | `biolink:ChemicalEntity` | KGX required |

### Optional Columns

| Column | Description | Example | Notes |
|--------|-------------|---------|-------|
| `pH` | Numeric pH value | `6.75` | For solutions/media where pH is controlled |
| `comments` | Preparation notes | `Adjust to pH 6.75 with KOH; 1 L deionized H2O` | Procedural details, volumes, mixing instructions |

Nodes include the three required KGX columns plus optional pH and comments for procedural/preparation context. Chemical properties and cross-references are stored on edges to preserve provenance context.

### Category Definitions

- **`biolink:ChemicalEntity`**: Individual chemical compounds (CHEBI, PubChem identifiers)
- **`biolink:ChemicalMixture`**: Stock solutions and defined mixtures (UUID or DOI identifiers)
- **`biolink:ComplexMolecularMixture`**: Complete culture media (DOI identifiers preferred)

### Example Nodes

**Simple chemical entity:**
```tsv
id	name	category	pH	comments
CHEBI:31440	copper(II) sulfate pentahydrate	biolink:ChemicalEntity
```

**Stock solution with preparation notes:**
```tsv
id	name	category	pH	comments
uuid:2c015a8c-75e8-43ad-8cf9-a5487d9cf525	PIPES stock 10X	biolink:ChemicalMixture	6.75	Adjust to pH 6.75 with KOH; 1 L deionized H2O
```

**Complex medium with procedural notes:**
```tsv
id	name	category	pH	comments
doi:10.1371/journal.pone.0062957.s005	MP medium from Delaney et al doi:10.1371/journal.pone.0062957	biolink:ComplexMolecularMixture		885 mL milliQ-H2O for final 1 L; mix all components except CaCl2, autoclave, then add CaCl2
```

## Edge Schema

### Core KGX Columns (Required)

| Column | Description | Example | Standard |
|--------|-------------|---------|----------|
| `subject` | Source node CURIE | `doi:10.1371/journal.pone.0062957.s005` | KGX required |
| `predicate` | Biolink relationship | `biolink:has_part` | KGX required |
| `object` | Target node CURIE | `CHEBI:114249` | KGX required |
| `knowledge_level` | Type of assertion | `knowledge_assertion` | Biolink required |
| `agent_type` | Source of assertion | `manual_validation_of_automated_agent` | Biolink required |

### Provenance Columns (Required)

| Column | Description | Example | Alignment |
|--------|-------------|---------|-----------|
| `primary_knowledge_source` | Original data source | `infores:cmm-ai-automation` | Biolink standard |
| `publications` | Supporting publication | `PMID:23646164` | Biolink standard |
| `source_specification` | Verbatim source text | `NaH2PO4·H2O` | PROV-O `prov:value` |

### Three-Tier Edge Property Structure

Edge properties follow a three-tier structure documenting data provenance from source to curation:

#### Tier 1: Source-Asserted Columns (What PDF/Source Said)

Verbatim data from the original publication, preserving exactly what was specified without normalization or correction.

| Column | Description | Example | Unit Column | Notes |
|--------|-------------|---------|-------------|-------|
| `source_specification` | Verbatim text from source | `NaH2PO4·H2O` | N/A | Free text specification |
| `source_asserted_formula` | Chemical formula from source | `C8H8N2O6S2` | N/A | May differ from canonical (e.g., PIPES PDF error) |
| `source_asserted_name` | Alternative name from source | `PIPES` | N/A | Common names |
| `source_asserted_molecular_weight` | Molecular weight from source | `302.37` | N/A | Daltons |
| `source_asserted_stock_concentration` | Stock concentration value | `300` | `source_asserted_stock_concentration_units` | As specified in source |
| `source_asserted_X` | Dilution factor | `10` | N/A | e.g., "10X" means 10-fold |
| `source_asserted_mass_added` | Mass added value | `90.711` | `source_asserted_mass_added_units` | As specified |
| `source_asserted_volume_added` | Volume added value | `100` | `source_asserted_volume_added_units` | For stock solutions |
| `source_asserted_stock_volume` | Stock prep volume | `1` | `source_asserted_stock_volume_unit` | Batch size |
| `source_asserted_final_concentration` | Final concentration value | `30` | `source_asserted_final_concentration_unit` | In final medium |
| `source_role` | Functional role from source | `Buffer/Nutrient` | N/A | As categorized by authors |

**Critical Principle**: Never modify source-asserted values. Errors and discrepancies are documented in Tier 2 comments.

#### Tier 2: Repo-Asserted Columns (Canonical/Contextual)

Assertions made by the repository curator about the subject and object in the context of THIS specific edge relationship.

**About the object (chemical being added):**

| Column | Description | Example | Notes |
|--------|-------------|---------|-------|
| `object_molecular_mass` | Canonical molecular mass | `302.37` | From ChEBI/PubChem; what MW was used for calculations |
| `object_xref` | Cross-reference for grounding | `WIKIDATA:Q27114864` | Documents HOW the object was identified |
| `object_amount_added` | Amount added (normalized) | `25.9` | With `object_amount_unit` (UO CURIE) |

**About the subject (solution being prepared):**

| Column | Description | Example | Notes |
|--------|-------------|---------|-------|
| `subject_volume_prepared` | Volume of subject prepared | `1` | With `subject_volume_unit` (UO CURIE) |

**About the relationship:**

| Column | Description | Example | Notes |
|--------|-------------|---------|-------|
| `calculated_concentration` | Molar concentration computed | `0.1876934003` | With `calculated_concentration_unit` (UO CURIE) |
| `comments` | Curation notes | `ChEBI formula differs from PDF` | Explains discrepancies, grounding decisions |

**Provenance Rationale**: These properties are on edges (not nodes) because they document the evidence and context for THIS specific assertion. If a source has an error (e.g., wrong formula), the edge shows what information was actually available when the grounding decision was made. This enables auditing: "Which facts clarified the identification?" Different edges for the same chemical might have different object_molecular_mass values if sources disagree, preserving the full provenance trail.

#### Tier 3: Unit Standardization

All units use Units Ontology (UO) CURIEs for semantic interoperability.

### Metadata Columns (Optional)

| Column | Description | Example | Standard |
|--------|-------------|---------|----------|
| `description` | Contextual notes | `Wikidata Q27288149 has no ChEBI; grounded to PUBCHEM` | Biolink standard |

### Example Edges

**Example 1: Source-specified final concentration** (PDF said "NaH2PO4·H2O 1.88 mM"):
```tsv
subject	predicate	object	source_specification	source_asserted_final_concentration	source_asserted_final_concentration_unit	subject_volume_prepared	subject_volume_unit	object_molecular_mass	comments
doi:10.1371/journal.pone.0062957.s005	biolink:has_part	CHEBI:114249	NaH2PO4·H2O	1.88	mM	1	L	137.99
```
**Tier 1 (source)**: PDF specified final concentration directly as 1.88 mM
**Tier 2 (repo)**: Canonical molecular mass from ChEBI used for any needed calculations
**No Tier 3**: No calculation needed since source gave final concentration

**Example 2: Mass-based stock with calculated concentration** (PDF: "NaH2PO4 22.5 g or 25.9 g NaH2PO4·H2O in 1 L"):
```tsv
subject	predicate	object	source_specification	source_asserted_mass_added	source_asserted_mass_added_units	source_asserted_stock_volume	source_asserted_stock_volume_unit	source_asserted_X	object_amount_added	object_amount_unit	subject_volume_prepared	subject_volume_unit	calculated_concentration	calculated_concentration_unit	object_molecular_mass	comments
uuid:a8a5a509-ba8c-4ae6-a6d3-98583066c984	biolink:has_part	CHEBI:114249	NaH2PO4 22.5 g (or 25.9 g NaH2PO4·H2O)	25.9	g	1	L	10	25.9	UO:0000021	1	UO:0000099	0.1876934003	UO:0000062	137.99
```
**Tier 1 (source)**: PDF gave mass (25.9 g hydrated form) and volume (1 L) for 10X stock
**Tier 2 (repo)**: Normalized to object_amount_added with UO units; subject_volume_prepared documented
**Tier 3 (calculated)**: Concentration = 25.9 g / 137.99 g/mol / 1 L = 0.1877 M

**Example 3: Source error documented** (PIPES formula discrepancy):
```tsv
subject	predicate	object	source_specification	source_asserted_formula	source_asserted_stock_concentration	source_asserted_stock_concentration_units	source_asserted_X	object_molecular_mass	comments
uuid:2c015a8c-75e8-43ad-8cf9-a5487d9cf525	biolink:has_part	CHEBI:44933	C8H8N2O6S2	C8H8N2O6S2	300	mM	10	302.37	ChEBI and PubChem both say C8H18N2O6S2, which matches the reported molecular mass
```
**Tier 1 (source)**: PDF formula C8H8N2O6S2 is WRONG (missing hydrogens)
**Tier 2 (repo)**: Canonical MW 302.37 from ChEBI matches the correct formula C8H18N2O6S2
**Comments**: Document the discrepancy - molecular mass is self-consistent even though formula is wrong

**Example 4: Grounding via Wikidata** (K2HPO4 has no ChEBI):
```tsv
subject	predicate	object	source_specification	source_asserted_final_concentration	source_asserted_final_concentration_unit	object_molecular_mass	object_xref	comments
doi:10.1371/journal.pone.0062957.s005	biolink:has_part	PUBCHEM.COMPOUND:16217523	K2HPO4	1.45	mM	228.22	WIKIDATA:Q27288149	WIKIDATA:Q27288149 provides no ChEBI id
```
**Tier 1 (source)**: PDF specified K2HPO4 at 1.45 mM
**Tier 2 (repo)**: Grounded to PubChem (no ChEBI available); Wikidata xref documents the grounding path
**Comments**: Explain why PubChem was used instead of ChEBI

## Unit Standardization

All measurement units must use Units Ontology (UO) CURIEs:

### Concentration Units

| Unit | Description | UO CURIE |
|------|-------------|----------|
| M | Molar | `UO:0000062` |
| mM | Millimolar | `UO:0000063` |
| μM | Micromolar | `UO:0000064` |

### Mass Units

| Unit | Description | UO CURIE |
|------|-------------|----------|
| g | Gram | `UO:0000021` |
| mg | Milligram | `UO:0000022` |
| μg | Microgram | `UO:0000023` |

### Volume Units

| Unit | Description | UO CURIE |
|------|-------------|----------|
| L | Liter | `UO:0000099` |
| mL | Milliliter | `UO:0000098` |
| μL | Microliter | `UO:0000101` |

## Provenance Strategy

### Scientific Integrity Requirements

The schema addresses specific concerns about data quality:

1. **Experimentalist Claims**: "Taxon T grows in medium M" requires traceable source
2. **LLM-Generated Data**: Noisy inputs must preserve original specification
3. **Manual Curation**: Human assertions tagged with `agent_type: manual_validation_of_automated_agent`

### Provenance Fields

- **`primary_knowledge_source`**: Links to institutional source (`infores:cmm-ai-automation`)
- **`publications`**: Links to peer-reviewed publication (PMID, DOI)
- **`source_specification`**: Preserves verbatim text from source (e.g., `NaH2PO4·H2O`)
- **`agent_type`**: Tracks who/what made the assertion:
  - `manual_agent`: Purely human curation with no automated extraction
  - `text_mining_agent`: LLM/NLP extraction without human verification
  - `manual_validation_of_automated_agent`: Human-verified automated output (used in this dataset)
  - See [Biolink AgentTypeEnum](https://biolink.github.io/biolink-model/) for complete list

### Audit Trail Example

```tsv
source_specification	primary_knowledge_source	publications	agent_type
NaH2PO4·H2O	infores:cmm-ai-automation	PMID:23646164	manual_validation_of_automated_agent
```

This enables:
- Tracing back to exact source text
- Verifying against original publication
- Identifying who/what made the claim
- Auditing LLM vs human contributions

## Validation

### Validation Script

```bash
just validate-kgx-custom
```

This runs the custom KGX validator that:
1. Monkey-patches `PrefixManager.is_curie` to allow slashes in DOIs
2. Adds custom prefixes (doi, uuid) from `config/kgx_validation_config.yaml`
3. Validates against KGX and Biolink Model requirements

### Validation Requirements

**Nodes must have:**
- Valid CURIE in `id` column
- Biolink category in `category` column
- Human-readable `name`

**Edges must have:**
- Valid subject/object CURIEs matching existing nodes
- Biolink predicate (e.g., `biolink:has_part`)
- `knowledge_level` and `agent_type` values
- At least one provenance field (publications or primary_knowledge_source)

**All edges pass if:**
```
SUCCESS: No validation errors found!
```

## Migration from Legacy Schema

### Deprecated Columns → New Standard

| Old Column | New Column | Notes |
|------------|------------|-------|
| `raw_specification` | `source_specification` | PROV-O aligned |
| `raw_name` | (removed) | Redundant with node `name` |
| `raw_molar_mass` | `molecular_mass` | Kept on edges for provenance |
| `raw_conc` + `raw_conc_units` | `concentration` + `concentration_unit` | UO CURIEs |
| `raw_role` | `description` | Biolink standard |
| `comments` | `description` | Biolink standard |
| `amount` + `units` | `amount` + `amount_unit` | Split and standardized |
| `liters_made` | `solution_volume_prepared` + `solution_volume_unit` | Split and standardized |
| `concentration_moles_per_liter` | `concentration` | With `concentration_unit: UO:0000062` |
| (new) | `xref` | Added to edges for cross-reference provenance |

### Breaking Changes

1. **No reification**: Quantities stored as flat columns, not QuantityValue objects
2. **UO CURIEs required**: All units must use Units Ontology identifiers
3. **Properties on edges**: molecular_mass and xref stay on edges to preserve provenance context
4. **Standard Biolink properties**: primary_knowledge_source, publications, description

## Best Practices

### When Adding New Data

1. **Identify entities properly**:
   - Prefer CHEBI IDs for chemicals
   - Use DOIs for published media
   - Generate UUIDs only when necessary

2. **Preserve source information**:
   - Copy exact specification text to `source_specification`
   - Link to publication via PMID or DOI
   - Tag with correct `agent_type`
   - Include molecular_mass if available (shows what MW was used for grounding)
   - Include xref if available (shows how the chemical was verified)
   - Document in `description` how xref relates to identifier choice

3. **Standardize measurements**:
   - Convert all concentrations to molar units when possible
   - Use UO CURIEs for all units
   - Store masses in grams or milligrams

4. **Document discrepancies**:
   - Use `description` field for notes about conflicts
   - Reference source documentation (see `docs/hypho_mp_grounding_and_next_steps.md`)

### Quality Checks

Before committing data changes:

```bash
# Validate KGX compliance
just validate-kgx-custom

# Run integration tests
uv run pytest tests/test_delaney_kgx_validation.py -v

# Check for common issues
grep -E "^[^\t]*\t[^\t]*\t[^\t]*\t[^\t]*$" data/private/static/delaney-media-edges.tsv
```

## Resources

- [KGX Specification](https://github.com/biolink/kgx)
- [Biolink Model](https://biolink.github.io/biolink-model/)
- [Units Ontology](https://www.ebi.ac.uk/ols/ontologies/uo)
- [PROV-O](https://www.w3.org/TR/prov-o/)
- Project documentation: `docs/hypho_mp_grounding_and_next_steps.md`

## Related Files

- **Data**: `data/private/static/delaney-media-{nodes,edges}.tsv` (gitignored)
- **Config**: `config/kgx_validation_config.yaml`
- **Validation**: `src/cmm_ai_automation/scripts/validate_kgx_custom.py`
- **Build**: `project.justfile` (line 193-199: `validate-kgx-custom` target)
- **Source PDFs**: `papers/pone.0062957.s00{5,6}.pdf`
