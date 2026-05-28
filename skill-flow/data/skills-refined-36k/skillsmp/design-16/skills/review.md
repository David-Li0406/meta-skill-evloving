---
name: design-review
description: Review implementation against spec for compliance. USE WHEN review implementation, check compliance, verify spec implementation.
context: fork
---

# Design Review

Reviews an implementation against its source specification for compliance. Runs in isolated context to avoid bloating main conversation with file scan details.

## Why Forked Context

- Implementation scanning can touch many files
- Cross-referencing requirements to code is verbose
- Test output and linting results are detailed
- Returns focused compliance summary to main context

## Usage

```
/design-review specs/feature-spec.md ./src/feature/
/design-review specs/api-spec.md ./api/ --check-conventions
```

## Execution

**Step 1: Load spec requirements**
- Parse spec file for requirements (bullet points, acceptance criteria)
- Extract validation criteria
- Load CONVENTIONS.md if present

**Step 2: Analyze implementation**
- Scan implementation path for relevant files
- Check for test coverage
- Look for validation commands
- Check convention compliance

**Step 3: Cross-reference**
- Map requirements to implementation
- Identify gaps
- Check edge case handling

**Step 4: Run validation commands**
- Execute test suites
- Check linting
- Run type checks

**Step 5: Generate compliance report**

## Output Format

```
Implementation Review
=====================

Spec: specs/feature-spec.md
Implementation: ./src/feature/

Requirements Coverage
---------------------
[x] Requirement 1: User can submit form
    Status: IMPLEMENTED
    Files: src/feature/form.tsx, src/feature/submit.ts
    Tests: tests/feature/form.test.ts

[x] Requirement 2: Form validates email format
    Status: IMPLEMENTED
    Files: src/feature/validation.ts
    Tests: tests/feature/validation.test.ts

[ ] Requirement 3: Error messages display inline
    Status: PARTIAL
    Files: src/feature/errors.tsx
    Missing: No test coverage for error display

[!] Requirement 4: Rate limit submissions
    Status: NOT IMPLEMENTED
    Note: No rate limiting found in codebase

Convention Compliance
--------------------
[x] TypeScript strict mode enabled
[x] ESLint rules passing
[x] Test coverage >= 80%
[ ] Component naming conventions - 2 violations
    - SubmitBtn.tsx should be SubmitButton.tsx
    - errorMsg.tsx should be ErrorMessage.tsx

Validation Commands
------------------
npm test: PASS (45/45)
npm run lint: PASS
npm run typecheck: PASS

SUMMARY
-------
Requirements: 3/4 implemented (75%)
Conventions: 3/4 passing (75%)
Tests: PASS

Status: NEEDS ATTENTION
- Complete rate limiting implementation
- Fix naming convention violations
- Add error display tests
```

## Return to Main Context

After completion, returns concise summary:
```
Review Complete
===============
Spec: specs/feature-spec.md
Implementation: ./src/feature/

Requirements: 3/4 (75%)
Conventions: 3/4 (75%)
Tests: PASS

Status: NEEDS ATTENTION

Gaps:
1. Rate limiting not implemented
2. 2 naming convention violations
3. Missing error display tests

Full report saved to: docs/design/reviews/feature-review-2026-01-19.md
```

## Related Commands

- `/design validate` — Check spec before review
- `/design orchestrate` — Full pipeline including review

---

*Forked skill — implementation scan isolated from main context*
