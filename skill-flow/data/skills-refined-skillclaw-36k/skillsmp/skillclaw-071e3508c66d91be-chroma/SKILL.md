---
name: chroma
description: Use this skill when you need guidance on integrating the Chroma vector database for semantic search applications, including vector search, embeddings, and RAG systems.
---

# Skill body

## Instructions

The Chroma skill has a few main abilities:

- Help the user understand how to design their search system.
- Help the user select an embedding model.
- Help the user understand what changes need to be made to their system to add search.
- Help the user design their search schema, pick an embedding model, and determine the type of search.

## Quick Start

### TypeScript (Chroma Cloud)

```typescript
import { CloudClient } from 'chromadb';
import { DefaultEmbeddingFunction } from '@chroma-core/default-embed';

const client = new CloudClient({
  apiKey: process.env.CHROMA_API_KEY,
  tenant: process.env.CHROMA_TENANT,
  database: process.env.CHROMA_DATABASE,
});

const embeddingFunction = new DefaultEmbeddingFunction();
const collection = await client.getOrCreateCollection({
  name: 'my_collection',
  embeddingFunction,
});

// Add documents
await collection.add({
  ids: ['doc1', 'doc2'],
  documents: ['First document text', 'Second document text'],
});

// Query
const results = await collection.query({
  queryTexts: ['search query'],
  nResults: 5,
});
```

### Python (Chroma Cloud)

```python
import os
import chromadb

client = chromadb.CloudClient(
    api_key=os.environ["CHROMA_API_KEY"],
    tenant=os.environ["CHROMA_TENANT"],
    database=os.environ["CHROMA_DATABASE"],
)

collection = client.get_or_create_collection(name="my_collection")

# Add documents
collection.add(
    ids=["doc1", "doc2"],
    documents=["First document text", "Second document text"],
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=5,
)
```

### Understanding Chroma

Chroma is a vector database that contains collections, which in turn contain documents. Unlike tables in a relational database, collections are created and destroyed at the application level, allowing for flexible organization of data. Each Chroma database can have millions of collections, and documents represent the text data that is to be searched.