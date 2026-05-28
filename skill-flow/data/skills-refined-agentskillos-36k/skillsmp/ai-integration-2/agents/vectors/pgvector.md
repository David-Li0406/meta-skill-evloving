---
name: pgvector
description: Expert pgvector - Vector search dans PostgreSQL
---

# pgvector - PostgreSQL Vector Database

Tu es expert en **pgvector** pour ajouter la recherche vectorielle a PostgreSQL.

## Pourquoi pgvector ?

- **Simplicite** : Si vous avez deja PostgreSQL
- **Gratuit** : Extension open source
- **Transactions** : ACID avec vos donnees relationnelles
- **SQL** : Requetes familieres
- **Ecosystem** : Supabase, Neon, RDS supportent pgvector

## Setup

### Installation

```sql
-- PostgreSQL
CREATE EXTENSION vector;

-- Verifier
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Schema de Base

```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  embedding vector(1536),  -- OpenAI text-embedding-3-small
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour recherche rapide
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Ou HNSW (plus rapide, plus de RAM)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

## Operations de Base

### Insertion

```sql
INSERT INTO documents (content, metadata, embedding)
VALUES (
  'Contenu du document',
  '{"source": "manual", "category": "faq"}',
  '[0.1, 0.2, ...]'::vector
);
```

### Recherche par Similarite

```sql
-- Cosine similarity (recommande)
SELECT id, content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 5;

-- Euclidean distance
SELECT id, content, embedding <-> query_embedding AS distance
FROM documents
ORDER BY embedding <-> query_embedding
LIMIT 5;

-- Inner product
SELECT id, content, embedding <#> query_embedding AS inner_product
FROM documents
ORDER BY embedding <#> query_embedding
LIMIT 5;
```

### Avec Filtres

```sql
SELECT id, content, 1 - (embedding <=> $1) AS similarity
FROM documents
WHERE metadata->>'category' = 'faq'
  AND created_at > NOW() - INTERVAL '30 days'
ORDER BY embedding <=> $1
LIMIT 5;
```

## Integration Node.js

### Avec Drizzle ORM

```typescript
// schema.ts
import { pgTable, serial, text, jsonb, timestamp } from 'drizzle-orm/pg-core';
import { vector } from 'pgvector/drizzle-orm';

export const documents = pgTable('documents', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  metadata: jsonb('metadata').default({}),
  embedding: vector('embedding', { dimensions: 1536 }),
  createdAt: timestamp('created_at').defaultNow(),
});
```

```typescript
// rag.ts
import { db } from './db';
import { documents } from './schema';
import { cosineDistance, desc, sql } from 'drizzle-orm';
import OpenAI from 'openai';

const openai = new OpenAI();

async function embed(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  return response.data[0].embedding;
}

async function addDocument(content: string, metadata: object = {}) {
  const embedding = await embed(content);

  await db.insert(documents).values({
    content,
    metadata,
    embedding,
  });
}

async function search(query: string, limit: number = 5) {
  const queryEmbedding = await embed(query);

  const results = await db
    .select({
      id: documents.id,
      content: documents.content,
      metadata: documents.metadata,
      similarity: sql<number>`1 - (${documents.embedding} <=> ${queryEmbedding}::vector)`,
    })
    .from(documents)
    .orderBy(desc(sql`1 - (${documents.embedding} <=> ${queryEmbedding}::vector)`))
    .limit(limit);

  return results;
}
```

### Avec Prisma

```prisma
// schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [vector]
}

model Document {
  id        Int      @id @default(autoincrement())
  content   String
  metadata  Json     @default("{}")
  embedding Unsupported("vector(1536)")?
  createdAt DateTime @default(now())
}
```

```typescript
// rag.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function search(queryEmbedding: number[], limit: number = 5) {
  const results = await prisma.$queryRaw`
    SELECT id, content, metadata,
           1 - (embedding <=> ${queryEmbedding}::vector) AS similarity
    FROM "Document"
    ORDER BY embedding <=> ${queryEmbedding}::vector
    LIMIT ${limit}
  `;

  return results;
}
```

### Avec LangChain

```typescript
import { OpenAIEmbeddings } from '@langchain/openai';
import { PGVectorStore } from '@langchain/community/vectorstores/pgvector';

const embeddings = new OpenAIEmbeddings({
  model: 'text-embedding-3-small',
});

const vectorStore = await PGVectorStore.initialize(embeddings, {
  postgresConnectionOptions: {
    connectionString: process.env.DATABASE_URL,
  },
  tableName: 'documents',
  columns: {
    idColumnName: 'id',
    vectorColumnName: 'embedding',
    contentColumnName: 'content',
    metadataColumnName: 'metadata',
  },
});

// Ajouter des documents
await vectorStore.addDocuments([
  { pageContent: 'Contenu 1', metadata: { source: 'doc1' } },
  { pageContent: 'Contenu 2', metadata: { source: 'doc2' } },
]);

// Rechercher
const results = await vectorStore.similaritySearch('ma question', 4);
```

## Indexing

### IVFFlat (Approximate)

```sql
-- Bon compromis vitesse/precision
-- lists = sqrt(nombre_de_lignes)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Requete avec probes (plus = plus precis, plus lent)
SET ivfflat.probes = 10;
```

### HNSW (Faster)

```sql
-- Plus rapide, plus de RAM
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Requete
SET hnsw.ef_search = 40;
```

### Quand indexer ?

| Nombre de vecteurs | Index |
|--------------------|-------|
| < 10k | Pas necessaire |
| 10k - 100k | IVFFlat |
| > 100k | HNSW |

## Optimisation

### Performance

```sql
-- Analyser les requetes
EXPLAIN ANALYZE
SELECT id, content
FROM documents
ORDER BY embedding <=> '[...]'::vector
LIMIT 5;

-- Vacuum regulier
VACUUM ANALYZE documents;
```

### Dimension Reduction

```typescript
// Si 1536 dimensions trop lourd
const embedding = await openai.embeddings.create({
  model: 'text-embedding-3-small',
  input: text,
  dimensions: 512,  // Reduire a 512
});
```

## Voir Aussi

- `vectors/embeddings` pour generation
- `rag/architecture` pour pipeline complet
- `backend-developer` pour PostgreSQL
