# Task TASK-XXX: <Title>

---

## WORKFLOW REQUIREMENT

**This task MUST be implemented via the `engineer` agent.**

Direct implementation is PROHIBITED. The correct workflow is:

1. PM creates this task file
2. PM invokes `engineer` agent with `subagent_type="engineer"`
3. Engineer agent implements, tracks metrics, creates PR
4. PM invokes `senior-engineer-pr-lead` agent for PR review
5. SR Engineer approves and merges

If you are reading this task file and about to implement it yourself, **STOP**.
Use the Task tool to spawn the engineer agent instead.

---

## Goal

<Clear, concise statement of what this task accomplishes. 1-2 sentences.>

## Non-Goals

<Explicitly list what this task does NOT do. Prevents scope creep.>

- Do NOT <thing 1>
- Do NOT <thing 2>
- Do NOT <thing 3>

## Deliverables

<List of files to create or modify>

1. New file: `<path/to/file.ts>`
2. Update: `<path/to/existing.ts>`

## Acceptance Criteria

<Checkboxes that must ALL be true for the task to be complete>

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] All CI checks pass

## Implementation Notes

<Detailed guidance on HOW to implement. Include code examples.>

### Key Patterns

```typescript
// Example code showing expected patterns
```

### Important Details

- Detail 1
- Detail 2

## Integration Notes

<How this task connects to other tasks/systems>

- Imports from: `<files>`
- Exports to: `<files>`
- Used by: TASK-XXX, TASK-YYY
- Depends on: TASK-ZZZ (must complete first)

## Do / Don't

### Do:

- <Positive guidance>
- <Positive guidance>

### Don't:

- <Negative guidance>
- <Negative guidance>

## When to Stop and Ask

<Conditions where the engineer should stop and ask the PM>

- If <condition 1>
- If <condition 2>
- If <condition 3>

## Testing Expectations (MANDATORY)

### Unit Tests

- Required: Yes / No
- New tests to write:
  - <what logic>
- Existing tests to update:
  - <what behavior>

### Coverage

- Coverage impact:
  - <must not decrease / target % / not enforced with reason>

### Integration / Feature Tests

- Required scenarios:
  - <scenario>

### CI Requirements

This task's PR MUST pass:
- [ ] Unit tests
- [ ] Integration tests (if applicable)
- [ ] Coverage checks
- [ ] Type checking
- [ ] Lint / format checks

**PRs without tests when required WILL BE REJECTED.**

## PR Preparation

- **Title**: `feat(scope): <description>`
- **Labels**: `<label1>`, `<label2>`
- **Depends on**: TASK-XXX (if applicable)

---

## PM Estimate (PM-Owned)

**Category:** `<schema | service | ipc | ui | refactor | test | config | docs>`

**Estimated Tokens:** ~XK-YK

**Token Cap:** XK (4x upper estimate)

> If you reach this cap, STOP and report to PM. See `.claude/docs/shared/token-cap-workflow.md`.

**Estimation Assumptions:**

| Factor | Assumption | Impact |
|--------|------------|--------|
| Files to create | X new files | +XK |
| Files to modify | X files (scope: small/medium/large) | +XK |
| Code volume | ~X lines | +XK |
| Test complexity | Low/Medium/High | +XK |

**Confidence:** Low / Medium / High

**Risk factors:**
- <uncertainty 1>
- <uncertainty 2>

**Similar past tasks:** <TASK-XXX (actual: XK tokens) if applicable>

---

## Implementation Summary (Engineer-Owned)

**REQUIRED: Record your agent_id immediately when the Task tool returns.**

*Completed: <DATE>*

### Agent ID

**Record this immediately when Task tool returns:**
```
Engineer Agent ID: <agent_id from Task tool output>
```

### Checklist

```
Files created:
- [ ] <file 1>
- [ ] <file 2>

Features implemented:
- [ ] <feature 1>
- [ ] <feature 2>

Verification:
- [ ] npm run type-check passes
- [ ] npm run lint passes
- [ ] npm test passes (if applicable)
```

### Metrics (Auto-Captured)

**From SubagentStop hook** - Run: `grep "<agent_id>" .claude/metrics/tokens.jsonl | jq '.'`

| Metric | Value |
|--------|-------|
| **Total Tokens** | X |
| Duration | X seconds |
| API Calls | X |
| Input Tokens | X |
| Output Tokens | X |
| Cache Read | X |
| Cache Create | X |

**Variance:** PM Est ~XK vs Actual ~XK (X% over/under)

### Notes

<REQUIRED: Document the following>

**Planning notes:**
<Key decisions from planning phase, revisions if any>

**Deviations from plan:**
<If you deviated from the approved plan, explain what and why. Use "DEVIATION:" prefix.>
<If no deviations, write "None">

**Design decisions:**
<Document any design decisions you made and the reasoning>

**Issues encountered:**
<Document any issues or challenges and how you resolved them>

**Reviewer notes:**
<Anything the reviewer should pay attention to>

### Estimate vs Actual Analysis

**REQUIRED: Compare PM token estimate to actual to improve future predictions.**

| Metric | PM Estimate | Actual | Variance |
|--------|-------------|--------|----------|
| **Tokens** | ~XK | ~XK | +/-X% |
| Duration | - | X sec | - |

**Root cause of variance:**
<1-2 sentence explanation of why estimate was off, e.g., "Complex type debugging", "Clean implementation with existing patterns">

**Suggestion for similar tasks:**
<What should PM estimate differently next time? e.g., "This category should use 0.5x multiplier">

---

## SR Engineer Review (SR-Owned)

**REQUIRED: Record your agent_id immediately when the Task tool returns.**

*Review Date: <DATE>*

### Agent ID

```
SR Engineer Agent ID: <agent_id from Task tool output>
```

### Metrics (Auto-Captured)

**From SubagentStop hook** - Run: `grep "<agent_id>" .claude/metrics/tokens.jsonl | jq '.'`

| Metric | Value |
|--------|-------|
| **Total Tokens** | X |
| Duration | X seconds |
| API Calls | X |

### Review Summary

**Architecture Compliance:** PASS / FAIL
**Security Review:** PASS / FAIL / N/A
**Test Coverage:** Adequate / Needs Improvement

**Review Notes:**
<Key observations, concerns addressed, approval rationale>

### Merge Information

**PR Number:** #XXX
**Merge Commit:** <hash>
**Merged To:** develop / int/xxx
