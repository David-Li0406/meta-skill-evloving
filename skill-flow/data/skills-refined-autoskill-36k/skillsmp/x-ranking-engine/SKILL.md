---
name: x-ranking-engine
description: Use this skill when you need to reason about the machine learning models that determine the final order of the "For You" timeline. It is essential for tasks involving model feature engineering, tuning engagement weights, or understanding the internal mechanics of the Heavy Ranker (Navi).
version: 1.0.0
license: MIT
---

# X Ranking Engine

Deep technical knowledge of the X Heavy Ranker, including MaskNet/Phoenix architectures, Multi-Task Learning (MTL) heads, probability calibration, and the mathematical WeightedScorer logic.

## Context

The **Heavy Ranker** is the final scoring stage of the pipeline. It reduces a pool of ~1,500 candidates to a sorted list based on predicted user engagement. The system has evolved from Gradient Boosted Decision Trees (GBDT) to deep neural networks like **MaskNet** and more recently, transformer-based architectures (Phoenix) that leverage learned embeddings rather than hand-engineered features.

For detailed technical specifications, see:
- [Model Architecture](./references/model-architecture.md)
- [Scoring Parameters & Weights](./references/scoring-parameters.md)

## What it does

* **Details Multi-Task Learning (MTL):** Explains how the model simultaneously predicts multiple engagement types (Like, Reply, Retweet, Video View, etc.) using a shared backbone.
* **Decodes Feature Hydration:** Maps how `HomeMixer` gathers User (SimClusters, TwHIN) and Tweet (Content, Engagement counts) features to pass to the `Navi` service.
* **Analyzes Calibration:** Explains the process of transforming raw model outputs into "calibrated" probabilities that reflect real-world interaction rates.
* **Explains Point-wise Ranking:** Details why the algorithm scores candidates in isolation (Candidate Isolation) to allow for massive horizontal scaling.

## Guidelines

* **Architecture Isolation:** When modifying the ranker, remember that the model cannot "see" other tweets in the same batch. Diversity and deduplication must happen in the `Selector` or `Mixer` stages, not the `Scorer`.
* **Weighting vs. Probability:** The model predicts *probabilities* (e.g., "What is the 0-1 chance this user likes this tweet?"). The `WeightedScorer` then applies *weights* to these probabilities to get the final score.
* **Negative Signals are Nuclear:** Signals like "Report" or "Show Less Often" have weights (e.g., -369.0) that are orders of magnitude larger than positive signals, ensuring toxic content is effectively removed from the candidate pool.
* **Recency Decay:** The engine applies a time-decay function ($e^{-\lambda t}$) to the final score to ensure the timeline remains fresh and doesn't get stuck on high-scoring old content.
* **Navi Interop:** The Heavy Ranker is hosted in the **Navi** (Rust) service. Features must be serialized into Thrift objects in Scala and sent via RPC.

## Example Trigger Prompts

* "/audit-ml show weights: Like vs Retweet"
* "/audit-ml explain MaskNet handling for this feature"
* "Relationship between P(Like) and final ranking score"
* "Impact of adding 'Long-form Read' head to MTL model"
* "How are probabilities calibrated for new low-data tweets?"
* "Where are Heavy Ranker features defined in Thrift?"
