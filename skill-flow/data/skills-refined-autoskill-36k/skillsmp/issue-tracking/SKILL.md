---
name: issue-tracking
description: Universal issue tracking and task management patterns using beads/bd system
license: MIT
compatibility: opencode
metadata:
    related_mcp_servers: For MCP server integration patterns, use skill `mcp-servers`
    related_knowledge_management: For storing issue-related knowledge, use skill `knowledge-management`
---

# Issue Tracking

## What I Do

Provide universal patterns for issue tracking and task management that can be applied across different projects and domains.

## Universal Issue Tracking Patterns

### Core Workflow

```bash
# Universal issue tracking workflow
bd ready --json                    # Find unblocked work
bd create "Task" -t bug|feature|task -p 0-4 --json  # Create issue
bd update <id> --status in_progress --json  # Claim task
bd close <id> --reason "Completed" --json   # Complete task
```

### Issue Types and Priorities

**Universal Issue Types:**

- `bug` - Something broken
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature with subtasks
- `chore` - Maintenance (dependencies, tooling)

**Universal Priority System:**

- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

### Dependency Management

```bash
# Universal dependency patterns
bd create "Subtask" --parent <epic-id> --json  # Hierarchical structure
bd create "Bug" -p 1 --deps discovered-from:<parent-id> --json  # Discovery linking
```

## When to Use Me

Use this skill when:

- Setting up issue tracking in new projects
- Standardizing task management across teams
- Creating reusable workflow patterns
- Implementing cross-project consistency

## Universal Integration Examples

### Git Integration

```bash
# Universal git-issue synchronization
bd sync  # Auto-sync with git (5s debounce)
git add .beads/issues.jsonl  # Always commit issue state with code
```

### MCP Server Integration

```python
# Universal MCP server usage
from beads_mcp import ready, create, update, close

# Find ready work
ready_issues = ready(limit=10)

# Create issue via MCP
new_issue = create(
    title="Universal pattern implementation",
    issue_type="feature",
    priority=1
)
```

## Best Practices

1. **Consistency**: Use the same issue types and priorities across projects
1. **Traceability**: Always link discovered work with `discovered-from` dependencies
1. **Automation**: Integrate with CI/CD pipelines for automatic status updates
1. **Documentation**: Store workflow documentation in project-specific files

## Compatibility

Works with:

- Any project using beads/bd system
- MCP-compatible clients (Claude, OpenCode, etc.)
- Cross-project workflow standardization
