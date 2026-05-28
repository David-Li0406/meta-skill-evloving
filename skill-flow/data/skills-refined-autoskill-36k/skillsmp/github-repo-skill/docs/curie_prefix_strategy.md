# CURIE and Prefix Strategy

**Date:** 2026-01-08
**Status:** Planning document - needs community input
**Related Issues:** #53, #98

---

## The Problem

We need to create CURIEs for many entity types. Some come from databases with their own IDs, some are entities we identify from literature. Creating and registering many prefixes is burdensome, but too few prefixes creates ambiguity.

**Constraints:**
- Marcin (reasonably) doesn't want to register dozens of prefixes
- We want numerical local IDs, not semantic mnemonics
- CURIEs should ideally resolve to something useful
- Different databases have different entity types (media, strains, solutions, ingredients)

---

## Entity Types Inventory

### From External Databases (Have Their Own IDs)

| Source | Entity Types | Their ID Format | Current Approach |
|--------|--------------|-----------------|------------------|
| **BacDive** | strains | Numeric (161512) | `bacdive:161512` works - registered! |
| **MediaDive** | media, solutions, ingredients, strains | Numeric + letters (104c, J562) | Unregistered `mediadive.medium:` etc. |
| **TogoMedium** | media, components | M443, SY85 | `togomedium:` ? |
| **NCBI** | taxa, genomes, biosamples | Numeric | `NCBITaxon:`, `insdc.sra:` - registered |
| **ChEBI** | chemicals | Numeric | `CHEBI:` - registered |
| **PubChem** | compounds | Numeric (CID) | `pubchem.compound:` - registered |

### Entities We May Need to Mint IDs For

| Entity Type | Source | Example | Notes |
|-------------|--------|---------|-------|
| Growth conditions | Literature | "37°C, pH 7, aerobic" | Combinations not in any database |
| Experimental observations | Our curation | "Strain X grows on medium Y" | The assertion itself |
| Literature-described media | Papers | "Modified MP medium from Smith 2019" | Not in MediaDive |
| Unmapped strains | Sheets | Lab designations like "AM1" | Need canonical ID |
| CMM-specific phenotypes | Our work | "High REE accumulation" | Domain-specific |

---

## Prefix Strategy Options

### Option 1: Many Type-Specific Prefixes

```
mediadive.medium:104c
mediadive.solution:S123
mediadive.ingredient:I456
mediadive.strain:7890
```

**Pros:**
- Type is unambiguous from CURIE alone
- Can have different URL patterns per type

**Cons:**
- Many prefixes to register (Marcin's concern)
- Registration overhead
- Maintenance burden

### Option 2: Single Database Prefix + Typed Local IDs

```
mediadive:medium_104c
mediadive:solution_S123
mediadive:ingredient_I456
mediadive:strain_7890
```

**Pros:**
- Only one prefix to register per database
- Type encoded in local ID
- URL pattern: `https://mediadive.dsmz.de/{local_id}` could route internally

**Cons:**
- Less "pure" CURIE semantics
- Local ID is no longer just the database's ID
- Relies on database having unified resolver

### Option 3: Single Database Prefix + Numeric IDs (Let Database Resolve)

```
mediadive:104c     → https://mediadive.dsmz.de/104c (let them figure out type)
mediadive:S123     → https://mediadive.dsmz.de/S123
bacdive:161512     → https://bacdive.dsmz.de/strain/161512 (they know it's a strain)
```

**Pros:**
- Simplest - one prefix per database
- Database handles type resolution
- Matches how `bacdive:` already works

**Cons:**
- Requires database to have unified resolver
- Type not visible in CURIE
- May not work for all databases

### Option 4: Project Prefix for Minted IDs + Database Prefixes for External

```
# External database entities - use their prefix
bacdive:161512
mediadive:104c
NCBITaxon:408

# Entities we mint - use project prefix with numeric IDs
cmm:1         → growth condition
cmm:2         → experimental observation
cmm:3         → literature-described medium
```

**Pros:**
- Clear separation: external vs minted
- Only need to register ONE new prefix (cmm:)
- Numeric IDs are stable, not semantic

**Cons:**
- `cmm:1` doesn't tell you it's a growth condition
- Need metadata/registry to know what each ID refers to
- Resolver needs to handle all types

### Option 5: Hybrid - Project Prefix with Type Codes

```
# External - use registered database prefixes
bacdive:161512
CHEBI:32599

# Minted - project prefix + type code + number
cmm:GC0001    → Growth Condition #1
cmm:OB0001    → Observation #1
cmm:LM0001    → Literature Medium #1
cmm:ST0001    → Strain (unmapped) #1
```

**Pros:**
- Single prefix to register
- Type visible in local ID
- Numeric portion is stable

**Cons:**
- Type codes are semantic (but short)
- Need to define and document codes
- Still need registry of what each ID means

---

## Questions for Community

### For Bioregistry

1. "We're building a microbial knowledge graph. MediaDive has media, solutions, ingredients, and strains - all with different ID formats. Should we register:
   - One `mediadive:` prefix that resolves all entity types?
   - Separate `mediadive.medium:`, `mediadive.solution:`, etc.?
   - Something else?"

2. "For entities we mint ourselves (growth conditions, observations), what's the recommended pattern? A single project prefix with typed local IDs?"

3. "What's the minimum viable registration? Can we start with a GitHub-hosted prefix map and formalize later?"

### For Biolink/KGX

1. "When we have assertions like 'strain X grows on medium Y at 37°C', should the growth condition be a node? An edge property? A reified statement?"

2. "For literature-described entities not in any database, what category should they have?"

### For w3id.org

1. "Can we register a `w3id.org/cmm/` namespace that routes to our GitHub Pages, so our minted IDs are resolvable even before formal Bioregistry registration?"

---

## Two Different Problems: Terms vs Instances

**Critical distinction:**

| Type | What It Is | Namespace | Examples |
|------|------------|-----------|----------|
| **Ontology terms** (T-box) | Classes, predicates, categories | METPO, Biolink, OBO ontologies | `METPO:1004005` (the class "Growth Medium") |
| **Instance data** (A-box) | Specific strains, media, experiments | Database prefixes, project prefix | `bacdive:161512` (a specific strain) |

**METPO is for terms, NOT instances.** You can't use `METPO:` to identify a specific strain from BacDive or a specific medium from MediaDive.

---

## METPO for Domain-Specific Terms

METPO provides a registered namespace for microbial phenotype ontology terms:

| Aspect | METPO Status | Notes |
|--------|--------------|-------|
| Prefix registered? | ✅ Yes (`METPO:`) | In OBO/Bioregistry |
| URL resolvable? | ✅ Yes | Via OBO PURLs |
| Formal local ID registry? | ❌ No | But has BioPortal dumps, code to analyze |
| Governance | Informal | BBOP team, responsive to requests |

**What METPO gives us:**
- Registered prefix for ontology terms
- Can create new classes/predicates relatively quickly
- Terms become part of a shared vocabulary
- Resolvable URIs via OBO infrastructure

**What we do for METPO local IDs:**
- Code analyzes old sheets and BioPortal dumps (location: TBD - @turbomam has this)
- Track what IDs exist, avoid collisions
- Informal but functional
- Can be agile about creating new terms for small categories

### Using METPO for CMM Categories and Predicates

For domain-specific **categories** (node types) and **predicates** (edge types) that don't fit Biolink:

| CMM Concept | Type | Potential METPO Term | Notes |
|-------------|------|---------------------|-------|
| Growth medium (category) | Class | `METPO:1004005` | Already exists |
| "grows in" (predicate) | Property | `METPO:2000517` | Already exists |
| Growth condition (category) | Class | `METPO:XXXXXXX` | Could propose |
| "optimal pH" (predicate) | Property | `METPO:XXXXXXX` | Could propose |

**METPO does NOT solve:** Identifying specific instances (strains, media, experiments) from external databases.

---

## The Instance ID Problem (Still Unsolved)

For actual instance data, we still need:

| Instance Type | Source | Prefix Needed |
|---------------|--------|---------------|
| BacDive strains | BacDive database | `bacdive:` ✅ registered |
| MediaDive media | MediaDive database | `mediadive:` ❌ not registered |
| TogoMedium media | TogoMedium database | `togomedium:` ❌ not registered |
| Literature-described media | Our curation | `cmm:` ❌ not registered |
| Growth conditions | Our curation | `cmm:` ❌ not registered |
| Experimental observations | Our curation | `cmm:` ❌ not registered |

**This is the real prefix registration burden** - not ontology terms (we have METPO), but instance identifiers from databases and our own minted entities.

---

## Proposed Strategy (Draft)

### Phase 1: Use What's Registered

| Entity Type | Prefix | Status |
|-------------|--------|--------|
| BacDive strains | `bacdive:` | ✅ Registered |
| NCBI taxa | `NCBITaxon:` | ✅ Registered |
| ChEBI chemicals | `CHEBI:` | ✅ Registered |
| PubChem compounds | `pubchem.compound:` | ✅ Registered |

### Phase 2: Register Database Prefixes

| Database | Proposed Prefix | URL Pattern | Action Needed |
|----------|-----------------|-------------|---------------|
| MediaDive | `mediadive:` | `https://mediadive.dsmz.de/{id}` | Check if they have unified resolver |
| TogoMedium | `togomedium:` | `http://togomedium.org/{id}` | Research their ID scheme |

### Phase 3: Register Project Prefix for Minted IDs

| Prefix | Purpose | URL Pattern |
|--------|---------|-------------|
| `cmm:` | Entities we mint | `https://w3id.org/cmm/{id}` → GitHub Pages registry |

### Local ID Format for `cmm:`

**Option A: Pure Numeric**
```
cmm:1, cmm:2, cmm:3, ...
```
Requires separate registry to know what each is.

**Option B: Type-Prefixed Numeric**
```
cmm:GC0001  (Growth Condition)
cmm:OB0001  (Observation)
cmm:LM0001  (Literature Medium)
```
Type visible, still mostly numeric.

**Recommendation:** Option B - minimal semantic content, but enough to route/categorize.

---

## Registry Requirements

If we mint IDs, we need a registry that tracks:

```yaml
# Example: cmm_id_registry.yaml
cmm:GC0001:
  type: GrowthCondition
  label: "Standard methylotroph conditions"
  temperature_celsius: 30
  ph: 7.0
  oxygen: aerobic
  created: 2026-01-08
  created_by: turbomam

cmm:LM0001:
  type: LiteratureMedium
  label: "Modified MP medium (Smith 2019)"
  source: PMID:12345678
  based_on: mediadive:104c
  modifications: "Added 0.1% yeast extract"
  created: 2026-01-08
```

This could be:
- YAML/JSON in the repo (version controlled)
- MongoDB collection (queryable)
- Both (YAML as source of truth, loaded into MongoDB)

---

## Research Findings

### MediaDive URL Structure (Verified 2026-01-08)

MediaDive does NOT have a unified resolver. URLs are type-specific:

| Entity Type | URL Pattern | Example |
|-------------|-------------|---------|
| Media | `https://mediadive.dsmz.de/medium/{id}` | `/medium/104c` |
| Solutions | `https://mediadive.dsmz.de/solutions/{id}` | `/solutions/179` |
| Ingredients | `https://mediadive.dsmz.de/ingredients/{id}` | `/ingredients/124` |
| Strains | `https://mediadive.dsmz.de/strains/medium/{id}` | `/strains/medium/104c` |

**Implication:** A single `mediadive:104c` prefix cannot resolve because the URL needs the entity type.

**Options:**
1. Register type-specific prefixes: `mediadive.medium:104c` → `https://mediadive.dsmz.de/medium/104c`
2. Include type in local ID: `mediadive:medium/104c` → `https://mediadive.dsmz.de/medium/104c`
3. Ask MediaDive to add a unified resolver that redirects based on ID format

Option 2 is interesting because then we only need ONE prefix but include the type in the local ID. The CURIE `mediadive:medium/104c` expands to the correct URL.

**Bioregistry status:** `mediadive` is NOT registered (404 on lookup).

### BacDive URL Structure (Comparison)

BacDive DOES have a unified resolver:
- `bacdive:161512` → `https://bacdive.dsmz.de/strain/161512`

They automatically add `/strain/` because all BacDive IDs are strains. This is why `bacdive:` works with a single prefix.

### TogoMedium URL Structure (from docs/togomedium.md)

TogoMedium uses a consistent ID scheme for media:
- Media IDs: M443, M2476, M1871 (prefixed with M)
- Component IDs: Different scheme
- Organism IDs: Different scheme

**API access:**
```
https://togomedium.org/sparqlist/api/gmdb_medium_by_gmid?gm_id=M443
```

**Bioregistry status:** `togomedium` is NOT registered (404 on lookup).

**Implication:** Could potentially use a single `togomedium:` prefix since media IDs start with "M", components with different prefix, etc. But need to verify if their ID scheme is truly unique per entity type.

---

## Identifier Registry Landscape

### Registries to Consider

| Registry | Purpose | Relationship |
|----------|---------|--------------|
| [Bioregistry](https://bioregistry.io) | Meta-registry aggregating from many sources | **Primary** - imports from OBO, prefix.cc, Identifiers.org |
| [OBO Foundry](https://obofoundry.org) | Ontology registry (T-box terms) | Bioregistry imports OBO prefixes |
| [Identifiers.org](https://identifiers.org) | Life science identifier resolution (MIRIAM) | Bioregistry imports from it |
| [prefix.cc](https://prefix.cc) | Community prefix registry | Bioregistry imports from it |
| [w3id.org](https://w3id.org) | **Persistent URI redirect service** | Different - provides resolution, not cataloging |
| [N2T.net](https://n2t.net) | ARK/EZID identifier resolution | Separate infrastructure |

**Key insight:** Bioregistry is a meta-registry. If a prefix is in OBO Foundry, prefix.cc, or Identifiers.org, it's likely already in Bioregistry.

**w3id.org is different:** It's a redirect service (register `w3id.org/cmm/` → your GitHub Pages), not a semantic registry.

### Project Prefix Status (Verified 2026-01-08)

| Prefix | Bioregistry | Identifiers.org | OBO Foundry | Notes |
|--------|-------------|-----------------|-------------|-------|
| `cmm` | ❌ 404 | ❌ 404 | ❌ 404 | Available |
| `cmm-ai` | ❌ Not checked | - | - | Likely available |
| `ber-cmm-ai` | ❌ Not checked | - | - | Clearly scoped to project |

**Note:** `cmo` (Clinical Measurement Ontology) IS registered - similar but different.

### Prefix Naming Trade-offs

**Short prefix (`cmm:`):**
- Pro: Concise CURIEs, easy to type
- Con: "CMM" is generic (Capability Maturity Model, etc.), harder to claim ownership

**Long prefix (`ber-cmm-ai:` or `cmm-ai:`):**
- Pro: Clearly scoped, unlikely to conflict, matches repo names
- Con: Verbose CURIEs

**Recommendation:** Lean toward `cmm-ai:` - matches repository naming, distinguishes from generic CMM uses.

---

## Custom Prefixes in Use (Audit 2026-01-08)

### kg-microbe Constants (`constants.py`)

| Prefix | Bioregistry | Notes |
|--------|-------------|-------|
| `kgmicrobe.strain:` | ❌ Not registered | For strains not in BacDive |
| `mediadive.medium:` | ❌ Not registered | MediaDive media |
| `mediadive.solution:` | ❌ Not registered | MediaDive solutions |
| `mediadive.ingredient:` | ❌ Not registered | MediaDive ingredients |
| `mediadive.medium-type:` | ❌ Not registered | Complex vs defined |
| `bacdive.isolation_source:` | ❌ Not registered | Isolation source categories |
| `cell_shape:` | ❌ Not registered | Cell morphology |
| `pathways:` | ❌ Not registered | Metabolic pathways |
| `carbon_substrates:` | ❌ Not registered | Carbon source utilization |
| `assay:` | ❌ Not registered | Assay types |
| `debio:` | ❌ Not registered | Debio ontology |
| `BSL:` | ❌ Not registered | Biosafety levels |
| `taxonomy_id:` | ❌ Not registered | Taxonomy identifiers |

### Registered Prefixes (for comparison)

| Prefix | Bioregistry | Notes |
|--------|-------------|-------|
| `bacdive:` | ✅ Registered | BacDive strains |
| `NCBITaxon:` | ✅ Registered | NCBI taxonomy |
| `CHEBI:` | ✅ Registered | ChEBI chemicals |
| `GO:` | ✅ Registered | Gene Ontology |
| `KEGG:` | ✅ Registered | KEGG |
| `RHEA:` | ✅ Registered | Rhea reactions |
| `METPO:` | ✅ Registered | Microbial phenotype ontology |
| `EC:` | ✅ Registered | Enzyme Commission |
| `PubChem:` | ✅ Registered | PubChem compounds |
| `CAS-RN:` | ✅ Registered | CAS Registry Numbers |

### CMM-AI Data Usage

Found in `CMM-AI/data/`:
- `kgmicrobe.medium:` (e.g., `kgmicrobe.medium:ATCC_1306`)
- `mediadive.medium:` (e.g., `mediadive.medium:632`)

### Observations

1. **13+ unregistered prefixes** in active use in kg-microbe
2. Most follow `database.entity_type:` convention
3. None resolve to URLs via Bioregistry
4. Some are very domain-specific (`cell_shape:`, `carbon_substrates:`)
5. The `kgmicrobe.*` prefixes are project-specific but not registered

---

## Action Items

- [x] Research MediaDive's resolver - **No unified resolver, URLs are type-specific**
- [x] Research TogoMedium's ID scheme - **IDs prefixed by type (M for media), may enable single prefix**
- [x] Check if `cmm` is registered - **Not registered as of 2026-01-08**
- [x] Audit custom prefixes in kg-microbe, CMM-AI, cmm-ai-automation
- [ ] Decide on project prefix name (`cmm-ai:` vs `ber-cmm-ai:` vs other)
- [ ] Draft Bioregistry issue asking about prefix strategy for type-specific resolvers
- [ ] Decide on local ID format for minted entities
- [ ] Design registry schema for minted IDs
- [ ] Register w3id.org/cmm-ai/ namespace (low barrier)
- [ ] Consider asking MediaDive to add unified resolver
- [ ] Verify TogoMedium ID uniqueness across entity types
- [ ] Prioritize which unregistered prefixes to formalize

---

## References

- [Bioregistry](https://bioregistry.io/) - Prefix registration
- [w3id.org](https://w3id.org/) - Persistent URI service
- [Biolink information-resource-registry](https://github.com/biolink/information-resource-registry) - infores: registration
- Issue #53 - Standardize CURIE prefixes
- Issue #98 - Canonical namespace policy
