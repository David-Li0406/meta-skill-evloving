---
name: planning
description: Provides expertise on how to plan for work in this repo
---


## Overview

This skill provides comprehensive guidance on how to plan a new feature in this repo.

- We always use a Test-Driven Development (TDD) approach
- We use **Vitest** (TypeScript) to test **bash** source code
- We maintain both **automated tests** and **visual demos**
- We track our progress through the phased based work with a LOG file

---

## Types of Testing

### 1. Automated Tests (Vitest)

Automated tests verify the **actual behavior** of bash functions during execution using TypeScript/Vitest.

**When to use:**

- Testing bash function outputs with various inputs
- Verifying error handling and edge cases
- Checking exit codes and command behavior
- Validating logic and algorithms in bash scripts
- Any test that can produce a boolean pass/fail result

**Tools:**

- Test runner: Vitest (`pnpm test`)
- Test files: `*.test.ts` in TypeScript
- Bash helper: `tests/helpers/bash.ts` for executing bash from TypeScript

**Example:**

```typescript
import { describe, it, expect } from 'vitest'
import { sourcedBash } from './helpers/bash'

describe('list utilities', () => {
  it('should retain items with matching prefixes', () => {
    const result = sourcedBash('./utils/lists.sh', `
      items=("apple" "banana" "cherry")
      retain_prefixes_ref items "a"
    `)
    expect(result).toContain('apple')
    expect(result).not.toContain('cherry')
  })
})
```

### 2. Visual Demos (Bash)

Visual demonstration scripts provide interactive examples that require human inspection.

**When to use:**

- Color output testing (visual verification needed)
- Interactive demonstrations of features
- Showcasing functionality to users
- Manual testing during development

**Tools:**

- Demo scripts: `*-demo.sh` or `showcase-*.sh` in `tests/demos/`
- Run directly: `./tests/demos/color-demo.sh`

---

## Decision Framework: Which Tests to Write?

**Use Automated Tests** (`*.test.ts`) when:
- Boolean pass/fail verification is possible
- Testing function behavior and logic
- CI/CD integration needed
- Regression testing required

**Use Demo Scripts** (`*.sh` in `tests/demos/`) when:
- Visual inspection is required (e.g., color output)
- Interactive demonstration of features
- Showcasing functionality to users

**Rule of thumb:** When in doubt, write automated tests. Only use demos when automation isn't feasible.

---

## Test Organization and Structure

### File Structure

Tests use a hybrid approach: TypeScript for automation, bash for visual demos.

```text
tests/
├── demos/                  # Visual demonstration scripts (bash)
│   ├── color-demo.sh      # Interactive color showcase
│   └── showcase.sh        # General feature demonstrations
├── helpers/               # TypeScript test utilities
│   ├── bash.ts           # Bash execution helpers
│   ├── bash.test.ts      # Tests for bash helper itself
│   └── example.test.ts   # Example/documentation
├── WIP/                   # Work in progress (during TDD phases)
│   └── *.test.ts         # In-progress tests
├── *.test.ts             # Automated Vitest tests
└── README.md             # Testing documentation
```

### Naming Conventions

- **Automated tests:** `*.test.ts` (TypeScript files testing bash functions)
- **Demo scripts:** `*-demo.sh` or `showcase-*.sh` (bash files for visual inspection)
- **Test descriptions:**
  - Use "should" statements: `it("should return true when...)`
  - Be specific about the scenario: `it("should handle empty strings")`
  - Describe the behavior, not the implementation

### Test Structure Principles

**DO:**

- Keep tests focused on a single behavior
- Use descriptive test names that explain the scenario
- Group related tests in `describe` blocks
- Test edge cases (empty, null, undefined, boundary values)
- Test error conditions and failure modes
- Make tests independent (no shared state between tests)

**DON'T:**

- Test implementation details (test behavior, not internals)
- Add logic to tests (no conditionals, loops, or complex computations)
- Share mutable state between tests
- Make tests depend on execution order
- Skip asserting the results (every test needs expectations)

---

## Plans using TDD Workflow for Phase-Based Development

When implementing a new feature, ALWAYS follow this comprehensive TDD workflow:

### Phase Structure Overview

0. **PLAN FORMALIZATION** - Improve upon the user's plan definition
1. **SNAPSHOT** - Capture current test state
2. **CREATE LOG** - Document starting position
3. **WRITE TESTS** - Create tests first (TDD)
4. **IMPLEMENTATION** - Build to pass tests
5. **CLOSE OUT** - Verify, migrate tests, document completion

---

### Step 0: PLAN FORMALIZATION

When a user provides you with a new feature or plan idea, the first step is always to take that as an input into making a more structured and formalized plan:

1. The initial request for a plan/feature/etc. should be analyzed and a reasonable name for the plan should be made.
    - A good name is between a few words up to a full sentence but never more. Less is more but make sure it's descriptive.
2. Unless the plan is VERY simple the plan should be broken up into multiple phases
    - Each phase of the plan should follow a TDD workflow unless there is an explicit reason not to
3. Your improved plan should be written as a Markdown file with a filename of:
    - `.ai/plans/${YYYY}-${MM}-${DD}-${NAME}.md`
    - all date based variables should use the user's local time not UTC
    - Formatting should follow good Markdown practices:
        - Never use a code block without a name; you can use `txt` if you are simply using the block as a text output.
        - Always include a blank line after headings
    - Once you've written the plan you should ask the user to review it unless they have expressly stated that you can execute it upon completion of the plan
        - If the user HAS granted you the right to execute the plan without review then you should execute the plan phase by phase
        - Never start a new phase if the previous phase is somehow incomplete; this indicates that you should checkpoint with the user

The remaining steps represent how each PHASE of the plan should be structured.

### Step 1: PHASE SNAPSHOT

Capture the current state of all tests before making any changes.

**Actions:**

1. Run all tests:

   ```bash
   pnpm test
   ```

2. Create a simple XML or text representation of test results
3. Document any existing failures (these are your baseline - don't fix yet)

**Purpose:** Establish a clear baseline so you can detect regressions and measure progress.

---

### Step 2: CREATE LOG

Create a log file to track this phase of work.

**Actions:**

1. Create log file with naming convention:

   ```bash
   mkdir -p .ai/logs
   touch .ai/logs/YYYY-MM-planName-phaseN-log.md
   ```

   Example: `.ai/logs/2025-10-symbol-filtering-phase1-log.md`

2. Add `## Starting Test Position` section with XML code block containing test results from SNAPSHOT

3. Add `## Repo Starting Position` section

4. Run the start-position script to capture git state:

   ```bash
   bun run .claude/skills/planning/scripts/start-position.ts planName phaseNumber
   ```

   This returns markdown content showing:
   - Last local commit hash
   - Last remote commit hash
   - Dirty files (uncommitted changes)
   - File snapshot (if not using --dry-run flag)

5. Append the start-position output to the log file

**Purpose:** Create a detailed record of the starting point for debugging and tracking progress.

---

### Step 3: WRITE TESTS

Write tests FIRST before any implementation. This is true Test-Driven Development.

**Actions:**

1. **Understand existing test structure:**
   - Review similar tests in the codebase
   - Identify patterns and conventions
   - Determine where your tests should eventually live

2. **Create tests in WIP directory:**
   - All new test files for this phase go in `tests/WIP/`
   - This isolation allows:
     - Easy GLOB pattern targeting: `pnpm test WIP`
     - Regression testing by exclusion: `pnpm test --grep -v WIP`
     - Clear separation of work-in-progress from stable tests

3. **Write comprehensive test coverage:**
   - Start with happy path (expected successful behavior)
   - Add edge cases (empty strings, null, undefined, boundaries)
   - Add error conditions (invalid input, missing files, etc.)
   - Test exit codes for bash functions

4. **Verify tests FAIL initially:**
   - Run your new tests: `pnpm test WIP`
   - Confirm they fail (you haven't implemented yet)
   - Failing tests prove they're valid and will detect when implementation is complete

**Example WIP structure:**

```text
tests/WIP/
├── phase1-text-utils.test.ts
├── phase1-list-utils.test.ts
└── phase1-filesystem.test.ts
```

**Purpose:** Tests define the contract and expected behavior before any code is written.

---

### Step 4: IMPLEMENTATION

Use the tests to guide your implementation.

**Actions:**

1. **Implement minimal code to pass each test:**
   - Work on one test at a time (or small group)
   - Write the simplest code that makes the test pass
   - Don't over-engineer or add features not covered by tests

2. **Iterate rapidly:**
   - Run tests frequently: `pnpm test WIP`
   - Use watch mode: `pnpm test:watch WIP`
   - Fix failures immediately
   - Keep the feedback loop tight

3. **Continue until all phase tests pass:**
   - All tests in `tests/WIP/` should be green
   - No shortcuts - every test must pass

4. **Refactor with confidence:**
   - Once tests pass, improve code quality
   - Tests act as a safety net
   - Re-run tests after each refactor

**Purpose:** Let tests drive the implementation, ensuring you build exactly what's needed.

---

### Step 5: CLOSE OUT

Verify completeness, check for regressions, and finalize the phase.

**Actions:**

1. **Run full test suite:**

   ```bash
   pnpm test        # All tests (excluding WIP)
   ```

2. **Handle any regressions:**

   If existing tests now fail:
   - **STOP and think deeply** - understand WHY the test is failing, not just the error message
   - Document the regression in the log file under `## Regressions Found`
   - Determine root cause:
     - Is your bash implementation incorrect?
     - Does the existing test need updating (only if requirements changed)?
     - Is there a side effect you didn't anticipate?
   - Fix the root cause, not just the symptom
   - Re-run all tests to confirm fix

3. **If no regressions, migrate tests to permanent locations:**

   - **Think carefully** about the right permanent location for each test
   - Tests usually go directly in `tests/` directory (e.g., `tests/lists.test.ts`)
   - Move tests from `tests/WIP/` to their permanent homes
   - Delete the `tests/WIP/` directory
   - **Rerun tests** to ensure nothing broke during migration

4. **Update the log file:**

   Add a `## Phase Completion` section with:
   - Date and time completed
   - Final test count (passing/total)
   - Any notable issues or decisions made
   - Location where tests were migrated to

5. **Report completion:**

   Inform the user that the phase is complete with a summary of:
   - What was implemented
   - Test coverage added
   - Any important notes or caveats

**Purpose:** Ensure quality, prevent regressions, and properly integrate work into the codebase.

---

## Testing Best Practices

### General Principles

- **Prefer real implementations over mocks**: Only mock external dependencies (APIs, file system, databases). Keep internal code integration real.

- **Use realistic test data**: Mirror actual usage patterns. If your function processes user objects, use realistic user data in tests.

- **One behavior per test**: Each `it()` block should test a single specific behavior. This makes failures easier to diagnose.

- **Tests should be deterministic**: Same input = same output, every time. Avoid depending on current time, random values, or external state unless that's what you're testing.

- **Keep tests independent**: Each test should be able to run in isolation. Use `beforeEach()` for setup, not shared variables.

- **Test the contract, not the implementation**: If you change HOW something works but it still behaves the same, tests shouldn't break.

### Error Handling

- **Prioritize fixing source code over changing tests**: When tests fail, your first instinct should be to fix the implementation to meet the test's expectation, not to change the test to match the implementation.

- **Understand failures deeply**: Don't just read the error message - understand WHY the test is failing. Use debugging, logging, or step through the code if needed.

- **Document complex test scenarios**: If a test needs explanation, add a comment describing what scenario it's covering and why it matters.

### Performance

- **Keep unit tests fast**: Unit tests should run in milliseconds. If a test is slow, it's likely testing too much or hitting external resources.

- **Separate fast and slow tests**: Integration tests can be slower. Keep them in separate files (e.g., `*.fast.test.ts` vs `*.test.ts`).

- **Use focused test runs during development**: Don't run the entire suite on every change. Use glob patterns to run just what you're working on.

### Bash Testing Specifics

- **Test exit codes**: Bash functions use exit codes (0 for success, non-zero for failure). Test these explicitly using `bashExitCode()` helper.

- **Test stdout and stderr separately**: Use the bash helper to capture output. Consider testing stderr for error messages.

- **Handle environment variables**: Set up required environment variables (like `ROOT`, `ADAPTIVE_SHELL`) in test setup.

- **Test with realistic data**: Use actual file paths, realistic strings, and representative arrays when testing bash functions.

- **Clean up temporary files**: Use `beforeEach`/`afterEach` to create and clean up any temporary files or directories needed for tests.

---

## Common Patterns and Examples

### Testing Bash Function Output

```typescript
import { describe, it, expect } from 'vitest'
import { sourcedBash } from './helpers/bash'

it("should trim whitespace from string", () => {
  const result = sourcedBash('./utils/text.sh', `trim "  hello  "`)
  expect(result).toBe('hello')
})

it("should handle empty strings", () => {
  const result = sourcedBash('./utils/empty.sh', `is_empty ""`)
  expect(result).toBe('')  // Success (exit 0)
})
```

### Testing Bash Exit Codes

```typescript
import { bashExitCode } from './helpers/bash'

it("should return 0 for successful operation", () => {
  const exitCode = bashExitCode(`
    source ./utils/lists.sh
    items=("apple" "banana")
    list_contains_ref items "apple"
  `)
  expect(exitCode).toBe(0)
})

it("should return 1 when item not found", () => {
  const exitCode = bashExitCode(`
    source ./utils/lists.sh
    items=("apple" "banana")
    list_contains_ref items "cherry"
  `)
  expect(exitCode).toBe(1)
})
```

### Testing with Temporary Files

```typescript
import { beforeEach, afterEach, it, expect } from 'vitest'
import { mkdtempSync, rmSync } from 'fs'
import { join } from 'path'
import { tmpdir } from 'os'
import { sourcedBash } from './helpers/bash'

let tempDir: string

beforeEach(() => {
  tempDir = mkdtempSync(join(tmpdir(), 'test-'))
})

afterEach(() => {
  rmSync(tempDir, { recursive: true, force: true })
})

it("should detect file exists", () => {
  const testFile = join(tempDir, 'test.txt')
  writeFileSync(testFile, 'content')

  const result = sourcedBash('./utils/filesystem.sh', `
    file_exists "${testFile}"
  `)
  expect(result).toBe('')  // Success (exit 0)
})
```

---

## Quick Reference

### Commands

```bash
# Test execution
pnpm test                    # Run all tests
pnpm test lists              # Run specific test file (e.g., lists.test.ts)
pnpm test WIP                # Run only WIP tests
pnpm test --grep -v WIP      # Run all except WIP (regression check)
pnpm test:watch              # Run in watch mode
pnpm test:watch WIP          # Watch mode for WIP tests
pnpm test:ui                 # Run with Vitest UI
pnpm test:coverage           # Run with coverage report

# Common patterns during development
pnpm test text               # Test text utilities
pnpm test lists              # Test list utilities
pnpm test --grep "trim"      # Test functions matching pattern
```

### Test Quality Checklist

Before considering tests complete, verify:

- [ ] All exported bash functions have automated tests
- [ ] Happy path is tested
- [ ] Edge cases are covered (empty strings, null, undefined, boundaries)
- [ ] Error conditions are tested (invalid input, missing files)
- [ ] Exit codes are tested where relevant
- [ ] Tests are independent (can run in any order)
- [ ] Tests are deterministic (consistent results)
- [ ] Test names clearly describe what's being tested
- [ ] No regressions in existing tests
- [ ] Tests run quickly (< 100ms per test)
- [ ] Temporary files are cleaned up

### Phase Completion Checklist

Before closing out a phase:

- [ ] SNAPSHOT captured
- [ ] Log file created with starting position
- [ ] Tests written in `tests/WIP/`
- [ ] Tests initially failed (proving validity)
- [ ] Implementation completed
- [ ] All WIP tests passing
- [ ] Full test suite run (no regressions)
- [ ] Tests migrated from WIP to permanent locations
- [ ] `tests/WIP/` directory removed
- [ ] Log file updated with completion notes
- [ ] User notified of phase completion

---

## Summary

Effective testing in this repo requires understanding **what** to test, **how** to test it, and **when** to use different testing approaches:

- **Bash functions** → Automated tests using Vitest (TypeScript)
- **Color/visual features** → Demo scripts for manual inspection
- **Simple utilities** → Focus on happy path + edge cases
- **Complex utilities** → Comprehensive coverage including error conditions

**Hybrid Approach:**

- Write automated tests in TypeScript using Vitest (`*.test.ts`)
- Create demo scripts in bash for visual verification (`*-demo.sh`)
- Use `tests/helpers/bash.ts` to execute and test bash functions from TypeScript

Follow TDD principles: write tests first, implement to pass them, then refactor with confidence. Keep tests fast, focused, and independent.

For phase-based development, use the five-step workflow: SNAPSHOT → CREATE LOG → WRITE TESTS → IMPLEMENTATION → CLOSE OUT. This ensures comprehensive test coverage, prevents regressions, and maintains clear documentation of your progress.

When tests fail, **understand why** before fixing. Prioritize fixing bash implementation over changing tests, unless the test itself was wrong.
