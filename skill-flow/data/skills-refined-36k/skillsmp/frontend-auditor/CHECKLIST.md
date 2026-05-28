# Frontend Audit Checklist

Complete checklist for auditing frontend code. Work through each section systematically.

---

## Security

### Cross-Site Scripting (XSS)

- [ ] **dangerouslySetInnerHTML** - All uses sanitized with DOMPurify or similar
- [ ] **innerHTML usage** - No direct DOM manipulation with user content
- [ ] **Markdown rendering** - Sanitized before display
- [ ] **URL injection** - `href`, `src` attributes validated
- [ ] **Template literals** - No user input in template strings for DOM
- [ ] **SVG injection** - SVGs sanitized before inline rendering
- [ ] **iframe src** - No user-controlled iframe sources

### Authentication & Session

- [ ] **Token storage** - Tokens NOT in localStorage (prefer httpOnly cookies)
- [ ] **CSRF protection** - State-changing requests include CSRF tokens
- [ ] **Session handling** - Proper logout, session expiry handling
- [ ] **Auth state sync** - Tabs/windows sync auth state correctly
- [ ] **Protected routes** - Auth checks on client AND server
- [ ] **Redirect after login** - Return URL validated (no open redirect)

### Secrets & Data Exposure

- [ ] **Client bundle secrets** - No API keys, secrets in client code
- [ ] **Environment variables** - Only `NEXT_PUBLIC_`/`VITE_` vars are public
- [ ] **Source maps** - Disabled in production
- [ ] **Console logs** - No sensitive data logged in production
- [ ] **Error messages** - No stack traces or internal details exposed
- [ ] **Network tab** - No sensitive data in request/response visible to user

### Dependencies & Build

- [ ] **Vulnerable packages** - No known CVEs in dependencies
- [ ] **Outdated dependencies** - UI libs reasonably up to date
- [ ] **CDN scripts** - Third-party scripts use SRI hashes
- [ ] **Build output** - No debug code in production builds

### Deep Links & URLs

- [ ] **Open redirects** - External redirect URLs validated
- [ ] **Deep link params** - URL parameters sanitized before use
- [ ] **Query string injection** - No SQL/code injection via URL params
- [ ] **Path traversal** - File paths from URLs validated

---

## Correctness & UX

### Loading States

- [ ] **Loading indicators** - All async operations show loading state
- [ ] **Skeleton screens** - Appropriate placeholders during load
- [ ] **Progressive loading** - Content appears as it loads
- [ ] **Timeout handling** - Long requests show appropriate feedback

### Error States

- [ ] **Error boundaries** - React error boundaries catch crashes
- [ ] **API error handling** - All fetch calls handle errors
- [ ] **User-friendly messages** - Errors are actionable, not technical
- [ ] **Retry mechanisms** - Failed requests can be retried
- [ ] **Offline handling** - Graceful degradation when offline

### Empty States

- [ ] **Empty lists** - Appropriate message when no data
- [ ] **Zero results** - Search/filter shows "no results" state
- [ ] **First-time user** - Onboarding for empty initial state

### Form Handling

- [ ] **Validation** - Client-side validation matches server
- [ ] **Error display** - Field-level errors shown correctly
- [ ] **Disabled states** - Submit disabled during submission
- [ ] **Double-submit prevention** - Cannot submit same form twice
- [ ] **Form reset** - Forms reset correctly after submit/cancel
- [ ] **Autofill** - Browser autofill works correctly
- [ ] **Required fields** - Clearly marked, validated

### Edge Cases

- [ ] **Boundary values** - Min/max values handled correctly
- [ ] **Special characters** - Unicode, emojis, RTL text handled
- [ ] **Long content** - Truncation, overflow handled gracefully
- [ ] **Rapid interactions** - Debouncing, throttling where needed

### Data Formatting

- [ ] **Timezones** - Dates displayed in user's timezone
- [ ] **Date formats** - Locale-appropriate date formatting
- [ ] **Currency** - Correct currency symbols, decimal places
- [ ] **Number formatting** - Locale-appropriate thousands separators
- [ ] **Rounding** - Financial calculations use proper rounding
- [ ] **i18n** - All user-visible text translatable

### State Consistency

- [ ] **Stale data** - Cache invalidation on mutations
- [ ] **Race conditions** - Concurrent requests handled correctly
- [ ] **Aborted requests** - Cancelled requests don't update state
- [ ] **Optimistic updates** - Rollback on failure implemented
- [ ] **Cross-tab sync** - State syncs across browser tabs

---

## Performance

### Bundle Size

- [ ] **Code splitting** - Routes lazy-loaded
- [ ] **Dynamic imports** - Heavy libs loaded on demand
- [ ] **Tree shaking** - Unused code eliminated
- [ ] **Bundle analysis** - No unexpected large dependencies
- [ ] **Duplicate dependencies** - No duplicate package versions

### Rendering Performance

- [ ] **Unnecessary re-renders** - Components memoized appropriately
- [ ] **useMemo/useCallback** - Expensive computations memoized
- [ ] **React.memo** - Pure components wrapped
- [ ] **Key props** - List items have stable keys
- [ ] **Virtual scrolling** - Large lists virtualized
- [ ] **Debouncing** - Frequent events debounced (scroll, resize, input)

### Assets

- [ ] **Image optimization** - Images properly sized, compressed
- [ ] **Lazy loading images** - Below-fold images lazy-loaded
- [ ] **Modern formats** - WebP/AVIF with fallbacks
- [ ] **Responsive images** - srcset for different screen sizes
- [ ] **Font loading** - Font-display: swap, preload critical fonts
- [ ] **Icon sprites** - SVG sprites or icon fonts for many icons

### Network

- [ ] **Overfetching** - Only requested data fetched
- [ ] **Duplicate requests** - Same data not fetched multiple times
- [ ] **Request batching** - Multiple requests batched where possible
- [ ] **Pagination** - Large datasets paginated
- [ ] **Caching** - API responses cached appropriately
- [ ] **Prefetching** - Likely-needed data prefetched
- [ ] **Request cancellation** - Stale requests cancelled

### Core Web Vitals

- [ ] **LCP (Largest Contentful Paint)** - < 2.5s
- [ ] **FID (First Input Delay)** - < 100ms
- [ ] **CLS (Cumulative Layout Shift)** - < 0.1
- [ ] **TTFB (Time to First Byte)** - < 800ms

---

## Accessibility (a11y)

### Keyboard Navigation

- [ ] **Tab order** - Logical tab sequence
- [ ] **Focus visible** - Focus indicator always visible
- [ ] **Focus trap** - Modals trap focus correctly
- [ ] **Skip links** - Skip to main content available
- [ ] **Keyboard shortcuts** - Documented, not conflicting
- [ ] **Escape key** - Closes modals, dropdowns

### Screen Readers

- [ ] **Semantic HTML** - Proper heading hierarchy, landmarks
- [ ] **Alt text** - All images have meaningful alt text
- [ ] **ARIA labels** - Interactive elements labeled
- [ ] **ARIA roles** - Custom components have correct roles
- [ ] **Live regions** - Dynamic content announced
- [ ] **Error announcements** - Form errors announced to SR

### Visual

- [ ] **Color contrast** - WCAG AA minimum (4.5:1 text, 3:1 UI)
- [ ] **Color not sole indicator** - Information not conveyed by color alone
- [ ] **Text sizing** - Text scales with browser zoom
- [ ] **Touch targets** - Minimum 44x44px on mobile
- [ ] **Motion** - Respects prefers-reduced-motion

### Forms

- [ ] **Labels** - All inputs have associated labels
- [ ] **Required indication** - Required fields marked (not just *)
- [ ] **Error identification** - Errors identify the field
- [ ] **Instructions** - Complex inputs have help text

---

## Maintainability

### Component Design

- [ ] **Single responsibility** - Components do one thing
- [ ] **Props interface** - Clear, documented prop types
- [ ] **Composition** - Prefer composition over inheritance
- [ ] **Reusability** - Shared components extracted
- [ ] **Naming** - Clear, consistent naming conventions

### Code Quality

- [ ] **TypeScript** - Strict mode, no `any` types
- [ ] **ESLint** - No warnings or errors
- [ ] **Prettier** - Consistent formatting
- [ ] **No dead code** - Unused components/imports removed
- [ ] **No TODOs in prod** - TODOs tracked in issues

### Testing

- [ ] **Unit tests** - Components have unit tests
- [ ] **Integration tests** - Key flows tested
- [ ] **E2E tests** - Critical paths covered
- [ ] **Visual regression** - UI changes caught
- [ ] **Accessibility tests** - Automated a11y checks

### Styling

- [ ] **Consistency** - Design system followed
- [ ] **No inline styles** - Styles in proper system
- [ ] **Responsive** - All breakpoints handled
- [ ] **Dark mode** - If supported, fully implemented
- [ ] **CSS specificity** - No !important abuse

---

## Quick Reference: Common Issues by Framework

### React
- Missing keys in lists
- State updates in useEffect without deps
- Memory leaks (subscriptions not cleaned up)
- Prop drilling instead of context

### Next.js
- Client/server component confusion (App Router)
- Hydration mismatches
- Missing loading.tsx/error.tsx
- Not using Image component

### Vue
- Mutating props directly
- Missing v-bind:key
- Not using computed for derived state
- Watchers without cleanup

### State Management
- Storing derived state
- Not normalizing data
- Missing loading/error states
- Global state for local data

---

## Severity Classification Guide

| Severity | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Security vulnerability, data exposure | XSS, token in localStorage, secrets in bundle |
| **HIGH** | Major UX regression, auth issue | Broken auth flow, data loss, crash |
| **MEDIUM** | Performance issue, a11y failure | Missing loading state, no keyboard nav |
| **LOW** | Minor issue, code smell | Missing memoization, inconsistent styling |
| **INFO** | Suggestion, observation | Could be more efficient, pattern improvement |
