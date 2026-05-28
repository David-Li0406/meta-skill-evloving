---
name: analyze-trends
description: Use this skill to analyze patterns and trends across a batch of articles, identifying hot topics, tracking momentum, and detecting emerging themes.
---

# Analyze Trends

Identify trending topics and patterns across news articles.

## Preconditions

- Articles must have entities extracted by the analyze-article skill.
- A memory system (e.g., Qdrant) should be available for historical comparison.

## Input Parameters

- **articles**: List of processed articles with extracted entities.
- **hot_threshold**: Minimum number of sources for a topic to be considered "hot" (default: 3).
- **lookback_days**: Number of days to look back for historical trend data (default: 7).

## Actions

### Step 1: Extract Topics from Entities

Group articles by shared entities:
- Collect all entities from all articles.
- Filter out entities shorter than 3 characters.
- Map each entity to the list of articles mentioning it.
- Retain only entities appearing in 2 or more articles.

### Step 2: Detect Hot Topics

For each topic (entity):
1. Count unique sources covering it.
2. If the count of sources is greater than or equal to `hot_threshold`, mark it as HOT.
3. Calculate momentum based on source coverage.

### Step 3: Compare to Historical Data

Query memory for historical theme data from the past `lookback_days`:
- Calculate trend status based on comparison:
  - **BREAKING**: New topic with high immediate coverage.
  - **HOT**: Multiple sources covering simultaneously.
  - **RISING**: Increasing coverage compared to history.
  - **ESTABLISHED**: Consistent coverage over time.
  - **FADING**: Decreasing coverage compared to history.

### Step 4: Calculate Momentum

For each topic:
```
momentum = (current_article_count - historical_average) / historical_average
```
- Positive momentum indicates increasing coverage.
- Negative momentum indicates decreasing coverage.
- Zero or undefined momentum indicates a new topic or lack of history.

### Step 5: Detect Entity Clusters

Identify entities that frequently co-occur in articles:
- Build a co-occurrence matrix.
- Identify pairs appearing together 2 or more times.
- Group into clusters based on total mention counts.

### Step 6: Store Theme for Future Tracking

Store each trend in memory for future comparisons.

## Success Criteria

- Topics are correctly grouped by entity.
- Hot topics are identified based on multi-source coverage.
- Trend status accurately reflects momentum.
- Entity clusters reveal related concepts.

## Trend Status Priority (for sorting)

1. BREAKING - Immediate, new, high-impact.
2. HOT - Multiple sources, active coverage.
3. RISING - Growing in coverage.
4. ESTABLISHED - Ongoing coverage.
5. FADING - Decreasing coverage.