# Reference: Scoring Parameters & Weights

The final ranking score ($S$) is a weighted sum of the calibrated probabilities predicted by the Heavy Ranker.

### The Scoring Formula
The `WeightedScorer` (typically in `HomeMixer`) calculates the final score as:
$$S = \sum (P_{action} \times W_{action}) \times \text{Multipliers}$$

### Core Weights (Reference Table)
These weights represent the "Value" X places on specific user actions.

| Action ($P$) | Weight ($W$) | Strategic Intent |
| :--- | :--- | :--- |
| **Author Reply** | **75.0** | Incentivizes creators to engage with their audience. |
| **Reply** | **13.5** | High value; promotes "Conversation" as the platform's core product. |
| **Retweet** | **1.0** | Base unit of amplification/virality. |
| **Like** | **0.5** | Low-effort signal; provides volume but less "depth" than a reply. |
| **Video View** | **0.005** | Very low weight, but high frequency allows video-heavy feeds to stay competitive. |
| **Report** | **-369.0** | Extremely punitive; ensures safety/compliance. |
| **Show Less Often**| **-10.0** | Strong negative preference for that specific topic/author. |

### Calibration
Raw model outputs are not used directly. They are **Calibrated** to ensure they represent true probabilities.
* **Logic:** If the model predicts $P(Like) = 0.1$, then exactly 10% of users in that cohort should actually Like the tweet.
* **Mechanism:** An isotonic regression or scaling layer is applied to the raw logit before the weight is applied.

### Post-Scoring Multipliers
After the weighted sum is calculated, final adjustments are made:
1.  **Recency Bias:** A decay factor based on the age of the tweet.
2.  **Author Diversity:** If a user has already seen many tweets from Author A, Author A's subsequent tweets are deboosted.
3.  **Blue Boost:** Verified users (Premium) receive a multiplier (often 1.2x - 1.5x) to their visibility at the sourcing and ranking layers.
