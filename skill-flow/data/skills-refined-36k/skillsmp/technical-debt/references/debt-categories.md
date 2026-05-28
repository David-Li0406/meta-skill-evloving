# Technical Debt Categories

Detailed breakdown of technical debt types with identification patterns.

## Code Debt

Poor code quality that makes the codebase harder to maintain.

### Duplication

**Indicators:**
- Same logic in multiple places
- Copy-pasted code blocks
- Similar methods with minor variations

**Detection:**
```bash
# Use code duplication detector
jscpd --reporters console --threshold 5 .
npx jsinspect --threshold 30 src/
```

**Example:**
```python
# Duplicated in 3 controllers
def format_phone(phone):
    return re.sub(r'\D', '', phone)[:10]
```

### Complexity

**Indicators:**
- Methods over 50 lines
- Cyclomatic complexity > 10
- Deep nesting (> 3 levels)

**Detection:**
```bash
# Python complexity
radon cc -a -s src/

# JavaScript complexity
npx complexity-report --format plain src/
```

**Example:**
```python
def process_order(order):  # 200+ lines
    if order.type == 'regular':
        if order.customer.is_premium:
            if order.total > 100:
                # 10 more levels...
```

### Missing Error Handling

**Indicators:**
- Bare except clauses
- No error recovery
- Silent failures

**Detection:**
```bash
grep -rn "except:" --include="*.py"
grep -rn "catch {" --include="*.ts"
```

### Hardcoded Values

**Indicators:**
- Magic numbers
- Hardcoded URLs/paths
- Embedded credentials

**Detection:**
```bash
grep -rn "http://\|https://" --include="*.py" | grep -v "example.com"
grep -rn "[0-9]\{4,\}" --include="*.py"  # Large numbers
```

## Architecture Debt

Structural issues that affect the overall system design.

### Tight Coupling

**Indicators:**
- Classes with many dependencies
- Circular imports
- God objects

**Detection:**
```bash
# Find circular imports
python -c "import myapp"  # Import errors indicate cycles

# Check class dependencies
grep -rn "import\|from" --include="*.py" | wc -l
```

**Example:**
```python
# OrderService depends on 15+ other services
class OrderService:
    def __init__(self, user_svc, product_svc, payment_svc,
                 shipping_svc, notification_svc, ...):
```

### Wrong Abstraction Level

**Indicators:**
- Premature optimization
- Over-engineering
- Wrong design patterns

**Example:**
```python
# Over-engineered for simple CRUD
class OrderFactory(AbstractFactory):
    class OrderBuilder(AbstractBuilder):
        class OrderDirector(AbstractDirector):
            # Just to create a simple order...
```

### Missing Boundaries

**Indicators:**
- Business logic in controllers
- Database queries in views
- No clear module boundaries

**Detection:**
```bash
# SQL in controllers
grep -rn "SELECT\|INSERT\|UPDATE" --include="*controller*"
```

## Test Debt

Insufficient or poor quality testing.

### Low Coverage

**Indicators:**
- Coverage below target (typically 80%)
- Critical paths untested
- Only happy path tested

**Detection:**
```bash
pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

### Flaky Tests

**Indicators:**
- Tests that sometimes pass/fail
- Time-dependent tests
- Order-dependent tests

**Detection:**
```bash
# Run tests multiple times
for i in {1..10}; do pytest tests/; done
```

### Missing Test Types

| Type | Purpose | Often Missing |
|------|---------|---------------|
| Unit | Isolated logic | Edge cases |
| Integration | Component interaction | Error paths |
| E2E | User workflows | Full flows |
| Performance | Speed/load | Any |
| Security | Vulnerabilities | Any |

## Documentation Debt

Missing or outdated documentation.

### No API Documentation

**Indicators:**
- No OpenAPI spec
- Undocumented endpoints
- Missing examples

**Detection:**
```bash
# Check for OpenAPI files
find . -name "openapi*" -o -name "swagger*"

# Check for docstrings
grep -rL '"""' --include="*.py" src/
```

### Outdated README

**Indicators:**
- Setup instructions don't work
- Missing sections
- Old screenshots

### Missing Code Comments

**Indicators:**
- Complex logic without explanation
- No "why" comments
- Outdated comments

## Dependency Debt

Issues with external dependencies.

### Outdated Dependencies

**Indicators:**
- Major versions behind
- Security vulnerabilities
- Deprecated packages

**Detection:**
```bash
# Python
pip list --outdated
pip-audit

# JavaScript
npm outdated
npm audit

# Ruby
bundle outdated
bundle-audit
```

### Abandoned Dependencies

**Indicators:**
- No commits in 2+ years
- Unresolved security issues
- No maintainer

**Detection:**
```bash
# Check package age
npm view <package> time
```

### Too Many Dependencies

**Indicators:**
- Large dependency tree
- Duplicate dependencies
- Unused dependencies

**Detection:**
```bash
# Python
pip freeze | wc -l

# JavaScript
npm ls --depth=0 | wc -l

# Find unused
npx depcheck
```

## Infrastructure Debt

Operational and deployment issues.

### Manual Processes

**Indicators:**
- Manual deployments
- No CI/CD
- Manual testing before release

### Missing Monitoring

**Indicators:**
- No error tracking
- No performance monitoring
- No alerting

### Configuration Sprawl

**Indicators:**
- Configs in multiple places
- Inconsistent between environments
- Secrets in code

## Severity Guidelines

| Severity | Impact | Response Time |
|----------|--------|---------------|
| Critical | Security vulnerability, data loss | Immediate |
| High | Major feature broken, blocking | This sprint |
| Medium | Development slowed | Next sprint |
| Low | Minor inconvenience | When convenient |

## Debt Interest

Technical debt accumulates "interest" over time:

```
Week 1: 1 hour to work around
Week 4: 2 hours (developers forget context)
Week 12: 4 hours (more code depends on it)
Week 52: 8 hours (became "how it's done")
```

Early resolution prevents interest accumulation.
