# Validation Gates

## Philosophy

**"It works on my machine" is not quality.**

Quality code passes systematic validation gates that prove:
- Style is consistent (linting)
- Types are correct (type checking)
- Logic works (tests)
- Components integrate (integration tests)
- Users experience success (E2E tests)

Gates are checkpoints, not suggestions. **All gates must pass before work is considered complete.**

## The Gate Model

```
Code Written
    ↓
Gate 1: Linting & Formatting ──┐
    ↓                          │
Gate 2: Type Checking ─────────┤ Fast gates (seconds)
    ↓                          │ Run frequently
Gate 3: Unit Tests ────────────┘
    ↓
Gate 4: Integration Tests ─────┐ Slower gates (minutes)
    ↓                          │ Run before commit
Gate 5: E2E Tests ─────────────┘
    ↓
Gate 6: Build/Deploy Check ──── Final gate (run before merge)
    ↓
Code Complete ✓
```

**If any gate fails:** Fix immediately. Don't defer. Don't skip.

## Gate 1: Linting & Formatting

**Purpose:** Enforce consistent code style

**Time:** Seconds

**Run:** After every file save (via editor plugin) or before commit

### Backend (Python)

```bash
# Linting - check style violations
uv run flake8 app/ tests/

# Formatting - enforce consistent style
uv run black --check app/ tests/

# Import sorting
uv run isort --check app/ tests/

# Auto-fix formatting issues
uv run black app/ tests/
uv run isort app/ tests/
```

**Configuration:**

```ini
# File: .flake8
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E203,W503  # Black compatibility
```

```toml
# File: pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

### Frontend (TypeScript)

```bash
# Linting - check style and potential errors
npm run lint

# Formatting - enforce consistent style
npm run format -- --check

# Auto-fix
npm run lint -- --fix
npm run format -- --write
```

**Configuration:**

```json
// File: .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:vue/vue3-recommended",
    "prettier"
  ],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

```json
// File: .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "trailingComma": "es5"
}
```

### Success Criteria

- [ ] No linting errors
- [ ] No formatting violations
- [ ] Imports sorted correctly
- [ ] No `any` types (TypeScript)
- [ ] No unused imports

**If gate fails:** Run auto-fixers, fix remaining issues manually.

## Gate 2: Type Checking

**Purpose:** Verify type safety

**Time:** Seconds

**Run:** Before commit

### Backend (Python with mypy)

```bash
# Type checking
uv run mypy app/ tests/

# Strict mode (recommended)
uv run mypy --strict app/
```

**Configuration:**

```ini
# File: mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
```

### Frontend (TypeScript)

```bash
# Type checking
npm run type-check

# Strict mode
npm run type-check -- --strict
```

**Configuration:**

```json
// File: tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

### Success Criteria

- [ ] No type errors
- [ ] No `any` types (explicit typing everywhere)
- [ ] No implicit type conversions
- [ ] Return types explicit
- [ ] Null checks explicit

**If gate fails:** Add type annotations, fix type mismatches.

## Gate 3: Unit Tests

**Purpose:** Prove individual units work correctly

**Time:** Seconds to minutes

**Run:** After implementing each function/component

### Backend (pytest)

```bash
# Run all unit tests
uv run pytest tests/unit/ -v

# Run specific test file
uv run pytest tests/unit/services/test_user_service.py -v

# Run with coverage
uv run pytest tests/unit/ --cov=app --cov-report=term-missing
```

### Frontend (Vitest)

```bash
# Run all unit tests
npm run test:unit

# Run specific test file
npm run test -- CreateUserForm.test.ts

# Run with coverage
npm run test:coverage
```

### Success Criteria

- [ ] All tests passing
- [ ] Coverage >= 80% for new code
- [ ] Tests run fast (< 10 seconds for unit tests)
- [ ] No skipped tests (unless documented reason)
- [ ] No flaky tests (pass/fail randomly)

**Coverage targets:**

- Service layer: >= 90%
- API endpoints: >= 85%
- Utilities: >= 95%
- Components: >= 80%

**If gate fails:** Fix failing tests immediately. Do not skip or disable tests.

## Gate 4: Integration Tests

**Purpose:** Verify components work together

**Time:** Minutes

**Run:** Before commit, after all unit tests pass

### Backend Integration Tests

```bash
# Run integration tests (with real database)
uv run pytest tests/integration/ -v

# Run with test database setup/teardown
uv run pytest tests/integration/ -v --create-db
```

**Example:**

```python
def test_user_creation_flow(client: TestClient):
    """Test complete user creation through API."""
    # Create user
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Retrieve user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

### Frontend Integration Tests

```bash
# Component integration tests
npm run test:integration

# E2E tests (headless)
npm run test:e2e:headless
```

### Success Criteria

- [ ] All integration tests passing
- [ ] Tests clean up after themselves (no state leakage)
- [ ] Database resets between tests
- [ ] Tests are deterministic (same result every time)

**If gate fails:** Check database state, verify fixtures, fix integration issues.

## Gate 5: E2E Tests

**Purpose:** Verify complete user workflows

**Time:** Minutes

**Run:** Before merge to main branch

### E2E Testing (Cypress/Playwright)

```bash
# Run E2E tests headless
npm run test:e2e:headless

# Run E2E tests with browser
npm run test:e2e

# Run specific spec
npm run test:e2e -- --spec cypress/e2e/user-creation.cy.ts
```

**Example:**

```typescript
// File: cypress/e2e/user-creation.cy.ts
describe('User Creation Flow', () => {
  it('creates user and displays in list', () => {
    cy.visit('/users');
    cy.get('[data-test="create-user-btn"]').click();

    cy.get('input#email').type('test@example.com');
    cy.get('input#first_name').type('Test');
    cy.get('input#last_name').type('User');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/users');
    cy.contains('test@example.com').should('be.visible');
  });
});
```

### Success Criteria

- [ ] Critical paths tested (login, create, update, delete)
- [ ] Tests pass consistently
- [ ] Tests use data-test attributes (not brittle selectors)
- [ ] Tests clean up test data

**E2E test count:** Keep minimal (5-10 tests covering critical workflows)

**If gate fails:** Check backend is running, verify test data setup, fix test selectors.

## Gate 6: Build/Deploy Check

**Purpose:** Verify code builds and deploys successfully

**Time:** Minutes

**Run:** Before merge, in CI/CD pipeline

### Backend Build Check

```bash
# Build Docker image
docker build -t app:latest .

# Run migrations
uv run alembic upgrade head

# Start server (smoke test)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/health  # Should return 200
```

### Frontend Build Check

```bash
# Build production bundle
npm run build

# Check bundle size
npm run analyze

# Serve built files (smoke test)
npm run preview
```

### Success Criteria

- [ ] Build completes without errors
- [ ] No warnings (or documented/approved warnings)
- [ ] Bundle size within limits (< 500KB initial load)
- [ ] Smoke test passes (app starts, health check responds)

**If gate fails:** Fix build errors, optimize bundle size.

## Gate Automation

### Pre-commit Hook

```bash
# File: .git/hooks/pre-commit
#!/bin/sh

echo "Running pre-commit checks..."

# Gate 1: Linting & Formatting
echo "🔍 Linting..."
uv run flake8 app/ tests/ || exit 1
uv run black --check app/ tests/ || exit 1

# Gate 2: Type Checking
echo "🔍 Type checking..."
uv run mypy app/ || exit 1

# Gate 3: Unit Tests
echo "🧪 Running unit tests..."
uv run pytest tests/unit/ -q || exit 1

echo "✅ Pre-commit checks passed!"
```

### CI/CD Pipeline

```yaml
# File: .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Gate 1 - Lint
        run: |
          uv run flake8 app/ tests/
          uv run black --check app/ tests/

      - name: Gate 2 - Type Check
        run: uv run mypy app/

      - name: Gate 3 - Unit Tests
        run: uv run pytest tests/unit/ --cov=app

      - name: Gate 4 - Integration Tests
        run: uv run pytest tests/integration/

      - name: Gate 6 - Build
        run: docker build -t app:latest .
```

## When Gates Fail

### Don't:
- Skip the gate "just this once"
- Disable the test
- Mark test as `@skip` or `@xfail`
- Commit with `--no-verify`
- Tell yourself "I'll fix it later"

### Do:
1. **Stop** - Don't proceed to next gate
2. **Fix** - Address the root cause
3. **Verify** - Re-run the gate until it passes
4. **Understand** - Learn why it failed

### Common Failures

| Gate | Failure | Fix |
|------|---------|-----|
| Linting | Unused import | Remove import |
| Type Check | `any` type | Add explicit type annotation |
| Unit Test | Assertion failed | Fix logic or update test |
| Integration Test | 500 error | Check logs, fix endpoint |
| E2E Test | Element not found | Check test selectors, verify UI |
| Build | Module not found | Check dependencies, update imports |

## Gate Performance

**Gates should be fast:**

- Gate 1 (Lint): < 5 seconds
- Gate 2 (Type): < 10 seconds
- Gate 3 (Unit): < 30 seconds
- Gate 4 (Integration): < 2 minutes
- Gate 5 (E2E): < 5 minutes
- Gate 6 (Build): < 3 minutes

**If gates are slow:**
- Optimize test setup/teardown
- Use test database in memory (SQLite)
- Run tests in parallel
- Cache dependencies in CI

## Validation Gate Checklist

Before marking work complete:

- [ ] Gate 1: Linting passed (no violations)
- [ ] Gate 2: Type checking passed (strict mode)
- [ ] Gate 3: Unit tests passed (>= 80% coverage)
- [ ] Gate 4: Integration tests passed
- [ ] Gate 5: E2E tests passed (critical paths)
- [ ] Gate 6: Build succeeded (no errors)
- [ ] All gates automated in CI/CD
- [ ] Pre-commit hook installed
- [ ] No skipped/disabled tests

## Philosophy

**Gates are not bureaucracy. Gates are proof.**

- **Linting** proves consistency
- **Type checking** proves type safety
- **Unit tests** prove logic correctness
- **Integration tests** prove components work together
- **E2E tests** prove users can complete workflows
- **Build** proves code deploys

**Passing all gates means:** Code is production-ready.

**Skipping gates means:** Code might work, might not, you don't know.

---

**Remember:** Fast feedback from gates prevents slow debugging in production. Run gates early, run gates often, trust gates completely.
