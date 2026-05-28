# Reference: Reputation & Trust (TweepCred)

`TweepCred` is a PageRank-style reputation score (0-100) assigned to every account. It acts as a global multiplier or "Gatekeeper" in the `Thunder` retrieval service.

### Authority Tiers
* **High Authority (>65):** Content is eligible for immediate "Out-of-Network" (OON) injection via SimClusters.
* **Standard (30-65):** Content is distributed normally to followers; OON discovery depends on high engagement velocity.
* **Low Authority (<30):** "Shadow-throttled." Content may only appear in the "Following" feed and is often excluded from the "For You" timeline during peak load.

### Trust Factors
1.  **Verification Status:** Premium accounts receive an internal "Blue Boost" coefficient in the ranker.
2.  **Safety Labels:** Any `VisibilityLib` flags (e.g., "Abusive") apply a dampening factor to the TweepCred.
3.  **Interaction Quality:** Receiving likes from high-TweepCred users "transfers" authority to your account.
