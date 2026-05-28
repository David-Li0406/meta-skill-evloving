---
name: x-data-signals
description: Use this skill to decode the "DNA" of the recommendation engine. These signals are the foundational data structures used to retrieve candidates (before ranking) and as features for the Heavy Ranker (during ranking).
version: 1.0.0
license: MIT
---

# X Data Signals

Deep dive into the X recommendation engine's core signal libraries: SimClusters (Community Embeddings), RealGraph (Interaction Probabilities), TweepCred (Reputation), and TwHIN (Knowledge Graph).

## Context

The engine relies on four primary signal pillars:
1.  **SimClusters (v2):** A Matrix Factorization framework that anchors users and tweets into ~145k community vectors. It is the primary driver for "Embedding-Based Candidate Generation" (EBCG).
2.  **RealGraph:** A weighted, directed graph of user interactions, predicting the probability `P(u -> v)` of engagement. It powers the "In-Network" feed.
3.  **TweepCred:** A continuous PageRank score (0-100) determining user authority.
4.  **TwHIN:** (Twitter Heterogeneous Information Network) Dense knowledge-graph embeddings that capture multi-modal relationships (Users, Tweets, Ads, Topics) in a shared vector space.

For detailed logic, see:
- [SimClusters (Communities)](./references/simclusters.md)
- [RealGraph (Interaction Graph)](./references/realgraph.md)
- [TweepCred (Reputation)](./references/tweepcred.md)

## What it does

* **Identifies "Lookalike" Audiences:** Uses SimClusters to find content popular in communities you *implicitly* belong to, even if you don't follow the authors.
* **Quantifies Relationship Strength:** Uses RealGraph to assign a floating-point weight to every user-user connection, prioritizing close friends over acquaintances.
* **Filters Low-Quality Nodes:** Uses TweepCred to prune candidate pools during the retrieval stage, saving compute by ignoring low-authority accounts.
* **Calculates Embedding Similarity:** Computes dot-product scores between User embeddings and Tweet embeddings to predict relevance in the "Earlybird" (Light Ranker) stage.

## Guidelines

* **SimClusters v2 Implementation:** The source code distinguishes between **"Known-For"** (what a Creator talks about) and **"Interested-In"** (what a Consumer likes). A tweet is recommended if the Creator's "Known-For" vector aligns with the Consumer's "Interested-In" vector.
* **GraphJet vs. RealGraph:**
    * **RealGraph:** The offline/batch-calculated interaction model (the "map").
    * **GraphJet:** The real-time, in-memory graph processing engine that *serves* the RealGraph data to the HomeMixer.
* **TwHIN vs. SimClusters:**
    * **SimClusters** is *sparse* and interpretable (e.g., "Cluster 123 = JavaScript").
    * **TwHIN** is *dense* and uninterpretable (64-dim float vectors). TwHIN is often used for "TwHIN-Collab" filtering in the candidate generation phase.
* **Signal Decay:** RealGraph weights decay over time. A "Like" from 2018 is worth significantly less than a "Like" from today. The `UserInteractionSignal` service handles this time-decay logic.
* **Code Locations:**
    * `src/scala/com/twitter/simclusters_v2`: Core logic for community embeddings.
    * `src/scala/com/twitter/graph/batch/job/twhin`: Knowledge graph embedding generation.
    * `src/java/com/twitter/search/earlybird`: Where real-time signals meet search indices.

## Example Trigger Prompts

* "/explain-graph TweepCred @user"
* "/explain-graph SimClusters @user"
* "/explain-graph RealGraph interactions"
* "How does SimClusters v2 compute 'InterestedIn' scores?"
* "Compare RealGraph weights vs Follow links"
* "How TweepCred affects HeavyRanker min_reputation"
* "Explain TwHIN embeddings with SimClusters"
* "Fave-based vs Follow-based clustering logic"
