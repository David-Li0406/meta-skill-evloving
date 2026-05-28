---
name: tdd-refactor
description: Use this skill to improve code quality while maintaining tests during the TDD REFACTOR phase, ensuring all tests remain GREEN.
---

# TDD REFACTOR Phase

This skill focuses on improving code quality while maintaining tests.

## Progress Checklist

Track your progress with the following checklist:

```
REFACTOR Progress:
- [ ] Confirm latest Cycle document
- [ ] Ensure all current tests PASS
- [ ] Perform refactoring
- [ ] Run tests → confirm success
- [ ] Update Cycle document
- [ ] Proceed to REVIEW phase
```

## Prohibited Actions

- Changes that break tests
- Adding new features (to be done in the next cycle)
- Deleting or modifying tests

## Workflow

### Step 1: Confirm Cycle Document

```bash
ls -t docs/cycles/*.md 2>/dev/null | head -1
```

### Step 2: Verify Tests

```bash
php artisan test  # PHP
pytest            # Python
```

Ensure all tests PASS before proceeding.

### Step 3: Refactoring

Focus on the following areas:

| Item          | Example                          |
|---------------|----------------------------------|
| DRY           | Consolidate duplicate code       |
| Constantization | Remove magic numbers           |
| Method Splitting | Split long methods            |
| Naming        | Improve variable and method names|

### Step 4: Run Tests → Confirm Success

**Expectation**: All tests must be **successful**.

### Verification Gate

| Check        | Condition | Requirement |
|--------------|-----------|-------------|
| Tests        | All PASS  | Mandatory    |
| Static Analysis | 0 Errors | Mandatory    |
| Formatting   | Applied   | Mandatory    |

If all checks pass, proceed to REVIEW. If any fail, fix and retry.

### Step 5: Completion → Guide to REVIEW

```
================================================================================
REFACTOR completed
================================================================================
Code quality has been improved. All tests PASS.
Next: Proceed to REVIEW phase (quality verification)
================================================================================
```

## Purpose of This Skill

- Maintain a safety net of GREEN tests while improving code, tests, and specifications.
- Systematically address internal structure debt to enhance "changeability."

## Preconditions (Stop if not met)

- **All tests must be GREEN** (confirmed just before).
- Changes should be internal improvements, not specification changes.
  - If specification changes are necessary, update the Spec and test expectations first with user consent (treat as a separate RED).

## Essential Focus Areas

- If Rust code is involved:
  - Use `cargo fix` for mechanical fixes.
  - Format with `cargo fmt --all`.
  - Address warnings with `cargo clippy --workspace --all-targets --all-features -- -D warnings`.
- If Markdown documents are involved:
  - Use `markdownlint-cli2 --fix` for mechanical fixes.

## Guidelines (Must Follow)

1. **Declare Phase**
   - `Current Phase: REFACTOR`
2. **Limit Refactoring Scope**
   - Start with up to 3 TODOs recorded from the last GREEN.
3. **Make Small Improvements → Test Immediately**
   - Changes should be small and explainable.
   - Run tests after every 1-3 steps to maintain GREEN.
4. **Target Examples (if necessary)**
   - Eliminate duplication (DRY), improve naming, separate concerns (SoC), simplify complex conditions, reduce unnecessary dependencies.
   - Test code should also be improved without changing expected behavior.
5. **Improve Spec Representation (as needed)**
   - Maintain traceability between Spec-ID and tests.

## Guardrails (What Not to Do)

- Do not mix changes that alter expected behavior with refactoring.
- Avoid starting large-scale redesigns (split into separate PRs/Specs).
- Limit options presented to avoid unnecessary discussions; proceed with default proposals and clarify exceptions only.

## Output Format

1. `Current Phase: REFACTOR`
2. `Refactoring Purpose:`
3. `Actions Taken:` (bullet points detailing improvements made)
4. `Impact Scope:` (main file paths)
5. `Execution Command:` (commands executed)
6. `Result:` (summary of all tests being GREEN)
7. `Next:` (if there are any RED candidates, specify one at the Spec-ID level)