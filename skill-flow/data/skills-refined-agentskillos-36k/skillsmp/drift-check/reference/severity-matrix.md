# Severity Scoring Matrix

## By Area and Drift Type

| Area | Missing Doc | Wrong Doc | Stale Doc |
|------|-------------|-----------|-----------|
| Auth/RLS | 🔴 Critical | 🔴 Critical | 🟠 High |
| Billing | 🔴 Critical | 🔴 Critical | 🟠 High |
| AI/Prompts | 🟠 High | 🟠 High | 🟡 Medium |
| Server Actions | 🟠 High | 🟠 High | 🟡 Medium |
| Schema | 🟠 High | 🔴 Critical | 🟡 Medium |
| Routes | 🟡 Medium | 🟡 Medium | 🟢 Low |
| Components | 🟢 Low | 🟡 Medium | 🟢 Low |
| Workflows | 🟡 Medium | 🟠 High | 🟡 Medium |

## Severity Definitions

### 🔴 Critical
- Security implications (auth/RLS docs wrong)
- Financial implications (billing docs incorrect)
- Data integrity risks (schema mismatch)
- **Action**: Fix immediately, block other work

### 🟠 High
- Core functionality undocumented
- Invariants violated in code
- Server actions missing from docs
- **Action**: Fix this session

### 🟡 Medium
- User-facing routes not documented
- Workflow steps outdated
- Test checklists stale
- **Action**: Fix soon (within week)

### 🟢 Low
- Minor description inaccuracies
- Outdated examples
- Component documentation gaps
- **Action**: Track and batch fix

## Priority Resolution

When multiple drift items found:
1. Fix all Critical before any High
2. Fix all High before any Medium
3. Batch Low items for periodic cleanup

## Anti-Patterns

❌ Don't fix code to match wrong docs — docs follow code
❌ Don't ignore "minor" drift — it accumulates
❌ Don't detect drift without time to fix
❌ Don't skip workflow checks — they cause most user pain
