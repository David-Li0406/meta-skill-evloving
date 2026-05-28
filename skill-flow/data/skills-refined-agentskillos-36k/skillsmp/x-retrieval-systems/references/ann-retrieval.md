# Reference: ANN & Embedding Retrieval

Approximate Nearest Neighbor (ANN) search is the core of X's Discovery (Out-of-Network) engine.

### The HNSW Algorithm
X uses **Hierarchical Navigable Small World (HNSW)** graphs to perform fast vector searches. 
- **Graph Structure:** Points (tweets) are organized in a hierarchy. The search starts at a coarse layer and zooms in on the most similar vectors.
- **Latency:** Allows searching millions of vectors in <10ms, which is impossible with standard "Brute Force" dot products.

### Phoenix Integration
Phoenix generates "Candidate Towers" for tweets. When a user requests a feed, their "User Tower" vector is used as a query in the HNSW index to find the 100-200 most relevant discovery tweets globally.
