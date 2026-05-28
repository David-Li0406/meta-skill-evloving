---
name: documentation-consistency-keeper
description: Keeps all project documents consistent after code or spec changes. Use after any approved update.
triggers: [spec-update, major-code-change]
outputs: [updated-docs, change-summary]
depends_on: [spec-auto-updater]
---

# Documentation Consistency Keeper

## Purpose

Ensures all project documentation stays **synchronized** after spec or code changes. Outdated documentation is technical debt that causes confusion and errors.

---

## When to Use

- After spec updates
- After major code changes
- After API contract changes
- Before release

---

## Instructions

### 1. Identify Dependent Documents

```markdown
## Document Dependency Map

**Changed:** spec/auth.md (AUTH-001 updated)

**Dependent Documents:**
- [ ] README.md - mentions auth flow
- [ ] docs/api.md - auth endpoint docs
- [ ] CHANGELOG.md - needs entry
- [ ] docs/security.md - references token expiry
```

### 2. Update Terminology and References

| Old Term | New Term | Files Affected |
|----------|----------|----------------|
| "1 hour token" | "24 hour token" | api.md, README |
| "session expiry" | "token expiry" | security.md |

### 3. Remove Outdated Statements

```markdown
## Outdated Content Removed

**File:** docs/api.md
**Line 42:** "Tokens expire after 1 hour" → REMOVED
**Replaced With:** "Tokens expire after 24 hours (AUTH-001)"
```

### 4. Produce Change Summary

```markdown
## Documentation Update Summary

**Trigger:** AUTH-001 spec update (token expiry change)
**Date:** 2026-01-22

### Files Updated
| File | Changes |
|------|---------|
| README.md | Updated auth section |
| docs/api.md | Fixed endpoint docs |
| CHANGELOG.md | Added entry |

### Verification
- [ ] All links still work
- [ ] No orphaned references
- [ ] Version numbers consistent
```

---

## Integration

- **Precedes:** `project-regression-checklist`
- **Follows:** `spec-auto-updater`
- **Validates:** Doc-to-code consistency

---

## Constraints

- Outdated docs are technical debt
- All spec changes must cascade to docs
- Version numbers must stay synchronized

Docs must match reality.
