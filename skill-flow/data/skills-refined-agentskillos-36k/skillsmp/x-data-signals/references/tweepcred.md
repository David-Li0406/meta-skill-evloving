# Reference: TweepCred (Reputation)

TweepCred is a legacy but critical signal acting as a global "Reputation Score" for every user ID on X. It is calculated using a **PageRank** variant on the entire interaction graph.

### The Score
* **Range:** 0 to 100.
* **Distribution:** Highly skewed. The vast majority of users have low scores (60 or below). Scores >80 indicate significant public authority.
* **Calculation:** It is calculated iteratively. Your score depends on the TweepCred of the people who interact with you. A Retweet from a high-TweepCred user transfers more "mass" to you than a Retweet from a new account.

### Operational Role (The "Gatekeeper")
TweepCred is primarily an **Efficiency Heuristic** used to save money on compute.
* **Candidate Generation:** When the `Thunder` or `Cr-Mixer` services are under heavy load, they apply a filter: `WHERE tweepcred > threshold`.
* **Implication:** If your TweepCred is low, your tweets may not even *enter* the ranking stage for your followers during peak times.

### Penalties
The score is dampened by:
* **Account Age:** New accounts start with a penalty until they establish a graph.
* **Follow/Ratio:** Following thousands of people while having few followers (churning) flags the account as "Low Quality," reducing the score.
* **Safety Status:** Accounts flagged as "NSFW" or "Spammy" in `VisibilityLib` receive a coefficient penalty to their TweepCred.
