---
# === PROGRESS TRACKING TEMPLATE ===
# Phase-level task tracking optimized for AI agent orchestration
# REQUIRED FIELDS: assigned_to, dependencies for EVERY task
# Copy this template and replace all [PLACEHOLDER] values

# Metadata: Identification and Classification
type: progress
prd: "[PRD_ID]"                          # e.g., "advanced-editing-v2", "artifact-flow-modal-redesign"
phase: [PHASE_NUMBER]                    # e.g., 1, 2, 3 (integer, not string)
title: "[PHASE_TITLE]"                   # e.g., "3-Panel Sync Status Redesign"
status: "planning"                       # planning|in-progress|review|complete|blocked
started: "[YYYY-MM-DD]"                  # Start date of this phase
completed: null                          # "YYYY-MM-DD" when complete, null if in progress

# Overall Progress: Status and Estimates
overall_progress: [0-100]                # 0-100, e.g., 35 for 35% complete
completion_estimate: "on-track"          # on-track|at-risk|blocked|ahead

# Task Counts: Machine-readable task state
total_tasks: [COUNT]                     # Total tasks in this phase, e.g., 10
completed_tasks: [COUNT]                 # Completed count, e.g., 2
in_progress_tasks: [COUNT]               # Currently in progress, e.g., 1
blocked_tasks: [COUNT]                   # Blocked by dependencies, e.g., 0
at_risk_tasks: [COUNT]                   # At risk of missing deadline, e.g., 1

# Ownership: Primary and secondary agents
owners: ["[AGENT_NAME]"]                 # Primary agent(s), e.g., ["ui-engineer-enhanced"]
contributors: ["[AGENT_NAME]"]           # Secondary agents, e.g., ["code-reviewer"]

# === TASKS (SOURCE OF TRUTH) ===
# Machine-readable task definitions with assignments and dependencies
# Update using: python scripts/update-status.py -f FILE -t TASK-X -s [pending|in_progress|complete|blocked|at-risk]
tasks:
  # Example task structure (REQUIRED for every task):
  - id: "TASK-1.1"
    description: "Brief task description"
    status: "pending"                    # pending|in_progress|complete|blocked|at-risk
    assigned_to: ["ui-engineer-enhanced"]
    dependencies: []                     # Empty if no dependencies, or ["TASK-1.0", "TASK-0.9"]
    estimated_effort: "2h"               # Optional: time estimate
    priority: "high"                     # Optional: low|medium|high|critical

  # Parallel tasks (no dependencies):
  - id: "TASK-1.2"
    description: "Another task that can run in parallel"
    status: "pending"
    assigned_to: ["ui-engineer-enhanced"]
    dependencies: []
    estimated_effort: "1.5h"
    priority: "medium"

  # Sequential task (depends on others):
  - id: "TASK-2.1"
    description: "Task that depends on TASK-1.1 and TASK-1.2"
    status: "pending"
    assigned_to: ["ui-engineer-enhanced"]
    dependencies: ["TASK-1.1", "TASK-1.2"]  # MUST wait for these to complete
    estimated_effort: "3h"
    priority: "high"

# Parallelization Strategy (computed from dependencies)
parallelization:
  batch_1: ["TASK-1.1", "TASK-1.2"]      # Can run simultaneously
  batch_2: ["TASK-2.1"]                  # Sequential, waits for batch_1
  critical_path: ["TASK-1.1", "TASK-2.1"] # Longest dependency chain
  estimated_total_time: "5h"             # If run optimally (parallel batches)

# Critical Blockers: For immediate visibility
blockers: []                             # Array of blocker objects
# Example blocker:
# - id: "BLOCKER-001"
#   title: "Missing API endpoint"
#   severity: "critical"                # critical|high|medium
#   blocking: ["TASK-2.1", "TASK-2.2"]
#   resolution: "Awaiting backend-engineer implementation"
#   created: "YYYY-MM-DD"

# Success Criteria: Acceptance conditions for phase completion
success_criteria: [
  # Example:
  # { id: "SC-1", description: "All components render correctly", status: "pending" },
  # { id: "SC-2", description: "All tests pass", status: "pending" }
]

# Files Modified: What's being changed in this phase
files_modified: [
  # Example:
  # "components/entity/sync-status/artifact-flow-banner.tsx",
  # "components/entity/unified-entity-modal.tsx"
]
---

# [PRD_ID] - Phase [PHASE_NUMBER]: [PHASE_TITLE]

**YAML frontmatter is the source of truth for tasks, status, and assignments.** Do not duplicate in markdown.

Use CLI to update progress:

```bash
python scripts/update-status.py -f .claude/progress/[prd]/phase-[N]-progress.md -t TASK-X -s completed
```

---

## Objective

Brief description of phase objectives - 1-2 sentences explaining what this phase delivers.

---

## Implementation Notes

### Architectural Decisions

Key architectural decisions made during this phase, including trade-offs and rationale.

### Patterns and Best Practices

Reference patterns being used, similar implementations elsewhere, integration points.

### Known Gotchas

Things to watch out for during implementation:
- Common mistakes to avoid
- Edge cases to handle
- Browser/compatibility issues
- Accessibility considerations

### Development Setup

Any special setup, configuration, or prerequisites needed for this phase.

---

## Completion Notes

Summary of phase completion (fill in when phase is complete):

- What was built
- Key learnings
- Unexpected challenges
- Recommendations for next phase
