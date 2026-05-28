# RAG Agent Pattern

Retrieval-Augmented Generation implementation.

## Signature

```python
class RAGSignature(Signature):
    query: str = InputField(description="User query")
    documents: str = InputField(description="Retrieved documents as JSON")
    answer: str = OutputField(description="Answer based on documents")
    sources: str = OutputField(description="Source citations as JSON")
```

## Agent

```python
class RAGAgent(BaseAgent):
    def __init__(self, config, retriever):
        super().__init__(config=config, signature=RAGSignature())
        self.retriever = retriever

    def query(self, question: str) -> dict:
        docs = self.retriever.search(question, top_k=5)
        result = self.run(query=question, documents=json.dumps(docs))
        sources = self.extract_list(result, "sources", default=[])
        return {**result, "document_count": len(docs)}
```

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 229-247
- **Examples**: `apps/kailash-kaizen/examples/4-advanced-rag/`
