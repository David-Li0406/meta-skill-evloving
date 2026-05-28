---
name: rag-system-implementation
description: Use this skill when building Retrieval-Augmented Generation (RAG) systems that integrate external knowledge sources for enhanced AI applications, such as document Q&A systems and chatbots.
---

# RAG System Implementation

## When to Use This Skill

Use this skill when:
- Building knowledge-based AI applications requiring external document access
- Implementing question-answering systems over large document collections
- Creating AI assistants with access to company knowledge bases
- Developing semantic search capabilities for document repositories
- Implementing chat systems that reference specific information sources
- Reducing hallucinations by grounding responses in factual data
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

## Quick Implementation Steps

### Initialize RAG Project

Create a new project with required dependencies. For a Java Spring Boot project, include the following in your `pom.xml`:

```xml
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-spring-boot-starter</artifactId>
    <version>1.8.0</version>
</dependency>
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>1.8.0</version>
</dependency>
```

### Setup Document Ingestion

Configure document loading and processing:

```java
@Configuration
public class RAGConfiguration {

    @Bean
    public EmbeddingModel embeddingModel() {
        return OpenAiEmbeddingModel.builder()
            .apiKey(System.getenv("OPENAI_API_KEY"))
            .modelName("text-embedding-3-small")
            .build();
    }

    @Bean
    public EmbeddingStore<TextSegment> embeddingStore() {
        return new InMemoryEmbeddingStore<>();
    }
}
```

### Add Content and Search

Ingest documents and implement search functionality. For example, in a TypeScript environment:

```typescript
import { rag } from "@convex-dev/rag";

export const addContent = action({
  args: { userId: v.string(), key: v.string(), text: v.string() },
  handler: async (ctx, { userId, key, text }) => {
    const namespace = `user:${userId}`;
    await rag.addContent(ctx, components.rag, {
      namespace,
      key,
      text,
    });
  },
});

export const answerWithContext = action({
  args: { threadId: v.string(), userId: v.string(), question: v.string() },
  handler: async (ctx, { threadId, userId, question }) => {
    const context = await rag.search(ctx, components.rag, {
      namespace: `user:${userId}`,
      query: question,
      limit: 10,
    });

    const augmentedPrompt = `# Context:\n\n${context.text}\n\n# Question:\n\n${question}`;
    const result = await thread.generateText({ prompt: augmentedPrompt });

    return result.text;
  },
});
```

## Key Principles

- **Namespaces isolate data**: Use `user:userId` or `team:teamId` for multi-tenant safety.
- **Hybrid search**: Combine text and vector search for better results.
- **Continuous optimization**: Track metrics and iterate on retrieval strategies for improved performance.