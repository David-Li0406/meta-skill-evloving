---
name: ms-agent-framework-rag
description: Comprehensive guide for building Agentic RAG systems using Microsoft Agent Framework in C#. Use when creating RAG applications with semantic search, document indexing, and intelligent agent orchestration. Includes scaffolding scripts, reference implementations, and documentation for vector databases, embedding models, and multi-agent workflows.
---

# Microsoft Agent Framework - Agentic RAG System

This skill provides scaffolding and guidance for building production-ready Agentic RAG (Retrieval-Augmented Generation) systems using Microsoft Agent Framework with C#.

## Quick Start

Use the scaffolding script to create a new RAG system:

```bash
scripts/create_rag_system.sh <project-name> [--output-dir <path>]
```

Example:
```bash
scripts/create_rag_system.sh MyKnowledgeBase --output-dir ./my-rag-project
```

## Architecture Overview

An Agentic RAG system consists of:

1. **Ingestion Layer**: Document parsing, chunking, and embedding generation
2. **Vector Store**: Semantic search index (Azure AI Search, Qdrant, or Pinecone)
3. **Agent Framework**: Multi-agent orchestration with Microsoft AutoGen
4. **LLM Integration**: Azure OpenAI or OpenAI API for generation
5. **API Layer**: RESTful endpoints for querying

## Core Components

### 1. Semantic Search

- Use Azure AI Search for integrated vector + keyword search
- Store embeddings with metadata (source, timestamp, tags)
- Implement hybrid search (vector + BM25) for best results

See `references/semantic_search.md` for implementation details.

### 2. Multi-Agent System

Build specialized agents:
- **Research Agent**: Finds relevant documents
- **Synthesis Agent**: Combines information from multiple sources
- **Validation Agent**: Checks accuracy and citations

See `references/agent_patterns.md` for agent design patterns.

### 3. Document Processing

- Supported formats: PDF, DOCX, TXT, MD, HTML
- Chunking strategies: semantic, sliding window, hierarchical
- Metadata extraction: title, author, date, tags

See `references/document_processing.md` for chunking strategies.

## Available Scripts

### `create_rag_system.sh`

Scaffolds a complete RAG system with:
- Project structure following best practices
- Configuration files (appsettings.json)
- Docker compose for local development
- Example agents and tools

Usage:
```bash
scripts/create_rag_system.sh <project-name> [--output-dir <path>]
```

### `ingest_documents.sh`

Batch document ingestion:

```bash
scripts/ingest_documents.sh <source-dir> <index-name>
```

### `run_local.sh`

Start the RAG system locally:

```bash
scripts/run_local.sh <project-dir>
```

## Configuration

Required environment variables:

```bash
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_KEY=<your-key>
AZURE_SEARCH_ENDPOINT=<your-search-endpoint>
AZURE_SEARCH_KEY=<your-search-key>
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_MODEL=gpt-4
```

## Reference Documentation

- `references/semantic_search.md` - Vector search implementation
- `references/agent_patterns.md` - Multi-agent design patterns
- `references/document_processing.md` - Chunking and preprocessing
- `references/evaluation.md` - RAG quality metrics

## Best Practices

1. **Start Simple**: Begin with basic RAG, add agents incrementally
2. **Metadata Matters**: Rich metadata improves retrieval accuracy
3. **Hybrid Search**: Combine vector and keyword search
4. **Citation Tracking**: Always include source references
5. **Evaluation**: Use RAGAS framework for quality metrics

## Common Patterns

### Multi-Step Retrieval

For complex queries, use iterative refinement:
1. Initial search with broad query
2. Research agent expands with sub-queries
3. Synthesis agent combines results
4. Validation agent checks citations

### Citation Management

Always track:
- Document ID
- Page number
- Chunk index
- Relevance score

See `references/citations.md` for implementation.

## Troubleshooting

### Poor Retrieval Quality

- Adjust chunk size (try 512-1024 tokens)
- Use hybrid search instead of pure vector
- Add more metadata for filtering
- Consider re-embedding with different model

### Slow Performance

- Enable caching on vector queries
- Use streaming responses
- Implement async document ingestion
- Consider partitioning large indices

### High Costs

- Use smaller models for embeddings
- Cache frequently asked questions
- Implement result pagination
- Use batch processing for ingestion
