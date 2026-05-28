# Reference: TwHIN (Twitter Heterogeneous Information Network)

TwHIN is the dense counterpart to SimClusters. While SimClusters uses sparse community mapping, TwHIN uses high-dimensional vector embeddings to represent entities.

### Heterogeneous Embedding Logic
TwHIN maps multiple entity types into a shared embedding space:
- **Users:** Embedded based on their following graph and interaction history.
- **Tweets:** Embedded based on content, engagement, and the users who interact with them.
- **Advertisers/Ads:** Embedded to facilitate high-relevance ad placement.

### Key Advantages
1. **Task Reusability:** A single set of TwHIN embeddings can be used across Ranking, Retrieval, and Safety filtering.
2. **Dense Relationships:** Unlike SimClusters (which may fail for users with few community ties), TwHIN provides a continuous vector for every active entity.
3. **Signal Fusion:** It fuses social signals (follows) with content signals (media engagement) into a 145k-dimensional space.

### Implementation in Pipeline
TwHIN embeddings are retrieved during the **Hydration** phase. The dot product between a user's TwHIN vector and a candidate tweet's TwHIN vector serves as a primary feature for the Heavy Ranker.
