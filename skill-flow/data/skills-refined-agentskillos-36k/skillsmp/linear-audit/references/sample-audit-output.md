# Sample Audit Output

Complete example AUDIT.md artifact from a real project audit.

---

# ARB Linear Audit

| | |
|---|---|
| **date** | 2025-01-22 |
| **project** | ~/Developer/arbor/arbor-xyz |
| **type** | convex-next |
| **score** | 78/100 |
| **grade** | C (gaps) |
| **v1 ready** | No |
| **trace** | tr_arb20250122 |

---

## Executive Summary

Arbor is in good shape for continued development but not yet V1 ready. Two blockers: 14 issues missing context markers (30%), and 2 dependency cycles in packages/backend. Coverage gap is minor (78% vs 80% target). Creative edge surfaced around ACP protocol integration - the daemon-web bridge is experimental and needs support.

**Key numbers:**
- 45 total issues, 32 with context (71%)
- 78% test coverage (target 80%)
- 0 critical bugs, 2 architecture cycles
- 12 commits in last week (active development)

---

## Code State

### Test Coverage

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Line Coverage | 78% | 80% | ⚠️ -2% |
| Branch Coverage | 72% | 70% | ✅ +2% |
| Uncovered Files | 8 | <10 | ✅ |

**Uncovered areas:**
- `packages/daemon/src/ipc/handlers.ts` - 0% (experimental)
- `packages/daemon/src/permissions/flow.ts` - 12%
- `apps/app/src/components/code/agent-terminal.tsx` - 45%

### Build Health

| Check | Status | Notes |
|-------|--------|-------|
| Build | ✅ passing | 45s total |
| TypeScript | ✅ clean | 0 errors |
| Lint | ⚠️ 3 warnings | unused imports |

### Recent Activity

| Period | Commits | Files Changed | Focus Areas |
|--------|---------|---------------|-------------|
| Last 7 days | 12 | 34 | daemon, ACP protocol |
| Last 30 days | 45 | 128 | agent integration, E2E tests |

**Trajectory:** Active development focused on ACP agent integration. Daemon package growing fastest.

---

## Architecture

### Package Structure

```
arbor-xyz/
├── apps/app (main web) - 156 files
├── apps/daemon (desktop) - 42 files
├── packages/backend (convex) - 89 files
├── packages/design (ui) - 67 files
├── packages/auth (clerk) - 12 files
└── packages/github - 8 files
```

### Cycles Detected

| Cycle | Packages | Severity |
|-------|----------|----------|
| 1 | backend → github → backend | 🔴 High |
| 2 | design → auth → design | 🟡 Medium |

**Recommendation:** Break cycle 1 by extracting shared types. Cycle 2 can wait.

### Dead Code

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Unused Exports | 12 | <20 | ✅ |
| Dead Code % | 3% | <5% | ✅ |

**Notable dead code:**
- `packages/backend/convex/gen-ui/` - entire directory unused (removed feature)
- `apps/app/src/lib/legacy-auth.ts` - pre-Clerk auth code

---

## Linear State

### Issue Distribution

| State | Count | % |
|-------|-------|---|
| Backlog | 18 | 40% |
| Todo | 12 | 27% |
| In Progress | 5 | 11% |
| Done | 10 | 22% |
| **Total** | **45** | 100% |

### Context Quality

| Status | Count | % | Action |
|--------|-------|---|--------|
| Fresh context (<7 days) | 24 | 53% | ✅ Ready |
| Aging context (7-14 days) | 8 | 18% | Consider refresh |
| Stale context (>14 days) | 8 | 18% | ⚠️ Refresh needed |
| No context | 5 | 11% | 🔴 Enrich required |

### Issues Needing Attention

| Issue | Problem | Action |
|-------|---------|--------|
| ARB-401 | No linked sub-issues | Break down permission refactor |
| ARB-234 | References old Clerk patterns | Archive, create fresh issue |
| ARB-189 | No description | Clarify or archive |
| ARB-156 | Duplicate of ARB-401 | Merge |
| ARB-092 | Stale 45 days, no activity | Archive |

### Priority Distribution

| Priority | Count |
|----------|-------|
| 🔴 Urgent | 1 |
| 🟠 High | 4 |
| 🟡 Medium | 22 |
| 🟢 Low | 18 |

---

## V1 Gap Analysis

### Template: convex-next-v1

| Category | Criterion | Current | Target | Gap | Status |
|----------|-----------|---------|--------|-----|--------|
| Code | Test coverage | 78% | 80% | -2% | ⚠️ Gap |
| Code | Build | passing | passing | - | ✅ Met |
| Code | Types | clean | clean | - | ✅ Met |
| Architecture | Cycles | 2 | 0 | -2 | 🔴 Blocker |
| Architecture | Dead code | 3% | <5% | - | ✅ Met |
| Linear | Context coverage | 71% | 100% | -29% | 🔴 Blocker |
| Linear | Freshness | 71% fresh | <14 days | - | ⚠️ Gap |
| Linear | Vague issues | 3 | 0 | -3 | ⚠️ Gap |
| Docs | AGENTS.md | present | accurate | drift | ⚠️ Gap |

### Blockers (must fix)

1. **14 issues missing context markers** (30% of active issues)
   - Fix: Run batch issue-context enrichment
   - Effort: ~30 minutes

2. **2 dependency cycles detected**
   - Fix: Extract shared types from backend/github cycle
   - Effort: ~2 hours

### Gaps (should fix)

1. **Test coverage 78% < 80%**
   - Fix: Add tests for daemon handlers
   - Effort: ~1 hour

2. **8 issues with stale context**
   - Fix: Refresh context markers
   - Effort: ~20 minutes

3. **AGENTS.md references removed gen-ui feature**
   - Fix: Update documentation
   - Effort: ~10 minutes

---

## Creative Edge Surfaced

### ACP Protocol Integration

**Status:** Active development, experimental
**Energy:** High - this is where Luke's attention is focused
**Issues:** ARB-401 (permission refactor) is the anchor

**What emerged:**
- Protocol design is solid, implementation is "hacky"
- Daemon-web bridge is the creative edge
- Permission flow needs cleanup but works
- No tests on experimental daemon code (intentional speed trade-off)

**Support needed:**
- Documentation for daemon IPC patterns
- Test coverage once design stabilizes
- Linked sub-issues for ARB-401 breakdown

### CSS Spring Physics (discovered)

**Status:** Graduated from experiment
**Location:** squish, not arbor - cross-pollination opportunity

---

## Disposition Log

### Enriched (8 issues)

| Issue | Title |
|-------|-------|
| ARB-445 | Add agent spawning E2E tests |
| ARB-432 | Implement ACP heartbeat |
| ARB-428 | Dashboard responsive layout |
| ARB-415 | Convex auth token refresh |
| ARB-398 | Daemon folder watching |
| ARB-387 | Permission request UI polish |
| ARB-372 | Agent output streaming |
| ARB-361 | Code page keyboard shortcuts |

### Archived (3 issues)

| Issue | Title | Reason |
|-------|-------|--------|
| ARB-234 | Refactor auth module | Outdated, replaced by fresh issue |
| ARB-092 | Fix login redirect | Stale 45 days, likely resolved |
| ARB-156 | Permission system cleanup | Duplicate of ARB-401 |

### Kept as-is (34 issues)

- 24 with fresh context: ready for V1
- 10 with aging context: acceptable for now

---

## Recommendations

| # | Action | Impact | Effort | Priority |
|---|--------|--------|--------|----------|
| 1 | Run batch issue-context on 5 missing | Removes blocker | Low | P1 |
| 2 | Break backend/github cycle | Removes blocker | Medium | P1 |
| 3 | Add daemon handler tests | Closes coverage gap | Medium | P2 |
| 4 | Refresh 8 stale issue contexts | Improves freshness | Low | P2 |
| 5 | Update AGENTS.md (remove gen-ui refs) | Documentation accuracy | Low | P3 |
| 6 | Break down ARB-401 into sub-issues | Better tracking | Low | P2 |

---

## Next Steps

1. **Immediate:** Run issue-context enrichment on 5 missing issues
2. **This week:** Break dependency cycle in backend/github
3. **Follow-up:** Re-audit in 1 week after blockers resolved

---

## Session Metadata

| Field | Value |
|-------|-------|
| Trace ID | tr_arb20250122 |
| Ask-deep rounds | 3 |
| Specialists used | 4 (code-state, architecture, linear-state, v1-gaps) |
| Duration | 23 minutes |
| HIL checkpoints | 2 (synthesis, disposition) |

---

## Confidence

| Domain | Confidence | Notes |
|--------|------------|-------|
| Code State | 9/10 | All tools ran successfully |
| Architecture | 8/10 | Cycles detected, dead code scan complete |
| Linear State | 8/10 | Full issue scan, context markers checked |
| V1 Gaps | 8/10 | Clear delta from template |
| **Overall** | **8/10** | High confidence, two clear blockers |

---

*Generated by linear-audit skill*
*Gist: https://gist.github.com/lnittman/arb-audit-20250122*
