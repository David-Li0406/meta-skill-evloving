---
name: implement
description: Implement code changes based on approved atomic specs. Executes one atomic spec at a time, gathers evidence, and escalates if implementation reveals spec gaps. Use after spec group approval.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
user-invocable: true
---

# Implementation Skill

## Purpose

Execute implementation from approved atomic specs with full traceability to requirements.

**Key Input**: Atomic specs from `.claude/specs/groups/<spec-group-id>/atomic/`

## Usage

```
/implement <spec-group-id>                    # Implement all atomic specs in order
/implement <spec-group-id> <atomic-spec-id>   # Implement specific atomic spec
/implement <spec-group-id> --parallel         # Dispatch parallel implementers per atomic spec
```

## Prerequisites

Before using this skill, verify:

1. **Spec group exists** at `.claude/specs/groups/<spec-group-id>/`
2. **review_state** is `APPROVED` in manifest.json
3. **Atomic specs exist** in `atomic/` directory
4. **Enforcement passed** (`atomic_specs.enforcement_status: "passing"`)
5. **Open questions** are resolved or explicitly deferred

If prerequisites not met → STOP and resolve before implementing.

## Implementation Process

### Step 0: Load Session Context

Check for existing session state to enable resuming mid-implementation:

```bash
# Check session checkpoint
cat .claude/context/session.json | jq '.phase_checkpoint'
```

If `atomic_specs_pending` has values, use those as the implementation queue instead of starting fresh. This enables cross-session recovery if implementation was interrupted.

```json
{
  "phase_checkpoint": {
    "phase": "implementing",
    "atomic_specs_pending": ["as-003", "as-004"],
    "atomic_specs_complete": ["as-001", "as-002"],
    "last_completed": "as-002"
  }
}
```

If no checkpoint exists or `phase` is not `implementing`, proceed with full atomic spec list from Step 2.

### Step 1: Load and Verify Spec Group

```
Read: .claude/specs/groups/<spec-group-id>/manifest.json
Read: .claude/specs/groups/<spec-group-id>/requirements.md
Read: .claude/specs/groups/<spec-group-id>/spec.md
List: .claude/specs/groups/<spec-group-id>/atomic/*.md
```

Verify in manifest.json:

- `review_state` is `APPROVED`
- `atomic_specs.enforcement_status` is `passing`
- No blocking open questions

### Step 2: List Atomic Specs

```
.claude/specs/groups/<spec-group-id>/atomic/
├── as-001-logout-button-ui.md
├── as-002-token-clearing.md
├── as-003-post-logout-redirect.md
└── as-004-error-handling.md
```

Each atomic spec is independently implementable. Execute in order (as-001, as-002, etc.).

### Step 3: Understand the Codebase

Before making changes, study existing patterns:

- File structure and naming conventions
- Error handling patterns
- Testing approaches

### Step 4: Execute Atomic Specs in Order

For each atomic spec:

#### 4a. Mark Atomic Spec as In Progress

Update atomic spec frontmatter:

```yaml
status: implementing
```

Update manifest.json:

```json
{
  "work_state": "IMPLEMENTING"
}
```

Update session checkpoint to track implementation phase:

```bash
# Update session checkpoint
node .claude/scripts/session-checkpoint.mjs transition-phase implementing
```

#### 4b. Read Atomic Spec

From the atomic spec file, extract:

- Description (single behavior to implement)
- Acceptance criteria
- Test strategy
- Deployment notes

#### 4c. Implement the Atomic Spec

Follow spec requirements exactly:

- Use existing patterns from codebase
- Maintain naming conventions
- Include error handling as specified
- Add comments linking to AC numbers

#### 4d. Run Relevant Tests

```bash
npm test -- <related-test>
```

#### 4e. Fill Implementation Evidence

Update the atomic spec's Implementation Evidence section:

```markdown
## Implementation Evidence

| File                         | Line | Description                  |
| ---------------------------- | ---- | ---------------------------- |
| src/services/auth-service.ts | 67   | logout() method clears token |
| src/components/UserMenu.tsx  | 42   | Logout button component      |
```

#### 4f. Mark Atomic Spec Complete

Update atomic spec frontmatter:

```yaml
status: implemented
```

Add to atomic spec Decision Log:

```markdown
## Decision Log

- `2026-01-14T10:30:00Z`: Created from spec.md decomposition
- `2026-01-14T14:30:00Z`: Implementation complete - auth-service.ts:67
```

#### 4g. Update Session Checkpoint

After each atomic spec completion, update session state for cross-session recovery:

```bash
# Mark atomic spec complete in session
node .claude/scripts/session-checkpoint.mjs complete-atomic-spec <atomic_spec_id>
```

This ensures that if the session ends unexpectedly, the next session can resume from the correct atomic spec.

### Step 5: Handle Spec Deviations

If you discover during implementation:

#### Scenario A: Missing Requirement

Spec doesn't cover a necessary case.

**Action**:

1. STOP implementation
2. Document in spec's Open Questions:

```markdown
## Open Questions

- Q3: How should logout behave if user has unsaved changes? (Status: blocking)
  - Discovered during implementation
  - Need user decision before proceeding
```

3. Ask user for guidance
4. Update spec with decision
5. Resume implementation

#### Scenario B: Invalid Assumption

Spec assumes something that's not true in the codebase.

**Action**:

1. STOP implementation
2. Document in spec's Decision & Work Log:

```markdown
- 2026-01-02: **Issue** - Spec assumes AuthService.logout() exists, but it doesn't
- **Proposed amendment**: Add AuthService.logout() method to task list
- **Status**: Awaiting approval
```

3. Propose spec amendment
4. Get user approval
5. Update spec
6. Resume implementation

#### Scenario C: Better Approach Discovered

Found a more efficient or clearer way to achieve the requirement.

**Action**:

1. Evaluate: Does this change the **behavior** or just the **implementation**?
2. If behavior unchanged → Proceed (implementation detail)
3. If behavior changes → Propose spec amendment with rationale
4. Get approval before deviating

**Never silently deviate from the spec.**

### Step 6: Validate Implementation

After all atomic specs complete:

```bash
# Run full test suite
npm test

# Check for lint errors
npm run lint

# Build if applicable
npm run build
```

Ensure:

- All tests passing
- No lint errors
- Build succeeds
- No console errors introduced

### Step 7: Update Manifest

Update manifest.json with implementation complete:

```json
{
  "work_state": "VERIFYING",
  "convergence": {
    "all_acs_implemented": true
  },
  "decision_log": [
    // ... existing entries ...
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "implementation_complete",
      "details": "All 4 atomic specs implemented, tests passing"
    }
  ],
  "session_ref": {
    "session_id": "<current-session-uuid>",
    "last_checkpoint": "<ISO-timestamp>",
    "last_atomic_spec": "<last-completed-as-id>",
    "checkpoint_phase": "implementing",
    "checkpoint_state": "clean"
  }
}
```

Transition to verifying phase for cross-session tracking:

```bash
# Transition to verifying phase
node .claude/scripts/session-checkpoint.mjs transition-phase verifying
```

### Step 8: Report Completion

```markdown
## Implementation Complete ✅

**Spec Group**: <spec-group-id>
**Atomic Specs**: 4/4 complete

**Evidence**:

- as-001: src/components/UserMenu.tsx:42
- as-002: src/services/auth-service.ts:67
- as-003: src/router/auth-router.ts:23
- as-004: src/services/auth-service.ts:78

**Tests**: All passing
**Build**: Successful

**Next Steps**:

1. Run `/test <spec-group-id>` to ensure test coverage (if not done in parallel)
2. Run `/unify <spec-group-id>` to validate convergence
```

## Parallel Execution with Test Writer

For larger tasks, implementation and test writing can run in parallel.

### When to Parallelize

- Multiple independent tasks in task list
- Clear acceptance criteria for each task
- Low coupling between tasks

### How to Parallelize

Use Task tool to dispatch subagents:

```javascript
// Dispatch implementer subagent
Task({
  description: "Implement logout functionality",
  prompt: `Implement tasks 1-3 from TaskSpec at .claude/specs/active/logout-button.md

  Focus on:
  - Adding logout button component
  - Implementing AuthService.logout() method
  - Adding error handling

  Do NOT implement tests - test-writer will handle that.

  Follow spec requirements exactly. Escalate if spec gaps discovered.`,
  subagent_type: "implementer",
});

// Dispatch test-writer subagent in parallel
Task({
  description: "Write tests for logout functionality",
  prompt: `Write tests for acceptance criteria AC1.1-AC2.3 from TaskSpec at .claude/specs/active/logout-button.md

  Map each AC to specific test cases.
  Follow AAA pattern.
  Tests will initially fail until implementation complete.`,
  subagent_type: "test-writer",
});
```

Main agent retains integration responsibility:

- Collect outputs from both subagents
- Ensure tests pass with implementation
- Run unifier to validate alignment

## Spec Conformance Rules

### DO:

- Follow spec requirements exactly
- Use existing codebase patterns
- Ask user when spec is unclear
- Update spec when discovering gaps
- Log evidence of completion
- Run tests after each task

### DON'T:

- Add features not in spec
- Deviate from specified behavior
- Assume unstated requirements
- Skip error handling specified in spec
- Make breaking changes not mentioned in spec
- Silently fix spec errors - propose amendments instead

## Integration with Other Skills

After implementation:

- Use `/unify` to validate spec-impl-test alignment

**After unify passes, the review chain is**:

1. `/code-review` - Code quality review (always)
2. `/security` - Security review (always)
3. `/browser-test` - UI validation (if UI changes)
4. `/docs` - Documentation generation (if public API)
5. Commit

## Error Handling

### Build Failures

```bash
npm run build
# Error: ...
```

**Action**:

1. Read error message carefully
2. Check if spec anticipated this (Security section, Edge Cases)
3. If spec covers it → Implement as specified
4. If spec doesn't cover it → Add to Open Questions, get guidance

### Test Failures

```bash
npm test
# FAIL: expected X, got Y
```

**Action**:

1. Determine if test or implementation is wrong
2. If test is wrong → Fix test to match spec
3. If implementation is wrong → Fix implementation to match spec
4. If spec is wrong → Propose spec amendment

### Merge Conflicts

If working in parallel with other workstreams:

```bash
git pull origin main
# CONFLICT: ...
```

**Action**:

1. Check MasterSpec contract registry
2. Verify your implementation matches contract interface
3. Resolve conflict favoring contract definition
4. If contract is ambiguous → Escalate to orchestrator

## Examples

### Example 1: Simple Task Execution

**Spec**: TaskSpec for logout button (AC1.1: Clear token)

**Implementation**:

```typescript
// src/services/auth.service.ts

async logout(): Promise<void> {
  try {
    // Call API to invalidate session
    await this.api.post('/auth/logout');

    // Clear local token (AC1.1)
    localStorage.removeItem('auth_token');

    // Update auth state
    this.authState.next({ isAuthenticated: false });
  } catch (error) {
    // AC2.1: Display error on failure
    throw new Error('Logout failed. Please try again.');
  }
}
```

**Evidence**:

- Task marked complete in spec
- Tests passing: `auth-service.test.ts` (2 tests)
- AC1.1 verified: Token cleared from localStorage

### Example 2: Discovering Spec Gap

**During implementation**, discovered:

- Spec says "redirect to login page"
- But doesn't specify: Should we preserve the return URL for after re-login?

**Action**:

```markdown
## Open Questions

- Q4: Should we preserve return URL for post-login redirect? (Status: blocking)
  - Discovered during implementation of redirect logic
  - Options:
    - A: Redirect to /login (simple, spec as written)
    - B: Redirect to /login?returnUrl=<current> (better UX)
  - **Recommendation**: Option B for better UX
  - Awaiting user decision
```

**Result**: User chooses Option B → Update spec → Implement with return URL preservation

### Example 3: Parallel Implementation

**Scenario**: MasterSpec with 3 workstreams

**Main agent**:

```javascript
// Dispatch implementers for each workstream
const ws1 = Task({
  description: "Implement WebSocket Server (ws-1)",
  prompt: "Implement workstream ws-1 from master spec...",
  subagent_type: "implementer",
});

const ws2 = Task({
  description: "Implement Frontend Client (ws-2)",
  prompt: "Implement workstream ws-2 from master spec...",
  subagent_type: "implementer",
});

const ws3 = Task({
  description: "Implement Notification Service (ws-3)",
  prompt: "Implement workstream ws-3 from master spec...",
  subagent_type: "implementer",
});

// Wait for all to complete
// Then run unifier for cross-workstream validation
```

**Result**: Parallel execution with main agent handling integration and contract validation
