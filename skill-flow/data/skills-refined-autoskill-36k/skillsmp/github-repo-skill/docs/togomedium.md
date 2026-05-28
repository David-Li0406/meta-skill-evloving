# TogoMedium Integration for CMM

TogoMedium is a comprehensive knowledge base of microbial culture media maintained by DBCLS (Database Center for Life Science) in Japan. This document summarizes its relevance to the Critical Mineral Metabolism (CMM) project.

## Overview

- **URL**: https://togomedium.org/
- **SPARQL Endpoint**: https://togomedium.org/sparql
- **REST API**: https://togomedium.org/sparqlist/api/
- **Ontology**: Growth Medium Ontology (GMO) - http://purl.jp/bio/10/gmo/
- **GitHub**: https://github.com/dbcls/medium-db (source code only, no data dumps)

## Data Statistics

| Class | Count | Description |
|-------|------:|-------------|
| NCBI Taxon | 223,586 | Taxonomy entries |
| SIO Organism | 81,130 | Organism/strain instances |
| PROV Entity | 56,466 | Provenance records |
| GMO Component | 50,202 | Ingredient definitions |
| GMO Ingredient Usage | 31,541 | Ingredient-in-medium links |
| GTDB Taxon | 18,385 | GTDB taxonomy |
| GMO Comment | 9,607 | Recipe comments/notes |
| **GMO Medium** | **2,917** | Culture media |
| Pathway | 425 | Metabolic pathways |

## Data Sources

TogoMedium aggregates media from multiple biological resource centers:

- **JCM** (RIKEN BioResource Center) - 1,376 media
- **NBRC** (NITE Biological Resource Center) - 749 media
- **Manual collection** - 709 media from research papers

## Relevance to CMM

### Media Coverage

TogoMedium contains several media used in CMM methylotroph research:

| CMM Media | TogoMedium ID | TogoMedium Name | Notes |
|-----------|---------------|-----------------|-------|
| LB | M2476, M443 | LB (Luria-Bertani) Medium/Agar | Not in MediaDive |
| NMS | M1871 | Nitrate mineral salts medium (NMS) | Complete medium (MediaDive only has stock) |
| R2A | M1376, M1235 | R2A Agar variants | Also in MediaDive |
| PYG | M695 | PYG Medium | Similar to MPYG |

### Media NOT in TogoMedium

- AMS (Ammonium mineral salts) - only in MediaDive as stock solution
- DSMZ:88 (SM medium for Paracoccus)
- ATCC:1306 (PIPES minimal with methanol)
- Hypho medium - unique to AM-1 lab
- MP medium (PIPES-buffered methylotroph minimal)

### Cross-References

TogoMedium provides links to external databases:

- **ChEBI** - Chemical Entities of Biological Interest
- **PubChem** - Chemical compound IDs
- **NCBI Taxonomy** - 223K taxon links
- **GTDB** - Genome Taxonomy Database (18K entries)
- **MediaDive** - via `rdfs:seeAlso` to ingredient URLs

## Growth Medium Ontology (GMO)

The GMO ontology defines the structure for media data:

### Key Classes

| Class ID | Label | Description |
|----------|-------|-------------|
| GMO_000001 | Medium | Culture medium |
| GMO_000002 | Component | Media ingredient |
| GMO_000003 | Defined medium | Chemically defined medium |
| GMO_000004 | Undefined medium | Complex medium |

### Key Properties

- `gmo:has_component` - Links medium to ingredients
- `gmo:has_role` - Ingredient role (carbon source, nitrogen source, etc.)
- `gmo:has_property` - Ingredient properties (organic, inorganic, etc.)

### Ontology Files

- **BioPortal**: https://bioportal.bioontology.org/ontologies/GMO
- **Local copy**: `data/ontologies/gmo.owl` (614KB, version 0.24 Beta)
- **Last updated**: August 28, 2024

## Data Access Methods

### REST API (SPARQList)

Pre-built endpoints for common queries:

```bash
# List all media (paginated)
curl "https://togomedium.org/sparqlist/api/list_media?limit=100&offset=0"

# Get medium details by ID
curl "https://togomedium.org/sparqlist/api/gmdb_medium_by_gmid?gm_id=M443"

# List components
curl "https://togomedium.org/sparqlist/api/list_components"

# List organisms
curl "https://togomedium.org/sparqlist/api/list_organisms"
```

### SPARQL Queries

Direct triplestore access for custom queries:

```sparql
# Count media by source
SELECT ?source (COUNT(?medium) AS ?count) WHERE {
  ?medium a <http://purl.jp/bio/10/gmo/GMO_000001> ;
          <http://purl.org/dc/terms/identifier> ?id .
  BIND(STRBEFORE(?id, "_") AS ?source)
}
GROUP BY ?source
ORDER BY DESC(?count)

# Find media containing specific ingredient
SELECT ?medium ?mediumName WHERE {
  ?medium a <http://purl.jp/bio/10/gmo/GMO_000001> ;
          rdfs:label ?mediumName ;
          <http://purl.jp/bio/10/gmo/has_component> ?usage .
  ?usage <http://purl.jp/bio/10/gmo/gmo_id> ?comp .
  ?comp rdfs:label ?compName .
  FILTER(CONTAINS(LCASE(?compName), "methanol"))
}

# Get cross-references for a medium
SELECT ?medium ?xref WHERE {
  ?medium a <http://purl.jp/bio/10/gmo/GMO_000001> ;
          rdfs:seeAlso ?xref .
}
```

## Local Data Infrastructure

**Note**: We previously maintained a local ChromaDB index and cache of TogoMedium data, but these were removed because:

1. TogoMedium only provides media names and IDs, not composition data
2. The semantic search wasn't effective for grounding custom lab media (MP, Hypho)
3. MediaDive provides better coverage with actual ingredient lists

For TogoMedium data, use the REST API or SPARQL endpoint directly (see "Data Access Methods" above).

## Integration with Other Data Sources

### MediaDive Comparison

| Feature | MediaDive | TogoMedium |
|---------|-----------|------------|
| Media count | 5,842 | 2,917 |
| Ingredient count | 1,234 | 50,202 |
| Strain associations | 47,264 | 81,130 organisms |
| Has LB medium | No | Yes |
| Has NMS medium | Stock only | Complete |
| API type | MongoDB | SPARQL + REST |
| Data format | JSON | RDF |

### kg-microbe Integration

TogoMedium media IDs (e.g., M443) are distinct from kg-microbe medium IDs (e.g., J511). Cross-walking requires:

1. Name-based matching via ChromaDB fuzzy search
2. Ingredient composition comparison
3. Manual curation for ambiguous cases

### Recommended Grounding Priority

1. **TogoMedium** - For LB, NMS, standard media with good cross-references
2. **MediaDive** - For MPYG, R2A, and media with strain associations
3. **kg-microbe** - For existing graph integration (J511, etc.)
4. **Manual definition** - For lab-specific media (Hypho, MP, ATCC:1306)

## Future Work

### Full RDF Dump

Create a SPARQL-based dumper to extract:
- All media with complete ingredient lists
- Cross-references to external databases
- Organism-media cultivation relationships

### Ingredient Alignment

Map TogoMedium GMO components to:
- ChEBI ontology terms
- PubChem CIDs
- MediaDive ingredient IDs

### Graph Integration

Add TogoMedium data to CMM knowledge graph:
- `Medium` nodes with TogoMedium IDs
- `hasIngredient` edges to chemical entities
- `cultivatedIn` edges from organisms to media

## References

- TogoMedium: https://togomedium.org/
- TogoMedium About: https://togomedium.org/about/
- GMO on BioPortal: https://bioportal.bioontology.org/ontologies/GMO
- DBCLS: https://dbcls.rois.ac.jp/
- Growth Medium Ontology paper: (not yet published)
