---
name: orchestrate
description: Orchestrate large multi-workstream projects using git worktrees for parallel development. Load MasterSpec, allocate worktrees, dispatch implementers, monitor convergence, process merge queue.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Orchestrate Skill

## Purpose

Orchestrate large multi-workstream projects (orchestrator workflow) using git worktrees for true parallel development. This skill coordinates the facilitator agent to manage worktree allocation, dependency ordering, subagent execution, and auto-merge after convergence gates pass.

## When to Use

Use this skill when:

- MasterSpec has been approved (3+ workstreams)
- Multiple workstreams need to execute in parallel
- Workstreams have dependencies that require ordered execution
- Git worktrees will enable isolated, parallel development

**Trigger**: After MasterSpec approval in orchestrator workflow

## Orchestration Flow

### 1. Load MasterSpec and Spec Group

```bash
# Load approved MasterSpec spec group
cat .claude/specs/groups/<master-spec-group-id>/manifest.json
cat .claude/specs/groups/<master-spec-group-id>/spec.md

# List workstream spec groups
ls .claude/specs/groups/<master-spec-group-id>/workstreams/
```

**Extract**:

- Workstream Overview (IDs, titles, dependencies)
- Contract Registry
- Dependency Graph
- Worktree Allocation Strategy (if present)
- Atomic specs for each workstream

### 2. Invoke Facilitator for Worktree Allocation

If MasterSpec doesn't have worktree allocation strategy, dispatch facilitator to analyze and allocate:

```javascript
Task({
  description: 'Allocate worktrees for MasterSpec',
  prompt: `
Analyze the MasterSpec spec group at .claude/specs/groups/<master-spec-group-id>/ and determine worktree allocation.

**Workstreams** (each has its own spec group with atomic specs):
- ws-1: <title> (dependencies: <deps>) - spec group at workstreams/ws-1/
- ws-2: <title> (dependencies: <deps>) - spec group at workstreams/ws-2/
- ws-3: <title> (dependencies: <deps>) - spec group at workstreams/ws-3/

**Your task**:
1. Analyze dependency graph
2. Identify independent workstreams (separate worktrees)
3. Identify tightly coupled workstreams (shared worktrees)
4. Apply allocation heuristics (see facilitator agent guidelines)
5. Document allocation strategy in MasterSpec manifest.json
6. Initialize session.json with worktree_allocation
  `,
  subagent_type: 'facilitator',
});
```

### 3. Create Worktrees

For each worktree in allocation strategy:

```bash
# Get repository name
REPO_NAME=$(basename $(pwd))

# Create worktree-1
git worktree add ../${REPO_NAME}-ws-1 -b feature/ws-1-<slug>

# Create worktree-2
git worktree add ../${REPO_NAME}-ws-2 -b feature/ws-2-<slug>

# Verify creation
git worktree list
```

**Update session.json**:

```json
{
  "worktree_allocation": {
    "strategy": "ws-1 and ws-4 share worktree (tight coupling), ws-2 and ws-3 isolated",
    "worktrees": [
      {
        "id": "worktree-1",
        "path": "/Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-1",
        "branch": "feature/ws-1-backend-api",
        "workstreams": ["ws-1", "ws-4"],
        "status": "active",
        "created_at": "2026-01-02T15:35:00Z"
      }
    ]
  }
}
```

### 4. Evaluate Initial Workstream Readiness

For each workstream, determine if ready to start:

**Ready** (no dependencies):

- ws-1: No dependencies → Ready to start
- ws-3: No dependencies → Ready to start

**Blocked** (has dependencies):

- ws-2: Depends on ws-1 → Blocked
- ws-4: Depends on ws-1 → Blocked (but shares worktree with ws-1)

**Update session.json**:

```json
{
  "workstream_execution": {
    "workstreams": [
      {
        "id": "ws-1",
        "title": "Backend API",
        "worktree_id": "worktree-1",
        "dependencies": [],
        "status": "ready"
      },
      {
        "id": "ws-2",
        "title": "Frontend UI",
        "worktree_id": "worktree-2",
        "dependencies": ["ws-1"],
        "status": "blocked",
        "blocking_reason": "Waiting for ws-1 to merge (dependency)"
      }
    ]
  }
}
```

### 5. Atomize and Enforce Each Workstream (CRITICAL)

**Before dispatching implementers**, each workstream spec must be atomized and validated. This step ensures the unified vision traceability chain (REQ → atomic spec → impl → test).

For each workstream (can run in parallel for independent workstreams):

```javascript
// Step 5a: Atomize workstream spec
Task({
  description: 'Atomize ws-1 spec',
  prompt: `
Run /atomize for workstream ws-1.

**Spec Group**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/
**Input**: spec.md (WorkstreamSpec)
**Output**: atomic/as-001-*.md, atomic/as-002-*.md, etc.

Decompose the workstream spec into atomic specs following atomicity criteria:
- Each atomic spec is independently testable
- Each atomic spec is independently deployable
- Each atomic spec is independently reviewable
- Each atomic spec is independently reversible

Update manifest.json with atomic_specs.count and atomic_specs.coverage.
  `,
  subagent_type: 'atomizer',
});

// Step 5b: Enforce atomicity validation
Task({
  description: 'Enforce atomicity for ws-1',
  prompt: `
Run /enforce for workstream ws-1.

**Spec Group**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/
**Atomic Specs**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/atomic/

Validate each atomic spec against atomicity criteria:
- NOT TOO_COARSE: Single behavior, single test suite, independent rollback
- NOT TOO_GRANULAR: Can test alone, can deploy alone, is a behavior not a code fragment

Also validate:
- Every REQ-XXX is covered by at least one atomic spec
- Requirements coverage >= 100%

Update manifest.json with enforcement_status: PASSING or FAILING.
  `,
  subagent_type: 'atomicity-enforcer',
});
```

**Gate Implementation on Enforcement**:

```javascript
// Check enforcement status before proceeding
const manifest = JSON.parse(fs.readFileSync('.claude/specs/groups/<id>/workstreams/ws-1/manifest.json'));

if (manifest.enforcement_status !== 'PASSING') {
  // Do NOT dispatch implementers
  // Either iterate with /atomize --refine or escalate to user
  throw new Error(`ws-1 atomicity enforcement failed: ${manifest.enforcement_issues}`);
}

// Only proceed to implementation if enforcement passes
```

**Update session.json**:

```json
{
  "workstream_execution": {
    "workstreams": [
      {
        "id": "ws-1",
        "status": "atomized",
        "atomic_specs_count": 4,
        "enforcement_status": "PASSING",
        "ready_for_implementation": true
      }
    ]
  }
}
```

### 6. Dispatch Implementers and Test-Writers

For each **ready** workstream, dispatch implementer and test-writer in parallel:

```javascript
// ws-1 is ready
const ws1Impl = Task({
  description: 'Implement ws-1 in worktree-1',
  prompt: `
You are implementing workstream ws-1.

## EXECUTION CONTEXT

**Worktree**: worktree-1
**Path**: /Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-1
**Branch**: feature/ws-1-backend-api
**Workstream**: ws-1 (Backend API)

## CRITICAL INSTRUCTIONS

1. **Working Directory**: All operations MUST occur in the worktree path above
2. **Isolation**: Do NOT modify files in the main worktree
3. **Spec Group Location**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/
4. **Atomic Specs**: Execute atomic specs in order (as-001, as-002, etc.)

${
  ws1.sharedWorktree
    ? `
## SHARED WORKTREE NOTICE
This worktree is shared with: ws-4 (Integration Tests)
Coordinate with test-writer: you implement, they test (parallel execution)
`
    : ''
}

## YOUR TASK
Implement all atomic specs in ws-1 spec group following standard implementation process.
Fill Implementation Evidence in each atomic spec as you complete them.
  `,
  subagent_type: 'implementer',
  run_in_background: true,
});

const ws1Tests = Task({
  description: 'Write tests for ws-1 in worktree-1',
  prompt: `
You are writing tests for workstream ws-1.

## EXECUTION CONTEXT

**Worktree**: worktree-1
**Path**: /Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-1
**Branch**: feature/ws-1-backend-api
**Workstream**: ws-1 (Backend API)

## YOUR TASK
Write tests for all acceptance criteria in ws-1 atomic specs.
Fill Test Evidence in each atomic spec as you complete them.
Test names should reference atomic spec ID and AC (e.g., "should X (as-001 AC1)").

**Spec Group**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/
**Atomic Specs**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/atomic/
  `,
  subagent_type: 'test-writer',
  run_in_background: true,
});
```

**Update session state**:

```json
{
  "workstream_execution": {
    "workstreams": [
      {
        "id": "ws-1",
        "status": "in_progress"
      }
    ]
  }
}
```

### 7. Monitor Subagent Completion

Poll background tasks for completion:

```javascript
// Wait for both implementer and test-writer
const ws1ImplResult = TaskOutput({ task_id: ws1Impl.task_id, block: true });
const ws1TestsResult = TaskOutput({ task_id: ws1Tests.task_id, block: true });

// Both complete → Ready for convergence validation
```

### 8. Run Convergence Validation

Dispatch unifier to validate workstream:

```javascript
Task({
  description: 'Validate ws-1 convergence in worktree-1',
  prompt: `
Validate convergence for workstream ws-1.

## EXECUTION CONTEXT

**Worktree**: worktree-1
**Path**: /Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-1
**Spec Group**: .claude/specs/groups/<master-spec-group-id>/workstreams/ws-1/

## VALIDATION REQUIREMENTS

- All atomic specs have status: implemented
- All atomic spec ACs have Implementation Evidence
- All atomic spec ACs have Test Evidence
- All tests passing
- Traceability chain complete (REQ → atomic spec → impl → test)
- Contract registry validated (if ws-1 owns contracts)

Produce convergence report with CONVERGED or NOT_CONVERGED status.
Update manifest.json convergence gates.
  `,
  subagent_type: 'unifier',
});
```

**If CONVERGED**:

- Update workstream status: "converged"
- Proceed to security review

**If NOT_CONVERGED**:

- Iteration count < 3 → Fix issues, re-run unifier
- Iteration count >= 3 → Escalate to user

### 9. Run Security Review

```javascript
Task({
  description: 'Security review for ws-1 in worktree-1',
  prompt: `
Review workstream ws-1 for security vulnerabilities.

**Worktree**: worktree-1
**Path**: /Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-1

Check: OWASP Top 10, input validation, auth/authz, secrets handling.
  `,
  subagent_type: 'security-reviewer',
});
```

**If PASSED**:

- Update convergence_status.security_reviewed: true
- Check if workstream has UI components → Run browser test (step 9a)
- If no UI → Add to merge queue

**If FAILED (Critical/High severity)**:

- Block merge
- Escalate to user with findings

### 9a. Run Browser Test (UI Workstreams Only)

For workstreams that include UI components (frontend, components, user-facing features):

```javascript
// Check if workstream has UI changes
const hasUIChanges = workstream.tags?.includes('ui') ||
  workstream.title.toLowerCase().includes('frontend') ||
  workstream.title.toLowerCase().includes('ui') ||
  workstream.title.toLowerCase().includes('component');

if (hasUIChanges) {
  Task({
    description: 'Browser test for ws-2 in worktree-2',
    prompt: `
Run browser-based UI testing for workstream ws-2.

**Worktree**: worktree-2
**Path**: /Users/matthewlin/Desktop/Personal Projects/engineering-assistant-ws-2

## TEST REQUIREMENTS

1. Navigate to relevant pages where UI changes were made
2. Verify visual appearance matches acceptance criteria
3. Test user interactions (clicks, form inputs, navigation)
4. Capture screenshots as evidence
5. Verify error states and edge cases

## ACCEPTANCE CRITERIA TO VERIFY

Reference the atomic specs for ws-2 and verify each UI-related AC:
- Visual elements render correctly
- Interactions work as specified
- Error messages display appropriately
- Responsive behavior (if applicable)

Report PASS or FAIL with evidence (screenshots, interaction logs).
    `,
    subagent_type: 'browser-tester',
  });
}
```

**If PASSED**:

- Update convergence_status.browser_tested: true
- Add to merge queue

**If FAILED**:

- Block merge
- Report UI issues to user with screenshots
- Wait for fixes, then re-validate

**If NO UI CHANGES**:

- Skip browser test
- Add directly to merge queue after security review

### 10. Process Merge Queue

For each workstream in merge queue (FIFO, respecting dependencies):

**Pre-Merge Checks**:

```bash
# Switch to worktree
cd /Users/matthewlin/Desktop/Personal\ Projects/engineering-assistant-ws-1

# Re-run tests (ensure still passing)
npm test

# Check for conflicts with main
git fetch origin main
git merge --no-commit --no-ff origin/main
if [ $? -ne 0 ]; then
  git merge --abort
  # Handle conflict (see facilitator error handling)
else
  git merge --abort  # Dry run successful
fi
```

**Execute Merge**:

```bash
# Commit any uncommitted changes in worktree
git add .
git commit -m "feat(ws-1): implement Backend API

Implements workstream ws-1 from <master-spec-group-id>

Atomic Specs:
- as-001: <title> ✅
- as-002: <title> ✅
- as-003: <title> ✅

Tests: 15 passing
Coverage: 92%
Convergence: PASSED (all atomic specs complete)
Security: PASSED

🤖 Generated with Claude Code
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Switch to main worktree
cd /Users/matthewlin/Desktop/Personal\ Projects/engineering-assistant

# Merge with --no-ff
git merge --no-ff feature/ws-1-backend-api -m "Merge ws-1: Backend API

Implements workstream ws-1 spec group

Atomic Specs: 3 complete
Contracts Provided:
- contract-backend-api: src/api/server.ts

Dependencies: none
Next: ws-2 can now proceed (dependency satisfied)"

# Push to remote
git push origin main
```

**Update session state**:

```json
{
  "workstream_execution": {
    "workstreams": [
      {
        "id": "ws-1",
        "status": "merged",
        "merge_timestamp": "2026-01-02T16:20:00Z"
      }
    ]
  }
}
```

### 11. Unblock Dependent Workstreams

After ws-1 merges, evaluate dependent workstreams:

```javascript
// Find workstreams that depend on ws-1
const dependents = workstreams.filter((ws) => ws.dependencies.includes('ws-1'));

for (const ws of dependents) {
  // Check if all dependencies now satisfied
  const allDepsMerged = ws.dependencies.every(
    (dep) => getWorkstream(dep).status === 'merged',
  );

  if (allDepsMerged) {
    // Unblock and dispatch
    updateWorkstreamStatus(ws.id, 'ready', null);
    dispatchImplementer(ws.id, ws.worktree_id);
  }
}
```

**Example**:

```
ws-1: merged ✅
ws-2: ready (dependency satisfied) → Dispatch implementer to worktree-2
ws-4: ready (dependency satisfied, shares worktree-1 with ws-1) → Dispatch test-writer to worktree-1
```

### 12. Repeat for All Workstreams

Continue cycle for each workstream:

1. Atomize and enforce (step 5)
2. Dispatch implementers/test-writers (step 6)
3. Monitor completion (step 7)
4. Run convergence validation (step 8)
5. Run security review (step 9)
6. Run browser test if UI workstream (step 9a)
7. Add to merge queue (step 10)
8. Merge to main
9. Unblock dependents (step 11)

Until all workstreams merged.

### 13. Cleanup Worktrees

After all workstreams merged:

```bash
# Remove all worktrees
git worktree remove ../engineering-assistant-ws-1
git worktree remove ../engineering-assistant-ws-2
git worktree remove ../engineering-assistant-ws-3

# Delete branches
git branch -d feature/ws-1-backend-api
git branch -d feature/ws-2-frontend-ui
git branch -d feature/ws-3-database-schema

# Verify cleanup
git worktree list  # Should only show main worktree
```

**Update session state**:

```json
{
  "worktree_allocation": {
    "worktrees": []
  }
}
```

### 14. Final Integration Validation

After all workstreams merged, run final validation:

```bash
# Full test suite on main
npm test

# Integration tests
npm run test:integration

# Build verification
npm run build
```

If all pass → Mark orchestrator task complete.

## Error Handling

### Merge Conflicts

If merge conflict detected:

1. Check if contract-based (favor contract owner)
2. Otherwise, escalate to user with conflict details
3. Preserve both worktrees for manual resolution

### Failed Convergence (3+ iterations)

If workstream fails convergence after 3 iterations:

1. Update workstream status: "blocked"
2. Preserve worktree for debugging
3. Escalate to user with validation results

### Security Failures (Critical/High)

If security review finds critical/high severity issues:

1. Block merge
2. Report findings to user
3. Wait for fixes, then re-validate

## State Management

Throughout orchestration, maintain session.json with:

- `worktree_allocation`: All active worktrees
- `workstream_execution`: Status of each workstream
- `merge_queue`: Workstreams ready to merge

Update after:

- Worktree creation
- Workstream status changes
- Convergence validation
- Merge completion
- Cleanup

## Success Criteria

Orchestrator task complete when:

- ✅ All workstream spec groups converged (all atomic specs implemented + tested)
- ✅ All UI workstreams browser tested
- ✅ All workstreams merged to main
- ✅ All worktrees cleaned up
- ✅ Integration tests passing
- ✅ No merge conflicts remain
- ✅ MasterSpec manifest.json shows all convergence gates passed
- ✅ Full traceability chain validated for each workstream

## Example Session

**User Request**: "Add real-time notifications"

**MasterSpec**: 3 workstreams

- ws-1: WebSocket Server (no deps)
- ws-2: Frontend Client (depends on ws-1)
- ws-3: Notification Service (depends on ws-1)

**Orchestration**:

1. Load MasterSpec ✅
2. Allocate worktrees (3 separate) ✅
3. Create worktrees ✅
4. Evaluate readiness (ws-1 ready, ws-2/ws-3 blocked) ✅
5. Atomize + enforce ws-1 ✅
6. Dispatch ws-1 implementer/test-writer ✅
7. ws-1 converges → Security review ✅ → Merge ✅
8. Unblock ws-2, ws-3 ✅
9. Atomize + enforce ws-2, ws-3 (parallel) ✅
10. Dispatch ws-2, ws-3 (parallel) ✅
11. ws-2 converges → Security review ✅ → Browser test (UI workstream) ✅ → Merge ✅
12. ws-3 converges → Security review ✅ → Merge ✅ (no browser test - backend only)
13. Cleanup worktrees ✅
14. Final validation ✅
15. Complete ✅
