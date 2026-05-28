# Enrichment

Find where adding data would increase graph connectivity and utility.

Note that `https://arxiv.org/html/<arxiv-id>` gives you the entire text including references.

## Papers With Few Connections

Papers with only required fields (no claims, concepts, or co-authors):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title (COUNT(DISTINCT ?conn) AS ?connections) WHERE {
  ?paper a paper:Paper ; rdfs:label ?title .
  OPTIONAL {
    { ?paper paper:hasClaim ?conn }
    UNION { ?paper paper:about ?conn }
    UNION { ?paper paper:author ?conn . FILTER NOT EXISTS { ?paper paper:primaryAuthor ?conn } }
    UNION { ?paper paper:cites ?conn }
  }
}
GROUP BY ?paper ?title
HAVING (COUNT(DISTINCT ?conn) < 2)
ORDER BY ?connections
LIMIT 50
```

## Isolated Claims

Claims not connected to other claims (no extends/refutes/supports):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?claim ?label ?paper ?paperTitle WHERE {
  ?claim a paper:Claim ; rdfs:label ?label .
  ?paper paper:hasClaim ?claim ; rdfs:label ?paperTitle .
  FILTER NOT EXISTS { ?claim paper:extends|paper:refutes|paper:supports ?other }
  FILTER NOT EXISTS { ?other paper:extends|paper:refutes|paper:supports ?claim }
}
LIMIT 50
```

## Missing Identifiers

Entities without external identifiers (harder to verify or deduplicate):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?type ?entity ?label WHERE {
  VALUES (?type ?class ?idProp) {
    ("Paper" paper:Paper paper:doi)
    ("Author" paper:Author paper:orcidId)
    ("Concept" paper:Concept paper:wikidataId)
  }
  ?entity a ?class ; rdfs:label ?label .
  FILTER NOT EXISTS { ?entity ?idProp ?id }
}
ORDER BY ?type ?label
LIMIT 50
```

## Papers Without Citations

Papers not citing any other papers (unusual for research papers):

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title ?year WHERE {
  ?paper a paper:Paper ; rdfs:label ?title .
  OPTIONAL { ?paper paper:year ?year }
  FILTER NOT EXISTS { ?paper paper:cites ?cited }
}
ORDER BY DESC(?year)
LIMIT 50
```

## Papers Without Venue

Papers missing publication venue information:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title ?year WHERE {
  ?paper a paper:Paper ; rdfs:label ?title .
  OPTIONAL { ?paper paper:year ?year }
  FILTER NOT EXISTS { ?paper paper:publishedIn ?venue }
}
ORDER BY DESC(?year)
LIMIT 50
```

## Isolated Field Pairs

Pairs of root concepts with no claim connections between their papers. Adding interdisciplinary papers here would reduce graph diameter:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?root1 ?label1 ?root2 ?label2 WHERE {
  ?root1 a paper:Concept ; rdfs:label ?label1 .
  ?root2 a paper:Concept ; rdfs:label ?label2 .
  FILTER(?root1 < ?root2)
  FILTER NOT EXISTS { ?root1 paper:broader ?p1 }
  FILTER NOT EXISTS { ?root2 paper:broader ?p2 }
  ?paper1 paper:about/paper:broader* ?root1 .
  ?paper2 paper:about/paper:broader* ?root2 .
  FILTER NOT EXISTS {
    ?paper1 paper:hasClaim ?c1 .
    ?paper2 paper:hasClaim ?c2 .
    { ?c1 paper:extends|paper:refutes|paper:supports ?c2 }
    UNION { ?c2 paper:extends|paper:refutes|paper:supports ?c1 }
  }
}
LIMIT 50
```

## Bridge Papers

Papers covering multiple root concepts. Natural candidates for connecting isolated fields:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title (GROUP_CONCAT(DISTINCT ?rootLabel; separator=", ") AS ?fields) WHERE {
  ?paper a paper:Paper ; rdfs:label ?title ; paper:about ?concept .
  ?concept paper:broader* ?root .
  ?root rdfs:label ?rootLabel .
  FILTER NOT EXISTS { ?root paper:broader ?parent }
}
GROUP BY ?paper ?title
HAVING (COUNT(DISTINCT ?root) > 1)
ORDER BY DESC(COUNT(DISTINCT ?root))
LIMIT 50
```
