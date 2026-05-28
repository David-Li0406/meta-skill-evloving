# Reference: Toxicity & Reputation Decay

The system uses a mathematical model to manage reputation and content quality over time.

### The pToxicity Model
Unlike the `pAbuse` model (which handles TOS violations), the `pToxicity` model identifies content that is "low quality" or "insulting."
* **Marginal Content:** Content that is toxic but not illegal is often given a "Downrank" clue rather than being dropped.
* **Reply Throttling:** If a reply has a high `pToxicity` score, it is moved to the bottom of the thread or hidden behind a "Show more replies" click.

### Linear Decay (Healing)
Reputation is not static. If an account stops generating negative signals, its score "heals."
* **Damage Multipliers:** A single verified "attack" (like a coordinated bot-report) can lead to a 25.11% decrease in reputation score.
* **Time-Decay:** The system uses a distributed time-decay mechanism to focus on recent behavior rather than historical mistakes.

### Feedback-based Fatigue
If a user consistently ignores or marks content from a specific author as "Not Interested," `VisibilityLib` applies a fatigue filter that lowers the score for that specific user-author pair for a period of up to 3 months.
