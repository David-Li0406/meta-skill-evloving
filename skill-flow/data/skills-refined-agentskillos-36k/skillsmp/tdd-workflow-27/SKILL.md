---
name: tdd-workflow
description: |
  Test-Driven Development (TDD) workflow for ultrawork tasks with approach: "tdd".
  Enforces RED-GREEN-REFACTOR cycle with gate hooks and evidence requirements.
  Required knowledge for worker agents implementing TDD tasks.
---

# TDD Workflow

Test-Driven Development (TDD) workflow for tasks marked with `approach: "tdd"`.

**CRITICAL: TDD tasks MUST follow this exact sequence. Gate hooks will block out-of-order operations.**

---

## Scoped vs Full Test Execution

**During TDD phases (RED/GREEN/REFACTOR):**
- Run **scoped tests** only (specific test file or pattern)
- Fast feedback loop for the feature being developed
- Full test suite is deferred to VERIFY task

**During VERIFICATION phase:**
- Verifier runs **full test suite** (`npm test` without scope)
- Ensures no regressions across entire codebase
- PASS/FAIL determination based on complete test coverage

**Why scoped execution?**
1. **Speed**: Test only what changed, not entire suite
2. **Focus**: TDD cycle targets specific behavior
3. **Separation**: Task implementation vs system verification

### Using test_scope from Task

When task has `test_scope` field, use it for scoped execution:

```bash
# Read test_scope from task
TEST_SCOPE=$(bun "{SCRIPTS_PATH}/task-get.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} --field test_scope)

# Run scoped test
npm test -- {test_scope}
```

**Example task.json:**
```json
{
  "id": "3",
  "subject": "Add input validation",
  "approach": "tdd",
  "test_scope": "tests/validation.test.ts"
}
```

If `test_scope` is not set, use the test file path you created.

---

## TDD Phase 1: RED - Write Failing Test

1. **Create test file FIRST** (before any implementation code)
2. Write test for expected behavior
3. Run test and **VERIFY IT FAILS**

```bash
# Record test creation
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "TDD-RED: Created test file tests/validateUser.test.ts"

# Run SCOPED test - MUST FAIL
npm test -- tests/validateUser.test.ts

# Record failure (expected)
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "TDD-RED: npm test -- tests/validateUser.test.ts (exit code 1)"
```

**Evidence Required:**
- Test file path created
- Scoped test execution output showing failure
- Exit code 1 (expected)
- Evidence includes full test command with scope

---

## TDD Phase 2: GREEN - Minimal Implementation

1. Write **MINIMAL** code to make the test pass
2. Do NOT add extra functionality beyond what test requires
3. Run test and **VERIFY IT PASSES**

```bash
# Record implementation
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "TDD-GREEN: Implemented src/validateUser.ts"

# Run SCOPED test - MUST PASS
npm test -- tests/validateUser.test.ts

# Record success
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "TDD-GREEN: npm test -- tests/validateUser.test.ts (exit code 0)"
```

**Evidence Required:**
- Implementation file path
- Scoped test execution output showing pass
- Exit code 0
- Evidence includes full test command with scope

---

## TDD Phase 3: REFACTOR (Optional)

1. Improve code quality (naming, structure, performance)
2. Run scoped tests again to ensure they still pass
3. Record any refactoring done

```bash
# Run SCOPED test after refactoring
npm test -- tests/validateUser.test.ts

# Record refactoring
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --add-evidence "TDD-REFACTOR: Renamed variables, npm test -- tests/validateUser.test.ts (exit code 0)"
```

---

## TDD Evidence Chain

A complete TDD task MUST have this evidence sequence:

```
1. TDD-RED: Test file created
2. TDD-RED: Scoped test execution failed (exit code 1, includes test scope)
3. TDD-GREEN: Implementation created
4. TDD-GREEN: Scoped test execution passed (exit code 0, includes test scope)
5. (Optional) TDD-REFACTOR: Improvements made, scoped tests still pass
```

**Evidence format MUST include:**
- Full test command with scope (e.g., `npm test -- tests/feature.test.ts`)
- Exit code in parentheses
- Phase prefix (TDD-RED, TDD-GREEN, TDD-REFACTOR)

**Verification will FAIL if:**
- Implementation evidence appears before TDD-RED evidence
- Missing TDD-RED or TDD-GREEN evidence
- Test never failed (suggests code-first, not test-first)
- Evidence missing test scope or exit code

---

## Gate Enforcement

The `gate-enforcement.js` hook blocks out-of-order TDD operations:

**During EXECUTION phase (TDD tasks only):**
- ✅ Allow: Test files first (`*.test.*`, `*.spec.*`, `__tests__/*`)
- ❌ Block: Implementation files before TDD-RED evidence

**Detection Logic:**
1. Hook reads task file to check `approach: "tdd"`
2. Searches evidence array for "TDD-RED" prefix
3. If TDD task + no RED evidence → blocks Write/Edit on non-test files

**Error Message:**
```
TDD gate: Cannot write implementation before RED phase
Required evidence: "TDD-RED: Test fails as expected (exit code 1)"
Current file: src/validateUser.ts (non-test file)
```

---

## TDD Task Completion

After all phases complete:

```bash
bun "{SCRIPTS_PATH}/task-update.js" --session ${CLAUDE_SESSION_ID} --id {TASK_ID} \
  --status resolved \
  --add-evidence "TDD complete: RED→GREEN→REFACTOR cycle finished"
```

---

## Quick Reference

| Phase | Action | Evidence Prefix | Exit Code |
|-------|--------|----------------|-----------|
| RED | Write test, verify failure | `TDD-RED: ...` | 1 (fail) |
| GREEN | Write minimal impl, verify pass | `TDD-GREEN: ...` | 0 (pass) |
| REFACTOR | Improve code, tests still pass | `TDD-REFACTOR: ...` | 0 (pass) |

---

## Example Evidence Sequence

```json
{
  "evidence": [
    "TDD-RED: Created test file tests/auth.test.ts",
    "TDD-RED: npm test -- tests/auth.test.ts (exit code 1)",
    "TDD-GREEN: Implemented src/auth.ts",
    "TDD-GREEN: npm test -- tests/auth.test.ts (exit code 0)",
    "TDD-REFACTOR: Extracted helper, npm test -- tests/auth.test.ts (exit code 0)"
  ]
}
```

**Note**: Full test suite (`npm test` without scope) is run only during VERIFICATION phase by the verifier agent.
