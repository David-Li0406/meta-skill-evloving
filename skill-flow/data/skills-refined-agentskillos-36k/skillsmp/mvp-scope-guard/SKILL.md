---
name: mvp-scope-guard
description: Prevents MVP scope creep based on this project's constraints. Use during early design.
triggers: [mvp-definition, feature-discussions]
outputs: [scope-decision, deferred-features]
depends_on: [project-vision-normalizer]
---

# MVP Scope Guard

## Purpose

Prevents **scope creep during MVP development** by rigorously evaluating every feature against MVP goals. Features that don't serve the core learning objective are deferred.

---

## When to Use

- MVP definition phase
- Feature discussions
- When stakeholders request additions
- During planning reviews

---

## Instructions

### 1. Validate Feature Against MVP Goals

```markdown
## Feature Evaluation: Social Login

**MVP Goal:** Validate core authentication flow

**Questions:**
- Does this help us learn? ❌ No - nice-to-have
- Is this required for core flow? ❌ No - email login sufficient
- Does this block user testing? ❌ No

**Decision:** DEFER to Phase 2
```

### 2. Reject Non-Essential Features

| Feature | Essential? | Decision |
|---------|------------|----------|
| Email login | ✅ Yes | INCLUDE |
| Password reset | ✅ Yes | INCLUDE |
| Social login | ❌ No | DEFER |
| Admin dashboard | ⚠️ Maybe | SIMPLIFY |

### 3. Tag Deferred Ideas Explicitly

```markdown
## Deferred Features (Post-MVP)

| Feature | Reason | Phase |
|---------|--------|-------|
| Social login | Not essential for validation | 2 |
| MFA | Adds complexity | 2 |
| Audit logging | Nice-to-have | 3 |
```

### 4. Preserve Delivery Speed

```
MVP exists to learn, not to impress.
Ship → Learn → Iterate
```

---

## Scope Decision Matrix

| Criterion | INCLUDE | SIMPLIFY | DEFER |
|-----------|---------|----------|-------|
| Core to learning goal | ✅ | - | - |
| Blocks user testing | ✅ | - | - |
| Nice-to-have | - | - | ✅ |
| Adds significant complexity | - | ✅ | ✅ |
| Stakeholder "want" | - | - | ✅ |

---

## Integration

- **Precedes:** `spec-driven-planning`
- **Follows:** `project-vision-normalizer`
- **Validates:** Feature requests during development

---

## Constraints

- MVP is about learning, not feature completeness
- Default to DEFER when uncertain
- Every inclusion must justify its value

Ship fast, learn faster.
