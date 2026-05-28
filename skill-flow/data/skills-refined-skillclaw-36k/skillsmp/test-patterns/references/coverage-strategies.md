# Coverage Strategies

Approaches to achieving meaningful test coverage.

## Understanding Coverage Metrics

### Types of Coverage

| Metric | What It Measures | Usefulness |
|--------|------------------|------------|
| **Line Coverage** | Lines executed | Basic, can be misleading |
| **Branch Coverage** | Decision paths taken | Better, catches conditionals |
| **Function Coverage** | Functions called | Good for API coverage |
| **Statement Coverage** | Statements executed | Similar to line |
| **Condition Coverage** | Boolean sub-expressions | Most thorough |

### Coverage Tools by Language

```bash
# Python - pytest-cov
pytest --cov=myapp --cov-report=html

# JavaScript/TypeScript - c8/istanbul
npx c8 npm test

# Ruby - SimpleCov
# Add to test_helper.rb:
# require 'simplecov'
# SimpleCov.start

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Coverage Strategies

### 1. Critical Path First

Focus on business-critical code first:

```python
# Identify critical paths
CRITICAL_MODULES = [
    "payment",
    "authentication",
    "order_processing",
    "user_management"
]

# Configure coverage requirements
# pytest.ini or pyproject.toml
[tool.coverage.run]
source = ["myapp"]

[tool.coverage.report]
fail_under = 90
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError"
]
```

### 2. Risk-Based Coverage

Prioritize by risk:

| Risk Level | Coverage Target | Examples |
|------------|-----------------|----------|
| Critical | 95%+ | Payment, Auth, Data mutations |
| High | 85%+ | Core business logic |
| Medium | 70%+ | API endpoints, Services |
| Low | 50%+ | Utilities, Helpers |

### 3. Boundary Coverage

Test boundaries and edge cases:

```python
def test_discount_boundaries():
    # Boundary: 0%
    assert calculate_discount(100, 0) == 100

    # Boundary: 100%
    assert calculate_discount(100, 100) == 0

    # Just inside valid range
    assert calculate_discount(100, 1) == 99
    assert calculate_discount(100, 99) == 1

    # Just outside valid range
    with pytest.raises(ValueError):
        calculate_discount(100, -1)
    with pytest.raises(ValueError):
        calculate_discount(100, 101)
```

### 4. Branch Coverage Strategy

Ensure all branches are tested:

```python
def process_order(order):
    if order.is_rush:
        if order.total > 100:
            apply_rush_discount(order)
        send_rush_notification(order)
    else:
        if order.total > 500:
            apply_bulk_discount(order)

    return order

# Tests for all branches
def test_rush_order_over_100():
    order = Order(is_rush=True, total=150)
    result = process_order(order)
    assert result.discount_applied

def test_rush_order_under_100():
    order = Order(is_rush=True, total=50)
    result = process_order(order)
    assert not result.discount_applied

def test_regular_order_over_500():
    order = Order(is_rush=False, total=600)
    result = process_order(order)
    assert result.bulk_discount_applied

def test_regular_order_under_500():
    order = Order(is_rush=False, total=100)
    result = process_order(order)
    assert not result.bulk_discount_applied
```

## Coverage Analysis

### Finding Coverage Gaps

```bash
# Generate detailed report
pytest --cov=myapp --cov-report=term-missing

# Output shows uncovered lines
Name                    Stmts   Miss  Cover   Missing
------------------------------------------------------
myapp/payment.py          100     10    90%   45-48, 72-75
myapp/orders.py            80      5    94%   33, 67-70
```

### Prioritizing Gaps

```python
# Script to analyze coverage gaps by risk
import json

def analyze_coverage_gaps(coverage_file, risk_config):
    with open(coverage_file) as f:
        coverage = json.load(f)

    gaps = []
    for file, data in coverage['files'].items():
        missing = data['missing_lines']
        if missing:
            risk = risk_config.get(file, 'low')
            gaps.append({
                'file': file,
                'missing': len(missing),
                'risk': risk,
                'priority': calculate_priority(len(missing), risk)
            })

    return sorted(gaps, key=lambda x: x['priority'], reverse=True)
```

## Mutation Testing

Go beyond line coverage with mutation testing:

```bash
# Python - mutmut
mutmut run --paths-to-mutate=myapp/

# JavaScript - Stryker
npx stryker run
```

### Understanding Mutations

```python
# Original code
def is_adult(age):
    return age >= 18

# Mutations tested:
# 1. return age > 18   (boundary mutation)
# 2. return age <= 18  (operator mutation)
# 3. return age >= 17  (value mutation)
# 4. return True       (return mutation)

# Good test catches all mutations:
def test_is_adult():
    assert is_adult(18) == True   # Catches mutation 1
    assert is_adult(17) == False  # Catches mutation 2, 3
    assert is_adult(19) == True   # Catches mutation 4
```

## Coverage Configuration

### Excluding Non-Testable Code

```python
# .coveragerc or pyproject.toml
[tool.coverage.report]
exclude_lines = [
    # Standard exclusions
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",

    # Type checking
    "if TYPE_CHECKING:",
    "if typing.TYPE_CHECKING:",

    # Debug/development code
    "if __name__ == .__main__.:",
    "if settings.DEBUG:",

    # Abstract methods
    "@abstractmethod",
]

omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]
```

### Per-Module Targets

```python
# Custom coverage checker
COVERAGE_TARGETS = {
    "myapp/payment": 95,
    "myapp/auth": 95,
    "myapp/api": 85,
    "myapp/utils": 70,
}

def check_coverage_targets(coverage_data):
    failures = []
    for module, target in COVERAGE_TARGETS.items():
        actual = coverage_data.get(module, 0)
        if actual < target:
            failures.append(f"{module}: {actual}% < {target}%")
    return failures
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run tests with coverage
  run: pytest --cov=myapp --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
    fail_ci_if_error: true

- name: Coverage comment on PR
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ github.token }}
```

### Coverage Gates

```yaml
# codecov.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%  # Allow 2% drop

    patch:
      default:
        target: 90%  # New code must be well tested

  flags:
    unit:
      target: 85%
    integration:
      target: 75%
```

## Coverage Anti-Patterns

### 1. Testing for Coverage Numbers

```python
# BAD - Tests lines but not behavior
def test_process_order():
    order = Order()
    process_order(order)  # Just runs code, no assertions!
```

### 2. Overtesting Trivial Code

```python
# Unnecessary - getters/setters don't need tests
def test_user_name_getter():
    user = User(name="Alice")
    assert user.name == "Alice"  # Tests Python, not your code
```

### 3. Ignoring Edge Cases for Coverage

```python
# Covers the line but misses bugs
def test_division():
    assert divide(10, 2) == 5  # 100% coverage
    # Missing: divide(10, 0) - the bug!
```

### 4. Coverage Theater

```python
# Achieves coverage without value
def test_all_the_things():
    for cls in [User, Order, Item, Payment]:
        obj = cls()
        str(obj)  # "Tests" __str__
        repr(obj)  # "Tests" __repr__
    # 100% coverage, 0% confidence
```

## Meaningful Coverage Checklist

- [ ] Critical business logic has >90% branch coverage
- [ ] All public APIs have integration tests
- [ ] Error handling paths are tested
- [ ] Boundary conditions are tested
- [ ] Security-sensitive code has comprehensive tests
- [ ] Mutation testing score >80% for critical modules
- [ ] Coverage doesn't decrease on new PRs
- [ ] Tests actually assert expected behavior
