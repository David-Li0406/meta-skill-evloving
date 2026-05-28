---
name: route
description: Analyze task complexity and route to appropriate workflow. Defaults to oneoff-spec (specs are cheap, bugs are expensive). Use oneoff-vibe only for truly trivial changes or explicit user override. Use orchestrator for large multi-workstream efforts. Use journal-only for non-spec work that needs documentation.
allowed-tools: Read, Glob, Grep
---

# Route Skill

## Purpose

Analyze the user request and determine the appropriate workflow path based on task complexity, scope, and estimated effort.

## Complexity Heuristics

> **Default to specs.** Use oneoff-spec unless the task is truly trivial OR the user explicitly requests to skip specs.

### Trivial (oneoff-vibe)

Route to quick execution **only when**:

**Truly trivial changes** (all must apply):

- Single-line or few-character fix (typo, off-by-one, missing semicolon)
- Zero ambiguity about what to change
- No behavioral impact beyond the obvious fix
- No tests needed or test change is equally trivial

**Examples of truly trivial**:

- Fix typo in README: "teh" → "the"
- Fix obvious syntax error
- Update version number in config
- Add missing import that's causing a build error
- Comment clarification

**User explicitly requests vibe**:

- User says: "just do it", "vibe", "skip the spec", "don't need a spec", "quick fix"
- Honor the request but note in rationale

**NOT trivial (use oneoff-spec instead)**:

- Bug fix requiring investigation
- "Simple" feature additions (even small ones have edge cases)
- Documentation updates with new content (not just typo fixes)
- Configuration changes affecting behavior
- Any change where you'd want to verify acceptance criteria

### Standard (oneoff-spec / Spec Group) — THE DEFAULT

Route to spec group workflow for **most tasks**:

- Any feature addition, enhancement, or new functionality
- Bug fixes (even "simple" ones benefit from AC definition)
- Refactoring with defined goals
- Documentation with new content
- API changes
- UI changes
- **Needs spec group**: requirements.md, spec.md, atomic specs
- **Spec location**: `.claude/specs/groups/<spec-group-id>/`
- **Why default**: Specs create accountability, testability, and prevent scope creep

### Large (orchestrator / MasterSpec)

Route to multi-workstream orchestration with git worktrees:

- 5+ files impacted across multiple layers
- Multiple workstreams with interdependencies
- Cross-cutting concerns (contracts, interfaces, shared state)
- Impacts multiple services, layers, or subsystems
- Requires parallel execution by multiple subagents
- Complex coordination and integration needs
- **Estimated effort**: 4+ hours
- **Needs MasterSpec with workstream spec groups**: Each workstream gets its own spec group with atomic specs
- **Spec structure**: `.claude/specs/groups/<master-spec-group-id>/` with workstream subdirectories
- **Parallel execution**: Workstreams execute in isolated git worktrees
- **Dependency orchestration**: Facilitator manages merge order based on dependencies
- **MANDATORY**: Run `/investigate` before implementation to surface cross-workstream inconsistencies (env vars, API contracts, data shapes, deployment assumptions)

### Refactor (refactor workflow)

Route to refactor workflow for code quality improvements:

- Explicit refactoring requests ("refactor this", "clean up", "improve code quality")
- Tech debt reduction tasks
- Pattern migration requests ("migrate from X to Y pattern")
- Code consolidation or deduplication
- Architecture improvements without feature changes
- **Key constraint**: Behavior must be preserved (no feature changes)
- **Needs**: Clear scope definition, before/after patterns, test verification
- **Uses**: `/refactor` skill with Refactorer subagent
- **Validation**: Tests must pass before and after (behavior preservation proof)

**Refactor triggers** (route to refactor when ANY apply):

- User says: "refactor", "clean up", "improve code quality", "reduce tech debt"
- User says: "migrate to <pattern>", "consolidate", "deduplicate"
- Request focuses on code structure without changing behavior
- Request mentions: "maintainability", "readability", "consistency"

**NOT refactor** (route to oneoff-spec instead):

- "Refactor and add feature X" → oneoff-spec (behavior changes)
- "Clean up and fix this bug" → oneoff-spec (behavior changes)
- Unclear if behavior should change → oneoff-spec (spec clarifies intent)

### Journal-Only (non-spec documentation)

Route to journal-only workflow for work that doesn't need a full spec but should be documented:

**When to use journal-only**:

- Quick investigation that produced findings worth documenting
- Bug fix outside of spec work (hotfix, emergency patch)
- Ad-hoc decision that should be recorded for future reference
- Exploration that uncovered architectural insights
- One-off configuration change with rationale worth preserving

**Journal-only triggers** (route to journal-only when ANY apply):

- Work is complete but findings should be preserved
- Decision was made that future developers should know about
- Investigation uncovered non-obvious behavior or gotchas
- User says: "document this", "record this decision", "log this finding"
- Bug was fixed but root cause analysis is valuable

**Journal types**:

- **Investigation journal**: Findings from exploration, debugging, research
- **Decision record**: Architectural or design decision with rationale (uses `.claude/templates/decision-record.template.md`)
- **Hotfix journal**: Emergency fix documentation with root cause

**NOT journal-only** (route to spec workflow instead):

- Work that needs formal acceptance criteria → oneoff-spec
- Feature development (even small) → oneoff-spec
- Planned refactoring → refactor
- Work that needs review gates → oneoff-spec

**Key distinction**: Journal-only is for **documenting completed work**, not planning future work. If you need to plan and verify, use a spec.

## Routing Process

### Step 0: Check for Incomplete Work

Before analyzing a new request, check for existing incomplete work that can be resumed.

**Check for active work**:

```bash
# Check if session.json exists with active work
cat .claude/context/session.json 2>/dev/null | node -e "
const data = JSON.parse(require('fs').readFileSync(0, 'utf8'));
if (data.active_work) {
  console.log(JSON.stringify(data.active_work, null, 2));
  process.exit(0);
}
process.exit(1);
"
```

**If active_work exists and is not null**, display a resume prompt:

```markdown
## Found Incomplete Work

**Objective**: [objective from session.json]
**Spec Group**: [spec_group_id]
**Phase**: [current_phase] ([progress summary])
**Last Updated**: [updated_at]

Would you like to resume this work? [Y/n]
```

**If user confirms (Y, yes, or empty/default)**:

1. Skip normal routing
2. Load the spec group manifest:
   ```bash
   cat .claude/specs/groups/<spec_group_id>/manifest.json
   ```
3. Continue from the current phase based on `current_phase` value:
   - `pm_interview` → Continue PM interview with `/pm`
   - `spec_authoring` → Continue spec authoring with `/spec`
   - `atomizing` → Continue atomization with `/atomize`
   - `enforcing` → Continue enforcement with `/enforce`
   - `investigating` → Continue investigation with `/investigate`
   - `awaiting_approval` → Remind user spec is awaiting approval, display approval prompt
   - `implementing` → Resume implementation with `/implement`, starting from next pending atomic spec
   - `testing` → Resume test writing with `/test`
   - `verifying` → Run unify validation with `/unify`
   - `reviewing` → Continue code review with `/code-review` or security review with `/security`
4. Output the appropriate next action based on phase

**If user declines (n, no, or "work on something else")**:

1. Archive the incomplete work:
   ```bash
   node .claude/scripts/session-checkpoint.mjs archive-incomplete
   ```
2. Proceed with normal routing (Step 1 onwards)

### Step 1: Load Context

If the user references an existing spec group:

```bash
# Check for active spec group
ls .claude/specs/groups/<spec-group-id>/manifest.json 2>/dev/null
```

Load the spec group and continue from its current state based on `review_state` and `work_state`.

### Step 2: Analyze Scope

Use Glob and Grep to understand impact:

```bash
# Find relevant files
glob "**/*.ts" | grep -i "<keyword>"

# Understand current architecture
grep -r "class <Name>" --include="*.ts"
```

### Step 3: Apply Heuristics

Count impacted files and assess complexity:

- **File count**: How many files need changes?
- **Coupling**: Are changes isolated or cross-cutting?
- **Unknowns**: How many open questions exist?
- **Testing**: What test coverage is needed?

### Step 4: Analyze Delegation Opportunities

**Delegation is the default.** Before making a routing decision, analyze whether the task can be decomposed into independent subtasks for parallel subagent execution:

**Always delegate when**:

- Task has 2+ independent components that can run in parallel
- Exploration/research is needed before implementation
- Multiple files need changes that don't depend on each other
- Code review, security review, or testing can run in parallel

**Delegation analysis checklist**:

1. Can parts of this work run independently? → Dispatch parallel subagents
2. Is exploration needed first? → Dispatch Explore subagent before deciding scope
3. Are there isolated concerns? → Dispatch specialized subagents (impl, test, review)
4. Would main-context benefit from delegation? → Always yes for non-trivial tasks

**Do NOT delegate only when**:

- Single-file typo/config fix (oneoff-vibe)
- Task requires tight coordination that subagents can't provide
- User explicitly requests direct execution

### Step 5: Make Routing Decision

Produce a routing decision with delegation plan:

```yaml
workflow: oneoff-vibe | oneoff-spec | orchestrator | refactor | journal-only
rationale: <Brief explanation of why this workflow was chosen>
estimated_scope: small | medium | large
estimated_files: <N>
delegation:
  parallel_subtasks:
    - <subtask 1>: <subagent type>
    - <subtask 2>: <subagent type>
  sequential_dependencies:
    - <subtask that must complete first>
  exploration_needed: true | false
  investigation_required: true | false # MANDATORY true for orchestrator
workstreams:
  - <workstream 1> (for orchestrator only)
  - <workstream 2>
investigation_scope: <spec-group-id | master-spec-id | null>
next_action: <Suggested next step>
```

**Investigation rules**:

- `orchestrator`: Investigation is MANDATORY before implementation
- `oneoff-spec`: Investigation recommended if spec has dependencies or references existing systems
- `oneoff-vibe`, `refactor`, `journal-only`: Investigation typically not needed

### Step 6: Persist Decision

Save routing decision to session state:

```bash
# Append to session context
echo "{\"timestamp\": \"$(date -Iseconds)\", \"workflow\": \"oneoff-spec\", \"rationale\": \"...\"}" >> .claude/context/session.json
```

**For non-trivial workflows (oneoff-spec, orchestrator, refactor)**, initialize active work tracking:

```bash
# Start work tracking for spec-based workflows
# <spec_group_id> is generated during routing (e.g., "logout-button-20260121")
# <workflow> is the routing decision (oneoff-spec, orchestrator, refactor)
# <objective> is a brief description of the user's request
node .claude/scripts/session-checkpoint.mjs start-work <spec_group_id> <workflow> "<objective>"
```

This enables resume detection (Step 0) if the session is interrupted.

**Example**:

```bash
node .claude/scripts/session-checkpoint.mjs start-work "logout-button-20260121" "oneoff-spec" "Add logout button to the user dashboard"
```

**Note**: Skip work tracking for oneoff-vibe and journal-only workflows as they complete in a single session.

## Edge Cases

### Ambiguous Complexity

When uncertain about task size:

- **Default to oneoff-spec** — specs are cheap, debugging without specs is expensive
- If task seems trivial but has any ambiguity → oneoff-spec
- Can escalate to orchestrator if spec reveals hidden complexity
- Better to "over-spec" a simple task than "under-spec" a complex one

### User Override

If user explicitly requests a workflow:

- "Just do it", "vibe", "quick fix", "skip spec" → oneoff-vibe (honor request, note in rationale)
- "Write a full spec first" → oneoff-spec or orchestrator
- User preference always wins, but default assumption is: user wants quality (specs)

### Existing Spec Group

If `.claude/specs/groups/<spec-group-id>/manifest.json` exists:

- Check `review_state` and `work_state` fields in manifest
- **review_state**:
  - `DRAFT` → Continue spec authoring or atomization
  - `REVIEWED` → Awaiting user approval
  - `APPROVED` → Route to implementation
- **work_state**:
  - `PLAN_READY` → Ready for implementation
  - `IMPLEMENTING` → Continue implementation
  - `VERIFYING` → Run unify validation
  - `READY_TO_MERGE` → Proceed to code review, security review

## Output Format

Always output a clear routing decision:

```markdown
## Routing Decision

**Workflow**: oneoff-spec

**Rationale**: This task involves adding a new API endpoint with authentication, requiring changes to 3-4 files (route handler, service layer, tests). The scope is well-defined but needs formal requirements and test planning.

**Estimated Scope**: medium

**Estimated Files**: 4 (controller, service, tests, types)

**Next Action**: Use `/pm` skill to interview user about endpoint requirements, then create TaskSpec.
```

For refactor workflows, include behavior preservation note:

```markdown
## Routing Decision

**Workflow**: refactor

**Rationale**: Explicit refactoring request to migrate to repository pattern. No behavior changes - code reorganization only.

**Estimated Scope**: medium

**Estimated Files**: 4 (service, repository, interface, tests)

**Behavior Preservation**: Tests must pass before and after refactoring.

**Next Action**: Use `/refactor` skill to define scope and patterns.
```

For journal-only workflows, specify the journal type:

```markdown
## Routing Decision

**Workflow**: journal-only

**Rationale**: Investigation into memory leak is complete. Findings (root cause in event listener cleanup) should be documented for future reference.

**Journal Type**: investigation

**Next Action**: Create investigation journal documenting the findings and resolution.
```

For architectural decisions, use the decision-record template:

```markdown
## Routing Decision

**Workflow**: journal-only

**Rationale**: Team decided to use Redis for session storage over PostgreSQL. This architectural decision should be recorded with rationale and trade-offs.

**Journal Type**: decision-record

**Next Action**: Create decision record using `.claude/templates/decision-record.template.md`.
```

## Integration with Other Skills

After routing:

- **oneoff-vibe**: Proceed directly to implementation
- **oneoff-spec**: Use `/pm` to gather requirements → (optional) `/prd draft` to write PRD to Google Docs → `/spec` to create spec group → `/atomize` to create atomic specs → `/enforce` to validate atomicity → [If spec has dependencies: `/investigate` to surface cross-spec inconsistencies] → User approval → `/implement` + `/test` → `/unify` → `/code-review` → `/security` → (if PRD exists) `/prd push` to sync discoveries
- **orchestrator**: Use `/pm` to create ProblemBrief → (optional) `/prd draft` for stakeholder PRD → `/spec` to create MasterSpec with workstream spec groups → For each workstream: `/atomize` + `/enforce` → **MANDATORY: `/investigate` to surface cross-workstream inconsistencies** → Resolve decisions → User approval → Facilitator orchestrates parallel execution → `/prd push` to sync discoveries
- **refactor**: Use `/refactor` skill → Define scope and patterns → Run tests (baseline) → Execute refactoring → Run tests (verification) → `/code-review` → `/security` (if applicable)
- **journal-only**: Create appropriate journal entry → For decisions: use decision-record template at `.claude/templates/decision-record.template.md` → For investigations: document findings, root cause, resolution → For hotfixes: document fix, root cause, prevention measures → Store in `.claude/journals/` directory

### Investigation Checkpoint

The `/investigate` skill surfaces inconsistencies that would otherwise become runtime bugs:

- **Env var naming**: GIT_SSH_KEY_PATH vs GIT_SSH_KEY_BASE64 conflicts
- **API contracts**: Hardcoded URLs vs discovery patterns, path inconsistencies
- **Data shapes**: Field naming conventions, required vs optional mismatches
- **Deployment assumptions**: CDK vs Terraform, SSM vs .env conflicts
- **Missing fields**: Template completeness across workstreams

For orchestrator workflows, investigation is MANDATORY before implementation. For oneoff-spec, it's recommended when the spec references existing systems or has declared dependencies.

## Examples

### Example 1: Truly Trivial (oneoff-vibe)

**Request**: "Fix the typo in README.md line 42: 'teh' should be 'the'"

**Routing**:

- workflow: oneoff-vibe
- rationale: Single character fix, zero ambiguity, no behavioral impact
- estimated_scope: trivial
- delegation: none
- next_action: Make the edit directly

### Example 2: Seems Simple But Gets Spec (oneoff-spec)

**Request**: "Add a loading spinner to the submit button"

**Routing**:

- workflow: oneoff-spec
- rationale: Seems simple but has decisions: spinner placement, when to show/hide, error states, accessibility. Spec ensures we don't miss edge cases.
- estimated_scope: small-medium
- estimated_files: 2-3 (component, styles, tests)
- delegation:
  - parallel_subtasks:
    - implementation: implementer
    - tests: test-writer
- next_action: Use `/pm` to clarify loading states and error handling

### Example 3: Standard Feature (oneoff-spec)

**Request**: "Add a logout button to the user dashboard"

**Routing**:

- workflow: oneoff-spec
- rationale: Requires UI component, event handler, API call, state management. Need to clarify placement, behavior on logout, error handling.
- estimated_scope: medium
- estimated_files: 4 (component, handler, API client, tests)
- delegation:
  - parallel_subtasks:
    - implementation: implementer
    - tests: test-writer
  - sequential_dependencies:
    - spec approval must complete before implementation
- next_action: Use `/pm` to gather UI/UX requirements

### Example 4: Large Task (Full Orchestration)

**Request**: "Implement real-time notifications across the application"

**Routing**:

- workflow: orchestrator
- rationale: Cross-cutting feature affecting multiple layers: WebSocket server, frontend client, database schema, auth middleware, notification service (8+ files, 3+ workstreams)
- estimated_scope: large
- workstreams:
  - ws-1: WebSocket server infrastructure
  - ws-2: Frontend notification client
  - ws-3: Notification persistence and delivery
- delegation:
  - parallel_subtasks:
    - ws-1 implementation: implementer (worktree)
    - ws-2 implementation: implementer (worktree)
    - ws-3 implementation: implementer (worktree)
    - per-workstream tests: test-writer (parallel)
  - sequential_dependencies:
    - ws-1 must complete before ws-2 (client depends on server)
  - exploration_needed: true (investigate WebSocket library options)
  - investigation_required: true (MANDATORY for orchestrator - surface cross-workstream conflicts before implementation)
- next_action: Use `/pm` to create ProblemBrief, dispatch Explore subagent for WebSocket research

### Example 4b: Orchestrator with Investigation Findings

**Request**: "Build deployment pipeline with build, deploy, and monitoring workstreams"

**Routing**:

- workflow: orchestrator
- rationale: Multi-workstream infrastructure project with 3 distinct concerns that will share env vars, secrets, and container conventions
- estimated_scope: large
- workstreams:
  - ws-build: CI build pipeline
  - ws-deploy: Deployment automation
  - ws-monitor: Monitoring and alerting
- delegation:
  - parallel_subtasks:
    - workstream specs: spec-author (parallel)
  - sequential_dependencies:
    - After specs complete: `/investigate ms-deployment-pipeline` (MANDATORY)
    - Investigation must complete before approval
    - Any blocker decisions must be resolved before implementation
  - investigation_required: true
- next_action: Use `/pm` to gather requirements, create MasterSpec

**Post-Investigation (example)**:

After `/investigate ms-deployment-pipeline`:

```
Issues Found:
  - BLOCKER: ws-monitor missing HMAC_SECRET, LOG_LEVEL from ws-build template
  - HIGH: GIT_SSH_KEY_PATH (ws-build) vs GIT_SSH_KEY_BASE64 (ws-deploy) conflict
  - HIGH: Container image format inconsistency

Decisions Required:
  - DEC-001: SSH key variable naming
  - DEC-002: Container image format
  - DEC-003: Required env vars set
```

User must resolve decisions before implementation proceeds.

### Example 5: Exploration-First (Delegation for Research)

**Request**: "Improve performance of the search feature"

**Routing**:

- workflow: oneoff-spec (may escalate to orchestrator)
- rationale: Requires investigation to understand bottlenecks before planning
- estimated_scope: unknown (pending exploration)
- delegation:
  - exploration_needed: true
  - parallel_subtasks:
    - codebase analysis: Explore subagent
    - performance profiling: Explore subagent (separate)
  - sequential_dependencies:
    - exploration must complete before spec authoring
- next_action: Dispatch Explore subagent to profile current search implementation

### Example 6: User Requests Vibe (Override)

**Request**: "Just add a console.log to debug this, don't need a spec"

**Routing**:

- workflow: oneoff-vibe
- rationale: User explicitly requested to skip spec ("don't need a spec"). Honoring user preference.
- estimated_scope: trivial
- delegation: none
- next_action: Make the change directly

**Note**: Without the explicit override, even a "simple" debug statement might warrant a spec if it's part of a larger investigation.

### Example 7: Refactor Request (refactor workflow)

**Request**: "Refactor the authentication service to use the repository pattern"

**Routing**:

- workflow: refactor
- rationale: Explicit refactoring request with pattern migration goal. No behavior changes expected - restructuring code organization only.
- estimated_scope: medium
- estimated_files: 3-5 (service, new repository, tests)
- delegation:
  - exploration_needed: true (understand current auth service structure)
  - parallel_subtasks:
    - codebase analysis: Explore subagent
  - sequential_dependencies:
    - exploration must complete before refactoring
    - tests must pass before refactoring (baseline)
    - tests must pass after refactoring (verification)
- next_action: Use `/refactor` skill to define scope and execute

### Example 8: Tech Debt Reduction (refactor workflow)

**Request**: "Clean up the utils folder - too much duplicated code"

**Routing**:

- workflow: refactor
- rationale: Tech debt reduction request focused on code consolidation. "Clean up" and "duplicated code" are refactor triggers. No feature changes.
- estimated_scope: small-medium
- estimated_files: 4-8 (multiple utils files to consolidate)
- delegation:
  - exploration_needed: true (identify duplication patterns)
  - parallel_subtasks:
    - duplication analysis: Explore subagent
- next_action: Use `/refactor` skill to identify duplications and consolidate

### Example 9: Refactor with Feature (routes to oneoff-spec, NOT refactor)

**Request**: "Refactor the payment service and add support for crypto payments"

**Routing**:

- workflow: oneoff-spec
- rationale: Although request includes "refactor", it also adds new behavior (crypto payments). Behavior changes require spec workflow for proper requirements and testing. The refactor portion can be part of implementation.
- estimated_scope: medium-large
- estimated_files: 5+
- delegation:
  - parallel_subtasks:
    - implementation: implementer
    - tests: test-writer
- next_action: Use `/pm` to gather crypto payment requirements, then create TaskSpec

**Note**: Mixed requests (refactor + feature) always route to oneoff-spec because behavior changes need formal specification.

### Example 10: Investigation Complete (journal-only)

**Request**: "I just spent an hour debugging why the cache was stale. Found that Redis TTL was being set incorrectly. Document this for the team."

**Routing**:

- workflow: journal-only
- rationale: Investigation is complete, work is done. Findings are valuable for future developers who might encounter similar issues.
- journal_type: investigation
- delegation: none
- next_action: Create investigation journal documenting the Redis TTL issue, root cause, and fix applied

### Example 11: Architectural Decision (journal-only with decision-record)

**Request**: "We decided to use WebSockets instead of polling for real-time updates. Record this decision."

**Routing**:

- workflow: journal-only
- rationale: Architectural decision has been made. Should be recorded with rationale and trade-offs for future reference.
- journal_type: decision-record
- delegation: none
- next_action: Create decision record using `.claude/templates/decision-record.template.md` documenting WebSocket vs polling decision

### Example 12: Hotfix Documentation (journal-only)

**Request**: "Just pushed a hotfix for the auth bug in production. Need to document what happened."

**Routing**:

- workflow: journal-only
- rationale: Emergency fix is complete. Root cause analysis and documentation valuable for preventing recurrence.
- journal_type: hotfix
- delegation: none
- next_action: Create hotfix journal documenting the incident, root cause, fix applied, and prevention measures

### Example 13: NOT Journal-Only (needs spec)

**Request**: "Found a bug during investigation. Want to fix it and document the fix."

**Routing**:

- workflow: oneoff-spec
- rationale: "Fix it" indicates future work, not documentation of completed work. Bug fixes need acceptance criteria even when simple.
- estimated_scope: small
- next_action: Use `/pm` to clarify bug behavior and expected fix, then create TaskSpec

**Note**: Journal-only is for documenting **completed** work. If work remains to be done (fix, implement, change), use a spec workflow.
