# Querying

How to query the knowledge graph using SPARQL.

## Query Patterns

### Concept Hierarchy (broader transitivity)

Find papers about a concept or any of its narrower concepts:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?paper ?title ?concept WHERE {
  ?paper a paper:Paper ; rdfs:label ?title ; paper:about ?concept .
  ?concept paper:broader* paper:co_m1n2o3p4 .
}
LIMIT 100
```

### Concept Composition (partOf transitivity)

Find all components of a concept:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?component ?label WHERE {
  ?component paper:partOf+ paper:co_transformer .
  ?component rdfs:label ?label .
}
LIMIT 100
```

### Concept Prerequisites (dependsOn)

Find what concepts are needed to understand a target concept:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?prerequisite ?label WHERE {
  paper:co_transfer_learning paper:dependsOn ?prerequisite .
  ?prerequisite rdfs:label ?label .
}
LIMIT 100
```

### Claim Chains (extends transitivity)

Trace how claims build on each other:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?claim ?text ?ancestor WHERE {
  ?claim a paper:Claim ; rdfs:label ?text .
  ?claim paper:extends+ ?ancestor .
  ?ancestor rdfs:label ?ancestorText .
}
LIMIT 100
```

### Author Inference (primaryAuthor → author)

`primaryAuthor` is a subproperty of `author`. Querying `author` matches both:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

# Finds papers where Alice is primaryAuthor OR co-author
SELECT ?paper ?title WHERE {
  ?paper paper:author paper:au_a1b2c3d4 ; rdfs:label ?title .
}
LIMIT 100
```

### Claims by Concept

Find claims about a specific concept:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?claim ?claimText ?paper ?paperTitle WHERE {
  ?claim paper:regarding paper:co_transformer ;
         rdfs:label ?claimText .
  ?paper paper:hasClaim ?claim ; rdfs:label ?paperTitle .
}
LIMIT 100
```

### Competing Claims

Find claims on the same concept that refute each other:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?claim1 ?text1 ?claim2 ?text2 ?concept WHERE {
  ?p1 paper:about ?concept ; paper:hasClaim ?claim1 .
  ?p2 paper:about ?concept ; paper:hasClaim ?claim2 .
  ?claim1 paper:refutes ?claim2 .
  ?claim1 rdfs:label ?text1 .
  ?claim2 rdfs:label ?text2 .
}
LIMIT 100
```

### Citation Network

Find papers citing a specific paper:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?citing ?citingTitle ?cited ?citedTitle WHERE {
  ?citing paper:cites ?cited ; rdfs:label ?citingTitle .
  ?cited rdfs:label ?citedTitle .
  ?cited paper:doi "10.1234/example" .
}
LIMIT 100
```

### Co-citation (papers cited together)

Find papers frequently cited together:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?cited1 ?title1 ?cited2 ?title2 (COUNT(?citing) AS ?coCiteCount) WHERE {
  ?citing paper:cites ?cited1, ?cited2 .
  ?cited1 rdfs:label ?title1 .
  ?cited2 rdfs:label ?title2 .
  FILTER(STR(?cited1) < STR(?cited2))
}
GROUP BY ?cited1 ?title1 ?cited2 ?title2
ORDER BY DESC(?coCiteCount)
LIMIT 20
```

### Citation with Claim Relationship

Find citations where claims are also semantically related:

```sparql
PREFIX paper: <https://kg.corca.ai/paper#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?citingPaper ?citingTitle ?citedPaper ?citedTitle ?relType WHERE {
  ?citingPaper paper:cites ?citedPaper ;
               rdfs:label ?citingTitle ;
               paper:hasClaim ?claim1 .
  ?citedPaper rdfs:label ?citedTitle ;
              paper:hasClaim ?claim2 .
  { ?claim1 paper:extends ?claim2 . BIND("extends" AS ?relType) }
  UNION
  { ?claim1 paper:supports ?claim2 . BIND("supports" AS ?relType) }
  UNION
  { ?claim1 paper:refutes ?claim2 . BIND("refutes" AS ?relType) }
}
LIMIT 100
```

### Shortest Path (GraphDB extension)

Find shortest citation path between two papers:

```sparql
PREFIX path: <http://www.ontotext.com/path#>

SELECT ?pathIndex ?edgeIndex ?edge WHERE {
    VALUES (?src ?dst) {
        ( <https://kg.corca.ai/paper#pa_abc> <https://kg.corca.ai/paper#pa_xyz> )
    }
    SERVICE path:search {
        [] path:findPath path:shortestPath ;
           path:sourceNode ?src ;
           path:destinationNode ?dst ;
           path:pathIndex ?pathIndex ;
           path:resultBindingIndex ?edgeIndex ;
           path:resultBinding ?edge .
    }
}
```

Returns all shortest paths (if multiple exist with same length). Each edge is an RDF* triple.

## Performance

- **Always use LIMIT**: Prevent runaway queries
- **Transitive properties are expensive**: `broader*` and `extends+` cost grows with data size. Consider limiting depth:
  ```sparql
  # Instead of: ?x paper:broader* ?root
  # Use explicit depth when possible:
  { ?x paper:broader ?root } UNION { ?x paper:broader/paper:broader ?root }
  ```
- **Filter early**: Place restrictive patterns first in WHERE clause
