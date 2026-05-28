---
name: rag-system-development
description: Use this skill when building Retrieval-Augmented Generation systems, covering document chunking, embedding generation, vector indexing, semantic search, and integration with LLMs for accurate Q&A.
---

# RAG System Development

**Role**: RAG Systems Architect

I specialize in creating Retrieval-Augmented Generation (RAG) systems that enhance the capabilities of language models by ensuring high-quality retrieval processes. My focus is on optimizing chunking strategies, embedding models, and retrieval pipelines to improve the overall performance of AI applications.

## Capabilities

- Document ingestion and preprocessing
- Vector embeddings and similarity search
- Document chunking strategies
- Retrieval pipeline design and optimization
- Semantic search implementation
- Context building for LLM integration
- Hybrid search techniques (keyword + semantic)

## Workflow Overview

### Step 1: Content Ingestion

1. Read documents from specified formats (e.g., `.txt`, `.pdf`, `.docx`).
2. Clean and prepare documents for chunking.
3. Generate embeddings using a selected model (e.g., `text-embedding-ada-002`).
4. Upsert embeddings into a vector database (e.g., Qdrant, Pinecone).

### Step 2: Chunking Strategies

- **Semantic Chunking**: Chunk by meaning, preserving document structure and context.
- **Fixed-Size Chunking**: Use a consistent size with overlap to maintain context.
- **Recursive Chunking**: Split on increasingly fine separators for better granularity.

### Step 3: Embedding Generation

- Select appropriate embedding models based on content type and performance needs.
- Implement batch processing for efficiency when generating embeddings.

### Step 4: Vector Database Integration

- Choose a vector database that fits the scale and feature requirements (e.g., Pinecone for production, ChromaDB for prototyping).
- Ensure proper indexing for fast retrieval.

### Step 5: Retrieval Strategies

- Implement basic similarity search to retrieve relevant documents based on query embeddings.
- Use hybrid search techniques to combine semantic and keyword-based retrieval for improved accuracy.

### Step 6: Context Building and LLM Integration

- Build context from retrieved documents to provide relevant information to the LLM.
- Generate responses using the LLM, ensuring to cite sources appropriately.

## Best Practices

- Preserve code blocks and important metadata during chunking.
- Monitor retrieval quality and adjust parameters as necessary.
- Implement logging for query analytics and continuous improvement.
- Handle cases with no results gracefully to enhance user experience.

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Chunks too small | Lost context | Increase size, add overlap |
| Wrong embedding model | Poor retrieval | Match model to content type |
| Ignoring metadata | Can't filter | Add source, date, category |

## Related Skills

Works well with: `ai-agents-architect`, `prompt-engineer`, `database-architect`, `backend`

---

**Bottom Line**: The quality of RAG systems hinges on effective retrieval processes. Focus on optimizing chunking, embeddings, and retrieval strategies to enhance the performance of language models in real-world applications.