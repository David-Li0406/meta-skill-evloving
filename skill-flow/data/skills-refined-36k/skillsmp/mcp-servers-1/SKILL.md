---
name: mcp-servers
description: Universal patterns for using MCP (Multi-Client Protocol) servers in agentic workflows
license: MIT
compatibility: opencode
metadata:
    related_issue_tracking: For task management with MCP servers, use skill `issue-tracking`
    related_knowledge_management: For memory and knowledge storage, use skill `knowledge-management`
---

# MCP Servers

## What I Do

Provide universal patterns and best practices for integrating MCP servers into agentic workflows across different projects and domains.

## Universal MCP Server Patterns

### Server Discovery and Selection

- Keep the authoritative list of servers in `.vscode/mcp.json` and audit it whenever project needs change
- Document server capabilities (inputs, outputs, limitations) so agents can choose correctly without probing
- Verify availability early by issuing lightweight health or `list_*` commands rather than waiting for first real use
- Prefer a small, purposeful tool set to keep the assistant's tool offers focused and predictable

### Common MCP Server Types

| Server Type | Typical Use Cases | Integration Pattern |
| --- | --- | --- |
| `memorygraph` | Long-term knowledge storage | `recall_memories(query="project-specific knowledge")` |
| `beads-mcp` | Issue tracking | `bd ready --json` |
| `sequential-thinking` | Complex problem analysis | Multi-step thought process |
| `desktop-commander` | File operations | Unified file system interface |
| `serena` | Semantic code operations | Symbol-level code retrieval and editing |
| `fetch` | Web content ingestion | `fetch(url="https://example.com")` |
| `gh_grep` | Public GitHub code search | Query literal or regex patterns across repos |
| `upstash-context7` | Documentation recall | Natural language queries over curated doc sets |

### Simple Utility Servers

These lightweight servers complement the core development stack without overwhelming the assistant:

- **fetch** — Retrieves up-to-date web content (HTML, markdown, raw text). Use it for vendor docs or standards that change frequently.
- **gh_grep** — Mirrors `grep.app` functionality for discovering real-world code snippets. Use literal or regex queries to find idiomatic usage.
- **upstash-context7** — Provides semantic retrieval across curated documentation (e.g., vendor APIs, SDK guides). Query with natural language to ground decisions in official sources.

### Integration Best Practices

1. **Context Management**: Always load project context before using MCP servers
1. **Error Handling**: Implement graceful fallbacks when servers are unavailable
1. **Performance**: Cache frequently used server responses
1. **Security**: Validate server responses before processing

## When to Use Me

Use this skill when:

- Setting up MCP server integrations in new projects
- Standardizing agent tool usage across multiple projects
- Creating reusable agent workflows
- Implementing cross-project knowledge sharing

## Universal Examples

### Memory Graph Integration

```python
# Universal memory storage pattern
store_memory(
    type="solution",
    title="Cross-project solution pattern",
    content="Reusable approach for X",
    tags=["universal", "pattern"],
    importance=0.8
)

# Universal memory recall
memories = recall_memories(
    query="reusable patterns",
    memory_types=["solution", "pattern"]
)
```

### Issue Tracking Workflow

```python
# Universal issue creation
issue = bd_create(
    title="Implement universal pattern",
    description="Create reusable component for X",
    issue_type="feature",
    priority=1
)

# Universal issue management
bd_update(issue.id, status="in_progress")
```

## Compatibility Notes

This skill is designed to work with:

- OpenCode agent framework
- Claude-compatible MCP clients
- Any project using MCP servers
- Cross-project knowledge sharing workflows
