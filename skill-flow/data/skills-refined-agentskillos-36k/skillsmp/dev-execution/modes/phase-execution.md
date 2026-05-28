# Phase Execution Mode

Detailed guidance for multi-phase YAML-driven development with batch delegation.

## When to Use

- Multi-phase implementation plans (>1 day of work)
- Features requiring PRD and progress tracking
- Cross-cutting concerns affecting multiple layers
- Work tracked in `.claude/progress/{PRD_NAME}/phase-N-progress.md`

## Phase 1: Initialize Context & Tracking

### 1.1 Extract Phase Information

From `$ARGUMENTS`, extract:
- `{PRD_NAME}`: From plan or PRD filename
- `{PHASE_NUM}`: Phase number to execute

### 1.2 Validate Tracking Infrastructure

```bash
progress_file=".claude/progress/${PRD_NAME}/phase-${PHASE_NUM}-progress.md"

# Check if progress file exists
if [ ! -f "$progress_file" ]; then
  Task("artifact-tracker", "Create Phase ${PHASE_NUM} progress for ${PRD_NAME}")
fi
```

## Phase 2: Execute Using Orchestration

### 2.1 Read Progress YAML Only (Token-Efficient)

**Critical**: Do NOT read entire progress file. Extract only YAML frontmatter:

```bash
# Extract YAML frontmatter (~2KB vs ~25KB for full file)
head -100 ${progress_file} | sed -n '/^---$/,/^---$/p'
```

From YAML, identify:
- Current `tasks` array with `assigned_to`, `dependencies`, `status`
- `parallelization` section with batch groupings
- Tasks ready to execute (dependencies have `status: completed`)

### 2.2 Delegate in Batches

**Use pre-computed Task() commands from "Orchestration Quick Reference" section when available.**

#### Batch Execution Strategy

1. **Batch 1** (No dependencies):
   - Execute ALL tasks in `parallelization.batch_1` in **parallel**
   - Use single message with multiple Task() tool calls:
   ```
   Task("ui-engineer-enhanced", "TASK-1.1: Implement X component...")
   Task("backend-typescript-architect", "TASK-1.2: Add API endpoint...")
   ```

2. **Wait** for Batch 1 to complete

3. **Batch 2+**: Continue batch-by-batch, tasks within batches in parallel

4. **Update Task Status** after each task completes:
   ```
   Task("artifact-tracker", "Update ${PRD_NAME} phase ${PHASE_NUM}: Mark TASK-1.1 completed")
   ```

### 2.3 Task Delegation Template

```
@{agent-from-assigned_to}

Phase ${PHASE_NUM}, {task_id}: {task_title}

{task_description}

Project Patterns to Follow:
- Layered architecture: routers → services → repositories → DB
- ErrorResponse envelopes for errors
- Cursor pagination for lists
- Telemetry spans and structured JSON logs
- DTOs separate from ORM models

Success criteria:
- [What defines completion]
```

**If subagent invocation fails**: Document in progress tracker and proceed with direct implementation.

### 2.4 Validate Task Completion

After each major task:

```
@task-completion-validator

Phase ${PHASE_NUM}, Task: {task_id}

Expected outcomes:
- [Outcome 1 from task description]
- [Outcome 2 from task description]

Files changed:
- {list files}

Validate:
1. Acceptance criteria met
2. Project architecture patterns followed
3. Tests exist and pass
4. No regression introduced
```

### 2.5 Commit After Each Task

```bash
git add {files}
git commit -m "feat(scope): implement {feature}

- Added {component/service/etc}
- Wired telemetry spans
- Added tests with {coverage}%

Refs: Phase ${PHASE_NUM}, {task_id}"
```

## Phase 3: Continuous Testing

Run after each significant change:

### Backend Tests

```bash
uv run --project services/api pytest app/tests/test_X.py -v
uv run --project services/api mypy app
uv run --project services/api ruff check
```

### Frontend Tests

```bash
pnpm --filter "./apps/web" test -- --testPathPattern="ComponentName"
pnpm --filter "./apps/web" typecheck
pnpm --filter "./apps/web" lint
```

**Test failure protocol:**
1. Fix immediately if related to current work
2. Document in progress tracker if unrelated
3. DO NOT proceed to next task if tests fail for current work

## Phase 4: Milestone Validation

At each major milestone (after completing a batch):

### 4.1 Run Full Validation

```bash
# Type checking
pnpm -r typecheck
uv run --project services/api mypy app

# Linting
pnpm -r lint
uv run --project services/api ruff check

# Tests
pnpm -r test
uv run --project services/api pytest

# Build check
pnpm --filter "./apps/web" build
```

### 4.2 Milestone Validation with Subagent

```
@task-completion-validator

Phase ${PHASE_NUM} Milestone: Batch {batch_num} Complete

Completed tasks:
- {task_id_1}
- {task_id_2}

Validate:
1. All batch tasks complete
2. Success criteria met
3. No regressions
4. Tests comprehensive
```

## Phase 5: Final Validation

When ALL tasks complete:

### 5.1 Quality Gates

All must pass:
- [ ] All tests passing (backend + frontend + e2e)
- [ ] Type checking clean
- [ ] Linting clean
- [ ] Build succeeds
- [ ] A11y tests pass (if UI phase)

### 5.2 Final Progress Update

```
Task("artifact-tracker", "Finalize ${PRD_NAME} phase ${PHASE_NUM}:
- Mark phase as completed
- Update completion to 100%
- Generate phase completion summary")
```

### 5.3 Push All Changes

```bash
git push origin ${branch_name}
```

## Error Recovery

### Common Recovery Strategies

**Git conflicts:**
```bash
git stash
git pull --rebase origin ${branch_name}
git stash pop
# Resolve conflicts
git add .
git rebase --continue
```

**Build failures:**
```bash
rm -rf .next node_modules/.cache
pnpm install
pnpm build
```

**Subagent failures:**
- Retry once
- If fails again, document and proceed with direct implementation

### If Unrecoverable

Update progress file:
```yaml
---
status: blocked
---

**Blocker Details:**
- Task: {task_id}
- Issue: {description}
- Attempted Solutions: {list}
- Needs: {what's needed to unblock}
```

Stop and report to user with:
- Clear description of blocker
- What was attempted
- What's needed to proceed
- Current state of work (all committed)
