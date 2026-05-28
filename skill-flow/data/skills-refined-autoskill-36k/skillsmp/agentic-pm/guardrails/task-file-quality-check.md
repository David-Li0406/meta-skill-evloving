# Guardrail: Task File Quality Check

## When to Run

Run this check **before issuing each task file** to an engineer.

## Required Sections

A task file is INCOMPLETE without ALL of these:

### 1. Goal
- [ ] Clear, concise (1-2 sentences)
- [ ] Single interpretation only
- [ ] Measurable outcome

### 2. Non-Goals
- [ ] At least 2-3 explicit non-goals
- [ ] Prevents obvious scope creep
- [ ] Adjacent work excluded

### 3. Deliverables
- [ ] Specific files listed
- [ ] New vs update clearly marked
- [ ] Paths are correct

### 4. Acceptance Criteria
- [ ] Binary (pass/fail) criteria
- [ ] All checkboxes
- [ ] "CI passes" included
- [ ] No subjective criteria ("looks good")

### 5. Implementation Notes
- [ ] Code examples provided
- [ ] Patterns to follow specified
- [ ] Key details documented

### 6. Integration Notes
- [ ] Dependencies on other tasks
- [ ] What this task exports
- [ ] Who consumes this work

### 7. Do/Don't
- [ ] Positive guidance (Do)
- [ ] Negative guidance (Don't)
- [ ] Common mistakes called out

### 8. Stop and Ask Triggers
- [ ] At least 2-3 conditions
- [ ] Covers ambiguity scenarios
- [ ] Covers scope concerns

### 9. Testing Expectations
- [ ] Unit tests: required yes/no
- [ ] Specific tests to write
- [ ] Coverage impact
- [ ] CI requirements

### 10. PR Preparation
- [ ] Title format
- [ ] Labels
- [ ] Dependencies

### 11. Implementation Summary
- [ ] Blank section present
- [ ] Marked as engineer-owned
- [ ] Rejection warning included

## Quality Checks

Beyond completeness, verify:

- [ ] No ambiguous acceptance criteria
- [ ] Code examples match project patterns
- [ ] Integration notes reference specific task IDs
- [ ] Testing is specific (not "add tests")

## Failure Handling

If any check fails:

1. **DO NOT** issue the task file
2. **FIX** the missing/unclear sections
3. **RE-RUN** this check

## Red Flags

Automatic failure if you see:

- "Implement the feature" (too vague)
- "Add appropriate tests" (not specific)
- No non-goals section
- Subjective acceptance criteria
- Missing code examples for non-trivial tasks

## Architecture Compliance Hints (Magic Audit Specific)

If the task touches sensitive areas, add warnings to the task file:

### Entry file changes
If task modifies `App.tsx`, `main.ts`, or `preload.ts`:
- [ ] Warn about line budget constraints (~70/~150/~50 lines)
- [ ] Require compositional changes only (no business logic)
- [ ] Reference senior-engineer-pr-lead guardrails

### window.api usage
If task introduces `window.api` or `window.electron` calls:
- [ ] Require service/hook abstraction
- [ ] No scattered calls in components
- [ ] Typed service abstractions only

### State machine changes
If task modifies `useAppStateMachine` or state flows:
- [ ] Require semantic interface pattern (verbs, not setters)
- [ ] Pass state machine object, not individual props
- [ ] Document in implementation notes

### Complex flows
If task involves onboarding, permissions, or secure storage:
- [ ] Must use dedicated hooks pattern
- [ ] Must be in feature modules, not global files
- [ ] Consider state machine for multi-step flows
