---
name: bug-reporting
description: Bug report format and documentation for failed validations
category: validation
depends-on: [validation-workflow]
---

# Bug Reporting Skill

> "A good bug report is half the fix – be specific, be reproducible."

## When to Use This Skill

Use when validation fails and `status` must be set to `needs_fixes`.

## Quick Start

```markdown
## Bug Report: {{TASK_ID}}

**Severity**: Critical / High / Medium / Low
**Found in**: Automated tests / Browser testing

### Summary

Brief one-line description of the issue.

### Steps to Reproduce

1. Step one
2. Step two
3. Step three

### Expected Behavior

What should happen.

### Actual Behavior

What actually happens.

### Evidence

- Console errors: {{error text}}
- Screenshot: {{path}}
```

## Bug Report Template

```markdown
# Bug Report: {{TASK_ID}} - {{BRIEF_TITLE}}

**Reported**: {{ISO_TIMESTAMP}}
**Reporter**: QA Agent
**Severity**: {{Critical | High | Medium | Low}}
**Category**: {{Build | TypeScript | Runtime | Visual | Performance}}

---

## Summary

{{One or two sentences describing the issue}}

## Environment

- **Browser**: {{Chrome 120 / Firefox / Safari}}
- **OS**: {{Windows / macOS / Linux}}
- **Node Version**: {{v20.x.x}}
- **Screen Resolution**: {{1920x1080}}

## Steps to Reproduce

1. {{First step}}
2. {{Second step}}
3. {{Third step}}
4. {{...}}

## Expected Behavior

{{What should happen when following the steps}}

## Actual Behavior

{{What actually happens instead}}

## Console Errors

\`\`\`
{{Paste console errors here}}
\`\`\`

## Screenshots

{{Include paths to screenshots or describe what was captured}}

## Additional Context

{{Any other relevant information:

- Related code files
- Recent changes that might have caused this
- Workarounds attempted
- Similar issues seen before}}

## Acceptance Criteria Status

| Criterion       | Status            | Notes     |
| --------------- | ----------------- | --------- |
| {{Criterion 1}} | ✅ Pass / ❌ Fail | {{notes}} |
| {{Criterion 2}} | ✅ Pass / ❌ Fail | {{notes}} |
| {{Criterion 3}} | ✅ Pass / ❌ Fail | {{notes}} |

---

## For Developer

**Files likely involved**:

- {{file1.ts}}
- {{file2.tsx}}

**Suggested investigation**:

- {{Suggestion 1}}
- {{Suggestion 2}}
```

## Severity Levels

| Severity     | Definition                                 | Example                        |
| ------------ | ------------------------------------------ | ------------------------------ |
| **Critical** | App crashes, data loss, blocks all testing | Build fails, app won't load    |
| **High**     | Major feature broken, no workaround        | Player controls don't work     |
| **Medium**   | Feature partially works, has workaround    | Physics jittery but functional |
| **Low**      | Minor issue, cosmetic, edge case           | Slight visual glitch on resize |

## Category Types

| Category        | Description            | Automated Check       |
| --------------- | ---------------------- | --------------------- |
| **Build**       | Build or bundle fails  | `npm run build`       |
| **TypeScript**  | Type errors            | `npm run type-check`  |
| **Lint**        | Code style issues      | `npm run lint`        |
| **Test**        | Unit test failure      | `npm run test`        |
| **Runtime**     | Error during execution | Browser console       |
| **Visual**      | Incorrect appearance   | Browser testing       |
| **Performance** | FPS drops, lag, memory | Performance profiling |

## Anti-Patterns

❌ **DON'T:**

- Report bugs without reproduction steps
- Use vague descriptions ("it doesn't work")
- Omit error messages
- Skip severity classification
- Blame the developer in the report

✅ **DO:**

- Include exact steps to reproduce
- Copy full error messages
- Attach screenshots
- Specify environment details
- Suggest where to investigate

## current-task.json Update

When reporting a bug:

````json
{
  "status": "needs_fixes",
  "bugNotes": "## Summary\n\nBuild fails with TypeScript error...\n\n## Steps to Reproduce\n\n1. Run npm run build\n2. Observe error\n\n## Error\n\n```\nTS2322: Type 'string' is not assignable...\n```",
  "retryCount": 1
}
````

## Commit Format for Failed Validation

```
[ralph] [qa] feat-XXX: Validation FAILED

- TypeScript: pass
- Lint: pass
- Tests: FAIL - 2 tests failing
- Build: pass
- Browser: **FAIL** (MANDATORY - browser testing cannot be skipped even when other checks fail)

Bug: Unit test 'player spawns correctly' assertion failed.
See current-task.json for full bug report.

PRD: feat-XXX | Agent: qa | Iteration: N
```

## Checklist

Before submitting bug report:

- [ ] Summary is clear and specific
- [ ] Reproduction steps are complete
- [ ] Expected vs actual clearly stated
- [ ] Console errors included
- [ ] Screenshots attached (if visual)
- [ ] Severity assigned
- [ ] Category assigned
- [ ] Environment specified
- [ ] current-task.json updated

## Reference

- [agents/qa/AGENT.md](../../AGENT.md) — Full QA instructions
- [agents/qa/skills/validation-workflow.md](validation-workflow.md) — Full workflow
