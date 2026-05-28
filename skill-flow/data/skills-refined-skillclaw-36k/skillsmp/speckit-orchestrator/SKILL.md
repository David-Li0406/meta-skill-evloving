---
name: speckit-orchestrator
description: Intelligent workflow orchestrator that analyzes user requirements, recommends an appropriate workflow, and executes speckit agents in sequence.
---

# Speckit Orchestrator

Analyzes complexity, recommends workflow, executes agents with checkpoints and feedback loops.

## Execution Flow

1. **Pre-Flight** → Check git, tools, constitution
2. **Workflow Selection** → Score complexity, recommend, confirm
3. **Planning Phase** → Run spec/plan agents
4. **🛑 Checkpoint** → Require user approval before implementation
5. **Implementation** → Run implement/test/review/e2e
6. **Summary** → Report results

---

## Agents

| Agent | Type | Purpose |
|-------|------|---------|
| specify | speckit-specify | Create spec from request |
| clarify | speckit-clarify | Resolve ambiguities |
| research | speckit-research | Fetch docs (Context7/web) |
| plan | speckit-plan | Generate implementation plan |
| checklist | speckit-checklist | Create validation checklist |
| tasks | speckit-tasks | Generate ordered tasks |
| analyze | speckit-analyze | Cross-artifact validation |
| implement | speckit-implement | Execute tasks (TDD) |
| test | speckit-test | Quality gate |
| review | speckit-review | Cleanup (files, duplicates) |
| e2e-test-builder | speckit-e2e-test-builder | Create E2E tests |
| e2e-test-fixer | speckit-e2e-test-fixer | Fix E2E failures |
| taskstoissues | speckit-taskstoissues | Convert to GitHub issues |

---

## Workflow Selection

### Complexity Scoring (0-3 each)

| Factor | 0 | 1 | 2 | 3 |
|--------|---|---|---|---|
| Scope | Single file | Module | Multi-module | Cross-service |
| Integration | None | Internal | External API | Multi-service |
| Risk | Experimental | Dev | Prod non-critical | Prod critical |
| Novelty | Existing | Variation | New feature | Novel arch |

**Score → Workflow**: 0-3=Simple, 4-6=Standard, 7-9=Full, 10+=Full+Research

### Workflows

| Workflow | Sequence |
|----------|----------|
| Simple | specify → 🛑 → implement → test |
| Standard | specify → clarify → plan → tasks → 🛑 → implement → test |
| Standard+E2E | ...tasks → 🛑 → implement → test → review → e2e-builder → e2e-fixer |
| Full | ...checklist → tasks → analyze → 🛑 → implement → test → review → e2e → taskstoissues |
| Full+Research | specify → clarify → research → plan → ...Full |

### Triggers

| Trigger | Action |
|---------|--------|
| `simple: [feature]` | Force Simple workflow |
| `full: [feature]` | Force Full workflow |
| `spec: [feature]` | specify → clarify only |
| `plan: [feature]` | ...→ plan → checklist → tasks → analyze |
| `implement` | 🛑 → implement → test → review |
| `e2e: [feature]` | e2e-builder → e2e-fixer |
| `issues` | taskstoissues only |

---

## Agent Context

Every agent receives:

```
WORKFLOW_CONTEXT:
  workflow_id: <uuid>
  feature_id: <id>
  feature_dir: specs/<id>/
  previous_results: { <agent>: { status, ... } }

USER_REQUEST: <original>

RESPONSE_FORMAT:
Success: {"agent":"<name>","status":"success","timestamp":"<ISO>","result":{...,"next_steps":[...]}}
Error: {"agent":"<name>","status":"error","timestamp":"<ISO>","error":{"type":"<Type>","message":"<msg>","recoverable":bool,"recovery_strategy":"<strategy>"}}

Error types: PrerequisiteError, ValidationError, QualityGateFailure, ConstitutionViolationError
Recovery: run_prerequisite_agent, feedback_loop, fix_and_retry, ask_user, manual_resolution
```

---

## 🛑 Checkpoint (Mandatory)

Before ANY implementation, require explicit user confirmation.

**Output**:
```
## 🛑 Pre-Implementation Checkpoint

Artifacts: spec.md, plan.md, tasks.md (X tasks)
Scope: X files to create, X to modify, ~X LOC

Type: proceed | review <artifact> | abort | pause
```

**Responses**: `proceed/yes` → implement | `review X` → show | `abort` → cancel | `pause` → save state

---

## Error Recovery

| Error | Strategy | Retries |
|-------|----------|---------|
| PrerequisiteError | Auto-run missing agent | 1 |
| ValidationError | Invoke clarify | 1 |
| QualityGateFailure | Feedback to source | 2 |
| TestValidationError | Re-run implement | 2 |
| TimeoutError | Retry | 1 |
| UnrecoverableError | Stop | 0 |

---

## Feedback Loops

Quality gates route issues back to source agents.

| Source | Target | Issues |
|--------|--------|--------|
| analyze | specify/clarify | Spec gaps, unclear reqs |
| analyze | plan | Architecture gaps |
| analyze | tasks | Coverage gaps, dependencies |
| test | implement | Test failures, coverage |
| review | implement | Constitution violations |

**Feedback Context**:
```
FEEDBACK_CONTEXT:
  feedback_from: <agent>
  iteration: N
  max_iterations: 3
  issues_to_fix: [{ severity, type, message, location, recommendation }]
```

**Limits**: analyze→spec/plan/tasks: 2 | test→implement: 2 | review→implement: 1

---

## E2E Testing

**Auto-added when**: Cross-service reqs, integration-heavy, or user requests `e2e:`

**Flow**: implement → test → review → e2e-builder → e2e-fixer (max 3 iterations)

**Fixer decisions**:
- TEST_BUG → Fix test
- SPEC_MISMATCH → Update spec + test
- IMPLEMENTATION_BUG (simple ≤3) → Fix in fixer
- IMPLEMENTATION_BUG (complex >3) → Return to implement

---

## State Persistence

`.specify/workflow-state/<id>.json`:
```json
{
  "workflow_id": "<uuid>",
  "workflow_type": "standard",
  "agents_to_execute": [...],
  "completed_agents": [...],
  "current_agent": "<name>",
  "status": "running|awaiting_approval|complete"
}
```

Resume: `orchestrator resume <id>` or `resume`

---

## Usage

```bash
orchestrator: Add OAuth2 auth     # Auto-recommend
simple: Add logging               # Force simple
full: Payment processing          # Force full
spec: WebSocket service           # Spec only
implement                         # Tasks only
e2e: Health monitoring            # E2E only
```
