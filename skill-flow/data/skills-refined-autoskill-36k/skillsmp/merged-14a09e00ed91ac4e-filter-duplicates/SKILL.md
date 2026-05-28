---
name: filter-duplicates
description: Use this skill to efficiently remove articles that have already been processed by leveraging Redis for fast URL lookups.
---

# Filter Duplicates

Remove articles that have already been processed using fast Redis lookup.

## Preconditions

- Redis connection available
- Articles have valid URL field

## Actions

### Step 1: Connect to Redis

Establish a connection to Redis for URL lookup.

### Step 2: Check Each Article URL

For each article in the input:
1. Generate URL hash/key.
2. Check if the key exists in the Redis `seen_urls` set.
3. If not seen, add to the output list.

### Step 3: Return Filtered Results

Return the list of articles not previously seen, along with the count of filtered duplicates.

## Output

- `new_articles`: Articles not previously seen.
- `seen_count`: Number of articles filtered as duplicates.

## Success Criteria

- All article URLs checked against Redis.
- No previously processed articles in output.
- New articles preserved for processing.