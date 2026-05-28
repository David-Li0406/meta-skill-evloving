# Search Patterns for Qdrant

## Basic Semantic Search

```typescript
import { QdrantClient } from '@qdrant/js-client';
import OpenAI from 'openai';

const qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function semanticSearch(query: string, limit = 5) {
  // 1. Generate query embedding
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: query,
  });
  
  const queryVector = embedding.data[0].embedding;
  
  // 2. Search Qdrant
  const results = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    limit,
    with_payload: true,
    score_threshold: 0.7, // Only return relevant results
  });
  
  // 3. Format results
  return results.map(r => ({
    text: r.payload.text,
    chapter: r.payload.chapter,
    section: r.payload.section,
    score: r.score,
  }));
}
```

## Filtered Search

Search specific chapters or sections:

```typescript
async function searchByChapter(query: string, chapter: string) {
  const queryVector = await generateEmbedding(query);
  
  const results = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    filter: {
      must: [
        {
          key: 'chapter',
          match: { value: chapter },
        },
      ],
    },
    limit: 5,
    with_payload: true,
  });
  
  return results;
}
```

## Multi-Filter Search

```typescript
async function searchROS2Code(query: string) {
  const queryVector = await generateEmbedding(query);
  
  const results = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    filter: {
      must: [
        {
          key: 'chapter',
          match: { value: 'Chapter 2' },
        },
        {
          key: 'hasCode',
          match: { value: true },
        },
      ],
    },
    limit: 10,
    with_payload: true,
  });
  
  return results;
}
```

## Hybrid Search (Keyword + Semantic)

Combine full-text and vector search:

```typescript
async function hybridSearch(query: string) {
  const queryVector = await generateEmbedding(query);
  
  // Semantic search
  const vectorResults = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    limit: 10,
  });
  
  // Keyword search in payloads
  const keywordResults = await qdrant.scroll('textbook_chunks', {
    filter: {
      must: [
        {
          key: 'text',
          match: { text: query },
        },
      ],
    },
    limit: 10,
    with_payload: true,
  });
  
  // Merge and deduplicate results
  const combined = [...vectorResults, ...keywordResults.points];
  const unique = Array.from(new Map(combined.map(r => [r.id, r])).values());
  
  return unique.slice(0, 10);
}
```

## Batch Search

Search multiple queries at once:

```typescript
async function batchSearch(queries: string[]) {
  // Generate all embeddings
  const embeddings = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: queries,
  });
  
  // Search all at once
  const searches = embeddings.data.map(async (emb, i) => {
    const results = await qdrant.search('textbook_chunks', {
      vector: emb.embedding,
      limit: 5,
    });
    
    return {
      query: queries[i],
      results,
    };
  });
  
  return await Promise.all(searches);
}
```

## Pagination

For large result sets:

```typescript
async function paginatedSearch(query: string, page = 1, pageSize = 10) {
  const queryVector = await generateEmbedding(query);
  
  const offset = (page - 1) * pageSize;
  
  const results = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    limit: pageSize,
    offset,
    with_payload: true,
  });
  
  return {
    results,
    page,
    pageSize,
    hasMore: results.length === pageSize,
  };
}
```

## Score Thresholding

Only return high-quality matches:

```typescript
async function highQualitySearch(query: string) {
  const queryVector = await generateEmbedding(query);
  
  const results = await qdrant.search('textbook_chunks', {
    vector: queryVector,
    limit: 20, // Get more candidates
    score_threshold: 0.8, // But only keep very relevant ones
    with_payload: true,
  });
  
  // Further filter by custom logic
  return results.filter(r => {
    // Prefer recent chapters
    const chapterNum = parseInt(r.payload.chapter.match(/\d+/)?.[0] || '0');
    return chapterNum >= 3 || r.score > 0.85;
  });
}
```

## Recommendation Engine

Find similar chunks to a given chunk:

```typescript
async function findSimilarChunks(chunkId: string, limit = 5) {
  // Get the chunk's vector
  const chunk = await qdrant.retrieve('textbook_chunks', {
    ids: [chunkId],
    with_vector: true,
  });
  
  if (!chunk[0]) return [];
  
  // Search for similar vectors
  const results = await qdrant.search('textbook_chunks', {
    vector: chunk[0].vector,
    limit: limit + 1, // +1 because first result will be the chunk itself
    with_payload: true,
  });
  
  // Remove the original chunk from results
  return results.filter(r => r.id !== chunkId);
}
```

## Helper Function

Reusable embedding generator:

```typescript
async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text.trim(),
  });
  
  return response.data[0].embedding;
}
```
