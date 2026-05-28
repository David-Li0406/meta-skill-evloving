# Reference: The Rust Candidate Pipeline

The core recommendation logic is implemented in the `candidate-pipeline` crate, providing a high-performance framework for the "For You" feed.

### Pipeline Stages
1.  **Query Hydration:** Captures the user's recent interactions (likes, clicks) to build a "User Profile" for the session.
2.  **Candidate Sourcing (Parallel):**
    * **Thunder:** Fetches recent posts from followed accounts.
    * **Phoenix Retrieval:** Uses a "User Tower" and "Candidate Tower" for embedding-based discovery of out-of-network content.
3.  **Candidate Hydration:** Supplementing IDs with post text, media, author verification, and video duration.
4.  **Pre-Scoring Filters:** Removing duplicates, blocked content, and previously seen posts.
5.  **Scoring (Sequential):** * **Phoenix Scorer:** ML predictions for 10+ engagement types.
    * **Weighted Scorer:** Aggregates probabilities into a final score.
    * **Author Diversity:** Down-ranks consecutive posts from the same author.
6.  **Selection:** Sorting and picking the top K candidates.

### Key Performance Rule: Candidate Isolation
During the scoring phase, the system uses **special attention masking**. A post's score is calculated only against the user context, never against other posts in the same batch.
