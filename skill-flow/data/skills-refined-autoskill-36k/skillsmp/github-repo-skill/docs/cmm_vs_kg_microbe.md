# CMM-AI vs kg-microbe: Methods and Outcomes

**Purpose:** Document key differences in approach and resulting data quality between this repository and kg-microbe.

**Date:** 2026-01-07
**Last Verified:** 2026-01-08
**Related Issue:** #123

---

## Executive Summary

While both projects create knowledge graphs for microbial data, cmm-ai-automation prioritizes strict KGX/Biolink compliance, explicit provenance tracking, and schema-driven validation. This leads to higher data quality but requires more upfront modeling work.

> **2026-01-08 Update:** Verification against kg-microbe commit `e2861c4` shows significant recent improvements. Some originally cited issues have been fixed (CURIE format, `capable_of` predicate). Remaining differences documented below with verification status.

---

## 1. Prefix Strategy and CURIE Validity

### kg-microbe Approach

> **Status (2026-01-08):** Surface improvements, but fundamental issues remain

**Current state (verified against commit `e2861c4`):**
- Changed from `strain:bacdive_161512` to `kgmicrobe.strain:161512`
- No spaces found in current CURIE IDs (improvement from #430)
- Uses `mediadive.medium:`, `bacdive.isolation_source:`

**However, these prefixes are NOT registered:**

| Prefix | Bioregistry Status | Resolvable URL? |
|--------|-------------------|-----------------|
| `kgmicrobe.strain:` | ❌ Not found (404) | No |
| `bacdive.isolation_source:` | ❌ Not found | No |
| `carbon_substrates:` | ❌ Not found | No |
| `pathways:` | ❌ Not found | No |

**The identifier lifecycle problem:**
```
BacDive strain 161512
    ↓
kg-microbe transforms to `kgmicrobe.strain:161512`
    ↓
Where does this CURIE resolve to?
    → Not Bioregistry (not registered)
    → Not BacDive directly (different ID scheme)
    → No durable registry tracks these local IDs
    ↓
Result: Looks like a CURIE but doesn't function as one
```

This is "KGX-shaped data" rather than "KGX-compliant data."

### CMM Approach (Long-term Goal)

We aim for **full identifier lifecycle management**:

1. **Use existing registered prefixes when possible:**
   - `NCBITaxon:408` - Bioregistry registered, resolvable
   - `CHEBI:32599` - Bioregistry registered, resolvable
   - `bacdive:161512` - Bioregistry registered, resolves to BacDive page

2. **Register new prefixes before using them:**
   - Submit to Bioregistry with URL pattern
   - Or register with w3id.org for persistent URIs
   - Document the identifier policy

3. **Track local ID assignments durably:**
   - If we mint IDs, maintain a registry
   - Document what each ID refers to
   - Plan for ID deprecation/merging

**Current CMM prefixes:**
- `bacdive.strain:` - Scoped prefix (needs Bioregistry registration - see #53)
- `mediadive.medium:` - Scoped prefix (needs registration)

**Documentation:** See [best-practices.md](best-practices.md) and [#53](https://github.com/turbomam/cmm-ai-automation/issues/53)

**Note:** CMM has the same registration gap as kg-microbe. The difference is we're tracking it as technical debt (#53) rather than considering it resolved.

---

## 2. Schema-Driven vs Ad-hoc Generation

### kg-microbe Approach

- TSV generation via custom Transform classes
- No formal schema validation before export
- Flexibility for rapid iteration

### CMM Approach

- **LinkML schema first**: `src/cmm_ai_automation/schema/cmm_ai_automation.yaml`
- Classes explicitly map to Biolink categories
- Enums with `meaning:` slots for ontology grounding
- Generated Python dataclasses via `gen-pydantic`

**Advantages:**
- Type safety and validation
- Self-documenting data structures
- Easier to detect incompatibilities early

**Documentation:** See [architecture.md](architecture.md)

---

## 3. Biolink Model Compliance

### kg-microbe Issues

> **Status (2026-01-08):** Predicate issue fixed, but provenance fields still missing

**Fixed (credit to kg-microbe team):**
- ✅ `biolink:capable_of` replaced with `METPO:2000103` (commit `19aeb82`, Dec 2025)
- ✅ Growth media category changed to `METPO:1004005` (commit `f422156`)

**Still missing (verified):**

| Required Field | kg-microbe Status | KGX/Biolink Requirement |
|----------------|-------------------|------------------------|
| `knowledge_level` | ❌ Missing | Required enum: `knowledge_assertion`, `prediction`, etc. |
| `agent_type` | ❌ Missing | Required enum: `manual_agent`, `automated_agent`, etc. |
| `primary_knowledge_source` | ⚠️ Wrong format | Uses `bacdive` instead of `infores:bacdive` |

**Current edge schema (all sources):**
```
subject  predicate  object  relation  primary_knowledge_source
```

Only 5 columns. Biolink 3.x requires `knowledge_level` and `agent_type` for proper provenance.

**Sample `primary_knowledge_source` values:**
```
bacdive
bacdive:1
bacdive:10
```

These are not valid `infores:` CURIEs. Should be `infores:bacdive` (registered in Biolink information-resource-registry).

### CMM Approach

- Explicit Biolink category mappings in schema:
  ```yaml
  classes:
    Strain:
      class_uri: biolink:OrganismalEntity
    Taxon:
      class_uri: biolink:OrganismTaxon
    GrowthMedium:
      # Evaluating: ChemicalMixture vs custom METPO class
  ```
- Edge predicates validated against Biolink Model or METPO
- Required provenance fields in edge model:
  ```python
  knowledge_level: Literal["knowledge_assertion", "prediction", ...]
  agent_type: Literal["manual_agent", "automated_agent", ...]
  primary_knowledge_source: list[str]  # Must be infores: CURIEs
  ```
- `kgx validate` target (currently non-blocking during METPO registration - see #91)

**Documentation:** See [#59](https://github.com/turbomam/cmm-ai-automation/issues/59) for alignment strategy

---

## 4. Entity Resolution and Provenance

### kg-microbe Approach

- Generates nodes/edges per source
- Post-merge deduplication via koza
- Limited provenance metadata

### CMM Approach

- **SourceRecord** class tracks which API provided which fields:
  ```yaml
  SourceRecord:
    slots:
      - source_name      # "pubchem", "chebi", "node_normalizer"
      - source_query     # Original query used
      - source_timestamp # When fetched
  ```

- **DataConflict** class records disagreements:
  ```yaml
  DataConflict:
    slots:
      - field_name
      - primary_source
      - primary_value
      - conflicting_source
      - conflicting_value
      - resolution  # enum: KEPT_PRIMARY, USED_CONFLICTING, MANUAL
  ```

**Advantages:**
- Transparent data lineage
- Reproducible enrichment
- Explicit conflict resolution

**Documentation:** See `src/cmm_ai_automation/store/enrichment_store.py`

---

## 5. Media Grounding Quality

### kg-microbe / CMM-AI Approach (from related project)

Analysis of mappings from CultureBotAI/CMM-AI project (which uses kg-microbe as target):

- **Method:** SQL `LIKE '%keyword%'` matching on media names
- **Quality:** 25% of mappings are WRONG due to substring matches
  - "MP" → "LAMPROBACTER" (contains "MP")
  - "MP" → "AMPHIBACILLUS" (contains "MP")

**Documentation:** See [kg_microbe_nodes_analysis.md](kg_microbe_nodes_analysis.md)

### CMM Approach (Planned)

- Structured mapping table with quality metadata:
  ```yaml
  MediaMapping:
    slots:
      - sheet_media_id
      - target_id
      - match_type  # enum: EXACT, VARIANT, CLOSE, WRONG
      - confidence  # 0.0-1.0
      - method      # "manual", "semantic_search", "sql_like"
      - curator     # Who validated it
  ```

- No semicolon-delimited multi-value fields (see #85)
- Explicit tracking of alignment quality (see #84)

---

## 6. Testing and Validation

### kg-microbe

- Has test suite (tox.ini)
- Does NOT run `kgx validate` in CI (see #81)
- Manual validation findings documented in issues

### CMM

- Pytest suite: 426 tests passing
- Pre-commit hooks: mypy, ruff, bandit, linkml-lint, pip-audit
- `kgx validate` target (non-blocking until METPO prefix registered)
- Integration tests marked separately

**Documentation:** See `pyproject.toml` and `.pre-commit-config.yaml`

---

## 7. KGX Field Usage and Provenance

### kg-microbe Field Issues

From kg-microbe#436 (BacDive edges.tsv violations):
- **Empty or inconsistent `relation` values** - unclear when to populate
- **Non-CURIE `primary_knowledge_source`** - violates infores: requirement
- **Missing required provenance** - knowledge_level, agent_type often absent

### CMM Approach: Strict KGX Compliance

**Edge Model** (`src/cmm_ai_automation/transform/kgx.py`):
```python
class KGXEdge(BaseModel):
    # Required fields
    subject: str                              # CURIE
    predicate: str                            # CURIE (biolink: or RO:)
    object: str                               # CURIE
    knowledge_level: Literal[                 # Biolink enum
        "knowledge_assertion",
        "logical_entailment",
        "prediction",
        "statistical_association"
    ]
    agent_type: Literal[                      # Biolink enum
        "manual_agent",
        "automated_agent",
        "computational_model",
        "not_provided"
    ]

    # Provenance (recommended)
    primary_knowledge_source: list[str] | None  # infores: CURIEs
    aggregator_knowledge_source: list[str] | None

    # Optional but useful
    id: str | None                            # Deterministic SHA256 hash
    publications: list[str] | None            # PMID: CURIEs
```

#### CMM Rules

**1. Predicate Selection**

- Use **Biolink predicates** when available:
  - `biolink:in_taxon` for taxonomy relationships
  - `biolink:capable_of` for enzyme/process assertions
  - `biolink:has_part` for composition

- Use **RO predicates** for fine-grained semantics:
  - `RO:0002162` (in taxon) - more specific than biolink
  - `RO:0001019` (contains) for ingredient relationships

- **Never use custom predicates** without Biolink/OBO registration

**2. Relation vs Predicate**

- `predicate` field: REQUIRED, always a CURIE
- `relation` field: DEPRECATED in Biolink 3.0+, do not use
- kg-microbe mixes these inconsistently

**3. Provenance Requirements**

All edges MUST have:
- `knowledge_level`: How was this asserted?
  - `"knowledge_assertion"` - direct database claim
  - `"prediction"` - ML/AI inferred
  - `"statistical_association"` - correlation-based

- `agent_type`: Who/what asserted it?
  - `"manual_agent"` - human curator
  - `"automated_agent"` - script/pipeline

- `primary_knowledge_source`: Where did it originate?
  - MUST use `infores:` prefix
  - Example: `["infores:bacdive"]`, `["infores:mediadive"]`
  - Register at https://github.com/biolink/information-resource-registry

**4. infores: Usage**

The `infores:` namespace identifies **information resources** (databases, APIs):

✅ **CORRECT:**
- `infores:bacdive` - BacDive database
- `infores:ncbi-taxonomy` - NCBI Taxonomy
- `infores:pubchem` - PubChem
- `infores:chebi` - ChEBI

❌ **WRONG:**
- `"BacDive"` - not a CURIE
- `bacdive:7142` - this is a strain ID, not a knowledge source
- `http://bacdive.dsmz.de` - not registered

**Before using a new infores:**, check:
1. Is it registered in the [Biolink information resource registry](https://github.com/biolink/information-resource-registry)?
2. If not, submit a registration PR

**5. Node Provenance**

Nodes use `provided_by` field (not `primary_knowledge_source`):
```python
KGXNode(
    id="NCBITaxon:408",
    category=["biolink:OrganismTaxon"],
    name="Methylorubrum extorquens",
    provided_by=["infores:ncbi-taxonomy"]
)
```

**Deduplication**: When same node from multiple sources, merge `provided_by`:
```python
# Before merge:
Node A: provided_by=["infores:ncbi"]
Node B: provided_by=["infores:bacdive"]

# After merge:
Node: provided_by=["infores:bacdive", "infores:ncbi"]  # sorted
```

**Documentation:**
- [bacdive_kgx_pipeline.md](bacdive_kgx_pipeline.md) - Provenance patterns
- [best_practices_strain_data_curation.md](best_practices_strain_data_curation.md) - CURIE requirements

---

## 8. Custom vs Standard KGX Fields

### kg-microbe Custom Fields

kg-microbe nodes/edges often include non-standard fields without documentation:
- Mixed use of Biolink standard vs custom properties
- Unclear which fields are queryable/meaningful
- No schema definition for validation

### CMM Approach: Lenient But Documented

**Node/Edge models use Pydantic with `extra="allow"`:**
```python
class KGXNode(BaseModel):
    # Required Biolink fields
    id: str
    category: list[str]

    # Optional Biolink fields  
    name: str | None = None
    description: str | None = None
    provided_by: list[str] | None = None
    xref: list[str] | None = None
    synonym: list[str] | None = None
    in_taxon: list[str] | None = None

    model_config = {"extra": "allow"}  # Permits custom fields
```

**Custom fields we add:**
- `type_strain: bool` - Type strain status (microbiology-specific)
- `biosafety_level: int` - Risk group (microbiology-specific)
- `strain_designation: str` - Lab designation (domain-specific)
- `has_genome: list[str]` - Genome assembly CURIEs

**Key difference**: Custom fields are:
1. **Documented** in LinkML schema with descriptions
2. **Typed** with explicit Python type hints
3. **Justified** as domain-specific extensions
4. **Proposed** to Biolink Model when broadly applicable

**Example from schema:**
```yaml
slots:
  type_strain:
    description: "Whether this strain is the nomenclatural type for the species"
    range: boolean
    comments:
      - "Per ICNP (International Code of Nomenclature of Prokaryotes)"
      - "Specific to microbiology, not general Biolink"
```

---

## 9. What True KGX/Biolink Compliance Requires

KGX is not just "nodes and edges in TSV files." It's part of an interoperability ecosystem with specific requirements:

### Identifier Requirements

| Requirement | Description | kg-microbe | CMM Goal |
|-------------|-------------|-----------|----------|
| **Registered prefixes** | All prefixes in Bioregistry or prefix.cc | ❌ `kgmicrobe.strain:` not registered | 🔄 Track in #53 |
| **Resolvable URLs** | CURIEs expand to working URLs | ❌ No expansion defined | 🔄 Plan w3id.org or Bioregistry |
| **Durable ID registry** | Local IDs tracked somewhere permanent | ❌ No registry | 🔄 Need to design |

### Edge Provenance Requirements (Biolink 3.x)

| Field | Purpose | kg-microbe | CMM |
|-------|---------|-----------|-----|
| `knowledge_level` | How assertion was made | ❌ Missing | ✅ In model |
| `agent_type` | Who/what made assertion | ❌ Missing | ✅ In model |
| `primary_knowledge_source` | Origin database | ⚠️ `bacdive` (not `infores:`) | ✅ `infores:` CURIEs |

### The Difference Between "KGX-Shaped" and "KGX-Compliant"

**KGX-Shaped (kg-microbe current state):**
- TSV files with correct column names
- Subject/predicate/object structure
- Looks like KGX but doesn't fully function in ecosystem

**KGX-Compliant (goal):**
- Passes `kgx validate` without errors
- CURIEs resolve to URLs via Bioregistry
- Provenance enables trust assessment
- Can merge safely with other Biolink KGs
- Works with downstream tools (GRAPE, Neo4j, SPARQL)

---

## 10. Documented Gray Zones / Incompatibilities

### kg-microbe Issues Status (Verified 2026-01-08)

| Issue | Original Problem | Current Status |
|-------|-----------------|----------------|
| #430 Invalid CURIEs | Spaces, extra colons | ✅ Fixed in current data (issue still open) |
| #438 Biolink violations | `capable_of` wrong object type | ✅ Fixed (commit `19aeb82`) |
| #436 KGX format | Missing provenance fields | ⚠️ Still missing `knowledge_level`, `agent_type` |
| Prefix registration | Unregistered prefixes | ⚠️ `kgmicrobe.strain:` etc. not in Bioregistry |
| infores: format | Bare strings for knowledge source | ⚠️ Uses `bacdive` not `infores:bacdive` |

### CMM Technical Debt (Honest Assessment)

| Issue | Status | Tracking |
|-------|--------|----------|
| `bacdive.strain:` not registered | ⚠️ Same problem as kg-microbe | #53 |
| `mediadive.medium:` not registered | ⚠️ Same problem | #53 |
| No w3id.org or persistent URIs | 🔄 Not yet addressed | Need new issue |
| Local ID registry | 🔄 Not designed | Need new issue |

### CMM Intentional Divergences

| Design Choice | CMM | kg-microbe | Rationale |
|---|---|---|---|
| Prefix style | `bacdive.strain:12345` | `kgmicrobe.strain:12345` | Neither registered yet |
| Schema | LinkML with Biolink mappings | Ad-hoc Python classes | Type safety, validation, documentation |
| Provenance | `SourceRecord` and `DataConflict` classes | Implicit in file structure | Transparent lineage, conflict resolution |
| Validation | CI + kgx validate | Manual + tox | Catch issues early |
| Entity IDs | Canonical namespace policy (#98) | Post-merge dedup | One ID per entity, explicit policy |
| Technical debt tracking | Explicit issues | Issues filed but may not reflect current code | Transparency |

---

## 11. Community Resources and Getting Help

### The "Too Broken to Test" Problem

A key lesson from kg-microbe: when data deviates too far from standards, the ecosystem tools designed to help identify problems cannot even run. This creates a vicious cycle:

```
Non-compliant data
    ↓
Tools like `kgx validate` fail to parse
    ↓
Can't get specific error counts or locations
    ↓
Don't know where to ask for help
    ↓
Problems accumulate
    ↓
More non-compliant data
```

**CMM strategy:** Stay close enough to compliance that tools work, even if imperfectly. A tool that reports "47 errors of type X" is more actionable than one that crashes.

### Community Resources for Help

| Resource | What They Help With | How to Engage |
|----------|--------------------|--------------|
| **Bioregistry** | Prefix registration, URL patterns | GitHub issues, PRs to add prefixes |
| **Biolink Model** | Category/predicate questions, infores registration | GitHub discussions, Slack |
| **KGX** | Validation errors, format questions | GitHub issues |
| **w3id.org** | Persistent URI registration | GitHub PR to w3id.org repo |
| **OBO Foundry** | Ontology term requests (METPO, etc.) | Ontology-specific trackers |

### Specific Asks We Could Make

1. **Bioregistry:** "We need to register `bacdive.strain` with URL pattern `https://bacdive.dsmz.de/strain/{id}` - is this the right approach for database-specific strain IDs?"

2. **Biolink:** "For microbial cultivation data, what's the recommended category for growth media? We're using METPO but want to ensure compatibility."

3. **KGX:** "We're trying to validate kg-microbe data but getting parse errors on CURIEs. Is there a lenient mode or pre-validation step?"

4. **infores registry:** "We want to register `infores:cmm-ai-automation` as an aggregator knowledge source. What metadata is required?"

---

## 12. Areas of Potential Coordination

Despite differences, there are collaboration opportunities:

1. **MediaDive transform** (#114)
   - Both projects transform MediaDive
   - CMM documents composition model gaps (#111)
   - Could share findings on solution nesting

2. **BacDive data quality**
   - CMM has detailed BacDive JSON schema analysis
   - Could contribute irregular path handling patterns (#69)

3. **METPO term proposals** (#9, #106)
   - Both need cultivation-specific predicates
   - Could jointly propose terms to berkeleybop/metpo

4. **TogoMedium integration** (#75)
   - Neither project fully integrates TogoMedium yet
   - Could share SPARQL patterns

5. **MicroMediaParam mappings** (#19, #22)
   - kg-microbe references MicroMediaParam compound mappings
   - CMM ingredient enrichment (#23) could leverage same data

---

## 13. When to Use Each Approach

### Use kg-microbe When

- Need comprehensive microbial KG quickly
- Willing to accept some data quality issues
- Post-processing pipeline can handle invalid CURIEs
- Flexibility more important than strict validation

### Use CMM When

- Strict KGX/Biolink compliance required
- Need explicit provenance tracking
- Want schema-driven type safety
- Working on CMM-specific (lanthanide/rare earth) research
- Contributing data to Biolink ecosystem

---

## 14. References

### CMM Documentation

- [Architecture](architecture.md)
- [Best Practices](best-practices.md)
- [kg-microbe Nodes Analysis](kg_microbe_nodes_analysis.md)
- [kg-microbe Risks](kg_microbe_risks.md) - Technical debt and FAIR compliance
- [Verification Notes 2026-01-08](kg_microbe_verification_2026-01-08.md) - Raw evidence
- [Session Notes 2025-12-16](session-notes-2025-12-16.md)

### CMM Issues

- #53 - Standardize CURIE prefixes
- #58 - Document modeling differences from kg-microbe
- #59 - Align LinkML schema with kg-microbe patterns
- #67 - Adopt kg-microbe CLI pattern (download/transform/merge)
- #81 - Add KGX validate to CI
- #84 - Track alignment quality
- #85 - Avoid semicolon-delimited multi-value fields
- #91 - METPO prefix registration
- #98 - Canonical namespace policy
- #114 - Coordinate with kg-microbe MediaDive transform

### kg-microbe Issues

- kg-microbe#430 - Invalid CURIEs (spaces, colons)
- kg-microbe#436 - KGX format violations
- kg-microbe#438 - Biolink Model predicate range violations

### External Resources

- [Biolink Model](https://biolink.github.io/biolink-model/)
- [Bioregistry](https://bioregistry.io/)
- [METPO Ontology](https://github.com/berkeleybop/metpo)
- [KGX Documentation](https://github.com/biolink/kgx)

---

## 15. Verification Log

### 2026-01-08 Verification

**Repository:** kg-microbe at commit `e2861c4`

**Method:**
```bash
cd ~/gitrepos/kg-microbe
git log --oneline -1  # e2861c4

# Examined headers
head -1 data/transformed/bacdive/nodes.tsv
head -1 data/transformed/bacdive/edges.tsv

# Checked prefixes
cut -f1 data/transformed/*/nodes.tsv | sed 's/:.*/:/' | sort -u

# Checked primary_knowledge_source values
cut -f5 data/transformed/bacdive/edges.tsv | sort -u | head -10

# Checked Bioregistry for prefix registration
curl -s https://bioregistry.io/registry/kgmicrobe  # 404
curl -s https://bioregistry.io/registry/kgmicrobe.strain  # 404
```

**Findings:**
- Node headers include edge columns (subject, predicate, object, relation)
- Edge files have only 5 columns (missing knowledge_level, agent_type)
- primary_knowledge_source uses `bacdive` not `infores:bacdive`
- Prefixes like `kgmicrobe.strain:` not registered in Bioregistry
- No spaces found in current CURIEs (improvement)
- `capable_of` replaced with METPO predicate (improvement)

---

**Last Updated:** 2026-01-08
**Maintainer:** @turbomam
