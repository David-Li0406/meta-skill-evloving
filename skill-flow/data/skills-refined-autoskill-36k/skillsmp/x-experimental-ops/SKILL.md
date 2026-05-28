---
name: x-experimental-ops
description: Use this skill when reasoning about how the algorithm is tuned, why different users see different behaviors, or how "Success" is defined by X's engineering team.
version: 1.0.0
license: MIT
---

# X Experimental Ops

Knowledge of X's A/B testing infrastructure (DuckDuckGoose) and the metrics used to measure algorithmic success.

## Context
The algorithm is never "finished." It is a living system managed by **DuckDuckGoose (DDG)**, X's internal experimentation platform. Every change to a weight or a filter is first tested on a small percentage of the user base.

- [DuckDuckGoose (A/B Testing)](./references/ab-testing-framework.md)
- [Metrics & Alignment](./references/metrics-alignment.md)

## What it does
* **Explains Bucketing:**
  * Details the mechanics of **DuckDuckGoose**, X's internal experimentation platform that uses salt-based consistent hashing to deterministically assign users to "Control" or "Treatment" variants.
  * Ensures "sticky" assignments so a user's experience remains consistent across sessions while maintaining statistically sound percentage-based rollouts (e.g., 1%, 5%, or 10% cohorts).
* **Decodes Success Metrics:**
  * Breaks down the **"Unregretted User Minutes" (UUM)** North Star metric, which prioritizes high-value time spent (replies, likes, and deep reads) over passive scrolling or "clickbait" interactions that lead to user regret.
  * Analyzes how experimental changes impact the Multi-Task Learning (MTL) "heads" to ensure a boost in one engagement signal (like Retweets) doesn't negatively correlate with platform health or retention.
* **Analyzes Feature Flags:**
  * Identifies how the system uses **Dynamic Configuration** and **Feature Gates** to toggle ranking logic or retrieval sources on and off for specific cohorts in real-time.
  * Explains the "Kill Switch" architecture that allows engineers to instantly roll back a new algorithmic feature if it causes a spike in latency or negative feedback without requiring a full code redeployment.

## Example Trigger Prompts

* "/run-experiment salt-based hashing for user buckets"
* "/run-experiment Unregretted User Minutes vs dwell time"
* "Trace feature flag logic for latest Grok retrieval test"
* "Show holdout group parameters for current Heavy Ranker A/B"
* "Compare control vs variant metrics for feed engagement test"
* "Explain how a new signal is staged in an experiment pipeline"
