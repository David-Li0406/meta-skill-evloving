---
id: agentic-rag
name: "Agentic RAG (RAG 2.0)"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

## Agentic RAG (RAG 2.0)

### Problem

Traditional RAG: single retrieval, no verification, limited reasoning.

### Solution: Agentic RAG

**Key Differences:**

| Traditional RAG | Agentic RAG |
|-----------------|-------------|
| Single retrieval | Multi-hop retrieval |
| Fixed pipeline | Dynamic reasoning |
| No self-correction | Iterative refinement |
| Context stuffing | Selective retrieval |

**Agentic RAG Loop:**
```
Query -> Think -> Retrieve -> Evaluate sufficiency
                                  |
                    Insufficient? -> Re-query/Different source
                                  |
                    Sufficient -> Generate answer -> Verify -> Output
```

**Implementation:**
```python
# Agentic RAG pattern
class AgenticRAG:
    def answer(self, query):
        context = []
        for attempt in range(max_attempts):
            retrieved = self.retrieve(query, context)
            context.extend(retrieved)

            if self.is_sufficient(query, context):
                break

            query = self.refine_query(query, context)

        answer = self.generate(query, context)
        return self.verify(answer, context)
```

**Use Cases:**
- Complex multi-step questions
- Research synthesis
- Compliance verification
- Multi-source fact-checking
