# Failure Categories

## Assertion Failures

Expected vs actual mismatch. Investigate:

- **Test expectations correct?** - Has the expected behavior changed?
- **Implementation changed?** - Did recent changes alter output?
- **Data setup correct?** - Is test data/fixtures properly configured?

**Common causes:**
- API response format changed
- Floating point precision issues
- String encoding differences
- Order-dependent comparisons (sets, dicts, maps)

## Exception/Error Failures

Runtime errors during test execution (language-specific):

### Python
| Error Type | Common Cause | Fix |
|------------|--------------|-----|
| `AttributeError` | Object missing attribute | Check object initialization |
| `KeyError` | Dictionary key missing | Validate data structure |
| `TypeError` | Wrong argument types | Check function signatures |
| `ValueError` | Invalid value passed | Validate input data |
| `IndexError` | List index out of range | Check collection sizes |

### Go
| Error Type | Common Cause | Fix |
|------------|--------------|-----|
| `nil pointer dereference` | Uninitialized pointer | Check nil before access |
| `index out of range` | Slice/array bounds | Validate length first |
| `interface conversion` | Type assertion failed | Use comma-ok idiom |
| `panic` | Unrecovered error | Add recover or handle error |

### JavaScript/TypeScript
| Error Type | Common Cause | Fix |
|------------|--------------|-----|
| `TypeError` | Undefined/null access | Add null checks |
| `ReferenceError` | Undefined variable | Check variable scope |
| `RangeError` | Invalid array length | Validate input ranges |
| `SyntaxError` | Parse error | Check JSON/template syntax |

## Import/Module Failures

Module loading issues vary by language:

### Python
**Check in order:**
1. PYTHONPATH correct? (`export PYTHONPATH=src:$PYTHONPATH`)
2. `__init__.py` files exist in all package directories?
3. Circular imports? (A imports B, B imports A)
4. Missing dependencies? (`pip install -r requirements.txt`)

**Diagnosing circular imports:**
```python
import sys
print([m for m in sys.modules if 'your_module' in m])
```

### Go
**Check in order:**
1. Module initialized? (`go mod init` / `go mod tidy`)
2. Package path correct? (matches directory structure)
3. Exported names? (capitalized = public)
4. Build constraints? (`//go:build` tags)

**Common fixes:**
```bash
go mod tidy           # Fix dependencies
go clean -modcache    # Clear module cache
```

### JavaScript/TypeScript
**Check in order:**
1. `node_modules` exists? (`npm install`)
2. Package in dependencies? (check package.json)
3. Import path correct? (relative vs package)
4. ESM vs CommonJS? (`import` vs `require`)

**Common fixes:**
```bash
rm -rf node_modules && npm install  # Fresh install
npm cache clean --force             # Clear cache
```

## Setup/Fixture Failures

Test setup and teardown issues:

### Python (pytest fixtures)
| Issue | Check |
|-------|-------|
| Fixture not found | Is it in conftest.py or same file? |
| Fixture name wrong | Does the parameter name match exactly? |
| Fixture scope issue | Is scope (function/class/module/session) appropriate? |
| Fixture dependency | Does fixture depend on another fixture that fails? |

**Fixture scopes:**
- `function` - New instance per test (default)
- `class` - Shared across class
- `module` - Shared across module
- `session` - Shared across entire test session

### Go (TestMain, setup/teardown)
| Issue | Check |
|-------|-------|
| TestMain not running | Ensure `m.Run()` is called |
| Setup failed | Check `TestMain` or `t.Cleanup()` |
| Parallel test conflict | Use `t.Parallel()` carefully |
| Resource cleanup | Ensure `defer` or `t.Cleanup()` |

### JavaScript (beforeEach, afterEach)
| Issue | Check |
|-------|-------|
| Hook not running | Check hook placement (describe scope) |
| Async hook timeout | Return promise or use done() |
| Shared state | Reset state in beforeEach |
| Mock not reset | Call `jest.resetAllMocks()` |

## Timeout Failures

Tests hanging or taking too long:

**Investigation steps (all runners):**
1. Run test in isolation to confirm it's slow
2. Add debug logging to identify bottleneck
3. Check for infinite loops or blocking I/O
4. Look for missing mocks of external services

### Setting Timeouts by Runner

**pytest:**
```python
@pytest.mark.timeout(30)  # 30 second limit
def test_slow_operation():
    pass
```

**Go:**
```bash
go test -timeout 30s ./...
```

**Jest:**
```javascript
jest.setTimeout(30000); // 30 seconds
// or per-test:
test('slow test', async () => { ... }, 30000);
```

## Flaky Tests

Non-deterministic failures:

**Common causes (all languages):**
- Race conditions in async/concurrent code
- Time-dependent logic (dates, timestamps)
- Random data generation without seeding
- Shared state between tests
- External service dependencies

### Detection Strategies

**pytest:**
```bash
pytest --count=10 test_file.py::test_name
pytest-randomly  # Detect order dependencies
```

**Go:**
```bash
go test -count=10 ./...
go test -race ./...  # Detect race conditions
```

**Jest:**
```bash
jest --runInBand  # Run serially to detect shared state
jest --detectOpenHandles  # Find leaked async operations
```

### Fixing Flaky Tests
- Seed random generators (all languages have equivalents)
- Mock time-dependent functions
- Isolate test state (fresh fixtures per test)
- Mock external services
- Use deterministic ordering for collections
