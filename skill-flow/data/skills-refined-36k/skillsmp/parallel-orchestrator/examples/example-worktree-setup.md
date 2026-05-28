# Example: Worktree Setup for Parallel Tasks

## Scenario
5 independent UI components need to be created in parallel.

## Worktree Creation Output

```bash
# Create worktrees for each task
./scripts/setup-worktree.sh task-1
./scripts/setup-worktree.sh task-2
./scripts/setup-worktree.sh task-3
./scripts/setup-worktree.sh task-4
./scripts/setup-worktree.sh task-5
```

## Expected Result

```
┌─────────────────────────────────────────────────────────────┐
│ Worktree Setup Complete                                     │
│                                                             │
│ Created 5 worktrees:                                        │
│   /tmp/auto-worktrees/task-1  →  branch: auto/task-1        │
│   /tmp/auto-worktrees/task-2  →  branch: auto/task-2        │
│   /tmp/auto-worktrees/task-3  →  branch: auto/task-3        │
│   /tmp/auto-worktrees/task-4  →  branch: auto/task-4        │
│   /tmp/auto-worktrees/task-5  →  branch: auto/task-5        │
│                                                             │
│ Each worktree contains:                                     │
│   ✓ Full project copy                                       │
│   ✓ .claude/project-profile.yaml                            │
│   ✓ node_modules (symlinked)                                │
└─────────────────────────────────────────────────────────────┘
```

## Agent Dispatch

```javascript
// Dispatch 5 agents in parallel
for (const task of parallelGroup) {
  Task({
    subagent_type: "autonomous-dev:task-executor",
    prompt: `
      Work in worktree at /tmp/auto-worktrees/${task.id}/

      Task: ${task.description}
      Files: ${task.files.join(', ')}

      Verification: npm test -- --testPathPattern='${task.testPattern}'

      When verification passes:
      <promise>READY_FOR_QA: ${task.id}</promise>
    `,
    run_in_background: true
  })
}
```

## Progress Tracking

```yaml
# .claude/auto-progress.yaml
session_id: "auto-20250118-100000"
parallel_group: 1
tasks:
  task-1:
    name: "Create Sidebar component"
    status: in_progress
    branch: auto/task-1
    worktree: /tmp/auto-worktrees/task-1
    iterations: 0
  task-2:
    name: "Create Header component"
    status: in_progress
    branch: auto/task-2
    worktree: /tmp/auto-worktrees/task-2
    iterations: 0
  # ... etc
```
