# Airweave Search Patterns

Common search patterns and recipes for effective data retrieval.

## Search Parameter Combinations

### High-Precision Search

For finding exact, high-quality matches:

```python
results = client.collections.search(
    readable_id=collection_id,
    query="authentication implementation guide",
    enable_reranking=True,
    enable_query_expansion=False,  # Use exact query
    top_k=20,  # Smaller candidate pool
    limit=10
)
```

### High-Recall Search

For finding all potentially relevant documents:

```python
results = client.collections.search(
    readable_id=collection_id,
    query="user onboarding",
    enable_query_expansion=True,
    search_type="hybrid",
    top_k=200,  # Large candidate pool
    limit=100
)
```

### Time-Sensitive Search

For recent updates and current information:

```python
results = client.collections.search(
    readable_id=collection_id,
    query="release notes",
    recency_bias=0.9,  # Strongly prefer recent
    limit=20
)
```

### Balanced Search

Good default for most use cases:

```python
results = client.collections.search(
    readable_id=collection_id,
    query="API documentation",
    search_type="hybrid",
    enable_reranking=True,
    recency_bias=0.3,
    limit=25
)
```

## Source-Specific Patterns

### Search Code Repositories

```python
from airweave import SearchRequest, Filter, FieldCondition, MatchAny

search_request = SearchRequest(
    query="error handling implementation",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["GitHub", "GitLab", "Bitbucket"])
            )
        ]
    ),
    enable_reranking=True
)

results = client.collections.search_advanced(
    readable_id=collection_id,
    search_request=search_request
)
```

### Search Communication Tools

```python
search_request = SearchRequest(
    query="meeting notes product launch",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["Slack", "Teams", "Gmail"])
            )
        ]
    ),
    recency_bias=0.7  # Recent conversations more relevant
)
```

### Search Documentation

```python
search_request = SearchRequest(
    query="deployment guide kubernetes",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["Notion", "Confluence", "Google Docs"])
            )
        ]
    ),
    enable_query_expansion=True
)
```

### Search Project Management

```python
search_request = SearchRequest(
    query="critical bugs P0",
    filter=Filter(
        must=[
            FieldCondition(
                key="source_name",
                match=MatchAny(any=["Jira", "Linear", "Asana"])
            )
        ]
    ),
    recency_bias=0.8
)
```

## Answer Generation Patterns

### Direct Q&A

Get a synthesized answer instead of raw results:

```python
answer = client.collections.search(
    readable_id=collection_id,
    query="What is our PTO policy?",
    response_type="completion",
    enable_reranking=True
)
```

### Summarization

```python
answer = client.collections.search(
    readable_id=collection_id,
    query="Summarize the key decisions from last week's product meetings",
    response_type="completion",
    recency_bias=0.9,
    limit=50  # More context for better summary
)
```

## Pagination Pattern

For browsing large result sets:

```python
def paginated_search(client, collection_id, query, page_size=20):
    """Generator for paginated search results."""
    offset = 0
    while True:
        results = client.collections.search(
            readable_id=collection_id,
            query=query,
            limit=page_size,
            offset=offset
        )
        
        if not results.results:
            break
            
        yield from results.results
        
        if len(results.results) < page_size:
            break
            
        offset += page_size

# Usage
for result in paginated_search(client, collection_id, "customer feedback"):
    print(result['payload']['md_content'][:100])
```

## Combining Multiple Searches

### Search then Refine

```python
# Broad initial search
broad_results = client.collections.search(
    readable_id=collection_id,
    query="authentication",
    top_k=200,
    limit=100
)

# If too many results, refine with more specific query
if len(broad_results.results) > 20:
    refined_results = client.collections.search(
        readable_id=collection_id,
        query="OAuth2 authentication implementation",
        enable_reranking=True,
        limit=20
    )
```

### Multi-Query Fusion

Search with multiple queries and combine results:

```python
queries = [
    "password reset flow",
    "forgot password implementation",
    "user credential recovery"
]

all_results = []
seen_ids = set()

for query in queries:
    results = client.collections.search(
        readable_id=collection_id,
        query=query,
        limit=10
    )
    
    for result in results.results:
        if result['id'] not in seen_ids:
            all_results.append(result)
            seen_ids.add(result['id'])

# Sort by score
all_results.sort(key=lambda x: x['score'], reverse=True)
```

## MCP Tool Usage Patterns

When using Airweave via MCP, the AI assistant translates natural language to parameters:

| User Request | MCP Parameters |
|--------------|----------------|
| "Find recent bug reports" | `query: "bug reports", recency_bias: 0.8` |
| "Get the top 5 results" | `limit: 5` |
| "Search only in Slack" | Uses filter on source_name |
| "Summarize the results" | `response_type: "completion"` |
| "Find exact matches only" | `search_method: "keyword"` |
| "Use AI reranking" | `enable_reranking: true` |

## Performance Tips

1. **Use appropriate limits**: Start with smaller limits (10-25) for interactive use
2. **Enable reranking judiciously**: Adds latency but improves relevance
3. **Use filters when possible**: Narrowing by source is faster than semantic filtering
4. **Adjust top_k**: Controls candidate pool size before reranking
5. **Use keyword search for exact matches**: `search_method: "keyword"` is faster for known terms

