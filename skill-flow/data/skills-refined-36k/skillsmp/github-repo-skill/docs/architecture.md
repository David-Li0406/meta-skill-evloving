# CMM AI Automation Architecture

This document describes the architectural principles and community tools used in the CMM AI Automation project for ingredient enrichment and knowledge graph generation.

## Design Principles

### 1. Entity Resolution via Composite Keys

The primary challenge in ingredient data integration is entity resolution - determining when records from different sources refer to the same chemical entity.

We use a **composite primary key** based on the `(InChIKey, CAS-RN)` tuple:

```
Key format: {inchikey}|{cas_rn}
Examples:
  CSNNHWWHGAXBCP-UHFFFAOYSA-L|7487-88-9  # Magnesium sulfate
  WQZGKKKJIJFFOK-GASJEMHNSA-N|50-99-7     # D-glucose
```

**Rationale:**
- InChIKey provides structural identity (what the molecule IS)
- CAS-RN provides registration identity (how the molecule is NAMED in commerce)
- Together they resolve most ambiguity from synonyms, hydration states, etc.

When one identifier is missing, we generate a UUID placeholder to maintain unique keys.

### 2. Source Authoritativeness

Each data source is considered **authoritative** for its own identifier type:

| Source | Authoritative For |
|--------|------------------|
| PubChem | `pubchem_cid` |
| ChEBI | `chebi_id`, biological/chemical roles |
| CAS Common Chemistry | `cas_rn` |
| MediaDive | `mediadive_id` |
| KEGG | `kegg_id` |

**Conflict Resolution Rules:**
1. If an authoritative source provides a value, that value wins
2. Non-authoritative conflicts are logged but don't block processing
3. Manual review can override automatic resolution

### 3. Iterative Spidering Enrichment

The enrichment process works iteratively, starting from whatever identifiers are available:

```
Input: ingredient name or partial identifiers
  │
  ▼
┌─────────────────┐
│ NodeNormalization│ ─── Bridge identifiers across databases
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ ChEBI 2.0 API   │ ─── Get ChEBI ID, roles, structure
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ PubChem         │ ─── Get PubChem CID, synonyms, structure
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ MediaDive       │ ─── Get growth media context
└─────────────────┘
  │
  ▼
Output: EnrichedIngredient with all available data
```

Each step may discover new identifiers that enable queries to additional sources.

## Community Tools

### LinkML Stack

We use the [LinkML](https://linkml.io/) ecosystem for schema-driven data management:

- **linkml-runtime**: Python dataclasses from LinkML schema
- **linkml-store**: Data persistence with DuckDB/MongoDB backends
- **LinkML schemas**: Define `EnrichedIngredient`, `SourceRecord`, `DataConflict` classes

**Why LinkML?**
- Schema-first design ensures data quality
- Generated Python classes provide type safety
- DuckDB backend enables SQL queries on enriched data
- Part of the BBOP/OBO ecosystem

### KGX (Knowledge Graph Exchange)

[KGX](https://github.com/biolink/kgx) is the standard for knowledge graph interchange in the Translator ecosystem:

```python
from kgx.graph.nx_graph import NxGraph
from kgx.sink.tsv_sink import TsvSink

# Build graph programmatically
graph = NxGraph()
graph.add_node(
    "CHEBI:32599",
    name="magnesium sulfate",
    category=["biolink:SmallMolecule"],
    xref=["CAS:7487-88-9", "PUBCHEM.COMPOUND:24083"],
    provided_by=["cmm-ai-automation"],
)

# Export using TsvSink
sink = TsvSink(owner=None, filename="output/cmm", format="tsv")
for node_id, data in graph.nodes(data=True):
    sink.write_node({"id": node_id, **data})
sink.finalize()
```

**Why KGX?**
- Standard TSV format for nodes/edges
- Compatible with KG-Microbe and other KG-Hub projects
- Supports Biolink Model categories and predicates
- Rich edge properties (knowledge_source, primary_knowledge_source, etc.)

### Biolink Model

All entities use [Biolink Model](https://biolink.github.io/biolink-model/) categories:

| Entity Type | Biolink Category |
|-------------|------------------|
| Chemicals/Ingredients | `biolink:SmallMolecule` |
| Organisms/Taxa | `biolink:OrganismTaxon` |
| Growth Media | `biolink:ChemicalMixture` |
| Solutions | `biolink:ChemicalMixture` |

Relationships use Biolink predicates:
- `biolink:has_part` - medium contains ingredient
- `biolink:occurs_in` - organism grows in medium
- `biolink:same_as` - cross-reference equivalence

### NCATS Translator NodeNormalization

The [NodeNormalization API](https://nodenormalization-sri.renci.org/) bridges identifiers across databases:

```python
# Query with any identifier
response = node_norm.get_normalized_nodes(["CHEBI:17634"])

# Returns equivalents from multiple databases
{
    "CHEBI:17634": {
        "id": {"identifier": "CHEBI:17634"},
        "equivalent_identifiers": [
            {"identifier": "PUBCHEM.COMPOUND:5793"},
            {"identifier": "CAS:50-99-7"},
            ...
        ]
    }
}
```

## API Clients

### ChEBI 2.0 REST API

The new ChEBI 2.0 backend API (launched October 2025) provides much richer data than the legacy SOAP service:

```python
from cmm_ai_automation.clients.chebi import ChEBIClient

client = ChEBIClient()
result = client.get_compound("CHEBI:17634")

# Access roles, synonyms, cross-references
roles = result.get_biological_roles()
cas_numbers = result.get_cas_numbers()
```

### MediaDive MongoDB

Local MongoDB mirror of MediaDive ingredient catalog:

```python
from cmm_ai_automation.clients.mediadive_mongodb import MediaDiveMongoClient

client = MediaDiveMongoClient()
results = client.search_ingredients_by_name("glucose")
```

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    Google Sheets (CMM Data)                   │
│  ingredients_tab | solutions_tab | media_tab | strains_tab   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    download-sheets CLI                        │
│           Export TSV files to data/private/                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 enrich-ingredients CLI                        │
│  - Parse ingredient names from TSV                            │
│  - Query NodeNormalization, ChEBI, PubChem, MediaDive         │
│  - Resolve entities via (InChIKey, CAS-RN) keys               │
│  - Log conflicts with source tracking                         │
│  - Store in linkml-store (DuckDB)                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    export_to_kgx()                            │
│  - Create KGX NxGraph with biolink categories                 │
│  - Write nodes/edges via TsvSink                              │
│  - Include rich edge properties (knowledge_source, etc.)      │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    KGX TSV Output                             │
│  cmm_nodes.tsv | cmm_edges.tsv                                │
│  Compatible with KG-Microbe merge pipeline                    │
└──────────────────────────────────────────────────────────────┘
```

## CURIE Prefix Map

All CURIEs (Compact URIs) in this project expand to full URIs according to `prefix_map.json` in the repository root. This follows [bioregistry](https://bioregistry.io/) conventions.

Key prefix expansions:

| Prefix | URI Base |
|--------|----------|
| `CHEBI` | `http://purl.obolibrary.org/obo/CHEBI_` |
| `NCBITaxon` | `http://purl.obolibrary.org/obo/NCBITaxon_` |
| `PUBCHEM.COMPOUND` | `http://identifiers.org/pubchem.compound/` |
| `CAS` | `http://identifiers.org/cas/` |
| `INCHIKEY` | `http://identifiers.org/inchikey/` |

Example: `CHEBI:17634` expands to `http://purl.obolibrary.org/obo/CHEBI_17634`

The full prefix map is used by the enrichment pipeline and KGX export to ensure consistent URI generation.

## Related Resources

- [Bioregistry](https://bioregistry.io/) - Community prefix registry
- [KG-Microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) - Microbial knowledge graph
- [METPO](https://github.com/berkeleybop/metpo) - Microbial Phenotype Ontology
- [Biolink Model](https://biolink.github.io/biolink-model/) - Standard for biological knowledge graphs
- [linkml-store](https://linkml.io/linkml-store/) - AI-ready data management
- [ChEBI](https://www.ebi.ac.uk/chebi/) - Chemical Entities of Biological Interest
