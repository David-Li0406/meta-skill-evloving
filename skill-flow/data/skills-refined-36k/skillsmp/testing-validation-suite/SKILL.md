---
name: testing-validation-suite
description: Execute Budget Buddy test suites including unit tests, API tests, and bank integration tests with coverage reporting. Use when running tests, validating code, checking coverage, or ensuring code quality.
allowed-tools: [Bash(pytest*), Bash(python*), Bash(npm*), Read, Grep]
---

# Testing & Validation Suite

Execute Budget Buddy's test suites systematically with coverage analysis.

## Quick Test Checklist

```
Testing Workflow:
- [ ] Run unit tests (isolated functions)
- [ ] Run API tests (backend running required)
- [ ] Run integration tests (Plaid sandbox)
- [ ] Check coverage report (aim for 80%+)
- [ ] Fix any failing tests
- [ ] Verify no regressions
```

## Quick Start

### Run All Backend Tests

```bash
pytest backend/tests/
```

### Run with Coverage

```bash
pytest backend/tests/ --cov=backend --cov-report=html
open htmlcov/index.html
```

### Run Specific Test File

```bash
pytest backend/tests/test_apply_planning.py -v
```

### Frontend Tests

```bash
cd frontend
npm test -- --watchAll=false --coverage
```

## Test Categories

### 1. Unit Tests

Test individual functions in isolation.

```bash
# Run only unit tests (exclude API tests)
pytest backend/tests/ --ignore=backend/tests/test_api_*.py -v
```

### 2. API Tests

Test API endpoints (requires backend running).

```bash
# Start backend first
python -m uvicorn backend.api.main:app --reload --port 8000 &

# Run API tests
pytest backend/tests/test_api_*.py -v

# Stop backend
pkill -f "uvicorn.*8000"
```

### 3. Integration Tests

Test bank integrations and external services.

```bash
pytest backend/tests/test_plaid_integration.py -v
```

## Essential Test Commands

### Run with Verbose Output

```bash
pytest backend/tests/ -v
```

### Run Single Test

```bash
pytest backend/tests/test_file.py::test_function_name -vv
```

### Debug with Print Statements

```bash
pytest backend/tests/test_file.py -s
```

### Debug with pdb

```bash
pytest backend/tests/test_file.py --pdb
```

### Measure Performance

```bash
# Show 10 slowest tests
pytest backend/tests/ --durations=10
```

## Coverage Analysis

### Generate Report

```bash
# HTML report
pytest backend/tests/ --cov=backend --cov-report=html

# Terminal report
pytest backend/tests/ --cov=backend --cov-report=term-missing
```

### Coverage Goals

- **Overall**: 80%+
- **Critical paths**: 95%+ (classification, budgets, Plaid, database)
- **UI components**: 70%+
- **Utilities**: 90%+

## CI/CD Mode

```bash
# Fast mode for continuous integration
pytest backend/tests/ \
  --tb=short \
  --maxfail=1 \
  --cov=backend \
  --cov-report=term-missing \
  --cov-fail-under=70
```

Flags:
- `--tb=short` - Shorter tracebacks
- `--maxfail=1` - Stop after first failure
- `--cov-fail-under=70` - Fail if coverage < 70%

## Common Test Patterns

**Detailed examples and patterns**: See [TEST_PATTERNS.md](TEST_PATTERNS.md)

Includes:
- Unit test examples (fuzzy matching, classification)
- API test examples (endpoints, CORS)
- Database test examples (CRUD operations)
- Mock data patterns
- Parametrized tests
- Async test patterns
- Test fixtures and conftest.py setup
- CI/CD integration (GitHub Actions)
- Test data management
- Performance testing

## Full Test Suite Script

```bash
#!/bin/bash
# Run all tests with coverage

# Unit tests
pytest backend/tests/ --ignore=backend/tests/test_api_*.py -v

# API tests (start backend first)
python -m uvicorn backend.api.main:app --reload --port 8000 &
BACKEND_PID=$!
sleep 5
pytest backend/tests/test_api_*.py -v
kill $BACKEND_PID

# Coverage report
pytest backend/tests/ --cov=backend --cov-report=html --cov-report=term
echo "Coverage report: htmlcov/index.html"
```

## Integration with Other Skills

- **Backend Server Startup** - Required for API tests
- **Database Migration Runner** - Test migrations don't break tests
- **Development Diagnostics** - Validates test environment

## References

- [TEST_PATTERNS.md](TEST_PATTERNS.md) - Complete test examples and patterns
- `backend/tests/` - All test files
- `pytest.ini` - Pytest configuration (if exists)
- Pytest docs: https://docs.pytest.org/

## Last Updated

January 1, 2026
