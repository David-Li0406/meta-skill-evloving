---
name: enhance-frontend
description: Enhance frontend to pixel-perfect standards with mobile responsiveness and industry-leading design quality
license: MIT
compatibility:
  - runtime:any
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
metadata:
  author: thoreinstein
  version: 1.0.0
---

# Enhance Frontend

Elevate frontend quality to pixel-perfect, mobile-responsive, accessible standards.

## When to Use This Skill

- When a UI needs visual polish and refinement
- When implementing or auditing a design system
- When improving mobile responsiveness
- When fixing accessibility issues
- When standardizing component styling

## Enhancement Areas

### 1. Pixel-Perfect Alignment

- **Grid System:** 8px base grid for all spacing and sizing
- **Spacing Scale:** Consistent spacing tokens (4, 8, 12, 16, 24, 32, 48, 64px)
- **Alignment:** Elements aligned to grid, consistent margins/padding
- **Sizing:** Components sized in grid increments

### 2. Color System

- **Palette:** Primary, secondary, neutral, semantic colors defined
- **Contrast:** WCAG AA minimum (4.5:1 for text, 3:1 for large text)
- **Semantic Colors:** Success, warning, error, info with consistent meaning
- **Dark Mode:** Consider light/dark theme support if applicable

### 3. Typography

- **Base Size:** 16px minimum for body text
- **Font Families:** 2-3 max (headings, body, mono)
- **Line Height:** 1.5-1.7 for body text, tighter for headings
- **Weight Hierarchy:** Clear distinction (400 regular, 500 medium, 600 semi, 700 bold)
- **Scale:** Consistent type scale (e.g., 12, 14, 16, 18, 20, 24, 30, 36, 48px)

### 4. Component Standards

- **Header/Footer:** Consistent across pages, responsive
- **Buttons:** Clear hierarchy (primary, secondary, tertiary, ghost)
- **Forms:** Labeled inputs, clear validation states, accessible
- **Cards:** Consistent padding, shadows, borders
- **Navigation:** Clear active states, keyboard accessible

### 5. Mobile Responsiveness

- **Breakpoints:** Mobile-first approach
  - Mobile: 320px+
  - Tablet: 768px+
  - Desktop: 1024px+
- **Touch Targets:** Minimum 44x44px for interactive elements
- **Fluid Typography:** Use `clamp()` for responsive sizing
- **Flexible Layouts:** Grid/flexbox that adapts to viewport

### 6. Visual Polish

- **Hover States:** Subtle feedback on interactive elements
- **Focus States:** Visible focus rings for keyboard navigation
- **Loading States:** Skeletons, spinners, progress indicators
- **Error States:** Clear error messaging with recovery actions
- **Transitions:** Smooth, purposeful animations (150-300ms)

### 7. Performance & Accessibility

- **Images:** WebP format, responsive sizes, lazy loading
- **Semantic HTML:** Correct heading hierarchy, landmarks, lists
- **ARIA:** Labels, roles, and states where needed
- **Keyboard Navigation:** All interactive elements reachable
- **Screen Readers:** Content makes sense when read linearly

## Workflow

### Phase 1: Audit

1. Review current frontend state
2. Identify gaps against enhancement areas
3. Prioritize issues by impact

### Phase 2: Design System Foundation

1. Establish or verify spacing scale
2. Define or audit color tokens
3. Set up typography scale
4. Document in CSS custom properties or theme file

### Phase 3: Component Enhancement

1. Update base components to match standards
2. Ensure consistent styling patterns
3. Add missing states (hover, focus, disabled, loading, error)

### Phase 4: Responsive Implementation

1. Audit mobile experience
2. Fix layout issues at each breakpoint
3. Verify touch target sizes
4. Test fluid typography

### Phase 5: Polish

1. Add/refine transitions and animations
2. Verify accessibility compliance
3. Performance audit (images, bundle size)
4. Cross-browser testing

## Constraints

- **Mobile-first** - start with mobile, enhance for larger screens
- **Accessibility required** - WCAG AA is the minimum standard
- **Performance matters** - don't sacrifice load time for polish
- **Consistency over novelty** - match existing patterns before introducing new ones
- **Progressive enhancement** - core functionality works without JavaScript

## Example

### Example: Button Component Enhancement

**Before:**
```css
.button {
  padding: 10px 15px;
  background: blue;
  color: white;
}
```

**After:**
```css
.button {
  /* Spacing on 8px grid */
  padding: 12px 24px;

  /* Color system tokens */
  background: var(--color-primary-600);
  color: var(--color-white);

  /* Typography */
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;

  /* Touch target */
  min-height: 44px;

  /* Visual polish */
  border-radius: 8px;
  transition: background-color 150ms ease;

  /* Focus state */
  &:focus-visible {
    outline: 2px solid var(--color-primary-400);
    outline-offset: 2px;
  }

  /* Hover state */
  &:hover {
    background: var(--color-primary-700);
  }

  /* Disabled state */
  &:disabled {
    background: var(--color-neutral-300);
    cursor: not-allowed;
  }
}
```

---

Begin by auditing the current frontend state against the enhancement areas before making changes.
