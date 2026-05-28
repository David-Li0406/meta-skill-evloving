---
id: graph-rag-advanced-retrieval
name: "Graph RAG and Advanced Retrieval"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

## Graph RAG and Advanced Retrieval

### Problem

Standard RAG struggles with global questions requiring entity relationships.

### Solution: Graph-Based Retrieval

**Graph RAG Architecture:**
```
Documents -> Entity Extraction -> Knowledge Graph
                                    |
Query -> Graph Traversal -> Subgraph Selection -> LLM Synthesis
```

**Key Techniques:**

| Technique | Description |
|-----------|-------------|
| Entity-Relationship Graphs | Build structured graph over corpus |
| Query-Focused Summarization | Move from local passages to global structure |
| Hybrid Retrieval | Combine vector + graph + keyword search |
| Multi-Vector Retrieval | Dense, sparse, and graph embeddings |
| Continuous Learning | Real-time index updates from streaming data |

**Microsoft GraphRAG Pipeline:**
1. Document chunking and entity extraction
2. Community detection for related concepts
3. Hierarchical summarization at multiple granularities
4. Query routing to appropriate retrieval strategy

**Context-Adaptive Models:**
- LLMs fine-tuned to handle retrieval noise gracefully
- Retrieval-Augmented Reasoning (RAR) patterns
- Agent-controlled retrieval decisions

**Performance:**
- Clinical RAG study: accuracy improved 68% -> 73%
- Substantial hallucination reduction
- Better handling of complex multi-hop queries
