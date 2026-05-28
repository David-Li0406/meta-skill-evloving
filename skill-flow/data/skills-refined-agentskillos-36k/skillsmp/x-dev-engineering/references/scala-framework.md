# Reference: ProductMixer (Scala Orchestration)

**ProductMixer** is the Scala-based framework used for high-level orchestration of different product surfaces (e.g., Home, Search, Explore).

### Core Abstractions
* **Product Pipelines:** The entry point for specific requests. It selects which Mixer or Recommendation pipeline to run.
* **Mixer Pipelines:** Combine heterogeneous content types—mixing Tweets from the Rust pipeline with Ads and "Who to Follow" modules.
* **Recommendation Pipelines:** Specialized for scoring and ranking homogeneous content (like the "For You" tweet list).

### The Scala-Rust Split
* **Scala (ProductMixer):** Handles "What to show" (e.g., "Mix 80% Tweets and 20% Ads").
* **Rust (HomeMixer/Candidate Pipeline):** Handles "Which specific items are best" (the heavy lifting of ML ranking and filtering).
