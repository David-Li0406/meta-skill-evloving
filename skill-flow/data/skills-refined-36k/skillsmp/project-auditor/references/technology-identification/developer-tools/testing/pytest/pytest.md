# Pytest

**Category**: developer-tools/testing
**Homepage**: https://pytest.org

## Package Detection

### PYPI
*Pytest testing framework*

- `pytest`
- `pytest-cov`
- `pytest-asyncio`
- `pytest-mock`
- `pytest-xdist`

## Import Detection

### Python

**Pattern**: `import\s+pytest`
- Type: python_import

**Pattern**: `@pytest\.`
- Type: decorator

**Pattern**: `def\s+test_`
- Type: test_function

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
