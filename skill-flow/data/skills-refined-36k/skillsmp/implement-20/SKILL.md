---
name: implement
version: 1.0.0
changelog: Added wave execution, deviation rules, goal-backward verification
description: Execute approved plan incrementally with verification at each step. Use after plan is approved.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
temperature: 0.0  # Deterministic for code generation
---

# Implementation Phase

Execute the approved plan incrementally.

## Plan Reference
$ARGUMENTS

## Instructions

Output: `## Implementation Phase`

**State**: At phase start, update STATE.md:
- Set `task:` from $ARGUMENTS (if STATE.md is idle/complete or task is "None")
- Set `phase: implement`
- Set `status: in_progress`

### 1. Consume Plan Handoff

Read `## Plan` from STATE.md:
- Use **Plan Summary** as execution checklist
- Run **Verification Commands** after each step
- Monitor **Risks Identified** during execution

### 2. Execute Using Wave Pattern
Group independent operations for efficiency:

**Wave-based execution**:
```
Wave 1 (parallel):     Wave 2 (sequential):   Wave 3 (verify):
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│ Edit file A │        │ Build       │        │ Test        │
└─────────────┘        └──────┬──────┘        └──────┬──────┘
┌─────────────┐   →           │          →          │
│ Edit file B │               ▼                     ▼
└─────────────┘        ┌─────────────┐        ┌─────────────┐
┌─────────────┐        │ Lint        │        │ Verify      │
│ Edit file C │        └─────────────┘        └─────────────┘
└─────────────┘
```

**Rules**:
- Wave 1: Independent edits — all parallel in one message
- Wave 2: Build/lint — sequential (depends on edits)
- Wave 3: Test/verify — sequential (depends on build)

**Per-step requirements**:
- Complete step fully before moving to next
- Verify each step per the plan's criteria
- Mark steps complete as you go

### 3. Maintain Context Hygiene

**Check metrics** after every 3-5 steps:

```bash
.claude/skills/shared/scripts/read-metrics.sh used_percentage
```

| Utilization | Action |
|-------------|--------|
| < 50% | Continue |
| 50-60% | Warn user, consider `/checkpoint` |
| 60%+ | **STOP**: Run `/summarize` then `/compact` before continuing |

**Output practices**:
- Keep output concise
- Use `run_silent` patterns for test/build (see [run_silent.sh](scripts/run_silent.sh))
- Summarize verbose command output
- Run `/checkpoint` after each verified phase

**Fail-fast flags** (stop at first failure):

| Framework | Flag |
|-----------|------|
| pytest | `-x` |
| jest | `--bail` |
| vitest | `--bail` |
| go test | `-failfast` |

### 4. Handle Deviations

**Deviation Rules** (from `agent_docs/workflow.md`):

| Condition | Action |
|-----------|--------|
| Minor syntax/typo fixes | Auto-fix, continue |
| Missing import/dependency | Add it, continue |
| Small refactor needed (<5 lines) | Do it, continue |
| Architectural change needed | **STOP**, explain, get approval |

If something doesn't work as planned:
1. Stop immediately
2. Explain what happened
3. Propose adjustment
4. Get approval before continuing

If errors occur:
1. Feed error back into context (formatted concisely)
2. Attempt self-correction
3. After 2-3 consecutive failures, escalate to human

### 5. Report Progress

Use the [progress report template](templates/progress-report.md):

```markdown
## Phase N Complete

### Completed
- [x] Step description

### Verified
- `npm test` ✓
- `npm run build` ✓

### Notes
Any learnings or adjustments made

### Next
What's coming in the next phase
```

### 6. Pause for Human Verification

- Pause after each phase for human review
- Never check off manual testing steps until user confirms
- Don't rush—maintain quality over speed

## Anti-Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| Overbaking | Adding unrequested features | Stick to spec |
| Running forever | No checkpoints | Bounded cycles with `/checkpoint` |
| Context hoarding | Keeping everything "just in case" | Aggressive pruning |
| Vibe coding | Implementation without understanding | Research first |

## Constraints

- Follow the plan's intent while adapting to what you find
- Plans are guides, not rigid specifications
- Maintain "forward momentum" while keeping end goal in mind
- If stuck for more than 2-3 attempts, ask for help

## Exit Criteria

All plan steps complete. Before marking done, verify each deliverable passes **Goal-Backward Verification**:

1. **Exists**: The thing was created/modified
2. **Substantive**: It does what it's supposed to do
3. **Wired**: It's connected to the rest of the system

### Verification Output Format

When implementation is complete, output:

```markdown
## Implementation Complete

### Deliverables
- [x] [What was created/modified]

### Verification Checklist
| Check | Status | Evidence |
|-------|--------|----------|
| Exists | ✓ | [file:line or description] |
| Substantive | ✓ | [test result or behavior confirmed] |
| Wired | ✓ | [how it connects to system] |

### Manual Testing Required
- [ ] [Specific steps for human to verify]

Ready for review.
```

**Gate**: "Implementation complete. Please verify."
