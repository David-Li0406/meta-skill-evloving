---
name: analyze-article
description: Use this skill when you need to analyze and enrich a raw news article with AI-generated insights, including summaries, entity extraction, and importance scoring.
---

# Skill body

## Preconditions

- Article must have a valid title and summary/content.
- LLM API (vLLM) must be accessible.

## Actions

### Step 1: Prepare Content

Combine the article title and summary for analysis. Truncate if longer than 2000 characters.

### Step 2: Call LLM for Analysis

Send the article to the LLM with a structured prompt requesting:

1. **Summary**: A 2-3 sentence summary of key points.
2. **Category**: One of `research`, `business`, `product`, `security`, `policy`, `general`.
3. **Entities**: A list of companies, people, technologies, and models mentioned.
4. **Importance Score**: A rating from 1-10 where:
   - 1-3: Minor news, incremental updates.
   - 4-6: Notable news, meaningful developments.
   - 7-8: Important news, significant impact.
   - 9-10: Major news, industry-changing announcements.
5. **Is Breaking**: True if it is major breaking news requiring immediate alert.
6. **Breaking Reason**: Explanation if breaking (e.g., "Major model release").

### Step 3: Parse LLM Response

Extract structured data from the JSON response. Handle:
- Qwen3 thinking tags (`<think>...</think>`) by stripping them.
- Markdown code blocks around JSON.
- Invalid JSON by returning defaults.

### Step 4: Apply Importance Boost

Boost the importance score by +2 (max 10) for official company blog posts, as these represent primary source announcements.

### Step 5: Generate Content Hash

Create a hash from the title and URL for deduplication tracking.

## Success Criteria

- The article is enriched with an AI-generated summary.
- A valid category is assigned.
- Entities are extracted (may be empty).
- The importance score is between 1-10.
- The breaking news flag is set appropriately.

## Fallback Behavior

If the LLM call fails:
- Use the original summary as the AI summary.
- Set the category to `general`.
- Set the importance to 5.
- Set `is_breaking` to false.
- Return entities as an empty list.