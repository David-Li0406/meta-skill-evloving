---
name: kg2
description: Query and manage a research paper knowledge graph. Search papers, add metadata, record claims and relationships (extends, refutes, supports). Use when working with SPARQL, knowledge graphs, papers, claims, citations, or the kg2 repository.
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Academic Paper Knowledge Graph

## How to Edit and Maintain this Document

When asked to edit this and other related documents, please follow these rules:

- Never modify and/or delete "How to Edit and Maintain this Document" section.
- Assume this file is always read before other documents. Do not repeat information from this file in other documents.
- Try to keep the document as concise as possible, especially try to minimize duplicate information.
- Keep this file short, and only include minimum necessary information. Task-specific information should be listed in "Additional resources" section.
- No ASCII art.

## Purpose

A research paper knowledge graph. An agent uses this to answer user questions by:

1. **Search**: Find relevant papers and concepts in the graph
2. **Collect**: If insufficient, search the web for papers and add metadata
3. **Connect**: Record claims and relationships between them (extends, refutes, supports)
4. **Answer**: Provide evidence-based answers from accumulated data

## Goals

- **Simplicity**: Minimum viable schema—only essential classes and properties
- **Correctness**: OWL reasoning and SHACL validation ensure data integrity
- **Practicality**: Focus on metadata that APIs can auto-collect
- **Reasoning**: Enable inference through well-defined relationships

## Non-Goals

- Storing full-text paper content
- Complex claim hierarchy (claims should be simple statements)
- Complete citation network replication (only record meaningful relationships)

## Design Principles

- **Rigor**: Tight OWL constraints, comprehensive SHACL
- **Split by Default**: Without a verified identifier (DOI, ORCID, arXiv ID, Semantic Scholar ID), treat entities as distinct. Merging duplicates later is far easier than splitting incorrectly merged records. This applies to both papers and authors.
- **No Inverse Properties**: Inverse properties (e.g., `claimOf` as inverse of `hasClaim`) are intentionally omitted. They add complexity without benefit—SPARQL can traverse relationships in either direction.

## Technical Notes

- **OWL Reasoner**: Enabled. Constraints like `IrreflexiveProperty` and `AsymmetricProperty` are enforced at reasoning time.
- **OWL/SHACL Division**: Cardinality (`FunctionalProperty`) is enforced by OWL; SHACL handles ranges, constraints, and uniqueness. No duplication between them.

## Agent Guidelines

- When you need to write a file, use `/tmp/` directory. Never pollute the current directory and/or skill directory.

## Endpoints

- **Query**: `https://kg.corca.ai/repositories/kg2` (GET with `query` param, or POST with SPARQL body)
- **Statements**: `https://kg.corca.ai/repositories/kg2/statements` (POST to insert, DELETE to clear)

## Schema

Main prefix: `paper: <https://kg.corca.ai/paper#>`

Core structure:

- **Paper**:
  - `primaryAuthor`/`author` → Author (authorship)
  - `about` → Concept, `hasClaim` → Claim (content)
  - `publishedIn` → Venue (publication)
  - `cites` → Paper (citations)
- **Concept** → `broader`/`partOf`/`dependsOn` → Concept (`broader` and `partOf` are transitive). Use `rdfs:comment` for descriptions.
- **Claim** → `extends`/`refutes`/`supports` → Claim (`extends` is transitive); `regarding` → Concept (optional)
- **Venue** may have `venueType`

**cites vs claim relations**: `cites` is a bibliographic link (paper A lists paper B in references). Claim relations (`extends`/`refutes`/`supports`) express semantic relationships between ideas. A citation may exist without claim relationship (background reference), and claims may relate without citation (independent discoveries).

**concept relations**: `broader` is taxonomic/is-a (CNN → neural network). `partOf` is mereological/component-of (attention mechanism → transformer). `dependsOn` is prerequisite (fine-tuning requires pre-trained models). Both `broader` and `partOf` are transitive; `dependsOn` is not.

URIs are opaque identifiers (`paper:pa_<8chars>`, `paper:au_<8chars>`, `paper:ve_<8chars>`, etc.). Identity is determined by properties (`paper:doi`, `paper:orcidId`), not URIs. See [curation.md](curation.md) for URI generation and data insertion.

## Paper Collection Script

`script/` contains a CLI tool for automated paper collection via citation network snowballing. See [script/README.md](script/README.md) for usage.

## Additional resources

Documentation:

- [query.md](query.md) — SPARQL queries, common patterns
- [curation.md](curation.md) — Paper search APIs, URI generation, data insertion
- [enrichment.md](enrichment.md) — Find opportunities to increase graph connectivity
- [merging.md](merging.md) — Find opportunities to merge duplicate entities
- [admin.md](admin.md) — Repository management (SHACL loading, export/clear, create/delete)

Data:

- [data/schema.ttl](data/schema.ttl) — Full schema definitions
- [data/shacl.ttl](data/shacl.ttl) — SHACL validation rules
- [data/examples.ttl](data/examples.ttl) — Turtle examples
- [data/repo-config.ttl](data/repo-config.ttl) — Repository configuration
