## Migrating Existing Tests to New Infrastructure

This section provides guidance for updating existing tests to use the modern fixture and utility patterns.

### Migration Checklist

When updating an existing test file, follow this checklist:

- [ ] Replace duplicated `TIMEOUTS` constant with import from `./fixtures/constants`
- [ ] Replace `Date.now()` with `generateRunId()` from `./fixtures/test-utils`
- [ ] Replace `fileURLToPath` pattern with `getTestDirname()` from `./fixtures/test-utils`
- [ ] Consider migrating to Playwright fixtures (optional, see below)
- [ ] Consider using `createTmpFilePath()` for temporary files (optional)

### Quick Wins (Low Effort, High Value)

These changes can be made independently and provide immediate benefits:

#### 1. Import TIMEOUTS from Constants

**Before:**
```typescript
const TIMEOUTS = {
  short: 5000,
  medium: 15000,
  long: 30000,
};
```

**After:**
```typescript
import { TIMEOUTS } from "./fixtures/constants";
```

#### 2. Use generateRunId()

**Before:**
```typescript
const runId = Date.now();
const spellName = `Test Spell ${Date.now()}`;
```

**After:**
```typescript
import { generateRunId } from "./fixtures/test-utils";

const runId = generateRunId();
const spellName = `Test Spell ${runId}`;
```

#### 3. Use getTestDirname()

**Before:**
```typescript
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

**After:**
```typescript
import { getTestDirname } from "./fixtures/test-utils";

const __dirname = getTestDirname(import.meta.url);
```

### Full Migration (Higher Effort, Maximum Benefit)

For comprehensive modernization, migrate to Playwright fixtures:

#### Before: Manual Lifecycle

```typescript
import { expect, test } from "@playwright/test";
import type { TauriAppContext } from "./fixtures/tauri-fixture";
import { cleanupTauriApp, launchTauriApp } from "./fixtures/tauri-fixture";

let appContext: TauriAppContext | null = null;

test.beforeAll(async () => {
  appContext = await launchTauriApp();
});

test.afterAll(async () => {
  if (appContext) {
    await cleanupTauriApp(appContext);
  }
});

test("my test", async () => {
  if (!appContext) throw new Error("App context not initialized");
  const { page } = appContext;
  // test code
});
```

#### After: Playwright Fixtures

```typescript
import { expect, test } from "./fixtures/test-fixtures";

test("my test", async ({ appContext }) => {
  const { page } = appContext;
  // test code
});
```

**Benefits:**
- 15+ lines of boilerplate removed
- Automatic cleanup guaranteed
- No null checks needed
- Type-safe fixture access

### Migration Example: Complete Before/After

#### Before (Old Pattern)

```typescript
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { expect, test } from "@playwright/test";
import type { TauriAppContext } from "./fixtures/tauri-fixture";
import { cleanupTauriApp, launchTauriApp } from "./fixtures/tauri-fixture";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const TIMEOUTS = {
  short: 5000,
  medium: 15000,
  long: 30000,
};

let appContext: TauriAppContext | null = null;

test.beforeAll(async () => {
  appContext = await launchTauriApp();
});

test.afterAll(async () => {
  if (appContext) {
    await cleanupTauriApp(appContext);
  }
});

test("my test", async () => {
  if (!appContext) throw new Error("App context not initialized");
  const { page } = appContext;
  const runId = Date.now();
  const testName = `Test ${runId}`;

  // test code
});
```

#### After (Modern Pattern)

```typescript
import { expect, test } from "./fixtures/test-fixtures";
import { TIMEOUTS } from "./fixtures/constants";
import { generateRunId, getTestDirname } from "./fixtures/test-utils";

const __dirname = getTestDirname(import.meta.url);

test("my test", async ({ appContext }) => {
  const { page } = appContext;
  const runId = generateRunId();
  const testName = `Test ${runId}`;

  // test code
});
```

**Result:** 24 lines → 12 lines (50% reduction)

## PR Review Checklist for New Tests

When reviewing PRs that add or modify E2E tests, verify:

### Required Standards

- [ ] Uses `import { expect, test } from "./fixtures/test-fixtures"` (not base Playwright)
- [ ] Uses `TIMEOUTS` from `./fixtures/constants` (no hardcoded timeout values)
- [ ] Uses `generateRunId()` for unique test data (not `Date.now()`)
- [ ] Uses `getTestDirname()` for `__dirname` (not manual `fileURLToPath`)
- [ ] Uses `SpellbookApp` page object for common interactions (not raw locators)
- [ ] Uses `test.step()` to organize test phases
- [ ] Follows locator strategy priority (role → label → placeholder → text → CSS)

### File Management

- [ ] Uses `fileTracker` fixture for temporary files
- [ ] Uses `createTmpFilePath()` for temp file creation (when applicable)
- [ ] No manual file cleanup in `finally` blocks (handled by fixture)

### Dialog Handling

- [ ] Uses `handleCustomModal()` for React modals
- [ ] Uses `setupDialogHandler()` for native dialogs with proper cleanup
- [ ] No `page.on('dialog')` without cleanup

### Test Quality

- [ ] Test names are descriptive and follow existing patterns
- [ ] Unique test data uses `runId` to avoid collisions
- [ ] Assertions use appropriate timeouts from `TIMEOUTS`
- [ ] Settlement waits (500ms) after navigation when needed
- [ ] No arbitrary `page.waitForTimeout()` without comments explaining why

### Documentation

- [ ] Complex test patterns are commented
- [ ] Non-obvious locator strategies are explained
- [ ] Test steps clearly describe what's being tested

## Common Migration Pitfalls

### Pitfall 1: Forgetting to Import fs

When using `createTmpFilePath()`, you may still need `fs` for file operations:

```typescript
import fs from "node:fs";
import { createTmpFilePath } from "./fixtures/test-utils";

const filePath = createTmpFilePath(__dirname, "data.json", fileTracker);
fs.writeFileSync(filePath, data); // Still need fs here
```

### Pitfall 2: Mixing Patterns

Don't mix manual lifecycle with fixtures in the same file:

```typescript
// ❌ BAD: Mixing patterns
import { test } from "./fixtures/test-fixtures";

let appContext: TauriAppContext | null = null; // Don't do this

test.beforeAll(async () => {
  appContext = await launchTauriApp(); // Fixture handles this
});
```

### Pitfall 3: Not Cleaning Up Dialog Handlers

Always call cleanup for native dialog handlers:

```typescript
// ❌ BAD: No cleanup
const cleanup = setupDialogHandler(page, { acceptDelete: true });
await page.getByRole("button", { name: "Delete" }).click();
// Missing cleanup() call!

// ✅ GOOD: Proper cleanup
const cleanup = setupDialogHandler(page, { acceptDelete: true });
try {
  await page.getByRole("button", { name: "Delete" }).click();
} finally {
  cleanup();
}
```
