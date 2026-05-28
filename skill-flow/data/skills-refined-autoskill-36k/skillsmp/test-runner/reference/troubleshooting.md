# Test Runner Troubleshooting Guide

## Issue: pytest not found

**Symptom:**
```
/bin/bash: line 1: pytest: command not found
```

**Solution:**
1. Use `python -m pytest` instead of `pytest`
2. Verify pytest is in requirements-dev.txt
3. Check if dependencies were installed

## Issue: Import errors in tests

**Symptom:**
```
ModuleNotFoundError: No module named 'src'
```

**Solution:**
1. Check pyproject.toml has `pythonpath = ["src"]`
2. Verify using `python -m pytest` (not bare `pytest`)
3. Ensure src/__init__.py exists

## Issue: Tests pass locally but fail in CI

**Symptom:**
Tests pass in test-runner skill but fail in GitHub Actions

**Possible causes:**
1. **Environment differences**: CI has different Python version
2. **Missing dependencies**: Not in requirements.txt
3. **File paths**: Hard-coded paths that don't exist in CI
4. **Secrets**: Tests need GCP_SERVICE_ACCOUNT_KEY

**Solution:**
1. Check CI logs: `gh run view <run-id> --log-failed`
2. Compare local Python version with CI (Python 3.11)
3. Verify all dependencies in requirements.txt
4. Use relative paths, not absolute

## Issue: Tests are slow

**Symptom:**
Tests take > 30 seconds to run

**Solution:**
1. **During development**: Run specific test files
   ```bash
   python -m pytest tests/test_specific.py -v
   ```
2. **Before commit**: Always run full suite
3. **Identify slow tests**: Use `--durations=10` flag
   ```bash
   python -m pytest tests/ -v --durations=10
   ```

## Issue: Cached test results

**Symptom:**
Tests show old results even after code changes

**Solution:**
1. Clear pytest cache:
   ```bash
   rm -rf .pytest_cache/
   python -m pytest tests/ -v
   ```
2. Clear Python cache:
   ```bash
   find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
   ```

## Performance Guidelines

**Fast feedback is critical:**
- Report results within 5 seconds for small test suites
- For large test suites (> 100 tests), show progress
- If tests take > 30s, note execution time prominently

**Optimization tips:**
- Use pytest's parallel execution: `pytest -n auto` (if pytest-xdist installed)
- Run only affected tests during development
- Always run full suite before commit
