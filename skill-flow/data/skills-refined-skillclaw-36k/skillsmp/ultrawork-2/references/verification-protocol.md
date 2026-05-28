# Verification Protocol

## Core Principle

**No completion claim without evidence.**

## Evidence Collection

### When to Collect

| Event | Action |
|-------|--------|
| Worker completes task | Extract evidence from output |
| Test command runs | Capture exit code + output |
| Build succeeds | Capture build output |
| API verified | Capture response |

### How to Collect

Workers must report evidence in their output:

```
TASK COMPLETE

Evidence:
- Criteria: "Tests pass"
  Command: npm test
  Output: "47 tests passed, 0 failed"
  Exit code: 0

- Criteria: "No lint errors"
  Command: npm run lint
  Output: "No issues found"
  Exit code: 0
```

### Evidence Storage

1. Parse worker output for evidence blocks
2. Add to task's evidence array in session.json
3. Add to global evidence_log
4. Update Task via TaskUpdate(addComment)

## Verification Checklist

Before marking any task complete:

```
[ ] All success criteria have evidence
[ ] Evidence is concrete (not "it works")
[ ] Commands show exit code 0 where relevant
[ ] No blocked phrases in output
[ ] TDD tasks have complete RED→GREEN evidence chain
```

---

## TDD Verification

### TDD Evidence Requirements

For tasks with `approach: "tdd"`, verify the evidence chain:

```
Required Evidence Sequence:
1. TDD-RED: Test file created
2. TDD-RED: Test execution failed (exit code 1)
3. TDD-GREEN: Implementation created
4. TDD-GREEN: Test execution passed (exit code 0)
5. (Optional) TDD-REFACTOR: Improvements made, tests still pass
```

### TDD Verification Checklist

```
[ ] TDD-RED evidence present (test written first)
[ ] Test failure recorded (exit code 1)
[ ] TDD-GREEN evidence present (implementation done)
[ ] Test pass recorded (exit code 0)
[ ] Evidence timestamps show RED before GREEN
```

### TDD Verification Fails If

| Condition | Problem |
|-----------|---------|
| Missing TDD-RED evidence | Test not written before implementation |
| Missing TDD-GREEN evidence | Implementation not verified |
| GREEN evidence before RED | Wrong order - code before test |
| No test failure recorded | Test may have been written after code |
| Implementation timestamp < Test timestamp | Code written before test |

### TDD Good Evidence

```
Evidence:
- TDD-RED: Created tests/validateUser.test.ts
  Command: npm test tests/validateUser.test.ts
  Output: "FAIL - validateUser is not defined"
  Exit code: 1

- TDD-GREEN: Implemented src/validateUser.ts
  Command: npm test tests/validateUser.test.ts
  Output: "PASS - 3/3 tests passed"
  Exit code: 0

- TDD-REFACTOR: Extracted helper function
  Command: npm test tests/validateUser.test.ts
  Output: "PASS - 3/3 tests passed"
  Exit code: 0
```

### TDD Bad Evidence

```
# Missing RED phase
"Wrote validateUser function and tests"
"Tests pass now"

# Wrong order indication
"Fixed the tests to match implementation"
"Updated test expectations"
```

## Blocked Phrases

If ANY of these appear without counter-evidence, block completion:

| Phrase | Problem |
|--------|---------|
| "should work" | Speculation |
| "probably" | Uncertainty |
| "might need" | Incomplete |
| "TODO" | Unfinished |
| "basic version" | Partial |
| "simplified" | Partial |
| "you can add" | Incomplete |
| "for now" | Temporary |

## Counter-Evidence

Blocked phrase can be overridden with explicit evidence:

```
Note: Using "basic version" of auth for MVP scope.
Counter-evidence: User confirmed MVP scope acceptable.
```

## Verification Task

The verification task (created by planner) runs last:

```markdown
## Verification Task Checklist

1. All implementation tasks resolved?
   → TaskList shows all child tasks resolved

2. All success criteria have evidence?
   → Check evidence_log covers all criteria

3. Tests pass?
   → Run test suite, capture output

4. Build succeeds?
   → Run build, capture output

5. No blocked phrases?
   → Scan all task outputs

6. TDD tasks have valid evidence chain?
   → For each task with `approach: "tdd"`:
     - Has TDD-RED evidence
     - Has TDD-GREEN evidence
     - RED timestamp < GREEN timestamp

Only mark COMPLETE if ALL pass.
```

## Failure Handling

If verification fails:

1. Identify failing criterion
2. Log failure reason
3. Keep phase as VERIFICATION (not COMPLETE)
4. Report specific failure to user
5. User decides: fix and retry, or cancel

## Evidence Quality

### Good Evidence
```
Command: npm test
Output: "
  PASS src/auth.test.ts
  PASS src/user.test.ts

  Test Suites: 2 passed, 2 total
  Tests: 15 passed, 15 total
"
Exit: 0
```

### Bad Evidence
```
"Tests work fine"
"I ran the tests and they passed"
"Should be good now"
```
