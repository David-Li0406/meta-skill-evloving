# Test File Locations

## Directory Structure

```
src/
├── **/__tests__/
│   ├── *.test.ts        # Unit tests
│   ├── *.test.tsx       # Component unit tests
│   └── *.integration.test.ts(x)  # Integration tests

playwright/
└── tests/
    └── *.spec.ts        # E2E tests
```

## Naming Conventions

| Test Type | Pattern | Example |
|-----------|---------|---------|
| Unit test | `*.test.ts(x)` | `MyComponent.test.tsx` |
| Integration | `*.integration.test.ts(x)` | `emailQueue.integration.test.ts` |
| E2E | `*.spec.ts` | `email-composer.spec.ts` |

## Location Rules

- Unit tests: Colocated with source in `__tests__/` subdirectory
- Integration tests: Same location, with `.integration.test` suffix
- E2E tests: All in `playwright/tests/` directory

## Test Discovery

```bash
# Find all unit tests
ls src/**/__tests__/*.test.ts src/**/__tests__/*.test.tsx

# Find all integration tests
ls src/**/__tests__/*.integration.test.ts src/**/__tests__/*.integration.test.tsx

# Find all E2E tests
ls playwright/tests/*.spec.ts
```

## Which Tests to Run

| Changed File Type | Run These Tests |
|-------------------|-----------------|
| Component (`.tsx`) | Unit + E2E |
| Hook (`use*.ts`) | Unit + Integration |
| Service (`*.service.ts`) | Unit + Integration |
| Utility (`utils/*.ts`) | Unit only |
| E2E fixture | E2E only |
