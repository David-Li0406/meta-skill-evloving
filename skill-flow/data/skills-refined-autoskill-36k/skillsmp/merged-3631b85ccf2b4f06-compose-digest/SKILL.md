---
name: compose-digest
description: Use this skill to compose a formatted news digest from processed articles and trends, generating a cohesive narrative summary with embedded citations for Discord readability.
---

# Compose Digest

Create a formatted news digest from articles and trends.

## Preconditions

- Articles processed with analyze-article skill
- Trends analyzed with analyze-trends skill
- LLM API available for summary generation

## Input Parameters

- **articles**: List of processed articles to include in the digest.
- **trends**: List of identified trends for the period.
- **period_hours**: Number of hours covered by this digest (default: 12).

## Actions

### Step 1: Select Articles by Importance

Sort articles by importance score and select:
1. **All high importance** (score >= 7)
2. **Top 5 medium importance** (score 5-6)
3. **Fallback**: If no notable articles, take top 5 by score.

### Step 2: Generate LLM Summary

Send selected articles to LLM with the following prompt:

```
Write a cohesive, professional summary of these news items:
1. Be written as flowing paragraphs, not bullet points.
2. Embed source citations inline using markdown [Source](url).
3. Highlight the most important developments first.
4. Group related news naturally in the narrative.
5. Be concise but comprehensive.

Write 2-4 paragraphs summarizing the key AI news.
```

### Step 3: Parse and Clean Response

- Strip Qwen3 thinking tags (`<think>...</think>`).
- Clean up any formatting artifacts.
- If LLM fails, use fallback bullet-point format.

### Step 4: Build NewsDigest Object

Create a digest with:
- Unique ID: `digest-{uuid[:8]}`
- Created timestamp
- Period start/end based on `period_hours`
- Generated headline summary
- Top 5 trends
- Article count
- Sources used

### Step 5: Format for Discord

Format the digest with sections:

```markdown
# AI News Digest - {date} ({Morning/Evening})

{LLM-generated summary with citations}

**Trending Topics:**
- {topic} (covered by {n} sources)

**Emerging Themes:**
- {rising topic}

---
*{n} articles from {n} sources*
```

## Success Criteria

- Coherent summary generated.
- Citations properly embedded.
- Trends highlighted appropriately.
- Format fits Discord constraints.

## Fallback Behavior

If LLM is unavailable, use the following format:

```markdown
**Today's AI News Highlights:**

- [{title}]({url}) ({source}): {summary}...
```