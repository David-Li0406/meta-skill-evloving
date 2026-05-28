---
name: initializer-protocol
description: >
  This skill defines the Initializer Agent protocol for the Two-Agent Pattern.
  The Initializer Agent runs ONCE at the start of a new task to analyze, plan,
  and set up state for Coding Agents. Use this when starting a new autonomous
  development task that requires session boundaries.
---

# Initializer Protocol

The Initializer Agent is responsible for analysis and planning. It runs once
and hands off to Coding Agents for execution.

## Anthropic Best Practice: Two-Agent Pattern

Separating initialization from execution provides:
- Cleaner session boundaries
- Better context management
- Easier resume from checkpoints
- More efficient token usage

## Initializer Responsibilities

### Phase 1: Project Detection

```bash
# Run project detector
${CLAUDE_PLUGIN_ROOT}/scripts/detect-project.sh
```

**Output:** `.claude/project-profile.yaml`

### Phase 2: Work Type Classification

Analyze user request and classify:

```yaml
# .claude/auto-context.yaml
work_type: FRONTEND | BACKEND | FULLSTACK | RESEARCH
execution_mode: two_agent
initialized_at: "2025-01-18T10:00:00Z"
initializer_complete: false
```

### Phase 3: Task Decomposition

Use task-decomposer skill to break down into atomic tasks:

```markdown
# .claude/plans/auto-{timestamp}.md

## Execution Plan

### Tasks
- Task 1: ...
- Task 2: ...

### Parallel Groups
- Group 1: [Task 1, Task 2]
- Group 2: [Task 3, Task 4]

### Dependencies
- Task 3 depends on Task 1
- Task 4 depends on Task 2
```

### Phase 4: Feature List Creation

Generate feature list with failing status:

```yaml
# .claude/plans/features-{timestamp}.yaml
features:
  - id: task-001
    description: "..."
    status: failing
    verification_command: "..."
    expected_output: "..."
    evidence_required: true
    can_be_removed: false
```

### Phase 5: State Machine Setup

Initialize state machine:

```yaml
# .claude/auto-state-machine.yaml
session_id: "auto-20250118-100000"
current_state: EXECUTE
work_type: FRONTEND
initialized: true
initializer_complete: true
current_group: 1
total_groups: 3
checkpoint_files: []
```

### Phase 6: Write Initial Checkpoint

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/checkpoint-manager.sh write INIT \
  "Initialization complete. Plan created with X tasks in Y groups."
```

### Phase 7: Exit with Handoff

Output handoff message and exit:

```
┌─────────────────────────────────────────────────────────────┐
│ Initializer Agent Complete                                  │
│                                                             │
│   Project: Next.js application                              │
│   Work Type: FRONTEND                                       │
│   Tasks: 8 total                                            │
│   Parallel Groups: 3                                        │
│                                                             │
│   Files Created:                                            │
│     ✓ .claude/project-profile.yaml                          │
│     ✓ .claude/auto-context.yaml                             │
│     ✓ .claude/plans/auto-20250118-100000.md                 │
│     ✓ .claude/plans/features-20250118-100000.yaml           │
│     ✓ .claude/auto-state-machine.yaml                       │
│                                                             │
│   Next Steps:                                               │
│     Run /auto-continue to start execution                   │
│                                                             │
│   Coding Agent will execute parallel group 1:               │
│     - Task 1: Create UserForm component                     │
│     - Task 2: Create Header component                       │
│     - Task 3: Create Sidebar component                      │
└─────────────────────────────────────────────────────────────┘

<promise>INITIALIZER_COMPLETE</promise>
```

## Initializer DO NOT

The Initializer Agent MUST NOT:

- ❌ Write any production code
- ❌ Modify existing source files
- ❌ Run tests (no code to test)
- ❌ Create worktrees (Coding Agent does this)
- ❌ Continue beyond handoff

## Token Budget

Initializer should use minimal tokens:

| Phase | Max Tokens |
|-------|------------|
| Project Detection | ~500 |
| Work Classification | ~300 |
| Task Decomposition | ~1500 |
| State Setup | ~200 |
| Checkpoint | ~200 |
| **Total** | ~3000 |

## Handoff Validation

Before signaling INITIALIZER_COMPLETE, verify:

- [ ] `.claude/project-profile.yaml` exists
- [ ] `.claude/auto-context.yaml` exists with `execution_mode: two_agent`
- [ ] Plan file exists at `.claude/plans/auto-*.md`
- [ ] Feature list exists at `.claude/plans/features-*.yaml`
- [ ] State machine initialized with `initializer_complete: true`
- [ ] Initial checkpoint written

## Error Handling

If initialization fails:

```
<promise>INITIALIZER_FAILED</promise>

## Failure Report

### Error
[What went wrong]

### Partial State
[What was completed before failure]

### Recovery
[How to recover or retry]
```

## Integration

The Initializer Protocol integrates with:

- **auto.md** - Invoked when `execution_mode: two_agent`
- **auto-continue.md** - Reads Initializer output
- **checkpoint-manager.sh** - Writes handoff checkpoint
