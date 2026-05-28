# Lane: Planning

Detailed reference for the Planning lane in Kyora Agent OS.

## Entry Conditions

Start in Planning when:

- Risk is medium or high
- Scope is cross-stack (backend + portal)
- Large refactor needed
- UX changes involved
- Multiple feature areas touched

## Owner

- **Primary**: Relevant Domain Lead (Backend Lead, Web Lead, etc.)
- **Supporting**: Other affected Leads (for cross-stack), Orchestrator (for routing)

## Outputs (Required)

1. **Phased plan** — Independently verifiable phases
2. **Acceptance checks** — What must be true for each phase to be "done"
3. **Gates** — What requires PO approval
4. **Contract (cross-stack)** — Endpoint, DTO, error semantics, i18n copy

## Definition of Done

- All phases are independently verifiable
- Contracts and boundaries are explicit
- Gates identified and listed
- Token-efficient (compact plan, SSOT links instead of copies)

## Phase Slicing Rules

Split into phases if any apply:

- Cross-stack work
- More than 2 feature areas touched
- High-risk axis involved
- Work likely exceeds a single session

### Standard Phase Template (Cross-Stack)

| Phase | Focus | DoD |
|-------|-------|-----|
| Phase 0 | Contract agreement + locate reuse targets | Endpoint/DTO/error shapes agreed; SSOT patterns identified |
| Phase 1 | Backend implementation + tests | Endpoint works; tests pass; OpenAPI updated |
| Phase 2 | Portal integration + UI + i18n | API wired; UI states complete; i18n keys present |
| Phase 3 | Cleanup + E2E + consistency | Dead code removed; RTL verified; E2E smoke green |

**Critical rule**: Never mix "new behavior" + "large refactor" in the same phase unless PO explicitly approves.

## Cross-Stack Coordination

If Backend + Web both involved:

1. **Phase 0 is mandatory** — Leads must agree contract BEFORE implementation
2. **Contract includes**:
   - Endpoint path and method
   - Request/response DTO shape
   - Error semantics (status codes, error codes, messages)
   - Required i18n keys (new user-facing copy)
3. **Both Leads sign off** on contract before Phase 1 starts

## Token Playbook

1. **Keep plan compact**: Use tables and bullets, not prose
2. **Link SSOT files**: Don't copy rules, reference them
3. **Anchor to quality gates**: Reference section 6 gates in KYORA_AGENT_OS.md
4. **Use existing patterns**: Search for similar implementations first

## Tool Allowlist

| Tool | When to Use |
|------|-------------|
| `read` | Read specs, existing implementations |
| `search` | Find patterns to reuse |
| `Context7` | Verify third-party API usage (if new library) |

**Forbidden**: `edit` (except for plan/notes), `execute`

## Output Format: Plan

```
PLANNING OUTPUT

Objective:
-

Classification:
- Type:
- Scope:
- Risk:

Contract (cross-stack only):
- Endpoint:
- DTO shape:
- Error semantics:
- i18n keys needed:

Plan:
- Phase 0: [objective] — DoD: [criteria]
- Phase 1: [objective] — DoD: [criteria]
- Phase 2: [objective] — DoD: [criteria]

Reuse targets:
- Backend patterns:
- Portal patterns:
- Existing components:

Gates (PO approval required):
-

Validation per phase:
- Phase 1:
- Phase 2:

SSOT references:
-
```

## Common Failure Modes

| Failure | Prevention |
|---------|------------|
| Plan too large | Split into smaller phases |
| Copying SSOT rules | Link instead of copy |
| Missing cross-stack contract | Enforce Phase 0 agreement |
| Vague DoD per phase | Make each phase independently verifiable |
| Skipping reuse check | Always search for existing patterns first |

## Escalation Triggers

Escalate to PO if:

- Schema changes or migrations needed
- New dependency required
- Breaking API contract
- Auth/RBAC/tenant boundary touched
- Major UX redesign
