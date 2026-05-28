---
name: rag-system-builder
description: Use this skill to build Retrieval-Augmented Generation (RAG) systems that enhance AI applications with external knowledge sources, enabling accurate question-answering and context-grounded responses.
---

# RAG System Builder Skill

## Overview

This skill creates complete Retrieval-Augmented Generation (RAG) systems that combine semantic search with LLM-powered Q&A. Users can ask natural language questions and receive accurate answers grounded in your document collection.

## When to Use

Use this skill when:

- Building knowledge-based AI applications requiring external document access
- Implementing question-answering systems over large document collections
- Creating AI assistants with access to company knowledge bases
- Developing chatbots with domain expertise
- Enabling natural language queries over knowledge bases
- Adding AI-powered search to existing document systems
- Reducing hallucinations with grounded responses

## Core Components

### Vector Databases
Store and efficiently retrieve document embeddings for semantic search.

**Key Options:**
- **Pinecone**: Managed, scalable, production-ready
- **Weaviate**: Open-source, hybrid search capabilities
- **Milvus**: High performance, on-premise deployment
- **Chroma**: Lightweight, easy local development
- **Qdrant**: Fast, advanced filtering
- **FAISS**: Meta's library, full control

### Embedding Models
Convert text to numerical vectors for similarity search.

**Popular Models:**
- **text-embedding-ada-002** (OpenAI): General purpose, 1536 dimensions
- **all-MiniLM-L6-v2**: Fast, lightweight, 384 dimensions
- **e5-large-v2**: High quality, multilingual

### Retrieval Strategies
Find relevant content based on user queries.

**Approaches:**
- **Dense Retrieval**: Semantic similarity via embeddings
- **Sparse Retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid Search**: Combine dense + sparse for best results

## Quick Implementation

### Basic RAG Setup

```java
// Load documents from file system
List<Document> documents = FileSystemDocumentLoader.loadDocuments("/path/to/docs");

// Create embedding store
InMemoryEmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

// Ingest documents into the store
EmbeddingStoreIngestor.ingest(documents, embeddingStore);

// Create AI service with RAG capability
Assistant assistant = AiServices.builder(Assistant.class)
    .chatModel(chatModel)
    .contentRetriever(EmbeddingStoreContentRetriever.from(embeddingStore))
    .build();
```

### Document Processing Pipeline

```java
// Split documents into chunks
DocumentSplitter splitter = new RecursiveCharacterTextSplitter(
    500,  // chunk size
    100   // overlap
);

// Create embedding model
EmbeddingModel embeddingModel = OpenAiEmbeddingModel.builder()
    .apiKey("your-api-key")
    .build();

// Process and store documents
for (Document document : documents) {
    List<TextSegment> segments = splitter.split(document);
    for (TextSegment segment : segments) {
        Embedding embedding = embeddingModel.embed(segment).content();
        embeddingStore.add(embedding, segment);
    }
}
```

## RAG Query Engine

```python
import anthropic
import openai

class RAGQueryEngine:
    def __init__(self, db_path, embedding_model):
        self.db_path = db_path
        self.model = embedding_model

    def query(self, question, top_k=5, provider='anthropic'):
        """Answer question using RAG."""
        results = semantic_search(self.db_path, question, self.model, top_k)
        context = "\n\n---\n\n".join([f"Source: {r['filename']}\n{r['text']}" for r in results])
        prompt = f"""Based on the following technical documents, answer the question.
If the answer is not in the documents, say so.

DOCUMENTS:
{context}

QUESTION: {question}

ANSWER:"""

        if provider == 'anthropic':
            return self._query_claude(prompt), results
        else:
            return self._query_openai(prompt), results

    def _query_claude(self, prompt):
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _query_openai(self, prompt):
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

## Best Practices

### Document Preparation
- Clean and preprocess documents before ingestion
- Remove irrelevant content and formatting artifacts
- Standardize document structure for consistent processing
- Add relevant metadata for filtering and context

### Chunking Strategy
- Use 500-1000 tokens per chunk for optimal balance
- Include 10-20% overlap to preserve context at boundaries
- Consider document structure when determining chunk boundaries

### Retrieval Optimization
- Start with high k values (10-20) then filter/rerank
- Use metadata filtering to improve relevance
- Combine multiple retrieval strategies for better coverage

## Common Issues and Solutions

### Poor Retrieval Quality
**Problem**: Retrieved documents don't match user queries
**Solutions**:
- Improve document preprocessing and cleaning
- Adjust chunk size and overlap parameters
- Try different embedding models

### Irrelevant Results
**Problem**: Retrieved documents contain relevant information but are not specific enough
**Solutions**:
- Add metadata filtering for domain-specific constraints
- Implement reranking with cross-encoder models

## Evaluation Framework

### Retrieval Metrics
- **Precision@k**: Percentage of relevant documents in top-k results
- **Recall@k**: Percentage of all relevant documents found in top-k results

## Resources

### Reference Documentation
- [Vector Database Comparison](references/vector-databases.md) - Detailed comparison of vector database options
- [Embedding Models Guide](references/embedding-models.md) - Model selection and optimization

## Execution Checklist

- [ ] Set up knowledge base with text extraction
- [ ] Generate vector embeddings for all chunks
- [ ] Configure API keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)
- [ ] Test semantic search independently
- [ ] Build and test RAG pipeline end-to-end