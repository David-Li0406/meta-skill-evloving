# Production E2E Reference

## Minimal Playwright config (production)

- Set `use.baseURL` to the production URL.
- Do not start a dev server in production runs.
- Keep screenshots and traces on failure.

```ts
// playwright.config.ts (production override example)
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  use: {
    baseURL: process.env.E2E_BASE_URL || process.env.NEXT_PUBLIC_APP_URL || "",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  // No webServer in production
});
```

## Environment variables

- `E2E_BASE_URL`: Explicit production URL override.
- `NEXT_PUBLIC_APP_URL`: Fallback base URL.
- `E2E_TEST_EMAIL`: Dedicated production test user.
- `E2E_TEST_PASSWORD`: Dedicated production test password.

## Test data hygiene

- Prefer read-only flows.
- If a write is required, tag created data (e.g., with a unique prefix) and delete it in the same test.
- If cleanup is not possible, stop and ask for explicit approval.

## Discovery-driven journey (read-only)

- Start at base URL; confirm initial render and key layout elements.
- Enumerate navigation entry points (menus, CTAs, footer links).
- Follow links to discover routes; record each unique route visited.
- Detect protected sections and authenticate only if required.
- For list/detail patterns, open at least one detail page.
- Stop when new routes stop appearing or a loop is detected.

## Mutation journey (requires explicit approval)

- Only run after explicit confirmation.
- **Form Integrity Rule:** For every form found, identify and fill EVERY input, select, and textarea. Avoid partial submissions to ensure all field annotations and database constraints are exercised.
- **Diary Mutation:**
  1. Navigate to [`/diary`](/diary).
  2. Fill "Who were you with?" (Select a character from the listbox).
  3. Fill "Where were you?" (Select a location from the listbox).
  4. Fill "What happened?" (Enter a detailed multiline description starting with "TEST_E2E").
  5. Click "Save Entry".
  6. Verify the entry appears in "Your Timeline", checking that character, location, and description are correctly displayed.
  7. Cleanup: Click "Delete" on the test entry and confirm the dialog.
- **Collection Mutation:**
  1. Navigate to [`/collections`](/collections).
  2. Fill "Collection Name" (unique name with "TEST_E2E" prefix).
  3. Fill "Description" (multiline text).
  4. Click "Create Collection".
  5. Verify the collection card appears with the correct name and description.
  6. Cleanup: Delete the collection if UI permits.
- **Character/Episode Social actions:**
  1. Navigate to a Character or Episode detail page.
  2. Test primary buttons (Like, Follow, Add to Collection).
  3. Verify optimistic UI updates and state persistence after refresh.
- Revert changes in the same test when possible.
- Stop if cleanup cannot be guaranteed.

## Reporting template

- Status: pass/fail
- Base URL:
- Timestamp (UTC):
- Routes discovered:
- Errors (console/network):
- Artifacts (screenshots/traces):
