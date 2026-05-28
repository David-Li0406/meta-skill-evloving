---
name: parallel-agent-dispatch
description: Use this skill to dispatch multiple independent agent tasks for concurrent execution when facing unrelated failures or features that require simultaneous work.
---

# Parallel Agent Dispatch Skill

## Overview

This skill addresses scenarios where multiple independent failures or features exist across different systems. Instead of sequential investigation, create separate agent tasks that work on distinct problem domains simultaneously.

## When to Use

**Use when:**
- 3+ test files failing with different root causes
- Multiple independent bugs/features
- No shared state between the work
- Features with no shared code paths
- Independent refactoring tasks

**Avoid when:**
- Failures might be related (fix one = fix others)
- Agents would edit the same files
- Full system context is required
- Sequential ordering matters
- Debugging requires a holistic view

## Implementation Pattern

### Step 1: Load Context

Get project config and check for prior strategies:

```
ec_search:
  query: project config
  type: config

ec_search:
  query: parallel agent strategy
  type: learning
```

### Step 2: Identify Independent Domains

Group problems by what's broken:

```
Failure Analysis:
├── approval-flow.test.ts → Approval subsystem
├── batch-completion.test.ts → Batch subsystem
├── abort-handler.test.ts → Abort subsystem
└── notification.test.ts → Notification subsystem
```

If fixing one might fix another, they are not independent.

### Step 3: Check for Shared Dependencies

Search EC for known coupling:

```
ec_search:
  query: [component A] depends
  type: learning

ec_search:
  query: [component B] coupling
  type: pattern
```

If EC indicates these components are coupled, don't parallelize.

### Step 4: Create Focused Tasks

Each agent gets:
- **Specific scope** - One file or subsystem
- **Clear goal** - Make these tests pass
- **Constraints** - Don't change other code
- **EC context** - Relevant patterns/learnings for that area
- **Expected output** - Summary of findings and fixes

Example task definition:

```markdown
## Agent Task: [Domain Name]

**Scope:** [Specific files/modules]

**Goal:** [Clear objective]

**Constraints:**
- Only modify files in [scope]
- Do NOT change [protected areas]
- Must maintain [invariants]

**Deliverable:**
- [ ] Tests passing
- [ ] Summary of changes
- [ ] Any discovered issues
```

### Step 5: Set Up Progress Tracking

**Choose ONE approach** (don't mix Tasks and TodoWrite):

**Option A: Tasks (Preferred)**
If TaskCreate/TaskUpdate tools are available:
```
TaskCreate: "Fix approval flow tests"
TaskCreate: "Fix batch completion tests"
TaskCreate: "Fix abort handler tests"
```

**Option B: TodoWrite (Fallback)**
If Tasks aren't available, use TodoWrite to track each workstream.

### Step 6: Dispatch in Parallel

Execute all tasks simultaneously:

```bash
# Terminal 1
claude -p "Fix approval flow tests. Only modify files in src/approval/..."

# Terminal 2
claude -p "Fix batch completion tests. Only modify files in src/batch/..."

# Terminal 3
claude -p "Fix abort handler tests. Only modify files in src/abort/..."
```

### Step 7: Review and Integrate

When agents return:
1. Read each summary
2. Check for conflicts (same files edited?)
3. Run full test suite
4. Integrate changes
5. Mark Tasks as completed (if using Tasks)

## Effective Agent Prompts

### Prompt Template

```markdown
You are fixing [specific domain] issues.

**Context:**
[Relevant background information]

**Files in scope:**
- src/domain/file1.ts
- src/domain/file2.ts
- tests/domain/*.test.ts

**Goal:**
Fix failing tests in [test file]

**Constraints:**
- Do NOT modify files outside scope
- Do NOT change [specific things]
- Maintain [specific invariants]

**Success criteria:**
- All tests in [file] pass
- No new test failures introduced
- Changes documented in summary

Provide a summary of changes when complete.
```

## Red Flags

**Never:**
- Dispatch agents for related failures
- Let agents edit the same files
- Skip the integration verification
- Trust agent success without checking

## Verification

### Pre-Dispatch Checklist

- [ ] Domains are truly independent
- [ ] No shared file modifications
- [ ] Each task has clear scope
- [ ] Constraints prevent interference
- [ ] Success criteria are measurable

### Post-Dispatch Checklist

- [ ] All agent tasks completed
- [ ] No conflicting file changes
- [ ] Comprehensive tests pass
- [ ] Integration tests pass
- [ ] No new issues introduced

## Best Practices

### Do

1. Clearly define domain boundaries
2. Include all necessary context in prompts
3. Set explicit constraints
4. Request summaries from each agent
5. Run integration tests after merging
6. Document coordination strategy

### Don't

1. Dispatch agents for interconnected issues
2. Allow overlapping file modifications
3. Skip the integration verification
4. Assume agents won't conflict
5. Use vague success criteria
6. Dispatch more agents than needed

## Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Parallel efficiency | >70% | Time saved vs. sequential |
| Conflict rate | <10% | Agent changes conflicting |
| First-run success | >80% | Tasks complete without re-run |
| Integration pass rate | >90% | Combined changes work |

## Related Skills

- [subagent-driven](../../development/subagent-driven/SKILL.md) - Sequential task execution
- [multi-agent-patterns](../multi-agent-patterns/SKILL.md) - Agent architectures
- [writing-plans](../../development/planning/writing-plans/SKILL.md) - Task planning