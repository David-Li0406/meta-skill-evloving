# Logging Triggers

Criteria for what to log and when, ensuring high signal-to-noise ratio.

## LEARNINGS.md Triggers

### Must Log

| Category | Pattern | Why Log |
|----------|---------|---------|
| API Discovery | Hook returns different property than expected | Prevent repeated debugging |
| Path Conventions | Actual directory structure differs from expected | Avoid file placement confusion |
| Type Patterns | Special typing required for library interop | Prevent recurring type errors |
| Test Mocks | Browser API mock required | Save setup time |
| Framework Quirks | SSR vs client behavior differences | Prevent hydration/runtime errors |
| Import Patterns | Barrel exports, path aliases, resolution | Avoid module resolution issues |

### Should Log

| Category | Pattern | When |
|----------|---------|------|
| Performance | Optimization technique that worked | When non-obvious |
| Build Config | Special configuration needed | When spent >15min figuring out |
| Debugging | Technique that revealed root cause | When would help future debugging |
| Integration | External service/API quirk | When not in official docs |

### Skip (Don't Log)

| Type | Example | Why Skip |
|------|---------|----------|
| Typos | Fixed spelling in variable name | One-off, no learning |
| Generic knowledge | "Use async/await for promises" | Common knowledge |
| Duplicates | Already documented pattern | Check first |
| Temporary fixes | Workaround for bug being fixed | Will become obsolete |
| Version-specific | Bug in specific version being upgraded | Will be irrelevant |

## ERROR_HISTORY.md Triggers

### Must Log

| Error Type | Characteristics | Example |
|------------|-----------------|---------|
| Recurrent | Same error 2+ times in session | Type inference failing same way |
| Multi-file | Spans >2 files to diagnose | Circular dependency |
| Hidden cause | Root cause non-obvious | Race condition |
| Configuration | Build/env/config issue | Mismatched versions |
| Integration | External service error | Auth token format |

### Should Log

| Error Type | When | Format |
|------------|------|--------|
| Security | Any auth/permission issue | Include secure fix |
| Data | Data integrity/validation | Include validation rule |
| Performance | Caused measurable degradation | Include metrics |
| Edge case | Rare but important | Include trigger conditions |

### Skip (Don't Log)

| Type | Example | Why Skip |
|------|---------|----------|
| Simple typos | Misspelled variable | Won't recur once fixed |
| IDE errors | False positive linting | Not actual error |
| Expected errors | Validation working correctly | Working as designed |
| External downtime | Third-party service outage | Not our bug |

## Logging Format

### LEARNINGS.md Entry

```markdown
## YYYY-MM-DD: [Brief Topic]

**Context:** [What was being done, 1-2 sentences]
**Learning:** [Key insight, specific and actionable]
**Apply when:** [Trigger conditions for using this knowledge]
```

**Example:**
```markdown
## 2024-01-15: Framer Motion Variant Types

**Context:** Creating stagger animation variants for list items.
**Learning:** Use `as const` assertion on variant objects for proper TypeScript inference. Without it, property types widen to `string | number`.
**Apply when:** Defining Framer Motion variants in TypeScript files.
```

### ERROR_HISTORY.md Entry

```markdown
## YYYY-MM-DD: [Error Type]

**Severity:** Low | Medium | High | Critical
**Files:** [List of affected files]
**Error:** [Error message or symptom]
**Root Cause:** [What actually caused it]
**Fix:** [How it was resolved]
**Prevention:** [How to avoid in future]
```

**Example:**
```markdown
## 2024-01-15: Route Parameter Conflict

**Severity:** Medium
**Files:** app/products/[id]/page.tsx, app/products/[slug]/page.tsx
**Error:** Next.js build failure: "Conflicting dynamic segments"
**Root Cause:** Two dynamic routes with different param names at same path level
**Fix:** Consolidated to single [id] param, removed [slug] variant
**Prevention:** Check for existing dynamic routes before adding new ones
```

## Signal Boosting

### High-Signal Patterns

Log with extra detail when:
- Error cost >30 minutes to debug
- Pattern affects multiple features
- Fix required non-obvious insight
- Would surprise a new team member

### Low-Signal Indicators

Probably skip if:
- Took <5 minutes to fix
- Obviously wrong code
- Already in documentation
- Framework version-specific

## Review Process

### Before Logging

1. **Check existing entries** - Don't duplicate
2. **Assess recurrence** - Will this happen again?
3. **Evaluate utility** - Would future-self benefit?
4. **Consider scope** - Project-specific or universal?

### After Logging

1. **Verify accuracy** - Re-read for correctness
2. **Check format** - Follows template
3. **Prune old entries** - Remove obsolete learnings
4. **Cross-reference** - Link related entries

## Session Patterns

### Beginning of Session

1. Read recent entries in LEARNINGS.md and ERROR_HISTORY.md
2. Note any patterns relevant to current task
3. Set mental flag for potential logging

### During Session

1. When error occurs, check ERROR_HISTORY.md first
2. When discovering pattern, note for potential logging
3. Keep brief notes for end-of-session review

### End of Session

1. Review session for logging candidates
2. Write entries while context is fresh
3. Update CLAUDE.md if needed
4. Consider skill updates if applicable
