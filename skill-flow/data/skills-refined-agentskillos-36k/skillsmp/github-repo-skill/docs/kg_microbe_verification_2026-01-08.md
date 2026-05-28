# kg-microbe Verification Notes (2026-01-08)

**Purpose:** Raw evidence from independent verification of kg-microbe data quality claims
**Verified by:** @turbomam with Claude Code assistance
**Repository:** kg-microbe at commit `e2861c4` (2026-01-05)

---

## Summary

This document provides reproducible evidence for claims made in [cmm_vs_kg_microbe.md](cmm_vs_kg_microbe.md) and [kg_microbe_risks.md](kg_microbe_risks.md).

**Key Findings:**
- Some originally cited issues have been fixed (CURIE format, `capable_of` predicate)
- Fundamental issues remain (missing Biolink 3.x fields, unregistered prefixes, wrong provenance format)
- New prefixes like `kgmicrobe.strain:` look better but aren't registered in Bioregistry
- This is "KGX-shaped data" not "KGX-compliant data"

---

## 1. Repository State

```bash
$ cd ~/gitrepos/kg-microbe
$ git log --oneline -5
e2861c4 Merge pull request #479 from Knowledge-Graph-Hub/trembl-fix
201cb9e Replace hardcoded TrEMBL prefix with TREMBL_PREFIX constant
4fe320e Correct misleading comment in Rhea mappings transform
16321e8 Filter out TrEMBL protein nodes from EC ontology transform
43c0db5 Merge pull request #477 from Knowledge-Graph-Hub/ontology-case
```

**Transformed data available:**
```bash
$ ls data/transformed/
bacdive  bactotraits  edge_patterns.tsv  madin_etal  ontologies
```

---

## 2. Node File Headers

### Bacdive, Bactotraits, Madin_etal (identical)

```bash
$ head -1 data/transformed/bacdive/nodes.tsv
id	category	name	description	xref	provided_by	synonym	iri	object	predicate	relation	same_as	subject	subsets
```

**Issue:** Edge-specific columns present in node files:
- `subject` - should only be in edges
- `predicate` - should only be in edges
- `object` - should only be in edges
- `relation` - should only be in edges (also deprecated in Biolink 3.x)

### Ontology Files (cleaner)

```bash
$ head -1 data/transformed/ontologies/ec_nodes.tsv
id	category	name	provided_by	synonym	deprecated	iri	same_as
```

Ontology transforms don't have this schema pollution.

---

## 3. Edge File Headers

### All Sources (identical)

```bash
$ head -1 data/transformed/bacdive/edges.tsv
subject	predicate	object	relation	primary_knowledge_source
```

**Only 5 columns.**

**Missing required Biolink 3.x fields:**
- `knowledge_level` - Required enum indicating how assertion was made
- `agent_type` - Required enum indicating who/what made assertion

**The `relation` field is deprecated** in Biolink 3.x, should use `predicate` only.

---

## 4. Primary Knowledge Source Format

```bash
$ cut -f5 data/transformed/bacdive/edges.tsv | sort -u | head -10
bacdive
bacdive:1
bacdive:10
bacdive:100
bacdive:1000
bacdive:10000
bacdive:100001
bacdive:100002
bacdive:100003
primary_knowledge_source
```

**Issue:** Values are `bacdive` or `bacdive:NUMBER`

**Should be:** `infores:bacdive`

The `infores:` prefix is required per KGX specification. It references the Biolink information-resource-registry where databases are registered with metadata.

---

## 5. CURIE Prefix Analysis

```bash
$ cat data/transformed/*/nodes.tsv | cut -f1 | sed 's/:.*/:/' | sort -u
bacdive.isolation_source:
carbon_substrates:
CAS-RN:
CHEBI:
EC:
envo:
foodon:
GO:
id
KEGG:
kgmicrobe.strain:
mediadive.medium:
METPO:
NCBITaxon:
pathways:
pato:
po:
UBERON:
```

### Bioregistry Registration Status

| Prefix | Bioregistry URL | Status |
|--------|-----------------|--------|
| `kgmicrobe.strain:` | https://bioregistry.io/registry/kgmicrobe.strain | 404 Not Found |
| `kgmicrobe:` | https://bioregistry.io/registry/kgmicrobe | 404 Not Found |
| `bacdive.isolation_source:` | https://bioregistry.io/registry/bacdive.isolation_source | 404 Not Found |
| `carbon_substrates:` | https://bioregistry.io/registry/carbon_substrates | 404 Not Found |
| `pathways:` | https://bioregistry.io/registry/pathways | 404 Not Found |
| `NCBITaxon:` | https://bioregistry.io/registry/ncbitaxon | ✅ Registered |
| `CHEBI:` | https://bioregistry.io/registry/chebi | ✅ Registered |
| `EC:` | https://bioregistry.io/registry/eccode | ✅ Registered |

**Unregistered prefixes cannot:**
- Expand to resolvable URLs
- Be used in standard Bioregistry-aware tools
- Provide durable identifiers

---

## 6. CURIE Format Validation

### Spaces in IDs (Original Issue #430)

```bash
$ cat data/transformed/*/nodes.tsv | cut -f1 | grep " " | wc -l
0
```

**Result:** No spaces found in current node IDs. This appears to be fixed.

### Extra Colons (Original Issue #430)

```bash
$ cat data/transformed/*/nodes.tsv | cut -f1 | grep ":-:" | wc -l
0
```

**Result:** No extra colons found. This appears to be fixed.

---

## 7. Predicate Analysis

### Recent Fix for `capable_of`

```bash
$ git log --oneline --grep="capable_of" -5
19aeb82 Replace biolink:capable_of with METPO:2000103 in BactoTraits and Madin et al transforms
```

**Commit date:** December 2025

**Verification:**
```bash
$ grep "capable_of" data/transformed/*/edges.tsv | wc -l
0
```

**Result:** `biolink:capable_of` has been replaced with METPO predicates. Issue #438 appears addressed.

---

## 8. Recent Positive Changes

From git log (Dec 2025):

| Commit | Description |
|--------|-------------|
| `19aeb82` | Replace biolink:capable_of with METPO:2000103 |
| `f422156` | Refactor growth media category to METPO:1004005 |
| `28d6a9c` | Prioritize METPO predicates and standardize chemical categories |
| `26c029b` | Fix NCBITaxon nodes filename case mismatch |

These show active maintenance and responsiveness to issues.

---

## 9. What "KGX-Shaped" vs "KGX-Compliant" Means

**kg-microbe produces KGX-shaped data:**
- ✅ TSV files with subject/predicate/object
- ✅ Biolink categories on nodes
- ✅ No obviously malformed CURIEs (after recent fixes)
- ❌ Missing required provenance fields
- ❌ Wrong format for knowledge_source
- ❌ Unregistered prefixes
- ❌ Schema pollution (edge columns in node files)

**KGX-compliant data would:**
- ✅ Pass `kgx validate` without errors
- ✅ Have all CURIEs resolvable via Bioregistry
- ✅ Include knowledge_level and agent_type on all edges
- ✅ Use infores: CURIEs for knowledge sources
- ✅ Enable safe merging with other Biolink KGs

---

## 10. Implications for LLM-Generated Analysis

The analysis provided by Marcin checked narrow criteria that pass:
- "Are edge columns populated in node files?" → No (but they exist as headers)
- "Do edges have 5 required columns?" → Yes (but 5 is not enough for Biolink 3.x)

Questions not checked:
- Are prefixes registered in Bioregistry?
- Is primary_knowledge_source using infores: format?
- Are knowledge_level and agent_type present?
- Can `kgx validate` run successfully?

This illustrates how questions can be framed to get passing results while avoiding harder compliance requirements.

---

## 11. Reproducibility

All commands in this document can be run against the kg-microbe repository to verify findings:

```bash
cd ~/gitrepos/kg-microbe
git checkout e2861c4  # or main for latest

# Run verification commands from sections above
```

---

**Document created:** 2026-01-08
**Based on:** kg-microbe commit e2861c4
