# Request Log Workflow Integration

How dev-execution integrates with meatycapture-capture for request-log operations.

## When to Use Request-Log Tracking

Always use request-log tracking when:

- Work originates from a `REQ-*` item
- Implementing logged enhancement/bug/idea
- Want searchable history of work
- Need to update stakeholders on progress

## Quick Commands (Token-Efficient)

Use `/mc` command for simple operations:

| Action | Command |
|--------|---------|
| List logs | `meatycapture log list PROJECT` |
| View item | `meatycapture log view PATH` |
| Search | `meatycapture log search "query" PROJECT` |
| Mark in-progress | `meatycapture log item update DOC ITEM --status in-progress` |
| Mark complete | `meatycapture log item update DOC ITEM --status done` |
| Add note | `meatycapture log note add DOC ITEM -c "text"` |

For batch operations or complex workflows, use **meatycapture-capture** skill.

## Workflow

### Starting Work

1. **Search for existing item**:
   ```bash
   meatycapture log search "feature name" meatycapture
   ```

2. **If found, mark in-progress**:
   ```bash
   meatycapture log item update REQ-*.md REQ-ITEM --status in-progress
   ```

3. **Add context note**:
   ```bash
   meatycapture log note add REQ-*.md REQ-ITEM -c "Starting work in Phase N, TASK-X.Y"
   ```

4. **If not found, capture new**:
   ```bash
   /mc capture {"title": "...", "type": "enhancement", "domain": "..."}
   ```

### During Work

Add progress notes at significant milestones:

```bash
meatycapture log note add REQ-*.md REQ-ITEM -c "Backend complete, starting frontend"
```

Track blocking issues:

```bash
meatycapture log note add REQ-*.md REQ-ITEM -c "Blocked: waiting on API dependency"
```

### Completing Work

1. **Mark complete**:
   ```bash
   meatycapture log item update REQ-*.md REQ-ITEM --status done
   ```

2. **Add completion note with context**:
   ```bash
   meatycapture log note add REQ-*.md REQ-ITEM -c "Completed in PR #123. Commits: abc123, def456"
   ```

## Integration with Execution Modes

### Phase Execution

When tasks reference request-log items:

```bash
# At task start
meatycapture log item update DOC ITEM --status in-progress
meatycapture log note add DOC ITEM -c "Starting Phase ${phase_num}, ${task_id}"

# During execution
meatycapture log note add DOC ITEM -c "API endpoint complete"

# At task complete
meatycapture log item update DOC ITEM --status done
meatycapture log note add DOC ITEM -c "Completed in Phase ${phase_num}"
```

### Quick Feature

```bash
# If input was REQ-ID, at start
meatycapture log item update DOC ITEM --status in-progress

# At completion
meatycapture log item update DOC ITEM --status done
meatycapture log note add DOC ITEM -c "Completed in quick-feature/{slug}"
```

### Story Execution

```bash
# When story maps to REQ item
meatycapture log item update DOC ${story_id} --status in-progress

# At completion
meatycapture log item update DOC ${story_id} --status done
meatycapture log note add DOC ${story_id} -c "Story completed. PR: #123"
```

## Capturing New Issues

When issues arise during execution:

```bash
# Bug discovered during work
/mc capture {"title": "...", "type": "bug", "domain": "...", "notes": "Found during..."}

# Enhancement idea
/mc capture {"title": "...", "type": "enhancement", "notes": "Could improve..."}

# Blocked issue
/mc capture {"title": "...", "type": "bug", "status": "blocked", "notes": "Needs..."}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `triage` | New, needs review |
| `in-progress` | Work started |
| `done` | Work completed |
| `blocked` | Cannot proceed |
| `wont-do` | Decided not to implement |

## Best Practices

### Search Before Creating

Always search existing logs before creating duplicates:

```bash
meatycapture log search "keyword" meatycapture
```

### Keep Notes Concise

Notes should be brief but informative:
- What was done
- Any blockers encountered
- References (commits, PRs)

### Update Status Promptly

- Mark `in-progress` when starting
- Mark `done` immediately when complete
- Don't forget to update if blocked

## Reference

Full meatycapture-capture skill: `.claude/skills/meatycapture-capture/SKILL.md`
