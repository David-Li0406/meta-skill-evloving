---
name: playwright-e2e-spellbook
description: Playwright E2E testing for the Spellbook Tauri desktop application with shared fixtures, page objects, and test utilities. Use when writing or modifying E2E tests for the Spellbook app, debugging test failures, or setting up new test infrastructure. Includes automatic app lifecycle management, file tracking, and common test patterns.
---

# Playwright E2E Testing for Spellbook

Specialized guidance for writing E2E tests for the Spellbook Tauri desktop application using Playwright with custom fixtures and utilities.

## Migrating Existing Tests

**Updating old tests to use modern infrastructure?** See [references/MIGRATION.md](references/MIGRATION.md) for:
- Step-by-step migration checklist
- Quick wins (low effort, high value changes)
- Complete before/after examples
- PR review checklist
- Common migration pitfalls

## Build Requirements Before Testing

> [!CRITICAL]
> **ALWAYS rebuild the application** before running tests after code changes. Playwright tests launch the compiled application, not source code.

### Backend Changes (Rust)

If you modified files in `src-tauri/src/` or `Cargo.toml`:

```powershell
cd spellbook/apps/desktop
pnpm tauri:build --debug
```

This rebuilds the Rust backend and bundles the frontend (30-90 seconds full, 5-15 incremental).

### Frontend Changes (TypeScript/React)

If you only modified files in `src/`:

```powershell
cd spellbook/apps/desktop
pnpm build
```

This creates the production bundle in `dist/` (5-20 seconds).

### Both or Unsure

When in doubt, perform a full rebuild:

```powershell
cd spellbook/apps/desktop
pnpm tauri:build --debug
```

**See `/test-workflow` for the complete rebuild and test workflow.**

## Quick Start Template

```typescript
import { expect, test } from "./fixtures/test-fixtures";
import { TIMEOUTS } from "./fixtures/constants";
import { createTmpFilePath, generateRunId, getTestDirname } from "./fixtures/test-utils";
import { SpellbookApp } from "./page-objects/SpellbookApp";

const __dirname = getTestDirname(import.meta.url);

test.describe("My Feature", () => {
  test("my test case", async ({ appContext, fileTracker }) => {
    const { page } = appContext;
    const app = new SpellbookApp(page);
    const runId = generateRunId();

    // Your test code here
  });
});
```

## Core Infrastructure

### Playwright Fixtures (Automatic Lifecycle)

Import custom fixtures instead of base Playwright test:

```typescript
import { expect, test } from "./fixtures/test-fixtures";
```

**Available fixtures:**
- `appContext`: Tauri app with browser, page, and process handles (auto cleanup)
- `fileTracker`: File tracker for temporary files (auto cleanup)

**Benefits:**
- No manual `beforeAll`/`afterAll` hooks
- Automatic cleanup even on test failure
- Type-safe fixture access

### Test Utilities

```typescript
import { createTmpFilePath, generateRunId, getTestDirname } from "./fixtures/test-utils";

// Get __dirname
const __dirname = getTestDirname(import.meta.url);

// Generate unique IDs
const runId = generateRunId();
const name = `Test Item ${runId}`;

// Create temp files with auto-tracking
const filePath = createTmpFilePath(__dirname, "backup.zip", fileTracker);
```

### Standard Timeouts

```typescript
import { TIMEOUTS } from "./fixtures/constants";

await expect(element).toBeVisible({ timeout: TIMEOUTS.medium });
```

| Constant | Value | Use Case |
|----------|-------|----------|
| `TIMEOUTS.short` | 5000ms | Quick UI updates |
| `TIMEOUTS.medium` | 15000ms | Form submissions, navigation |
| `TIMEOUTS.long` | 30000ms | App startup, complex operations |
| `TIMEOUTS.batch` | 120000ms | Batch imports, file processing |

## SpellbookApp Page Object

Always use the page object for common interactions:

```typescript
const app = new SpellbookApp(page);

// Navigation
await app.navigate("Library" | "Characters" | "Import" | "Add Spell");

// Spell management
await app.createSpell({ name, level, description, ... });
await app.openSpell(name);
await app.importFile(path, allowOverwrite?);

// Character management
await app.createCharacter(name);
await app.selectCharacter(name);
await app.openCharacterEditor(name);
await app.addClass(className);
await app.addSpellToClass(className, spellName, "KNOWN" | "PREPARED");
```

## Dialog Handling

### Custom Modals (React-based)

```typescript
import { handleCustomModal } from "./utils/dialog-handler";

await page.getByRole("button", { name: "Save" }).click();
await handleCustomModal(page, "OK");

await page.getByRole("button", { name: "Delete" }).click();
await handleCustomModal(page, "Confirm");
```

### Native Browser Dialogs

```typescript
import { setupDialogHandler } from "./utils/dialog-handler";

const cleanup = setupDialogHandler(page, {
  acceptDelete: true,
  dismissValidation: true,
  debug: true,
});

// Trigger action that shows dialog
await page.getByRole("button", { name: "Reset" }).click();

cleanup(); // CRITICAL: Stop listening after action
```

## Test Organization

Use `test.step()` for logical phases:

```typescript
test("Feature Test", async ({ appContext }) => {
  await test.step("Setup: Create test data", async () => {
    // setup
  });

  await test.step("Action: Perform operation", async () => {
    // main test action
  });

  await test.step("Verify: Check results", async () => {
    // assertions
  });
});
```

## Locator Strategy

Use the most user-facing, semantic locators available. Follow this priority hierarchy:

| Priority | Locator Method | Use Case | Example |
|----------|---------------|----------|---------|
| **1** | `getByTestId()` | Interactive elements, dynamic content | `page.getByTestId('save-button')` |
| **2** | `getByRole()` | Semantic HTML elements | `page.getByRole('button', { name: 'Save' })` |
| **3** | `getByLabel()` | Form fields with labels | `page.getByLabel('Character Name')` |
| **4** | `getByPlaceholder()` | Inputs with placeholders | `page.getByPlaceholder('Search spells...')` |
| **5** | `getByText()` | Static text content | `page.getByText('Fireball')` |
| **6** | `locator()` with CSS | Last resort only | `page.locator('.btn-primary')` |

### When New UI Elements Are Added

Before writing tests for new UI components:

1. **Verify the element has a `data-testid`**:
   ```typescript
   const count = await page.getByTestId('new-element-id').count();
   console.log(`Found ${count} elements`); // Should be 1
   ```

2. **If `data-testid` is missing**, check if semantic locators work:
   ```typescript
   await page.getByRole('button', { name: 'New Button' }).click();
   ```

3. **If neither works**, request the UI developer add `data-testid` to the component (see `src/AGENTS.md` for guidelines).

### Debugging Locators

If you can't find an element:

```typescript
// List all available data-testid attributes
const testIds = await page.locator('[data-testid]').evaluateAll(
  nodes => nodes.map(n => n.getAttribute('data-testid'))
);
console.log('Available testids:', testIds);

// Check if element exists anywhere
const exists = await page.locator('text=My Element').count();
console.log(`Element exists: ${exists > 0}`);
```

## Common Patterns

### Creating Unique Test Data

```typescript
const runId = generateRunId();
const spellName = `Test Spell ${runId}`;
const tmpFile = createTmpFilePath(__dirname, "data.json", fileTracker);
```

### Working with Temporary Files

```typescript
test("backup flow", async ({ fileTracker }) => {
  const backupPath = createTmpFilePath(__dirname, "backup.zip", fileTracker);

  // Use the file
  fs.writeFileSync(backupPath, data);

  // Cleanup is automatic!
});
```

### Settlement Waits

After navigation or complex UI switches:

```typescript
await app.navigate("Library");
await page.waitForTimeout(500); // Standard settlement wait
```

## Running Tests

```powershell
# Run all tests
npx playwright test

# Run specific test file
npx playwright test vault.spec.ts

# Run with UI mode
npx playwright test --ui

# Show HTML report
npx playwright show-report
```

## Debugging Test Failures

When tests fail, follow this systematic approach to gather useful debug information:

### 1. View the HTML Report

```powershell
npx playwright show-report
```

The report provides:
- Failed test details with stack traces
- Screenshots at the point of failure
- Full execution traces with DOM snapshots
- Network activity and console logs

### 2. Analyze the Trace

In the HTML report:
1. Click on the failed test
2. Select the **Trace** tab
3. Review:
   - **DOM snapshots** at each test step
   - **Network requests** (look for failed API calls)
   - **Console logs** (check for JavaScript errors)
   - **The exact line** where the test failed

### 3. Capture Debug Screenshots

Add a screenshot immediately before the failing assertion:

```typescript
// Add this before the assertion that's failing
await page.screenshot({ path: 'tests/screenshots/debug.png', fullPage: true });

// Then the assertion
await expect(element).toBeVisible();
```

The screenshot will be saved to `spellbook/apps/desktop/tests/screenshots/debug.png`.

### 4. Extract Error Context

When reporting or analyzing failures, include:
- **The assertion that failed** (exact line and message)
- **DOM state** at failure (from trace or screenshot)
- **Console errors** (check browser console in trace)
- **Network failures** (failed requests in trace)
- **Recent code changes** that might have affected the test

### 5. Common Failure Patterns

| Error Pattern | Likely Cause | Solution |
|---------------|--------------|----------|
| `Timeout: element not found` | Missing `data-testid` or element doesn't exist | Check UI code, add `data-testid`, or use semantic locators |
| `Strict mode violation` | Multiple elements match locator | Make locator more specific with filters |
| `Navigation timeout` | App startup too slow or crashed | Check app logs, increase timeout, verify build |
| `Database is locked` | Previous test didn't clean up | Kill orphaned processes, check data isolation |

### 6. Use Playwright Inspector

For interactive debugging:

```powershell
npx playwright test --debug
```

This opens the Playwright Inspector where you can:
- Step through the test line-by-line
- Inspect the DOM at each step
- Try different locators interactively
- See live screenshots

### 7. Verify Element Exists

Before writing assertions, verify the element can be found:

```typescript
// Debug: Check element count
const count = await page.getByTestId('new-element').count();
console.log(`Found ${count} elements with testid 'new-element'`);

// Debug: List all testids
const allTestIds = await page.locator('[data-testid]').allTextContents();
console.log('Available testids:', allTestIds);
```

## Troubleshooting

### Port Collisions

Tests use isolated ports per worker. If "Address already in use" errors occur:

1. Ensure no other app instances are running
2. Check for orphaned processes: `Get-Process | Where-Object {$_.ProcessName -match "spellbook"} | Stop-Process`

### WebView2 State Pollution

Tests use isolated data directories. If state leaks between runs:

- Check `tests/tmp/data-w*` directories
- Cleanup happens automatically but may fail if processes don't terminate cleanly

### Blank Screen on Launch

Debug builds expect Vite dev server at `http://127.0.0.1:5173`. The test infrastructure handles this automatically.

## Advanced: Manual Lifecycle

For test suites sharing app state across multiple tests:

```typescript
import { type TauriAppContext, cleanupTauriApp, createFileTracker, launchTauriApp } from "./fixtures/tauri-fixture";

let appContext: TauriAppContext | null = null;
const fileTracker = createFileTracker();

test.beforeAll(async () => {
  appContext = await launchTauriApp();
});

test.afterAll(async () => {
  if (appContext) {
    await cleanupTauriApp(appContext);
  }
  fileTracker.cleanup();
});

test("my test", async () => {
  if (!appContext) throw new Error("App context not initialized");
  const { page } = appContext;
  // test code
});
```

**Use manual lifecycle when:**
- Sharing app state across multiple tests
- Running large test suites (minimize app launches)
- Need fine-grained control over lifecycle

## Key Constraints

- **Windows only**: Tests require WebView2 (Windows-only)
- **Workers**: Configured for `workers: 1` to avoid port collisions
- **Timeout**: Default test timeout is 120000ms (2 minutes)
- **Data isolation**: Each test run uses unique data directory
