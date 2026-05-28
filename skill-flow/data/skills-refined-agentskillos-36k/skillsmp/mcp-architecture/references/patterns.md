# MCP Architecture Patterns

Comprehensive organizational patterns for multi-tool MCP servers.

## Pattern Catalog

### 1. Hub-and-Spoke Pattern

**Use when:** Central data source feeds multiple analysis tools

**Structure:**
```
       search (hub)
          |
    ------+------
    |     |     |
  get   find  analyze
 (spoke)(spoke)(spoke)
```

**Example: Code Search**
- Hub: `search_code` returns result IDs
- Spokes: `get_definition`, `find_references`, `analyze_dependencies` consume IDs

**Benefits:**
- Single entry point for discovery
- Efficient token usage (ID references)
- Clear data flow

**Implementation:**
```json
{
  "hub_tool": {
    "name": "search_code",
    "generates": ["result_id"],
    "response_format": {
      "results": [
        {"id": "r1", "preview": "..."},
        {"id": "r2", "preview": "..."}
      ]
    }
  },
  "spoke_tools": [
    {
      "name": "get_definition",
      "consumes": ["result_id"],
      "input": {"result_id": "r1"}
    }
  ]
}
```

### 2. Pipeline Pattern

**Use when:** Sequential operations build on previous results

**Structure:**
```
search → filter → enrich → format
```

**Example: Data Processing**
1. `search_data` - Find candidates
2. `filter_results` - Refine by criteria
3. `enrich_data` - Add contextual information
4. `format_output` - Present in desired format

**Token flow:**
```
search_data
  → Generates: search_token
filter_results(search_token)
  → Generates: filtered_token
enrich_data(filtered_token)
  → Generates: enriched_token
format_output(enriched_token)
  → Final result
```

### 3. CRUD Pattern

**Use when:** Managing persistent resources

**Structure:**
- Create: `create_*`, `start_*`, `init_*`
- Read: `get_*`, `list_*`, `describe_*`
- Update: `update_*`, `modify_*`, `configure_*`
- Delete: `delete_*`, `stop_*`, `remove_*`

**Example: Process Management**

| Operation | Tools | Generates | Consumes |
|-----------|-------|-----------|----------|
| Create | start_process | process_id | - |
| Read | get_status, list_processes | - | process_id |
| Update | configure_process | - | process_id |
| Delete | stop_process | - | process_id |

### 4. Discovery-Detail Pattern

**Use when:** Progressive information access needed

**Layers:**
1. **Discovery** - What's available?
2. **Summary** - High-level overview
3. **Detail** - Full information
4. **Deep Dive** - Comprehensive analysis

**Example: Knowledge Base**

```
Layer 1: list_topics
  → ["authentication", "deployment", "monitoring"]

Layer 2: get_topic_summary("authentication")
  → {articles: 12, last_updated: "2024-01"}

Layer 3: get_article("auth-basics")
  → {content: "...", related: [...]}

Layer 4: get_article_history("auth-basics")
  → {versions: [...], contributors: [...]}
```

### 5. Aggregation Pattern

**Use when:** Combining data from multiple sources

**Structure:**
```
Multiple sources → aggregator → unified view
```

**Example: System Monitoring**

```json
{
  "aggregator": {
    "name": "get_system_status",
    "sources": [
      "cpu_metrics",
      "memory_metrics",
      "disk_metrics",
      "network_metrics"
    ],
    "output": {
      "cpu": {...},
      "memory": {...},
      "disk": {...},
      "network": {...}
    }
  }
}
```

### 6. Batch Operations Pattern

**Use when:** Operating on multiple items efficiently

**Tools:**
- Singular: `get_file(id)` - One item
- Batch: `get_files([id1, id2, id3])` - Multiple items
- Bulk: `get_all_files(filter)` - All matching items

**Example:**

| Tool | Input | Output | Token Cost |
|------|-------|--------|------------|
| get_file | file_id | File details | ~100 |
| get_files | [file_id] (max 10) | Array of files | ~800 |
| get_all_files | {filter} | All matching | ~2000 |

### 7. Versioning Pattern

**Use when:** Supporting multiple API versions or modes

**Approaches:**

**1. Tool Suffix:**
```
search_v1
search_v2
search_v3
```

**2. Parameter:**
```json
{
  "tool": "search",
  "input": {
    "query": "...",
    "api_version": "v2"
  }
}
```

**3. Server Instances:**
```
code-search-v1 (stable)
code-search-v2 (beta)
code-search-v3 (experimental)
```

**Recommendation:** Use parameter approach for minor changes, separate servers for major breaking changes.

### 8. Lazy Loading Pattern

**Use when:** Expensive operations should be deferred

**Structure:**
```
get_overview (cheap, ~50 tokens)
  ↓
get_details (moderate, ~200 tokens)
  ↓
get_full_analysis (expensive, ~1000 tokens)
```

**Example: Code Analysis**

```json
{
  "lazy_loading": {
    "overview": {
      "tool": "get_symbol_overview",
      "cost": 50,
      "includes": ["name", "type", "location"]
    },
    "details": {
      "tool": "get_symbol_details",
      "cost": 200,
      "includes": ["signature", "docs", "usages_count"]
    },
    "full": {
      "tool": "get_symbol_full",
      "cost": 1000,
      "includes": ["all_usages", "callers", "callees", "history"]
    }
  }
}
```

## Pattern Selection Guide

| Scenario | Recommended Pattern | Reason |
|----------|---------------------|--------|
| Code search/analysis | Hub-and-Spoke | Central search, many detail operations |
| Data processing | Pipeline | Sequential transformations |
| Resource management | CRUD | Standard lifecycle operations |
| Documentation/KB | Discovery-Detail | Progressive information access |
| System monitoring | Aggregation | Multiple data sources |
| File operations | Batch Operations | Efficiency for bulk operations |
| API evolution | Versioning | Backward compatibility |
| Performance optimization | Lazy Loading | Defer expensive operations |

## Anti-Patterns to Avoid

### 1. Flat Structure (Too Many Top-Level Tools)

❌ **Bad:**
```
search_users
search_posts
search_comments
search_likes
search_shares
... (20+ search tools)
```

✅ **Good:**
```
search (with type parameter)
  - type: "users"
  - type: "posts"
  - etc.
```

### 2. Inconsistent Naming

❌ **Bad:**
```
getUser
fetch_post
retrieveComment
findLikes
```

✅ **Good:**
```
get_user
get_post
get_comment
get_likes
```

### 3. Missing Token Systems

❌ **Bad:**
```
search_code
  → Returns: Full code blocks (1000+ tokens each)
get_more_context
  → Requires: Repeating search query
```

✅ **Good:**
```
search_code
  → Returns: [{id: "r1", preview: "..."}]
get_definition(id: "r1")
  → Returns: Full details
```

### 4. No Progressive Discovery

❌ **Bad:**
```
get_everything
  → Returns 5000 tokens
  → User overwhelmed
```

✅ **Good:**
```
info
  → Returns: Tool categories
list_category("query")
  → Returns: Tools in category
get_help("search_code")
  → Returns: Detailed help
```

## Real-World Examples

### Lightning Code Index (lci)

**Pattern:** Hub-and-Spoke + Discovery-Detail

```
Hub: search
  ↓
Spokes:
  - get_definition (detail)
  - find_references (detail)
  - get_context (enrichment)

Discovery:
  - info (overview)
  - code_insight (analysis modes)
```

**Token strategy:** IDs for progressive detail

### Browser Proxy (agnt)

**Pattern:** CRUD + Aggregation

```
CRUD:
  - start_proxy (create)
  - get_status (read)
  - stop_proxy (delete)

Aggregation:
  - currentpage (combines errors, metrics, interactions)
```

**Token strategy:** proxy_id, session_id for cross-tool references

### Process Manager

**Pattern:** CRUD + Lazy Loading

```
CRUD:
  - start_process
  - list_processes
  - stop_process

Lazy Loading:
  - get_status (quick)
  - get_output (moderate)
  - get_full_logs (expensive)
```

## Pattern Combinations

Most real-world MCPs use multiple patterns:

**Code Search Example:**
- Hub-and-Spoke (search → details)
- Discovery-Detail (info → categories → tools)
- Lazy Loading (overview → details → full analysis)
- Batch Operations (get_definitions for multiple IDs)

**Workflow:**
```
1. info → Shows categories
2. search_code → Returns result IDs
3. get_definitions([id1, id2, id3]) → Batch fetch
4. trace_callers(id1) → Deep dive on one result
```

This combines patterns for optimal token efficiency and user experience.
