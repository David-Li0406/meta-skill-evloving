---
name: frontend
description: Ensures consistency in vanilla TypeScript development for the apiary frontend, maintaining architectural integrity and code quality.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  project: apiary
---

# Frontend Engineering Skill for apiary

## Purpose
This Skill is activated when writing, modifying, or reviewing frontend code in the apiary project. It ensures consistency in vanilla TypeScript development without frameworks, maintaining the project's architectural integrity and code quality standards.

## Assumptions
- Environment: Browser-based desktop application using Wails for Go backend integration.
- Tooling: Vite for bundling, Bun for package management, TypeScript with strict settings, ESLint for linting.
- Dependencies: GoldenLayout for tabbed interface, CodeMirror for editors, custom utils for reactivity and DOM manipulation.
- No external UI frameworks; all components built from scratch using vanilla TypeScript.

## Explicit Rules

### Component Organization
- Request kinds are implemented as factory functions in `frontend/src/Request*.ts` (e.g., `RequestHTTP.ts`).
- Each factory function takes `(el: HTMLElement, show_request: Signal<boolean>, on: {update: (patch: Partial<Request>) => Promise<void>, send: () => Promise<void>})` and returns `{loaded(r: get_request): void, push_history_entry(he: HistoryEntry): void, unmount(): void}`.
- Components are registered in `App.ts` `panelkaFactory` switch statement.
- UI components are in `frontend/src/components/` as `N*` functions returning DOM elements (e.g., `NButton`, `NInput`).

### TypeScript Usage Patterns
- Use strict TypeScript with all strict options enabled.
- Prefer `const` over `let`; avoid `var`.
- Use double quotes for strings.
- Omit semicolons.
- Prefer functional programming: use `map`, `filter`, `reduce` over loops where natural; loops are acceptable when more readable.
- Define types explicitly; avoid `any`.
- Use interface for object types, type for unions/aliases.

### DOM Access and Lifecycle
- Use `m(tag, props, children)` from `utils.ts` for element creation.
- Set event handlers via `on*` props in `m()` or direct `addEventListener`.
- Manage subscriptions with `signal.sub(generator)` for reactivity.
- Use `replaceChildren()` for efficient DOM updates.
- Implement `unmount()` functions to clean up subscriptions and event listeners.
- Use `setDisplay(el, show)` for conditional visibility without `display: none`.

### State and Data Flow
- Use `signal<T>(value)` from `utils.ts` for reactive state.
- Central store in `store.ts` for app-wide state (requests, layout).
- Data flow: User actions → update signals/store → re-render via subscriptions.
- Optimistic updates in store with rollback on error.
- Use `Promise` for async operations; handle errors via `notification.error`.

### Error Handling
- Errors from backend API calls are handled in store functions with `notification.error`.
- Use try-catch only for synchronous errors; async errors via `.catch()`.
- Display errors via alert (simple notification system).

### Performance and Complexity Boundaries
- Avoid unnecessary re-renders by subscribing only to needed signals.
- Use `replaceChildren` for batch DOM updates.
- Keep components small; break into sub-functions if complex.
- Lazy load editors/components if possible.
- No VDOM; direct DOM manipulation for performance.

## Forbidden Patterns and Behaviors
- No external UI frameworks (React, Vue, etc.).
- No class-based components; all functional.
- No `Array.forEach`; use `map` or loops.
- No `overflow: hidden`.
- No `!important` in styles.
- No disabling linter rules.
- No modifying config files unless explicitly required.
- No auto-formatting tools; respect existing formatting.

## Decision Heuristics
- When adding new state: Use signal if local to component; use store if app-wide.
- When choosing loops vs functional: Use functional for simple transforms; loops for complex logic or when more readable.
- When styling: Use `css()` from `styles.ts` for reusable classes; inline styles for one-off.
- When handling events: Use `on*` in `m()` for simple; `addEventListener` for complex.
- When multiple approaches: Prefer consistency with existing codebase over novelty.

## Expected Output Shape
When generating or modifying frontend code:
- Export default function for request components.
- Use `m()` for DOM construction.
- Implement unmount for cleanup.
- Use signals for reactivity.
- Follow linting rules (double quotes, no semicolons, etc.).
- Ensure `bun run ci` passes (run in frontend/).
