---
name: serena-memory
description: Manage project knowledge using Serena's memory system. Use for storing design decisions, coding conventions, learned patterns, and project-specific context that persists across sessions.
---

# Serena Memory Skill

Manage persistent project knowledge using Serena MCP's memory system.

## Core Principles

1. **Structured storage**: Organize memories by category for easy retrieval
2. **Actionable content**: Store information that helps future development
3. **Keep current**: Update memories when decisions change
4. **Clean regularly**: Remove outdated or redundant memories

## Serena MCP Tools

### Memory Operations
- `mcp__serena__write_memory`: Create or update a memory
- `mcp__serena__read_memory`: Retrieve specific memory content
- `mcp__serena__list_memories`: List all available memories
- `mcp__serena__delete_memory`: Remove outdated memories

### Context Tools
- `mcp__serena__read_file`: Read code for context when needed
- `mcp__serena__get_symbols_overview`: Understand code structure
- `mcp__serena__search_for_pattern`: Find relevant code patterns

## Memory Categories

### Architecture Decisions (ADR)
- Technology choices and rationale
- Pattern selections
- Trade-off analyses
- Rejected alternatives

### Coding Conventions
- Naming patterns
- File organization rules
- Error handling patterns
- Testing conventions

### Project Context
- Business domain concepts
- Key terminology
- Stakeholder requirements
- Known constraints

### Learned Patterns
- Common code patterns in this project
- Gotchas and pitfalls
- Performance considerations
- Security requirements

### Task History
- Completed refactorings
- Migration status
- Technical debt items
- Future improvement ideas

## Memory Naming Convention

Use structured names for easy discovery:

```
adr/[topic]           - Architecture decisions
conventions/[area]    - Coding standards
context/[domain]      - Business context
patterns/[name]       - Code patterns
tasks/[status]/[name] - Task tracking
```

## Operations

### Store New Knowledge
```
1. Determine category
2. Choose descriptive name
3. Write structured content
4. Verify with list_memories
```

### Retrieve Knowledge
```
1. list_memories to find relevant items
2. read_memory for specific content
3. Apply to current task
```

### Update Knowledge
```
1. read_memory current content
2. Modify as needed
3. write_memory with updated content
```

### Cleanup
```
1. list_memories to review all
2. Identify outdated items
3. delete_memory for each
```

## Response Format

```
## Operation: [store/retrieve/update/cleanup]

### Action Taken

[Description of what was done]

### Memory Content

[Content stored/retrieved if applicable]

### Current Memories

| Name | Category | Summary |
|------|----------|---------|
| ...  | ...      | ...     |
```

## Task: $ARGUMENTS

Manage project knowledge as requested:

$ARGUMENTS

Use Serena's memory system to persist information across sessions.
