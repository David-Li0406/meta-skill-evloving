# Bug Fix Plan Reference

## Planning Approach

Bug fix plans focus on thorough root cause analysis and prevention of regression. Understanding the cause is critical to implementing an effective fix.

## Key Sections

A bug fix plan should include:

1. **Description**: Clear explanation of the bug and its impact
2. **Reproduction Steps**: Step-by-step instructions to reproduce the bug
3. **Root Cause Analysis**: Technical explanation of why the bug occurs
4. **Fix Strategy**: High-level approach to fixing the bug
5. **Tasks**: Specific implementation tasks
6. **Validation**: Steps to verify the fix works
7. **Testing**: Test cases to prevent regression

## Investigation Focus

When analyzing a bug:

- Trace the execution path that leads to the bug
- Identify the specific conditions that trigger it
- Look for related code paths that may have similar issues
- Check if there are existing tests that should have caught this
- Understand the impact scope (which users/features are affected)

## Root Cause Categories

Common root causes to investigate:

- **Logic Errors**: Incorrect conditions, off-by-one errors, wrong operators
- **State Management**: Race conditions, stale data, incorrect state transitions
- **Error Handling**: Unhandled exceptions, silent failures, missing edge cases
- **Integration Issues**: API contract violations, data format mismatches
- **Configuration**: Environment-specific issues, missing settings
- **Resource Management**: Memory leaks, connection exhaustion, deadlocks

## Fix Strategy Guidelines

- Address the root cause, not just symptoms
- Consider defensive measures to prevent similar bugs
- Avoid fixes that introduce new complexity
- Prefer targeted changes over broad refactoring
- Include test coverage for the specific failure case

## Milestone Patterns

Typically 1-3 milestones per bug fix. Common patterns:

1. **Investigation & Setup**: Reproduce bug, identify root cause, document findings
2. **Implementation**: Apply fix, handle edge cases
3. **Validation & Testing**: Verify fix, add regression tests

## Template

```markdown
# Bug Fix: {{bug_title}}

## Progress

### Implementation

{{implementation_checklist}}

### Validation

{{validation_checklist}}

## Description

{{description}}

## Reproduction Steps

{{reproduction_steps}}

## Root Cause Analysis

{{root_cause}}

## Fix Strategy

{{fix_strategy}}

## Milestones

### Milestone {{milestone_number}}: {{milestone_title}}

{{milestone_description}}

#### Task {{milestone_number}}.{{task_number}}: {{task_title}}

{{task_description}}

## Validation

{{validation}}

## Testing

{{testing}}
```

<!--
Type-specific placeholders (see SKILL.md for common milestone/task placeholders):
- {{bug_title}}: Concise title for the bug (e.g., "Login Timeout on Safari OAuth Redirect")
- {{description}}: Clear explanation of the bug and its impact
- {{reproduction_steps}}: Numbered steps to reproduce the bug
- {{root_cause}}: Technical explanation with code references
- {{fix_strategy}}: High-level approach to fixing the bug
- {{validation}}: Steps to verify the bug is fixed
- {{testing}}: Test cases to add to prevent regression
-->
