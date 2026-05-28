# Common Plan Lint Failure Patterns

## Blocking Failures (FAIL)

| Pattern | Verdict | Fix |
|---------|---------|-----|
| No invariants listed | FAIL | Run /doc-discovery, extract invariants from feature docs |
| No test plan | FAIL | Add verification steps, at minimum one smoke test |
| Schema change without migration plan | FAIL | Add migration strategy + rollback procedure |
| Primary feature not identified | FAIL | Identify from FEATURE_INDEX.md |

## Warnings (WARN)

| Pattern | Verdict | Fix |
|---------|---------|-----|
| Missing coupled features | WARN | Check FEATURE_INDEX coupling notes |
| High blast radius without Doc Agent | WARN | Spawn Doc Agent for validation |
| Workflow impact not assessed | WARN | Check WORKFLOW_INDEX.md |
| Vague file references | WARN | Specify exact file paths |
| No docs-to-update listed | WARN | Identify docs that will need changes |

## Examples

### Failing Plan

```
Primary: (not specified)
Files: "some components"
Test: "will check it works"

Verdict: FAIL
- No primary feature identified
- No invariants listed
- Vague file references
- No real test plan
```

### Good Plan

```
Primary: course-player-and-progress
Impacted: dashboard, collections-and-context
Invariants:
- Progress persists across sessions
- Watch time triggers credits
- Progress scoped to user+course
Files: CoursePlayer.tsx, progressActions.ts
Test: Manual playback, verify DB update
Docs: Update course-player-and-progress.md

Verdict: PASS (Blast Radius: 3 - Medium)
```

## Escalation to Doc Agent

If blast radius >= 6, escalate:

```
@doc-agent: Please validate this plan against documented constraints:
[plan]

Specific checks needed:
- Invariant completeness
- Coupling analysis
- Security implications
```
