---
name: filter-duplicates
description: Use this skill to efficiently remove articles that have already been processed, leveraging Redis for quick URL lookups to avoid unnecessary LLM calls.
---

# Skill body

## Preconditions

- Redis connection available
- Articles have valid URL field

## Actions

### Step 1: Connect to Redis

Establish a connection to Redis for URL lookup.

### Step 2: Check Each Article URL

For each article in the input list:
1. Generate a URL hash/key.
2. Check if the key exists in the Redis `seen_urls` set.
3. If the URL is not seen, add the article to the output list.

### Step 3: Return Filtered Results

Return the list of articles that have not been previously seen, along with the count of filtered duplicates.

## Input

- **articles**: list[RawArticle] - Articles to filter.

## Output

- **new_articles**: list[RawArticle] - Articles not previously seen.
- **seen_count**: int - Number of articles filtered as duplicates.

## Success Criteria

- All article URLs checked against Redis.
- No previously processed articles in the output.
- New articles preserved for processing.