# Summarize Session Run

Analyze a Claude Code session log and produce a structured summary.

## Input

A Claude Code session log (JSONL format) containing conversation turns, tool calls, and results.

## Instructions

1. **Identify the Task**
   - What was the user trying to accomplish?
   - Was there a clear goal or was it exploratory?

2. **Trace the Workflow**
   - What tools were used and in what order?
   - Were there any tool failures or retries?
   - How many iterations did it take?

3. **Note Key Decisions**
   - What architectural or implementation choices were made?
   - Were there alternatives considered?
   - Why was the chosen approach selected?

4. **Identify What Worked**
   - Which approaches succeeded on first try?
   - What patterns led to quick resolution?
   - Any clever solutions or shortcuts?

5. **Identify What Didn't Work**
   - What caused errors or required retries?
   - Were there misunderstandings or incorrect assumptions?
   - What approaches were abandoned?

6. **Extract Surprising Behaviors**
   - Anything unexpected about tool behavior?
   - Edge cases encountered?
   - Gotchas or pitfalls discovered?

## Output Format

```markdown
## Session Summary

**Task:** [Brief description of what was attempted]

**Outcome:** [Success/Partial/Failed]

**Duration:** [Approximate session length if determinable]

### Workflow

1. [Step 1]
2. [Step 2]
...

### What Worked

- [Success pattern 1]
- [Success pattern 2]

### What Didn't Work

- [Failure pattern 1]
- [Failure pattern 2]

### Key Decisions

- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### Surprises/Gotchas

- [Unexpected behavior or discovery]
```

## Notes

- Focus on patterns that could be reusable across projects
- Redact any sensitive information (secrets, personal paths)
- If the session is unclear or corrupted, note that and extract what you can
