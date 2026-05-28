# Reference: Pipeline Lifecycle

The X Recommendation Pipeline processes requests in a strict "Funnel" architecture, reducing millions of candidates to ~100 tweets in sub-second time.

### 1. Candidate Generation (Retrieval)
Fetching top-k candidates from distributed indices (~1500-3000 candidates).
* **In-Network (RealGraph/UTEG):** Retrieval from the internal `UserTweetEntityGraph`. Finds tweets from people the user follows, ranked by interaction probability.
* **Out-of-Network (Social Graph):** Finds tweets liked by people the user follows ("Social Proof").
* **Embedding-Based (SimClusters/TwHIN):** "Lookalike" retrieval. Finds tweets that cluster in the same semantic space as the user's interests.
* **Search Index (Earlybird):** Real-time inverted index retrieval for trending topics.

### 2. Light Ranking
A high-throughput, low-latency pass to reduce the candidate pool before expensive hydration.
* **Logistic Regression:** Earlybird processing uses simple models to prune "obviously bad" candidates.
* **Metadata Filtering:** Hard filters for language, region, and basic safety checks.

### 3. Feature Hydration
Before the heavy model can run, candidates must be enriched with dense features.
* **User Features:** `SimClusters` (Interests), `TwHIN` (Graph embeddings), `TweepCred` (Reputation).
* **Graph Features:** Real-time counts of likes, retweets, and replies (from `Manhattan` KV store).

### 4. Heavy Ranking
The core ML stage hosted on **Navi**.
* **Model Architecture:** MaskNet (or Transformer-based variants).
* **Scoring:** Computes `P(engagement)` for multiple heads (Like, Reply, Retweet, Video View).
* **Weighting:** Raw probabilities are combined using weights (e.g., `Score = P(Like)*0.5 + P(Reply)*27.0`).
    * *Note: Reply weights are typically much higher than Like weights to promote conversation.*

### 5. Heuristics & Filtering
Business logic applied *after* the ML score is determined.
* **VisibilityLib:** The "Final Gate". Removes blocks, mutes, NSFW (if settings apply), and withheld content.
* **Author Diversity:** Penalizes multiple tweets from the same author to prevent timeline domination.
* **Content Balance:** Enforces ratios between In-Network and Out-of-Network content (e.g., 50/50 split).
* **Blue Boost:** Multipliers applied to candidates from Twitter Blue/Premium users.

### 6. Mixing & Decoration (Content Hydration)
* **Mixing:** Merging separate candidate pipelines (e.g., Ads + Organic Tweets).
* **Decoration:** `Tweetypie` fetches the actual display strings, media URLs, and user objects for the final JSON response.
