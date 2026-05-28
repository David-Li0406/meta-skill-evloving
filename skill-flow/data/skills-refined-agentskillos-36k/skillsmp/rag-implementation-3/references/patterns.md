# RAG Implementation

## Patterns


---
  #### **Name**
Semantic Chunking
  #### **Description**
Chunk by meaning, not arbitrary size
  #### **When**
Processing documents for RAG
  #### **Example**
    class SemanticChunker {
        async chunk(document: string): Promise<Chunk[]> {
            // Split into sentences
            const sentences = splitSentences(document);
    
            // Group by semantic similarity
            const chunks: Chunk[] = [];
            let currentChunk: string[] = [];
            let currentEmbedding: number[] | null = null;
    
            for (const sentence of sentences) {
                const embedding = await embed(sentence);
    
                if (!currentEmbedding) {
                    currentChunk.push(sentence);
                    currentEmbedding = embedding;
                    continue;
                }
    
                const similarity = cosineSimilarity(currentEmbedding, embedding);
    
                if (similarity > 0.8 && currentChunk.length < 10) {
                    // Similar enough, add to current chunk
                    currentChunk.push(sentence);
                    currentEmbedding = averageEmbeddings([currentEmbedding, embedding]);
                } else {
                    // Start new chunk
                    chunks.push({ text: currentChunk.join(' '), embedding: currentEmbedding });
                    currentChunk = [sentence];
                    currentEmbedding = embedding;
                }
            }
    
            if (currentChunk.length > 0) {
                chunks.push({ text: currentChunk.join(' '), embedding: currentEmbedding! });
            }
    
            return chunks;
        }
    }
    

---
  #### **Name**
Hybrid Search
  #### **Description**
Combine dense (vector) and sparse (keyword) search
  #### **When**
Need both semantic and exact match capability
  #### **Example**
    class HybridRetriever {
        async retrieve(query: string, k: number = 10): Promise<Document[]> {
            // Dense retrieval (semantic)
            const queryEmbedding = await embed(query);
            const denseResults = await vectorStore.search(queryEmbedding, k * 2);
    
            // Sparse retrieval (BM25/keyword)
            const sparseResults = await bm25Search(query, k * 2);
    
            // Reciprocal Rank Fusion
            const scores = new Map<string, number>();
    
            denseResults.forEach((doc, idx) => {
                const score = 1 / (60 + idx);  // RRF constant = 60
                scores.set(doc.id, (scores.get(doc.id) || 0) + score);
            });
    
            sparseResults.forEach((doc, idx) => {
                const score = 1 / (60 + idx);
                scores.set(doc.id, (scores.get(doc.id) || 0) + score);
            });
    
            // Sort by combined score
            const ranked = [...scores.entries()]
                .sort((a, b) => b[1] - a[1])
                .slice(0, k);
    
            return ranked.map(([id]) => getDocument(id));
        }
    }
    

---
  #### **Name**
Contextual Reranking
  #### **Description**
Rerank retrieved docs with LLM for relevance
  #### **When**
Top-k retrieval not accurate enough
  #### **Example**
    async function rerankWithLLM(
        query: string,
        candidates: Document[],
        topK: number = 5
    ): Promise<Document[]> {
        // Use smaller model for reranking (cost efficient)
        const prompt = `Rate these documents' relevance to the query.
        Query: "${query}"
    
        Documents:
        ${candidates.map((d, i) => `[${i}] ${d.text.slice(0, 500)}`).join('\n\n')}
    
        Return JSON: { "rankings": [{"index": 0, "score": 0.9}, ...] }
        Score 0-1 where 1 is highly relevant.`;
    
        const response = await llm.complete(prompt, { model: 'gpt-3.5-turbo' });
        const rankings = JSON.parse(response).rankings;
    
        return rankings
            .sort((a, b) => b.score - a.score)
            .slice(0, topK)
            .map(r => candidates[r.index]);
    }
    

## Anti-Patterns


---
  #### **Name**
Fixed-Size Chunking
  #### **Description**
Splitting documents at arbitrary character/token counts
  #### **Why**
Breaks sentences, loses context, poor retrieval
  #### **Instead**
Use semantic or recursive chunking that respects boundaries.

---
  #### **Name**
No Overlap
  #### **Description**
Non-overlapping chunks losing context at boundaries
  #### **Why**
Important context at chunk edges lost
  #### **Instead**
Use 10-20% overlap between chunks.

---
  #### **Name**
Single Retrieval Strategy
  #### **Description**
Only using vector search
  #### **Why**
Misses exact matches, proper nouns, codes
  #### **Instead**
Hybrid search combining dense and sparse retrieval.

---
  #### **Name**
No Evaluation
  #### **Description**
Not measuring retrieval quality
  #### **Why**
Retrieval degradation is silent, affects all downstream
  #### **Instead**
Regular evaluation with ground truth, track MRR/recall.