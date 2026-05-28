# Reference: Engagement Weights

The final ranking of a post is determined by the `WeightedScorer`. It takes the probabilities predicted by the ML model ($P$) and multiplies them by static weights ($W$).

### The Weighted Scoring Formula
$$TotalScore = \sum (P_{action} \times W_{action})$$

### Core Weights (approx. based on source)
| Action | Weight | Strategic Note |
| :--- | :--- | :--- |
| **Reply** | **13.5** | The strongest positive signal for distribution. |
| **Retweet** | **1.0** | A standard endorsement signal. |
| **Like** | **0.5** | Lower weight than replies, but acts as a "Top-of-Funnel" signal. |
| **Video View** | **0.005** | Low weight per view, but high volume leads to significant aggregate boosts. |
| **Author Reply** | **75x (Eff.)** | Not a direct weight, but triggers a "Conversation" multiplier in the pipeline. |

### Negative Weights (The "Reach Killers")
| Action | Weight | Impact |
| :--- | :--- | :--- |
| **Report** | **-369.0** | Instant death for the post; triggers safety review. |
| **Show Less Often** | **-10.0** | Massive de-boost; prevents the user from seeing your content for weeks. |
| **Block** | **-50.0** | Signals extreme irrelevance or toxicity. |
