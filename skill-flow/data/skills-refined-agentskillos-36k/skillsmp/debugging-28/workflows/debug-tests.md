# Test Debugging Workflow

## When to Use

- Tests failing unexpectedly
- Flaky tests (pass sometimes, fail others)
- Tests passing but code is broken
- Coverage gaps
- Test environment issues
- Slow test suites

## Step 1: Understand the Failure

```
□ Read the full error message
□ Which test(s) are failing?
□ Is it consistent or flaky?
□ Did it ever pass? When did it start failing?
□ What changed? (git log, deps update)
```

### Run just the failing test:
```bash
# pytest
pytest path/to/test_file.py::TestClass::test_method -v

# jest
npm test -- --testNamePattern="test name"

# go
go test -run TestName -v
```

## Step 2: Analyze the Error Type

### Assertion Failure
```
Expected: X
Actual: Y

→ Either the code is wrong or the expectation is wrong
→ Check: Is the test correct? Is the code correct?
```

### Setup/Teardown Error
```
Error in fixture/beforeEach/afterEach

→ Test infrastructure problem
→ Check: Database connections, file handles, mocks
```

### Timeout
```
Test exceeded timeout

→ Infinite loop, deadlock, or slow operation
→ Check: Async handling, network calls, database
```

### Import/Module Error
```
Cannot find module/ModuleNotFoundError

→ Missing dependency or wrong path
→ Check: package.json/requirements.txt, import paths
```

## Step 3: Debug the Test

### Add visibility:
```python
# Python - pytest
def test_something():
    result = function_under_test()
    print(f"DEBUG: result = {result}")  # Use -s flag
    assert result == expected

# Run with: pytest -s test_file.py
```

```javascript
// JavaScript - jest
test('something', () => {
  const result = functionUnderTest();
  console.log('DEBUG: result =', result);
  expect(result).toBe(expected);
});
```

### Use debugger:
```python
# Python
def test_something():
    import pdb; pdb.set_trace()
    result = function_under_test()
    assert result == expected

# Run with: pytest -s --pdb test_file.py
```

## Step 4: Flaky Test Diagnosis

Flaky tests are tests that sometimes pass, sometimes fail without code changes.

### Common causes:
1. **Race conditions** - Async operations, timing
2. **Shared state** - Tests not isolated
3. **External dependencies** - Network, databases, time
4. **Order dependency** - Tests depend on run order
5. **Resource leaks** - File handles, connections

### Diagnostic steps:
```bash
# Run test in isolation
pytest test_file.py::test_name

# Run test repeatedly
pytest test_file.py::test_name --count=10  # pytest-repeat plugin

# Run in different order
pytest test_file.py --random-order  # pytest-random-order plugin

# Run with verbose timing
pytest test_file.py -v --durations=0
```

### Fixing flaky tests:
```python
# Bad: relies on timing
time.sleep(1)  # Hope it's done
assert result == expected

# Good: wait for condition
from tenacity import retry, stop_after_delay
@retry(stop=stop_after_delay(5))
def wait_for_result():
    return get_result() == expected

assert wait_for_result()
```

## Step 5: Test Isolation Issues

Tests should not affect each other.

### Check for shared state:
```python
# Bad: module-level state
cache = {}  # Persists across tests

# Good: reset in fixtures
@pytest.fixture(autouse=True)
def reset_cache():
    cache.clear()
    yield
    cache.clear()
```

### Database isolation:
```python
# Use transactions that rollback
@pytest.fixture
def db_session():
    session = create_session()
    session.begin_nested()  # Savepoint
    yield session
    session.rollback()
    session.close()
```

## Step 6: Mock/Stub Issues

### Symptoms:
- Test passes but production breaks
- Test tests the mock, not the code
- Mock setup is fragile

### Anti-patterns to check:
```python
# Bad: testing mock behavior
mock.return_value = 42
result = mock()
assert result == 42  # Useless!

# Bad: over-mocking
def test_user_creation(mock_db, mock_email, mock_logger, mock_cache):
    # So many mocks, is anything real?

# Better: test with real collaborators when possible
def test_user_creation(test_db):  # Real test database
    user = create_user(db=test_db)
    assert test_db.get(user.id) == user
```

### Mock debugging:
```python
# See what was called
print(mock.call_args_list)
print(mock.method_calls)

# Assert specific calls
mock.assert_called_once_with(expected_arg)
```

## Step 7: Test Environment Issues

### Check environment parity:
```
□ Same Python/Node version as CI?
□ Same database version?
□ Same OS? (path separators, line endings)
□ Environment variables set?
□ Test data/fixtures present?
```

### Reproduce CI locally:
```bash
# Use same commands as CI
npm ci  # Not npm install
pip install -r requirements.txt  # Exact versions

# Use Docker to match CI environment
docker run -it ci-image:latest /bin/bash
```

## Step 8: Coverage Gap Analysis

Tests passing doesn't mean code works.

```bash
# Generate coverage report
pytest --cov=mypackage --cov-report=html

# Find uncovered code
# Look for red lines in htmlcov/index.html
```

### Focus areas:
- Error handling paths
- Edge cases (empty, null, max values)
- Conditional branches
- Exception handlers

## Step 9: Fix and Prevent

```
1. Fix the root cause (not just the symptom)
2. If flaky, add logging to catch next occurrence
3. Add comments explaining non-obvious test logic
4. Consider if test is testing right thing
5. Check for similar issues in other tests
```

## Quick Reference: Test Debugging Commands

| Framework | Run one test | Verbose | With debugger |
|-----------|--------------|---------|---------------|
| pytest | `-k "name"` | `-v` | `--pdb -s` |
| jest | `--testNamePattern` | `--verbose` | `--inspect-brk` |
| go test | `-run Name` | `-v` | `dlv test` |
| rspec | `--example name` | `--format d` | `binding.pry` |

## Common Fixes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Works locally, fails CI | Environment diff | Docker, lock deps |
| Random failures | Shared state | Isolation fixtures |
| Timeout | Async issue | Proper awaits, mocks |
| Wrong assertion | Test bug | Review expected value |
| Import error | Missing dep | Check requirements |
