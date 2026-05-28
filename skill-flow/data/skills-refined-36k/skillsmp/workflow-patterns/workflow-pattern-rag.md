---
name: workflow-pattern-rag
description: "RAG (Retrieval Augmented Generation) workflow patterns. Use when asking 'RAG', 'retrieval augmented', 'vector search', 'semantic search', or 'document Q&A'."
---

# RAG Workflow Patterns

Retrieval Augmented Generation patterns for AI-powered document search and Q&A.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-ai-reference`](../nodes/nodes-ai-reference.md), [`workflow-pattern-ai-document`](workflow-pattern-ai-document.md)
> Related Subagents: `pattern-expert` (RAG workflows), `kaizen-specialist` (AI agents)

## Quick Reference

RAG workflow components:
- **Document ingestion** - Load and chunk documents
- **Embedding generation** - Convert text to vectors
- **Vector storage** - Store in vector database
- **Similarity search** - Find relevant chunks
- **LLM generation** - Generate answers with context

## Pattern 1: Document Ingestion Pipeline

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. Load document
workflow.add_node("DocumentProcessorNode", "load_doc", {
    "file_path": "{{input.document_path}}",
    "extract_metadata": True
})

# 2. Split into chunks
workflow.add_node("TextChunkerNode", "chunk_text", {
    "input": "{{load_doc.content}}",
    "chunk_size": 512,
    "chunk_overlap": 50,
    "strategy": "semantic"  # Preserve sentence boundaries
})

# 3. Generate embeddings
workflow.add_node("EmbeddingNode", "generate_embeddings", {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "text": "{{chunk_text.chunks}}"
})

# 4. Store in vector database
workflow.add_node("VectorStoreNode", "store_vectors", {
    "collection": "documents",
    "vectors": "{{generate_embeddings.embeddings}}",
    "metadata": {
        "doc_id": "{{input.document_id}}",
        "chunk_index": "{{chunk_text.indices}}",
        "text": "{{chunk_text.chunks}}"
    }
})

workflow.add_connection("load_doc", "chunk_text")
workflow.add_connection("chunk_text", "generate_embeddings")
workflow.add_connection("generate_embeddings", "store_vectors")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build(), inputs={
    "document_path": "docs/manual.pdf",
    "document_id": "doc_001"
})
```

## Pattern 2: RAG Query Pipeline

```python
workflow = WorkflowBuilder()

# 1. Generate query embedding
workflow.add_node("EmbeddingNode", "query_embedding", {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "text": "{{input.query}}"
})

# 2. Vector similarity search
workflow.add_node("VectorSearchNode", "search_similar", {
    "collection": "documents",
    "query_vector": "{{query_embedding.embedding}}",
    "top_k": 5,
    "min_score": 0.7
})

# 3. Rerank results (optional)
workflow.add_node("RerankNode", "rerank", {
    "query": "{{input.query}}",
    "documents": "{{search_similar.results}}",
    "model": "rerank-english-v2.0"
})

# 4. Build context prompt
workflow.add_node("TransformNode", "build_prompt", {
    "input": "{{rerank.documents}}",
    "transformation": """
        context = '\n\n'.join([doc['text'] for doc in input])
        return f'''Answer the question based on this context:

Context:
{context}

Question: {{input.query}}

Answer:'''
    """
})

# 5. Generate answer with LLM
workflow.add_node("LLMNode", "generate_answer", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "{{build_prompt.result}}",
    "temperature": 0.3
})

workflow.add_connection("query_embedding", "search_similar")
workflow.add_connection("search_similar", "rerank")
workflow.add_connection("rerank", "build_prompt")
workflow.add_connection("build_prompt", "generate_answer")
```

## Pattern 3: Multi-Document RAG

```python
workflow = WorkflowBuilder()

# 1. Query embedding
workflow.add_node("EmbeddingNode", "query_embed", {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "text": "{{input.query}}"
})

# 2. Search multiple collections in parallel
workflow.add_node("VectorSearchNode", "search_docs", {
    "collection": "documents",
    "query_vector": "{{query_embed.embedding}}",
    "top_k": 3
})

workflow.add_node("VectorSearchNode", "search_code", {
    "collection": "codebase",
    "query_vector": "{{query_embed.embedding}}",
    "top_k": 3
})

workflow.add_node("VectorSearchNode", "search_api", {
    "collection": "api_docs",
    "query_vector": "{{query_embed.embedding}}",
    "top_k": 3
})

# 3. Merge and rerank all results
workflow.add_node("MergeNode", "merge_results", {
    "inputs": [
        "{{search_docs.results}}",
        "{{search_code.results}}",
        "{{search_api.results}}"
    ],
    "strategy": "combine"
})

workflow.add_node("RerankNode", "rerank_all", {
    "query": "{{input.query}}",
    "documents": "{{merge_results.combined}}",
    "top_k": 5
})

# 4. Generate comprehensive answer
workflow.add_node("LLMNode", "generate", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": """Answer using context from docs, code, and API:

Context: {{rerank_all.documents}}

Question: {{input.query}}

Provide a comprehensive answer with examples."""
})

# Parallel searches
workflow.add_connection("query_embed", "search_docs")
workflow.add_connection("query_embed", "search_code")
workflow.add_connection("query_embed", "search_api")

workflow.add_connection("search_docs", "merge_results")
workflow.add_connection("search_code", "merge_results")
workflow.add_connection("search_api", "merge_results")

workflow.add_connection("merge_results", "rerank_all")
workflow.add_connection("rerank_all", "generate")
```

## Pattern 4: Conversational RAG with Memory

```python
workflow = WorkflowBuilder()

# 1. Load conversation history
workflow.add_node("DatabaseQueryNode", "load_history", {
    "query": """
        SELECT role, content FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at DESC LIMIT 5
    """,
    "parameters": ["{{input.conversation_id}}"]
})

# 2. Build conversation context
workflow.add_node("TransformNode", "build_context", {
    "input": "{{load_history.results}}",
    "transformation": "'\n'.join([f'{m.role}: {m.content}' for m in input])"
})

# 3. Embed query with context
workflow.add_node("EmbeddingNode", "embed_query", {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "text": "{{input.query}} Context: {{build_context.context}}"
})

# 4. Vector search
workflow.add_node("VectorSearchNode", "search", {
    "collection": "documents",
    "query_vector": "{{embed_query.embedding}}",
    "top_k": 5
})

# 5. Generate answer with history
workflow.add_node("LLMNode", "generate", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": """Conversation History:
{{build_context.context}}

Relevant Documents:
{{search.results}}

User: {{input.query}}
