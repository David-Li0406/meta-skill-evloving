# Reference: Model Architecture (MaskNet & MTL)

The X Heavy Ranker utilizes a Deep Learning architecture optimized for "Click-Through Rate" (CTR) style predictions across multiple engagement dimensions.

### 1. MaskNet Backbone
The core architecture is often **MaskNet**, which is designed to capture complex, non-linear feature interactions without the manual effort of feature crossing.
* **Instance-wise Masking:** A dedicated masking layer "masks" out features that are irrelevant for a specific User-Tweet pair before they enter the deep layers.
* **High-Order Interactions:** Unlike linear models, MaskNet can learn that "User interest in [Topic A]" is only relevant when "Tweet contains [Media Type B]".

### 2. Multi-Task Learning (MTL)
The model uses a shared set of "Bottom" layers (embeddings and dense layers) and branches out into specific "Heads" for each action:
* **Engagement Heads:** $P(Like)$, $P(Reply)$, $P(Retweet)$, $P(Quote)$, $P(VideoView)$.
* **Continuous Heads:** Estimates **Dwell Time** (log-space seconds) and **Profile Clicks**.
* **Negative Heads:** $P(Report)$, $P(ShowLessOften)$, $P(NegativeFeedback)$.

### 3. Feature Inputs
The model consumes thousands of features, categorized into:
* **User Features:** `SimClusters` (Interest vectors), `TwHIN` (Graph embeddings), and recent interaction history.
* **Tweet Features:** `ContentEmbeddings`, media metadata, and global engagement counts (Likes/RTs over the last 24h).
* **Relationship Features:** `RealGraph` weights (Is this the user's close friend?).

### 4. Candidate Isolation (Point-wise)
The system is strictly **Point-wise**.
* **Logic:** Every candidate in the ~1,500 pool is scored independently of the others.
* **Attention:** In modern transformer-based versions (Phoenix), a post only attends to the **User Context** (the Query), never to other tweets in the batch. This prevents $O(N^2)$ complexity but requires downstream "Diversity Filters" to handle variety.
