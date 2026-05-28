# Roadmap

This document organizes open issues into prioritized milestones. Updated: 2025-12-20.

## Priority Definitions

| Priority | Definition | Timeline |
|----------|------------|----------|
| **P0** | Critical - blocking core functionality | This week |
| **P1** | High - important for quality/usability | This month |
| **P2** | Medium - nice to have improvements | Next quarter |
| **P3** | Future - research/exploration | When resources allow |

---

## Milestone 1: Core Data Pipeline (P0-P1)

Get the MediaDive → KGX → Neo4j pipeline production-ready.

### P0 - Critical

| Issue | Title | Status |
|-------|-------|--------|
| #104 | Create KGX transforms for MediaDive/TogoMedium media-ingredient relationships | In Progress |
| #91 | Track METPO/CMM prefix registration for KGX compliance | Open |
| #90 | Fix KGX validation errors for growth edges | Open |

### P1 - High Priority

| Issue | Title |
|-------|-------|
| #115 | Add Neo4j loading targets for Google Sheets KGX exports |
| #116 | Add unified Neo4j load-all target |
| #117 | Standardize just target naming for KGX exports |
| #97 | Add MongoDB index for culture collection ID lookups |
| #95 | Add credential validation warnings to Neo4j justfile targets |
| #88 | Avoid Custom_ prefixes - use resolvable CURIEs only |
| #93 | ~~Address Copilot code review comments on export_strains_kgx.py~~ (superseded: script deleted, replaced by strains_kgx_from_curies.py) |

---

## Milestone 2: Documentation & Quality (P1)

Improve documentation and code quality for maintainability.

| Issue | Title | Category |
|-------|-------|----------|
| #107 | Document local MongoDB setup and usage patterns | Documentation |
| #108 | Document ChromaDB indexes and semantic search usage | Documentation |
| #109 | Document blessed external APIs and caching strategy | Documentation |
| #111 | MediaDive KGX: Document medium→solution relationship gap | Documentation |
| #87 | Document media grounding analysis and quality findings | Documentation |
| #86 | Add doctests to core modules | Quality |
| #92 | Include scripts/ in all forms of QA | Quality |
| #80 | Add docstring coverage checking | Quality |
| #81 | Add KGX validate to CI pipeline | Quality |
| #82 | Test on Python 3.11 in addition to 3.12 | Quality |

---

## Milestone 3: Schema & Data Model (P1-P2)

Align schema with standards and improve data modeling.

| Issue | Title | Priority |
|-------|-------|----------|
| #98 | Define canonical namespace policy per entity type | P1 |
| #101 | Refactor Google Sheets to align with LinkML schema | P1 |
| #59 | Align LinkML schema elements with kg-microbe, METPO, and data sources | P1 |
| #77 | Add reconciliation slots to LinkML schema for entity resolution | P2 |
| #76 | ~~Refactor export_strains_kgx.py to use LinkML-generated Strain class~~ (superseded: script deleted, replaced by strains_kgx_from_curies.py) | P2 |
| #79 | Define strain record data completeness requirements | P2 |
| #85 | Avoid semicolon-delimited multi-value fields without metadata | P2 |
| #61 | Add valid and invalid data examples for schema testing | P2 |

---

## Milestone 4: External Integrations (P2)

Integrate additional data sources and external tools.

| Issue | Title |
|-------|-------|
| #103 | Create KGX transforms for BacDive strain relationships |
| #75 | Add TogoMedium as data source for growth media and strain enrichment |
| #106 | Ingest METPO ontology for predicate/relation terms |
| #105 | Decide ChEBI/NCBITaxon ingest scope for KGX |
| #68 | Add TAXRANK ontology download and transform step |
| #89 | Add JSONL export option for KGX output |
| #83 | Add rate limiting to external API calls |

---

## Milestone 5: Entity Resolution & Enrichment (P2)

Improve entity resolution and data enrichment pipelines.

| Issue | Title |
|-------|-------|
| #73 | Implement iterative entity resolution with spider enrichment |
| #70 | Resolve unmapped strains without NCBI or BacDive identifiers |
| #71 | Handle strains/taxa with missing or 'no rank' taxonomic rank |
| #69 | Ensure robust handling of irregular BacDive/MediaDive JSON paths |
| #84 | Track alignment quality for entity mappings |
| #99 | Create grounding verification workflow for data submitters |
| #63 | DuckDB schema evolution: fields not persisting after merge |

---

## Milestone 6: Architecture & Patterns (P2-P3)

Adopt community patterns and improve architecture.

| Issue | Title | Priority |
|-------|-------|----------|
| #67 | Adopt kg-microbe CLI pattern (download/transform/merge) | P2 |
| #114 | Coordinate with kg-microbe MediaDive transform | P2 |
| #112 | Evaluate linkml-map for CMM→KGX schema mapping when stable | P3 |
| #100 | Evaluate alternative input formats beyond Google Sheets | P3 |
| #64 | Reduce dependence on global B110 (try-except-pass) skip in bandit | P2 |

---

## Milestone 7: ML & Advanced Analytics (P3)

Machine learning and graph analytics exploration.

| Issue | Title |
|-------|-------|
| #113 | Evaluate GRAPE/Embiggen for graph ML on CMM knowledge graph |
| #102 | Document ML integration approach with Marcin's methods |
| #66 | Future enrichment sources for strain knowledge graph |

---

## Completed Recently

Track recently completed work to show progress.

| Issue | Title | Completed |
|-------|-------|-----------|
| - | Quick-start guide in README | 2025-12-20 |
| - | Just targets reference documentation | 2025-12-20 |
| - | Pipeline documentation with infrastructure setup | 2025-12-20 |
| #104 | MediaDive KGX export (partial - media, ingredients, solutions, strains) | 2025-12-20 |

---

## How to Use This Roadmap

1. **Find work**: Look at P0/P1 issues in Milestones 1-2
2. **Pick an issue**: Comment "I'll work on this" to claim it
3. **Create a branch**: `git checkout -b {issue-number}-short-description`
4. **Submit PR**: Reference the issue with "Closes #NNN"

## Updating This Roadmap

This roadmap should be updated when:
- New issues are created
- Issues are completed
- Priorities shift based on project needs

Run `gh issue list --state open` to see current issues.
