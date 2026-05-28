# Reference: Distribution Logic & Penalties

Beyond ML scores, the algorithm applies several hard-coded heuristics to ensure timeline health and diversity.

### 1. Frequency Deboost (The 1-Hour Rule)
The system tracks the time delta between posts from the same author.
* **Rule:** If `Post_B` is published within **3600 seconds** (1 hour) of `Post_A`, it receives a **0.5x penalty** to its final score.
* **Strategy:** Space major updates by at least 61 minutes to ensure both receive full ranking potential.

### 2. The Link Penalty
The algorithm is "Content Blind" to many types, but it is highly sensitive to external URLs.
* **Mechanism:** Posts containing links are often excluded from the "Out-of-Network" candidate sources (Phoenix/SimClusters).
* **Workaround:** Place the link in the **second tweet** of a thread once the "Hook" has established engagement velocity.

### 3. Native Video Boost
* **Eligibility:** Posts marked `vqv_eligibility = true` (native video) are processed by a specialized `VideoScorer`.
* **Benefit:** Video-native users have a different "Dwell Time" threshold, making them more likely to stay in the candidate pool longer than text-only users.

### 4. Diversity Filtering
The `Selector` stage in `HomeMixer` enforces author diversity. Even with a high score, a user will rarely see more than 2 posts from the same author in a single "session" (one scroll).
