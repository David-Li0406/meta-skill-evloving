# Reference: SimClusters (Community Embeddings)

SimClusters (specifically **SimClusters v2**) is a general-purpose representation layer based on Matrix Factorization. It groups Users and Tweets into sparsely populated communities.

### The Algorithm: Metropolis-Hastings
The source code uses a Metropolis-Hastings sampling algorithm to generate these communities on a massive scale (tens of millions of users, ~145k clusters).

### Key Vectors
SimClusters generates two primary vectors for every entity:
* **Known-For (Producer):** What is this user an expert in? (e.g., Elon Musk is "Known-For" Space, EV, Tech).
* **Interested-In (Consumer):** What does this user want to see? (Derived from who they follow and what they like).

### The "Fave" Signal
While early versions relied on Follows, modern SimClusters relies heavily on **Favorites (Likes)**.
* **Logic:** If you Like a tweet anchored to the "Rust Lang" cluster, your "Interested-In" vector for "Rust Lang" increases.
* **Log-Odds Scoring:** The association score is often calculated using Log-Odds to normalize against global popularity (preventing "Viral" tweets from polluting niche clusters).

### Usage in Ranking
In the **Heavy Ranker**, the model computes the **Dot Product** between:
$$Score = \vec{User}_{InterestedIn} \cdot \vec{Tweet}_{Representation}$$
A high dot product indicates the tweet falls exactly into the niche the user cares about, often overriding a lower generic popularity score.
