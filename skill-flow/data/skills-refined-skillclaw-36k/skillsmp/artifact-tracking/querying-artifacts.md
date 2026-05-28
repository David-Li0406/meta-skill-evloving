# QUERY Function: Finding Tasks, Blockers, and Generating Reports

Use artifact-query agent for token-efficient queries across progress files.

## Find Pending Tasks

**Command**:
```markdown
Task("artifact-query", "Show all pending tasks in [PRD] phases 1-3")
```

**Returns**: Task IDs, descriptions, assigned agents, dependencies

## Find Blocked Tasks

**Command**:
```markdown
Task("artifact-query", "Find all blocked tasks in [PRD] with blocker details")
```

**Returns**: Task IDs, blocker IDs, severity, blocking chains

## Find Tasks by Agent

**Command**:
```markdown
Task("artifact-query", "Show all tasks assigned to ui-engineer-enhanced in [PRD]")
```

**Returns**: Tasks grouped by phase with status

## Find Critical Path

**Command**:
```markdown
Task("artifact-query", "Show critical path for [PRD] Phase [N]")
```

**Returns**: Longest dependency chain with total estimated time

## Generate Session Handoff

**Command**:
```markdown
Task("artifact-query", "Generate session handoff for [AGENT] continuing [PRD] Phase [N]")
```

**Returns**:
- Current phase status
- Pending tasks in priority order
- Active blockers
- Implementation decisions from context
- Immediate next actions

## Calculate Progress

**Command**:
```markdown
Task("artifact-query", "Calculate overall progress for [PRD] across all phases")
```

**Returns**: Phase-by-phase breakdown with completion percentages

## Query Context Decisions

**Command**:
```markdown
Task("artifact-query", "Show all implementation decisions in [PRD] context file")
```

**Returns**: Decisions with rationale and locations

## Query Gotchas

**Command**:
```markdown
Task("artifact-query", "List all gotchas from [PRD] context affecting [component]")
```

**Returns**: Gotchas with solutions and affected files

## Token Efficiency Examples

| Query | Traditional | Optimized |
|-------|-------------|-----------|
| All pending tasks | 480KB (3 files) | 6KB |
| Session handoff | 820KB (6 files) | 7KB |
| Critical path | 160KB (1 file) | 2KB |

## Query Patterns

See `./query-patterns.md` for advanced query examples including:
- Cross-phase queries
- Filter combinations
- Aggregation queries
- Timeline queries
