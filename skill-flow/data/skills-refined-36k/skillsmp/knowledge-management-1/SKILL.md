---
name: knowledge-management
description: Universal knowledge storage and retrieval patterns using memory graph
license: MIT
compatibility: opencode
metadata:
    related_issue_tracking: For tracking knowledge-related tasks, use skill `issue-tracking`
    related_mcp_servers: For MCP server integration, use skill `mcp-servers`
---

# Knowledge Management

## What I Do

Provide universal patterns for storing, retrieving, and managing project knowledge across different contexts and projects.

## Universal Knowledge Management Patterns

### Memory Storage Triggers

Store memories on these universal events:

- **Solution implementation** → Problem + solution + context
- **Bug fix** → Root cause + fix + prevention
- **Architecture decision** → Options + choice + rationale
- **Pattern discovery** → Reusable approach + examples

### Memory Structure

```yaml
# Universal memory fields
memory:
  type: solution | problem | code_pattern | fix | error | workflow
  title: "Specific, searchable title (not generic)"
  content: "Detailed explanation with context"
  tags: ["project-agnostic", "universal", "pattern"]
  importance: 0.8  # 0.8+ critical, 0.5-0.7 standard, 0.3-0.4 minor
  relationships: ["SOLVES:problem-1", "RELATED_TO:pattern-5"]
```

### Universal Recall Patterns

```python
# Universal knowledge recall
from memorygraph import recall_memories, search_memories

# Fuzzy recall for conceptual queries
results = recall_memories(
    query="timeout handling patterns",
    memory_types=["solution", "pattern"]
)

# Exact search for specific terms
exact_results = search_memories(
    tags=["timeout", "pattern"],
    min_importance=0.7
)
```

## When to Use Me

Use this skill when:

- Implementing cross-project knowledge sharing
- Creating reusable solution patterns
- Standardizing documentation practices
- Building organizational memory systems

## Universal Integration Examples

### Cross-Project Knowledge Sharing

```python
# Universal knowledge storage
store_memory(
    type="code_pattern",
    title="Universal timeout handling pattern",
    content="""
    def with_timeout(func, timeout=5, default=None):
        try:
            return func()
        except TimeoutError:
            return default
    """,
    tags=["python", "timeout", "pattern", "universal"],
    importance=0.9
)
```

### Solution Relationships

```python
# Universal relationship mapping
create_relationship(
    from_memory_id="solution-timeout-pattern",
    to_memory_id="problem-slow-api",
    relationship_type="SOLVES",
    context="Pattern addresses API timeout issues"
)
```

## Best Practices

1. **Tagging**: Use consistent tags across projects for discoverability
1. **Importance**: Standardize importance scoring system
1. **Relationships**: Link related knowledge across projects
1. **Maintenance**: Regular knowledge base cleanup and organization

## Compatibility

Designed for:

- Cross-project knowledge management
- Organizational learning systems
- Reusable pattern libraries
- Universal documentation standards
