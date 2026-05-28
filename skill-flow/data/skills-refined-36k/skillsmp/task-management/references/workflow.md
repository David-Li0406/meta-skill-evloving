# Task Workflow

## Task Lifecycle

```
pending → in_progress → completed (auto-archived)
    ↓
  blocked
```

## Best Practices

### Creating Tasks
- Use clear, action-oriented titles
- Add priority and effort for planning
- Use tags for categorization
- Link to plans when applicable

```bash
task add "Implement user auth API" -p high -e L -t "backend,security"
```

### Working on Tasks
1. Use `work` to mark in_progress
2. Task context displayed automatically
3. Update notes as you progress

```bash
task work t-001
task update t-001 -n "Started JWT implementation"
```

### Completing Tasks
- Include completion notes
- Tasks auto-archive to `archive/{YYMMDD}-batch.yaml`

```bash
task complete t-001 -n "Done, tests passing"
```

### Managing Dependencies
- Use `block` to set relationships
- Blocked tasks can't start until blocker completes

```bash
task block t-002 --by t-001
```

## Integration with Plans

Link tasks to plan phases:
```bash
task update t-001 --context '{"plan":"plans/260122-feature/plan.md","phase":2}'
```

Or via code:
```javascript
updateTask('t-001', {
  context: {
    plan: 'plans/260122-feature/plan.md',
    phase: 2,
    branch: 'feature/auth'
  }
});
```

## Daily Workflow

1. **Morning**: `task list -s pending` - Review pending tasks
2. **Start**: `task work t-XXX` - Pick and start task
3. **Progress**: `task update t-XXX -n "notes"` - Track progress
4. **Complete**: `task complete t-XXX` - Mark done
5. **Review**: `task view` - Generate summary

## Filtering Examples

```bash
# High priority pending
task list -s pending -p high

# Backend tasks
task list -t backend

# Assigned to me
task list -a claude

# Export for review
task export daily-tasks.md
```
