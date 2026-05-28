# Pagination Reference

Notion API paginates responses for large result sets. Default page size is 100 (also max).

## Using Helper Functions

The SDK provides pagination helpers that handle cursors automatically:

### Collect All Results

```python
from notion_client.helpers import collect_paginated_api

# Get ALL pages from database (loads into memory)
all_pages = collect_paginated_api(
    client.databases.query,
    database_id="abc123..."
)

print(f"Found {len(all_pages)} pages")
```

### Iterate Without Loading All

```python
from notion_client.helpers import iterate_paginated_api

# Memory-efficient iteration
for page in iterate_paginated_api(
    client.databases.query,
    database_id="abc123..."
):
    title = page["properties"]["Name"]["title"][0]["plain_text"]
    print(f"Processing: {title}")
```

### Async Variants

```python
from notion_client.helpers import (
    async_collect_paginated_api,
    async_iterate_paginated_api,
)

# Async collect
all_pages = await async_collect_paginated_api(
    async_client.databases.query,
    database_id="abc123..."
)

# Async iterate
async for page in async_iterate_paginated_api(
    async_client.databases.query,
    database_id="abc123..."
):
    process(page)
```

## Manual Pagination

For fine-grained control:

```python
results = []
has_more = True
start_cursor = None

while has_more:
    response = client.databases.query(
        database_id="abc123...",
        start_cursor=start_cursor,
        page_size=100,  # Max 100
    )

    results.extend(response["results"])
    has_more = response["has_more"]
    start_cursor = response.get("next_cursor")

print(f"Total: {len(results)} pages")
```

## Pagination Response Structure

```python
{
    "object": "list",
    "results": [...],        # Array of pages/blocks
    "next_cursor": "abc...", # Use for next request (None if last page)
    "has_more": True,        # False on last page
    "type": "page_or_database",
    "page_or_database": {}
}
```

## Rate Limit Considerations

- Pagination helpers don't throttle automatically
- Each page fetch counts against rate limit (3 req/sec)
- For large datasets (1000+ items), add delays:

```python
import time
from notion_client.helpers import iterate_paginated_api

count = 0
for page in iterate_paginated_api(client.databases.query, database_id="..."):
    count += 1
    process(page)

    # Throttle every 100 items
    if count % 100 == 0:
        time.sleep(1)
```

## Block Children Pagination

Blocks also paginate:

```python
from notion_client.helpers import collect_paginated_api

# Get all blocks in a page
blocks = collect_paginated_api(
    client.blocks.children.list,
    block_id="page-id..."
)

# Process nested blocks
for block in blocks:
    if block.get("has_children"):
        children = collect_paginated_api(
            client.blocks.children.list,
            block_id=block["id"]
        )
```

## Search Pagination

```python
from notion_client.helpers import collect_paginated_api

# Search across workspace
results = collect_paginated_api(
    client.search,
    query="project"
)

# Filter to pages only
pages = [r for r in results if r["object"] == "page"]
```

## Best Practices

| Scenario          | Approach                                  |
| ----------------- | ----------------------------------------- |
| < 100 items       | Single query, no pagination               |
| 100-1000 items    | `collect_paginated_api()`                 |
| 1000+ items       | `iterate_paginated_api()` with throttling |
| Real-time display | Manual pagination with progress           |
| Async context     | Use `async_*` variants                    |

## Error Handling

```python
from notion_client import APIResponseError, APIErrorCode

try:
    for page in iterate_paginated_api(client.databases.query, database_id="..."):
        process(page)
except APIResponseError as e:
    if e.code == APIErrorCode.RateLimited:
        # Wait and restart from last cursor
        time.sleep(int(e.additional_data.get("retry_after", 1)))
    else:
        raise
```

## Read-After-Write Consistency

Newly created content may not be immediately available for query due to eventual consistency.

### Minimum Delay Required

```python
import time

# After creating or appending content
append_blocks(client, page_id, blocks)

# Wait before reading back
time.sleep(0.5)  # 0.5s minimum recommended

# Now query is consistent
children = client.blocks.children.list(page_id)
```

### When This Applies

| Operation                                       | Delay Needed          |
| ----------------------------------------------- | --------------------- |
| `append_blocks()` then `blocks.children.list()` | Yes (0.5s)            |
| `pages.create()` then `search()`                | Yes (may need longer) |
| `pages.update()` then `pages.retrieve()`        | Usually not           |
| Query same database twice                       | No                    |

_Verified in: `test_integration.py::TestBlockAppend::test_retrieve_appended_blocks`_
