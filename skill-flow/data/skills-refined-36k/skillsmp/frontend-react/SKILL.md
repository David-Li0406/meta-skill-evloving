---
name: frontend-react
description: React and Next.js frontend development skill combining project-specific patterns (SSR/CSR, theme, API) with Vercel's performance optimization best practices. Use for all React/Next.js work.
license: MIT
metadata:
  author: finance-report + vercel
  version: "2.0.0"
---

# Frontend React Development

> **Merged Skill**: Combines project-specific frontend patterns with Vercel's React best practices.

## Part 1: Project Patterns

### SSR vs CSR Handling

#### Mounted State Pattern

Handle hydration mismatches when using client-side state (localStorage, window):

```tsx
const [mounted, setMounted] = useState(false);
useEffect(() => setMounted(true), []);

if (!mounted) return null; // or loading skeleton
```

**Applied In**: `ThemeToggle.tsx`, `Sidebar.tsx`

### Theme System

Use CSS variables to avoid FOUC and support system preferences:

```css
/* Good */
bg-[var(--background-card)]
text-[var(--muted-foreground)]

/* Avoid */
bg-white
text-gray-500
```

**Structure**:
- `app/globals.css`: Defines `:root` and `.dark` variables
- `lib/theme.ts`: Theme state management
- `ThemeToggle.tsx`: Theme switcher component

### API Integration

All API calls must use `apiFetch` or `apiUpload` from `lib/api.ts`:

- **NO Direct `fetch()`**: Never use native fetch for `/api/*` calls
- **X-User-Id**: Auto-injected from local storage
- **Absolute URLs**: Use `APP_URL` constant

### Security

- **AuthGuard**: Protects all `(main)` routes
- **Public Routes**: Only `/login` and `/ping-pong` exempt
- **Injection Protection**: Via `apiFetch` wrapper

### Shared Types

Define in `src/lib/types.ts`:
- `Account`, `JournalEntry`, `JournalLine`
- `BankStatement`, `BankStatementTransaction`
- `ReportLine`, `BalanceSheetResponse`, `IncomeStatementResponse`

---

## Part 2: Vercel React Best Practices

Comprehensive performance optimization guide for React and Next.js applications.

### Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

### Quick Reference

#### 1. Eliminating Waterfalls (CRITICAL)

- `async-defer-await` - Move await into branches where actually used
- `async-parallel` - Use Promise.all() for independent operations
- `async-dependencies` - Use better-all for partial dependencies
- `async-api-routes` - Start promises early, await late in API routes
- `async-suspense-boundaries` - Use Suspense to stream content

#### 2. Bundle Size Optimization (CRITICAL)

- `bundle-barrel-imports` - Import directly, avoid barrel files
- `bundle-dynamic-imports` - Use next/dynamic for heavy components
- `bundle-defer-third-party` - Load analytics/logging after hydration
- `bundle-conditional` - Load modules only when feature is activated
- `bundle-preload` - Preload on hover/focus for perceived speed

#### 3. Server-Side Performance (HIGH)

- `server-cache-react` - Use React.cache() for per-request deduplication
- `server-cache-lru` - Use LRU cache for cross-request caching
- `server-serialization` - Minimize data passed to client components
- `server-parallel-fetching` - Restructure components to parallelize fetches
- `server-after-nonblocking` - Use after() for non-blocking operations

#### 4. Client-Side Data Fetching (MEDIUM-HIGH)

- `client-swr-dedup` - Use SWR for automatic request deduplication
- `client-event-listeners` - Deduplicate global event listeners

#### 5. Re-render Optimization (MEDIUM)

- `rerender-defer-reads` - Don't subscribe to state only used in callbacks
- `rerender-memo` - Extract expensive work into memoized components
- `rerender-dependencies` - Use primitive dependencies in effects
- `rerender-derived-state` - Subscribe to derived booleans, not raw values
- `rerender-functional-setstate` - Use functional setState for stable callbacks
- `rerender-lazy-state-init` - Pass function to useState for expensive values
- `rerender-transitions` - Use startTransition for non-urgent updates

#### 6. Rendering Performance (MEDIUM)

- `rendering-animate-svg-wrapper` - Animate div wrapper, not SVG element
- `rendering-content-visibility` - Use content-visibility for long lists
- `rendering-hoist-jsx` - Extract static JSX outside components
- `rendering-svg-precision` - Reduce SVG coordinate precision
- `rendering-hydration-no-flicker` - Use inline script for client-only data
- `rendering-activity` - Use Activity component for show/hide
- `rendering-conditional-render` - Use ternary, not && for conditionals

#### 7. JavaScript Performance (LOW-MEDIUM)

- `js-batch-dom-css` - Group CSS changes via classes or cssText
- `js-index-maps` - Build Map for repeated lookups
- `js-cache-property-access` - Cache object properties in loops
- `js-cache-function-results` - Cache function results in module-level Map
- `js-cache-storage` - Cache localStorage/sessionStorage reads
- `js-combine-iterations` - Combine multiple filter/map into one loop
- `js-length-check-first` - Check array length before expensive comparison
- `js-early-exit` - Return early from functions
- `js-hoist-regexp` - Hoist RegExp creation outside loops
- `js-min-max-loop` - Use loop for min/max instead of sort
- `js-set-map-lookups` - Use Set/Map for O(1) lookups
- `js-tosorted-immutable` - Use toSorted() for immutability

#### 8. Advanced Patterns (LOW)

- `advanced-event-handler-refs` - Store event handlers in refs
- `advanced-use-latest` - useLatest for stable callback refs

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

For the complete guide with all rules expanded: `AGENTS.md`
