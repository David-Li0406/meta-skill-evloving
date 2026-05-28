# TDD Failure Recovery Procedures
**Version:** {{VERSION}}

Step-by-step procedures for recovering from common TDD failures.

---

## Test Pollution Recovery

**Symptom:** Tests pass in isolation but fail when run together

### Procedure

1. **Identify the polluting test**
   - Run failing test alone → passes
   - Run full suite → fails
   - Binary search: run half the tests with failing test

2. **Find shared state**
   - Global variables modified
   - Class-level attributes changed
   - Database records not cleaned up
   - File system artifacts left behind

3. **Fix isolation**
   ```
   Option A: Add cleanup in polluting test
   Option B: Add setup in affected test
   Option C: Use fresh fixtures for each test
   ```

4. **Verify fix**
   - Run full suite multiple times
   - Run in different orders if framework supports
   - Confirm consistent results

---

## Fixture Failure Recovery

**Symptom:** Test setup or teardown fails

### Procedure

1. **Read fixture error message**
   - Which fixture failed?
   - Setup or teardown?
   - What resource is missing?

2. **Check fixture dependencies**
   - Database connection available?
   - Required files exist?
   - External services running?

3. **Fix fixture**
   ```
   Database: Ensure test DB exists and is accessible
   Files: Create required test files/directories
   Services: Mock external dependencies
   ```

4. **Add fixture resilience**
   - Use try/finally for cleanup
   - Check preconditions in setup
   - Provide clear error messages

5. **Verify fix**
   - Run affected tests
   - Run full suite
   - Confirm setup/teardown works consistently

---

## Assertion Failure Recovery

**Symptom:** Test assertion fails with unexpected value

### Procedure

1. **Read assertion message carefully**
   ```
   Expected: [what test expects]
   Actual:   [what code returned]
   ```

2. **Determine root cause**

   | Situation | Likely Cause |
   |-----------|--------------|
   | Expected correct, actual wrong | Implementation bug |
   | Expected wrong, actual correct | Test needs updating |
   | Both seem wrong | Requirements misunderstood |

3. **Fix based on cause**
   ```
   Implementation bug → Fix the code
   Test outdated → Update test expectations
   Requirements unclear → Clarify and adjust both
   ```

4. **Verify fix**
   - Run the specific test
   - Run related tests
   - Run full suite for regressions

---

## Timeout Failure Recovery

**Symptom:** Test fails due to timeout/slow execution

### Procedure

1. **Identify timeout type**
   - Framework, network, database, or async timeout

2. **Diagnose cause**
   - Infinite loop → Check loop conditions
   - Slow query → Check database indexes
   - Network → Check connectivity or mock
   - Deadlock → Check resource locking

3. **Fix timeout**
   - Fix slow code (optimize, add indexes)
   - Mock slow dependencies (APIs, database)
   - Increase timeout only as last resort

4. **Verify** - Run test, ensure reasonable time

---

## Flaky Test Recovery

**Symptom:** Test passes sometimes, fails randomly

### Procedure

1. **Confirm flakiness** - Run test 10+ times

2. **Identify source**
   - Fails after specific test → Test pollution
   - Random timing → Race condition
   - Works locally, fails CI → Environment difference

3. **Fix flakiness**
   - Pollution → Add proper isolation
   - Race condition → Add synchronization/waits
   - Environment → Mock external factors

---

## Quick Recovery Checklist

- [ ] Read full error message
- [ ] Check if test passes in isolation
- [ ] Review recent changes
- [ ] Apply recovery procedure above
- [ ] Run full suite before proceeding
