---
name: detect-breaking-news
description: Use this skill to identify articles that qualify as breaking news requiring immediate alerts based on article metadata.
---

# Detect Breaking News

Identify articles that require immediate breaking news alerts.

## Preconditions

- Articles have been processed with the analyze-article skill.
- Articles must have the `is_breaking` flag set to true and an `importance_score` assigned.

## Actions

### Step 1: Apply Breaking News Criteria

For each article, check if it meets ALL criteria:

1. **is_breaking**: Must be true (set during analysis).
2. **importance_score**: Must be >= 8 (indicating high or critical importance).

Both conditions must be met to prevent:
- Low-importance articles from being flagged as breaking (score < 8).
- High-importance routine updates from being incorrectly marked as breaking (is_breaking = false).

### Step 2: Collect Breaking Articles

Add all qualifying articles to the breaking news list.

### Step 3: Return Results

Return the list of breaking articles and the count of articles detected.

## Success Criteria

- All articles checked against criteria.
- Breaking articles correctly identified.
- No false positives (low importance flagged as breaking).
- No false negatives (true breaking news missed).

## Example Breaking News Categories

Typical breaking news includes:
- Major model releases (e.g., GPT-5, Claude 4, Gemini 2).
- Security vulnerabilities in AI systems.
- Major company announcements (e.g., acquisitions, leadership changes).
- Regulatory decisions affecting the AI industry.
- Significant research breakthroughs.
- Safety incidents or model failures.