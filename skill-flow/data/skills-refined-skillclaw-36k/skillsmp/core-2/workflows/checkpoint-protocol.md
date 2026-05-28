# Checkpoint Protocol (Enhanced v2.0)

## Overview

Claude Code 2.0+ creates automatic checkpoints before file modifications. This workflow provides patterns for leveraging checkpoints in PAI workflows for safe, recoverable operations.

## Quick Reference

| Command | Effect |
|---------|--------|
| `/rewind` | Interactive checkpoint selection |
| `/rewind 1` | Go back 1 checkpoint |
| `/rewind 3` | Go back 3 checkpoints |

## Checkpoint Types

### Automatic Checkpoints (CC Creates These)

CC automatically checkpoints before:
- File modifications (Write, Edit tools)
- Destructive bash operations (rm, git reset, etc.)
- Multi-file refactoring
- Git operations modifying history

### Explicit Checkpoints (You Request These)

Request checkpoints at milestones:
```
"Create a checkpoint before we begin the migration"
```

Use before:
- Experimental changes
- Database migrations
- Multi-step refactors
- Anything irreversible outside of git

## Rollback Decision Tree

```
Operation Failed?
├── File changes only → /rewind (CC handles it)
├── Git changes → git reflog + /rewind
├── Database changes → Manual restore (CC can't help)
└── External API calls → Manual rollback (CC can't help)
```

## Workflow Templates

### Template 1: Destructive File Operations

```markdown
## Before Deleting/Moving Files

1. **List targets**: `ls -la <targets>`
2. **Verify intent**: "These files will be deleted: [list]"
3. **Execute**: CC auto-checkpoints before rm/mv
4. **Verify**: Check expected state
5. **Recover if needed**: `/rewind`
```

### Template 2: Refactoring Operations

```markdown
## Multi-File Refactor

1. **Scope check**: Identify all affected files
2. **Run tests first**: Establish baseline
3. **Refactor incrementally**: CC checkpoints each edit
4. **Test after each major change**
5. **If tests fail after 2 attempts**: `/rewind` to last green state

Recovery: `/rewind` restores all files to pre-refactor state
```

### Template 3: Git Operations

```markdown
## Before Git History Changes

Operations requiring extra care:
- git rebase
- git reset --hard
- git push --force
- git clean -fd

Pattern:
1. `git stash` (backup uncommitted work)
2. `git reflog` (note current HEAD for git recovery)
3. CC auto-checkpoints file state
4. Execute git operation
5. If wrong: `git reflog` + `git reset --hard <ref>` + `/rewind`
```

### Template 4: Iteration Loop Safety

```markdown
## Iterative Fix Pattern

1. Attempt fix (CC checkpoints)
2. Test result
3. If failing after 3 iterations:
   - STOP iterating
   - `/rewind` to iteration 0
   - Try fundamentally different approach
4. If still failing: Escalate to Jean-Marc

Max iterations: 5 (prevent infinite loops)
```

### Template 5: Database Migrations

```markdown
## Database Migration (CC Cannot Rollback DB!)

1. **Backup first**: `pg_dump` or equivalent
2. Create CC checkpoint: "Checkpoint before migration"
3. Run migration
4. Verify data integrity
5. If failed:
   - `/rewind` for file changes only
   - Restore DB from backup manually
```

### Template 6: Multi-Agent Recovery

```markdown
## Parallel Agent Conflict Resolution

When parallel agents cause merge conflicts:
1. `/rewind` to before agent launch
2. Re-decompose task with explicit file ownership:
   - Agent A: files matching `src/api/**`
   - Agent B: files matching `src/ui/**`
3. Add non-overlapping constraints to prompts
4. Re-launch with boundaries
```

## Integration Patterns

### Pre-Tool-Use Hook Integration

The security hook (`pre-tool-use-security.ts`) runs before dangerous operations. When it flags something:

1. Hook logs to `memory/security-checks.jsonl`
2. CC creates checkpoint automatically
3. After approval, operation proceeds
4. If it goes wrong: `/rewind` to pre-operation state

### Stop Hook Recovery Suggestions

When the stop hook detects errors in the session, it may suggest recovery:

- Multiple failed attempts → "Consider `/rewind` to try different approach"
- Destructive operation errors → "Use `/rewind` to restore previous state"

### State Tracking

Checkpoint events are logged to `state/checkpoint-events.jsonl`:
```json
{
  "timestamp": "2026-01-12T10:30:00Z",
  "event": "pre_destructive",
  "operation": "rm -rf dist/",
  "session_id": "abc123"
}
```

## Failure Detection Patterns

### Signs You Should `/rewind`

1. **Same error 3+ times** - You're in a loop
2. **Tests that were passing now fail** - Regression introduced
3. **"Undo" attempts making things worse** - Manual fixes going sideways
4. **File corruption or unexpected deletions** - Something went wrong

### Signs You Should NOT `/rewind`

1. **Making progress** - Errors are decreasing
2. **Learning new information** - Errors teach you something
3. **External system issues** - `/rewind` won't fix API problems
4. **Database state issues** - `/rewind` only affects files

## Limitations

Checkpoints **DO restore**:
- All file changes in the working directory
- Conversation context (what you discussed)

Checkpoints **DO NOT restore**:
- Database state
- External API calls (already sent)
- Git remote state (already pushed)
- Running processes
- Environment variables

## Best Practices

1. **Trust auto-checkpoints** - CC is smart about when to save
2. **Don't over-checkpoint** - Manual checkpoints for milestones only
3. **Name checkpoints descriptively** - "Before API refactor" not "checkpoint"
4. **Test `/rewind` early** - Verify it works before relying on it
5. **Know the limits** - Checkpoints are file-based, not system-wide

## Factor 6 Compliance

This protocol supports **12-Factor Agent - Factor 6: Launch, Pause, Resume**:

- **Launch** - Session starts with clean checkpoint
- **Pause** - Checkpoint preserves exact file state
- **Resume** - `/rewind` restores any checkpoint
- **Resilience** - Long-running tasks can recover from failures

## Related Documentation

- `delegation-guide.md` - Multi-agent coordination with checkpoint recovery
- `pre-tool-use-security.ts` - Security hook that triggers checkpoints
- `stop-hook.ts` - Stop hook with error detection
