# Delegation Reference

## Core Principle

**Delegate first, act later.** Never search, plan, or edit before delegation completes.

## Context Budget

Control how much context to pass to delegates based on task scope.

| Task Size | Context Strategy | Max Lines |
|-----------|------------------|-----------|
| Small | Single relevant file | ~500 |
| Medium | File + direct imports + related tests | ~2000 |
| Large | Summary + key sections + file list only | ~1000 |

### Context Selection Priority
1. Files directly mentioned in the task
2. Files discovered during search phase
3. Test files for touched code
4. Import/dependency files (one level)
5. Config files if behavior-relevant

### Trimming Strategy
- Remove boilerplate (license headers, long comments)
- Collapse repetitive code (show first + "... N more similar")
- Summarize large data structures
- Keep function signatures, trim implementations if needed

## Delegation Contract

### Input Requirements
Every delegate call MUST include:
```json
{
  "goal": "one-line task description",
  "constraints": ["constraint1", "constraint2"],
  "files": ["path/to/file1.ts", "path/to/file2.ts"],
  "context": "relevant code snippets or summaries",
  "output_format": "json|markdown|patch"
}
```

### Output Requirements
Delegate MUST return at least one of:
- Concrete commands to run
- File paths + exact edits (line numbers)
- Checklist with pass/fail criteria

## Failure Handling

| Failure Type | Action |
|--------------|--------|
| Timeout (>120s) | Retry once with 50% context |
| Parse error | Ask delegate to reformat as JSON |
| Empty response | Retry with simpler prompt |
| Inconsistent output | Log conflict, ask user to verify |
| MCP unavailable | Use subagent fallback, disclose it |

### Retry Policy
```
max_retries: 1
backoff: 500ms
context_reduction: 50% on timeout
```

### Fallback Chain
1. MCP tool (primary)
2. Subagent with same role config (fallback)
3. Ask user to enable MCP (last resort)

## Parallel vs Sequential

| Delegate Type | Execution |
|---------------|-----------|
| Read-only (pathfinder, scout) | Parallel OK |
| Analysis (sage) | Parallel OK |
| Write-capable (patch output) | Sequential only |

### Write-capable Rules
- One write delegate at a time
- Verify output before next delegate
- Host applies edits (delegate returns patch only)
- If delegate attempts direct edit, stop and re-run as patch-only

## Delegation Sequence

### Standard Task
```
1. pathfinder → find relevant files
2. [parallel] scout + sage → analyze
3. synthesize findings
4. execute changes
5. verify
```

### Ultrawork Mode (staged)
```
Stage 1 (Discovery):
  - pathfinder: file structure + entrypoints

Stage 2 (Analysis):
  - sage: deep reasoning (mandatory for complex tasks)
  - scout: doc/pattern verification

Stage 3 (Review):
  - additional roles as configured

Then: plan → execute → verify → cleanup
```
