---
name: create-plan
description: Use this skill when you need to create detailed implementation plans through interactive research and iteration, especially for new features or technical work.
---

# Skill body

## When to Use This Skill

- Planning new features or functionality
- Designing technical implementations before coding
- Creating phased development roadmaps
- Structuring complex refactoring work
- Any task requiring upfront planning and design

## Initial Input Handling

Parse the user's request to identify:

1. **Task description** - What needs to be implemented
2. **Context files** - Relevant existing code or documentation
3. **Constraints** - Timeline, technology, or scope limitations

| Scenario | Action |
|----------|--------|
| Parameters provided | Read all referenced files completely, then proceed to Research |
| Missing task description | Ask: "What feature or functionality should I plan?" |
| No context provided | Ask: "Are there existing files or documentation I should review?" |

## Planning Workflow

### Phase 1: Research

**Critical**: Thoroughly investigate the codebase before planning.

Spawn parallel sub-tasks using specialized agents:

```
Research Tasks:
- codebase-locator: Find all files related to the feature area
- codebase-analyzer: Understand existing patterns and architecture
- Explore: Investigate integration points and dependencies
```

For each research task, provide:
- Specific directories to examine
- Exact patterns or code to find
- Required output: file:line references

**Read all identified files completely** - no partial reads or summaries.

### Phase 2: Present Understanding

Before any design work, present findings:

1. **Codebase Analysis**
   - Relevant existing code with file:line references
   - Current patterns and conventions discovered
   - Integration points and dependencies

2. **Clarifying Questions**
   - Ask only questions that code investigation couldn't answer
   - Focus on business logic, user requirements, edge cases
   - Avoid questions answerable by reading more code

Wait for user response before proceeding to design the implementation plan.