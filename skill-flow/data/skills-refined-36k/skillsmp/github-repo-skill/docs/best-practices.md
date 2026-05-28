# Best Practices

This document describes the engineering, data modeling, and community practices followed in cmm-ai-automation. These align with [BBOP/Mungall group standards](https://github.com/berkeleybop/bbop-skills) and represent modern approaches to knowledge graph development.

## Design Principles

### Schema-First Development

All data structures are defined in [LinkML schemas](https://linkml.io/) before writing any code. This ensures:

- **Type safety**: Auto-generated Pydantic models catch errors at development time
- **Documentation**: Schema serves as machine-readable documentation
- **Validation**: Data is validated against schema before storage
- **Interoperability**: Standard formats (JSON-LD, RDF, TSV) generated automatically

```yaml
# src/cmm_ai_automation/schema/cmm_ai_automation.yaml
EnrichedIngredient:
  class_uri: biolink:SmallMolecule
  slots:
    - inchikey           # Structural identity
    - cas_rn             # Registration identity
    - source_records     # Provenance tracking
    - conflicts          # Data conflict documentation
```

**Contrast with legacy approaches**: Imperative code that builds data structures directly without schema validation leads to inconsistent data, undocumented fields, and runtime errors.

### Explicit Source Authoritativeness

Each data source is explicitly designated as authoritative for specific fields:

| Source | Authoritative For | Rationale |
|--------|-------------------|-----------|
| ChEBI | `chebi_id`, biological/chemical roles | OBO Foundry ontology with expert curation |
| CAS Common Chemistry | `cas_rn` | Official registry operator |
| PubChem | `pubchem_cid`, structure data | NIH's authoritative compound database |
| MediaDive | `mediadive_id` | Primary growth media database |

When sources conflict, the authoritative source wins automatically. Conflicts are logged with full provenance for review.

**Contrast with legacy approaches**: Accepting the first or last value encountered, or silently overwriting, leads to data quality issues that are impossible to debug.

### Composite Keys for Entity Resolution

Chemical entities are identified by the `(InChIKey, CAS-RN)` tuple:

```
CSNNHWWHGAXBCP-UHFFFAOYSA-L|7487-88-9  # Magnesium sulfate
WQZGKKKJIJFFOK-GASJEMHNSA-N|50-99-7     # D-glucose
```

- **InChIKey**: What the molecule IS (structural identity)
- **CAS-RN**: How the molecule is NAMED (registration identity)

This resolves ambiguity from synonyms, hydration states, and trivial names.

**Contrast with legacy approaches**: Using string matching on names, or single identifiers, leads to incorrect entity merging (different compounds with same name) or missed merging (same compound with different names).

### Provenance Tracking

Every piece of data records its source:

```python
@dataclass
class SourceRecord:
    source_name: DataSource      # e.g., "chebi", "pubchem"
    source_id: str               # ID returned by that source
    source_query: str            # What we searched for
    source_timestamp: datetime   # When retrieved
    source_fields: list[str]     # Which fields came from this source
```

This enables:
- Audit trails for regulatory compliance
- Debugging data quality issues
- Updating stale data from specific sources

**Contrast with legacy approaches**: "Curated" data with no citations or provenance cannot be verified, updated, or trusted.

## Engineering Practices

### Modern Python Toolchain

| Tool | Purpose | Why |
|------|---------|-----|
| **uv** | Dependency management | Fast, deterministic, replaces pip/poetry/pipenv |
| **ruff** | Linting + formatting | Single fast tool replaces flake8/black/isort |
| **mypy** | Type checking | Catches errors before runtime |
| **pytest** | Testing | Parametrize, fixtures, markers |
| **pre-commit** | Git hooks | Enforce quality on every commit |

**Contrast with legacy approaches**: Using pip with loose requirements, no type checking, and manual style enforcement leads to "works on my machine" problems and inconsistent code quality.

### Test Separation

```python
# Unit tests (fast, no network) - run by default
def test_enriched_ingredient_creation():
    """Test dataclass instantiation."""
    ing = EnrichedIngredient(id="test", name="glucose")
    assert ing.name == "glucose"

# Integration tests (slow, real APIs) - marked and skipped by default
@pytest.mark.integration
def test_chebi_api_glucose():
    """Test real ChEBI API call."""
    client = ChEBIClient()
    result = client.get_compound("CHEBI:17234")
    assert result.name == "D-glucose"
```

Run unit tests: `uv run pytest` (default)
Run integration tests: `uv run pytest -m integration`

**Contrast with legacy approaches**: Mixing unit and integration tests causes slow CI, flaky tests from network issues, and developers avoiding running tests locally.

### CLI Design

CLIs are thin wrappers over library code:

```python
@click.command()
@click.option("-i", "--input", "input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", type=click.Path(), default="-")
@click.option("-f", "--format", "input_format", default="tsv")
def enrich(input_file, output_file, input_format):
    """Enrich ingredients from TSV file."""
    # CLI just handles I/O, delegates to library
    data = load_data(input_file, format=input_format)
    enriched = enrich_ingredients(data)  # Core logic is testable
    write_output(enriched, output_file)
```

Standard options follow [clig](https://clig.dev/) conventions:
- `-i/--input`, `-o/--output` (default stdout)
- `-f/--format`, `-O/--output-format`
- `-v/-vv` for verbosity

**Contrast with legacy approaches**: Putting business logic in CLI functions makes it untestable. Non-standard option names confuse users.

### Identifier Handling

All identifiers use CURIEs (Compact URIs) with proper prefix mapping:

```python
from curies import Converter

converter = Converter.from_prefix_map({
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "CAS": "http://identifiers.org/cas/",
    "PUBCHEM.COMPOUND": "http://identifiers.org/pubchem.compound/",
})

# Expand: CHEBI:17234 -> http://purl.obolibrary.org/obo/CHEBI_17234
# Compress: http://purl.obolibrary.org/obo/CHEBI_17234 -> CHEBI:17234
```

**Contrast with legacy approaches**:
- Mixing URIs and CURIEs inconsistently
- IDs with spaces or extra colons (invalid CURIEs)
- Prefix matching instead of exact matching (CHEBI:17234 matching CHEBI:172340)

## Data Quality Patterns

### Validation Before Storage

```python
def store_enriched_ingredient(ingredient: EnrichedIngredient) -> None:
    # Schema validation via Pydantic
    validated = EnrichedIngredientModel.model_validate(ingredient)

    # Business rule validation
    if validated.chebi_id and not validated.chebi_id.startswith("CHEBI:"):
        raise ValueError(f"Invalid ChEBI ID format: {validated.chebi_id}")

    store.insert(validated)
```

**Contrast with legacy approaches**: Storing whatever comes in and hoping downstream consumers can handle inconsistencies.

### Conflict Detection and Resolution

```python
@dataclass
class DataConflict:
    field_name: str              # Which field has conflict
    primary_source: DataSource   # Authoritative source
    primary_value: str           # Value from authoritative source
    conflicting_source: DataSource
    conflicting_value: str
    resolution: ConflictResolution  # AUTHORITATIVE_WINS, MANUAL_REVIEW, etc.
```

Conflicts are recorded, not silently resolved. This allows:
- Review of potential data quality issues
- Override of automatic resolution when needed
- Audit trails for data decisions

**Contrast with legacy approaches**: Last-write-wins or first-write-wins with no record of what was overwritten.

### Exact Matching for Identifiers

When querying by identifier, use exact matching:

```python
# CORRECT: Exact match
def get_by_chebi_id(chebi_id: str) -> Optional[Ingredient]:
    return collection.find_one({"chebi_id": chebi_id})

# WRONG: Prefix/substring match can return wrong entities
def get_by_chebi_id_broken(chebi_id: str) -> list[Ingredient]:
    # This would match CHEBI:17234, CHEBI:172340, CHEBI:1723499...
    return collection.find({"chebi_id": {"$regex": chebi_id}})
```

**Contrast with legacy approaches**: Using regex or contains() for ID lookups leads to spurious matches (see [CMM-AI#52](https://github.com/CultureBotAI/CMM-AI/issues/52) for a real example where CHEBI:17790 matched CHEBI:177907, CHEBI:177901, etc.).

## AI Integration Guardrails

### Never Commit Unverified AI Output

AI-generated content must be verified before committing:

- Publication DOIs: Verify they resolve
- Chemical identifiers: Verify against authoritative APIs
- Code: Run tests, check for hallucinated imports

**Contrast with legacy approaches**: Committing AI "curated" data without verification leads to hallucinated entries (see [CMM-AI#36](https://github.com/CultureBotAI/CMM-AI/issues/36) for fabricated arXiv/bioRxiv URLs that were committed).

### Structured Prompts with Schema Context

When using AI for data curation, provide schema context:

```python
prompt = f"""
Extract ingredient data from this text. Return JSON matching this schema:

{json.dumps(EnrichedIngredient.model_json_schema(), indent=2)}

Text: {input_text}
"""
```

**Contrast with legacy approaches**: Freeform prompts that produce inconsistent output structures.

### Citation Requirements

Any "curated" data must include citations:

```python
@dataclass
class CuratedIngredient:
    name: str
    cas_rn: str
    source_doi: str       # Required: citation for this data
    curator_notes: str    # Why this mapping was made
```

**Contrast with legacy approaches**: "Curated" data with no source attribution cannot be verified or updated.

## Documentation Standards

### Diataxis Framework

Documentation follows the [Diataxis framework](https://diataxis.fr/):

| Type | Purpose | Example |
|------|---------|---------|
| **Tutorial** | Learning-oriented | "Getting started with ingredient enrichment" |
| **How-to** | Problem-oriented | "How to add a new data source" |
| **Reference** | Information-oriented | API documentation, schema reference |
| **Explanation** | Understanding-oriented | This best practices document |

### Examples as Tests

Code examples in documentation should be tested:

```python
def enrich_ingredient(name: str) -> EnrichedIngredient:
    """Enrich an ingredient by name.

    Example:
        >>> result = enrich_ingredient("glucose")
        >>> result.chebi_id
        'CHEBI:17234'
    """
    # Doctest runs as part of test suite
```

## Community Standards

### Biolink Model Alignment

All entities use [Biolink Model](https://biolink.github.io/biolink-model/) categories:

| Entity | Biolink Category |
|--------|------------------|
| Chemicals | `biolink:SmallMolecule` |
| Organisms | `biolink:OrganismTaxon` |
| Growth media | `biolink:ChemicalMixture` |

### OBO Foundry Ontologies

Use OBO Foundry ontologies for semantic annotation:

- **ChEBI**: Chemical entities
- **NCBITaxon**: Organisms
- **ENVO**: Environments
- **OBI**: Assays and protocols

### KGX Format Compliance

Knowledge graph exports follow [KGX](https://github.com/biolink/kgx) format:

- Valid CURIEs for all identifiers
- Biolink categories and predicates
- Rich edge provenance (knowledge_source, primary_knowledge_source)

**Contrast with legacy approaches**: Custom formats that require format conversion, inconsistent CURIEs (spaces, extra colons), missing provenance (see [kg-microbe#430](https://github.com/Knowledge-Graph-Hub/kg-microbe/issues/430) for examples of invalid CURIEs).

## References

- [SKILL.md](https://github.com/turbomam/cmm-ai-automation/blob/main/SKILL.md) - BBOP github-repo-skill guidelines
- [Architecture](architecture.md) - Technical architecture details
- [LinkML](https://linkml.io/) - Schema language documentation
- [Biolink Model](https://biolink.github.io/biolink-model/) - Standard categories and predicates
- [clig](https://clig.dev/) - CLI design guidelines
- [Diataxis](https://diataxis.fr/) - Documentation framework
