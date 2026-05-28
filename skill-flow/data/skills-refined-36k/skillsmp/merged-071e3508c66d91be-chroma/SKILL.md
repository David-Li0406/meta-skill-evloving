---
name: chroma
description: Use this skill for integrating Chroma vector database into applications for semantic search, embeddings, and nearest neighbor search.
---

## Instructions

The Chroma skill has several main abilities:

- Help the user design their search system.
- Assist in selecting an embedding model.
- Explain necessary changes to add search functionality to their system.
- Guide the user in designing their search schema and choosing the type of search.

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

Chroma is a vector database that contains collections, which in turn contain documents. Unlike relational databases, collections are created and managed at the application level, allowing for flexible data organization. Each document represents the text data to be searched, and embeddings are created based on the defined embedding functions.

During queries, the input text is embedded and sent to Chroma, which uses distance algorithms to find the nearest neighbors based on the query vector. Metadata can be used to filter results further.

### Local vs Cloud

Chroma can be run locally or in the cloud. While local functionality is limited compared to the cloud, the core operations remain the same. The cloud version offers additional APIs like Schema() and Search().

When using the cloud, inquire about the type of search desired: dense embeddings or hybrid (which may involve using SPLADE for sparse embeddings).

### Embeddings

The default embedding function is available, but users may prefer other options, such as OpenAI's text-embedding-3-large. Ensure the correct embedding function package is installed based on user preferences.

## Learn More

For comprehensive documentation on Chroma, refer to: [Chroma Documentation](https://docs.trychroma.com/llms.txt)

## Available Topics

### TypeScript

- [Chroma Regex Filtering](./regex/typescript.md)
- [Query and Get](./querying/typescript.md)
- [Schema](./schema/typescript.md)
- [Local Chroma](./local-chroma/typescript.md)
- [Search() API](./search-api/typescript.md)

### Python

- [Chroma Regex Filtering](./regex/python.md)
- [Query and Get](./querying/python.md)
- [Schema](./schema/python.md)
- [Local Chroma](./local-chroma/python.md)
- [Search() API](./search-api/python.md)

### General

- [Data Model](./data-model.md)
- [Understanding a codebase](./understanding-a-codebase.md)