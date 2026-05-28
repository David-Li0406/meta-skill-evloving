---
name: x-safety-filtering
description: Use this skill when analyzing why content is not appearing, checking for "shadowban" conditions, or understanding the safety compliance layer. This skill covers the `VisibilityLib` logic that runs *after* candidate sourcing but *before* final ranking to ensure platform health.
version: 1.0.0
license: MIT
---

# X Safety & Filtering

Expert knowledge of X's VisibilityLib, covering safety labels, shadowban logic, NSFW filtering, and content health suppression mechanisms.

## Context

The filtering stage is the "Gatekeeper" of the timeline. Even if a tweet has a high ML score from the Heavy Ranker, `VisibilityLib` can drop it entirely or apply a "Do Not Amplify" label that restricts it to the author's profile. This layer enforces legal compliance, user blocks, mutes, and platform safety rules (e.g., NSFW or Toxicity).

## What it does

* **Decodes "Shadowbans":** Explains the specific internal labels (like `SearchBlacklist`) that cause users to perceive they are shadowbanned.
* **Enforces User Preferences:** Handles the logic for Mutes, Blocks, and "Show less often" signals.
* **Manages Content Health:** Identifies toxic content or misinformation using models like `pToxicity` and `pAbuse` and applies downstream penalties.
* **NSFW Handling:** Segments content into "Adult" or "Graphic" categories using `pNSFWMedia` and ensures it respects the viewer's sensitivity settings.

## Guidelines

* **SafetyLevel Context:** Rules are evaluated based on the `SafetyLevel` (e.g., Timeline vs. Profile). A tweet might be visible on a Profile but blocked in the Home Timeline.
* **The "Do Not Amplify" (DNA) Label:** Disqualifies tweets from the "For You" (Out-of-Network) timeline and Search results without removing them from the profile.
* **Visibility vs. Ranking:** 1.  **Pre-Scoring:** Hard filters (Drop) remove blocked or legally prohibited content.
    2.  **Post-Scoring:** Soft filters (Labels) apply safety checks (e.g., author diversity) after the Heavy Ranker has assigned scores.
* **Toxicity Thresholds:** If a user enters a "Reply Guy" mode with consistently high `pToxicity` scores, their account enters a state that limits the reach of all their future replies.
* **Linear Decay:** Negative reputation signals follow a linear decay model; an account can "heal" its reputation over time by stopping negative behavior.

## Example Trigger Prompts

* "/safety-check shadowban or SearchBlacklist status"
* "/safety-check toxicity decay for @user"
* "/safety-check flagged content vs safe content ratio"
* "/safety-check audit applied filters on a thread"
* "what are the visibility rules affecting recent posts"
* "show suppressed accounts in a community"
