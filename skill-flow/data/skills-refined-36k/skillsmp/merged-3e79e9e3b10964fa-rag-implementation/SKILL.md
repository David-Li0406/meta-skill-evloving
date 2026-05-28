---
name: rag-implementation
description: Build Retrieval-Augmented Generation (RAG) systems for AI applications that integrate external knowledge sources, enabling accurate and context-grounded responses.
---

# RAG Implementation

## When to Use This Skill

Use this skill when:
- Building knowledge-based AI applications requiring external document access
- Implementing question-answering systems over large document collections
- Creating AI assistants with access to company knowledge bases
- Enabling semantic search capabilities for document repositories
- Reducing hallucinations by grounding responses in specific data
- Managing user-specific or team-specific knowledge namespaces

## Overview

Retrieval-Augmented Generation (RAG) enhances AI applications by retrieving relevant information from knowledge bases and incorporating it into AI responses, improving accuracy and reducing hallucinations.

## Core Components

### Vector Databases
Store and efficiently retrieve document embeddings for semantic search. Key options include:
- **Pinecone**: Managed, scalable, production-ready
- **Weaviate**: Open-source, hybrid search capabilities
- **Milvus**: High performance, on-premise deployment
- **Chroma**: Lightweight, easy local development
- **Qdrant**: Fast, advanced filtering
- **FAISS**: Meta's library, full control

### Embedding Models
Convert text to numerical vectors for similarity search. Popular models include:
- **text-embedding-ada-002** (OpenAI): General purpose, 1536 dimensions
- **all-MiniLM-L6-v2**: Fast, lightweight, 384 dimensions
- **e5-large-v2**: High quality, multilingual

### Retrieval Strategies
Find relevant content based on user queries using:
- **Dense Retrieval**: Semantic similarity via embeddings
- **Sparse Retrieval**: Keyword matching (BM25, TF-IDF)
- **Hybrid Search**: Combine dense and sparse for best results

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
DocumentSplitter splitter = new RecursiveCharacterTextSplitter(500, 100);

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

## Implementation Patterns

### Simple Document Q&A

Create a basic Q&A system over your documents.

```java
public interface DocumentAssistant {
    String answer(String question);
}

DocumentAssistant assistant = AiServices.builder(DocumentAssistant.class)
    .chatModel(chatModel)
    .contentRetriever(retriever)
    .build();
```

### Metadata-Filtered Retrieval

Filter results based on document metadata.

```java
// Add metadata during document loading
Document document = Document.builder()
    .text("Content here")
    .metadata("source", "technical-manual.pdf")
    .build();

// Filter during retrieval
EmbeddingStoreContentRetriever retriever = EmbeddingStoreContentRetriever.builder()
    .embeddingStore(embeddingStore)
    .maxResults(5)
    .filter(metadataKey("source").isEqualTo("technical-manual.pdf"))
    .build();
```

### Multi-Source Retrieval

Combine results from multiple knowledge sources.

```java
ContentRetriever webRetriever = EmbeddingStoreContentRetriever.from(webStore);
ContentRetriever documentRetriever = EmbeddingStoreContentRetriever.from(documentStore);

// Combine results
List<Content> allResults = new ArrayList<>();
allResults.addAll(webRetriever.retrieve(query));
allResults.addAll(documentRetriever.retrieve(query));

// Rerank combined results
List<Content> rerankedResults = reranker.reorder(query, allResults);
```

## Best Practices

### Document Preparation
- Clean and preprocess documents before ingestion
- Standardize document structure for consistent processing
- Add relevant metadata for filtering and context

### Chunking Strategy
- Use 500-1000 tokens per chunk for optimal balance
- Include 10-20% overlap to preserve context at boundaries

### Retrieval Optimization
- Start with high k values (10-20) then filter/rerank
- Use metadata filtering to improve relevance

## Common Issues and Solutions

### Poor Retrieval Quality
**Problem**: Retrieved documents don't match user queries
**Solutions**:
- Improve document preprocessing and cleaning
- Adjust chunk size and overlap parameters

### Irrelevant Results
**Problem**: Retrieved documents contain relevant information but are not specific enough
**Solutions**:
- Add metadata filtering for domain-specific constraints
- Implement reranking with cross-encoder models

### Performance Issues
**Problem**: Slow response times during retrieval
**Solutions**:
- Optimize vector store configuration and indexing
- Implement caching for frequently retrieved content

## References

- [Vector Database Comparison](references/vector-databases.md) - Detailed comparison of vector database options
- [Embedding Models Guide](references/embedding-models.md) - Model selection and optimization
- [LangChain4j RAG Guide](references/langchain4j-rag-guide.md) - Official implementation patterns