---
name: summarize
version: 1.0.0
changelog: Initial FILTER-CHUNK-STITCH-VERIFY pattern
description: Prepare context for compaction. Run before /compact to ensure critical state survives.
---

# Summarize

Prepare context for compaction using FILTER-CHUNK-STITCH-VERIFY pattern.

Run this before `/compact` to ensure critical state survives.

## Task
$ARGUMENTS

## Instructions

Output: `## Summarize`

**State**: Preserve current phase in STATE.md. This command prepares for compaction, not phase transition.

### 1. FILTER — Extract Critical State

Identify only decision-critical information:
- Current phase (research | plan | implement | debug)
- Task description (one sentence)
- Decisions made with rationale
- Blockers and open questions
- Key file references (`path:line` format)

**Discard**: Exploratory content, verbose tool outputs, superseded attempts.

### 2. CHUNK — Structure for Parsing

**Read current metrics** using shared script:

```bash
.claude/skills/shared/scripts/read-metrics.sh used_percentage
```

Write STATE.md with YAML frontmatter (see [state template](../shared/templates/state.md)):

```markdown
---
task: "Brief task description"
status: in_progress | blocked | complete
phase: research | plan | implement | debug
context_percent: [from metrics]
last_updated: [today's date]
---

## Decisions
- [Decision]: [rationale]

## Blockers
- [ ] [Unresolved issue]

## Key Files
- `path:line` — [why it matters]

## Next Steps
[Specific guidance for resuming]
```

### 3. STITCH — Dual Output

1. **Write STATE.md** (survives compact/clear/new session)
2. **Output summary to conversation**:

```markdown
## Context Summary

**Task**: [one-line]
**Phase**: [current phase]
**Status**: [in_progress | blocked | complete]

**Key decisions**: [bullet list]
**Blockers**: [if any]
**Next**: [what to do after compact]
```

This in-context summary is what `/compact` will preserve.

### 4. VERIFY — Completeness Check

Ask yourself: "Given only STATE.md and the summary above, could work resume?"

If uncertain, flag what might be missing before proceeding.

## Constraints

- Keep STATE.md under 100 lines
- YAML frontmatter must be valid (no tabs, proper quoting)
- Don't include full file contents — only references
- Focus on "what's needed to continue" not "what happened"

## Exit Criteria

STATE.md written. Summary output to conversation. Ready for `/compact`.
