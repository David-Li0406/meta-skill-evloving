# RAG and Memory Patterns

Guide to implementing Retrieval-Augmented Generation (RAG) and conversation memory in Mastra.

## Overview

Mastra supports multiple memory and retrieval patterns:

- **Conversation Memory** - Thread-based message history
- **Vector Storage** - Semantic search over documents
- **RAG Integration** - Combining retrieval with generation
- **Context Network Storage** - Framework knowledge persistence

## Conversation Memory

### Basic Memory Configuration

```typescript
import { Mastra } from "@mastra/core/mastra";
import { LibSQLStore } from "@mastra/libsql";

const mastra = new Mastra({
  agents: { myAgent },
  storage: new LibSQLStore({
    url: "file:./mastra.db",
  }),
});
```

### Using Memory in Agent Calls

```typescript
// First interaction
const response1 = await agent.generate("My name is Alex and I work at TechCorp", {
  memory: {
    thread: "conversation-123",  // Unique thread ID
    resource: "user-456",        // User identifier
  },
});

// Later in same thread - agent remembers context
const response2 = await agent.generate("What company do I work for?", {
  memory: {
    thread: "conversation-123",
    resource: "user-456",
  },
});
// Agent responds: "You work at TechCorp"
```

### Thread Management

```typescript
// Create new thread
const thread = await mastra.storage?.createThread({
  resourceId: "user-456",
  metadata: {
    topic: "customer-support",
    createdAt: new Date().toISOString(),
  },
});

// List threads for a user
const threads = await mastra.storage?.listThreads({
  resourceId: "user-456",
  page: 1,
  perPage: 10,
});

// Get thread messages
const messages = await mastra.storage?.getMessages({
  threadId: "thread-123",
  page: 1,
  perPage: 50,
});

// Delete thread
await mastra.storage?.deleteThread("thread-123");
```

### Message History Window

```typescript
// Limit context window for cost/performance
const response = await agent.generate("Continue our conversation", {
  memory: {
    thread: "conversation-123",
    resource: "user-456",
    options: {
      maxMessages: 10,     // Last 10 messages
      maxTokens: 4000,     // Or token limit
    },
  },
});
```

## Vector Storage

### Setting Up Vector Store

```typescript
import { Mastra } from "@mastra/core/mastra";
import { PgVector } from "@mastra/pg-vector";

const mastra = new Mastra({
  agents: { myAgent },
  vectors: {
    default: new PgVector({
      connectionString: process.env.DATABASE_URL,
      tableName: "embeddings",
    }),
  },
});
```

### Indexing Documents

```typescript
import { embedMany } from "@ai-sdk/openai";

// Chunk and embed documents
const documents = [
  { id: "doc-1", content: "Mastra is a TypeScript AI framework...", metadata: { source: "docs" } },
  { id: "doc-2", content: "Agents in Mastra can use tools...", metadata: { source: "docs" } },
];

// Generate embeddings
const { embeddings } = await embedMany({
  model: openai.embedding("text-embedding-3-small"),
  values: documents.map(d => d.content),
});

// Store in vector database
await mastra.vectors?.default.upsert({
  indexName: "knowledge-base",
  vectors: documents.map((doc, i) => ({
    id: doc.id,
    vector: embeddings[i],
    metadata: {
      content: doc.content,
      ...doc.metadata,
    },
  })),
});
```

### Querying Vectors

```typescript
import { embed } from "@ai-sdk/openai";

// Embed query
const { embedding } = await embed({
  model: openai.embedding("text-embedding-3-small"),
  value: "How do Mastra agents work?",
});

// Search
const results = await mastra.vectors?.default.query({
  indexName: "knowledge-base",
  queryVector: embedding,
  topK: 5,
  filter: { source: "docs" },
});

// results: [{ id, score, metadata: { content, source } }, ...]
```

## RAG Implementation

### Basic RAG Tool

```typescript
export const ragTool = createTool({
  id: "knowledge-search",
  description: "Search the knowledge base for relevant information",
  inputSchema: z.object({
    query: z.string().describe("Search query"),
    limit: z.number().optional().default(5),
  }),
  outputSchema: z.object({
    results: z.array(z.object({
      content: z.string(),
      score: z.number(),
      source: z.string(),
    })),
  }),
  execute: async (input, context) => {
    const { query, limit } = input;
    const { mastra } = context;

    // Embed query
    const { embedding } = await embed({
      model: openai.embedding("text-embedding-3-small"),
      value: query,
    });

    // Search
    const results = await mastra?.vectors?.default.query({
      indexName: "knowledge-base",
      queryVector: embedding,
      topK: limit,
    });

    return {
      results: results?.map(r => ({
        content: r.metadata.content,
        score: r.score,
        source: r.metadata.source,
      })) || [],
    };
  },
});
```

### RAG-Enabled Agent

```typescript
const ragAgent = new Agent({
  name: "rag-agent",
  instructions: `You are a helpful assistant with access to a knowledge base.

When answering questions:
1. First search the knowledge base for relevant information
2. Use the retrieved information to inform your response
3. Cite sources when possible
4. If the knowledge base doesn't have relevant info, say so`,
  model: openai("gpt-4o-mini"),
  tools: { ragTool },
});
```

## Context Network Integration

For operating-frameworks, context networks map to agent memory patterns:

### Vocabulary Maps as RAG

```typescript
// Store vocabulary maps for retrieval
await mastra.vectors?.default.upsert({
  indexName: "vocabulary-maps",
  vectors: [{
    id: `${userId}-${topic}-vocabulary`,
    vector: embedding,
    metadata: {
      topic,
      coreTerms: vocabularyMap.coreTerms,
      synonyms: vocabularyMap.synonyms,
      depthLevels: vocabularyMap.depthLevels,
      lastUpdated: new Date().toISOString(),
    },
  }],
});
```

### Prior Research Retrieval

```typescript
export const retrievePriorResearch = createTool({
  id: "retrieve-prior-research",
  description: "Retrieve prior research on a topic including vocabulary maps",
  inputSchema: z.object({
    topic: z.string().describe("Research topic"),
    userId: z.string().describe("User identifier"),
  }),
  execute: async (input, context) => {
    const { topic, userId } = input;
    const { mastra } = context;

    // Embed topic
    const { embedding } = await embed({
      model: openai.embedding("text-embedding-3-small"),
      value: topic,
    });

    // Search for prior vocabulary maps
    const vocabularyResults = await mastra?.vectors?.default.query({
      indexName: "vocabulary-maps",
      queryVector: embedding,
      filter: { userId },
      topK: 3,
    });

    // Search for prior research notes
    const notesResults = await mastra?.vectors?.default.query({
      indexName: "research-notes",
      queryVector: embedding,
      filter: { userId },
      topK: 5,
    });

    return {
      vocabularyMaps: vocabularyResults?.map(v => v.metadata) || [],
      priorNotes: notesResults?.map(n => n.metadata) || [],
      hasPriorResearch: (vocabularyResults?.length || 0) > 0,
    };
  },
});
```

### Framework Knowledge Indexing

```typescript
// Index framework content for agent self-awareness
const indexFrameworkKnowledge = async (framework: FrameworkDocument) => {
  // Chunk by section
  const sections = parseFrameworkSections(framework);

  const { embeddings } = await embedMany({
    model: openai.embedding("text-embedding-3-small"),
    values: sections.map(s => s.content),
  });

  await mastra.vectors?.default.upsert({
    indexName: "framework-knowledge",
    vectors: sections.map((section, i) => ({
      id: `${framework.id}-${section.id}`,
      vector: embeddings[i],
      metadata: {
        frameworkId: framework.id,
        sectionType: section.type,  // "diagnostic-state", "anti-pattern", "process"
        content: section.content,
        stateId: section.stateId,   // For diagnostic states
      },
    })),
  });
};
```

### Thread Per Topic Pattern

```typescript
// Use unique thread IDs per research topic
const getResearchThread = (userId: string, topic: string) => {
  return `research-${userId}-${topic.toLowerCase().replace(/\s+/g, "-")}`;
};

const response = await researchAgent.generate(message, {
  memory: {
    thread: getResearchThread(userId, "gentrification of workwear"),
    resource: userId,
  },
});
```

## Memory Consolidation

### Summarizing Long Conversations

```typescript
const summarizeThread = async (threadId: string) => {
  const messages = await mastra.storage?.getMessages({
    threadId,
    page: 1,
    perPage: 100,
  });

  const summarizer = new Agent({
    name: "summarizer",
    model: openai("gpt-4o-mini"),
    instructions: "Create a concise summary of the conversation.",
  });

  const conversation = messages
    ?.map(m => `${m.role}: ${m.content}`)
    .join("\n");

  const summary = await summarizer.generate(
    `Summarize this conversation:\n\n${conversation}`
  );

  // Store summary as new message type
  await mastra.storage?.addMessage({
    threadId,
    role: "system",
    content: `[SUMMARY] ${summary.text}`,
    metadata: { type: "summary", originalMessageCount: messages?.length },
  });

  return summary.text;
};
```

## Best Practices

### 1. Thread Isolation

```typescript
// Use unique thread IDs per conversation context
const threadId = `${userId}-${sessionId}`;

// Or per topic
const threadId = `${userId}-research-${topicId}`;
```

### 2. Metadata Enrichment

```typescript
// Rich metadata enables better filtering
await vectorStore.upsert({
  vectors: [{
    id: "doc-1",
    vector: embedding,
    metadata: {
      content: text,
      source: "framework",
      frameworkId: "research",
      sectionType: "diagnostic-state",
      stateId: "R1",
      createdAt: new Date().toISOString(),
    },
  }],
});
```

### 3. Memory Limits

```typescript
// Prevent runaway context costs
const response = await agent.generate(message, {
  memory: {
    thread: threadId,
    resource: userId,
    options: {
      maxMessages: 20,
      maxTokens: 8000,
      summarizeAfter: 15, // Auto-summarize after 15 messages
    },
  },
});
```

### 4. Cache Embeddings

```typescript
const embeddingCache = new Map<string, number[]>();

async function getEmbedding(text: string): Promise<number[]> {
  const cacheKey = createHash("md5").update(text).digest("hex");

  if (embeddingCache.has(cacheKey)) {
    return embeddingCache.get(cacheKey)!;
  }

  const { embedding } = await embed({
    model: openai.embedding("text-embedding-3-small"),
    value: text,
  });

  embeddingCache.set(cacheKey, embedding);
  return embedding;
}
```
