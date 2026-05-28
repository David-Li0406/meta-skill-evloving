# Vector Specialist

## Patterns


---
  #### **Name**
Reciprocal Rank Fusion
  #### **Description**
Combine multiple retrieval methods for robust results
  #### **When**
Any retrieval system - always use multiple signals
  #### **Example**
    def reciprocal_rank_fusion(
        result_lists: List[List[SearchResult]],
        k: int = 60
    ) -> List[SearchResult]:
        """Combine multiple ranked lists using RRF."""
        scores: Dict[str, float] = defaultdict(float)
        items: Dict[str, SearchResult] = {}
    
        for results in result_lists:
            for rank, result in enumerate(results):
                scores[result.id] += 1.0 / (k + rank + 1)
                items[result.id] = result
    
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return [items[id] for id in sorted_ids]
    
    # Usage: Combine vector, keyword, and graph results
    fused = reciprocal_rank_fusion([
        vector_results,
        keyword_results,
        graph_neighbor_results,
    ])
    

---
  #### **Name**
Two-Stage Retrieval with Reranking
  #### **Description**
Fast first-stage retrieval, accurate second-stage reranking
  #### **When**
Quality matters more than pure speed
  #### **Example**
    async def retrieve_with_rerank(
        query: str,
        limit: int = 10
    ) -> List[Memory]:
        # Stage 1: Fast retrieval (100+ candidates)
        query_vector = await embed(query)
        candidates = await qdrant.search(
            query_vector,
            limit=limit * 5  # Over-retrieve
        )
    
        # Stage 2: Cross-encoder reranking
        pairs = [(query, c.content) for c in candidates]
        scores = reranker.predict(pairs)
    
        # Combine and sort
        ranked = sorted(
            zip(candidates, scores),
            key=lambda x: x[1],
            reverse=True
        )
    
        return [c for c, _ in ranked[:limit]]
    

---
  #### **Name**
Query Expansion
  #### **Description**
Expand user query to bridge semantic gap
  #### **When**
User queries are short or use different vocabulary than documents
  #### **Example**
    async def expand_query(query: str) -> List[str]:
        """Generate query variations to improve recall."""
        # Use LLM for expansion
        response = await llm.complete(
            f"""Given the search query: "{query}"
            Generate 3 related search queries that might help find relevant documents.
            Return only the queries, one per line."""
        )
    
        expansions = response.strip().split("\n")
    
        # Embed all variations
        all_queries = [query] + expansions
        all_vectors = await embed_batch(all_queries)
    
        # Average the embeddings
        combined_vector = np.mean(all_vectors, axis=0)
    
        return combined_vector
    

---
  #### **Name**
Embedding Cache Pattern
  #### **Description**
Cache embeddings to avoid redundant API calls
  #### **When**
Same content may be embedded multiple times
  #### **Example**
    class EmbeddingCache:
        def __init__(self, cache: Redis, ttl: int = 3600):
            self.cache = cache
            self.ttl = ttl
    
        async def embed(self, text: str) -> List[float]:
            # Hash the text for cache key
            cache_key = f"emb:{hashlib.sha256(text.encode()).hexdigest()}"
    
            # Check cache
            cached = await self.cache.get(cache_key)
            if cached:
                return json.loads(cached)
    
            # Generate embedding
            embedding = await self.embedder.embed(text)
    
            # Cache it
            await self.cache.setex(
                cache_key,
                self.ttl,
                json.dumps(embedding)
            )
    
            return embedding
    

## Anti-Patterns


---
  #### **Name**
Vector Search Alone
  #### **Description**
Using only vector similarity without other signals
  #### **Why**
Embeddings miss keywords, recency, and graph relationships. Recall suffers.
  #### **Instead**
Always combine vector + keyword (BM25) + recency + graph proximity

---
  #### **Name**
No Reranking
  #### **Description**
Returning first-stage retrieval results directly
  #### **Why**
Fast retrieval sacrifices precision. Reranking recovers it.
  #### **Instead**
Always rerank top candidates with cross-encoder

---
  #### **Name**
Mismatched Embedding Models
  #### **Description**
Different models for query and document embedding
  #### **Why**
Vector spaces are model-specific. Different models = incompatible vectors.
  #### **Instead**
Use same model version for query and document embedding

---
  #### **Name**
Ignoring Quantization Cost
  #### **Description**
Enabling scalar/binary quantization without measuring recall
  #### **Why**
Quantization reduces precision. Some use cases can't tolerate the loss.
  #### **Instead**
Measure recall before and after quantization, accept consciously

---
  #### **Name**
Large Chunk Sizes
  #### **Description**
Embedding entire documents as single vectors
  #### **Why**
Long text dilutes meaning. Specific information gets lost in average.
  #### **Instead**
Chunk into 256-512 token segments with overlap