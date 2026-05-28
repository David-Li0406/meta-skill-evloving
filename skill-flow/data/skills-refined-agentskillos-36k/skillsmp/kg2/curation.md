# Data Curation

How to search for papers, collect metadata, and insert data into the knowledge graph.

## Citations vs Claims

| Relation | Level | Meaning | Use Case |
|----------|-------|---------|----------|
| `paper:cites` | Paper → Paper | Bibliographic reference (A lists B in references) | Citation networks, literature review lineage |
| `paper:extends` | Claim → Claim | Conceptual advancement (claim X builds on claim Y) | Research progression, idea genealogy |
| `paper:supports` | Claim → Claim | Evidence relationship (claim X provides evidence for Y) | Validation chains |
| `paper:refutes` | Claim → Claim | Contradiction (claim X contradicts claim Y) | Controversy mapping |

**Key distinction**: `cites` is a factual bibliographic link; claim relations express semantic relationships between ideas. A paper may cite another without any claim relationship (e.g., citing for background), or claims may relate without direct citation (e.g., independent discoveries).

## Concept Relationships

| Relation | Transitivity | Meaning | Use Case |
|----------|--------------|---------|----------|
| `paper:broader` | Transitive | Taxonomic hierarchy (A is-a B) | "neural networks" broader "machine learning" |
| `paper:partOf` | Transitive | Mereological composition (A is component of B) | "attention mechanism" partOf "transformer" |
| `paper:dependsOn` | Not transitive | Prerequisite (understanding A requires B) | "transfer learning" dependsOn "pre-trained models" |

**Key distinctions**:
- `broader`: Taxonomic/is-a relationship. "CNN" is a type of "neural network"
- `partOf`: Compositional/has-a relationship. "Backpropagation" is a component of "neural network training"
- `dependsOn`: Conceptual prerequisite. "Fine-tuning" depends on understanding "pre-trained models"

## Claim-Concept Links

| Relation | Meaning | Use Case |
|----------|---------|----------|
| `paper:regarding` | Claim → Concept | Tag claims with the concepts they address |

Claims can optionally be linked to zero or more concepts via `regarding`. This enables queries like "find all claims about transformers" or "compare claims across concepts". Note that `paper:about` links Papers to Concepts; `paper:regarding` links Claims to Concepts.

## Paper Search APIs

- **Semantic Scholar**: `https://api.semanticscholar.org/graph/v1/paper/search?query=<query>` — includes citations/references
- **OpenAlex**: `https://api.openalex.org/works?search=<query>` — large-scale scholarly data
- **CrossRef**: `https://api.crossref.org/works?query=<query>` — DOI metadata
- **arXiv**: `http://export.arxiv.org/api/query?search_query=<query>` — preprints
- **PubMed**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<query>` — biomedical/life sciences

## Full-text access

- `https://arxiv.org/html/<arxiv-id>` gives you the entire text including references

## Identifier Lookup

- **ORCID**: `https://pub.orcid.org/v3.0/search/?q=<name>`

## Generating URIs

All entities use opaque URIs with random hash:

| Class | Pattern | Example |
|-------|---------|---------|
| Paper | `paper:pa_<8chars>` | `paper:pa_a3f2k9x1` |
| Author | `paper:au_<8chars>` | `paper:au_b7m2p4q8` |
| Claim | `paper:cl_<8chars>` | `paper:cl_n5j8w2y6` |
| Concept | `paper:co_<8chars>` | `paper:co_x9k3m7v2` |
| Venue | `paper:ve_<8chars>` | `paper:ve_k4p9r2w7` |

Generate 8-char random hash:

```bash
LC_ALL=C tr -dc 'a-z0-9' < /dev/urandom | head -c 8
```

## Duplicate Check Before Insert

Before creating a new entity, check if it already exists.

For Paper:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

# By DOI
SELECT ?paper WHERE { ?paper paper:doi "10.1234/example" }

# By arXiv ID
SELECT ?paper WHERE { ?paper paper:arxivId "2401.00001" }
```

If found, update the existing paper instead of creating a duplicate.

For Author:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

# By ORCID
SELECT ?author WHERE { ?author paper:orcidId "0000-0001-1234-5678" }
```

For Concept:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# By Wikidata ID
SELECT ?concept WHERE { ?concept paper:wikidataId "Q12345" }

# By label
SELECT ?concept WHERE { ?concept a paper:Concept ; rdfs:label "Machine Learning" }
```

For Venue:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# By label
SELECT ?venue WHERE { ?venue a paper:Venue ; rdfs:label "NeurIPS" }
```

## Workflow for Rich Connections

Before inserting, search existing entities to maximize graph connectivity:

1. **Venue**: Search by label → reuse if exists. Set `venueType` to one of: `conference`, `journal`, `preprint`, `workshop`
2. **Author**: Search by ORCID → reuse if exists
3. **Concept**: Search by label → reuse if exists, link via `broader`/`partOf`/`dependsOn` to related concepts. Add `rdfs:comment` to describe the concept briefly
4. **Claim**: Search related claims → link via `extends`/`refutes`/`supports`; optionally link via `regarding` to relevant concepts
5. **Citations**: Search papers in reference list by DOI/arXiv ID → link via `cites`

This ensures papers in the same venue, by the same author, on the same topic, with related claims, or citing each other are connected.

### Adding Citations

Use Semantic Scholar API to fetch references (papers this paper cites) and citations (papers citing this paper):

```bash
# Get references (outgoing citations)
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=references.externalIds"

# Get citations (incoming citations)
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=citations.externalIds"
```

For each reference/citation, check if it exists in the graph (by DOI or arXiv ID), then add:

```turtle
paper:pa_citing paper:cites paper:pa_cited .
```

## Inserting Data

```bash
curl -X POST 'https://kg.corca.ai/repositories/kg2/statements' \
  -H 'Content-Type: text/turtle' \
  --data-binary @data.ttl
```

**Important**: All entities must connect to a Paper (SHACL constraint). Author, Claim, and Venue require direct links; Concept must be reachable via `broader` chain from a Paper's `about`. Insert them together in a single request.

**Note**: `primaryAuthor` is a subproperty of `author`. Setting `primaryAuthor` automatically infers `author`—no need to specify both. Multiple primary authors are allowed (e.g., equal-contribution first authors). For co-authors, use `paper:author` directly.

See [data/examples.ttl](data/examples.ttl) for complete examples.

SHACL validation will reject incomplete data (missing `rdfs:label`, `primaryAuthor`, etc.) with HTTP 500.
