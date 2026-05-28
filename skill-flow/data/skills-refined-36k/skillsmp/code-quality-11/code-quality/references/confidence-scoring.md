# Confidence Scoring

Score factors (0-100):
- occurrence frequency
- consistency_ratio (0-1)
- recency_weight (0-1)
- author_distribution (unique authors normalized)

Example scoring heuristic:
score = 100 * (
  0.35 * min(occurrences / 10, 1) +
  0.35 * consistency_ratio +
  0.15 * recency_weight +
  0.15 * min(author_distribution / 3, 1)
)

Confidence tiers:
- High: occurrences >= 5 and consistency > 0.90 -> auto-apply
- Medium: occurrences >= 5 and 0.70-0.90 -> MCQ confirmation
- Low: occurrences < 5 or consistency < 0.70 -> manual review
- Conflicting: multiple patterns with >=5 occurrences each -> conflict flow
