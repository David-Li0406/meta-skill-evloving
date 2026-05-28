---
name: x-post-optimizer
description: Use this skill when advising on post structure, timing, media selection, and account health to align with the HeavyRanker's scoring weights and anti-spam heuristics.
version: 1.0.0
license: MIT
---

# X Post Optimizer

Strategic expertise for maximizing content reach on X. It focuses on the "Engagement Velocity" required to pass from candidate sourcing to the top of the "For You" timeline.

## Context

The X algorithm utilizes a `WeightedScorer` that aggregates multiple probability heads (e.g., $P(\text{Like})$, $P(\text{Reply})$). While the `HeavyRanker` (Phoenix/MaskNet) predicts the likelihood of an action, the **Weights** determine the final distribution. Understanding these weights is key to "Algorithm-Native" content creation.

For specific tactical data, refer to:
- [Engagement Weights](./references/engagement-weights.md)
- [Reputation & Trust (TweepCred)](./references/reputation-trust.md)
- [Distribution Logic & Penalties](./references/distribution-logic.md)

## What it does

* **Calculates Expected Value:** Estimates the "Score Boost" of different media types (e.g., Video vs. Static Text).
* **Optimizes Conversation Depth:** Advises on "Author-In-Thread" interactions, which carry massive weight in the `WeightedScorer`.
* **Protects Account Reputation:** Identifies "Anti-Signals" (external links, rapid-fire posting) that trigger the `VisibilityLib` de-amplification.
* **Timing Strategy:** Leverages knowledge of the "Frequency Deboost" window (3600s) to prevent internal cannibalization of posts.

## Guidelines

* **The 13.5x Rule:** Replies are significantly more valuable than Likes in the modern ranker. Content that invites a meaningful "back-and-forth" creates a feedback loop that the `HeavyRanker` optimizes for.
* **Author Reply Multiplier:** In the code, author engagement on their own thread acts as a "Freshness" and "Conversation" signal, often effectively multiplying the thread's reach by keeping it at the top of the retrieval stack.
* **Negative Signal Avoidance:** Avoid "Engagement Bait" that leads to "Show Less Often" or "Report" actions. The weight for a "Report" (-369.0) is mathematically impossible to overcome with positive engagement.
* **Media Strategy:** Native video receives a dedicated weight (`vqv_weight_eligibility`), making it the preferred format for "Out-of-Network" discovery.

## Example Trigger Prompts

* "/post-check optimize draft: [Insert Post Text]"
* "/post-check why is reach low for this post?"
* "Should I put the link in the main post or first reply?"
* "Why is my second post 50% weaker than the first?"
* "Explain reach differences: video vs text-only"
* "Maximize 'Conversation' weight for 5-tweet thread"
* "Impact of 'Show Less Often' clicks on my account"
