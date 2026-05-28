---
name: analyze-trends
description: Use this skill when you need to identify and analyze trending topics across a batch of articles, tracking their momentum and detecting emerging themes.
---

# Skill body

## Preconditions

- Articles must have entities extracted by the analyze-article skill.
- A memory system (e.g., Qdrant) should be available for historical comparison.

## Actions

### Step 1: Extract Topics from Entities

1. Group articles by shared entities:
   - Collect all entities from all articles.
   - Filter out entities shorter than 3 characters.
   - Map each entity to the list of articles mentioning it.
   - Keep only entities appearing in 2 or more articles.

### Step 2: Detect Hot Topics

1. For each topic (entity):
   - Count unique sources covering it.
   - If the count of sources is greater than or equal to the `hot_threshold` (default is 3), mark the topic as HOT.
   - Calculate momentum based on source coverage.

### Step 3: Compare to Historical Data

1. Query the memory for historical theme data from the past `lookback_days`:
   - Calculate trend status based on comparison:
     - **BREAKING**: New topic with high immediate coverage.
     - **HOT**: Multiple sources covering simultaneously.
     - **RISING**: Increasing coverage compared to history.
     - **ESTABLISHED**: Consistent coverage over time.
     - **FADING**: Decreasing coverage compared to history.

### Step 4: Calculate Momentum

1. For each topic, calculate momentum using the formula:
   ```
   momentum = (current_article_count - historical_average) / historical_average
   ```
   - Positive momentum indicates increasing coverage.
   - Negative momentum indicates decreasing coverage.
   - Zero or undefined momentum indicates a new topic or no historical data.

### Step 5: Detect Entity Clusters

1. Identify entities that frequently co-occur in articles:
   - Build a co-occurrence matrix.
   - Identify pairs of entities appearing together in 2 or more articles.
   - Group these entities into clusters based on their co-occurrence.