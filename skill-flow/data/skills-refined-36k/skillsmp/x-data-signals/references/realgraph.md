# Reference: RealGraph (User Interaction Affinity)

RealGraph (often served via **GraphJet**) is the model that quantifies the strength of the relationship between two users. It transforms a binary "Follow" into a weighted probability of interaction.

### The Scoring Model
RealGraph calculates a weight for the directed edge $User A \rightarrow User B$. This is not just "Do they follow?" but "Do they care?".

**Interaction Weights (descending impact):**
1.  **Direct Message (DM):** Explicit, private intent.
2.  **Retweet:** Public endorsement.
3.  **Like:** Casual acknowledgment.
4.  **Follow:** The baseline signal (often weak on its own).

### Decay and Freshness
RealGraph applies a **half-life decay** to interactions.
* Recent interactions boost the edge weight significantly.
* If User A hasn't interacted with User B in months, the weight drops, even if they still follow each other.
* *Code Reference:* Look for `InteractionGraph` logic in the `graph-feature-service`.

### Usage in Pipeline
1.  **Candidate Selection (Thunder):** When fetching In-Network tweets, the system queries the RealGraph. It retrieves the top $N$ users by weight and fetches *their* tweets first. This effectively "sorts by friendship" before any ML ranking happens.
2.  **Out-of-Network (RealGraph-OON):** The system traverses the graph 2 hops away ($User \rightarrow Friend \rightarrow Friend's Like$). If your close friends (high RealGraph weight) all interact with a specific stranger, that stranger's content is pulled into your feed.
