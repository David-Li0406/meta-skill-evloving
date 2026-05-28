---
name: overnight-mode
description: Internal skill for overnight autonomous execution. Provides context and rules for unattended development.
agent: general-purpose
user-invocable: false
---

# Overnight Mode Context

You are currently running in **OVERNIGHT MODE**. This skill provides essential context for unattended autonomous development.

## Current State

Read your current state from these files:

### Primary State: `.claude/auto-overnight.local.md`
```yaml
active: true/false     # Is overnight mode active?
iteration: N           # Current loop iteration
max_iterations: N      # Stop after this many
max_hours: N           # Maximum runtime
started_at: ISO8601    # When overnight started
deadline_at: ISO8601   # Hard stop time
current_phase: PHASE   # INIT/PLAN/EXECUTE/VERIFY/COMPLETE
tasks_completed: N     # How many tasks done
tasks_total: N         # Total tasks in plan
last_checkpoint: ISO   # Last checkpoint time
```

### Progress: `.claude/auto-progress.yaml`
```yaml
tasks:
  task-1:
    status: done/in_progress/pending/failed
    branch: auto/task-1
    iterations: N
```

### Memory: `.claude/auto-memory/`
- `context-summary.md` - Full context for resume
- `overnight-checkpoint.md` - Latest overnight checkpoint
- `next-actions.md` - What to do next

## Overnight Rules

### 1. NO USER INTERACTION
- DO NOT use `AskUserQuestion` tool
- DO NOT wait for approval
- Make autonomous decisions
- Document decisions in `.claude/overnight-decisions.md`

### 2. STRICT TDD (Still Required!)
Even overnight, you MUST follow TDD:
```
RED    → Write ONE failing test FIRST
GREEN  → Implement MINIMAL code to pass
REFACTOR → Clean up while tests pass
MUTATE → Verify test quality (if tools available)
```

### 3. CHECKPOINT FREQUENTLY
After every significant action:
```bash
# Update checkpoint timestamp
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
sed -i '' "s/last_checkpoint: .*/last_checkpoint: \"$TIMESTAMP\"/" .claude/auto-overnight.local.md
```

### 4. EVIDENCE-BASED VERIFICATION
Never claim "tests pass" without running them:
```bash
# WRONG
echo "Tests should pass"

# RIGHT
npm test 2>&1 | tee .claude/overnight-test-output.log
echo "Test output saved to .claude/overnight-test-output.log"
```

### 5. AUTO-RESTART ON CONTEXT LIMIT
If context is filling up:
1. Write checkpoint to `.claude/auto-memory/overnight-checkpoint.md`
2. Include: current task, next steps, important context
3. Stop hook will restart with `/auto-continue`

## Error Handling

### When Tests Fail
1. **Max 3 fix attempts** per issue
2. **Use systematic-debugging** (4-phase protocol)
3. **If still failing:** Document in `.claude/overnight-issues.md` and continue

### When Unknown Error Occurs
1. **Document everything** in `.claude/overnight-issues.md`
2. **Try to continue** with remaining tasks
3. **Flag for human review** in overnight report

## Completion Criteria

The stop hook will use prompt-based LLM evaluation to check:

1. **All plan tasks completed?**
   - Read `.claude/auto-progress.yaml`
   - Every task status should be `done`

2. **All verification passing?**
   - Tests pass (actual output required)
   - Lint clean (actual output required)
   - Build succeeds (if applicable)

3. **No critical issues?**
   - `.claude/overnight-issues.md` has no unresolved CRITICAL items

Only when ALL three are true, overnight mode completes.

## Report Generation

When complete, generate `.claude/overnight-report-{timestamp}.md`:

```markdown
# Overnight Development Report

## Execution Summary
- **Started:** {started_at}
- **Completed:** {timestamp}
- **Duration:** {duration}
- **Iterations:** {iteration}
- **Tasks:** {completed}/{total}

## Changes Made
| File | Action | Lines |
|------|--------|-------|
| src/foo.ts | Created | +150 |
| src/bar.ts | Modified | +30/-10 |

## Verification Results
### Tests
\`\`\`
{actual npm test output}
\`\`\`

### Lint
\`\`\`
{actual npm run lint output}
\`\`\`

### Build
\`\`\`
{actual npm run build output}
\`\`\`

## Issues Encountered
{contents of overnight-issues.md or "None"}

## Git History
\`\`\`
{git log --oneline for overnight commits}
\`\`\`

## Recommendations
{any follow-up work or concerns}
```

## Safety Reminders

1. **All changes are in git** - can be reverted
2. **Never modify outside project dir**
3. **Never push without explicit flag**
4. **When in doubt, checkpoint and document**

## Handoff to Human

If overnight mode ends with issues:
1. Report is at `.claude/overnight-report-*.md`
2. Issues are at `.claude/overnight-issues.md`
3. Human can review and decide next steps
4. Use `/auto-continue` to resume if needed
