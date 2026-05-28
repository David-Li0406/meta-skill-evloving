# kg-microbe Technical Debt and KGX Compliance Issues

This document captures the technical debt and compliance issues identified in kg-microbe as of January 2026, based on analysis and Slack discussions.

## Overview

Marcin initiated a joint session (Jan 7, 2026) noting:
> "We have some ongoing technical debt in KG-Microbe mostly around KGX compliance perhaps. I am thinking a joint session would be more fun and productive also to learn about the review process since I think there is no actual compliance tool."

The main work is tracked in **kg-microbe PR #485** - Major KGX compliance refactoring.

---

## Critical Issues

### 1. Missing Biolink 3.x Required Columns

**Severity**: HIGH

Biolink 3.x requires 7 edge columns, but kg-microbe only has 5:

| Required Column | Status |
|-----------------|--------|
| subject | Present |
| predicate | Present |
| object | Present |
| knowledge_level | **MISSING** |
| agent_type | **MISSING** |
| category | Present |
| id | Present |

**Verification**:
```bash
head -1 data/transformed/bacdive/edges.tsv | tr '\t' '\n' | wc -l
# Returns 5, should be 7
```

**Fix**: Add `knowledge_level` and `agent_type` columns with appropriate enum values:
- `knowledge_level`: knowledge_assertion, prediction, observation, etc.
- `agent_type`: manual_agent, automated_agent, text_mining_agent, etc.

---

### 2. Invalid CURIE Syntax (5,210 issues in 6.2M rows)

**Severity**: HIGH (for spaces), MEDIUM (for others)

#### Spaces in CURIEs (171 occurrences) - INVALID
```
assay:API_rID32STR_beta GLU     # 61 in node IDs, 109 in edge objects
assay:API_zym_Esterase Lipase C 8
assay:API_zym_Cystine arylamidase
assay:API_zym_Acid phosphatase
```

#### Missing colons in relation column (364 occurrences) - INVALID
```
subPropertyOf    # should be RO:subPropertyOf or similar
inverseOf        # should be RO:inverseOf or similar
```
Note: Only in the deprecated `relation` column.

#### NRRL strain IDs with extra colons (37 occurrences)
```
kgmicrobe.strain:NRRL-:-NRS-341  # double colon
kgmicrobe.strain:NRRL:-NRS-236   # colon in local ID
```
Pattern suggests BacDive data processing issue.

#### Full URLs instead of CURIEs (1,832 occurrences) - Non-critical
```
https://w3id.org/chemrof/charge    # should be chemrof:charge
https://w3id.org/metpo/1000188     # should be METPO:1000188
```
Technically valid but defeats the purpose of CURIEs.

---

### 3. Unregistered Prefixes

**Severity**: MEDIUM

These prefixes return 404 on Bioregistry:

| Prefix | Example | Issue |
|--------|---------|-------|
| `kgmicrobe.strain:` | `kgmicrobe.strain:DSM-1234` | Not registered |
| `mediadive.medium:` | `mediadive.medium:M123` | Not registered |
| `mediadive.solution:` | `mediadive.solution:S456` | Not registered |
| `mediadive.ingredient:` | `mediadive.ingredient:I789` | Not registered |
| `bacdive.isolation_source:` | `bacdive.isolation_source:soil` | Not registered |
| `carbon_substrates:` | `carbon_substrates:glucose` | Not registered |
| `pathways:` | `pathways:glycolysis` | Not registered |
| `cell_shape:` | `cell_shape:rod` | Not registered |
| `assay:` | `assay:API_20A_IND` | Not registered |

**Verification**:
```bash
for prefix in kgmicrobe.strain mediadive.medium mediadive.solution \
  mediadive.ingredient bacdive.isolation_source carbon_substrates \
  pathways cell_shape assay; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://bioregistry.io/registry/$prefix")
  echo "$prefix: $code"
done
# All return 404
```

**Options**:
1. Register prefixes with Bioregistry
2. Use existing registered prefixes where possible
3. Use `infores:` for provenance sources

---

### 4. Edge Columns in Node Files

**Severity**: MEDIUM

Node files contain columns that should only be in edge files:

```bash
head -1 data/transformed/bacdive/nodes.tsv | tr '\t' '\n' | grep -E 'subject|predicate|object|relation'
# Returns 4 lines = 4 columns that shouldn't exist
```

Empty edge columns in node files:
- Bloat file sizes
- Confuse downstream tools
- Wrong by design even if unpopulated

---

### 5. Wrong Provenance Format

**Severity**: MEDIUM

Current: `bacdive:123`
Should be: `infores:bacdive`

The `infores:` prefix is the standard for information resource provenance in Biolink.

---

## Predicate and Category Issues (Being Fixed in PR #485)

### Category Corrections

| Before (Wrong) | After (Correct) | Affected Nodes |
|----------------|-----------------|----------------|
| `biolink:Enzyme` | `biolink:MolecularActivity` | All EC nodes |
| `biolink:ChemicalSubstance` | `biolink:ChemicalEntity` | All generic chemicals |
| `biolink:ChemicalEntity` | `biolink:ChemicalMixture` | 9,916 growth media nodes |

### Predicate Changes

| Before | After | Notes |
|--------|-------|-------|
| `biolink:consumes` | `biolink:has_input` | Semantically correct for enzyme-substrate |
| Generic biolink predicates | METPO predicates | Domain-specific semantics |
| `biolink:capable_of` | `METPO:2000103` | Organism capabilities |
| `biolink:produces` | `METPO:2000202` | 850 production edges |

### Biolink Predicate Deprecations

| Predicate | v3.6.0 | v4.3.3 | v4.3.6 |
|-----------|--------|--------|--------|
| `biolink:assesses` | Active | DEPRECATED | REMOVED |

This broke kg-microbe patterns. Solution: Use METPO predicates like `assesses`, `is_assessed_by`.

---

## METPO Predicate Gaps

Marcin identified that Biolink lacks granularity for microbial traits:

### Missing Predicates (need METPO additions)
- `assesses` / `is_assessed_by` - for assay relationships
- Domain-specific predicates for organism-medium relationships

### Issue #440: `biolink:occurs_in` Used Incorrectly

Current usage:
```
CHEBI:16828 biolink:occurs_in assay:API_20A_IND
```

Problem: Domain/range violation
- `occurs_in` domain: Process
- `occurs_in` range: Material entity or site
- Chemicals cannot "occur in" processes

Correct representation unclear - may need METPO predicate.

---

## Open Issues to Track

### kg-microbe Issues

| Issue | Title | Priority |
|-------|-------|----------|
| [#484](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/484) | Use LPSN data to normalize strain IDs | Medium |
| [#482](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/482) | Remove all `custom_curies.yaml` mappings | High |
| [#480](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/480) | Use synonym mappings from METPO sheet | Medium |
| [#478](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/478) | Ingest LASER db | Low |
| [#474](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/474) | BacDive loses ~22% of phenotype data (arrays bug) | High |
| [#473](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/473) | Integrate BacDive API fetching into kg download | Medium |
| [#458](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/458) | METPO predicates for Madin and BactoTraits | High |
| [#441](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/441) | Comprehensive edge pattern semantic assessment | High |
| [#440](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/440) | `biolink:occurs_in` used incorrectly | High |
| [#439](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/439) | METPO phenotype nodes missing categories | Medium |

### METPO Issues

| Issue | Title | Priority |
|-------|-------|----------|
| [#319](https://github.com/berkeleybop/metpo/issues/319) | Standardize CLI output/logging | Low |
| [#313](https://github.com/berkeleybop/metpo/issues/313) | Sync ChromaDB with ontology changes | Medium |
| [#307](https://github.com/berkeleybop/metpo/issues/307) | Don't use obsolete classes as definition sources | Medium |
| [#306](https://github.com/berkeleybop/metpo/issues/306) | Reconcile aerobic/anaerobic terms | Medium |

---

## What cmm-ai-automation Does Right

This repo implements stricter KGX compliance that kg-microbe should adopt:

### 1. PROV-O Fields on All Edges
```python
class KGXEdge(BaseModel):
    subject: str
    predicate: str
    object: str
    knowledge_level: str      # Required!
    agent_type: str           # Required!
    primary_knowledge_source: Optional[str]
    aggregator_knowledge_source: Optional[List[str]]
    publications: Optional[List[str]]
```

### 2. Custom KGX Validation
- Monkey-patches `PrefixManager.is_curie()` to allow slashes in local parts (for DOIs)
- Injects custom prefixes from `config/kgx_validation_config.yaml`
- Integration tests for DOI/UUID/CURIE validation

### 3. Deterministic Edge IDs
```python
def generate_edge_id(subject: str, predicate: str, object: str) -> str:
    """SHA256-based deterministic edge ID generation."""
    content = f"{subject}|{predicate}|{object}"
    return f"uuid:{hashlib.sha256(content.encode()).hexdigest()[:32]}"
```

### 4. Node Deduplication
```python
def deduplicate_nodes(nodes: List[KGXNode]) -> List[KGXNode]:
    """Merge duplicate nodes by ID with property combination."""
```

---

## Recommended Actions

### For kg-microbe

1. **Add missing columns**: `knowledge_level`, `agent_type` to all edge files
2. **Fix CURIE syntax**: Remove spaces, fix double colons, standardize prefixes
3. **Remove edge columns from nodes**: Clean up node file schema
4. **Register prefixes**: Submit `kgmicrobe.strain`, `mediadive.*` to Bioregistry
5. **Use infores: for provenance**: Replace `bacdive:123` with `infores:bacdive`
6. **Adopt METPO predicates**: Where Biolink is insufficient

### For this repo (cmm-ai-automation)

1. **Export validation tooling**: Make custom validator reusable for kg-microbe
2. **Document CURIE strategy**: Already done in `curie_prefix_strategy.md`
3. **Coordinate with kg-microbe**: Ensure compatible output formats

---

## References

- [Biolink Model 4.3.6](https://biolink.github.io/biolink-model/)
- [KGX Documentation](https://kgx.readthedocs.io/)
- [METPO on BioPortal](https://bioportal.bioontology.org/ontologies/METPO)
- [Bioregistry](https://bioregistry.io/)
- [kg-microbe PR #485](https://github.com/Knowledge-Graph-Hub/kg-microbe/pull/485)

---

*Last updated: 2026-01-14*
*Based on analysis from Slack #kg-microbe-ldrd and #culturebot channels*
