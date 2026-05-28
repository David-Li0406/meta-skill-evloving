---
name: compound-engineering
description: "Compound Engineering workflow for AI-assisted development. Use when planning features, executing work, reviewing code, or codifying learnings. Follows the Plan -> Work -> Review -> Compound loop where each unit of engineering makes subsequent work easier. Triggers on: plan this feature, implement this, review this code, compound learnings, create implementation plan, systematic development."
---

# Compound Engineering

A development methodology where each unit of work makes subsequent work easier, not harder.

## Core Philosophy

**Each unit of engineering work should make subsequent units of work easier--not harder.**

Traditional development accumulates technical debt. Compound engineering inverts this by creating a learning loop where each bug, failed test, or problem-solving insight gets documented and used by future work.

## The Compound Engineering Loop

```
Plan -> Work -> Review -> Compound -> (repeat)
```

1. **Plan (40%)**: Research approaches, synthesize information into detailed implementation plans
2. **Work (20%)**: Execute the plan systematically with continuous validation
3. **Review (20%)**: Evaluate output quality and identify learnings
4. **Compound (20%)**: Feed results back into the system to make the next loop better

80% of compound engineering is in planning and review. 20% is in execution.

## Step 1: Plan

Before writing any code, create a comprehensive plan.

### Research Phase
1. **Codebase Analysis**: Search for similar patterns, conventions, and prior art
2. **Commit History**: Use `git log` to understand how related features were built
3. **Documentation**: Check README, AGENTS.md, and inline documentation
4. **External Research**: Search for best practices relevant to the problem

### Plan Document Structure

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

Execute the plan systematically:

1. **Create isolated environment**: Use feature branch or git worktree
2. **Break down into tasks**: Create TODO list from plan
3. **Execute systematically**: One task at a time
4. **Validate continuously**: Run tests after each change
5. **Commit incrementally**: Small, focused commits

### Quality Checks During Work
```bash
npm run typecheck
npm test
npm run lint
```

## Step 3: Review

### Review Checklist

**Code Quality**
- [ ] Follows existing codebase patterns and conventions
- [ ] No unnecessary complexity
- [ ] Clear naming that matches project conventions
- [ ] No debug code left behind

**Security**
- [ ] No secrets or sensitive data exposed
- [ ] Input validation where needed

**Performance**
- [ ] No obvious performance regressions
- [ ] Database queries are efficient (no N+1)

**Testing**
- [ ] Tests cover acceptance criteria
- [ ] Edge cases considered

## Step 4: Compound

Capture learnings to make future work easier:

### What to Compound

**Patterns**: Document new patterns discovered
```markdown
## Pattern: [Name]
When to use: [context]
Implementation: [example code]
See: [file reference]
```

**Decisions**: Record why certain approaches were chosen
```markdown
## Decision: [Choice Made]
Context: [situation]
Options considered: [alternatives]
Rationale: [why this choice]
```

**Failures**: Turn every bug into a lesson
```markdown
## Lesson: [What Went Wrong]
Symptom: [what was observed]
Root cause: [actual problem]
Fix: [solution]
Prevention: [how to avoid in future]
```

### Where to Codify Learnings

1. **AGENTS.md**: Project-wide guidance
2. **Subdirectory AGENTS.md**: Specific guidance for subsystems
3. **Inline comments**: Only when the code isn't self-explanatory
4. **Test cases**: Turn bugs into regression tests

## Key Principles

1. **Prefer duplication over wrong abstraction**
2. **Document as you go**
3. **Quality compounds**
4. **Systematic beats heroic**
5. **Knowledge should be codified**

## Success Metrics

You're doing compound engineering well when:
- Each feature takes less effort than the last similar feature
- Bugs become one-time events (documented and prevented)
- New team members can be productive quickly
- Code reviews surface fewer issues
- Technical debt decreases over time
