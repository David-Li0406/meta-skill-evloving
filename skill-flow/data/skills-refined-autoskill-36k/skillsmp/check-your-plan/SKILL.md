---
name: check-your-plan
description: Validates AI implementation plans before execution. Use when user says "check your plan", "validate this plan", "review the plan", or "is this plan good". Launches 5 parallel validators + devil's advocate.
allowed-tools: Task, Read, Glob, Grep, AskUserQuestion
version: 1.1.0
---

# Check Your Plan

> Validate AI-generated implementation plans before execution to catch hallucinations, pattern violations, and scope creep.

<when_to_use>

## When to Use

Invoke when user says:

- "check your plan"
- "validate this plan"
- "review the plan"
- "is this plan good"
- After Claude presents an implementation plan
- Before starting significant implementation work

**Different from check-your-code/work**: check-your-code and check-your-work review written code. check-your-plan reviews the PLAN before code is written.
</when_to_use>

<workflow>

## Workflow Overview

| Phase | Agents     | Action                                        |
| ----- | ---------- | --------------------------------------------- |
| 1     | -          | Plan Discovery (locate plan, extract content) |
| 2     | 5 parallel | Plan Validation (specialized reviewers)       |
| 3     | 1          | Devil's Advocate (challenge all findings)     |
| 4     | -          | Report + User Decision                        |

For Phase 2 details: [references/phase-2-plan-validators.md](references/phase-2-plan-validators.md)
For Phase 3 details: [references/phase-3-devil-advocate.md](references/phase-3-devil-advocate.md)
For report format: [templates/plan-assessment.md](templates/plan-assessment.md)
</workflow>

<agents>

## Agent Summary

### Phase 2 (5 Parallel)

| Agent                      | Focus                                                   |
| -------------------------- | ------------------------------------------------------- |
| completeness-checker       | All requirements addressed? 70% problem? Vague steps?   |
| pattern-compliance-checker | CLAUDE.md rules? TanStack Query? Zod? File conventions? |
| feasibility-checker        | Hallucinated APIs? Real file paths? Valid dependencies? |
| risk-assessor              | Security gaps? Missing error handling? Rollback plan?   |
| scope-discipline-checker   | Over-engineering? Scope creep? Simplest solution?       |

### Phase 3 (Devil's Advocate)

| Agent          | Focus                                          |
| -------------- | ---------------------------------------------- |
| devil-advocate | Challenge all findings, reduce false positives |

</agents>

<severity>

## Severity Classification

| Level | Meaning                 | Example                                            |
| ----- | ----------------------- | -------------------------------------------------- |
| P0    | Plan will fail          | Hallucinated API, wrong file path, missing dep     |
| P1    | Major pattern violation | useState+service, handwritten interface, no org_id |
| P2    | Could be better         | Minor pattern deviation, missing edge case         |
| P3    | Suggestion              | Over-engineering detected, style preference        |

**P0 requires evidence**: "File X doesn't exist" not just "might be wrong"
</severity>

<approval_gates>

## Approval Gates

| Gate   | Phase | Question                                    |
| ------ | ----- | ------------------------------------------- |
| Scope  | 1     | "Review this plan?" (if plan >50 lines)     |
| Action | 4     | "Revise plan / Proceed as-is / Start over?" |

</approval_gates>

<execution>

## Phase 1: Plan Discovery

1. Locate the plan to validate:
   - Check for plan file path in conversation context
   - Look in `.claude/plans/` for recent plan files
   - If no plan file, check if plan was stated inline in conversation

2. Extract plan content and metadata:
   - Files to be modified
   - Steps/tasks count
   - Dependencies mentioned

3. If plan >50 lines, use AskUserQuestion to confirm scope

## Phase 2: Plan Validation (5 Parallel)

Launch ALL 5 agents in a single message with multiple Task calls.
See [references/phase-2-plan-validators.md](references/phase-2-plan-validators.md) for agent prompts.

Provide each agent:

- Full plan content
- Original user request (from conversation context)
- Relevant pattern file content (load from claude-patterns/)

## Phase 3: Devil's Advocate

Launch 1 agent to challenge ALL findings from Phase 2.
See [references/phase-3-devil-advocate.md](references/phase-3-devil-advocate.md) for agent prompt.

Provide:

- All findings from Phase 2
- Plan content for context verification

Output: Validated findings with status (CONFIRMED/DOWNGRADED/DISMISSED/UPGRADED)

## Phase 4: Report + User Decision

1. Generate report using [templates/plan-assessment.md](templates/plan-assessment.md)
2. Present findings grouped by severity (P0, P1, P2, P3)
3. Use AskUserQuestion:

```typescript
{
  questions: [
    {
      question: "How would you like to proceed with this plan?",
      header: "Action",
      options: [
        {
          label: "Revise plan",
          description:
            "Update plan to address P0/P1 findings before implementing",
        },
        {
          label: "Proceed as-is",
          description: "Accept the plan and start implementation",
        },
        {
          label: "Start over",
          description: "Request a completely new plan approach",
        },
      ],
      multiSelect: false,
    },
  ];
}
```

</execution>

<key_checks>

## Key Validation Checks

### Completeness (The "70% Problem")

- Are hard parts (error handling, edge cases, testing) as detailed as easy parts?
- Does plan address ALL original requirements?
- Are there vague steps like "implement the business logic"?

### Pattern Compliance

- TanStack Query for data fetching (not useState + service calls)
- Zod schemas in `src/types/forms/` (not handwritten interfaces)
- `mutateAsync` in modal forms (not `mutate()`)
- `contactFilters.ts` for contact filtering (not inline filters)
- `notifyApi` for notifications (not direct useToast)
- `organization_id` filter on all queries

### Feasibility (Hallucination Detection)

- Do referenced files actually exist?
- Do referenced functions have correct signatures?
- Are dependencies at correct versions?
- Are API endpoints real?

### Risk Assessment

- Missing security considerations?
- No error handling for failure scenarios?
- No rollback plan for data mutations?
- No testing strategy?

### Scope Discipline

- Does plan stay focused on original request?
- Signs of over-engineering (abstractions for one-time ops)?
- Signs of scope creep (unrelated "improvements")?

</key_checks>

<limitations>

## What This Skill Does NOT Check

- Runtime behavior (requires execution)
- Actual code quality (use check-your-code after implementation)
- Bug detection (use check-your-work after implementation)
- Test coverage (use test runner)
- Build errors (use typecheck/lint)

**For comprehensive quality**: check-your-plan (before) + check-your-code + check-your-work (after)
</limitations>

<quick_reference>

## Quick Reference

**Pattern files checked for compliance**:

- `CLAUDE.md`
- `tanstack-query-patterns.md`
- `zod-form-patterns.md`
- `react-typescript-antipatterns.md`
- `modal-form-patterns.md`
- `notification-patterns.md`
- `settings-patterns.md`

**Common P0 findings**:

- Hallucinated file path: `src/services/foo.ts` doesn't exist
- Hallucinated API: `useAccounts()` hook doesn't exist
- Missing dependency: Plan uses package not in package.json

**Common P1 findings**:

- useState + service call pattern (should use TanStack Query)
- Handwritten interface (should use Zod schema)
- Missing org_id filter (security violation)
  </quick_reference>

<references>

## References

- [references/phase-2-plan-validators.md](references/phase-2-plan-validators.md) - All 5 validator agents
- [references/phase-3-devil-advocate.md](references/phase-3-devil-advocate.md) - Challenge agent
- [templates/plan-assessment.md](templates/plan-assessment.md) - Report format
  </references>

<version_history>

## Version History

- **v1.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Eliminate vague pronouns ("Those skills" → explicit skill names)

- **v1.0.0** (2025-01-12): Initial release
  - 4-phase workflow with 5 parallel validators
  - Devil's advocate challenge phase
  - P0-P3 severity aligned with codebase patterns
  - Based on research: 3 Cs framework, 70% problem detection, hallucination checking

</version_history>
