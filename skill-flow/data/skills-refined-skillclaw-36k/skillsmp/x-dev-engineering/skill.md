---
name: x-dev-engineering
description: Use this skill when implementing new features or debugging the core "For You" pipeline. The system has shifted from legacy heuristics toward a unified **Rust-based** pipeline powered by the **Phoenix** transformer (Grok).
version: 1.0.0
license: MIT
---

# X Development Engineering

Technical expertise for developing and extending the X recommendation engine, focusing on the Grok-powered Phoenix model, Rust candidate pipelines, and the removal of hand-engineered features.

## Context

The modern X algorithm prioritizes a "No Hand-Engineered Features" philosophy. Relevance is learned directly from user engagement sequences using a transformer architecture.

For technical deep-dives, see:
- [The Rust Candidate Pipeline](./references/rust-pipeline.md)
- [Phoenix (Grok) Model Scoring](./references/phoenix-scoring.md)
- [Visibility & Safety Engineering](./references/visibility-safety.md)

## What it does

* **Implements Grok-Native Components:** Guidance on integrating with the Phoenix transformer for multi-action prediction (Like, Repost, Reply, etc.).
* **Architects Candidate Sources:** Logic for the two primary retrieval engines: **Thunder** (In-Network) and **Phoenix Retrieval** (Out-of-Network).
* **Enforces Pipeline Order:** Ensures components follow the strict sequence: Query Hydration -> Sourcing -> Hydration -> Pre-Scoring Filters -> Scoring -> Selection.
* **Optimizes for Parallelism:** Leverages Rust's async/await to execute independent hydration and sourcing tasks concurrently.

## Guidelines

* **Candidate Isolation:** During scoring, ensure candidates cannot "attend" to each other in the transformer. This maintains score consistency and enables batching.
* **No Heuristics:** Avoid adding manual "if/then" rules for relevance; the Phoenix model should handle weightings through learned engagement probabilities.
* **Hydration Efficiency:** Fetch only necessary metadata (text, media, author status) during the Candidate Hydration stage after initial sourcing to minimize I/O.
* **Safety First:** All content must pass through `VisibilityLib` (Rust) for legal compliance and safety filtering before reaching the user.

## Example Trigger Prompts

* "/gen-thrift new ranking signal"
* "/gen-thrift scaffold Rust Filter trait"
* "Add a new engagement signal to Phoenix prediction"
* "Show Rust implementation for Thunder candidate source"
* "Explain 'No Hand-Engineered Features' in ranking update"
* "How is candidate isolation applied in transformer attention?"
