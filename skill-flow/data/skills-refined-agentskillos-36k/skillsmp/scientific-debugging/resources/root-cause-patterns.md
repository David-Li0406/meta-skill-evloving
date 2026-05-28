# Root Cause Patterns

> Common reasons for bugs in this project.

## 1. DOM & Events
- **Non-interactive Elements**: Adding `onClick` to a `div` without `role="button"` or `tabindex`.
- **Focus Traps**: Modals not trapping focus or not restoring it.
- **Overlay Blocking**: Higher `z-index` transparent layers blocking clicks.

## 2. React & State
- **Stale Closures**: `useEffect` or `useCallback` missing dependencies.
- **Race Conditions**: Two async operations updating state out of order.
- **Zustand Destructuring**: Causing re-renders on unrelated state changes.

## 3. Network
- **N+1 Requests**: Fetching list items individually instead of batching.
- **Optimistic UI failures**: Sync failure rolling back state abruptly.
