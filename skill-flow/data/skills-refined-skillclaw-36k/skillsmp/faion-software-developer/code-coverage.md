---
id: code-coverage
name: "Code Coverage"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Code Coverage

## Overview

Code coverage measures how much of your source code is executed during testing. It helps identify untested code paths, but high coverage doesn't guarantee quality tests. Coverage is a tool for finding gaps, not a goal in itself.

## When to Use

- Identifying untested code paths
- Setting minimum coverage standards for CI/CD
- Prioritizing testing efforts
- Tracking testing progress over time
- Code review to ensure new code is tested

## Key Principles

- **Coverage is a guide, not a goal**: 100% coverage doesn't mean bug-free
- **Focus on critical paths**: Business logic over boilerplate
- **Branch coverage over line coverage**: Test all conditions
- **New code should be tested**: Enforce coverage on changes
- **Quality over quantity**: Good tests > many tests

## Best Practices

### Coverage Types

```
┌─────────────────────────────────────────────────────────────┐
│                   COVERAGE TYPES                            │
├─────────────────────────────────────────────────────────────┤
│ LINE COVERAGE                                               │
│   Measures: Which lines were executed                       │
│   Limitation: Doesn't test all conditions                   │
│                                                             │
│   if condition:        # Line covered if condition is True  │
│       do_something()   # Line covered                       │
│   else:                                                     │
│       do_other()       # Might not be covered               │
├─────────────────────────────────────────────────────────────┤
│ BRANCH COVERAGE                                             │
│   Measures: Both branches of conditionals tested            │
│   Better than: Line coverage                                │
│                                                             │
│   if condition:        # Need tests for True AND False      │
│       do_something()                                        │
│   else:                                                     │
│       do_other()                                            │
├─────────────────────────────────────────────────────────────┤
│ PATH COVERAGE                                               │
│   Measures: All possible execution paths                    │
│   Most thorough: But exponential complexity                 │
│                                                             │
│   if a: ...            # Paths: TT, TF, FT, FF              │
│   if b: ...            # 4 paths to test                    │
├─────────────────────────────────────────────────────────────┤
│ CONDITION COVERAGE                                          │
│   Measures: Each boolean sub-expression                     │
│                                                             │
│   if a and b:          # Test: a=T,b=T / a=T,b=F / a=F      │
│       do_something()                                        │
└─────────────────────────────────────────────────────────────┘
```

### Python Coverage with pytest-cov

```bash
# Install
pip install pytest-cov

# Basic coverage run
pytest --cov=mypackage tests/

# With HTML report
pytest --cov=mypackage --cov-report=html tests/

# With branch coverage
pytest --cov=mypackage --cov-branch tests/

# Fail if coverage below threshold
pytest --cov=mypackage --cov-fail-under=80 tests/

# Multiple report formats
pytest --cov=mypackage \
       --cov-report=term-missing \
       --cov-report=html \
       --cov-report=xml \
       tests/
```

### Coverage Configuration

```ini
# pyproject.toml
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/migrations/*",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
fail_under = 80
show_missing = true

[tool.coverage.html]
directory = "htmlcov"

# .coveragerc (alternative)
[run]
source = src
branch = True
omit =
    */tests/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    @abstractmethod
fail_under = 80
```

### pytest.ini Configuration

```ini
# pytest.ini
[pytest]
addopts =
    --cov=src
    --cov-branch
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

testpaths = tests
python_files = test_*.py
python_functions = test_*
```

### Coverage in CI/CD

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-branch --cov-report=xml --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true

      - name: Upload coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: htmlcov/
```

### TypeScript/Jest Coverage

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/**/*.test.{ts,tsx}',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Per-file thresholds
    './src/utils/': {
      branches: 90,
      functions: 90,
      lines: 90,
    },
  },
};
```

```bash
# Run with coverage
npm test -- --coverage

# Watch mode with coverage
npm test -- --coverage --watchAll

# Generate only specific reports
npm test -- --coverage --coverageReporters="text" --coverageReporters="lcov"
```

### Analyzing Coverage Reports

```python
# Example: Identifying uncovered code

# payment_processor.py
class PaymentProcessor:
    def process_payment(self, amount: Decimal, card: Card) -> PaymentResult:
        if amount <= 0:
            raise ValueError("Amount must be positive")  # Line 10

        if not self._validate_card(card):
            raise InvalidCardError("Card validation failed")  # Line 13

        try:
            result = self._charge_card(card, amount)
            if result.success:
                self._send_confirmation(result)  # Line 18
                return result
            else:
                self._log_failure(result)  # Line 21 - UNCOVERED
                raise PaymentFailedError(result.error)
        except NetworkError:
            self._handle_network_error()  # Line 24 - UNCOVERED
            raise

# Coverage report shows:
# Lines 21, 24 not covered - need tests for failure cases

# Add missing tests:
def test_process_payment_logs_failure_on_decline():
    processor = PaymentProcessor()
    processor._charge_card = Mock(return_value=PaymentResult(success=False, error="Declined"))
    processor._log_failure = Mock()

    with pytest.raises(PaymentFailedError):
        processor.process_payment(Decimal("100"), valid_card)

    processor._log_failure.assert_called_once()

def test_process_payment_handles_network_error():
    processor = PaymentProcessor()
    processor._charge_card = Mock(side_effect=NetworkError())
    processor._handle_network_error = Mock()

    with pytest.raises(NetworkError):
        processor.process_payment(Decimal("100"), valid_card)

    processor._handle_network_error.assert_called_once()
```

### Coverage for Specific Code

```python
# Exclude code from coverage

# pragma: no cover - exclude single line or block
def debug_function():  # pragma: no cover
    """Only used for debugging, not tested."""
    print_debug_info()

# Exclude abstract methods
class BaseHandler(ABC):
    @abstractmethod
    def handle(self, request):  # pragma: no cover
        pass

# Exclude type checking blocks
if TYPE_CHECKING:  # pragma: no cover
    from typing import TypeAlias
    RequestType: TypeAlias = dict[str, Any]

# Exclude defensive code
def process(data):
    if data is None:  # pragma: no cover (defensive)
        return None
    return transform(data)

# Mark code as needing tests
def new_feature():  # TODO: Add tests, pragma: no cover
    """New feature, tests pending."""
    pass
```

### Coverage-Driven Development

```python
# Step 1: Check current coverage
# pytest --cov=mypackage --cov-report=term-missing

# Example output:
# Name                    Stmts   Miss Branch BrPart  Cover   Missing
# -------------------------------------------------------------------
# mypackage/auth.py          45     12     20      5    70%   23-28, 45-50
# mypackage/payments.py      80      5     30      2    93%   67, 89-91
# -------------------------------------------------------------------
# TOTAL                     125     17     50      7    84%

# Step 2: Analyze missing lines
# auth.py lines 23-28: Error handling for invalid tokens
# auth.py lines 45-50: Password reset flow

# Step 3: Write targeted tests
def test_invalid_token_returns_unauthorized():
    """Cover auth.py lines 23-28."""
    response = client.get("/protected", headers={"Authorization": "invalid"})
    assert response.status_code == 401

def test_password_reset_sends_email():
    """Cover auth.py lines 45-50."""
    response = client.post("/reset-password", json={"email": "user@example.com"})
    assert response.status_code == 200
    mock_email_service.send.assert_called_once()

# Step 4: Verify coverage improved
# pytest --cov=mypackage --cov-report=term-missing
```

### Coverage Badges

```yaml
# Add coverage badge to README using codecov
# README.md
[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)

# Or using shields.io with coverage report
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/username/gist-id/raw/coverage.json)](https://github.com/username/repo/actions)
```

### Coverage Best Practices Summary

```markdown
## Coverage Guidelines

### Target Coverage Levels
- Overall project: 80%+
- Critical business logic: 90%+
- Utility functions: 70%+
- Generated/boilerplate code: Exclude

### What to Test
- Business logic and domain rules
- Error handling paths
- Edge cases and boundary conditions
- Integration points

### What to Exclude
- Auto-generated code
- Abstract base classes
- Type hints and protocols
- Simple property getters
- Debug/development utilities

### Coverage Review Checklist
[ ] All new code has tests
[ ] Branch coverage for conditionals
[ ] Error paths are tested
[ ] Coverage didn't decrease
[ ] No unnecessary pragma: no cover

### CI/CD Integration
- Fail build if coverage drops
- Report coverage on PRs
- Track coverage trends over time
- Set per-directory thresholds
```

## Anti-patterns

- **Chasing 100%**: Testing trivial code to hit targets
- **Coverage without assertions**: Tests that run code but don't verify
- **Testing implementation**: High coverage of internal details
- **Ignoring branch coverage**: Only checking line coverage
- **Coverage gaming**: Writing tests just to increase numbers
- **No coverage on new code**: Only measuring overall percentage

## References

- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Jest Coverage](https://jestjs.io/docs/configuration#collectcoverage-boolean)
- [Codecov Documentation](https://docs.codecov.com/)
