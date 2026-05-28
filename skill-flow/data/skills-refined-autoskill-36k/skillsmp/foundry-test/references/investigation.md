# Investigation Patterns

## Systematic Approach

1. **Reproduce reliably** - Run test in isolation first
2. **Minimize scope** - Find smallest failing input
3. **Form hypothesis** - What do you think is wrong?
4. **Test hypothesis** - Add logging/assertions to verify
5. **Fix and verify** - Make minimal change, run tests

## Using Debug Output

### pytest (Python)
```bash
pytest -vvs tests/test_file.py::test_name  # Verbose with stdout
```

Add print statements (captured by pytest):
```python
def test_something():
    result = function_under_test()
    print(f"DEBUG: result = {result}")
    assert result == expected
```

Use built-in debugging:
```bash
pytest --pdb tests/test_file.py::test_name  # Drop into debugger on failure
```

### go test
```bash
go test -v -run TestName ./...  # Verbose output
```

Add logging:
```go
func TestSomething(t *testing.T) {
    result := functionUnderTest()
    t.Logf("DEBUG: result = %v", result)  // Only shows on failure or -v
    if result != expected {
        t.Errorf("Expected %v, got %v", expected, result)
    }
}
```

Use Delve debugger:
```bash
dlv test -- -test.run TestName
```

### Jest (JavaScript)
```bash
jest path/to/test.js --verbose  # Verbose output
```

Add console logging:
```javascript
test('something', () => {
    const result = functionUnderTest();
    console.log('DEBUG: result =', result);
    expect(result).toBe(expected);
});
```

Use Node debugger:
```bash
node --inspect-brk node_modules/.bin/jest --runInBand path/to/test.js
```

## Running Specific Tests

### pytest
```bash
pytest tests/test_file.py::test_name           # Single test
pytest tests/test_file.py::TestClass           # All tests in class
pytest tests/test_file.py::TestClass::test_method  # Specific method
pytest -k "test_name"                          # Pattern matching
```

### go test
```bash
go test -run TestName ./...                    # Tests matching pattern
go test -run "TestName/subtest" ./...          # Specific subtest
go test -run "TestName$" ./pkg                 # Exact match in package
```

### Jest
```bash
jest path/to/test.js                           # Specific file
jest -t "test name"                            # Tests matching pattern
jest --testPathPattern="pattern"               # Files matching pattern
```

## Reading Stack Traces

**From bottom to top:**
1. Bottom: The actual error message
2. Above: The line where it occurred
3. Higher: The call chain that led there

**Key information to extract:**
- Which file and line number
- What function was being called
- What arguments were passed (if visible)

### Language-Specific Stack Trace Notes

**Python:**
- Most recent call is at the bottom
- Look for your code (not library internals)
- `raise from` shows exception chaining

**Go:**
- Goroutine stack traces start with `goroutine N:`
- `runtime/debug.Stack()` can print current stack
- Panic traces show from panic point up

**JavaScript:**
- Most recent call is at the top
- Async stack traces may be truncated
- Source maps affect line numbers in TypeScript

## Isolating the Problem

### Step 1: Run test alone
```bash
# pytest
pytest tests/test_file.py::test_name

# go
go test -run TestName -count=1 ./pkg

# jest
jest path/to/test.js -t "test name"
```

### Step 2: Check if order-dependent
```bash
# pytest
pytest --randomly-seed=12345

# go
go test -shuffle=on ./...

# jest
jest --randomize
```

### Step 3: Eliminate external dependencies
- Mock network calls
- Use test databases
- Freeze time-dependent code

### Step 4: Minimize reproducer
- Comment out unrelated test code
- Simplify input data
- Remove assertions until you find the failing one
