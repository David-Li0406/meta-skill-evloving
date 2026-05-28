# Knowledge Graphs & Semantic Systems

Relationship modeling and graph-based reasoning for structured context.

## When to Use Knowledge Graphs

| Use Case                | Vector DB | Knowledge Graph | Hybrid |
| ----------------------- | --------- | --------------- | ------ |
| Semantic similarity     | ✓         |                 |        |
| Entity relationships    |           | ✓               |        |
| Multi-hop reasoning     |           | ✓               |        |
| Temporal facts          |           | ✓               |        |
| Complex queries         |           |                 | ✓      |
| Enterprise knowledge    |           |                 | ✓      |

## Knowledge Graph Architecture

```
┌─────────────────────────────────────────┐
│           Knowledge Graph               │
├─────────────────────────────────────────┤
│  Entities     ──relates_to──▶ Entities  │
│  (nodes)        (edges)       (nodes)   │
├─────────────────────────────────────────┤
│  Properties: attributes on nodes/edges  │
│  Labels: categorization of nodes        │
│  Temporal: valid_from, valid_to         │
└─────────────────────────────────────────┘
```

## Temporal Knowledge Graph

```python
class TemporalKnowledgeGraph:
    def __init__(self):
        self.facts = []
        self.entities = {}

    def add_fact(self, subject, predicate, obj, valid_from, valid_to=None):
        """Add a time-bounded fact."""
        self.facts.append({
            "triple": (subject, predicate, obj),
            "valid_from": valid_from,
            "valid_to": valid_to or "current"
        })
        self._index_entity(subject)
        self._index_entity(obj)

    def query_at_time(self, subject, predicate, timestamp):
        """Query facts valid at a specific time."""
        for fact in self.facts:
            s, p, o = fact["triple"]
            if s == subject and p == predicate:
                if self._is_valid_at(fact, timestamp):
                    return o
        return None

    def _is_valid_at(self, fact, timestamp):
        return (fact["valid_from"] <= timestamp and
                (fact["valid_to"] == "current" or fact["valid_to"] >= timestamp))

    def get_entity_history(self, entity_id, predicate=None):
        """Get temporal evolution of an entity."""
        history = []
        for fact in self.facts:
            s, p, o = fact["triple"]
            if s == entity_id:
                if predicate is None or p == predicate:
                    history.append({
                        "predicate": p,
                        "object": o,
                        "valid_from": fact["valid_from"],
                        "valid_to": fact["valid_to"]
                    })
        return sorted(history, key=lambda x: x["valid_from"])
```

## Entity Linking

```python
class EntityLinker:
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.aliases = {}  # alias -> canonical_id

    def link(self, mention, context=None):
        """Resolve text mention to knowledge graph entity."""
        # Exact match
        if mention in self.aliases:
            return self.aliases[mention]

        # Fuzzy match
        candidates = self.fuzzy_search(mention)
        if not candidates:
            return None

        # Disambiguate using context
        if context and len(candidates) > 1:
            return self.disambiguate(candidates, context)

        return candidates[0]

    def disambiguate(self, candidates, context):
        """Use context to select correct entity."""
        scores = {}
        for candidate in candidates:
            entity = self.kg.get_entity(candidate)
            # Score based on context overlap
            scores[candidate] = self.context_similarity(entity, context)
        return max(scores, key=scores.get)
```

## Graph-Based Reasoning

```python
def multi_hop_query(kg, start_entity, path_pattern, max_hops=3):
    """
    Execute multi-hop traversal.
    path_pattern: ["works_for", "located_in"]
    """
    current_entities = {start_entity}

    for predicate in path_pattern[:max_hops]:
        next_entities = set()
        for entity in current_entities:
            neighbors = kg.get_neighbors(entity, predicate)
            next_entities.update(neighbors)
        current_entities = next_entities

    return current_entities

# Example: Find cities where employees of company X work
# Start: Company X
# Path: ["employs", "lives_in", "is_city"]
```

## Ontology Design

```yaml
# Domain ontology example
entities:
  Project:
    properties:
      - name: string
      - status: enum[active, completed, archived]
      - start_date: date
    relations:
      - has_member: Person (many)
      - uses_technology: Technology (many)
      - owned_by: Organization (one)

  Person:
    properties:
      - name: string
      - role: string
    relations:
      - works_on: Project (many)
      - reports_to: Person (one)
      - has_skill: Skill (many)

  Technology:
    properties:
      - name: string
      - category: string
    relations:
      - requires: Technology (many)
```

## GraphRAG Pattern

Combine knowledge graphs with retrieval for structured + unstructured.

```python
class GraphRAG:
    def __init__(self, kg, vector_store):
        self.kg = kg
        self.vectors = vector_store

    def query(self, question):
        # 1. Extract entities from question
        entities = self.extract_entities(question)

        # 2. Get graph context around entities
        graph_context = self.kg.get_subgraph(entities, depth=2)

        # 3. Get vector context
        vector_context = self.vectors.search(question, top_k=5)

        # 4. Combine contexts
        combined = self.merge_contexts(graph_context, vector_context)

        # 5. Generate answer with structured + unstructured context
        return self.generate(question, combined)
```

## Benchmark Performance

| System     | DMR Accuracy | Approach                  |
| ---------- | ------------ | ------------------------- |
| Zep        | 94.8%        | Temporal knowledge graphs |
| MemGPT     | 93.4%        | Hierarchical memory       |
| GraphRAG   | 75-85%       | Knowledge graphs          |
| Vector RAG | 60-70%       | Embedding similarity      |

## Guidelines

1. Use knowledge graphs for relationship-heavy domains
2. Implement temporal awareness for evolving facts
3. Combine with vector search for hybrid retrieval
4. Design ontology before building graph
5. Index entities for fast lookup
6. Support multi-hop queries for complex reasoning
7. Version facts for audit trails

## Related

- [Memory Systems](./memory-systems.md)
- [Vector Databases](./vector-databases.md)
