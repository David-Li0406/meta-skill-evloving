---
name: check-your-work
description: Orchestrates 6 quality agents in parallel (duplicate-detector, jenny, deep-bug-hunter, security, performance, correctness) with severity validation. Use when user says "check your work", "review what we wrote", "quality check", or after writing new features.
allowed-tools: Task, Read, Glob, Grep, Bash, AskUserQuestion
version: 4.2.0
---

# Check Your Work

> Orchestrate specialized agents to detect bugs, security issues, and quality problems in code changes.

<when_to_use>

## When to Use

Invoke when user says:

- "check your work"
- "review what we wrote"
- "quality check the new code"
- "check for bugs in [files/feature]"
- After completing feature implementation
- Before committing significant changes
  </when_to_use>

<workflow>
## Workflow Overview

| Phase | Agents        | Action                                                               |
| ----- | ------------- | -------------------------------------------------------------------- |
| 1     | -             | Scope Discovery (identify files)                                     |
| 2     | 6 parallel    | All Checks (duplicate-detector, jenny, deep-bug-hunter, 3 reviewers) |
| 3     | up to 3       | Severity Validation (one agent per P0/P1/P2 level with findings)     |
| 4     | 1 conditional | Deep Investigation (root cause for validated P0)                     |
| 5     | -             | Consolidated Report + User Decision                                  |

For Phase 2 details: [references/phase-2-quality-checks.md](references/phase-2-quality-checks.md)
For Phase 3 details: [references/phase-3-validation.md](references/phase-3-validation.md)
For report format: [references/consolidated-report.md](references/consolidated-report.md)
</workflow>

<agents>
## Agent Summary

### Phase 2 (6 Parallel)

| Agent                   | Focus                                         |
| ----------------------- | --------------------------------------------- |
| duplicate-code-detector | Reimplemented utilities/services              |
| jenny                   | User voice - did we build what was requested? |
| deep-bug-hunter         | Logic errors, race conditions, edge cases     |
| Security Reviewer       | SQL injection, org_id isolation, XSS, PII     |
| Performance Reviewer    | Memory leaks, bug-causing antipatterns        |
| Correctness Reviewer    | Logic errors, null handling, async issues     |

### Phase 3 (up to 3 Parallel)

| Agent        | Focus                                          |
| ------------ | ---------------------------------------------- |
| p0-validator | Validates P0 findings against codebase context |
| p1-validator | Validates P1 findings against codebase context |
| p2-validator | Validates P2 findings against codebase context |

Only spawns agents for severity levels that have findings.

</agents>

<severity>
## Severity Classification

| Level | Meaning                                        | Action                              |
| ----- | ---------------------------------------------- | ----------------------------------- |
| P0    | Critical (security, data corruption, outage)   | **DO NOT COMMIT** - fix immediately |
| P1    | High (logic errors, performance, workflows)    | Recommend fixing before commit      |
| P2    | Medium (duplications, antipatterns, spec gaps) | Safe to commit, track issues        |
| P3    | Low (style, minor improvements)                | Optional improvements               |

</severity>

<approval_gates>

## Approval Gates

| Gate        | Phase | Question                                               |
| ----------- | ----- | ------------------------------------------------------ |
| Scope       | 1     | "Confirm files to review?" (if >2000 lines)            |
| Remediation | 5     | "Fix P0 now / Fix P0+P1 / Create todos / Report only?" |

</approval_gates>

<scope>
## Scope Guidelines

| Size       | Lines     | Recommendation               |
| ---------- | --------- | ---------------------------- |
| Ideal      | 200-1000  | Fast, thorough               |
| Acceptable | 1000-2000 | May take 3-5 min             |
| Large      | >2000     | Warn user, suggest splitting |

**Include**: Changed files, related files, test files
**Exclude**: Generated types, node_modules, build artifacts
</scope>

<critical_rule>

## Critical Rule: Report ALL Bugs

**NEVER dismiss findings because they are in "pre-existing code".**

Report ALL bugs found in reviewed files regardless of when they were introduced. A bug discovered today that was written 3 months ago is still a bug worth fixing.

**Invalid reasoning (DO NOT USE):**

- "This is pre-existing code unrelated to the current feature"
- "I didn't introduce this bug in this session"
- "This code was written before my changes"

**Correct approach:**

- Report ALL bugs found in the reviewed files
- Classify by severity (P0-P3) based on impact, not origin
- Let the user decide which to fix
  </critical_rule>

<limitations>
## What This Skill Does NOT Check

- Runtime behavior (use manual testing)
- Business logic correctness (requires domain knowledge)
- Test coverage (use test runner)
- Build errors (use typecheck/lint)
- Database migrations (use migration-test-and-push skill)

**For comprehensive quality**: Run check-your-work + typecheck + lint + tests
</limitations>

<quick_reference>

## Quick Reference

**Pattern files enforced**:

- `react-typescript-antipatterns.md`
- `CLAUDE.md`
- `zod-form-patterns.md`
- `tanstack-query-patterns.md`
- `performance-patterns.md`
  </quick_reference>

<references>
## References

- [references/phase-2-quality-checks.md](references/phase-2-quality-checks.md) - All 6 agents for parallel analysis
- [references/phase-3-validation.md](references/phase-3-validation.md) - Severity validation (up to 3 parallel by level)
- [references/consolidated-report.md](references/consolidated-report.md) - Finding interface and report format
  </references>

<version_history>

## Version History

- **v4.2.0** (2026-01-20): Add critical rule for pre-existing bugs
  - Report ALL bugs in reviewed files regardless of when introduced
  - Fix flawed "not my code" dismissal pattern

- **v4.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title

- **v4.0.0** (2025-01-11): Maximum parallelization + unified validation
  - Merged Phase 2 + Phase 3 into single Phase 2 (6 parallel agents)
  - Phase 3 validation now spawns up to 3 agents (one per P0/P1/P2 level)
  - Consistent with check-your-code P0-P3 severity system

- **v3.0.0** (2025-12-28): Refactored to follow skill-authoring-patterns

- **v2.0.0** (2025-10-31): Added severity validation

- **v1.0.0** (2025-10-26): Initial release
  </version_history>
