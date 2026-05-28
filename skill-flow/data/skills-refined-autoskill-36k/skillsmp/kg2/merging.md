# Merging

Find entities created separately due to Split by Default principle that may be the same. Be very conservative when merging. You must be absolutely sure that the entities are the same. Search the web to collect evidence. If you are not sure, do not merge.

## Merge Candidates

### Authors With Same Name

Different author URIs with identical labels. Excludes co-authors on the same paper (likely different people):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?a1 ?a2 ?label WHERE {
  ?a1 a paper:Author ; rdfs:label ?label .
  ?a2 a paper:Author ; rdfs:label ?label .
  FILTER(?a1 < ?a2)
  FILTER NOT EXISTS { ?a1 paper:orcidId ?id1 }
  FILTER NOT EXISTS { ?a2 paper:orcidId ?id2 }
  FILTER NOT EXISTS { ?paper paper:author ?a1, ?a2 }
}
LIMIT 50
```

### Authors in Same Field

Same name authors publishing in the same concept area (higher merge probability):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?a1 ?a2 ?label ?sharedConcept WHERE {
  ?a1 a paper:Author ; rdfs:label ?label .
  ?a2 a paper:Author ; rdfs:label ?label .
  FILTER(?a1 < ?a2)
  FILTER NOT EXISTS { ?a1 paper:orcidId ?id1 }
  FILTER NOT EXISTS { ?a2 paper:orcidId ?id2 }
  FILTER NOT EXISTS { ?paper paper:author ?a1, ?a2 }
  ?p1 paper:author ?a1 ; paper:about ?sharedConcept .
  ?p2 paper:author ?a2 ; paper:about ?sharedConcept .
}
LIMIT 50
```

### Concepts With Same Label

Different concept URIs with identical labels. Excludes concepts used together in the same paper (likely different meanings):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?c1 ?c2 ?label WHERE {
  ?c1 a paper:Concept ; rdfs:label ?label .
  ?c2 a paper:Concept ; rdfs:label ?label .
  FILTER(?c1 < ?c2)
  FILTER NOT EXISTS { ?c1 paper:wikidataId ?id1 }
  FILTER NOT EXISTS { ?c2 paper:wikidataId ?id2 }
  FILTER NOT EXISTS { ?paper paper:about ?c1, ?c2 }
}
LIMIT 50
```

### Papers With Same Title

Different paper URIs with identical titles (same year increases merge probability):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?p1 ?p2 ?title ?year1 ?year2 WHERE {
  ?p1 a paper:Paper ; rdfs:label ?title .
  ?p2 a paper:Paper ; rdfs:label ?title .
  FILTER(?p1 < ?p2)
  FILTER NOT EXISTS { ?p1 paper:doi ?d1 }
  FILTER NOT EXISTS { ?p2 paper:doi ?d2 }
  OPTIONAL { ?p1 paper:year ?year1 }
  OPTIONAL { ?p2 paper:year ?year2 }
}
LIMIT 50
```

### Venues With Same Label

Different venue URIs with identical labels:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?v1 ?v2 ?label WHERE {
  ?v1 a paper:Venue ; rdfs:label ?label .
  ?v2 a paper:Venue ; rdfs:label ?label .
  FILTER(?v1 < ?v2)
}
LIMIT 50
```

## Performing Merges

After confirming a merge, update references and delete duplicate.

### Merge Authors

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

DELETE { ?paper paper:author <duplicate> }
INSERT { ?paper paper:author <canonical> }
WHERE { ?paper paper:author <duplicate> } ;

DELETE { ?paper paper:primaryAuthor <duplicate> }
INSERT { ?paper paper:primaryAuthor <canonical> }
WHERE { ?paper paper:primaryAuthor <duplicate> } ;

DELETE WHERE { <duplicate> ?p ?o }
```

### Merge Concepts

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

DELETE { ?paper paper:about <duplicate> }
INSERT { ?paper paper:about <canonical> }
WHERE { ?paper paper:about <duplicate> } ;

DELETE { ?child paper:broader <duplicate> }
INSERT { ?child paper:broader <canonical> }
WHERE { ?child paper:broader <duplicate> } ;

DELETE { <duplicate> paper:broader ?parent }
INSERT { <canonical> paper:broader ?parent }
WHERE { <duplicate> paper:broader ?parent } ;

DELETE WHERE { <duplicate> ?p ?o }
```

### Merge Venues

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

DELETE { ?paper paper:publishedIn <duplicate> }
INSERT { ?paper paper:publishedIn <canonical> }
WHERE { ?paper paper:publishedIn <duplicate> } ;

DELETE WHERE { <duplicate> ?p ?o }
```

### Merge Papers

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>

# Transfer outgoing citations
DELETE { <duplicate> paper:cites ?cited }
INSERT { <canonical> paper:cites ?cited }
WHERE { <duplicate> paper:cites ?cited } ;

# Transfer incoming citations
DELETE { ?citing paper:cites <duplicate> }
INSERT { ?citing paper:cites <canonical> }
WHERE { ?citing paper:cites <duplicate> } ;

DELETE WHERE { <duplicate> ?p ?o }
```
