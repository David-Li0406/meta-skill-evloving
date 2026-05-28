---
name: rag-architecture
description: Expert architecture RAG - Design, patterns, et implementation complete
---

# RAG Architecture

Tu es expert en **architecture RAG** (Retrieval Augmented Generation).

## Pourquoi RAG ?

| Probleme LLM | Solution RAG |
|--------------|--------------|
| Connaissances datees | Donnees a jour |
| Hallucinations | Sources verifiables |
| Pas de donnees privees | Vos documents |
| Contexte limite | Retrieval cible |

## Architecture Overview

```mermaid
flowchart TB
    subgraph INGESTION["📥 Ingestion Pipeline"]
        D[Documents] --> L[Loader]
        L --> S[Splitter]
        S --> C[Chunks]
        C --> E[Embeddings]
        E --> V[(Vector DB)]
    end

    subgraph RETRIEVAL["🔍 Retrieval Pipeline"]
        Q[Query] --> QE[Query Embedding]
        QE --> VS[Vector Search]
        V --> VS
        VS --> RR[Reranker]
        RR --> CTX[Context]
    end

    subgraph GENERATION["🤖 Generation Pipeline"]
        CTX --> P[Prompt Builder]
        Q --> P
        P --> LLM[LLM]
        LLM --> R[Response]
    end

    style INGESTION fill:#e1f5fe
    style RETRIEVAL fill:#fff3e0
    style GENERATION fill:#e8f5e9
```

## Types avec Validation Zod

```typescript
// types.ts
import { z } from 'zod';

// Schemas de validation
export const DocumentSchema = z.object({
  id: z.string().uuid(),
  content: z.string().min(1),
  metadata: z.object({
    source: z.string().optional(),
    createdAt: z.coerce.date().optional(),
    category: z.string().optional(),
  }).passthrough(),
});

export const ChunkSchema = z.object({
  id: z.string().uuid(),
  documentId: z.string().uuid(),
  content: z.string().min(1),
  embedding: z.array(z.number()).length(1536), // OpenAI dimensions
  metadata: z.record(z.unknown()),
});

export const RetrievalResultSchema = z.object({
  chunk: ChunkSchema.omit({ embedding: true }),
  score: z.number().min(0).max(1),
});

export const RAGQuerySchema = z.object({
  question: z.string().min(1).max(2000),
  filters: z.object({
    category: z.string().optional(),
    dateFrom: z.coerce.date().optional(),
    dateTo: z.coerce.date().optional(),
  }).optional(),
  topK: z.number().int().min(1).max(20).default(4),
});

// Types inferes
export type Document = z.infer<typeof DocumentSchema>;
export type Chunk = z.infer<typeof ChunkSchema>;
export type RetrievalResult = z.infer<typeof RetrievalResultSchema>;
export type RAGQuery = z.infer<typeof RAGQuerySchema>
```

### Configuration

```typescript
// config/rag.ts
import { z } from 'zod';

// Schema de configuration avec defaults
const RAGConfigSchema = z.object({
  // Chunking
  chunkSize: z.coerce.number().int().min(100).max(4000).default(1000),
  chunkOverlap: z.coerce.number().int().min(0).max(500).default(200),

  // Retrieval
  topK: z.coerce.number().int().min(1).max(50).default(4),
  similarityThreshold: z.coerce.number().min(0).max(1).default(0.7),

  // LLM
  llmModel: z.string().default('gpt-4o'),
  embeddingModel: z.string().default('text-embedding-3-small'),
  temperature: z.coerce.number().min(0).max(2).default(0),

  // Database
  tableName: z.string().default('documents'),
  embeddingDimension: z.coerce.number().int().default(1536),

  // Timeouts (ms)
  embeddingTimeout: z.coerce.number().int().default(30_000),
  llmTimeout: z.coerce.number().int().default(60_000),
  dbQueryTimeout: z.coerce.number().int().default(10_000),

  // Connection pool
  poolMin: z.coerce.number().int().min(1).default(2),
  poolMax: z.coerce.number().int().min(1).default(10),
  poolIdleTimeout: z.coerce.number().int().default(30_000),
});

export type RAGConfig = z.infer<typeof RAGConfigSchema>;

// Charger depuis env avec validation
export function loadRAGConfig(): RAGConfig {
  return RAGConfigSchema.parse({
    chunkSize: process.env.RAG_CHUNK_SIZE,
    chunkOverlap: process.env.RAG_CHUNK_OVERLAP,
    topK: process.env.RAG_TOP_K,
    similarityThreshold: process.env.RAG_SIMILARITY_THRESHOLD,
    llmModel: process.env.RAG_LLM_MODEL,
    embeddingModel: process.env.RAG_EMBEDDING_MODEL,
    temperature: process.env.RAG_TEMPERATURE,
    tableName: process.env.RAG_TABLE_NAME,
    embeddingDimension: process.env.RAG_EMBEDDING_DIMENSION,
    embeddingTimeout: process.env.RAG_EMBEDDING_TIMEOUT,
    llmTimeout: process.env.RAG_LLM_TIMEOUT,
    dbQueryTimeout: process.env.RAG_DB_QUERY_TIMEOUT,
    poolMin: process.env.RAG_POOL_MIN,
    poolMax: process.env.RAG_POOL_MAX,
    poolIdleTimeout: process.env.RAG_POOL_IDLE_TIMEOUT,
  });
}

// Exemple .env
// RAG_CHUNK_SIZE=1000
// RAG_CHUNK_OVERLAP=200
// RAG_TOP_K=4
// RAG_LLM_MODEL=gpt-4o
// RAG_EMBEDDING_MODEL=text-embedding-3-small
```

### Pipeline Complet

```typescript
// rag-pipeline.ts
import { OpenAIEmbeddings } from '@langchain/openai';
import { PGVectorStore } from '@langchain/community/vectorstores/pgvector';
import { ChatOpenAI } from '@langchain/openai';
import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { loadRAGConfig, type RAGConfig } from './config/rag';

class RAGPipeline {
  private embeddings: OpenAIEmbeddings;
  private vectorStore: PGVectorStore | null = null;
  private llm: ChatOpenAI;
  private splitter: RecursiveCharacterTextSplitter;
  private config: RAGConfig;
  private isInitialized = false;

  constructor(config?: Partial<RAGConfig>) {
    // Merge provided config with env/defaults
    this.config = { ...loadRAGConfig(), ...config };

    this.embeddings = new OpenAIEmbeddings({
      model: this.config.embeddingModel,
      timeout: this.config.embeddingTimeout,
    });

    this.llm = new ChatOpenAI({
      model: this.config.llmModel,
      temperature: this.config.temperature,
      timeout: this.config.llmTimeout,
    });

    this.splitter = new RecursiveCharacterTextSplitter({
      chunkSize: this.config.chunkSize,
      chunkOverlap: this.config.chunkOverlap,
    });
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    this.vectorStore = await PGVectorStore.initialize(this.embeddings, {
      postgresConnectionOptions: {
        connectionString: process.env.DATABASE_URL,
        // Connection pool settings
        max: this.config.poolMax,
        min: this.config.poolMin,
        idleTimeoutMillis: this.config.poolIdleTimeout,
        connectionTimeoutMillis: this.config.dbQueryTimeout,
      },
      tableName: this.config.tableName,
      columns: {
        idColumnName: 'id',
        vectorColumnName: 'embedding',
        contentColumnName: 'content',
        metadataColumnName: 'metadata',
      },
    });

    this.isInitialized = true;
  }

  // Cleanup resources
  async close(): Promise<void> {
    if (this.vectorStore) {
      await this.vectorStore.end();
      this.vectorStore = null;
      this.isInitialized = false;
    }
  }

  // 1. INGESTION
  async ingest(documents: Document[]): Promise<void> {
    if (!this.vectorStore) throw new Error('Pipeline not initialized');

    for (const doc of documents) {
      const chunks = await this.splitter.createDocuments(
        [doc.content],
        [{ documentId: doc.id, ...doc.metadata }]
      );

      await this.vectorStore.addDocuments(chunks);
    }
  }

  // 2. RETRIEVAL
  async retrieve(query: string, k?: number): Promise<RetrievalResult[]> {
    if (!this.vectorStore) throw new Error('Pipeline not initialized');

    const topK = k ?? this.config.topK;
    const results = await this.vectorStore.similaritySearchWithScore(query, topK);

    return results
      .filter(([, score]) => score >= this.config.similarityThreshold)
      .map(([doc, score]) => ({
        chunk: {
          id: doc.id,
          documentId: doc.metadata.documentId,
          content: doc.pageContent,
          embedding: [],
          metadata: doc.metadata,
        },
        score,
      }));
  }

  // 3. GENERATION
  async generate(query: string, context: RetrievalResult[]): Promise<string> {
    const contextText = context
      .map((r) => r.chunk.content)
      .join('\n\n---\n\n');

    const prompt = `Tu es un assistant qui repond aux questions en utilisant uniquement le contexte fourni.

CONTEXTE:
${contextText}

QUESTION: ${query}

INSTRUCTIONS:
- Reponds uniquement avec les informations du contexte
- Si l'information n'est pas dans le contexte, dis-le
- Cite les sources quand possible

REPONSE:`;

    const response = await this.llm.invoke(prompt);
    return response.content as string;
  }

  // Pipeline complet
  async query(question: string): Promise<{
    answer: string;
    sources: RetrievalResult[];
  }> {
    const sources = await this.retrieve(question);
    const answer = await this.generate(question, sources);

    return { answer, sources };
  }
}
```

## Strategies de Chunking

| Strategie | Use Case | Taille |
|-----------|----------|--------|
| Fixed size | General | 500-1000 tokens |
| Semantic | Documents structures | Variable |
| Sentence | Q&A precis | 1-3 phrases |
| Paragraph | Articles, blogs | ~500 tokens |
| Recursive | Code, markdown | Variable |

```typescript
// Chunking semantique avec structure
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 1000,
  chunkOverlap: 200,
  separators: ['\n\n', '\n', '. ', ' ', ''],
});

// Pour le code
const codeSplitter = RecursiveCharacterTextSplitter.fromLanguage('typescript', {
  chunkSize: 2000,
  chunkOverlap: 200,
});
```

## Strategies de Retrieval

### Similarity Search (Base)

```typescript
const results = await vectorStore.similaritySearch(query, 4);
```

### Hybrid Search (Semantic + Keyword)

```typescript
// Avec Weaviate ou autre DB supportant hybrid
const results = await vectorStore.similaritySearch(query, 4, {
  hybridSearch: {
    query,
    alpha: 0.5, // 0 = keyword only, 1 = semantic only
  },
});
```

### MMR (Maximum Marginal Relevance)

```typescript
// Diversifie les resultats
const results = await vectorStore.maxMarginalRelevanceSearch(query, {
  k: 4,
  fetchK: 20,
  lambda: 0.5, // Balance relevance/diversity
});
```

### Reranking

```typescript
import { CohereRerank } from '@langchain/cohere';

const reranker = new CohereRerank({
  model: 'rerank-english-v3.0',
});

// Recuperer plus de documents
const initialResults = await vectorStore.similaritySearch(query, 20);

// Reranker pour affiner
const rerankedResults = await reranker.compressDocuments(initialResults, query);
const topResults = rerankedResults.slice(0, 4);
```

## Optimisation du Prompt

```typescript
const RAG_PROMPT = `Tu es un assistant expert qui repond aux questions en utilisant les documents fournis.

DOCUMENTS SOURCES:
{context}

QUESTION DE L'UTILISATEUR:
{question}

INSTRUCTIONS:
1. Base ta reponse UNIQUEMENT sur les documents fournis
2. Si l'information n'est pas dans les documents, reponds "Je n'ai pas trouve cette information dans les documents disponibles."
3. Cite les sources pertinentes entre crochets [Source: nom_du_document]
4. Structure ta reponse de maniere claire

REPONSE:`;
```

## Metriques de Qualite

| Metrique | Description | Cible |
|----------|-------------|-------|
| **Faithfulness** | Reponse basee sur le contexte | > 0.9 |
| **Answer Relevance** | Reponse pertinente a la question | > 0.8 |
| **Context Relevance** | Contexte pertinent | > 0.7 |
| **Context Recall** | Infos importantes recuperees | > 0.8 |

## Patterns Avances

### Parent Document Retriever

```typescript
// Stocker les chunks, retourner le document parent
// Meilleur contexte pour le LLM
```

### HyDE (Hypothetical Document Embeddings)

```typescript
// 1. LLM genere une reponse hypothetique
// 2. Embed cette reponse
// 3. Recherche avec cet embedding
// Meilleur pour questions complexes
```

### CRAG (Corrective RAG)

```typescript
// 1. Evaluer la pertinence des documents
// 2. Si faible: web search ou reformulation
// 3. Generer avec documents corriges
```

## Configuration Recommandee

### Connection Pool (PostgreSQL/pgvector)

```typescript
// Recommandations par environnement
const POOL_CONFIGS = {
  development: {
    min: 2,
    max: 5,
    idleTimeoutMillis: 30_000,
    connectionTimeoutMillis: 5_000,
  },
  production: {
    min: 5,
    max: 20,
    idleTimeoutMillis: 60_000,
    connectionTimeoutMillis: 10_000,
  },
  serverless: {
    min: 0,  // Scale to zero
    max: 1,  // Un seul client par instance
    idleTimeoutMillis: 10_000,
    connectionTimeoutMillis: 5_000,
  },
};

// Formule: max_connections = (num_cores * 2) + effective_spindle_count
// Pour 4 cores: max = (4 * 2) + 1 = 9
```

### Timeouts Recommandes

| Operation | Dev | Prod | Notes |
|-----------|-----|------|-------|
| **Embedding** | 30s | 30s | Stable, batch si > 100 docs |
| **LLM** | 60s | 120s | Augmenter pour contexts longs |
| **DB Query** | 5s | 10s | Index si > 10s |
| **Total Request** | 120s | 300s | API Gateway timeout |

### Resource Management

```typescript
// Pattern: Using with cleanup
async function processQuery(question: string) {
  const pipeline = new RAGPipeline();

  try {
    await pipeline.initialize();
    return await pipeline.query(question);
  } finally {
    await pipeline.close(); // Toujours cleanup
  }
}

// Pattern: Singleton pour API
let pipelineInstance: RAGPipeline | null = null;

export async function getPipeline(): Promise<RAGPipeline> {
  if (!pipelineInstance) {
    pipelineInstance = new RAGPipeline();
    await pipelineInstance.initialize();

    // Cleanup on process exit
    process.on('SIGTERM', async () => {
      await pipelineInstance?.close();
      process.exit(0);
    });
  }
  return pipelineInstance;
}
```

## Voir Aussi

- `rag/chunking` pour strategies de decoupage
- `rag/retrieval` pour strategies de recherche
- `vectors/` pour choix de vector DB
- `rag/evaluation` pour mesurer la qualite
