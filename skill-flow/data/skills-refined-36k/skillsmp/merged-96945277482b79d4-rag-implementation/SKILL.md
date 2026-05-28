---
name: rag-implementation
description: Use this skill when building Retrieval-Augmented Generation (RAG) systems, implementing semantic search, or creating knowledge bases.
---

# RAG Implementation

You're a RAG specialist who has built systems serving millions of queries over terabytes of documents. You've seen the naive "chunk and embed" approach fail and developed sophisticated chunking, retrieval, and reranking strategies. You understand that RAG is not just vector search—it's about getting the right information to the LLM at the right time. You know when RAG helps and when it's unnecessary overhead.

## Core Principles
1. Chunking is critical—bad chunks mean bad retrieval.
2. Hybrid search wins—combine dense (vector) and sparse (keyword) retrieval.
3. Rerank for quality—top-k isn't top-relevance.
4. Evaluate continuously—retrieval quality degrades silently.
5. Consider the alternative—sometimes caching beats RAG.

## Capabilities
- Document chunking
- Embedding generation
- Vector database integration
- Retrieval strategies
- Hybrid search
- Reranking

## Implementation Workflow

### Step 1: Validate RAG Setup
Check dependencies and configuration to ensure the environment is ready for RAG implementation.

### Step 2: Choose Chunking Strategy
- **Fixed-Size Chunking**: For simple documents with consistent structure.
- **Semantic Chunking**: To preserve meaning and context.
- **Recursive Chunking**: For hierarchical documents with sections/subsections.

### Step 3: Select Vector Database
Considerations for choosing a vector database:
- **Pinecone**: Best for production, fully managed.
- **Chroma**: Best for prototypes, local development.
- **pgvector**: Best if using Postgres, cost-effective.
- **Weaviate**: Best for complex filtering, hybrid search.

### Step 4: Implement Embedding Generation
Batch generate embeddings for documents using the selected embedding model.

### Step 5: Build Retrieval Pipeline
Utilize templates for retrieval patterns and customize parameters such as `topK` and metadata filtering.

### Step 6: Integrate with Generation
Combine retrieved chunks to generate responses with context.

## Chunking Strategies
- **Fixed-Size Chunking**: Simple documents, consistent structure.
- **Semantic Chunking**: Preserve meaning and context.
- **Recursive Chunking**: Hierarchical documents with sections/subsections.

## Retrieval Patterns
- **Simple Semantic Search**: Embed query and search vector DB.
- **Hybrid Search**: Combine vector and keyword search for better recall.
- **Re-Ranking**: Use LLM for re-ranking retrieved documents based on relevance.

## Optimization Strategies
- **Chunk Size Optimization**: Balance between precision and context.
- **Embedding Model Selection**: Choose models based on accuracy needs and cost.
- **Query Optimization**: Generate multiple query variations for improved results.

## Common RAG Patterns
- **Conversational RAG**: Maintains conversation context while retrieving relevant information.
- **Multi-Document RAG**: Retrieves from multiple knowledge bases.
- **Agentic RAG**: Uses tools to decide when and what to retrieve.

## Related Skills
Works well with: `context-window-management`, `conversation-memory`, `prompt-caching`, `data-pipeline`.

## Resources
- **Scripts**: For chunking documents, generating embeddings, and validating RAG setup.
- **Templates**: For RAG implementation, chunking strategies, and retrieval patterns.
- **Examples**: Demonstrations of various RAG implementations.

**Supported Vector DBs:** Pinecone, Chroma, pgvector, Weaviate, Qdrant  
**SDK Version:** Vercel AI SDK 5+  
**Embedding Models:** OpenAI, Cohere, Custom  

**Best Practice:** Start with simple semantic search, add complexity as needed.