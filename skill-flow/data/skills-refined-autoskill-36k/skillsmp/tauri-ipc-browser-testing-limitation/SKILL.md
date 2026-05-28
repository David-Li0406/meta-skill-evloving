---
name: tauri-ipc-browser-testing-limitation
description: |
  Tauri IPC commands fail silently when testing via browser at localhost. Use when:
  (1) Tauri invoke() calls return no data or fail silently in Playwright/browser tests,
  (2) window.__TAURI__ is undefined when accessing localhost:port directly,
  (3) App works in Tauri window but not when tested via browser automation,
  (4) React Query or other data fetching shows empty results for Tauri commands.
  The fix is to test in the actual Tauri webview or mock the Tauri API for browser tests.
author: Claude Code
version: 1.0.0
date: 2025-01-23
---

# Tauri IPC Browser Testing Limitation

## Problem
Tauri commands invoked via `@tauri-apps/api/core` fail silently when the app is accessed
through a regular browser (e.g., Playwright automation at localhost:1420) instead of the
actual Tauri webview. The `invoke()` calls return empty results or fail without errors.

## Context / Trigger Conditions

**Symptoms:**
- `invoke('command_name', {...})` returns undefined or empty arrays
- No console errors visible
- React Query shows "No results found" for queries that should work
- `window.__TAURI__` is `undefined` in browser console

**When this occurs:**
- Running `cargo tauri dev` starts both Vite dev server (localhost:1420) and Tauri app
- Testing via Playwright or any browser automation against localhost:1420
- Opening localhost:1420 directly in Chrome/Firefox instead of using the Tauri window
- The Tauri desktop window works fine, but browser tests fail

**NOT this issue if:**
- Tauri window itself shows errors
- Commands fail with visible error messages
- Compilation errors in Rust backend

## Solution

### Option 1: Test in Actual Tauri Webview (Recommended)
Use Tauri's built-in webview for testing. The Tauri window that opens when running
`cargo tauri dev` has full IPC access.

For automated testing, use WebDriver with Tauri:
```rust
// In Cargo.toml
[dev-dependencies]
tauri = { version = "2", features = ["test"] }
```

### Option 2: Mock Tauri API for Browser Tests
Create a mock layer for browser testing:

```typescript
// src/lib/tauri-mock.ts
const isTauri = typeof window !== 'undefined' && window.__TAURI__;

export async function invoke<T>(cmd: string, args?: Record<string, unknown>): Promise<T> {
  if (isTauri) {
    const { invoke: tauriInvoke } = await import('@tauri-apps/api/core');
    return tauriInvoke(cmd, args);
  }

  // Mock responses for browser testing
  const mocks: Record<string, unknown> = {
    'search_platforms': [
      { id: '1', title: 'Mock Result', platform: 'hackernews', score: 100 }
    ],
    // Add other commands...
  };

  return mocks[cmd] as T ?? [];
}
```

### Option 3: Use HTTP API Fallback
For commands that need browser testing, expose them as HTTP endpoints:

```rust
// Alternative: Create HTTP endpoints for browser access
#[tauri::command]
async fn search_platforms(...) -> Result<Vec<SearchResult>, String> {
    // This only works in Tauri webview
}

// For browser testing, also expose via HTTP in dev mode
#[cfg(debug_assertions)]
pub fn setup_dev_server(app: &mut App) {
    // Set up axum/actix server on separate port
}
```

## Verification

Check if running in Tauri:
```typescript
// In browser console or code
if (typeof window.__TAURI__ !== 'undefined') {
  console.log('Running in Tauri webview - IPC available');
} else {
  console.log('Running in browser - IPC NOT available');
}
```

## Example

**Test that fails in browser:**
```typescript
// This works in Tauri window, fails silently in browser
const results = await invoke('search_platforms', {
  query: 'test',
  platforms: ['hackernews'],
});
console.log(results); // [] in browser, actual data in Tauri
```

**Detection pattern:**
```typescript
// Add this to your app for debugging
useEffect(() => {
  if (typeof window.__TAURI__ === 'undefined') {
    console.warn('⚠️ Tauri IPC not available - running in browser mode');
  }
}, []);
```

## Notes

- This is by design: Tauri IPC uses a custom protocol that only works in the webview
- The Vite dev server at localhost:1420 is for hot reload, not for direct browser access
- When `cargo tauri dev` runs, use the Tauri window that opens, not the browser
- For E2E testing, consider using Tauri's WebDriver support or Playwright with the
  actual Tauri app binary
- Some teams maintain a separate "browser mode" with mocked data for rapid UI development

## Related

- Tauri Testing Guide: https://tauri.app/v2/guides/test/
- WebDriver support: https://tauri.app/v2/guides/test/webdriver
