---
name: testing
description: Comprehensive guide to running tests, coverage, and writing tests for backend, frontend, E2E, and Tauri
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---

# Testing Guide

Use this skill when running tests, checking coverage, writing new tests, or debugging test failures.

## Architecture Overview

| Layer        | Runner     | Location                 | Coverage              |
| ------------ | ---------- | ------------------------ | --------------------- |
| **Backend**  | Bun test   | `api/src/**/*.test.ts`   | Bun native            |
| **Frontend** | Vitest     | `src/**/*.test.ts`       | V8 (Node.js required) |
| **E2E**      | Playwright | `tests/e2e/**/*.spec.ts` | N/A                   |
| **Rust**     | cargo test | `src-tauri/src/`         | Not yet implemented   |

## Quick Commands

```bash
# Run all tests
make test

# Individual test suites
make test-backend      # Backend only (Bun)
make test-frontend     # Frontend only (Vitest)
make test-e2e          # E2E only (Playwright)

# With coverage
make test-backend-coverage   # Bun native coverage
make test-frontend-coverage  # Requires Node.js
make test-coverage           # Both (skips frontend if no Node.js)

# Quality checks
make lint              # ESLint + Clippy
make format-check      # Prettier + rustfmt
```

## Coverage Goals

| Metric                 | Goal  | Current        |
| ---------------------- | ----- | -------------- |
| Backend line coverage  | >=80% | ~94%           |
| Frontend line coverage | >=80% | Measured in CI |
| Total test count       | >600  | 681            |

## Node.js Exception for Frontend Coverage

> **This is the ONLY exception to the "no Node.js" rule in this project.**

### Why Required

Vitest's coverage provider (`@vitest/coverage-v8`) depends on `node:inspector`, which Bun hasn't implemented yet.

- **Tracking issue**: https://github.com/oven-sh/bun/issues/2445

### Setup (macOS)

1. Install NVM:

   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
   source ~/.zshrc
   ```

2. Install and use Node.js 22:

   ```bash
   nvm install 22
   nvm use 22
   ```

3. Run coverage:
   ```bash
   make test-frontend-coverage
   # or: npx vitest run --coverage
   ```

The project has a `.nvmrc` file configured for Node.js 22.

---

## Backend Testing (Bun)

### Configuration

- **Runner**: Bun's native test runner
- **Files**: `api/src/**/*.test.ts` (co-located with source)
- **Command**: `cd api && bun test`

### Test Structure

```
api/src/
├── services/
│   ├── bills-service.ts
│   ├── bills-service.test.ts    # Tests next to source
│   ├── storage.ts
│   └── storage.test.ts
└── utils/
    ├── validators.ts
    └── validators.test.ts
```

### Writing Backend Tests

```typescript
import { describe, it, expect, beforeEach, mock } from 'bun:test';
import { BillsService } from './bills-service';

describe('BillsService', () => {
  let service: BillsService;

  beforeEach(() => {
    service = new BillsService();
  });

  it('should create a bill', async () => {
    const bill = await service.create({ name: 'Test', amount: 100 });
    expect(bill.id).toBeDefined();
    expect(bill.name).toBe('Test');
  });

  it('should validate required fields', () => {
    expect(() => service.validate({})).toThrow('Name is required');
  });
});
```

### Mocking in Bun

```typescript
import { mock } from 'bun:test';

// Mock a module
mock.module('./storage', () => ({
  read: mock(() => Promise.resolve([])),
  write: mock(() => Promise.resolve()),
}));
```

---

## Frontend Testing (Vitest)

### Configuration

- **Config file**: `vitest.config.ts`
- **Environment**: jsdom
- **Files**: `src/**/*.{test,spec}.ts`
- **Setup file**: `vitest-setup.ts`

### Key Config Options

```typescript
// vitest.config.ts
export default defineConfig({
  plugins: [sveltekit(), svelteTesting()],
  test: {
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.{js,ts}'],
    globals: true,
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,svelte}'],
    },
  },
});
```

### Writing Frontend Tests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { get } from 'svelte/store';
import { billsStore } from './bills';

describe('billsStore', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('should start with empty bills', () => {
    const bills = get(billsStore);
    expect(bills).toEqual([]);
  });

  it('should add a bill', async () => {
    await billsStore.add({ name: 'Test', amount: 50 });
    const bills = get(billsStore);
    expect(bills).toHaveLength(1);
  });
});
```

### Testing Svelte Components

```typescript
import { render, screen } from '@testing-library/svelte';
import Toast from './Toast.svelte';

describe('Toast', () => {
  it('renders message', () => {
    render(Toast, { props: { message: 'Hello' } });
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });
});
```

---

## E2E Testing (Playwright)

### Configuration

- **Config file**: `playwright.config.ts`
- **Test directory**: `tests/e2e/`
- **Base URL**: `http://localhost:1420`
- **Web server**: `make dev-browser` (auto-started)

### Running E2E Tests

```bash
# Run all E2E tests
make test-e2e

# Run with UI (interactive)
npx playwright test --ui

# Run specific test file
npx playwright test tests/e2e/smoke.spec.ts

# Debug mode
npx playwright test --debug
```

### Writing E2E Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test('should load the main page', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Budget');
  });

  test('should navigate to settings', async ({ page }) => {
    await page.goto('/');
    await page.click('text=Settings');
    await expect(page).toHaveURL('/settings');
  });
});
```

### Playwright Tips

- Screenshots on failure: automatically saved
- Traces: enabled on first retry (`trace: 'on-first-retry'`)
- Reports: HTML report at `playwright-report/`

---

## Rust Testing (Tauri)

Currently **no Rust tests** exist in `src-tauri/`. To add them:

### Adding Rust Unit Tests

```rust
// src-tauri/src/lib.rs

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_port_parsing() {
        let line = "Listening on http://localhost:3456";
        let port = extract_port(line);
        assert_eq!(port, Some(3456));
    }
}
```

### Running Rust Tests

```bash
cd src-tauri && cargo test
```

### Adding to Makefile (future)

```makefile
test-rust: ## Run Rust tests
	@echo "Running Rust tests..."
	@cd src-tauri && cargo test
```

---

## CI Integration

GitHub Actions runs tests automatically on PRs:

1. **Backend tests**: `bun test` with coverage
2. **Frontend tests**: `npx vitest run --coverage` (uses Node.js)
3. **E2E tests**: Playwright on headless Chromium
4. **Linting**: ESLint + Clippy

Coverage reports are uploaded as artifacts on each PR.

---

## Test File Inventory

### Backend Tests (29 files)

```
api/src/services/*.test.ts   # Service tests
api/src/utils/*.test.ts      # Utility tests
```

### Frontend Tests (14 files)

```
src/stores/*.test.ts         # Store tests
src/lib/*.test.ts            # Library tests
src/components/**/*.test.ts  # Component tests
```

### E2E Tests (1 file)

```
tests/e2e/smoke.spec.ts      # Smoke tests
```

---

## Troubleshooting

### "Cannot find module" in tests

```bash
# Reinstall dependencies
bun install
cd api && bun install
```

### Frontend coverage not working

```bash
# Ensure Node.js is installed
node --version  # Should be 22.x

# If using nvm
nvm use 22
make test-frontend-coverage
```

### E2E tests timing out

```bash
# Kill stray processes
make kill-dev

# Increase timeout in playwright.config.ts if needed
```

### Vitest hanging

```bash
# Clear Vite cache
rm -rf node_modules/.vite

# Run with verbose output
bunx vitest run --reporter=verbose
```
