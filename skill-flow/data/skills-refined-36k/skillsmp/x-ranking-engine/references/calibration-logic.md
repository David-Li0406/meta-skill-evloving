# Reference: Calibration Logic

Raw scores from the Multi-Task Learning (MTL) heads (like $P(Like)$ or $P(Reply)$) must be calibrated before they can be used in a weighted formula.

### Why Calibrate?
Machine learning models often produce "overconfident" probabilities. Calibration ensures that a predicted probability of 0.1 corresponds to a 10% actual occurrence rate in the real world.

### The Scoring Service Flow
1. **Raw Inference:** Navi serves the MaskNet model to get probabilities.
2. **Platt/Isotonic Scaling:** A calibration layer adjusts these probabilities based on historical engagement data.
3. **Weighting:** The calibrated $P(Action)$ is then multiplied by its strategic weight (e.g., 75x for Author Reply) to produce the final ranking score.
