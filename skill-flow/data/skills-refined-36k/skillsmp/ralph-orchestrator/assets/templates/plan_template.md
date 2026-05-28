# Plan: {{task-name}}

**Created**: {{timestamp}}
**Status**: draft
**Type**: freeform

## Goal

{{goal}}

## Success Criteria

{{#each success_criteria}}
- [ ] {{this}}
{{/each}}

## Verification

**Method**: {{verification.method}}
{{#if verification.command}}
**Command**: `{{verification.command}}`
{{/if}}
**Description**: {{verification.description}}

## Out of Scope

{{#each out_of_scope}}
- {{this}}
{{/each}}
{{#unless out_of_scope}}
- None specified
{{/unless}}

---

## Phases

{{#each phases}}
### {{id}}: {{name}}

**Steps**:
{{#each steps}}
- [ ] {{this}}
{{/each}}

**Verify**: {{verification}}

**Status**: {{#if complete}}COMPLETE{{else}}pending{{/if}}

{{#if notes}}
**Notes**: {{notes}}
{{/if}}

---

{{/each}}

## Completion Checklist

Before outputting the completion promise `<promise>ALL PHASES COMPLETE</promise>`, verify:

- [ ] All phases marked as complete
- [ ] All success criteria met
- [ ] Verification command/method passes
- [ ] No known regressions introduced
- [ ] Code committed with descriptive messages

## Progress Tracking

During the Ralph loop, update `.claude/ralph/{{task-name}}/progress.md` after each action:

```markdown
## Learnings (append-only)

[Iteration 1] <what you learned>
[Iteration 2] <what you learned>
...

## Current State

**Current Phase**: P1
**Working on**: <current step>
**Attempts on current issue**: 0
```

## Escape Hatches

If stuck after 3 attempts on the same issue:
1. Document the issue in progress.md
2. Try ONE alternative approach
3. If still stuck, mark phase as BLOCKED and move to next phase
4. Do NOT output false completion promise
