---
name: test-runner
description: Run the relevant tests for the current change and summarize results. Use in Flow 3 (Build) and optionally in Flow 4 (Gate).
allowed-tools: Bash, Read, Write
---

# Test Runner Skill

You are a helper for running tests in this repository.

The test-runner is a mechanical skill that executes tests and captures output. It does not make judgment calls about test quality or coverage. Those decisions belong to agents (test-critic, test-author).

---

## Purpose

Execute the repository's test suite with appropriate scoping and capture structured output for downstream agents. The skill:

- Runs tests (scoped or full)
- Captures raw output and exit codes
- Produces structured summaries with counts
- Handles framework-specific invocation patterns

**What this skill does NOT do:**

- Write or modify tests (that's test-author)
- Judge test quality (that's test-critic)
- Make decisions about what to test (that's orchestrator / test-strategist)
- Classify failures (that's flakiness-detector)

---

## When to Use

| Context                        | Selection Strategy       | Example                            |
| ------------------------------ | ------------------------ | ---------------------------------- |
| **AC loop (Flow 3)**           | AC-scoped, fail-fast     | Run only tests for AC-001          |
| **Post-AC verification**       | Changed-file scope       | Tests for files touched in this AC |
| **Global hardening (Flow 3)**  | Full suite               | All tests after all ACs complete   |
| **Gate verification (Flow 5)** | Full suite, no fail-fast | Comprehensive verification         |
| **Quick sanity check**         | Smoke tests only         | Fast feedback during iteration     |

---

## Test Selection Strategies

### 1. Run All Tests (Full Suite)

Use when: Global hardening, Gate verification, or no scope information available.

```bash
# Rust
cargo test --workspace --tests --color=always

# Python (pytest)
pytest --color=yes -v

# JavaScript (jest)
npm test -- --colors

# Go
go test ./...
```

### 2. Run Changed Tests (Scoped by Diff)

Use when: Focused verification of what changed since main.

```bash
# Get changed files
git diff --name-only origin/main...HEAD

# Filter to test files and run those specifically
# (Framework-specific filtering)
```

### 3. Run Related Tests (Dependency Aware)

Use when: Implementation changed, need to run tests that exercise that code.

For Rust:

```bash
cargo test -p <crate> -- <test-name-pattern>
cargo test --test <integration-test-name>
```

For pytest:

```bash
pytest tests/unit/test_<module>.py -v
pytest -k "auth or login"
```

### 4. Run AC-Scoped Tests

Use when: Verifying a specific Acceptance Criterion in the AC loop.

Test naming conventions for AC filtering:

- `test_ac_001_*` (name prefix)
- `@AC-001` marker/tag
- File-based: `tests/ac_001_*.py`

```bash
# pytest with marker
pytest -m "AC_001" --color=yes

# cargo test with pattern
cargo test ac_001

# jest with pattern
npm test -- --testNamePattern="AC-001"
```

### 5. Run Smoke Tests Only

Use when: Quick sanity check, not full verification.

```bash
# If smoke marker exists
pytest -m smoke --color=yes

# Or first N tests
pytest --maxfail=5 -x
```

---

## Commands by Framework

### Rust (cargo test)

```bash
# Full suite
cargo test --workspace --tests --color=always

# Specific crate
cargo test -p <crate-name>

# Pattern match
cargo test <pattern>

# Single test
cargo test <full::path::to::test>

# Integration test file
cargo test --test <name>

# With fail-fast (implicit with --test-threads=1)
cargo test -- --test-threads=1
```

### Python (pytest)

```bash
# Full suite
pytest --color=yes -v

# Specific file
pytest tests/unit/test_auth.py -v

# Pattern match
pytest -k "login or session" -v

# Marker-based
pytest -m "unit" -v
pytest -m "AC_001" -v

# Fail-fast
pytest -x --color=yes

# With coverage
pytest --cov=src --cov-report=term-missing
```

### JavaScript/TypeScript (jest)

```bash
# Full suite
npm test -- --colors

# Specific file
npm test -- --colors tests/auth.test.ts

# Pattern match
npm test -- --testNamePattern="login"

# Fail-fast
npm test -- --bail --colors

# With coverage
npm test -- --coverage
```

### Go (go test)

```bash
# Full suite
go test ./...

# Specific package
go test ./pkg/auth/...

# Pattern match
go test -run "TestLogin" ./...

# Fail-fast
go test -failfast ./...

# Verbose
go test -v ./...
```

---

## Output Format

### Raw Output

Save raw test output to `test_output.log` (overwrite per run).

### Structured Summary

Save parsed summary to `test_summary.md` with this structure:

```markdown
# Test Summary

## Overall Status

- **Result:** PASS | FAIL
- **Exit Code:** <int>
- **Duration:** <time>

## Counts

- Passed: <int>
- Failed: <int>
- Skipped: <int>
- xfailed: <int>
- xpassed: <int>

## Failing Tests (if any)

- `path::to::test_name` - <short error>
- `path::to::other_test` - <short error>

## Top Error Snippets
```

<first 5-10 lines of first failure>

```

```

### Canonical Summary Line

For machine parsing, include a canonical line:

```
passed=15 failed=2 skipped=1 xfailed=0 xpassed=0
```

Use `null` for any count that cannot be reliably extracted.

---

## Handling Test Failures

### Exit Codes

| Code | Meaning                   |
| ---- | ------------------------- |
| 0    | All tests passed          |
| 1+   | One or more tests failed  |
| null | Command could not execute |

### Failure Output

When tests fail:

1. Capture the full output to `test_output.log`
2. Extract failing test names to `test_summary.md`
3. Include up to 20 lines of the most relevant error output
4. Report exit code accurately

### Do Not Modify on Failure

The test-runner skill does not fix failing tests. It reports results. Routing decisions belong to the orchestrator. Fixes belong to code-implementer or test-author.

---

## Flaky Test Awareness

The test-runner itself does not classify flakiness. However, it should:

1. **Record raw results faithfully** - Each run produces accurate counts
2. **Include test identifiers** - So flakiness-detector can compare across runs
3. **Note any timeout or intermittent signals** - In the summary notes

For actual flakiness classification, the orchestrator routes to `flakiness-detector`, which:

- Re-runs failures with a budget
- Classifies: DETERMINISTIC_REGRESSION vs FLAKY vs ENV_TOOLING
- Produces a worklist for routing

---

## Integration with Agents

### Called by: test-executor

The `test-executor` agent invokes this skill and writes the formal artifact:

- `.runs/<run-id>/build/test_execution.md`

The test-executor handles:

- Mode selection (verify vs verify_ac)
- Fail-fast decisions based on flow context
- Formal handoff to orchestrator

### Called by: test-author

The `test-author` agent may invoke this skill to verify tests work:

- Quick run of newly written tests
- Scope to just the tests being authored
- Not a formal execution report

### Informs: flakiness-detector

The `flakiness-detector` reads test-runner output to understand what failed, then re-runs to classify. It does not call test-runner directly; it runs tests itself with a rerun budget.

---

## Configuration

### Repository Config

If `demo-swarm.config.json` exists, read test commands from:

```json
{
  "commands": {
    "test": "cargo test --workspace --tests --color=always",
    "test_scoped": "cargo test -p {crate}",
    "test_ac": "cargo test {ac_pattern}"
  },
  "flakiness": {
    "budget_seconds": 180,
    "rerun_count": 3,
    "command": null
  }
}
```

### Fallback Detection

If no config exists, detect the stack:

- `Cargo.toml` present → Rust/cargo test
- `package.json` with test script → npm test
- `pytest.ini` or `pyproject.toml` → pytest
- `go.mod` present → go test

Do not invent commands. If detection fails, record `missing_required` and bounce to `pack-customizer`.

---

## Examples

### Example 1: AC-Scoped Run (Flow 3 Microloop)

```bash
# Run tests for AC-001 only, fail-fast
cargo test ac_001 -- --test-threads=1
```

Output in `test_summary.md`:

```markdown
# Test Summary

## Overall Status

- **Result:** FAIL
- **Exit Code:** 1
- **Duration:** 4.2s

## Counts

- Passed: 3
- Failed: 1
- Skipped: 0

## Failing Tests

- `auth::tests::test_ac_001_invalid_password` - assertion failed: expected 401, got 200
```

### Example 2: Full Suite (Global Hardening)

```bash
cargo test --workspace --tests --color=always
```

Output:

```markdown
# Test Summary

## Overall Status

- **Result:** PASS
- **Exit Code:** 0
- **Duration:** 45.3s

## Counts

- Passed: 127
- Failed: 0
- Skipped: 3
- xfailed: 2
- xpassed: 0

## Notes

- 3 tests skipped: require external service
- 2 xfail tests: known issues tracked in #123, #124
```

### Example 3: Changed Files Scope

```bash
# Identify changed files
git diff --name-only origin/main...HEAD | grep '\.rs$'

# Run tests for changed crates
cargo test -p auth_service -p session_manager
```

---

## Troubleshooting

### Test Command Not Found

**Symptom:** `cargo: command not found` or similar.

**Solution:** This is an environment issue. Record as ENV_TOOLING and bounce to fix environment. Do not continue with broken tooling.

### Cannot Determine Counts

**Symptom:** Test output does not match expected format.

**Solution:** Record counts as `null` rather than guessing. Note the parsing issue in summary. The skill contract is to report accurately, not to fabricate.

### Tests Hang or Timeout

**Symptom:** Tests do not complete within reasonable time.

**Solution:** Note the timeout in summary. If the run was partial, include whatever counts were observed. Record as potentially flaky for flakiness-detector to investigate.

### No Test Files Found

**Symptom:** Test command runs but finds nothing to test.

**Solution:** This is valid output. Report `passed=0 failed=0 skipped=0`. The orchestrator decides if this is expected (new feature without tests yet) or a problem (tests deleted).

---

## Behavior (Inherited from Original)

1. Prefer scoped test runs:
   - Use `git diff --name-only origin/main...HEAD` to list changed files when available.
   - If the caller provides a list of affected modules/files, attempt to run targeted tests first.

2. Runtime flags and run bounds:
   - Prefer to keep runs bounded; if the full suite is required, note this in the summary.

3. Capture output and artifacts:
   - Save raw output to `test_output.log` (overwrite per run) and a parsed summary to `test_summary.md`.
   - `test_summary.md` should include: overall status (PASS/FAIL), failing test names, top error snippets, and counts.

4. Failure handling:
   - Exit status is used by calling subagent; include failing test names in `test_summary.md`.

5. Do not modify source or tests.

6. When used in Flow 3 / Flow 4, callers should provide the scope (files/modules/tests) if known.
