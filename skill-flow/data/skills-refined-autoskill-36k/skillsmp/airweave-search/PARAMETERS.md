# Search Parameters Deep Dive

Detailed guidance on when and how to use each Airweave search parameter.

## Core Parameters

### `query` (required)
The search query text. Use natural language—Airweave uses semantic search.

**Good queries:**
- "customer feedback about shipping delays"
- "authentication implementation OAuth"
- "Q4 sales report"

**Avoid:**
- Single words without context ("pricing")
- Boolean operators ("pricing AND feedback") - use natural language instead
- Exact phrases in quotes (semantic search handles this)

### `response_type`
Controls what you get back.

| Value | Returns | Best For |
|-------|---------|----------|
| `raw` (default) | List of matching documents with scores | When you need to see sources, cite them, or process multiple results |
| `completion` | AI-synthesized answer | Direct Q&A, summaries, when user wants "the answer" not "the documents" |

**Use `completion` when:**
- User asks a direct question ("What is our refund policy?")
- User wants a summary ("Summarize the meeting notes")
- Single authoritative answer is expected

**Use `raw` when:**
- User wants to see sources ("Show me messages about...")
- You need to cite where information came from
- Multiple perspectives or documents are relevant
- User is exploring/browsing

### `limit`
Maximum number of results to return (1-1000, default: 100).

| Limit | Use Case |
|-------|----------|
| 3-5 | Quick precise answer, top matches only |
| 10-20 | Standard search, balance of coverage and relevance |
| 50-100 | Exploration, comprehensive research |
| 100+ | Analysis across large dataset |

**Tip:** Start with lower limits for faster responses. Increase if results seem incomplete.

### `offset`
Skip this many results (for pagination). Default: 0.

Use when browsing through large result sets:
- First page: `limit: 20, offset: 0`
- Second page: `limit: 20, offset: 20`
- Third page: `limit: 20, offset: 40`

## Ranking Parameters

### `recency_bias`
How much to favor recent documents (0-1).

| Value | Effect |
|-------|--------|
| 0 | Pure relevance, ignore dates |
| 0.3 | Slight preference for recent |
| 0.5 | Balance relevance and recency |
| 0.7 | Strong preference for recent |
| 0.9 | Heavily favor recent |
| 1.0 | Sort by date only |

**Use high recency (0.7+) for:**
- "Recent", "latest", "this week", "today"
- Conversations, messages, updates
- Fast-moving topics (bugs, incidents)
- News, announcements

**Use low/no recency (0-0.3) for:**
- Documentation, policies, guides
- Historical research
- "Best" or "most relevant" (not "most recent")

### `score_threshold` (Deprecated)

> **Note:** This parameter is deprecated and may be ignored by the backend. Use `enable_reranking: true` instead for quality filtering.

Minimum similarity score to include (0-1). If supported:

| Value | Effect |
|-------|--------|
| 0.5 | Moderate quality filter |
| 0.7 | High quality only |
| 0.85 | Very high confidence only |

**Better alternative:** Use `enable_reranking: true` to improve result quality.

### `enable_reranking`
Use AI to rerank results for better relevance (default: true).

| Value | Effect |
|-------|--------|
| `true` | Better relevance, slightly slower |
| `false` | Faster, pure vector similarity |

**Keep enabled (true) for:**
- Most searches
- When relevance quality matters
- Complex queries

**Disable (false) for:**
- Speed-critical applications
- Simple keyword lookups
- Very large result sets

## Search Method Parameters

### `search_method`
How to match documents.

| Method | How It Works | Best For |
|--------|--------------|----------|
| `hybrid` (default) | Combines semantic + keyword | Most searches, best overall |
| `neural` | Pure semantic/meaning | Conceptual questions, synonyms |
| `keyword` | Text matching | Exact terms, names, codes, IDs |

**Use `hybrid` for:**
- General searches (default choice)
- When unsure which method is best

**Use `neural` for:**
- "Find documents about..." (conceptual)
- When exact words don't matter
- Synonym-heavy domains

**Use `keyword` for:**
- Searching for names ("John Smith")
- Error codes, IDs ("ERR-4032")
- Exact technical terms
- When semantic matching gives wrong results

### `expansion_strategy`
How to expand the query for better recall.

| Strategy | Effect |
|----------|--------|
| `auto` (default) | Smart expansion based on query |
| `llm` | AI-powered expansion (best quality) |
| `no_expansion` | Use exact query only |

**Use `no_expansion` when:**
- Query is already perfect
- You want exact matching
- Speed is critical
- LLM expansion gives wrong variations

### `enable_query_interpretation`
Extract filters from natural language (default: false).

When enabled, queries like "Slack messages from last week" automatically filter to Slack source and recent timeframe.

**Enable when:**
- Users mention specific sources ("in Slack", "from GitHub")
- Users mention time ranges ("last week", "today")
- Natural language queries that imply filters

**Keep disabled (default) when:**
- You're constructing precise queries
- You want full control over filtering
- Automatic interpretation causes unexpected results

## Common Parameter Combinations

### Quick Answer
```
query: "What is our PTO policy?"
response_type: "completion"
limit: 5
enable_reranking: true
```

### Recent Conversations
```
query: "product launch discussion"
recency_bias: 0.8
limit: 15
search_method: "hybrid"
```

### Precise Document Search
```
query: "API authentication guide"
search_method: "keyword"
enable_reranking: true
limit: 10
```

### Comprehensive Research
```
query: "customer feedback pricing"
limit: 50
enable_reranking: true
expansion_strategy: "llm"
```

### Speed-Optimized
```
query: "deployment checklist"
search_method: "keyword"
enable_reranking: false
expansion_strategy: "no_expansion"
limit: 10
```

