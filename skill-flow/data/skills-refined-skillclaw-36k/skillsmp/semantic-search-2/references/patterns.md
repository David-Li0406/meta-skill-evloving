# Semantic Search

## Patterns


---
  #### **Name**
Vector Database Setup with Upstash
  #### **Description**
Serverless vector search for edge and Vercel deployments
  #### **When To Use**
Need vector search without managing infrastructure, Vercel/edge deployment
  #### **Implementation**
    // lib/vector-store.ts
    import { Index } from "@upstash/vector";
    import OpenAI from "openai";
    
    const vectorIndex = new Index({
      url: process.env.UPSTASH_VECTOR_REST_URL!,
      token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
    });
    
    const openai = new OpenAI();
    
    interface Document {
      id: string;
      content: string;
      metadata: Record<string, unknown>;
    }
    
    // Generate embedding
    async function embed(text: string): Promise<number[]> {
      const response = await openai.embeddings.create({
        model: "text-embedding-3-small",
        input: text,
        dimensions: 1536, // Upstash default
      });
      return response.data[0].embedding;
    }
    
    // Index documents
    async function indexDocuments(documents: Document[]) {
      const vectors = await Promise.all(
        documents.map(async (doc) => ({
          id: doc.id,
          vector: await embed(doc.content),
          metadata: {
            ...doc.metadata,
            content: doc.content.slice(0, 1000), // Store for retrieval
          },
        }))
      );
    
      // Batch upsert (max 1000 per call)
      for (let i = 0; i < vectors.length; i += 1000) {
        await vectorIndex.upsert(vectors.slice(i, i + 1000));
      }
    
      return { indexed: vectors.length };
    }
    
    // Query with metadata filter
    async function search(
      query: string,
      options?: {
        topK?: number;
        filter?: Record<string, unknown>;
        includeMetadata?: boolean;
      }
    ) {
      const { topK = 5, filter, includeMetadata = true } = options || {};
    
      const queryVector = await embed(query);
    
      const results = await vectorIndex.query({
        vector: queryVector,
        topK,
        filter,
        includeMetadata,
      });
    
      return results.map((r) => ({
        id: r.id,
        score: r.score,
        content: r.metadata?.content,
        metadata: r.metadata,
      }));
    }
    

---
  #### **Name**
Pinecone with Serverless
  #### **Description**
Enterprise-grade vector search with Pinecone serverless
  #### **When To Use**
Need billion-scale vectors, multi-region, enterprise SLA
  #### **Implementation**
    // lib/pinecone-search.ts
    import { Pinecone } from "@pinecone-database/pinecone";
    import OpenAI from "openai";
    
    const pinecone = new Pinecone({
      apiKey: process.env.PINECONE_API_KEY!,
    });
    
    const openai = new OpenAI();
    const index = pinecone.index("your-index-name");
    
    interface UpsertRecord {
      id: string;
      text: string;
      metadata?: Record<string, string | number | boolean>;
    }
    
    // Embed text
    async function embed(texts: string[]): Promise<number[][]> {
      const response = await openai.embeddings.create({
        model: "text-embedding-3-small",
        input: texts,
      });
      return response.data.map((d) => d.embedding);
    }
    
    // Batch upsert with namespace
    async function upsertDocuments(
      records: UpsertRecord[],
      namespace?: string
    ) {
      const batchSize = 100;
      const ns = index.namespace(namespace || "");
    
      for (let i = 0; i < records.length; i += batchSize) {
        const batch = records.slice(i, i + batchSize);
        const embeddings = await embed(batch.map((r) => r.text));
    
        await ns.upsert(
          batch.map((record, idx) => ({
            id: record.id,
            values: embeddings[idx],
            metadata: {
              ...record.metadata,
              text: record.text.slice(0, 40000), // Pinecone metadata limit
            },
          }))
        );
      }
    
      return { upserted: records.length };
    }
    
    // Query with filters
    async function query(
      queryText: string,
      options?: {
        topK?: number;
        namespace?: string;
        filter?: Record<string, unknown>;
      }
    ) {
      const { topK = 10, namespace, filter } = options || {};
    
      const [queryEmbedding] = await embed([queryText]);
      const ns = index.namespace(namespace || "");
    
      const results = await ns.query({
        vector: queryEmbedding,
        topK,
        filter,
        includeMetadata: true,
      });
    
      return results.matches?.map((m) => ({
        id: m.id,
        score: m.score,
        text: m.metadata?.text,
        metadata: m.metadata,
      })) || [];
    }
    
    // Delete by filter
    async function deleteByMetadata(
      filter: Record<string, unknown>,
      namespace?: string
    ) {
      const ns = index.namespace(namespace || "");
      await ns.deleteMany({ filter });
    }
    

---
  #### **Name**
Hybrid Search with Qdrant
  #### **Description**
Combined vector + keyword search with Qdrant
  #### **When To Use**
Need complex filtering, hybrid search, self-hosted option
  #### **Implementation**
    // lib/qdrant-hybrid.ts
    import { QdrantClient } from "@qdrant/js-client-rest";
    import OpenAI from "openai";
    
    const qdrant = new QdrantClient({
      url: process.env.QDRANT_URL || "http://localhost:6333",
      apiKey: process.env.QDRANT_API_KEY,
    });
    
    const openai = new OpenAI();
    const COLLECTION_NAME = "documents";
    
    // Create collection with hybrid search
    async function createCollection() {
      await qdrant.createCollection(COLLECTION_NAME, {
        vectors: {
          size: 1536,
          distance: "Cosine",
        },
        sparse_vectors: {
          text: {}, // For BM25-style keyword matching
        },
        optimizers_config: {
          default_segment_number: 2,
        },
      });
    
      // Create payload index for filtering
      await qdrant.createPayloadIndex(COLLECTION_NAME, {
        field_name: "category",
        field_schema: "keyword",
      });
    }
    
    // Generate sparse vector from text (simple BM25-like)
    function sparseEncode(text: string): { indices: number[]; values: number[] } {
      const words = text.toLowerCase().split(/\W+/).filter(Boolean);
      const termFreq: Record<string, number> = {};
    
      for (const word of words) {
        termFreq[word] = (termFreq[word] || 0) + 1;
      }
    
      // Simple hashing for indices
      const indices: number[] = [];
      const values: number[] = [];
    
      for (const [term, freq] of Object.entries(termFreq)) {
        const hash = term.split("").reduce((a, c) => a + c.charCodeAt(0), 0) % 30000;
        indices.push(hash);
        values.push(Math.log(1 + freq)); // TF-IDF-like
      }
    
      return { indices, values };
    }
    
    // Upsert with both dense and sparse vectors
    async function upsertHybrid(
      documents: Array<{ id: string; text: string; metadata?: Record<string, unknown> }>
    ) {
      const embeddings = await Promise.all(
        documents.map(async (doc) => {
          const response = await openai.embeddings.create({
            model: "text-embedding-3-small",
            input: doc.text,
          });
          return response.data[0].embedding;
        })
      );
    
      const points = documents.map((doc, i) => ({
        id: doc.id,
        vector: embeddings[i],
        sparse_vectors: {
          text: sparseEncode(doc.text),
        },
        payload: {
          text: doc.text,
          ...doc.metadata,
        },
      }));
    
      await qdrant.upsert(COLLECTION_NAME, { points, wait: true });
    }
    
    // Hybrid search with RRF fusion
    async function hybridSearch(
      query: string,
      options?: {
        topK?: number;
        filter?: Record<string, unknown>;
        denseWeight?: number; // 0-1, default 0.7
      }
    ) {
      const { topK = 10, filter, denseWeight = 0.7 } = options || {};
    
      // Get dense embedding
      const response = await openai.embeddings.create({
        model: "text-embedding-3-small",
        input: query,
      });
      const denseVector = response.data[0].embedding;
      const sparseVector = sparseEncode(query);
    
      // Hybrid query with prefetch
      const results = await qdrant.query(COLLECTION_NAME, {
        prefetch: [
          {
            query: denseVector,
            using: "default",
            limit: topK * 2,
          },
          {
            query: {
              indices: sparseVector.indices,
              values: sparseVector.values,
            },
            using: "text",
            limit: topK * 2,
          },
        ],
        query: { fusion: "rrf" }, // Reciprocal Rank Fusion
        limit: topK,
        filter: filter
          ? {
              must: Object.entries(filter).map(([key, value]) => ({
                key,
                match: { value },
              })),
            }
          : undefined,
        with_payload: true,
      });
    
      return results.map((r) => ({
        id: r.id,
        score: r.score,
        text: r.payload?.text,
        metadata: r.payload,
      }));
    }
    

---
  #### **Name**
Semantic Chunking
  #### **Description**
Smart document chunking that preserves context
  #### **When To Use**
Indexing documents for RAG, need coherent chunks
  #### **Implementation**
    // lib/chunking.ts
    import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
    
    interface Chunk {
      content: string;
      metadata: {
        pageNumber?: number;
        section?: string;
        chunkIndex: number;
        startChar: number;
        endChar: number;
      };
    }
    
    // Basic recursive chunking with overlap
    async function chunkDocument(
      text: string,
      options?: {
        chunkSize?: number;
        chunkOverlap?: number;
        separators?: string[];
      }
    ): Promise<Chunk[]> {
      const {
        chunkSize = 1000,
        chunkOverlap = 200,
        separators = ["\n\n", "\n", ". ", " ", ""],
      } = options || {};
    
      const splitter = new RecursiveCharacterTextSplitter({
        chunkSize,
        chunkOverlap,
        separators,
      });
    
      const docs = await splitter.createDocuments([text]);
    
      return docs.map((doc, i) => ({
        content: doc.pageContent,
        metadata: {
          chunkIndex: i,
          startChar: doc.metadata.loc?.start || 0,
          endChar: doc.metadata.loc?.end || doc.pageContent.length,
        },
      }));
    }
    
    // Semantic chunking with sentence boundaries
    function semanticChunk(
      text: string,
      options?: {
        targetSize?: number;
        maxSize?: number;
        preserveHeaders?: boolean;
      }
    ): Chunk[] {
      const { targetSize = 800, maxSize = 1200, preserveHeaders = true } = options || {};
    
      // Split into sentences
      const sentences = text.match(/[^.!?]+[.!?]+\s*/g) || [text];
      const chunks: Chunk[] = [];
    
      let currentChunk = "";
      let currentSection = "";
      let chunkStart = 0;
      let charPos = 0;
    
      for (const sentence of sentences) {
        // Detect section headers
        if (preserveHeaders && /^#+\s+/.test(sentence.trim())) {
          // If we have content, save it
          if (currentChunk.trim()) {
            chunks.push({
              content: currentSection
                ? `## ${currentSection}\n\n${currentChunk.trim()}`
                : currentChunk.trim(),
              metadata: {
                section: currentSection,
                chunkIndex: chunks.length,
                startChar: chunkStart,
                endChar: charPos,
              },
            });
          }
          currentSection = sentence.replace(/^#+\s+/, "").trim();
          currentChunk = "";
          chunkStart = charPos;
        } else if (currentChunk.length + sentence.length > maxSize) {
          // Save current chunk
          if (currentChunk.trim()) {
            chunks.push({
              content: currentSection
                ? `## ${currentSection}\n\n${currentChunk.trim()}`
                : currentChunk.trim(),
              metadata: {
                section: currentSection,
                chunkIndex: chunks.length,
                startChar: chunkStart,
                endChar: charPos,
              },
            });
          }
          currentChunk = sentence;
          chunkStart = charPos;
        } else {
          currentChunk += sentence;
        }
        charPos += sentence.length;
      }
    
      // Save last chunk
      if (currentChunk.trim()) {
        chunks.push({
          content: currentSection
            ? `## ${currentSection}\n\n${currentChunk.trim()}`
            : currentChunk.trim(),
          metadata: {
            section: currentSection,
            chunkIndex: chunks.length,
            startChar: chunkStart,
            endChar: charPos,
          },
        });
      }
    
      return chunks;
    }
    
    // Estimate tokens (rough: 4 chars per token)
    function estimateTokens(text: string): number {
      return Math.ceil(text.length / 4);
    }
    

---
  #### **Name**
Reranking with Cohere
  #### **Description**
Second-stage reranking for precision
  #### **When To Use**
Need high-precision retrieval, have latency budget for reranking
  #### **Implementation**
    // lib/reranker.ts
    import { CohereClient } from "cohere-ai";
    
    const cohere = new CohereClient({
      token: process.env.COHERE_API_KEY!,
    });
    
    interface RerankResult {
      id: string;
      text: string;
      originalScore: number;
      rerankScore: number;
      metadata?: Record<string, unknown>;
    }
    
    // Rerank search results
    async function rerankResults(
      query: string,
      documents: Array<{ id: string; text: string; score: number; metadata?: Record<string, unknown> }>,
      options?: {
        topN?: number;
        model?: "rerank-english-v3.0" | "rerank-multilingual-v3.0" | "rerank-v3.5";
      }
    ): Promise<RerankResult[]> {
      const { topN = 5, model = "rerank-v3.5" } = options || {};
    
      if (documents.length === 0) return [];
    
      const response = await cohere.rerank({
        model,
        query,
        documents: documents.map((d) => d.text),
        topN,
        returnDocuments: false,
      });
    
      return response.results.map((result) => {
        const original = documents[result.index];
        return {
          id: original.id,
          text: original.text,
          originalScore: original.score,
          rerankScore: result.relevanceScore,
          metadata: original.metadata,
        };
      });
    }
    
    // Full retrieval pipeline with reranking
    async function retrieveAndRerank(
      query: string,
      vectorSearch: (query: string, topK: number) => Promise<
        Array<{ id: string; text: string; score: number; metadata?: Record<string, unknown> }>
      >,
      options?: {
        retrieveK?: number; // How many to retrieve
        rerankK?: number;   // How many to keep after reranking
      }
    ): Promise<RerankResult[]> {
      const { retrieveK = 20, rerankK = 5 } = options || {};
    
      // Stage 1: Vector retrieval (cast wide net)
      const candidates = await vectorSearch(query, retrieveK);
    
      if (candidates.length === 0) return [];
    
      // Stage 2: Rerank for precision
      const reranked = await rerankResults(query, candidates, { topN: rerankK });
    
      return reranked;
    }
    

---
  #### **Name**
LlamaIndex RAG Pipeline
  #### **Description**
Complete RAG pipeline with LlamaIndex TypeScript
  #### **When To Use**
Building RAG app in TypeScript, need full pipeline
  #### **Implementation**
    // lib/rag-pipeline.ts
    import {
      Document,
      VectorStoreIndex,
      SimpleDirectoryReader,
      OpenAIEmbedding,
      Settings,
      serviceContextFromDefaults,
    } from "llamaindex";
    import { PineconeVectorStore } from "@llamaindex/pinecone";
    import { Pinecone } from "@pinecone-database/pinecone";
    
    // Configure LlamaIndex settings
    Settings.embedModel = new OpenAIEmbedding({
      model: "text-embedding-3-small",
    });
    
    // Initialize Pinecone client
    const pinecone = new Pinecone({
      apiKey: process.env.PINECONE_API_KEY!,
    });
    
    // Create vector store
    async function createVectorStore(indexName: string) {
      const pineconeIndex = pinecone.index(indexName);
    
      return new PineconeVectorStore({
        pineconeIndex,
      });
    }
    
    // Index documents
    async function indexDocuments(
      documentsPath: string,
      indexName: string
    ) {
      // Load documents
      const reader = new SimpleDirectoryReader();
      const documents = await reader.loadData(documentsPath);
    
      // Create vector store
      const vectorStore = await createVectorStore(indexName);
    
      // Build index
      const index = await VectorStoreIndex.fromDocuments(documents, {
        vectorStore,
      });
    
      return index;
    }
    
    // Query with context
    async function queryRAG(
      query: string,
      indexName: string,
      options?: {
        topK?: number;
        systemPrompt?: string;
      }
    ) {
      const { topK = 3, systemPrompt } = options || {};
    
      const vectorStore = await createVectorStore(indexName);
    
      const index = await VectorStoreIndex.fromVectorStore(vectorStore);
    
      const queryEngine = index.asQueryEngine({
        similarityTopK: topK,
      });
    
      const response = await queryEngine.query({
        query,
      });
    
      return {
        answer: response.response,
        sourceNodes: response.sourceNodes?.map((node) => ({
          text: node.node.text,
          score: node.score,
          metadata: node.node.metadata,
        })),
      };
    }
    
    // Chat with history
    async function chatRAG(
      message: string,
      indexName: string,
      history: Array<{ role: "user" | "assistant"; content: string }>
    ) {
      const vectorStore = await createVectorStore(indexName);
      const index = await VectorStoreIndex.fromVectorStore(vectorStore);
    
      const chatEngine = index.asChatEngine({
        similarityTopK: 3,
      });
    
      // Add history
      for (const msg of history) {
        if (msg.role === "user") {
          chatEngine.chatHistory.addMessage({
            role: "user",
            content: msg.content,
          });
        } else {
          chatEngine.chatHistory.addMessage({
            role: "assistant",
            content: msg.content,
          });
        }
      }
    
      const response = await chatEngine.chat({ message });
    
      return {
        answer: response.response,
        sources: response.sourceNodes?.map((n) => n.node.text),
      };
    }
    

---
  #### **Name**
Voyage AI Embeddings
  #### **Description**
High-performance embeddings with Voyage AI
  #### **When To Use**
Need best-in-class retrieval accuracy, budget allows
  #### **Implementation**
    // lib/voyage-embeddings.ts
    interface VoyageEmbedding {
      embedding: number[];
      usage: { total_tokens: number };
    }
    
    interface VoyageResponse {
      data: Array<{ embedding: number[] }>;
      usage: { total_tokens: number };
    }
    
    const VOYAGE_API_URL = "https://api.voyageai.com/v1/embeddings";
    
    async function voyageEmbed(
      texts: string[],
      options?: {
        model?: "voyage-3" | "voyage-3-lite" | "voyage-large-2" | "voyage-code-2";
        inputType?: "query" | "document";
      }
    ): Promise<{ embeddings: number[][]; totalTokens: number }> {
      const {
        model = "voyage-3-lite", // Good balance of cost/quality
        inputType = "document",
      } = options || {};
    
      const response = await fetch(VOYAGE_API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.VOYAGE_API_KEY}`,
        },
        body: JSON.stringify({
          input: texts,
          model,
          input_type: inputType,
        }),
      });
    
      if (!response.ok) {
        throw new Error(`Voyage API error: ${response.statusText}`);
      }
    
      const data: VoyageResponse = await response.json();
    
      return {
        embeddings: data.data.map((d) => d.embedding),
        totalTokens: data.usage.total_tokens,
      };
    }
    
    // Batch embed with rate limiting
    async function batchEmbed(
      texts: string[],
      options?: {
        model?: "voyage-3" | "voyage-3-lite";
        batchSize?: number;
        delayMs?: number;
      }
    ): Promise<number[][]> {
      const { model = "voyage-3-lite", batchSize = 128, delayMs = 100 } = options || {};
    
      const allEmbeddings: number[][] = [];
    
      for (let i = 0; i < texts.length; i += batchSize) {
        const batch = texts.slice(i, i + batchSize);
        const { embeddings } = await voyageEmbed(batch, { model });
        allEmbeddings.push(...embeddings);
    
        // Rate limit
        if (i + batchSize < texts.length) {
          await new Promise((r) => setTimeout(r, delayMs));
        }
      }
    
      return allEmbeddings;
    }
    

## Anti-Patterns


---
  #### **Name**
Single-Stage Retrieval
  #### **Description**
Using only vector search without reranking
  #### **Why Bad**
    Vector search is recall-optimized, not precision-optimized.
    First 5 results may not be the best 5. Reranking boosts
    precision by up to 48% (Databricks research).
    
  #### **Instead**
Add Cohere/Jina reranker as second stage for important queries

---
  #### **Name**
Fixed-Size Chunking
  #### **Description**
Blindly splitting at 512 or 1000 characters
  #### **Why Bad**
    Cuts sentences mid-thought, breaks context, separates related
    information. Results in incoherent chunks that embed poorly.
    
  #### **Instead**
Use semantic chunking with sentence boundaries and header preservation

---
  #### **Name**
Pure Vector Search for Exact Matches
  #### **Description**
Expecting vector search to find exact identifiers
  #### **Why Bad**
    Vector search captures semantic meaning, not exact strings.
    Query for 'E-404' may return conceptually similar errors but
    miss the exact error code in documents.
    
  #### **Instead**
Use hybrid search (vector + BM25 keyword) for production systems

---
  #### **Name**
Ignoring Embedding Model Choice
  #### **Description**
Defaulting to text-embedding-ada-002
  #### **Why Bad**
    ada-002 is outdated. text-embedding-3-small is same price with
    better performance. Voyage-3 outperforms OpenAI by 9.74% on
    retrieval benchmarks.
    
  #### **Instead**
Evaluate Voyage-3-lite ($0.02/1M) or text-embedding-3-small for your use case

---
  #### **Name**
No Metadata Filtering
  #### **Description**
Searching entire vector space for every query
  #### **Why Bad**
    Slower, less relevant. If user is asking about 'React hooks',
    searching through Python and Go documentation wastes resources.
    
  #### **Instead**
Add metadata (category, date, source) and filter before vector search

---
  #### **Name**
Embedding in Request Path
  #### **Description**
Generating embeddings on every search request
  #### **Why Bad**
    Adds 100-300ms latency per query. API rate limits become
    bottleneck under load.
    
  #### **Instead**
Pre-embed documents at index time, cache query embeddings