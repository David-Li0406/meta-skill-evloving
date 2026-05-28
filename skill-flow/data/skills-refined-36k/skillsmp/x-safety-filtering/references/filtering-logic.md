# Reference: Filtering Logic & Architecture

`VisibilityLib` is a centralized Rust-based library that determines if a viewer is allowed to see a specific piece of content based on a map of features (SafetyLabels, User Graph, and Settings).

### The Filtering Pipeline
When a request is made, the `RuleEngine` executes a chain of logic according to a specific `SafetyLevel`:

1.  **Legal & Compliance:**
    * **Geo-blocking:** Removes content prohibited in the user's country.
    * **Suspensions:** Filters out deactivated or suspended authors.

2.  **User Graph State:**
    * **Hard Blocks:** If User A blocks User B (or vice versa), content is hidden.
    * **Mutes:** If User A has muted User B, content is dropped from the timeline.

3.  **Content Safety Models:**
    * **pNSFWMedia/Text:** Detects adult or sexual topics.
    * **pToxicity:** Detects insults and harassment that do not necessarily violate TOS but impact quality.
    * **pAbuse:** Detects hate speech and targeted harassment.

4.  **Downstream Actions:**
    * **Drop:** Hard filtering where the content is completely removed.
    * **Interstitials:** Soft filtering where the content is hidden behind a warning.
    * **Ranking Clues:** Provides metadata to the Heavy Ranker to apply negative weights.
