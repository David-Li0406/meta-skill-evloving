# Implementation Patterns

Extracted patterns for parallel execution and task planning.

## Parallel Execution

### When to Split

| Size | Lines | Strategy |
|------|-------|----------|
| SMALL | <3,000 | Sequential implementation |
| MEDIUM | 3,000-8,000 | Consider parallel if >3 independent tasks |
| LARGE | >8,000 | MUST split into parallel |

### Option A: Parallel Feedback Checking (Phase 0)

When multiple feedback sources exist:

```
Spawn 2 parallel Explore agents:

Agent 1: "Read grimoires/loa/a2a/sprint-N/auditor-sprint-feedback.md:
1. Does file exist?
2. If yes, verdict (CHANGES_REQUIRED or APPROVED)?
3. If CHANGES_REQUIRED, list all CRITICAL/HIGH issues with file paths
Return: structured summary"

Agent 2: "Read grimoires/loa/a2a/sprint-N/engineer-feedback.md:
1. Does file exist?
2. If yes, verdict (All good or changes requested)?
3. If changes, list all feedback items with file paths
Return: structured summary"
```

### Option B: Parallel Task Implementation (Phase 2)

When sprint has multiple independent tasks:

```
1. Read sprint.md and identify all tasks
2. Analyze task dependencies
3. Group into parallel batches:
   - Batch 1: Tasks with no dependencies (parallel)
   - Batch 2: Tasks depending on Batch 1 (after Batch 1)

For independent tasks, spawn parallel agents:
Agent 1: "Implement Task 1.2 - read acceptance criteria, review patterns, implement, write tests, return summary"
Agent 2: "Implement Task 1.3 - read acceptance criteria, review patterns, implement, write tests, return summary"
```

### Consolidation

1. Collect results from all parallel agents
2. Verify no conflicts between implementations
3. Run integration tests across all changes
4. Generate unified report

---

## Task Planning (v0.19.0)

### What is a Complex Task?

A task is complex if ANY of these apply:
- Touches 3+ files/modules
- Involves architectural decisions
- Implementation path is unclear
- Estimated at >2 hours
- Has multiple acceptance criteria
- Involves security-sensitive code

### Planning Requirement

For complex tasks, create a plan BEFORE writing code:

```markdown
## Task Plan: [Task Name]

### Objective
[What this task accomplishes]

### Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Files to Modify
- `path/to/file.ts` - [what changes]
- `path/to/other.ts` - [what changes]

### Dependencies
- [What must exist before this task]
- [External services needed]

### Risks
- [What could go wrong]
- [Mitigation approach]

### Verification
- [How we'll know it works]
- [Specific tests to write]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### Plan Review

Before implementing:
1. Review plan for completeness
2. Identify any blockers
3. Confirm approach aligns with SDD
4. Get human approval if high-risk

### Simple Tasks

For simple tasks (documentation updates, config changes, small fixes), planning is optional. Use judgment.

### Plan as Artifact

Task plans are stored in `grimoires/loa/a2a/sprint-N/task-{N}-plan.md` and become part of the review artifact.

---

## Beads Workflow (beads_rust)

When beads_rust (`br`) is installed, the full task lifecycle:

### Session Start
```bash
br sync --import-only  # Import latest state from JSONL
```

### Task Lifecycle
```bash
# Get ready work
.claude/scripts/beads/get-ready-work.sh 1 --ids-only

# Update task status
br update <task-id> --status in_progress

# Log discovered issues during implementation
.claude/scripts/beads/log-discovered-issue.sh "<parent-id>" "Issue description" bug 2

# Complete task
br close <task-id> --reason "Implemented per acceptance criteria"
```

### Semantic Labels for Tracking

| Label | Purpose | Example |
|-------|---------|---------|
| `discovered-during:<id>` | Traceability | Auto-added by log-discovered-issue.sh |
| `needs-review` | Review gate | `br label add <id> needs-review` |
| `review-approved` | Passed review | `br label add <id> review-approved` |
| `security` | Security concern | `br label add <id> security` |

### Session End
```bash
br sync --flush-only  # Export SQLite → JSONL before commit
```

**Protocol Reference**: See `.claude/protocols/beads-integration.md`
