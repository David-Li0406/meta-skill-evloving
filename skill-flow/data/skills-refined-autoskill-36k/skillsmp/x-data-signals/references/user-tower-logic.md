# Reference: User Tower Logic

The "User Tower" is a neural network component that compresses a user's complex, multi-modal history into a single vector representation for real-time retrieval.

### Model Input
- **Engagement History:** Recent likes, replies, and "Not Interested" signals.
- **Profile Metadata:** Account age, verification status, and language preferences.
- **Embedding Context:** The user's current TwHIN and SimCluster memberships.

### Functionality
The User Tower acts as one half of a **Two-Tower Model** (common in Phoenix). 
1. **Encoding:** It transforms the user's state into a normalized embedding.
2. **Similarity:** This embedding is compared against millions of "Candidate Tower" (tweet) embeddings in milliseconds.
3. **Dynamic Updates:** The tower is periodically retrained to reflect shifts in user interest, ensuring the "For You" feed stays fresh.
