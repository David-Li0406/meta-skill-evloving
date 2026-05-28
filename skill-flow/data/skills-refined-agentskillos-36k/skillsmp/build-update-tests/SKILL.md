---
name: build-update-tests
description: Evaluate existing test coverage, identify gaps and pattern violations, then create or update comprehensive tests. Use when user says "build tests", "update tests", "test [component]", "add test coverage", or "check test coverage".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 3.2.0
---

# Build/Update Tests Skill

> Evaluate test coverage and create or update tests when gaps or pattern violations are identified.

<when_to_use>

## When to Use

Invoke when user says:

- "build tests for [file]"
- "update tests for [file]"
- "test [component/service/hook]"
- "add test coverage for [file]"
- "check test coverage"
  </when_to_use>

<workflow>
## Workflow Overview

| Phase | Action                                       | Reference                                                     |
| ----- | -------------------------------------------- | ------------------------------------------------------------- |
| 1     | Code Analysis & Risk Assessment              | [execution-phases.md](references/execution-phases.md#phase-1) |
| 2     | Existing Test Discovery & Pattern Compliance | [execution-phases.md](references/execution-phases.md#phase-2) |
| 3     | Test Design                                  | [execution-phases.md](references/execution-phases.md#phase-3) |
| 4     | Test Implementation                          | [execution-phases.md](references/execution-phases.md#phase-4) |
| 5     | Validation                                   | [execution-phases.md](references/execution-phases.md#phase-5) |
| 6     | Reporting                                    | [report-template.md](references/report-template.md)           |

For detailed phase instructions: [references/execution-phases.md](references/execution-phases.md)
</workflow>

<risk_matrix>

## Risk Matrix

| Risk Level | Characteristics                                  | Required Tests                   |
| ---------- | ------------------------------------------------ | -------------------------------- |
| **High**   | Business logic, mutations, forms, auth, payments | Unit + Integration + E2E         |
| **Medium** | Data fetching, filtering, validation, hooks      | Unit + Integration OR Unit + E2E |
| **Low**    | Pure utilities, formatters, type guards          | Unit only                        |

### Code Type Requirements

| Code Type                   | Required Tests           |
| --------------------------- | ------------------------ |
| User-facing component       | Unit + E2E               |
| Form component              | Unit + E2E               |
| Service with mutations      | Unit + Integration + E2E |
| Service read-only (simple)  | Unit                     |
| Service read-only (complex) | Unit + Integration       |
| Pure utility                | Unit                     |
| React hook (simple)         | Unit                     |
| React hook (complex)        | Unit + Integration       |
| Page component              | E2E                      |

</risk_matrix>

<test_locations>

## Test File Locations

| Level       | Pattern                                 | Example                                            |
| ----------- | --------------------------------------- | -------------------------------------------------- |
| Unit        | `src/**/__tests__/[name].test.{ts,tsx}` | `src/components/__tests__/SessionForm.test.tsx`    |
| Integration | `src/**/*.integration.test.{ts,tsx}`    | `src/services/__tests__/email.integration.test.ts` |
| E2E         | `playwright/tests/*.spec.ts`            | `playwright/tests/session-creation.spec.ts`        |

</test_locations>

<pattern_compliance>

## Pattern Compliance

Check these pattern documents before writing tests:

- `claude-patterns/testing-patterns.md` (React component unit tests)
- `claude-patterns/vitest-testing-patterns.md` (Service/utility unit tests)
- `claude-patterns/playwright-best-practices.md` (E2E tests)

### Priority Order

| Priority          | Type                 | Examples                                                              |
| ----------------- | -------------------- | --------------------------------------------------------------------- |
| P0 (Must Fix)     | Safety & Correctness | No direct DB inserts in E2E, proper async handling, worker validation |
| P1 (Should Fix)   | Maintainability      | test.step() usage, proper cleanup, comprehensive assertions           |
| P2 (Nice to Have) | Best Practices       | Naming conventions, organization, comments                            |

Fix P0 violations before creating new tests—a test that violates patterns is worse than no test.

For detailed patterns: [references/best-practices.md](references/best-practices.md)
</pattern_compliance>

<invocation>
## Invocation

Basic:

```
Use build-update-tests skill for src/components/MyComponent.tsx
```

With requirements:

```
Use build-update-tests for src/services/email.service.ts with critical flows from docs/email-requirements.md
```

</invocation>

<commands>
## Commands

```bash
# Run unit tests for specific file
npm run test:unit -- [test-file-name]

# Run all unit tests
npm run test:unit

# Run E2E tests
npx playwright test [spec-file]
```

</commands>

<output>
## Output

Produce a comprehensive report using [references/report-template.md](references/report-template.md):

1. **Evaluation Phase**: Risk assessment, test discovery, pattern compliance, gap analysis
2. **Implementation Phase**: Actions taken, tests created/updated, coverage achieved
3. **Summary**: Strengths, warnings, gaps fixed, recommendations
   </output>

<approval_gates>

## Approval Gates

| Gate | Phase | Question                                                 |
| ---- | ----- | -------------------------------------------------------- |
| None | -     | This skill runs autonomously without user approval gates |

Note: Test creation is non-destructive. User reviews output report and decides what to keep.
</approval_gates>

<safety_rules>

## Safety Rules

1. **Never delete existing passing tests** - only add or update
2. **Fix P0 pattern violations before creating new tests** - bad tests are worse than no tests
3. **Preserve existing test structure** - don't reorganize without clear benefit
   </safety_rules>

<limitations>
## Limitations

- Cannot create E2E tests without understanding full user workflow
- Cannot determine test priority without requirements documentation
- Complex mocking may require code refactoring for testability
  </limitations>

<quick_reference>

## Quick Reference

```bash
# Find existing tests
glob "src/**/__tests__/**/*.test.{ts,tsx}"
glob "playwright/tests/*.spec.ts"

# Check for pattern docs
cat claude-patterns/testing-patterns.md
cat claude-patterns/playwright-best-practices.md
```

</quick_reference>

<references>
## References

- [references/execution-phases.md](references/execution-phases.md) - Detailed 6-phase workflow
- [references/report-template.md](references/report-template.md) - Output report format
- [references/best-practices.md](references/best-practices.md) - Testing patterns and examples
  </references>

<version_history>

## Version History

- **v3.2.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Soften directive language per Opus 4.5 guidance

- **v3.1.0** (2025-12-28): Added missing sections per skill-authoring-patterns audit
  - Added trigger phrases to frontmatter description
  - Added `<approval_gates>` section
  - Added `<safety_rules>` section
  - Added `<references>` section

- **v3.0.0** (2025-12-28): Refactored to follow skill-authoring-patterns
  - Reduced from 850 to ~180 lines
  - Created references/: execution-phases.md, report-template.md, best-practices.md
  - Added XML tags for structure
  - Converted to imperative writing style

- **v2.0.0** (2025-11-15): Combined audit and implementation workflows

- **v1.0.0** (2025-10-01): Initial release
  </version_history>
