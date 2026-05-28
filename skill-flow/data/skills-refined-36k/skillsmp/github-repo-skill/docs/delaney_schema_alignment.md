# Delaney Media: LinkML Schema Alignment & Ontology Mappings

## Overview

This document maps Delaney media data to the repo's LinkML schema and provides ontology-based predicate mappings for edge properties.

## Schema Alignment

### Current KGX Categories → LinkML Classes

| KGX Category (Biolink) | LinkML Schema Class | Notes |
|------------------------|---------------------|-------|
| `biolink:ChemicalEntity` | `Ingredient` | Chemical compounds (CHEBI, PubChem) |
| `biolink:ChemicalMixture` | `Solution` | Stock solutions (e.g., 1000x Vishniac, 10X buffer) |
| `biolink:ComplexMolecularMixture` | `GrowthMedium` | Complete culture media |

✅ **Perfect alignment!** The LinkML schema already has the right classes.

### Node Mappings

#### Chemical Entities (CHEBI compounds)
```yaml
# KGX representation
id: CHEBI:114249
category: biolink:ChemicalEntity
name: Sodium dihydrogen phosphate monohydrate

# LinkML Schema class: Ingredient
Ingredient:
  id: CHEBI:114249
  name: Sodium dihydrogen phosphate monohydrate
  chebi_id: CHEBI:114249
  chemical_formula: NaH2PO4·H2O
  molecular_mass: 137.99
```

#### Solutions (Stock solutions)
```yaml
# KGX representation
id: uuid:9f55f0b7-fe05-4374-a423-380ec2671484
category: biolink:ChemicalMixture
name: 1000x Vishniac solution

# LinkML Schema class: Solution
Solution:
  id: uuid:9f55f0b7-fe05-4374-a423-380ec2671484
  name: 1000x Vishniac solution
  solution_type: trace_element_solution
  has_ingredient_component:
    - ingredient: CHEBI:31440  # CuSO4·5H2O
      concentration_value: 0.001257589593
      concentration_unit: molar
```

#### Media (Complete culture media)
```yaml
# KGX representation
id: doi:10.1371/journal.pone.0062957.s005
category: biolink:ComplexMolecularMixture
name: MP medium from Delaney et al

# LinkML Schema class: GrowthMedium
GrowthMedium:
  id: doi:10.1371/journal.pone.0062957.s005
  name: MP medium from Delaney et al
  source_reference: doi:10.1371/journal.pone.0062957
  medium_type: defined
  ph: 7.0
  has_solution_component:
    - solution: uuid:a8a5a509-ba8c-4ae6-a6d3-98583066c984
      volume_per_liter: 10.0
      volume_unit: milliliter
  has_ingredient_component:
    - ingredient: CHEBI:114249
      concentration_value: 1.88
      concentration_unit: millimolar
```

## Edge Column → Ontology Predicate Mappings

### Core KGX Fields (Already Correct)

| Column | Ontology Predicate | Example Value | Notes |
|--------|-------------------|---------------|-------|
| `subject` | - | `doi:10.1371/journal.pone.0062957.s005` | CURIE (required) |
| `predicate` | - | `biolink:has_part` | Biolink predicate (required) |
| `object` | - | `CHEBI:114249` | CURIE (required) |
| `knowledge_level` | `biolink:knowledge_level` | `knowledge_assertion` | Required for Biolink |
| `agent_type` | `biolink:agent_type` | `manual_agent` | Required for Biolink |

### Quantity/Measurement Fields

| Current Column | Suggested Ontology Predicate | Range | Example | Notes |
|----------------|----------------------------|-------|---------|-------|
| `amount` | `NCIT:C25488` (Amount) | float | `100` | Numeric value |
| `units` | `UO:0000000` (unit) | UO term | `UO:0000098` (milliliter) | Unit ontology term |
| `liters_made` | `cmm:batch_volume` | float | `1` | Volume of batch prepared |
| `concentration_value` | `NCIT:C25488` (Amount) | float | `1.88` | Already in schema! |
| `concentration_unit` | `UO:0000000` (unit) | enum | `millimolar` | Already in schema! |
| `concentration_moles_per_liter` | `cmm:molar_concentration` | float | `0.00188` | Normalized concentration |

### Chemical/Specification Fields

| Current Column | Suggested Ontology Predicate | Range | Example | Notes |
|----------------|----------------------------|-------|---------|-------|
| `raw_specification` | `schema:description` or `cmm:specification_text` | string | `NaH2PO4·H2O` | Free text from source |
| `raw_name` | `schema:alternateName` | string | `sodium citrate` | Common name |
| `raw_molar_mass` | `CHEMINF:000216` (molecular mass) | float | `294.1` | Daltons |
| `chemical_formula` | `CHEMINF:000042` (molecular formula) | string | `Na3C6H5O7·2H2O` | Already in schema! |

### Role/Function Fields

| Current Column | Suggested Ontology Predicate | Range | Example | Notes |
|----------------|----------------------------|-------|---------|-------|
| `raw_role` | `RO:0000087` (has role) | string | `Buffer/Nutrient` | OBO Relations Ontology |
| `roles` | `CHEBI:50906` (role) | enum | `buffer_role` | Already in schema! |

### Metadata Fields

| Current Column | Suggested Ontology Predicate | Range | Example | Notes |
|----------------|----------------------------|-------|---------|-------|
| `comments` | `rdfs:comment` | string | `See wikidata...` | RDFS standard |
| `notes` | `schema:comment` | string | `EDTA disodium...` | Already in schema! |

## Recommended Ontology Predicates by Category

### Units & Measurements (UO - Units Ontology)
```yaml
# Common unit mappings
UO:0000098  # milliliter (mL)
UO:0000099  # liter (L)
UO:0000106  # microliter (µL, uL)
UO:0000063  # millimolar (mM)
UO:0000064  # micromolar (µM, uM)
UO:0000062  # molar (M)
UO:0000021  # gram (g)
UO:0000022  # milligram (mg)
```

### Chemical Information (CHEMINF - Chemical Information Ontology)
```yaml
CHEMINF:000042  # molecular formula descriptor
CHEMINF:000216  # molecular mass descriptor
CHEMINF:000059  # SMILES descriptor
CHEMINF:000113  # InChI descriptor
CHEMINF:000059  # InChIKey descriptor
```

### Relations (RO - Relations Ontology)
```yaml
RO:0002002  # has component (for mixture composition)
RO:0002180  # has specified input (for ingredients in a procedure)
RO:0000087  # has role (for ingredient roles like buffer, nutrient)
BFO:0000051 # has part (alternative to biolink:has_part)
```

### Biological Role (CHEBI - Chemical Entities of Biological Interest)
```yaml
CHEBI:33281  # antimicrobial agent
CHEBI:50906  # role (root term)
CHEBI:24433  # nutrient
CHEBI:35225  # buffer
CHEBI:33893  # metal cofactor
CHEBI:26666  # vitamin
```

## Mapping Strategy: Current → Schema-Aligned

### Option 1: Direct KGX Edge with Edge Properties

**Current approach** - Keep edge properties as extra fields in KGX:

```tsv
subject	predicate	object	knowledge_level	agent_type	amount	units	concentration_moles_per_liter	raw_role
doi:10.1371/journal.pone.0062957.s005	biolink:has_part	CHEBI:114249	knowledge_assertion	manual_agent	25.9	g	0.1876934003	Buffer/Nutrient
```

**Pros:**
- ✅ Simple, minimal transformation
- ✅ All data preserved
- ✅ KGX spec allows extra properties
- ✅ Works with existing tools

**Cons:**
- ❌ Edge properties not semantically mapped
- ❌ Units are strings not ontology terms

### Option 2: Reified Relationships (LinkML Native)

**Recommended** - Use LinkML schema's reified relationship classes:

```yaml
# GrowthMedium with composition
medium:
  id: doi:10.1371/journal.pone.0062957.s005
  name: MP medium from Delaney et al
  has_ingredient_component:
    - ingredient: CHEBI:114249
      concentration_value: 1.88
      concentration_unit: millimolar
      roles: [buffer, nutrient]
      notes: "NaH2PO4·H2O"
```

**Pros:**
- ✅ Fully semantic with ontology terms
- ✅ Matches LinkML schema design
- ✅ Type-safe with enums
- ✅ Queryable structured data

**Cons:**
- ❌ Requires transformation from KGX format
- ❌ More complex to generate

### Option 3: Hybrid Approach (Recommended)

Use KGX for graph exchange, LinkML instances for rich data:

1. **KGX TSV** for knowledge graph operations:
   - Subject-predicate-object triples
   - Minimal edge properties (concentration, role as strings)
   - Biolink compliant

2. **LinkML YAML/JSON** for full data representation:
   - Complete Ingredient/Solution/GrowthMedium instances
   - Typed fields with ontology terms
   - Reified relationships with context

3. **Bidirectional conversion scripts**:
   - KGX → LinkML for enrichment
   - LinkML → KGX for graph export

## Ontology Term Recommendations

### Replace String Units with Ontology Terms

**Before:**
```tsv
amount	units
100	mL
```

**After (LinkML):**
```yaml
volume_per_liter: 100.0
volume_unit: milliliter  # enum → UO:0000098
```

**After (KGX with ontology):**
```tsv
amount	amount_unit	amount_unit_curie
100	milliliter	UO:0000098
```

### Replace Role Strings with CHEBI Terms

**Before:**
```tsv
raw_role
Buffer/Nutrient
```

**After (LinkML):**
```yaml
roles:
  - buffer_role      # → CHEBI:35225
  - nutrient_role    # → CHEBI:24433
```

**After (KGX):**
```tsv
role	role_curie
buffer	CHEBI:35225
```

## Implementation Recommendations

### 1. Add Ontology Columns to KGX Edges (Minimal Change)

Keep current columns, add parallel ontology columns:

```tsv
subject	predicate	object	knowledge_level	agent_type	amount	units	concentration_unit_curie	role	role_curie
doi:10...s005	biolink:has_part	CHEBI:114249	knowledge_assertion	manual_agent	100	mL	UO:0000098	buffer	CHEBI:35225
```

### 2. Create LinkML Instances (Full Semantic)

Generate complete LinkML YAML from your data:

```yaml
ingredients:
  - id: CHEBI:114249
    name: Sodium dihydrogen phosphate monohydrate
    chebi_id: CHEBI:114249
    chemical_formula: NaH2PO4·H2O
    molecular_mass: 137.99

solutions:
  - id: uuid:a8a5a509-ba8c-4ae6-a6d3-98583066c984
    name: 10X P solution for MP medium
    has_ingredient_component:
      - ingredient: CHEBI:114249
        concentration_value: 0.1876934003
        concentration_unit: molar
        notes: "NaH2PO4 22.5 g (or 25.9 g NaH2PO4·H2O)"

media:
  - id: doi:10.1371/journal.pone.0062957.s005
    name: MP medium from Delaney et al
    source_reference: doi:10.1371/journal.pone.0062957
    medium_type: defined
    has_solution_component:
      - solution: uuid:a8a5a509-ba8c-4ae6-a6d3-98583066c984
        volume_per_liter: 10.0
        volume_unit: milliliter
```

### 3. Conversion Scripts

Create bidirectional converters:

```bash
# KGX → LinkML
uv run python -m cmm_ai_automation.scripts.kgx_to_linkml_delaney \
  --nodes data/private/delaney-media-kgx-nodes-fixed.tsv \
  --edges data/private/delaney-media-kgx-edges-fixed.tsv \
  --output data/private/delaney-media.yaml

# LinkML → KGX
uv run python -m cmm_ai_automation.scripts.linkml_to_kgx_delaney \
  --input data/private/delaney-media.yaml \
  --nodes-output output/kgx/delaney-nodes.tsv \
  --edges-output output/kgx/delaney-edges.tsv
```

## Validation Checklist

### KGX Files (Current State)
- [x] Nodes have valid CURIEs
- [x] Nodes have biolink: categories
- [x] Edges have subject/predicate/object
- [x] Edges have knowledge_level
- [x] Edges have agent_type
- [x] All edge objects have nodes
- [ ] Units are ontology terms (optional)
- [ ] Roles are ontology terms (optional)

### LinkML Alignment (Future State)
- [ ] Ingredients map to Ingredient class
- [ ] Solutions map to Solution class
- [ ] Media map to GrowthMedium class
- [ ] Compositions use IngredientComponent
- [ ] Units use LinkML enums
- [ ] Roles use IngredientRole enum
- [ ] All required fields present

## Next Steps

1. **Keep current KGX files working** ✅
   - Already compliant and tested
   - Can be used immediately

2. **Add ontology term columns** (recommended)
   - Parallel columns with CURIEs
   - Backwards compatible
   - Enables semantic queries

3. **Generate LinkML instances** (future)
   - Create proper Ingredient/Solution/GrowthMedium objects
   - Use schema validation
   - Enable richer queries

4. **Create conversion scripts** (future)
   - Automate KGX ↔ LinkML transformations
   - Maintain both representations
   - Use each for its strength
