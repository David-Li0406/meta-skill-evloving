# Verification Commands Reference

Complete reference for verification commands across different tech stacks.

## JavaScript/TypeScript Projects

### TypeScript Type Checking
```bash
# Standard TypeScript
tsc --noEmit

# With project references
tsc --build --noEmit

# Specific tsconfig
tsc --noEmit --project tsconfig.json
```

### Linting
```bash
# ESLint
eslint . --ext .ts,.tsx,.js,.jsx
eslint . --fix  # Auto-fix

# Next.js
next lint
next lint --fix

# Biome
biome check .
biome check --apply .  # Auto-fix
```

### Testing
```bash
# Jest
jest
jest --coverage
jest --watchAll=false
jest --changedSince=main  # Only changed files

# Vitest
vitest run
vitest run --coverage
vitest run --changed  # Only changed files

# Playwright (E2E)
playwright test
playwright test --ui
```

### Building
```bash
# Generic
npm run build

# Next.js
next build

# Vite
vite build

# Turbo (monorepo)
turbo build
```

## Python Projects

### Type Checking
```bash
# mypy
mypy .
mypy src/
mypy --strict .

# pyright
pyright
pyright src/
```

### Linting
```bash
# Ruff (fast, recommended)
ruff check .
ruff check --fix .

# Flake8
flake8 .
flake8 --max-line-length=100 .

# Black (formatting)
black --check .
black .  # Apply formatting
```

### Testing
```bash
# pytest
pytest
pytest -v
pytest --cov=src
pytest -x  # Stop on first failure
pytest -k "test_user"  # Pattern match
```

### Building
```bash
# Poetry
poetry build

# setuptools
python -m build
```

## Go Projects

### Type Checking (compile check)
```bash
go build ./...
go vet ./...
```

### Linting
```bash
# golangci-lint (recommended)
golangci-lint run
golangci-lint run --fix

# staticcheck
staticcheck ./...
```

### Testing
```bash
go test ./...
go test -v ./...
go test -cover ./...
go test -race ./...  # Race detection
```

### Building
```bash
go build ./...
go build -o bin/app ./cmd/app
```

## Rust Projects

### Type Checking
```bash
cargo check
cargo check --all-targets
```

### Linting
```bash
# Clippy
cargo clippy
cargo clippy -- -D warnings  # Treat warnings as errors
cargo clippy --fix  # Auto-fix

# Format check
cargo fmt --check
cargo fmt  # Apply formatting
```

### Testing
```bash
cargo test
cargo test --all-features
cargo test -- --nocapture  # Show output
```

### Building
```bash
cargo build
cargo build --release
```

## Verification Order Rationale

### Optimal Order: Typecheck → Lint → Test → Build

| Step | Time | Catches |
|------|------|---------|
| 1. Typecheck | ~5-30s | Type errors, missing imports |
| 2. Lint | ~10-60s | Style issues, potential bugs |
| 3. Test | ~30s-5min | Logic errors, regressions |
| 4. Build | ~30s-5min | Bundling issues, env problems |

### Why This Order?
1. **Fast feedback first** - Typecheck is fastest
2. **Catch cheap errors early** - Don't run slow tests if types are wrong
3. **Build last** - Most expensive, catches least

## Smart Testing Strategies

### Only Test Changed Files
```bash
# Jest
jest --changedSince=HEAD~1
jest --onlyChanged

# Vitest
vitest run --changed

# pytest
pytest --lf  # Last failed
pytest -x    # Stop on first failure
```

### Parallel Testing
```bash
# Jest
jest --maxWorkers=4
jest --runInBand  # Sequential (debugging)

# pytest
pytest -n auto  # Requires pytest-xdist
```

### Watch Mode (Development)
```bash
# Jest
jest --watch

# Vitest
vitest

# pytest
pytest-watch
```

## Exit Code Handling

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Continue to next step |
| 1 | Test/check failures | Fix and retry |
| 2 | Command error | Check command syntax |
| 127 | Command not found | Install dependency |
| 130 | Interrupted (Ctrl+C) | Retry or abort |
