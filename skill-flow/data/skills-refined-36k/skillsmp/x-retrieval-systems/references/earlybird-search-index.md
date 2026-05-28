# Reference: Earlybird Search Index

Earlybird is X's real-time search engine, built on a custom implementation of Apache Lucene.

### Cluster Architecture
1. **Realtime Cluster:** Indexes all public tweets from the last 7 days. Optimized for high-frequency updates.
2. **Protected Cluster:** Indexes tweets from private accounts that the user is authorized to see.
3. **Archive Cluster:** A massive distributed index of all historical tweets.

### Retrieval Mechanism
- **Inverted Index:** Maps terms (hashtags, words, UserIDs) to posting lists.
- **Single-Writer / Multi-Reader:** A concurrency model that ensures the index is searchable within seconds of a tweet being posted.
- **Light Ranking:** Earlybird performs a "light" rank using basic features (recency, term frequency) to return the top candidates to HomeMixer.
