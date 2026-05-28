# Delaney Media KGX/Biolink Compliance Guide

## Overview

This document describes how to ensure Delaney media data files follow KGX (Knowledge Graph Exchange) and Biolink Model standards.

## What is KGX/Biolink Compliance?

**KGX** is a standard format for exchanging knowledge graphs. **Biolink Model** is a high-level data model for biological and biomedical knowledge graphs.

### Required Standards

**For Nodes (data entities):**
- Must have `id` (CURIE format: `prefix:local_id`)
- Must have `category` (from Biolink Model, e.g., `biolink:ChemicalEntity`)
- Category must use lowercase `biolink:` prefix
- Should have `name` for human readability

**For Edges (relationships):**
- Must have `subject` (CURIE of source node)
- Must have `predicate` (Biolink predicate, e.g., `biolink:has_part`)
- Must have `object` (CURIE of target node)
- Must have `knowledge_level` (e.g., `knowledge_assertion`)
- Must have `agent_type` (e.g., `manual_agent`)
- All edge objects must have corresponding nodes

## Your Data Model

### Chemical Entities
- **Category**: `biolink:ChemicalEntity`
- **Identifiers**: CHEBI (preferred) or PubChem
- **Examples**: `CHEBI:114249`, `pubchem.compound:16217523`

### Solutions (Chemical Mixtures)
- **Category**: `biolink:ChemicalMixture`
- **Identifiers**: UUID (temporary) or DOI (preferred)
- **Examples**: `uuid:1953b3d6-1112-48a6-8572-04fa3eafb4e6`

### Media (Complex Mixtures)
- **Category**: `biolink:ComplexMolecularMixture`
- **Identifiers**: DOI (from journal articles) or UUID (temporary)
- **Examples**: `doi:10.1371/journal.pone.0062957.s005`

### Relationships
- **Predicate**: `biolink:has_part`
- Media can have solutions or chemical entities as parts
- Solutions can have chemical entities as parts

## Validation and Fixing

### Validate Current Files

Check if your files are compliant:

```bash
uv run python -m cmm_ai_automation.scripts.validate_fix_delaney_kgx --validate-only
```

### Fix Issues Automatically

Generate compliant fixed files:

```bash
uv run python -m cmm_ai_automation.scripts.validate_fix_delaney_kgx
```

This creates:
- `data/private/delaney-media-kgx-nodes-fixed.tsv`
- `data/private/delaney-media-kgx-edges-fixed.tsv`

### Run Compliance Tests

Verify compliance with comprehensive tests:

```bash
uv run pytest tests/test_delaney_kgx_validation.py -v
```

All 14 tests should pass:
- ✅ Node structure validation
- ✅ Edge structure validation
- ✅ Category capitalization
- ✅ CURIE format validation
- ✅ Required fields present
- ✅ All edge objects have nodes
- ✅ Valid knowledge_level and agent_type values

## Common Issues and Solutions

### Issue 1: Category Capitalization

**Problem**: `Biolink:ComplexMolecularMixture` (incorrect)

**Solution**: `biolink:ComplexMolecularMixture` (correct - lowercase prefix)

### Issue 2: Missing Required Edge Fields

**Problem**: Edges without `knowledge_level` and `agent_type`

**Solution**: Add these fields:
- `knowledge_level`: Use `knowledge_assertion` for manually curated data
- `agent_type`: Use `manual_agent` for manually entered data

### Issue 3: Missing Nodes for Edge Objects

**Problem**: Edge points to `CHEBI:114249` but no node exists for it

**Solution**: Create a node:
```tsv
id	category	name
CHEBI:114249	biolink:ChemicalEntity	Sodium dihydrogen phosphate monohydrate
```

## Maintaining Compliance

### When Adding New Data

1. **Nodes**: Ensure all nodes have:
   - Valid CURIE id
   - Lowercase `biolink:` category
   - Human-readable name

2. **Edges**: Ensure all edges have:
   - Valid subject/object CURIEs
   - `biolink:` predicate
   - `knowledge_level` = `knowledge_assertion`
   - `agent_type` = `manual_agent`

3. **Validate**: Run validation script after changes

4. **Test**: Run pytest tests to ensure compliance

### Automated Validation in CI

Add to your GitHub Actions workflow:

```yaml
- name: Validate KGX files
  run: |
    uv run python -m cmm_ai_automation.scripts.validate_fix_delaney_kgx --validate-only
    uv run pytest tests/test_delaney_kgx_validation.py
```

## KGX Field Reference

### Node Fields

| Field | Required | Example | Description |
|-------|----------|---------|-------------|
| `id` | ✅ Yes | `CHEBI:114249` | Unique CURIE identifier |
| `category` | ✅ Yes | `biolink:ChemicalEntity` | Biolink category (list) |
| `name` | ⚠️ Recommended | `Sodium phosphate` | Human-readable name |
| `description` | Optional | `A sodium salt...` | Detailed description |
| `xref` | Optional | `pubchem.compound:123` | Cross-references |
| `synonym` | Optional | `NaH2PO4` | Alternative names |

### Edge Fields

| Field | Required | Example | Description |
|-------|----------|---------|-------------|
| `subject` | ✅ Yes | `uuid:abc123` | Source node CURIE |
| `predicate` | ✅ Yes | `biolink:has_part` | Biolink predicate |
| `object` | ✅ Yes | `CHEBI:114249` | Target node CURIE |
| `knowledge_level` | ✅ Yes | `knowledge_assertion` | Type of knowledge |
| `agent_type` | ✅ Yes | `manual_agent` | Source of assertion |
| `publications` | Optional | `PMID:12345` | Supporting publications |
| `primary_knowledge_source` | Optional | `infores:delaney2013` | Original source |

### Valid knowledge_level Values

- `knowledge_assertion` - Manually curated facts (use this for your data)
- `logical_entailment` - Inferred by reasoning
- `prediction` - Computational prediction
- `statistical_association` - From statistical analysis
- `observation` - Direct observation
- `not_provided` - Unknown

### Valid agent_type Values

- `manual_agent` - Human curator (use this for your data)
- `automated_agent` - Fully automated system
- `data_analysis_pipeline` - Data processing pipeline
- `computational_model` - Computational model prediction
- `text_mining_agent` - Text mining system
- `manual_validation_of_automated_agent` - Human-verified automated result
- `not_provided` - Unknown

## Resources

- [KGX Specification](https://github.com/biolink/kgx)
- [Biolink Model](https://biolink.github.io/biolink-model/)
- [KGX Format Guide](https://github.com/biolink/kgx/blob/master/specification/kgx-format.md)
- [Biolink Category Hierarchy](https://biolink.github.io/biolink-model/NamedThing/)
- [Biolink Predicate Hierarchy](https://biolink.github.io/biolink-model/related_to/)

## Example: Creating a New Medium

```tsv
# nodes file
id	category	name
doi:10.1234/journal.001	biolink:ComplexMolecularMixture	My Custom Medium
uuid:solution-abc	biolink:ChemicalMixture	10X Buffer Solution
CHEBI:15377	biolink:ChemicalEntity	Water

# edges file
subject	predicate	object	knowledge_level	agent_type	amount	units
doi:10.1234/journal.001	biolink:has_part	uuid:solution-abc	knowledge_assertion	manual_agent	100	mL
doi:10.1234/journal.001	biolink:has_part	CHEBI:15377	knowledge_assertion	manual_agent	900	mL
uuid:solution-abc	biolink:has_part	CHEBI:15377	knowledge_assertion	manual_agent	1	L
```

## Troubleshooting

### Validation Fails with "Category capitalization error"

**Fix**: Change `Biolink:` to `biolink:` (lowercase)

### Validation Fails with "Missing required field: knowledge_level"

**Fix**: Add `knowledge_level	knowledge_assertion` to edge

### Validation Fails with "Missing required field: agent_type"

**Fix**: Add `agent_type	manual_agent` to edge

### Test Fails with "edge objects don't have nodes"

**Fix**: Create nodes for all CHEBIs, UUIDs, DOIs used as edge objects

## Getting Help

1. Run validation: `uv run python -m cmm_ai_automation.scripts.validate_fix_delaney_kgx --validate-only`
2. Check error messages - they tell you exactly what's wrong
3. Use auto-fix to generate compliant files
4. Run tests to verify: `uv run pytest tests/test_delaney_kgx_validation.py`
