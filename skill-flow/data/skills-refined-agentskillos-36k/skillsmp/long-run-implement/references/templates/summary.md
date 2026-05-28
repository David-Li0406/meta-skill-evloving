---
version: "1.0"
plan: NN
task_group: [group-name]
status: completed|failed|partial|skipped|timeout
completed_at: YYYY-MM-DDTHH:MM:SSZ
duration_minutes: 0
---

# Plan NN: [Task Group Name] Summary

**Status:** [Completed / Failed / Partial / Skipped / Timeout]

## Tasks Completed
- [x] Task 1: [name] - commit abc1234
- [x] Task 2: [name] - commit def5678
- [ ] Task 3: [name] - not started (if partial)

## Files Modified
| File | Action | Lines Changed |
|------|--------|---------------|
| path/to/file.ts | Created | +120 |
| path/to/other.ts | Modified | +15, -3 |

## Verification Results
- [x] `npm test -- path/to/test.ts` - PASSED (N/N tests)
- [x] Build check - PASSED
- [ ] Manual verification - PENDING (end of run)

## Deviations from Plan
### Auto-Fixed (Rules 1-3)
- [Rule N] Description of auto-fix applied

### Logged (Rule 5)
- ISS-XXX: Description of deferred enhancement

## Decisions Made
| Decision | Choice | Rationale |
|----------|--------|-----------|
| None | - | - |

## Issues Encountered
None.

## Next Steps
- Plan NN+1 ready for execution
- No blockers
