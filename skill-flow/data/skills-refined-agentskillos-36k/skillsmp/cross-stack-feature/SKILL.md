---
name: cross-stack-feature
description: 'Phase-sliced workflow for cross-stack features (backend + portal). Use when implementing features that span both backend API and portal-web UI. Triggers: cross-stack, backend + portal, endpoint + UI, API + frontend, full-stack feature, Phase 0 contract.'
---

# Cross-Stack Feature Workflow

Structured workflow for implementing features that span both `backend/` and `portal-web/`. Enforces phase slicing, contract agreement, and handoff packets between phases.

## When to Use This Skill

- New feature touching both backend API and portal UI
- Cross-stack bug fix
- Refactor affecting API contracts and frontend consumers
- Any work classified as `scope: cross-stack`

## Prerequisites

- Backend Lead and Web Lead available for Phase 0 agreement
- Access to both `backend/` and `portal-web/` codebases
- Familiarity with [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md) phase slicing rules

## Phase Structure (Mandatory)

| Phase | Focus | Owner | DoD |
|-------|-------|-------|-----|
| Phase 0 | Contract Agreement | Backend Lead + Web Lead | Endpoint/DTO/error/i18n agreed |
| Phase 1 | Backend Implementation | Backend Implementer | API works; tests pass; OpenAPI updated |
| Phase 2 | Portal Integration | Web Implementer | API wired; UI states complete; i18n present |
| Phase 3 | Cleanup + E2E | QA + Implementers | Dead code removed; RTL verified; E2E green |

**Critical Rule**: Never mix "new behavior" + "large refactor" in the same phase unless PO explicitly approves.

## Phase 0: Contract Agreement (Mandatory for Cross-Stack)

Before ANY implementation begins, Backend Lead and Web Lead must agree on:

### Contract Elements

1. **Endpoint**
   - Path: `/api/v1/...`
   - Method: GET/POST/PUT/PATCH/DELETE
   - Auth required: yes/no

2. **Request DTO**
   - Required fields
   - Optional fields
   - Validation rules

3. **Response DTO**
   - Success shape
   - Pagination (if list)
   - Included relations

4. **Error Semantics**
   - HTTP status codes
   - Error code enum values
   - Error message keys

5. **i18n Keys**
   - New user-facing strings
   - Error message keys
   - UI label keys

### Phase 0 Output

```
PHASE 0 CONTRACT

Feature:
Date:
Backend Lead:
Web Lead:

Endpoint:
- Path:
- Method:
- Auth:

Request DTO:
```typescript
interface RequestDTO {
  // fields
}
```

Response DTO:
```typescript
interface ResponseDTO {
  // fields
}
```

Error Semantics:
- 400: validation errors (code: VALIDATION_ERROR)
- 404: not found (code: NOT_FOUND)
- ...

i18n Keys Needed:
- label_key: "English" / "Arabic"
- ...

Agreement:
- [ ] Backend Lead approved
- [ ] Web Lead approved
```

## Phase 1: Backend Implementation

### Entry

- Phase 0 contract agreed and signed off

### Outputs

1. Endpoint implementation
2. DTOs matching contract
3. Unit tests
4. OpenAPI update (if repo requires)

### Validation Commands

```bash
make test.quick          # Unit tests
make openapi.check       # OpenAPI alignment
make test                # Full test suite (if touching shared code)
```

### DoD

- [ ] Endpoint returns correct response shape
- [ ] Validation errors follow contract
- [ ] Tests cover happy path + key error cases
- [ ] OpenAPI updated (if required)
- [ ] No dead code or TODOs

### Phase 1 Handoff

Create Phase Handoff Packet before proceeding to Phase 2.

## Phase 2: Portal Integration

### Entry

- Phase 1 complete with handoff packet
- Backend endpoint deployed or running locally

### Outputs

1. API client function in `portal-web/src/api/`
2. TanStack Query hook (query or mutation)
3. UI component with all states
4. i18n keys in both locales

### Validation Commands

```bash
make portal.check        # Lint + typecheck
make portal.build        # Build succeeds
```

### DoD

- [ ] API client matches contract
- [ ] Query/mutation handles loading/error states
- [ ] UI handles loading/empty/error states
- [ ] RTL layout verified
- [ ] i18n keys present in ar + en
- [ ] Uses existing components (no new primitives)
- [ ] No hardcoded UI strings

### Phase 2 Handoff

Create Phase Handoff Packet before proceeding to Phase 3.

## Phase 3: Cleanup + E2E

### Entry

- Phase 2 complete with handoff packet
- Feature functional end-to-end

### Outputs

1. Dead code removed
2. Consistency pass (tokens, patterns)
3. E2E smoke test (if applicable)
4. RTL verification

### Validation Commands

```bash
make test                # Full backend tests
make portal.build        # Portal builds clean
# E2E if applicable
```

### DoD

- [ ] No commented-out code
- [ ] No unused exports/files
- [ ] No TODO/FIXME placeholders
- [ ] RTL-safe layout confirmed
- [ ] E2E smoke passes (if applicable)

## Quality Gates Reference

See [Quality Gates](./references/quality-gates.md) for detailed checklists per area.

## Success Checklist (Overall)

- [ ] Phase 0 contract agreed before implementation
- [ ] Phase Handoff Packet created after each phase
- [ ] No new behavior + large refactor mixed
- [ ] All phase DoDs met
- [ ] Validation commands green
- [ ] No surprise docs generated
- [ ] Stop-and-ask triggers checked (see quality-gates)

## Stop-and-Ask Triggers

**MUST ask PO before proceeding** if any are true:

- Schema changes or migrations needed
- New dependency required
- Breaking API contract
- Auth/RBAC/tenant boundary touched
- Major UX redesign implied

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Phase 0 skipped | Urgency or oversight | Stop, get Lead agreement before continuing |
| Contract mismatch | Leads didn't align on DTO/errors | Revisit Phase 0, update contract |
| Phase 2 blocked by Phase 1 | Backend not ready | Wait for Phase 1 handoff packet |
| RTL layout broken | `left`/`right` used instead of `start`/`end` | Fix per frontend/_general/ui-patterns.instructions.md |
| i18n keys missing | Copy added without translation | Add keys to both ar/ and en/ locales |

## Validation Commands Summary

```bash
# Phase 1 (Backend)
make test.quick
make openapi.check

# Phase 2 (Portal)
make portal.check
make portal.build

# Phase 3 (Full)
make test
make portal.build
```

## SSOT References

Do not duplicate; link instead:

- Phase slicing: [KYORA_AGENT_OS.md#L547-L575](../../../KYORA_AGENT_OS.md#L547-L575)
- Cross-stack coordination: [KYORA_AGENT_OS.md#L382-L395](../../../KYORA_AGENT_OS.md#L382-L395)
- Quality gates: [KYORA_AGENT_OS.md#L701-L789](../../../KYORA_AGENT_OS.md#L701-L789)
- Backend SSOT: [backend-core.instructions.md](../../instructions/backend-core.instructions.md)
- Portal SSOT: [frontend/projects/portal-web/architecture.instructions.md](../../instructions/frontend/projects/portal-web/architecture.instructions.md)
