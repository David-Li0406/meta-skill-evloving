# Quality Gates Reference

Consolidated quality gates for cross-stack features. These gates prevent common failure modes: inconsistency, wrong assumptions, partial completion, and drift.

**Important**: This file links to SSOT instruction files. Do not duplicate their rules here.

## Gate 1: No Surprise Docs

- If user did not ask for docs: do not create or expand docs/README/long summaries

## Gate 2: No Dead Code

- No commented-out blocks
- No unused exports
- No unused files
- No TODO/FIXME placeholders

## Gate 3: UI Consistency (Portal)

**SSOT References**:
- [frontend/_general/ui-patterns.instructions.md](../../instructions/frontend/_general/ui-patterns.instructions.md)
- [kyora/design-system.instructions.md](../../instructions/kyora/design-system.instructions.md)
- [kyora/ux-strategy.instructions.md](../../instructions/kyora/ux-strategy.instructions.md)

### Checklist

- [ ] Uses existing components/patterns (no new primitives by default)
- [ ] RTL-safe layout and spacing (use `start`/`end` not `left`/`right`)
- [ ] Loading/empty/error states exist
- [ ] Copy is simple and non-technical

### Reuse-First Verification

Before building a new component/pattern:

1. Search `portal-web/src/components/` for existing components
2. Search `portal-web/src/features/` for feature-specific patterns
3. Search `portal-web/src/api/` for similar API calls

## Gate 4: Forms

**SSOT Reference**: [frontend/_general/forms.instructions.md](../../instructions/frontend/_general/forms.instructions.md)

### Checklist

- [ ] Uses the project form system (TanStack Form + useKyoraForm)
- [ ] Validation errors shown consistently
- [ ] Submit/disabled/server errors handled
- [ ] Field pattern used: `<form.AppField>` + `{(field) => <field.Component />}`

## Gate 5: i18n

**SSOT Reference**: [frontend/_general/i18n.instructions.md](../../instructions/frontend/_general/i18n.instructions.md)

### Checklist

- [ ] No hardcoded UI strings
- [ ] Keys exist in both `ar/` and `en/` locales
- [ ] Arabic phrasing is natural + consistent with domain language
- [ ] No accounting jargon in UI copy

## Gate 6: Backend API Contract

**SSOT References**:
- [backend-core.instructions.md](../../instructions/backend-core.instructions.md)
- [errors-handling.instructions.md](../../instructions/errors-handling.instructions.md)
- [responses-dtos-swagger.instructions.md](../../instructions/responses-dtos-swagger.instructions.md)

### Checklist

- [ ] Inputs validated
- [ ] Tenant isolation enforced (workspace > business)
- [ ] Errors follow Kyora Problem/RFC7807 patterns
- [ ] DTOs/OpenAPI aligned (per repo norms)

### Reuse-First Verification

Before adding a new pattern/util:

1. Search `backend/internal/platform/utils/`
2. Search related domain modules
3. Prefer existing domain boundaries: domain in `domain/**`, infra in `platform/**`

## Gate 7: Cross-Stack Alignment

### Checklist

- [ ] Backend endpoint + portal API client agree on request/response
- [ ] Error semantics handled in UI (per HTTP layer SSOT)
- [ ] i18n keys added for new user-facing text
- [ ] Phase 0 contract was agreed before implementation

## Gate 8: Testing

### Checklist

- [ ] Run the smallest relevant test suite
- [ ] Add/adjust tests where natural
- [ ] Don't fix unrelated failures

### Validation Commands

```bash
# Backend
make test.quick        # Unit tests (fast)
make test              # All tests
make openapi.check     # OpenAPI alignment

# Portal
make portal.check      # Lint + typecheck
make portal.build      # Build succeeds

# Full validation
make doctor            # Tooling sanity
```

## Gate 9: Security Non-Negotiables

**Critical**: These ALWAYS require extra review.

- [ ] Tenant isolation maintained (no cross-workspace/cross-business access)
- [ ] Auth/RBAC checked for protected endpoints
- [ ] No secrets in code or logs
- [ ] PII handled per privacy requirements

If any of these are touched: involve Security/Privacy Reviewer.

## Gate 10: Stop-and-Ask Triggers

**MUST ask PO before proceeding** if any are true:

- Acceptance criteria missing and behavior ambiguous
- Schema changes or migrations needed
- New dependency needed
- Breaking API contract or major UX redesign implied
- Auth/RBAC/tenant boundary touched

## Summary Table

| Gate | When to Check | Validation |
|------|---------------|------------|
| No Surprise Docs | Always | Manual review |
| No Dead Code | Phase 3 | Code review |
| UI Consistency | Phase 2-3 | `make portal.check` + manual |
| Forms | Phase 2 | `make portal.check` |
| i18n | Phase 2 | Check locale files |
| Backend Contract | Phase 1 | `make test.quick` + `make openapi.check` |
| Cross-Stack Alignment | Phase 2 | Compare DTOs |
| Testing | Phase 1-3 | `make test` / `make portal.build` |
| Security | All phases | Manual review + Security Reviewer |
| Stop-and-Ask | Pre-implementation | Check triggers |
