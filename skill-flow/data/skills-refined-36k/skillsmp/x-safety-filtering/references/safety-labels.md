# Reference: Safety Labels & Shadowbans

The X codebase uses `SafetyLabels` to tag content and users for remediation. "Shadowbanning" is a collection of these states that restrict reach.

### Critical Labels
| Label | Description | Impact |
| :--- | :--- | :--- |
| **`DoNotAmplify`** | The "Discovery Kill-Switch." | Content is visible on profile but removed from Home/Search. |
| **`SearchBlacklist`** | Account-level restriction. | User's account and tweets are hidden from all search results. |
| **`TrendsBlacklist`** | Trend restriction. | User is disqualified from appearing in the Trending tab. |
| **`NsfwUser`** | Adult content label. | Content is hidden unless the viewer opts-in to sensitive media. |
| **`UntrustedUrl`** | Spam/Malware label. | Tweets containing these links are de-amplified or blocked. |

### Trigger Conditions
* **Bot Detection:** Rapid-fire posting, following, or automated "Reply Guy" behavior.
* **Graph Blocking:** Being "graph-blocked" by a large, cohesive cluster of high-reputation users.
* **Negative Feedback Spike:** A sudden influx of "Reports" (carrying a -369x penalty) or "Blocks" (-74x penalty).
