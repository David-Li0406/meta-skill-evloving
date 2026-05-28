---
name: spec
description: Author specifications (TaskSpec for small-medium tasks, WorkstreamSpec for complex single-workstream tasks, or coordinate MasterSpec creation for multi-workstream efforts). Use after PM requirements gathering or when refining existing specs.
allowed-tools: Read, Write, Edit, Glob, Grep, Task
user-invocable: true
---

# Spec Author Skill

## Purpose

Create specifications that serve as the authoritative contract for implementation. Specs document requirements, design decisions, task breakdowns, and test plans.

**Key Output**: Creates `spec.md` in a spec group, reading from `requirements.md`.

## Usage

```
/spec <spec-group-id>           # Create spec.md from requirements.md in spec group
/spec refine <spec-group-id>    # Refine existing spec based on feedback
```

## Prerequisites

Before running `/spec`:
1. Spec group must exist at `.claude/specs/groups/<spec-group-id>/`
2. `requirements.md` must exist (from `/pm` or `/prd sync`)
3. `manifest.json` must exist with valid metadata

## Output Location

All specs are written to the spec group directory:
```
.claude/specs/groups/<spec-group-id>/
├── manifest.json      # Updated by /spec
├── requirements.md    # Input (from /pm or /prd)
└── spec.md           # Output (created by /spec)
```

## Spec Tiers

The complexity of the spec is determined by the requirements, but **all specs output to `spec.md`** in the spec group.

### TaskSpec (Light) - For Small to Medium Tasks
Use for:
- Single feature or enhancement
- 2-5 files impacted
- Clear scope, single workstream
- Estimated 30 min - 4 hours

**Sections**:
- Context & Goal
- Requirements Summary (references requirements.md)
- Acceptance Criteria
- Design Notes (optional)
- Task List
- Test Plan
- Decision & Work Log

### WorkstreamSpec (Full) - For Complex Single-Workstream Tasks
Use for:
- Complex feature requiring detailed design
- Multiple components or layers involved
- Needs sequence diagrams and interface definitions
- Estimated 4-8 hours
- Part of a larger effort but can be worked independently

**Sections**:
- Context
- Goals / Non-goals
- Requirements Summary (references requirements.md)
- Core Flows
- Sequence Diagrams (Mermaid)
- Edge Cases
- Interfaces & Data Model
- Security
- Additional Considerations
- Task List
- Testing
- Open Questions
- Workstream Reflection
- Decision & Work Log

### MasterSpec (Multi-workstream) - For Large Projects
Use for:
- 5+ workstreams needed
- Multiple parallel efforts
- Complex dependencies and contracts
- Requires orchestration and integration

**Approach**: Use `/orchestrate` skill which creates separate spec groups per workstream.

## Process: Spec Creation in Spec Group

### Step 1: Validate Spec Group

```
Read: .claude/specs/groups/<spec-group-id>/manifest.json
Read: .claude/specs/groups/<spec-group-id>/requirements.md
```

Verify:
- Spec group exists
- `requirements.md` has REQ-XXX requirements
- `manifest.json` has valid metadata

### Step 2: Read Requirements

From `requirements.md`, extract:
- Problem statement
- Goals and non-goals
- REQ-XXX requirements in EARS format
- Constraints and assumptions
- Open questions

### Step 3: Fill Context & Goal

From `requirements.md`:
- Summarize the problem and motivation
- State the clear goal and success criteria

### Step 4: Reference Requirements

**Do NOT duplicate requirements** — reference `requirements.md`:

```markdown
## Requirements Summary

See `requirements.md` for full EARS-format requirements.

| ID | Title | Priority |
|----|-------|----------|
| REQ-001 | User-initiated logout | Must Have |
| REQ-002 | Token clearing | Must Have |
| REQ-003 | Post-logout redirect | Must Have |
| REQ-004 | Error handling | Must Have |
```

### Step 5: Define Acceptance Criteria

Map requirements to testable acceptance criteria:

```markdown
## Acceptance Criteria

- AC1.1: Logout button clears authentication token
- AC1.2: User is redirected to login page after logout
- AC1.3: Confirmation message is displayed
- AC2.1: Network error shows error message
- AC2.2: User remains logged in on error
- AC2.3: Retry button appears on error
```

### Step 5: Add Design Notes
If non-trivial, document approach:
- Architecture decisions
- Key algorithms or data structures
- Sequence diagrams for primary flows

```markdown
## Design Notes

The logout flow will:
1. Call `/api/auth/logout` endpoint
2. Clear local storage token on success
3. Update auth context state
4. Router will redirect based on auth state change

Sequence diagram:

\`\`\`mermaid
sequenceDiagram
  autonumber
  participant User
  participant UI
  participant AuthService
  participant API
  User->>UI: Click logout
  UI->>AuthService: logout()
  AuthService->>API: POST /api/auth/logout
  API-->>AuthService: 200 OK
  AuthService->>AuthService: clearToken()
  AuthService-->>UI: Success
  UI->>UI: Redirect to /login
  UI-->>User: Show confirmation
\`\`\`
```

### Step 6: Generate Task List
Break down requirements into concrete tasks:

```markdown
## Task List

- [ ] Add logout button to UserMenu component
- [ ] Implement AuthService.logout() method
- [ ] Create /api/auth/logout endpoint
- [ ] Add error handling for network failures
- [ ] Update router to redirect on auth state change
- [ ] Add confirmation message toast
```

### Step 7: Map Test Plan
Map each acceptance criterion to test cases:

```markdown
## Test Plan

- AC1.1 → `__tests__/auth-service.test.ts`: "should clear token on logout"
- AC1.2 → `__tests__/auth-router.test.ts`: "should redirect to /login after logout"
- AC1.3 → `__tests__/user-menu.test.ts`: "should show confirmation message"
- AC2.1 → `__tests__/auth-service.test.ts`: "should show error on network failure"
- AC2.2 → `__tests__/auth-service.test.ts`: "should keep user logged in on error"
- AC2.3 → `__tests__/user-menu.test.ts`: "should show retry button on error"
```

### Step 8: Record Initial Decision

Add to Decision & Work Log:

```markdown
## Decision & Work Log

- 2026-01-14: Spec created from requirements.md
- 2026-01-14: Decision - Use toast for confirmation (consistent with existing patterns)
```

### Step 9: Write spec.md

Save to spec group:
```
.claude/specs/groups/<spec-group-id>/spec.md
```

### Step 10: Update manifest.json

Update the spec group manifest:

```json
{
  "convergence": {
    "spec_complete": true
  },
  "decision_log": [
    // ... existing entries ...
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "spec_authored",
      "details": "spec.md created with X ACs, Y tasks"
    }
  ]
}
```

### Step 11: Report Completion

```markdown
## Spec Created ✅

**Spec Group**: <spec-group-id>
**Location**: .claude/specs/groups/<spec-group-id>/spec.md

**Summary**:
- X acceptance criteria mapped to requirements
- Y tasks identified
- Z open questions

**Next Steps**:
1. Review spec: `.claude/specs/groups/<spec-group-id>/spec.md`
2. Run `/atomize <spec-group-id>` to decompose into atomic specs
3. Run `/enforce <spec-group-id>` to validate atomicity
```

## Process: Complex Specs (WorkstreamSpec-level detail)

For complex features requiring sequence diagrams and interface definitions:

### Additional Sections Required

Follow the template structure:
1. **Context**: Background and motivation
2. **Goals / Non-goals**: Explicit boundaries
3. **Requirements**: Atomic, testable requirements (EARS format)
4. **Core Flows**: Primary user flows and system behaviors
5. **Sequence Diagram(s)**: At least one Mermaid diagram
6. **Edge Cases**: Failure scenarios and unusual conditions
7. **Interfaces & Data Model**: Contracts, APIs, data structures
8. **Security**: Security considerations and requirements
9. **Additional Considerations**: Best practices, docs, memory bank updates
10. **Task List**: Discrete tasks with dependencies
11. **Testing**: Testing strategy and coverage
12. **Open Questions**: Unresolved questions with status
13. **Workstream Reflection**: (Fill during/after implementation)
14. **Decision & Work Log**: Decisions and approvals

### Step 3: Define Contracts
If this workstream creates interfaces used by others:

```yaml
contracts:
  - id: contract-auth-service
    type: API
    path: src/services/auth.service.ts
    version: 1.0
```

Add to contract registry in MasterSpec (if applicable).

### Step 4: Identify Dependencies
List other workstreams this depends on:

```yaml
dependencies:
  - ws-database-schema
  - ws-api-gateway
```

## Process: MasterSpec Coordination

For large multi-workstream efforts, coordinate parallel spec authoring.

### Step 1: Create ProblemBrief
Start with high-level brief:

```bash
cp .claude/templates/master-spec.template.md .claude/specs/active/<slug>/master.md
```

Fill Problem Brief section from PM discovery.

### Step 2: Identify Workstreams
Decompose into parallel workstreams:
- Each workstream should be independently executable
- Minimize cross-workstream coupling
- Identify clear contracts/interfaces between workstreams

Example workstream breakdown:
```markdown
## Workstream Overview

| ID | Title | Owner | Estimated Effort |
|----|-------|-------|------------------|
| ws-1 | WebSocket Server | spec-author-1 | 6-8h |
| ws-2 | Frontend Client | spec-author-2 | 4-6h |
| ws-3 | Notification Service | spec-author-3 | 6-8h |
```

### Step 3: Dispatch Spec-Author Subagents
Use Task tool to create workstream specs in parallel:

```javascript
// Dispatch subagent for ws-1
Task({
  description: "Author WebSocket Server workstream spec",
  prompt: `Create a WorkstreamSpec for the WebSocket Server workstream.

Context from ProblemBrief:
<paste relevant context>

Your scope:
- WebSocket server infrastructure
- Authentication middleware
- Message routing

Contracts you provide:
- contract-websocket-api: Client connection API

Dependencies:
- ws-3 (Notification Service provides messages)

Follow the WorkstreamSpec template at .claude/templates/workstream-spec.template.md`,
  subagent_type: "spec-author"
})
```

Dispatch one subagent per workstream.

### Step 4: Collect and Review
Review completed workstream specs:
- Check for missing sections
- Verify contracts are registered
- Confirm dependencies are valid (no cycles)

### Step 5: Merge into MasterSpec
Update MasterSpec with:
- Links to workstream specs
- Contract registry (consolidated)
- Dependency graph
- Gates & acceptance criteria

```markdown
## Contract Registry

| Contract ID | Type | Owner Workstream | Path | Version |
|-------------|------|------------------|------|---------|
| contract-websocket-api | API | ws-1 | src/websocket/server.ts | 1.0 |
| contract-notification-api | API | ws-3 | src/services/notifications.ts | 1.0 |

## Cross-Workstream Dependencies

\`\`\`mermaid
graph TD
  ws-1[WebSocket Server] --> ws-3[Notification Service]
  ws-2[Frontend Client] --> ws-1
\`\`\`
```

### Step 5.5: Determine Worktree Allocation

Analyze dependency graph and workstream coupling to allocate worktrees:

**Allocation Analysis**:
1. **Identify independent workstreams**:
   - No shared files
   - No tight coupling
   - Can execute fully in parallel
   - → Assign separate worktrees

2. **Identify tightly coupled workstreams**:
   - Implementation + tests for same feature
   - Sequential modifications to same files
   - One workstream's output is immediate input to another
   - → Share worktree

3. **Consider dependency ordering**:
   - Workstreams with no dependencies can start immediately
   - Dependent workstreams blocked until prerequisites merge
   - Document merge order in allocation strategy

**Example Allocation**:
```markdown
# Analyzing 4 workstreams

ws-1: Backend API (no dependencies, independent) → worktree-1
ws-2: Frontend UI (depends on ws-1, independent from ws-3) → worktree-2
ws-3: Database schema (no dependencies, independent) → worktree-3
ws-4: Integration tests (tests ws-1, tight coupling) → worktree-1 (shared with ws-1)

**Rationale**:
- ws-1 and ws-4 share worktree: ws-4 tests ws-1 implementation (tight coupling)
- ws-2 separate: Independent frontend work, no file conflicts with backend
- ws-3 separate: Independent database work, can run in parallel

**Merge Order**:
1. ws-1 (no dependencies) + ws-4 (tests ws-1) → Merge together from worktree-1
2. ws-2 (depends on ws-1) → Blocked until ws-1 merges
3. ws-3 (no dependencies) → Can merge anytime (parallel with ws-1)
```

**Document in MasterSpec**:
Add worktree allocation strategy to MasterSpec:
```markdown
## Worktree Allocation Strategy

**Strategy**: ws-1 and ws-4 share worktree (tight coupling), ws-2 and ws-3 isolated (independent)

| Worktree ID | Branch | Workstreams | Rationale |
|-------------|--------|-------------|-----------|
| worktree-1 | feature/ws-1-backend-api | ws-1, ws-4 | ws-4 tests ws-1 implementation |
| worktree-2 | feature/ws-2-frontend-ui | ws-2 | Independent frontend work |
| worktree-3 | feature/ws-3-database-schema | ws-3 | Independent database work |

**Merge Order**:
1. ws-1+ws-4 (no dependencies)
2. ws-3 (no dependencies) - can merge in parallel with ws-1
3. ws-2 (depends on ws-1) - blocked until ws-1 merges
```

Update Workstream Overview table with Worktree column.

### Step 6: Validate Gates
Check spec-complete gates:
- [ ] All workstream specs approved
- [ ] Contract registry complete and validated
- [ ] No unresolved cross-workstream conflicts
- [ ] Dependency graph is acyclic
- [ ] All critical open questions resolved or deferred

## Spec is Contract Principle

**Critical constraint**: Spec is the authoritative source of truth.

- Implementation must conform to spec
- Tests must verify spec requirements
- Any deviation requires spec amendment first
- Spec updates require user approval

If during implementation you discover:
- Missing requirements → Add to spec Open Questions, get approval
- Invalid assumptions → Update spec, note in Decision Log
- Better approaches → Propose spec amendment before implementing

**Never deviate silently from the spec.**

## Spec Approval Process

Before implementation begins:

1. **Present spec summary** to user
2. **Highlight key decisions** and assumptions
3. **Call out open questions** that need resolution
4. **Request approval** to proceed
5. **Record approval** in Decision & Work Log with date

Example approval request:
```markdown
## Spec Ready for Approval

I've created a TaskSpec for adding the logout button.

**Key decisions**:
- Using toast for confirmation (consistent with existing patterns)
- Network errors keep user logged in and allow retry

**Open questions**:
- Should we add keyboard shortcut (Cmd+L) for logout? (Low priority, can defer)

**Task list**: 6 tasks, estimated 2-3 hours

May I proceed with implementation?
```

## Integration with Spec Group Workflow

After spec creation:

```
/pm → requirements.md
  ↓
/spec → spec.md (YOU ARE HERE)
  ↓
/atomize → atomic/*.md
  ↓
/enforce → validation
  ↓
User approves → review_state: APPROVED
  ↓
/implement + /test (parallel, per atomic spec)
  ↓
/unify → convergence validation
  ↓
/code-review + /security
  ↓
Merge
```

### State After /spec Completes

```json
{
  "review_state": "DRAFT",        // Still needs user review
  "work_state": "PLAN_READY",     // Ready for atomization
  "convergence": {
    "spec_complete": true         // Spec authored
  }
}
```

### Handoff to /atomize

After `/spec` creates `spec.md`:
1. User reviews spec
2. Run `/atomize <spec-group-id>` to decompose into atomic specs
3. Run `/enforce <spec-group-id>` to validate atomicity
4. User approves → `review_state: APPROVED`
5. Implementation begins

## Examples

### Example 1: TaskSpec for Logout Button

```markdown
---
id: task-logout-button
title: Add Logout Button to User Dashboard
date: 2026-01-02
status: draft
---

# Add Logout Button to User Dashboard

## Context
Users currently cannot log out from the dashboard. They must manually delete cookies or close the browser.

## Goal
Provide a visible, accessible logout button that clears authentication and redirects to login page.

## Requirements (EARS Format)

- **WHEN** user clicks logout button
- **THEN** system shall clear authentication token
- **AND** redirect to login page
- **AND** display confirmation message

- **WHEN** logout fails due to network error
- **THEN** system shall display error message
- **AND** keep user logged in
- **AND** show retry button

## Acceptance Criteria

- AC1.1: Logout button clears authentication token
- AC1.2: User redirected to /login after logout
- AC1.3: Confirmation toast displayed
- AC2.1: Network error shows error message
- AC2.2: User remains logged in on error
- AC2.3: Retry button appears on error

## Design Notes

Use AuthService.logout() method. Toast for confirmation (consistent with existing patterns).

## Task List

- [ ] Add logout button to UserMenu component
- [ ] Implement AuthService.logout() method
- [ ] Add error handling for network failures
- [ ] Add confirmation toast
- [ ] Write tests for all acceptance criteria

## Test Plan

- AC1.1 → `__tests__/auth-service.test.ts`: "should clear token"
- AC1.2 → `__tests__/auth-router.test.ts`: "should redirect to /login"
- AC1.3 → `__tests__/user-menu.test.ts`: "should show confirmation"
- AC2.1 → `__tests__/auth-service.test.ts`: "should show error on failure"
- AC2.2 → `__tests__/auth-service.test.ts`: "should keep user logged in on error"
- AC2.3 → `__tests__/user-menu.test.ts`: "should show retry button"

## Decision & Work Log

- 2026-01-02: Spec created
- 2026-01-02: Decision - Toast for confirmation
```

### Example 2: WorkstreamSpec for WebSocket Server

See `.claude/templates/workstream-spec.template.md` for full structure.

Key sections filled:
- Context: Real-time notifications require WebSocket infrastructure
- Requirements: Authentication, message routing, connection management (EARS format)
- Sequence Diagram: Client connection, authentication, message delivery flows
- Contracts: `contract-websocket-api` with connection interface
- Dependencies: ws-3 (Notification Service)
- Task List: 8 tasks broken down by component
