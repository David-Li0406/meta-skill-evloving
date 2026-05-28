---
name: knowledge-graph-query
description: Query the SEA-Forge™ Knowledge Graph using SPARQL to retrieve concepts, relationships, and semantic patterns. Use for semantic lookups, concept validation, relationship discovery, and ontology exploration. Integrates with DomainForge™ and Oxigraph.
license: Complete terms in LICENSE.txt
---

# Knowledge Graph Query

Query SEA-Forge™'s Knowledge Graph using SPARQL to discover concepts, validate semantic references, and explore ontology relationships.

**For reference:** [DomainForge Handbook](../../../docs/handbooks/DomainForge_Handbook/README.md) | [SDS-003: Knowledge Graph Service](../../../docs/specs/semantic-core/sds/003-knowledge-graph-service.md)

---

## When to Use This Skill

1. **Validate ConceptId**: Check if `sea:BoundedContext` exists
2. **Find Related Concepts**: What concepts link to `sea:Deployment`?
3. **Discover Patterns**: What artifacts are in stage "IntellectualCapital"?
4. **Ontology Exploration**: Browse available concepts
5. **Semantic Anchoring**: Link artifacts to Knowledge Graph

---

## Quick Reference

### Basic Queries

```sparql
# Find all concepts in SEA ontology
PREFIX sea: <http://sea-forge.org/ontology#>

SELECT ?concept ?label
WHERE {
  ?concept a sea:Concept ;
           rdfs:label ?label .
}
```

### Validate ConceptId

```sparql
PREFIX sea: <http://sea-forge.org/ontology#>

ASK {
  sea:BoundedContext a sea:Concept .
}
# Returns: true if exists
```

### Find Related Concepts

```sparql
PREFIX sea: <http://sea-forge.org/ontology#>

SELECT ?related ?relationship
WHERE {
  sea:Deployment ?relationship ?related .
}
```

---

## Common Query Patterns

### 1. List All Bounded Contexts

```sparql
PREFIX sea: <http://sea-forge.org/ontology#>

SELECT ?context ?description
WHERE {
  ?context a sea:BoundedContext ;
           sea:description ?description .
}
```

### 2. Find Artifacts by Stage

```sparql
PREFIX sea: <http://sea-forge.org/ontology#>

SELECT ?artifact ?title ?stage
WHERE {
  ?artifact a sea:Artifact ;
            sea:title ?title ;
            sea:stage ?stage .
  FILTER(?stage = "IntellectualCapital")
}
```

### 3. Discover Concept Hierarchy

```sparql
PREFIX sea: <http://sea-forge.org/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?subclass ?superclass
WHERE {
  ?subclass rdfs:subClassOf ?superclass .
}
```

---

## Integration with SEA-Forge™

### CADSL Semantic Anchoring

Validate semantic refs before generating artifacts:

```python
# Check if conceptId exists
query = """
ASK {
  sea:QualityGate a sea:Concept .
}
"""
exists = kg_service.query(query)

if exists:
    # Safe to use in artifact
    artifact["semanticRefs"] = ["sea:QualityGate"]
```

### Case Management Enrichment

Link cases to domain concepts:

```sparql
SELECT ?case ?concept ?relationship
WHERE {
  ?case a sea:Case ;
        sea:relatedTo ?concept .
  ?concept a sea:Concept .
}
```

---

## References

- [DomainForge Handbook](../../../docs/handbooks/DomainForge_Handbook/README.md)
- [Knowledge Graph Service](../../../docs/specs/semantic-core/sds/003-knowledge-graph-service.md)
- [SPARQL Cookbook](../../../docs/handbooks/DomainForge_Handbook/Runbooks/graph_queries.md)
