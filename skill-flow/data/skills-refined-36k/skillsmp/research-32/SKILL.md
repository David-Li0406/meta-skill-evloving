---
name: research
version: 1.0.0
changelog: Added wave execution, subagent model selection
description: Understand problem space before proposing changes. Use when exploring unfamiliar code, analyzing requirements, or planning features that need investigation.
allowed-tools: Read, Grep, Glob, Task, WebFetch
temperature: 0.3-0.5  # Slight creativity for exploration
---

# Research Phase

Before proposing changes, understand the problem space.

## Task
$ARGUMENTS

## Instructions

Output: `## Research Phase`

**State**: At phase start, update STATE.md:
- Set `task:` from $ARGUMENTS (if STATE.md is idle/complete or task is "None")
- Set `phase: research`
- Set `status: in_progress`

### 1. Study the Relevant Context
- Read all user-mentioned files completely (no limit/offset)
- Study existing patterns in the codebase
- Don't assume functionality is missing—confirm with search first

### 2. Decompose the Problem
Break into composable research areas. Use subagents for parallel exploration:
- Up to 500 parallel subagents for searches/reads
- Keep parent context focused on synthesis

**Wave-based execution** — group operations by dependency:

```
Wave 1 (parallel):     Wave 2 (parallel):     Wave 3 (synthesis):
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│ Glob: find  │        │ Read file A │        │ Analyze     │
│ all *.ts    │        └─────────────┘        │ patterns    │
└─────────────┘        ┌─────────────┐        └─────────────┘
┌─────────────┐   →    │ Read file B │   →
│ Grep: find  │        └─────────────┘
│ "pattern"   │        ┌─────────────┐
└─────────────┘        │ Read file C │
                       └─────────────┘
```

**Rules**:
- Wave 1: Discovery (glob, grep) — all parallel
- Wave 2: Reading (Task with haiku) — all parallel
- Wave 3: Synthesis — sequential, in parent context

**Subagent model selection** (10x cost difference):

| Task Type | Model | Why |
|-----------|-------|-----|
| File searches, grep, glob | `haiku` | Pattern matching only |
| Reading/summarizing files | `haiku` | Extraction, not reasoning |
| Code exploration | `sonnet` | Balance speed/understanding |
| Complex analysis | `opus` | Multi-step reasoning |

Example: Launch multiple searches in one message:
```
Task(prompt="find all API routes", model="haiku")
Task(prompt="find all middleware", model="haiku")
Task(prompt="find auth patterns", model="haiku")
```

### 3. Map the Territory
- Identify files, modules, and dependencies involved
- Understand information flow
- Note existing conventions and patterns
- Surface assumptions for validation

### 4. Identify Risks
- What could go wrong?
- What's unclear or underspecified?
- Where might the approach need adjustment?

### 5. Produce Research Artifact

Use the [findings template](templates/findings.md) structure:

```yaml
## Summary
[Concise overview of findings]

## Relevant Files
- `file:line` — description

## Patterns Discovered
- Pattern name: where it's used

## Assumptions
- [ ] Assumption to validate

## Questions
- Open questions for clarification

## Recommended Approach
[Brief description of proposed direction]
```

**Structured output hint**: For complex research, consider JSON-style output for machine-parseable sections:

```json
{
  "files": [{"path": "src/auth.ts", "line": 42, "role": "entry point"}],
  "patterns": [{"name": "singleton", "usage": "database connection"}],
  "risks": ["coupling", "missing tests"]
}
```

This aids downstream planning tools if integrated.

## Constraints

- **Do not propose solutions or write code**
- Focus on understanding, not implementing
- Be a documentarian, not a critic
- Maximum 125 characters for quoted source material
- Verify claims before stating them

### 6. Incremental State Updates

Update STATE.md **during research** when:
- Significant pattern or constraint discovered → add to `## Decisions`
- Key file identified → add to `## Key Files`
- Blocker found → add to `## Blockers`

**At research completion**:
- Update `## Next Steps` with research conclusions
- Run `/checkpoint` if context is heavy or taking a break

### 7. Produce Handoff

Before exit gate, append handoff to STATE.md under `## Research Findings`:

```markdown
## Research Findings

### Completed
- [x] [What was researched]

### Context
**Key Files**:
- `path:line` — why it matters

**Patterns Discovered**:
- [Pattern]: [where used]

**Constraints**:
- [Must/Cannot statements]

**Decisions Made**:
- [Decision]: [rationale]

### Remaining
- [ ] Create implementation plan
- [ ] [Specific items for planning phase]
```

See [handoff template](../shared/templates/handoff.md) for full format.

## Exit Criteria

Can explain the problem space and proposed approach without hand-waving.

**Gate**: "Here's what I found. Ready to plan?"
