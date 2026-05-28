---
name: chunkhound
description: Semantic code chunking and search patterns for codebase exploration
license: MIT
compatibility: opencode
metadata:
    related_mcp_servers: Universal MCP server integration patterns, use skill `mcp-servers`
    related_knowledge_management: For storing research findings, use skill `knowledge-management`
---

# ChunkHound

## What I Do

Provide universal patterns and best practices for using ChunkHound MCP server tools for semantic code search, regex pattern matching, and deep architectural research across codebases.

## Universal ChunkHound Usage Patterns

### Tool Selection Guide

| Tool | When to Use | Best For |
| --- | --- | --- |
| `chunkhound_search_semantic` | Understanding concepts, finding similar functionality | "How does authentication work?" "Find error handling patterns" |
| `chunkhound_search_regex` | Exact code patterns, symbol references | "Find all uses of `validateToken`" "Search for `import.*React`" |
| `chunkhound_code_research` | Architectural exploration, complex relationships | "Map the complete auth flow" "Understand how caching works" |
| `chunkhound_get_stats` | Database health, performance monitoring | Checking chunk counts, file coverage |
| `chunkhound_health_check` | Server status verification | Ensuring MCP server is operational |

### Semantic Search Patterns

```python
# Universal pattern for conceptual code discovery
from chunkhound import search_semantic

# Find authentication-related code by concept
results = search_semantic(
    query="how does user authentication work in this codebase?",
    page_size=10,
    max_response_tokens=20000
)

# Narrow search to specific directory
results = search_semantic(
    query="error handling patterns",
    path="src/components",
    page_size=5
)
```

### Regex Search Patterns

```python
# Universal pattern for exact pattern matching
from chunkhound import search_regex

# Find all function definitions
results = search_regex(
    pattern=r"def \w+\(",
    page_size=20
)

# Find all class definitions in Python files
results = search_regex(
    pattern=r"class \w+:",
    include="*.py"
)
```

### Code Research Patterns

```python
# Universal pattern for architectural exploration
from chunkhound import code_research

# Deep architectural analysis
report = code_research(
    query="how does the payment processing system work?"
)

# Research specific component relationships
report = code_research(
    query="map the data flow from API to database"
)
```

## When to Use Me

Use this skill when:

- Exploring unfamiliar codebases for architectural understanding
- Finding existing patterns before implementing new features
- Debugging by mapping complete system flows
- Refactoring preparation with dependency analysis
- Code archaeology in legacy systems

## Universal Examples

### Architecture Discovery Workflow

```python
# Step 1: Broad semantic search to understand concepts
auth_concepts = search_semantic(query="authentication implementation")

# Step 2: Extract key symbols for comprehensive search
key_symbols = extract_symbols_from_results(auth_concepts)

# Step 3: Find all references with regex
for symbol in key_symbols:
    references = search_regex(pattern=symbol)

# Step 4: Deep research for complete understanding
full_report = code_research(query="complete authentication architecture")
```

### Debugging Pattern Matching

```python
# Find error handling patterns
error_patterns = search_semantic(query="error handling and logging")

# Search for specific error types
validation_errors = search_regex(pattern=r"ValidationError|InvalidInput")

# Research complete error flow
error_flow = code_research(query="how errors propagate through the system")
```

### Refactoring Preparation

```python
# Understand current implementation
current_impl = code_research(query="current caching strategy")

# Find all usage patterns
cache_usage = search_semantic(query="cache usage patterns")

# Identify all cache-related code
cache_symbols = search_regex(pattern=r"(?i)cache")
```

## Best Practices

### Search Strategy

1. **Start Broad**: Use semantic search for conceptual understanding
2. **Narrow Down**: Use regex search for precise symbol locations
3. **Go Deep**: Use code research for architectural relationships

### Performance Optimization

- Use `path` parameter to limit search scope when possible
- Adjust `page_size` based on expected result volume
- Use `max_response_tokens` to control output size

### Result Interpretation

- Semantic search finds conceptually related code
- Regex search finds exact matches and references
- Code research provides structured architectural reports

## Compatibility Notes

This skill works with:

- Any codebase with ChunkHound MCP server configured
- OpenCode agent framework
- Claude-compatible MCP clients
- Projects requiring deep code understanding

## Integration with Other Skills

**With knowledge-management**: Store research findings as memories

```python
store_memory(
    type="code_pattern",
    title="Authentication architecture discovered",
    content=research_report,
    tags=["architecture", "authentication"]
)
```

**With issue-tracking**: Create tasks based on research findings

```python
create_issue(
    title="Refactor authentication based on research",
    description=f"Research shows: {key_findings}"
)
```
