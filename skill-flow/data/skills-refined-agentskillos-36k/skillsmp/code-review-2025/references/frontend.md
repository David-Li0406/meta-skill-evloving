# Frontend Review Standards (2025)
## 1. Core Web Vitals: The "Big Three"
By Dec 2025, Google's "Page Experience" signals prioritize session-wide stability and responsiveness.
| Metric | "Good" | 2025 Optimization Strategy |
| :--- | :--- | :--- |
| **INP** (Interaction to Next Paint) | **≤ 200ms** | Use `scheduler.yield()` to break long JS tasks; avoid heavy main-thread work. |
| **LCP** (Largest Contentful Paint) | **≤ 2.5s** | Prioritize "Priority Hints" `fetchpriority="high"`) for hero assets. |
| **CLS** (Cumulative Layout Shift) | **≤ 0.1** | Use CSS `aspect-ratio` and reserved "skeleton" slots for streaming RSC content. |
### Performance Checklist
- [ ] **Interaction Responsiveness:** Are heavy event handlers (e.g., search filtering) debounced or moved to Web Workers?
- [ ] **Priority Loading:** Are non-critical scripts (Analytics, Chat) using `next/script` with `strategy="lazyOnload"`?
- [ ] **Streaming & Suspense:** Does the app use `<Suspense>` boundaries to prevent "all-or-nothing" page loads?
- [ ] **Image Modernization:** Are all images served in AVIF/WebP with `srcset` for high-DPI displays?
## 2. Accessibility: WCAG 3.0 Silver Readiness
While WCAG 2.2 remains the legal baseline, 2025 enterprise standards target the **WCAG 3.0 Bronze/Silver** outcome model.
### The APCA Contrast Model
- [ ] **Perceptual Contrast:** Does text meet APCA targets? (Lc 60+ for body text; Lc 45+ for large headings). *Discard 4.5:1 ratio for APCA.*
- [ ] **Visual Indicators:** Are focus states high-contrast and never suppressed?
- [ ] **Target Size:** Are all interactive elements (buttons, links) at least **24x24 CSS pixels** to satisfy WCAG 2.2?
### Functional Outcomes
- [ ] **Keyboard Nav:** Can the entire application be navigated without a mouse, including modals and nested menus?
- [ ] **Screen Reader Flow:** Are `aria-live` regions used for dynamic content (e.g., "Items added to cart")?
- [ ] **Dragging Alternatives:** Do drag-and-drop features have "Click-to-Move" or keyboard-based reordering?
## 3. Architecture: RSC & Next.js Patterns
The "Vibe Coding" era favors frameworks that handle the server-client boundary automatically (Next.js 15/16+, Remix 2.10+).
### Data Flow Patterns
- [ ] **Parallel Fetching:** Are multiple data requirements initiated simultaneously in the layout/page rather than awaited sequentially?
- [ ] **Partial Prerendering (PPR):** Is PPR enabled for dynamic routes to serve the static shell immediately?
- [ ] **Server Actions:** Are forms using native Server Actions with `useActionState` (React 19) for pending and error states?
- [ ] **Hydration Efficiency:** Is `'use client'` used at the "leaves" of the tree? (Avoid wrapping entire layouts in client context).
### "Vibe Coding" Sanitization
- [ ] **Tailwind Optimization:** Check for redundant class duplication (e.g., five `flex` declarations on nested children).
- [ ] **Semantic HTML:** Ensure AI hasn't used `<div>` with an `onClick` instead of a semantic `<button>`.
- [ ] **Component Consolidation:** Flag "Component Bloat" where AI has generated 10 slightly different buttons instead of one reusable primitive.
## 4. Testing & Reliability
- [ ] **Interaction Testing:** Use Playwright or Vitest to verify INP-sensitive user paths.
- [ ] **Visual Regression:** Are UI changes tested for layout shifts across mobile/tablet/desktop breakpoints?
- [ ] **Accessibility Audit:** Automate with `axe-core` in CI, but perform manual screen reader spot-checks on new patterns.
