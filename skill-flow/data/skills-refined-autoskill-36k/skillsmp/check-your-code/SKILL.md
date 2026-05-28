---
name: check-your-code
description: Reviews code quality, pattern adherence, and architecture with red-team validation. Use when user says "check your code", "code quality review", "is this well-written", or "review code quality". Different from check-your-work which finds bugs.
allowed-tools: Task, Read, Glob, Grep, Bash, AskUserQuestion
version: 1.3.0
---

# Check Your Code

> Review code quality, pattern adherence, and architecture—focused on "Is this well-written?" not "Will this break?"

<when_to_use>

## When to Use

Invoke when user says:

- "check your code"
- "code quality review"
- "is this well-written"
- "review code quality"
- "did you follow the patterns"

**Different from check-your-work**: check-your-work finds bugs and security issues. check-your-code evaluates code quality (pattern adherence, architecture, readability). Both use P0-P3 severity.
</when_to_use>

<workflow>

## Workflow Overview

| Phase | Agents     | Action                                           |
| ----- | ---------- | ------------------------------------------------ |
| 1     | -          | Scope Discovery (identify files)                 |
| 2     | 5 parallel | Quality Review (all agents at once)              |
| 3     | 1          | Red Team - Challenge Findings (devil's advocate) |
| 4     | -          | Report + User Decision                           |

For Phase 2 details: [references/phase-2-quality-review.md](references/phase-2-quality-review.md)
For Phase 3 details: [references/phase-3-red-team.md](references/phase-3-red-team.md)
For report format: [templates/quality-report.md](templates/quality-report.md)
</workflow>

<agents>

## Agent Summary

### Phase 2 (5 Parallel)

| Agent             | Focus                                      |
| ----------------- | ------------------------------------------ |
| pattern-enforcer  | CLAUDE.md, claude-patterns/\* compliance   |
| react-quality     | Component design, hooks, state management  |
| architecture      | SOLID principles, separation of concerns   |
| readability       | 30-second rule, naming, complexity         |
| ai-smell-detector | Over-engineering, unnecessary abstractions |

### Phase 3 (Red Team)

| Agent          | Focus                                          |
| -------------- | ---------------------------------------------- |
| devil-advocate | Challenge all findings, reduce false positives |

</agents>

<severity>

## Severity Classification

| Level | Meaning                                        | Action                |
| ----- | ---------------------------------------------- | --------------------- |
| P0    | Critical quality (major pattern violations)    | Fix before commit     |
| P1    | High (SOLID violations, component structure)   | Recommend fixing      |
| P2    | Medium (readability, minor pattern deviations) | Safe to commit, track |
| P3    | Low (style preferences, optional improvements) | Optional              |

**Note**: Quality P0s are less urgent than bug P0s. A quality P0 means "this is very poorly written" not "this will break production."
</severity>

<approval_gates>

## Approval Gates

| Gate   | Phase | Question                                         |
| ------ | ----- | ------------------------------------------------ |
| Scope  | 1     | "Review these files?" (if >2000 lines)           |
| Action | 4     | "Improve now / Accept as-is / Discuss findings?" |

</approval_gates>

<scope>

## Scope Guidelines

| Size       | Lines     | Recommendation               |
| ---------- | --------- | ---------------------------- |
| Ideal      | 200-1000  | Fast, thorough               |
| Acceptable | 1000-2000 | May take 3-5 min             |
| Large      | >2000     | Warn user, suggest splitting |

**Include**: Changed files, related files
**Exclude**: Generated types, node_modules, build artifacts, test files
</scope>

<critical_rule>

## Critical Rule: Report ALL Issues

**NEVER dismiss findings because they are in "pre-existing code".**

Report ALL quality issues found in reviewed files regardless of when they were introduced. A pattern violation discovered today that was written months ago is still worth flagging.

**Invalid reasoning (DO NOT USE):**

- "This is pre-existing code unrelated to the current feature"
- "I didn't write this code in this session"
- "This pattern violation was there before my changes"

**Correct approach:**

- Report ALL quality issues found in the reviewed files
- Classify by severity (P0-P3) based on impact, not origin
- Let the user decide which to address
  </critical_rule>

<execution>

## Phase 1: Scope Discovery

1. Use `git status` to identify modified files
2. Filter to .ts, .tsx files (exclude generated types)
3. Count total lines
4. If >2000 lines, use AskUserQuestion to confirm scope

## Phase 2: Quality Review (5 Parallel)

Launch ALL 5 agents in a single message with multiple Task calls.
See [references/phase-2-quality-review.md](references/phase-2-quality-review.md) for agent prompts.

Provide each agent:

- List of files to review
- Relevant pattern file content (read claude-patterns/ first)

## Phase 3: Red Team Challenge

Launch 1 agent to challenge ALL findings from Phase 2.
See [references/phase-3-red-team.md](references/phase-3-red-team.md) for agent prompt.

Provide:

- All findings from Phase 2
- File list for context verification

Output: Validated findings with status (CONFIRMED/DOWNGRADED/DISMISSED/UPGRADED)

## Phase 4: Report + User Decision

1. Generate report using [templates/quality-report.md](templates/quality-report.md)
2. Present findings grouped by severity (P0, P1, P2, P3)
3. Use AskUserQuestion:

```typescript
{
  questions: [
    {
      question: "What would you like to do with these findings?",
      header: "Action",
      options: [
        {
          label: "Improve now",
          description: "Fix the quality issues before committing",
        },
        { label: "Accept as-is", description: "Proceed without changes" },
        {
          label: "Discuss findings",
          description: "Review specific issues in detail",
        },
      ],
      multiSelect: false,
    },
  ];
}
```

</execution>

<limitations>

## What This Skill Does NOT Check

- Bugs and correctness (use check-your-work)
- Security vulnerabilities (use check-your-work)
- Test coverage (use test runner)
- Build errors (use typecheck/lint)
- Runtime behavior (use manual testing)

**For comprehensive quality**: Run check-your-code + check-your-work + typecheck + tests
</limitations>

<quick_reference>

## Quick Reference

**Pattern files checked**:

- `CLAUDE.md`
- `react-typescript-antipatterns.md`
- `zod-form-patterns.md`
- `tanstack-query-patterns.md`
- `settings-patterns.md`
- `service-refactoring-patterns.md`

**Key quality dimensions**:

- Pattern adherence
- React component quality
- SOLID architecture
- Code readability
- AI over-engineering detection
  </quick_reference>

<version_history>

## Version History

- **v1.3.0** (2026-01-20): Add critical rule for pre-existing issues
  - Report ALL quality issues in reviewed files regardless of when introduced
  - Fix flawed "not my code" dismissal pattern

- **v1.2.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Eliminate vague pronouns ("That skill" → "check-your-work")

- **v1.1.0** (2025-01-11): Switch to P0-P3 severity system
  - Replaced A-F grading with P0-P3 severity (matches check-your-work)
  - Merged Phase 4+5 into single Phase 4

- **v1.0.0** (2025-01-11): Initial release
  - 5-phase workflow with red-team validation
  - 5 quality agents + 1 devil's advocate
  - Progressive disclosure with references/

</version_history>
