---
name: browser-ops-guard
description: Optimizes browser usage to reduce system overhead and ensures code quality via console verification.
---

# Browser Operations Guard

This skill governs all browser-related interactions to ensure they are efficient, resource-conscious, and serve as a final quality gate for code changes.

## Tab Management Rules
1. **Reuse Existing Tabs**: Before calling `open_browser_url`, always check the current browser state. If a tab with the same domain or relevant URL is already open, reuse it instead of opening a new one.
2. **Minimize Background Tabs**: Do not leave unnecessary tabs open. If a task requires visiting multiple pages, close the previous ones unless comparison is explicitly requested.
3. **Limit Total Tabs**: Try to keep the total number of open tabs to a minimum (typically 1-2) to avoid slowing down the user's system.

## Performance Optimization
- Avoid frequent browser restarts or subagent calls if the same information can be retrieved via terminal tools (like `curl` or `grep`).
- Use `browser_subagent` only when visual verification or JavaScript execution is strictly necessary.

## Mandatory Verification Rule
**ALWAYS check the browser console for errors after writing code and before marking a task as complete.**

1. After implementing code changes that affect the frontend, navigate to the relevant page(s).
2. Use `capture_browser_console_logs` to inspect for errors, warnings, or failed network requests.
3. Fix any errors discovered during this verification before reporting success to the user.
4. If errors persist that are unrelated to your changes, document them clearly but prioritize fixing regressions introduced by your work.
