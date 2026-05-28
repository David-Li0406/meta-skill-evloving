# Create Plan Summary Workflow

## Purpose

Generate a SUMMARY.md file after a plan completes execution, documenting tasks completed, files modified, deviations, and outcomes.

## Inputs

```typescript
interface CreateSummaryInput {
  plan_path: string;           // Path to executed PLAN.md
  plan_number: string;         // e.g., "02"
  task_group: string;          // e.g., "API Endpoints"
  executed_by_agent: string;   // e.g., "backend-specialist" - which agent ran this plan
  state_path: string;          // Path to .long-run/ directory
  execution_result: {
    status: 'completed' | 'failed' | 'partial';
    tasks: TaskResult[];
    start_time: string;        // ISO timestamp
    end_time: string;          // ISO timestamp
    deviations: Deviation[];
    decisions: Decision[];
  };
}

interface TaskResult {
  task_number: number;
  name: string;
  status: 'completed' | 'failed' | 'skipped';
  commit_hash?: string;
  files_modified: FileChange[];
  verification_passed: boolean;
}

interface FileChange {
  path: string;
  action: 'created' | 'modified' | 'deleted';
  lines_added: number;
  lines_removed: number;
}

interface Deviation {
  rule: 1 | 2 | 3 | 4 | 5;
  description: string;
  action_taken: string;
}

interface Decision {
  topic: string;
  choice: string;
  rationale: string;
}
```

## Output

Creates: `.long-run/summaries/{plan_number}-SUMMARY.md`

## Workflow Steps

### Step 1: Calculate Metrics

```typescript
function calculateMetrics(execution_result: ExecutionResult) {
  const tasks_completed = execution_result.tasks.filter(t => t.status === 'completed').length;
  const tasks_total = execution_result.tasks.length;

  const start = new Date(execution_result.start_time);
  const end = new Date(execution_result.end_time);
  const duration_minutes = Math.round((end - start) / 60000);

  const files_modified = execution_result.tasks
    .flatMap(t => t.files_modified)
    .reduce((acc, f) => {
      const existing = acc.find(x => x.path === f.path);
      if (existing) {
        existing.lines_added += f.lines_added;
        existing.lines_removed += f.lines_removed;
      } else {
        acc.push({...f});
      }
      return acc;
    }, []);

  const commits = execution_result.tasks
    .filter(t => t.commit_hash)
    .map(t => t.commit_hash);

  return { tasks_completed, tasks_total, duration_minutes, files_modified, commits };
}
```

### Step 2: Generate Frontmatter

```yaml
---
version: "1.0"
plan: {plan_number}
task_group: {task_group}
executed_by_agent: {executed_by_agent}
status: {completed|failed|partial}
completed_at: {ISO timestamp}
duration_minutes: {number}
---
```

### Step 3: Build Tasks Completed Section

```markdown
## Tasks Completed

- [x] Task 1: {name} - commit {hash}
- [x] Task 2: {name} - commit {hash}
- [ ] Task 3: {name} - {reason if failed/skipped}
```

**Rules:**
- `[x]` for completed tasks with commit hash
- `[ ]` for failed/skipped tasks with explanation
- Include task name exactly as in PLAN.md

### Step 4: Build Files Modified Table

```markdown
## Files Modified

| File | Action | Lines Changed |
|------|--------|---------------|
| src/api/users/route.ts | Created | +120 |
| src/middleware/auth.ts | Modified | +15, -3 |
| src/utils/old-helper.ts | Deleted | -45 |
```

**Formatting:**
- Action: Created, Modified, or Deleted
- Lines Changed: `+N` for additions, `-N` for removals, `+N, -M` for both

### Step 5: Build Verification Results Section

```markdown
## Verification Results

- [x] `npm test -- api/users.test.ts` - PASSED (6/6 tests)
- [x] `npm run build` - PASSED
- [ ] Manual verification - PENDING (end of run)
```

**Rules:**
- Extract verify commands from PLAN.md tasks
- Mark as PASSED/FAILED with details
- Manual verification always PENDING

### Step 6: Build Deviations Section

```markdown
## Deviations from Plan

### Auto-Fixed (Rules 1-3)
- [Rule 1] Fixed null pointer exception in auth check
- [Rule 2] Added missing input validation for POST body
- [Rule 3] Installed missing dependency: zod@3.22.0

### Logged (Rule 5)
- ISS-001: Could optimize database query with index (deferred)
- ISS-002: Consider adding rate limiting (deferred)
```

**Rules:**
- Group by auto-fixed (1-3) vs logged (5)
- Rule 4 deviations don't appear here (they stop execution)
- Reference ISS-XXX IDs for logged issues

### Step 7: Build Decisions Made Table

```markdown
## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth method | JWT | Matches existing auth middleware |
| Validation lib | Zod | Already in use elsewhere |
| None | - | - |
```

**Rules:**
- Only include decisions made during execution
- Use "None" row if no decisions were made

### Step 8: Build Issues Encountered Section

```markdown
## Issues Encountered

1. **Test flakiness (Task 2):** Intermittent timeout in async test
   - Resolution: Increased timeout from 5s to 10s
   - Commit: abc1234

2. **Build error (Task 3):** Missing type definition
   - Resolution: Added @types/node to devDependencies
   - Commit: def5678

**OR if none:**

## Issues Encountered

None.
```

### Step 9: Build Next Steps Section

```markdown
## Next Steps

- Plan 03 ready for execution
- No blockers identified
- Manual verification recommended for auth flows

**OR if failed/partial:**

## Next Steps

- Resolve Task 3 failure before continuing
- See ISSUES.md for deferred items
- Re-run with: `/long-run-implement --resume`
```

### Step 10: Write Summary File

```typescript
function writeSummary(state_path: string, plan_number: string, content: string) {
  const summary_path = `${state_path}/summaries/${plan_number}-SUMMARY.md`;

  // Ensure directory exists
  mkdir_p(`${state_path}/summaries`);

  // Write atomically
  write_atomic(summary_path, content);

  return summary_path;
}
```

## Complete Template

```markdown
---
version: "1.0"
plan: {NN}
task_group: {group-name}
executed_by_agent: {agent-type}
status: {completed|failed|partial}
completed_at: {YYYY-MM-DDTHH:MM:SSZ}
duration_minutes: {N}
---

# Plan {NN}: {Task Group Name} Summary

**Status:** {Completed / Failed / Partial}
**Executed by:** {agent-type}

## Tasks Completed

{task list with checkboxes and commit hashes}

## Files Modified

| File | Action | Lines Changed |
|------|--------|---------------|
{file rows}

## Verification Results

{verification checkboxes}

## Deviations from Plan

### Auto-Fixed (Rules 1-3)
{deviations or "None."}

### Logged (Rule 5)
{logged issues or "None."}

## Decisions Made

| Decision | Choice | Rationale |
|----------|--------|-----------|
{decisions or "None | - | -"}

## Issues Encountered

{issues or "None."}

## Next Steps

{next steps based on status}
```

## Error Handling

| Error | Action |
|-------|--------|
| Missing execution_result | Generate minimal summary with status: "unknown" |
| Invalid timestamps | Use current time, note in Issues section |
| Write failure | Retry with atomic write, fail loudly if persists |
| Missing PLAN.md | Generate summary from execution_result only |
