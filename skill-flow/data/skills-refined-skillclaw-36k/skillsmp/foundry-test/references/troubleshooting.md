# Advanced Troubleshooting

## Test Collection/Discovery Errors

When the test runner can't find or collect tests:

### pytest (Python)
```bash
pytest --collect-only tests/  # See what pytest finds
```
**Common causes:**
- Syntax errors in test files
- Import errors in test files
- Invalid test naming (`test_` prefix required)
- Missing `__init__.py` in test directories

### go test
```bash
go test -list '.*' ./...  # List all tests
go test -v ./... 2>&1 | head -50  # See discovery output
```
**Common causes:**
- Test files not ending in `_test.go`
- Test functions not starting with `Test`
- Build errors preventing compilation
- Wrong package path

### Jest
```bash
jest --listTests  # List all test files
jest --showConfig  # Show configuration
```
**Common causes:**
- Test files not matching pattern (default: `*.test.js`, `*.spec.js`)
- Configuration issues in `jest.config.js`
- TypeScript compilation errors
- Module resolution issues

### npm test
```bash
npm test -- --help  # See underlying test runner options
cat package.json | jq '.scripts.test'  # Check test script
```
**Common causes:**
- No `test` script in package.json
- Underlying runner not installed
- Script syntax error

## Coverage Analysis

Find untested code:

### pytest
```bash
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html  # Generate HTML report
```

### go test
```bash
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out  # Generate HTML report
```

### Jest
```bash
jest --coverage
jest --coverage --coverageReporters="text" --coverageReporters="html"
```

## Parallel Test Execution

Run tests in parallel for speed:

### pytest
```bash
pytest -n auto  # Uses pytest-xdist, auto-detect CPU count
pytest -n 4     # Use 4 workers
```

### go test
```bash
go test -parallel 4 ./...  # 4 parallel tests per package
go test -p 4 ./...         # 4 packages in parallel
```

### Jest
```bash
jest --maxWorkers=4
jest --runInBand  # Disable parallelism (for debugging)
```

**Note:** Parallel execution requires tests to be independent. If tests fail only in parallel, they likely have shared state issues.

## Test Isolation Verification

Ensure tests don't affect each other:

### pytest
```bash
pytest --forked  # Run each test in subprocess
pytest -x --randomly-seed=12345  # Run with fixed random order
```

### go test
```bash
go test -count=1 ./...  # Disable test caching
go test -shuffle=on ./...  # Randomize test order (Go 1.17+)
```

### Jest
```bash
jest --runInBand --detectOpenHandles
jest --randomize  # Randomize test order
```

## Debugging Specific Tests

### pytest
```bash
pytest -vvs tests/test_file.py::test_name  # Verbose with stdout
pytest --pdb tests/test_file.py::test_name  # Drop into debugger on failure
pytest -k "test_name"  # Run tests matching pattern
```

### go test
```bash
go test -v -run TestName ./...  # Run specific test
go test -v -run "TestName/subtest" ./...  # Run specific subtest
dlv test -- -test.run TestName  # Debug with Delve
```

### Jest
```bash
jest path/to/test.js -t "test name"  # Run specific test
node --inspect-brk node_modules/.bin/jest --runInBand  # Debug
jest --watch  # Watch mode for development
```

## Environment Issues

### Python
```bash
python -c "import sys; print(sys.path)"  # Check Python path
pip list  # Check installed packages
pip check  # Verify dependency compatibility
```

### Go
```bash
go env  # Check Go environment
go mod verify  # Verify dependencies
go mod why <package>  # Why is package required?
```

### JavaScript
```bash
node -e "console.log(require.resolve('package'))"  # Find package location
npm ls  # List dependency tree
npm ls --depth=0  # Top-level dependencies only
```

---

## Success Criteria

A test session is successful when:
- All tests pass
- No regressions introduced
- Root cause understood
- Fix documented (if complex)

**Post-fix checklist:**
1. Run the specific failing test
2. Run related tests in the same module/package
3. Run full test suite
4. Verify no new failures introduced
