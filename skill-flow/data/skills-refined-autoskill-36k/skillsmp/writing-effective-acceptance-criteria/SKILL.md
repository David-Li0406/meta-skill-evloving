---
name: writing-effective-acceptance-criteria
description: Use when writing acceptance criteria for milestones or user stories. Covers testability, scope constraints, format selection, and grain-level distinctions.
---

# Writing Effective Acceptance Criteria

## Overview

Acceptance criteria answer the question: "How will we know this is done — and done right?" Good AC are testable, appropriately scoped, and match the grain of the work item they describe. They provide clear completion signals for both human and LLM engineers.

## When to Use

- Writing or reviewing milestone definitions
- Breaking user stories into verifiable conditions
- When AC feel vague ("works correctly", "is user-friendly")
- When AC count exceeds 5 and you need to decide whether to split
- When unsure whether an AC belongs at milestone or task level

## Core Pattern

### Step 1: Verify Testability

Each AC must have a clear pass/fail determination. Ask: "Could I write a test for this? Could I demo it?"

**Testability check**:
- Can someone unfamiliar with the work verify this?
- Is there observable behavior or output?
- Are success conditions unambiguous?

### Step 2: Choose the Right Format

| Format | When to Use | Example |
|--------|-------------|---------|
| **Checklist** | Simple verification, scaffolding, setup | `[ ] CLI returns exit code 0` |
| **Given/When/Then** | Behavior specifications, test automation | `Given a logged-in user, When they click logout, Then session is invalidated` |
| **Rules-based** | Business logic, conditionals | `If order total > $100, then free shipping applies` |
| **Quantitative** | Performance, SLAs, compliance | `Page loads in < 2 seconds at p95` |

Default to **checklist** for simplicity, but use `AskUserQuestion` to ask the user if they have a preference.

### Step 3: Constrain Scope

**Target 5 AC per milestone** (excluding automated tests). More than 5 is a signal the milestone may be too broad.

**When you identify more than 5 AC**:

1. **Propose all AC first.** Don't silently drop criteria — they may be important.
2. **Use AskUserQuestion** to present options:
   - Keep all AC (justified if truly atomic and necessary)
   - Split into separate milestones (if AC cluster into distinct deliverables)
   - Demote some to task-level AC (if some are implementation details)
   - Consolidate redundant AC (if some overlap)
3. **Document the decision.** Note why the constraint was exceeded or how it was resolved.

The 5-AC limit is a smell detector, not a hard rule. Some milestones legitimately need more; the key is making that a conscious choice, not an accident.

### Step 4: Match Grain to Work Item

AC exists at multiple levels:

| Level | Purpose | Example |
|-------|---------|---------|
| **Milestone AC** | Verify milestone is done (demo-focused) | "User can see available commands via --help" |
| **Task AC** | Verify individual work item is done | "Auth command group has login and status subcommands" |

**Heuristic**: Milestone AC should match the specificity of the milestone description. If your description says "command groups for auth, activities, export" then AC can enumerate those groups.

### Step 5: Write the AC

For each criterion:
1. State the observable outcome (not the implementation)
2. Include enough context to verify independently
3. Avoid compound conditions — split "X and Y" into two AC

## Quick Reference

```
AC Checklist:
[ ] Testable — clear pass/fail
[ ] Observable — behavior or output, not internal state
[ ] Independent — can verify without knowing implementation
[ ] Atomic — one condition per AC, no "and"
[ ] Count discussed — if > 5, user chose how to handle
```

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Vague AC ("works correctly") | Not testable, subjective | Specify observable behavior |
| Implementation-focused ("uses Redis") | Prescriptive, not outcome-focused | State the outcome ("cache hit rate > 90%") |
| Compound AC ("X and Y and Z") | Partial pass is ambiguous | Split into separate AC |
| 6+ AC without discussion | User didn't consciously choose scope | Propose all AC, then ask user how to handle |
| Missing expected result | Unclear what success looks like | Include what user sees/receives |
| Task-level detail in milestone AC | Wrong grain, clutters milestone | Save implementation details for task breakdown |

## Anti-Rationalizations

- "This AC is obvious" — If it's obvious, it's quick to write. Write it anyway. Obvious to you isn't obvious to the next engineer.
- "We'll know it when we see it" — That's not acceptance criteria, that's hope. Specify the observable outcome.
- "Five AC is too restrictive" — Five is a signal, not a prison. If you need more, propose them all and ask the user how to proceed. The constraint exists to surface scope conversations, not to silently drop important criteria.
- "This is just a small feature" — Small features still need clear completion criteria. Size doesn't excuse vagueness.

## Formats Reference

### Checklist Format

Best for simple verification. Each item is a yes/no check.

```markdown
**Acceptance Criteria**:
- [ ] `trackman --help` displays available command groups
- [ ] Each command group has a description
- [ ] All commands return exit code 0
```

### Given/When/Then Format

Best for behavior specifications and test automation.

```markdown
**Acceptance Criteria**:
- [ ] Given a user with valid credentials, When they run `trackman auth login`, Then they see "Authentication successful"
- [ ] Given invalid credentials, When they run `trackman auth login`, Then they see an error message and exit code 1
```

### Rules-Based Format

Best for business logic with conditionals.

```markdown
**Acceptance Criteria**:
- [ ] If activity type is RANGE_PRACTICE, include stroke count in output
- [ ] If activity type is COMBINE_TEST, include score and max club speed
- [ ] If activity has no strokes, display "No data available"
```

### Quantitative Format

Best for performance requirements and SLAs.

```markdown
**Acceptance Criteria**:
- [ ] Activity list loads in < 3 seconds for 50 activities
- [ ] Export to CSV completes in < 5 seconds for 1000 shots
- [ ] CLI startup time < 500ms
```

## Summary

1. **Every AC must be testable.** If you can't write a test or demo it, rewrite it.
2. **Target 5 AC per milestone.** More than 5 is a signal — propose all, then ask user how to proceed.
3. **Match grain to work item.** Milestone AC are demo-focused; task AC are implementation-focused.
4. **State outcomes, not implementations.** "User sees confirmation" not "function returns true."
