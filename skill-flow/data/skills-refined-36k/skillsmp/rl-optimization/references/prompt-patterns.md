# Prompt & Template Patterns

Reference guide for effective prompt and template design based on RL intake findings.

## Prompt Patterns

### 1. Action Specificity

**Bad**: Vague verbs that leave room for interpretation
```markdown
Create the specification document.
```

**Good**: Specific actions with clear expectations
```markdown
Create the specification document by:
1. Reading the template from `.specify/extensions/workflows/feature/spec-template.md`
2. Filling in EVERY section - do not skip any, even if brief
3. Writing to `specs/{feature-num}-{name}/spec.md`
4. Creating a symlink: `ln -sf spec.md spec-feature.md`
```

**Why**: Agents perform better with explicit step-by-step instructions.

---

### 2. Decision Trees

**Bad**: Open-ended choices without criteria
```markdown
Choose the appropriate workflow for the task.
```

**Good**: Clear criteria for each option
```markdown
Select the workflow based on task characteristics:

| If the task is... | Use this workflow |
|-------------------|-------------------|
| New functionality (>7 tasks) | `/speckit.specify` |
| Small improvement (<7 tasks) | `/speckit.enhance` |
| Bug fix with known cause | `/speckit.bugfix` |
| Change to existing feature | `/speckit.modify` |
| Code quality (no behavior change) | `/speckit.refactor` |
| Production emergency | `/speckit.hotfix` |
| Removing a feature | `/speckit.deprecate` |
```

**Why**: Eliminates guesswork and ensures consistent workflow selection.

---

### 3. Output Format Specification

**Bad**: Implicit output expectations
```markdown
Report the results of the analysis.
```

**Good**: Explicit format with example
```markdown
Report results in this format:

```
✓ Analysis Complete

Files analyzed: {N}
Issues found: {N} critical, {N} warning, {N} info

Critical Issues:
- {file}:{line} - {description}

Next Steps:
1. {action}
```
```

**Why**: Consistent output helps users parse results and enables automation.

---

### 4. Error Recovery Paths

**Bad**: No guidance for failure cases
```markdown
Run the test suite.
```

**Good**: Explicit handling for each outcome
```markdown
Run the test suite:

```bash
npm test
```

**If all tests pass**: Proceed to next step.

**If tests fail**:
1. Check if failures relate to your changes
2. If yes: Fix issues and re-run before continuing
3. If no (pre-existing failures):
   - Document in the spec under "Known Issues"
   - Proceed with caution
   - Note: Do NOT mark the task complete until tests pass

**If tests timeout**: Check for infinite loops in recent changes.
```

**Why**: Agents need explicit guidance for non-happy-path scenarios.

---

### 5. Completion Signals

**Bad**: No clear endpoint
```markdown
Implement the feature based on the plan.
```

**Good**: Explicit completion criteria
```markdown
The implementation is complete when:
- [ ] All tasks in tasks.md are marked `[X]`
- [ ] All tests pass (`npm test` exits 0)
- [ ] No TypeScript errors (`npm run typecheck` exits 0)
- [ ] Changes are committed with descriptive message

Report completion with:
```
✓ Implementation Complete

Tasks: {completed}/{total}
Tests: {passing}/{total}
Ready for: /speckit.review
```
```

**Why**: Prevents premature completion and ensures quality gates are met.

---

### 6. Context Loading

**Bad**: Assuming context is available
```markdown
Review the specification and create a plan.
```

**Good**: Explicit context loading steps
```markdown
### 1. Load Context

First, load the feature context:

```bash
cd "$(git rev-parse --show-toplevel)" && \
source .specify/scripts/bash/common.sh && \
get_feature_paths
```

This provides:
- `FEATURE_DIR` - Feature directory path
- `FEATURE_SPEC` - Specification file (spec.md)
- `IMPL_PLAN` - Implementation plan (plan.md)
- `TASKS` - Task list (tasks.md)

Read these files to understand:
- Feature requirements and acceptance criteria
- Current implementation status
- Remaining work items
```

**Why**: Makes context acquisition reliable and repeatable.

---

### 7. Constraint Boundaries

**Bad**: Unbounded scope
```markdown
Improve the code quality.
```

**Good**: Clear boundaries and limits
```markdown
Improve code quality within these constraints:

**DO**:
- Fix linting errors in modified files
- Add missing type annotations
- Extract repeated code (>3 occurrences)

**DON'T**:
- Refactor files you didn't modify
- Change public API signatures
- Add new dependencies
- Exceed 7 tasks total

If improvements would exceed these boundaries, document them as
"Future Improvements" in the spec and stop.
```

**Why**: Prevents scope creep and keeps changes focused.

---

## Template Patterns

### 1. Section Headers with Guidance

**Bad**: Empty headers
```markdown
## Root Cause

## Prevention
```

**Good**: Headers with inline guidance
```markdown
## Root Cause

What is the underlying cause of this bug? Use Five Whys analysis:
1. Why did [symptom] occur?
2. Why did [cause 1] occur?
3. Why did [cause 2] occur?
4. Why did [cause 3] occur?
5. Why did [cause 4] occur? → Root cause

## Prevention

How will we prevent this class of bug in the future?
- [ ] Tests to add (specific test cases)
- [ ] Code review checklist updates
- [ ] Monitoring/alerting improvements
- [ ] Documentation updates
```

**Why**: Guides users to provide useful content rather than minimal responses.

---

### 2. Required vs Optional Sections

**Bad**: All sections appear equal
```markdown
## Description
## Impact
## Nice to Have
## Future Ideas
```

**Good**: Clear required/optional distinction
```markdown
## Description *(required)*
[What is being changed and why]

## Impact *(required)*
[Who/what is affected by this change]

---
*Optional sections below - include if relevant*

## Nice to Have
[Non-blocking improvements to consider]

## Future Ideas
[Out of scope but worth documenting]
```

**Why**: Ensures critical information isn't skipped while allowing flexibility.

---

### 3. Placeholder Examples

**Bad**: Generic placeholders
```markdown
**Author**: {{AUTHOR}}
**Date**: {{DATE}}
**Status**: {{STATUS}}
```

**Good**: Placeholders with format hints
```markdown
**Author**: {{AUTHOR e.g., @username}}
**Date**: {{DATE e.g., 2024-01-15}}
**Status**: {{STATUS: Draft | In Review | Approved | Implemented}}
```

**Why**: Reduces ambiguity about expected values.

---

### 4. Checklists Over Prose

**Bad**: Narrative requirements
```markdown
Before submitting, make sure you've tested all the edge cases,
verified the documentation is updated, and confirmed the tests pass.
```

**Good**: Actionable checklist
```markdown
## Pre-Submit Checklist

- [ ] All new code has tests
- [ ] Edge cases documented and tested:
  - [ ] Empty input
  - [ ] Maximum size input
  - [ ] Invalid input types
- [ ] Documentation updated
- [ ] `npm test` passes
- [ ] `npm run lint` passes
- [ ] Commit message follows convention
```

**Why**: Checklists are verifiable; prose is interpretable.

---

### 5. Progressive Disclosure

**Bad**: All information at once
```markdown
## Implementation

[Massive section with everything]
```

**Good**: Layered detail
```markdown
## Implementation Overview

Brief description of the approach (2-3 sentences).

### Phase 1: Foundation
- Task 1.1: ...
- Task 1.2: ...

### Phase 2: Core Logic
- Task 2.1: ...
- Task 2.2: ...

### Phase 3: Integration
- Task 3.1: ...
- Task 3.2: ...

---

## Detailed Design

*Expand this section only after Overview is approved.*

### Component A
[Detailed design]

### Component B
[Detailed design]
```

**Why**: Allows review at appropriate levels without overwhelming.

---

## Anti-Patterns to Avoid

### 1. Circular References
```markdown
# Bad
See the implementation plan for details.
(Plan says: See the specification for requirements.)
```

### 2. Outdated Examples
```markdown
# Bad - example doesn't match current structure
Example: `./scripts/old-script.sh`  # Script was renamed
```

### 3. Assumed Tooling
```markdown
# Bad - assumes specific test framework
Run `jest --watch`  # Project might use vitest
```

### 4. Magic Numbers
```markdown
# Bad
Maximum 7 tasks.  # Why 7?

# Good
Maximum 7 tasks (single-phase scope - if more are needed, use full feature workflow).
```

### 5. Ambiguous Pronouns
```markdown
# Bad
After it completes, run it again with the flag.

# Good
After the build completes, run the test suite again with the --coverage flag.
```

---

## Scoring Rubric

When evaluating prompts/templates, score each criterion 1-5:

| Score | Meaning |
|-------|---------|
| 5 | Excellent - No improvement needed |
| 4 | Good - Minor polish possible |
| 3 | Adequate - Works but could be clearer |
| 2 | Poor - Causes frequent confusion |
| 1 | Failing - Regularly breaks workflows |

**Target**: All criteria should score 4+ before release.
