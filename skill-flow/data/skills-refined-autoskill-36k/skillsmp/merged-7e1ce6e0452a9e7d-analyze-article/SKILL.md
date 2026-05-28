---
name: analyze-article
description: Use this skill to analyze and enrich a raw news article with AI-generated metadata, including summary, entities, category, importance score, and breaking news detection.
---

# Analyze Article

Use LLM to analyze and enrich a single news article.

## Preconditions

- Article must have a valid title and summary/content.
- LLM API (vLLM) must be accessible.

## Actions

### Step 1: Prepare Content

Combine the article title and summary for analysis. Truncate if longer than 2000 characters.

### Step 2: Call LLM for Analysis

Send the article to the LLM with a structured prompt requesting:

1. **Summary**: 2-3 sentence summary of key points.
2. **Category**: One of `research`, `business`, `product`, `security`, `policy`, `general`.
3. **Entities**: List of companies, people, technologies, models mentioned.
4. **Importance Score**: 1-10 rating where:
   - 1-3: Minor news, incremental updates.
   - 4-6: Notable news, meaningful developments.
   - 7-8: Important news, significant impact.
   - 9-10: Major news, industry-changing announcements.
5. **Is Breaking**: True if major breaking news requiring immediate alert.
6. **Breaking Reason**: Explanation if breaking (e.g., "Major model release").

### Step 3: Parse LLM Response

Extract structured data from the JSON response. Handle:
- Qwen3 thinking tags (`<think>...</think>`) - strip them.
- Markdown code blocks around JSON.
- Invalid JSON - return defaults.

### Step 4: Apply Importance Boost

Boost the importance score by +2 (max 10) for official company blog posts, as these represent primary source announcements.

### Step 5: Generate Content Hash

Create a hash from the title and URL for deduplication tracking.

## Success Criteria

- Article enriched with AI summary.
- Valid category assigned.
- Entities extracted (may be empty).
- Importance score between 1-10.
- Breaking news flag set appropriately.

## Fallback Behavior

If the LLM call fails:
- Use the original summary as the AI summary.
- Set category to `general`.
- Set importance to 5.
- Set is_breaking to false.
- Return entities as an empty list.