---
name: chroma
description: Use this skill when integrating Chroma vector database for semantic search applications, including vector search, embeddings, and RAG systems.
---

## Instructions

The Chroma skill has a few main abilities:

- Help the user understand how to design their search system.
- Help the user select an embedding model.
- Help the user understand what changes need to be made to their system to add search.
- Help the user design their search schema and pick an embedding model.

## Quick Start

**TypeScript (Chroma Cloud):**

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

**Python (Chroma Cloud):**

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

Chroma is a database that contains collections, which in turn contain documents. Unlike tables in a relational database, collections are created and destroyed at the application level, allowing for millions of collections per database. Each document represents the text data to be searched.

When data is created or updated, the client generates an embedding based on the provided embedding function. This embedding process typically occurs via a third-party service over HTTP. Documents can also include metadata for further partitioning or filtering.

During query time, the query text is embedded using the collection's defined embedding function and sent to Chroma along with any query parameters. Chroma then searches for the nearest neighbors using a distance algorithm.

### Local vs Cloud

Chroma can be run locally or in the cloud. While everything that can be done locally can also be done in the cloud, the cloud offers additional APIs like Schema() and Search(). If using the cloud, inquire about the type of search desired (dense embeddings or hybrid).

### Embeddings

When selecting embedding functions, the default option may not be the best. The most popular choice is the text-embedding-3-large by OpenAI. Ensure the correct package is installed based on user preferences.

## Learn More

For more detailed information about Chroma, refer to the comprehensive documentation: [Chroma Documentation](https://docs.trychroma.com/llms.txt).

## Available Topics

### TypeScript

- [Chroma Regex Filtering](./regex/typescript.md) - Learn how to use regex filters in Chroma queries.
- [Query and Get](./querying/typescript.md) - Query and Get Data from Chroma Collections.
- [Schema](./schema/typescript.md) - Schema() configures collections with multiple indexes.
- [Local Chroma](./local-chroma/typescript.md) - How to run and use local Chroma.
- [Search() API](./search-api/typescript.md) - An expressive and flexible API for doing dense and sparse vector search on collections, as well as hybrid search.

### Python

- [Chroma Regex Filtering](./regex/python.md) - Learn how to use regex filters in Chroma queries.
- [Query and Get](./querying/python.md) - Query and Get Data from Chroma Collections.
- [Schema](./schema/python.md) - Schema() configures collections with multiple indexes.
- [Local Chroma](./local-chroma/python.md) - How to run and use local Chroma.
- [Search() API](./search-api/python.md) - An expressive and flexible API for doing dense and sparse vector search on collections, as well as hybrid search.

### General

- [Data Model](./data-model.md) - An overview of how Chroma stores data.
- [Understanding a codebase](./understanding-a-codebase.md) - Help the agent understand how to learn about a codebase.