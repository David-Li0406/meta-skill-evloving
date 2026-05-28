# BACKLOG-XXX: CI - [Specific Issue Title]

> **Category:** `test` | `infra`
> **Priority:** [Critical/High/Medium/Low]
> **Created By:** SR Engineer
> **Created Date:** YYYY-MM-DD
> **Status:** Pending

---

## Problem Statement

**Test file:** `[path/to/test.ts]`
**Test name:** `[describe block > it block]`
**Line:** `[line number]`

**Symptom:** [What the test failure looks like]

**Frequency:**
- [ ] Every CI run
- [ ] >50% of CI runs
- [ ] Intermittent (10-50%)
- [ ] Rare (<10%)

**Platforms affected:**
- [ ] macOS CI
- [ ] Windows CI
- [ ] Local development

---

## Root Cause Analysis

**Investigation date:** YYYY-MM-DD
**Investigator:** [SR Engineer name/agent]

### Failure Classification

- [ ] **Performance** - Timing/ratio assertions fail
- [ ] **Flaky** - Race condition, shared state
- [ ] **Environment** - CI-specific issue
- [ ] **Regression** - Recent code change
- [ ] **Infrastructure** - CI system issue

### Investigation Details

**What was tested:**
```bash
# Commands run to investigate
```

**Observed data:**
| Run | Environment | Result | Time/Value |
|-----|-------------|--------|------------|
| 1   | Local       | Pass   | XXms       |
| 2   | CI macOS    | Fail   | XXms       |
| 3   | CI Windows  | Fail   | XXms       |

**Root cause determination:**

[Detailed explanation of what's actually wrong]

**Supporting evidence:**
1. [Evidence point 1]
2. [Evidence point 2]
3. [Evidence point 3]

---

## Current Workaround (if any)

**Workaround applied:** [Yes/No]

**If Yes:**
- **PR:** #XXX
- **Change:** [What was changed - e.g., CI_TOLERANCE increased from 1.5 to 2.0]
- **Justification:** [Why this is acceptable temporarily]
- **Risk:** [What regression might be masked]

**Backlog reference in code:**
```typescript
// TODO: BACKLOG-XXX - [Brief description]
// Current tolerance masks potential O(n²) in threadGroupingService
const CI_TOLERANCE = process.env.CI ? 2.0 : 1.0;
```

---

## Proper Fix Options

### Option A: [Name]

**Description:** [What would be done]

**Effort:** [Low/Medium/High]

**Pros:**
-

**Cons:**
-

### Option B: [Name]

**Description:** [What would be done]

**Effort:** [Low/Medium/High]

**Pros:**
-

**Cons:**
-

### Recommendation

**Recommended option:** [A/B]
**Rationale:** [Why this option]

---

## Acceptance Criteria

- [ ] Test passes reliably on all CI platforms
- [ ] No CI_TOLERANCE or arbitrary multipliers needed
- [ ] Performance meets documented baseline: [X]ms for [Y] items
- [ ] No regression in: [related functionality]
- [ ] Workaround code/comments removed

---

## Related Items

- **Related PRs:** #XXX (where workaround was added)
- **Related tests:** [list other affected tests]
- **Related services:** [services with potential issues]

---

## PM Notes

**Sprint assignment:**
**Estimated effort:**
**Dependencies:**
**Blocked by:**

---

## Completion Checklist (for engineer assigned)

- [ ] Reproduced issue locally
- [ ] Implemented proper fix (not tolerance adjustment)
- [ ] Verified fix on CI (all platforms)
- [ ] Removed workaround code/comments
- [ ] Updated test documentation if needed
- [ ] SR Engineer approved fix
