---
name: compound-engineering
description: Use this skill when planning features, executing work, reviewing code, or codifying learnings in a way that each unit of engineering makes subsequent work easier.
---

# Compound Engineering

A development methodology where each unit of work makes subsequent work easier, not harder. This approach helps to minimize technical debt and fosters a continuous learning loop.

## Core Philosophy

**Each unit of engineering work should make subsequent units of work easier—not harder.** Traditional development often accumulates technical debt, but compound engineering inverts this by creating a learning loop where each bug, failed test, or problem-solving insight gets documented and utilized in future work.

## The Compound Engineering Loop

```
Plan → Work → Review → Compound → (repeat)
```

1. **Plan (40%)**: Research approaches and synthesize information into detailed implementation plans.
2. **Work (20%)**: Execute the plan systematically with continuous validation.
3. **Review (20%)**: Evaluate output quality and identify learnings.
4. **Compound (20%)**: Feed results back into the system to improve the next loop.

80% of compound engineering is in planning and review; 20% is in execution.

## Step 1: Plan

Before writing any code, create a comprehensive plan. Good plans start with research:

### Research Phase

1. **Codebase Analysis**: Search for similar patterns, conventions, and prior art in the codebase.
2. **Commit History**: Use `git log` to understand how related features were built.
3. **Documentation**: Check README, AGENTS.md, and inline documentation.
4. **External Research**: Search for best practices relevant to the problem.

### Plan Document Structure

Create a plan document (markdown) with:

```markdown
# Feature: [Name]

## Context

- What problem does this solve?
- Who is affected?
- What's the current behavior vs desired behavior?

## Research Findings

- Similar patterns found in codebase: [list with file links]
- Relevant prior implementations: [commit references]
- Best practices discovered: [external references]

## Acceptance Criteria

- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (testable)

## Technical Approach

1. Step 1: [specific action]
2. Step 2: [specific action]

## Testing Strategy

- Unit tests: [what to test]
- Integration tests: [what to test]
- Manual verification: [steps]

## Risks & Mitigations

- Risk 1: [mitigation]
```

## Step 2: Work

Execute the plan while continuously validating the implementation against the acceptance criteria.