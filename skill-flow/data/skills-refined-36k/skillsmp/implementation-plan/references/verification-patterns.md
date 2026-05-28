# Verification Command Patterns

This reference provides common verification command patterns for different project types and tools.

## Python Projects

### Standard Test Setup
```bash
# pytest (most common)
pytest tests/ -v

# pytest with coverage
pytest tests/ --cov=src --cov-report=term-missing

# unittest (built-in)
python -m unittest discover

# behave (BDD)
behave features/
```

### Linting and Formatting
```bash
# ruff (fast)
ruff check .

# black (formatting check)
black --check .

# mypy (type checking)
mypy .

# flake8 (linting)
flake8 .

# pylint
pylint src/
```

### Combined Verification
```markdown
## Verification Commands
- `pytest tests/ -v` - Run tests
- `ruff check .` - Linting
- `mypy .` - Type checking
```

## JavaScript/TypeScript Projects

### Node.js with npm
```bash
# Standard test
npm test

# Test with coverage
npm run test:coverage

# Linting
npm run lint

# Type checking
npm run type-check
```

### Vitest
```bash
# Run tests
vitest run

# Run with coverage
vitest run --coverage

# Watch mode
vitest
```

### Jest
```bash
# Run tests
jest

# Run with coverage
jest --coverage

# Watch mode
jest --watch
```

### ESLint and Prettier
```bash
# ESLint check
eslint . --ext .js,.jsx,.ts,.tsx

# Prettier format check
prettier --check "src/**/*.{js,jsx,ts,tsx,json,css,md}"
```

### TypeScript
```bash
# Type check only
tsc --noEmit

# Type check with watch
tsc --watch
```

## Go Projects

### Standard Testing
```bash
# Run all tests
go test ./...

# Run with verbose output
go test -v ./...

# Run with coverage
go test -cover ./...

# Run specific package
go test ./pkg/package_name

# Race condition detection
go test -race ./...
```

### Linting and Formatting
```bash
# gofmt (formatting check)
gofmt -l .

# go vet (static analysis)
go vet ./...

# golangci-lint (comprehensive)
golangci-lint run

# golint (deprecated but still used)
golint ./...
```

### Combined Verification
```markdown
## Verification Commands
- `go test -v ./...` - Run tests
- `gofmt -l .` - Check formatting
- `go vet ./...` - Static analysis
```

## Rust Projects

### Standard Testing
```bash
# Run all tests
cargo test

# Run tests without output
cargo test --quiet

# Run specific test
cargo test test_name

# Run tests in single thread
cargo test -- --test-threads=1
```

### Linting and Formatting
```bash
# clippy (linter)
cargo clippy -- -D warnings

# fmt (formatting check)
cargo fmt -- --check

# Format code
cargo fmt
```

### Combined Verification
```markdown
## Verification Commands
- `cargo test` - Run tests
- `cargo clippy -- -D warnings` - Linting
- `cargo fmt -- --check` - Formatting check
```

## Ruby Projects

### RSpec
```bash
# Run all specs
rspec

# Run with documentation format
rspec --format documentation

# Run specific file
rspec spec/file_spec.rb
```

### Rubocop
```bash
# Linting
rubocop

# Auto-fix issues
rubocop -a

# Check only (no auto-fix)
rubocop --display-only-fail-levels
```

## Java Projects

### Maven
```bash
# Run tests
mvn test

# Run with coverage
mvn test jacoco:report

# Compile and test
mvn clean test
```

### Gradle
```bash
# Run tests
./gradlew test

# Run with coverage
./gradlew test jacocoTestReport

# Check style
./gradlew checkstyleMain
```

## DevOps and Infrastructure

### Docker
```bash
# Build container
docker build -t app:latest .

# Run container
docker run --rm app:latest

# Compose build
docker-compose build

# Compose up
docker-compose up -d
```

### Terraform
```bash
# Validate configuration
terraform validate

# Format check
terraform fmt -check

# Plan (dry-run)
terraform plan

# Lint with tflint
tflint .
```

### Kubernetes
```bash
# Validate manifests
kubectl apply --dry-run=client -f k8s/

# Lint with kube-linter
kube-lint k8s/
```

## Web Projects

### Playwright (E2E)
```bash
# Run E2E tests
npx playwright test

# Run with UI
npx playwright test --ui

# Run specific test
npx playwright test tests/example.spec.ts
```

### Cypress (E2E)
```bash
# Run E2E tests
npx cypress run

# Open interactive mode
npx cypress open

# Run specific spec
npx cypress run --spec "cypress/e2e/spec.cy.js"
```

## Database Verification

### PostgreSQL
```bash
# Run SQL migrations
psql -U user -d database -f migrations/up.sql

# Check migration status
psql -U user -d database -c "SELECT * FROM schema_migrations;"
```

### Alembic (Python)
```bash
# Show current revision
alembic current

# Upgrade to head
alembic upgrade head

# Check for new migrations
alembic check
```

## Multi-Language Projects

For projects using multiple languages, group verification commands by language:

```markdown
## Verification Commands

### Backend (Python)
- `pytest backend/tests/` - Run backend tests
- `mypy backend/` - Type check backend

### Frontend (TypeScript)
- `npm run test --workspace=frontend` - Run frontend tests
- `npm run lint --workspace=frontend` - Lint frontend code

### Infrastructure
- `terraform validate` - Validate Terraform configs
- `docker-compose build` - Build containers
```

## Best Practices

### 1. Order Matters
Put faster checks first to fail early:
```markdown
## Verification Commands
- `ruff check .` - Quick lint check (seconds)
- `mypy .` - Type check (seconds)
- `pytest tests/` - Full test suite (minutes)
```

### 2. Use Specific Paths
Don't waste time running unrelated tests:
```markdown
## Verification Commands
- `pytest tests/test_feature.py` - Test only changed feature
```

### 3. Include Coverage for Important Code
```markdown
## Verification Commands
- `pytest tests/ --cov=src --cov-report=term-missing` - Run with coverage
```

### 4. Separate Fast and Slow Verification
For quick iteration vs. complete verification:

```markdown
## Quick Verification (Development)
- `pytest tests/ -k "test_specific"` - Run specific test
- `ruff check .` - Linting only

## Full Verification (Before Commit)
- `pytest tests/` - All tests
- `ruff check .` - Linting
- `mypy .` - Type checking
- `pytest tests/ --cov=src` - Coverage check
```

## Continuous Integration

For CI/CD pipelines, use commands that produce machine-readable output:

```markdown
## CI Verification Commands
- `pytest tests/ --junitxml=test-results.xml` - JUnit XML output
- `ruff check . --output-format=json > ruff-results.json` - JSON lint results
- `mypy . --html-report mypy-report` - HTML type check report
```

## Troubleshooting

### Tests Pass Locally But Fail in CI
- Check environment differences
- Ensure all dependencies are installed
- Verify test isolation (no shared state)

### Verification Takes Too Long
- Use parallel test execution
- Run only affected tests
- Split unit tests from integration tests

### Flaky Tests
- Run tests multiple times: `pytest --sw` (pytest-xdist)
- Add retries for specific tests
- Check for race conditions with `--race` (Go) or `-race` (Go)
