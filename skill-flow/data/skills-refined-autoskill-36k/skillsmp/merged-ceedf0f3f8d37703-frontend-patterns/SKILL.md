---
name: frontend-patterns
description: Use this skill when building web frontends, components, or client-side apps, focusing on best practices for component design, state management, performance, and accessibility.
---

# Frontend Development Patterns

This skill provides best practices and patterns for frontend development, supporting framework-specific loading as needed.

## Trigger Conditions

- Create or modify frontend components
- Design UI/UX interactions
- Implement state management
- Optimize performance
- Develop with accessibility in mind

## Framework-Specific Patterns

Load the corresponding framework-specific files based on the project technology stack:

| Technology Stack | Load File   | Framework          |
| ---------------- | ----------- | -------------------|
| Vue              | `vue.md`    | Vue 3, Nuxt 3      |
| React            | `react.md`  | React 18, Next.js  |
| Svelte           | `svelte.md` | Svelte, SvelteKit  |
| Angular          | `angular.md`| Angular 17+        |

**Loading Method**: Detect the technology stack from the `package.json` dependencies.

---

## General Component Patterns

### Component Classification

```
┌─────────────────────────────────────────────────────┐
│                    Component Pyramid                 │
├─────────────────────────────────────────────────────┤
│  Page Components (Pages/Views)                       │
│  ├─ Responsible for routing and layout               │
│  ├─ Composes multiple functional components           │
│  └─ Manages page-level state                          │
├─────────────────────────────────────────────────────┤
│  Functional Components (Features/Containers)         │
│  ├─ Contains business logic                            │
│  ├─ Connects to state management                      │
│  └─ Calls APIs                                       │
├─────────────────────────────────────────────────────┤
│  UI Components (UI/Presentational)                   │
│  ├─ Purely presentational, no business logic         │
│  ├─ Receives data via props                           │
│  └─ Notifies parent components via events             │
├─────────────────────────────────────────────────────┤
│  Base Components (Base/Primitives)                   │
│  ├─ Button, Input, Card, etc.                        │
│  ├─ Highly reusable                                   │
│  └─ Foundation of design systems                      │
└─────────────────────────────────────────────────────┘
```

### Component Design Principles

| Principle         | Description                                   |
| ----------------- | --------------------------------------------- |
| **Single Responsibility** | A component should do one thing only      |
| **Props Down**    | Data flows from parent to child components    |
| **Events Up**     | Events notify parent components from children  |
| **Composition Over Inheritance** | Use slots/children to compose components |
| **Predictable**   | Same props yield the same output              |

### Naming Conventions

```
components/
├── ui/                    # Base components (PascalCase)
│   ├── Button.vue/tsx
│   ├── Input.vue/tsx
│   └── Card.vue/tsx
├── feature/               # Functional components (PascalCase)
│   ├── UserCard.vue/tsx
│   └── OrderList.vue/tsx
└── layout/                # Layout components (PascalCase)
    ├── Header.vue/tsx
    └── Sidebar.vue/tsx
```

---

## State Management Patterns

### State Layers

| Level           | Scope      | Storage Method  | Example            |
| --------------- | ---------- | ---------------- | -------------------|
| **Component State** | Single component | useState/ref  | Form input, UI state |
| **Shared State**    | Multiple components | Context/Store | User info, theme    |
| **Server State**    | From API         | Query Cache   | List data, details  |
| **URL State**       | Route parameters  | Router        | Page number, filters |
| **Persistent State** | Across sessions   | localStorage  | User preferences     |

### State Management Choices

```
Simple shared state → Context/Provide
  ↓ Complexity increases
Medium apps → Pinia/Zustand
  ↓ Complexity increases
Large apps → Redux/Vuex + normalization
```

### Server State Management

```
API requests → Query Library (TanStack Query)
  ├─ Automatic caching
  ├─ Revalidation
  ├─ Optimistic updates
  └─ Error retries
```

---

## Performance Optimization Patterns

### Rendering Optimization

| Technique          | Purpose       | Framework Implementation                  |
| ------------------ | ------------- | ----------------------------------------- |
| **Memoization**    | Avoids recalculation | useMemo/computed                          |
| **Lazy Loading**   | Delays component loading | lazy/defineAsyncComponent                 |
| **Virtual List**   | Renders large lists | react-window/vue-virtual-scroller         |
| **Code Splitting** | Loads code on demand | Dynamic import                             |

### Resource Optimization

```
Image Optimization:
├─ Responsive images (srcset)
├─ Lazy loading (loading="lazy")
├─ Modern formats (WebP/AVIF)
└─ Image CDN

Script Optimization:
├─ Tree Shaking
├─ Bundle analysis
├─ Preload critical resources
└─ Defer non-critical scripts
```

### Performance Metrics

| Metric   | Target   | Description       |
| -------- | -------- | ------------------|
| **LCP**  | < 2.5s  | Largest Contentful Paint |
| **FID**  | < 100ms | First Input Delay  |
| **CLS**  | < 0.1   | Cumulative Layout Shift |
| **TTI**  | < 3.8s  | Time to Interactive |

---

## Accessibility Patterns (a11y)

### Basic Checklist

- [ ] **Semantic HTML** - Use correct elements (button, nav, main...)
- [ ] **Keyboard Accessible** - All interactions should be keyboard operable
- [ ] **Focus Management** - Logical focus order, visible focus
- [ ] **ARIA Labels** - Add appropriate labels for dynamic content
- [ ] **Color Contrast** - Meet WCAG 2.1 AA standards (4.5:1)
- [ ] **Alt Text** - Images should have alt text, icons should have aria-label

### Common ARIA Patterns

```html
<!-- Button -->
<button aria-label="Close menu" aria-expanded="false">
  <Icon name="close" aria-hidden="true" />
</button>

<!-- Form -->
<input
  aria-labelledby="label-id"
  aria-describedby="hint-id error-id"
  aria-invalid="true"
/>

<!-- Dynamic Content -->
<div aria-live="polite" aria-busy="false">Loading complete</div>

<!-- Dialog -->
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Dialog Title</h2>
</div>
```

### Keyboard Interactions

| Element | Key         | Action    |
| ------- | ----------- | --------- |
| Button  | Enter/Space | Activate  |
| Link    | Enter       | Navigate  |
| Menu    | ↑↓          | Move focus|
| Dialog  | Esc         | Close     |
| Tab List| ←→          | Switch tabs|

---

## Form Patterns

### Form Validation

```
Client-side validation:
├─ Real-time validation (onChange)
├─ Submission validation (onSubmit)
├─ Field-level errors
└─ Form-level errors

Validation Libraries:
├─ React: react-hook-form + zod
├─ Vue: vee-validate + zod
└─ General: yup/zod
```

### Form State

```
{
  values: {},        // Field values
  errors: {},        // Validation errors
  touched: {},       // Fields interacted with
  isSubmitting: false,
  isValid: true
}
```

### Error Handling

```html
<!-- Field Error -->
<div class="field">
  <label for="email">Email</label>
  <input id="email" aria-invalid="true" aria-describedby="email-error" />
  <span id="email-error" role="alert" class="error">
    Please enter a valid email address
  </span>
</div>

<!-- Form-level Error -->
<div role="alert" class="form-error">Submission failed: Network error, please try again</div>
```

---

## Animation Patterns

### Animation Types

| Type            | Purpose         | Implementation         |
| --------------- | ----------------| ----------------------- |
| **Enter/Exit**  | Element appears/disappears | CSS Transition       |
| **State Change**| Hover/active    | CSS Transition          |
| **List Animation**| Add/remove/reorder | FLIP animation        |
| **Page Transition**| Route transition | Route animation       |
| **Complex Animation**| Multi-stage animation | Framer Motion/GSAP |

### Animation Principles

1. **Meaningful** - Animations should convey information
2. **Fast** - Duration of 150-300ms
3. **Disableable** - Respect `prefers-reduced-motion`
4. **Non-blocking** - Should not hinder user interaction

### Reducing Animation

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Design Aesthetics (Avoid AI Slop)

### Core Philosophy

Create **unique, memorable** interfaces rather than generic "AI styles".

### ❌ Avoid Common AI Aesthetics

| Category | Avoided Patterns                             |
| -------- | -------------------------------------------- |
| **Fonts** | Common fonts like Inter, Roboto, Arial, system-ui |
| **Colors** | Purple gradients on white backgrounds, blue-purple combinations, rainbow gradients |
| **Layouts** | Centered cards, symmetrical grids, templated hero sections |
| **Animations** | Generic fade-ins, meaningless pulse effects |
| **Elements** | Overuse of glassmorphism cards, generic icons, stock images |

### ✅ Pursue Design Directions

| Dimension | Approach                                                   |
| --------- | ---------------------------------------------------------- |
| **Fonts** | Choose **distinctive** fonts, contrasting title and body fonts |
| **Colors** | Submit a **dominant color**, use sharp accent colors, avoid even distribution |
| **Layouts** | Asymmetrical, overlapping, diagonal flow, breaking grids, negative space or density control |
| **Animations** | Focus on **high-impact moments**: well-choreographed page loads, staggered appearances, scroll-triggered |
| **Backgrounds** | Gradient grids, noise textures, geometric patterns, transparent layers, shadow depth |

### Design Decision Process

```
1. Understand the context
   - What problem does this interface solve?
   - Who is the target user?
   - What is the brand tone?

2. Choose an aesthetic direction (extremes)
   - Minimalism vs Maximalism
   - Retro-futurism vs Natural Organic
   - Luxurious vs Playful
   - Editorial vs Brutalism
   - Decorative vs Industrial Practicality

3. Identify memorable points
   - What will users remember?
   - What makes this design **unique**?

4. Execute thoroughly
   - Bold maximalism requires rich code, animations, effects
   - Refined minimalism requires restraint, precision, and detail polishing
```

### Code Example

```css
/* ❌ Generic AI Style */
.card {
  font-family: Inter, system-ui;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* ✅ Distinctive Design */
.card {
  font-family: "Space Mono", monospace; /* or other unique font */
  background:
    linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.8) 100%),
    url("noise.svg");
  border: 1px solid rgba(255, 255, 255, 0.1);
  clip-path: polygon(
    0 0,
    100% 0,
    100% calc(100% - 20px),
    calc(100% - 20px) 100%,
    0 100%
  );
  /* Diagonal cut design, breaking the convention of rounded cards */
}
```

### Remember

> Claude has the ability to create **extraordinary** works. Don't hold back; showcase truly out-of-the-box, fully invested unique visuals.

---

## Testing Patterns

### Testing Pyramid

```
       △ E2E Testing
      ╱  ╲ Few critical flows
     ╱────╲
    △ Integration Testing
   ╱  ╲ Component interactions, API calls
  ╱────────╲
 △ Unit Testing
╱  ╲ Utility functions, pure components
╱──────────────╲
```

### Component Testing Principles

```
Test user behavior, not implementation details:
├─ ✅ Show text after clicking a button
├─ ❌ Check state variable values
├─ ✅ Submit form after entering text
└─ ❌ Check internal method calls
```

### Testing Libraries

| Framework | Unit/Integration | E2E                |
| --------- | ---------------- | ------------------ |
| React     | Testing Library  | Playwright/Cypress  |
| Vue       | Testing Library  | Playwright/Cypress  |
| General    | Vitest           | Playwright          |

---

## Framework-Specific Content

For detailed framework-specific implementations, please refer to:

- **Vue**: [vue.md](./vue.md) - Vue 3 + Composition API
- **React**: [react.md](./react.md) - React 18 + Hooks
- **Svelte**: [svelte.md](./svelte.md) - Svelte/SvelteKit
- **Angular**: [angular.md](./angular.md) - Angular 17+

---

## Maintenance

- Sources: MDN, WCAG 2.1, web.dev, official documentation of various frameworks
- Last updated: 2025-01-22
- Pattern: General checklist + framework-specific loading