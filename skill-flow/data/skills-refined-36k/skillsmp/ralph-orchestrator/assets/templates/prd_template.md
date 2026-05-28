# PRD: {{task-name}}

**Created**: {{timestamp}}
**Status**: draft

## Problem Statement

{{problem_statement}}

## Success Criteria

When all of the following are true, the task is complete:

{{#each success_criteria}}
- [ ] {{this}}
{{/each}}

## Out of Scope

The following are explicitly NOT part of this task:

{{#each out_of_scope}}
- {{this}}
{{/each}}

## Verification Method

**Method**: {{verification.method}}
{{#if verification.command}}
**Command**: `{{verification.command}}`
{{/if}}
**Description**: {{verification.description}}

## User Stories

{{#each stories}}
### {{id}}: {{title}}

{{description}}

**Acceptance Criteria**:
{{#each acceptance_criteria}}
- [ ] {{this}}
{{/each}}

**Verification**: {{verification}}

**Status**: {{#if passes}}PASS{{else}}PENDING{{/if}}

---
{{/each}}

## Completion Checklist

Before outputting the completion promise, verify:

- [ ] All user stories marked as PASS
- [ ] All acceptance criteria checked
- [ ] Verification method confirms functionality
- [ ] No known regressions introduced
- [ ] Code committed with descriptive messages

## Notes

<!-- Add any additional context, decisions, or clarifications here -->
