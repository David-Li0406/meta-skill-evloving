# Reference: Thunder Event Processing

`Thunder` is the high-throughput Rust service responsible for the "In-Network" (Follow-based) candidate sourcing.

### Real-Time Ingestion
Thunder maintains an in-memory database of tweets from every user's following graph.
1. **Kafka Streams:** Thunder consumes events for `PostCreation` and `PostDeletion`.
2. **Sub-millisecond Lookups:** When a user requests a feed, Thunder performs a fan-out lookup to find recent posts from everyone that user follows.
3. **Retention Management:** To maintain performance, Thunder automatically prunes posts that exceed age or count thresholds, focusing on the most recent ~1,000 posts per author.
