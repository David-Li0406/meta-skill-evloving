---
name: task-selection
description: Priority algorithm for selecting next PRD task based on category, dependencies, and risk
category: coordination
depends-on: []
---

# Task Selection Skill

> "Fail fast on risky work – tackle hard problems before easy wins."

## When to Use This Skill

Use when:

- Assigning a new task from the PRD
- Current task is null or status is "passed"
- After retrospective completes

## Quick Start

```javascript
// 1. Filter incomplete items
const incomplete = prd.items.filter((item) => !item.passes);

// 2. Filter unblocked items (dependencies met)
const unblocked = incomplete.filter((item) =>
  item.dependencies.every((depId) => prd.items.find((i) => i.id === depId)?.passes === true)
);

// 3. Sort by priority and select first
const next = unblocked.sort(priorityComparator)[0];
```

## Decision Framework

| Category            | Priority    | When to Use                           |
| ------------------- | ----------- | ------------------------------------- |
| `architectural`     | 1 (Highest) | Affects entire codebase structure     |
| `integration`       | 2           | Reveals incompatibilities early       |
| `spike` / `unknown` | 3           | Exploratory work, reduces uncertainty |
| `functional`        | 4           | Standard feature implementation       |
| `polish`            | 5 (Lowest)  | UI, optimization, documentation       |

## Progressive Guide

### Level 1: Basic Selection

Select first incomplete, unblocked task:

```javascript
const next = prd.items.find(
  (item) =>
    !item.passes && item.dependencies.every((d) => prd.items.find((i) => i.id === d)?.passes)
);
```

### Level 2: Priority-Weighted Selection

Apply category priority ordering:

```javascript
const priorityOrder = {
  architectural: 1,
  integration: 2,
  unknown: 3,
  spike: 3,
  functional: 4,
  polish: 5,
};

const priorityValue = { high: 1, medium: 2, low: 3 };

unblocked.sort((a, b) => {
  const catDiff = priorityOrder[a.category] - priorityOrder[b.category];
  if (catDiff !== 0) return catDiff;
  return priorityValue[a.priority] - priorityValue[b.priority];
});
```

### Level 3: Risk-Adjusted Selection

Consider retry count and complexity:

```javascript
// Deprioritize repeatedly failing tasks
if (task.retryCount >= 3) {
  // Consider skipping or escalating
  logWarning(`Task ${task.id} failed ${task.retryCount} times`);
}

// Boost tasks that unblock many others
const unblockScore = prd.items.filter((i) => i.dependencies.includes(task.id)).length;
```

## Anti-Patterns

❌ **DON'T:**

- Select tasks with unmet dependencies
- Assign new task while current task is `ready_for_qa`
- Skip retrospective to assign faster
- Assign multiple tasks simultaneously

✅ **DO:**

- Verify all dependencies have `passes: true`
- Wait for QA validation before assigning next
- Complete retrospective before clearing `currentTask`
- Log selection rationale in progress file

## Checklist

Before assigning a task:

- [ ] **Current task is `null`** (MUST be null, not "passed")
- [ ] **NOT in "in_retrospective" status** (forbidden to assign during retrospective)
- [ ] **NOT in "skill_research" status** (forbidden to assign during skill research)
- [ ] **Retrospective complete** (if previous task existed, retrospective AND skill_research must be complete)
- [ ] Task has all required fields (id, title, description, acceptanceCriteria)
- [ ] All dependencies have `passes: true`
- [ ] Worker heartbeats are fresh (< 60 seconds)
- [ ] Selection rationale logged to coordinator-progress.txt

**⚠️ CRITICAL:** When `currentTask.status === "passed"`, you MUST run retrospective first, then skill_research, and ONLY THEN set `currentTask = null` before selecting the next task. Never assign a new task while `currentTask` is not null.

## Reference

- [agents/pm/AGENT.md](../../AGENT.md) — Full PM instructions
- [agents/pm/skills/scale-adaptive.md](scale-adaptive.md) — Scale-adaptive planning
