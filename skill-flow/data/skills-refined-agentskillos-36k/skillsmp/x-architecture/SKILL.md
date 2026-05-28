---
name: x-architecture
description: Use this skill when reasoning about the distributed system design, service orchestration, or request lifecycle of the X recommendation engine. It is essential for tasks involving the "For You" timeline construction, HomeMixer logic, or ProductMixer component definitions.
version: 1.0.0
license: MIT
---

# X Algorithm Architecture

Master reference for the X (Twitter) recommendation engine architecture, specifically the HomeMixer orchestration layer, ProductMixer functional components, and the Scala-to-Rust candidate pipeline bridge.

## Context

The X recommendation engine operates as a "Lambda Architecture" variant. The orchestration layer (**HomeMixer**) is written in Scala using the **ProductMixer** framework, which defines the business logic graph. High-compute tasks (Candidate Retrieval, Scoring) are offloaded to optimized services (Rust/C++/Java).

For detailed technical breakdowns, see:
- [Pipeline Lifecycle](./references/pipeline-lifecycle.md)
- [Service Map](./references/service-map.md)

## What it does

* **Maps the Request Graph:** Traces the execution path from `HomeMixer` down to leaf services like `Earlybird` (Search) and `Navi` (ML Scoring).
* **Defines ProductMixer Traits:** Explains the specific Scala traits used to build feed features: `CandidateSource`, `Filter`, `Scorer`, `Gate`, `Selector`, and `SideEffect`.
* **Identifies Data Models:** Recognizes key data structures like `SimClusters` (Community Embeddings), `TwHIN` (Knowledge Graph), and `RealGraph` (User Interaction probabilities).
* **Locates Logic:** Helps determine if logic resides in the orchestration layer (Scala) or the compute layer (Rust/Thrift).

## Guidelines

* **Directory Navigation:**
    * `home-mixer/`: Main orchestration logic for the timeline.
    * `product-mixer/`: Core framework defining how pipelines are built.
    * `cr-mixer/`: Content Recommender Mixer (Out-of-Network retrieval logic).
    * `navi/`: ML Model serving infrastructure (Heavy Ranker host).
    * `visibility-lib/`: Rust-based filtering logic (Safety, Blocks, Mutes).
* **ProductMixer Hierarchy:** The system is composed of pipelines.
    1.  **Mixer Pipeline:** The top-level entry (e.g., "For You").
    2.  **Candidate Pipeline:** Parallel fetching of candidates (e.g., "In-Network", "Ads", "Who to Follow").
    3.  **Functional Components:** Atomic units of logic (`Filter`, `Scorer`, `Hydrator`).
* **Scoring Stages:** distinguish between **Light Ranking** (fast, heuristic-based, often inside `Earlybird`) and **Heavy Ranking** (full neural network, hosted in `Navi`).
* **Candidate Isolation:** In the Heavy Ranker (MaskNet/Transformer), candidates are scored in a batch but *cannot* attend to each other (no cross-candidate attention). They only attend to the User Context.
* **Thrift Boundaries:** Scala components communicate with Rust services via Thrift. If a field isn't in the Thrift definition, `HomeMixer` cannot see it.
* **Feature Stores:** Understand that `SignalIngester` and `UserSignalService` provide the raw interaction data that feeds `SimClusters` and `RealGraph`.

## Example Trigger Prompts

* "/trace-feed ForYou"
* "/trace-feed HomeMixer → HeavyRanker"
* "/trace-feed CandidateSource vs Gate in ProductMixer"
* "Where are SimClusters embeddings injected in the pipeline?"
* "Explain cr-mixer’s Out-of-Network candidate generation"
* "How does visibility-lib enforce feed filtering?"
