---
name: ui-skills
description: Opinionated constraints for building better interfaces with agents. Combines UI Skills and Vercel Web Interface Guidelines. Use when building UI components, reviewing frontend code, or implementing interactions.
---

# UI Skills

Opinionated constraints for building better interfaces with agents.

---

## Stack

- MUST use Tailwind CSS defaults (spacing, radius, shadows) before custom values
- MUST use `motion/react` (formerly `framer-motion`) when JavaScript animation is required
- SHOULD use `tw-animate-css` for entrance and micro-animations in Tailwind CSS
- MUST use `cn` utility (`clsx` + `tailwind-merge`) for class logic

## Components

- MUST use accessible component primitives for anything with keyboard or focus behavior (`Base UI`, `React Aria`, `Radix`)
- MUST use the project's existing component primitives first
- NEVER mix primitive systems within the same interaction surface
- SHOULD prefer [`Base UI`](https://base-ui.com/react/components) for new primitives if compatible with the stack
- MUST add an `aria-label` to icon-only buttons
- NEVER rebuild keyboard or focus behavior by hand unless explicitly requested

## Interaction

- MUST use an `AlertDialog` for destructive or irreversible actions
- SHOULD use structural skeletons for loading states
- NEVER use `h-screen`, use `h-dvh`
- MUST respect `safe-area-inset` for fixed elements
- MUST show errors next to where the action happens
- NEVER block paste in `input` or `textarea` elements

## Animation

- NEVER add animation unless it is explicitly requested
- MUST animate only compositor props (`transform`, `opacity`)
- NEVER animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`)
- SHOULD avoid animating paint properties (`background`, `color`) except for small, local UI (text, icons)
- SHOULD use `ease-out` on entrance
- NEVER exceed `200ms` for interaction feedback
- MUST pause looping animations when off-screen
- MUST respect `prefers-reduced-motion`
- NEVER introduce custom easing curves unless explicitly requested
- SHOULD avoid animating large images or full-screen surfaces

## Typography

- MUST use `text-balance` for headings and `text-pretty` for body/paragraphs
- MUST use `tabular-nums` for data
- SHOULD use `truncate` or `line-clamp` for dense UI
- NEVER modify `letter-spacing` (`tracking-`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-x`)
- SHOULD use `size-x` for square elements instead of `w-x` + `h-x`

## Performance

- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones

---

# Vercel Web Interface Guidelines

Standards for building excellent web interfaces.

---

## Interactions

- All flows MUST be keyboard-operable following WAI-ARIA standards
- MUST manage focus properly (return focus after dialogs, etc.)
- MUST match visual and hit targets (clickable area matches visual element)
- MUST prevent double-tap zoom on mobile (use `touch-action: manipulation`)
- NEVER disable paste in `<input>` or `<textarea>`
- SHOULD implement optimistic updates for better perceived performance
- MUST confirm destructive actions with dialogs
- SHOULD use tooltips for icon-only actions
- MUST respect scroll behavior preferences
- SHOULD support deep linking for important states
- MUST make drag interactions accessible with keyboard alternatives

## Animations

- MUST honor `prefers-reduced-motion` user preference
- SHOULD prefer CSS animations over JavaScript when possible
- MUST ensure animations are interruptible (user can cancel mid-animation)
- SHOULD only animate when clarifying cause-and-effect relationships
- MUST use GPU-accelerated properties (`transform`, `opacity`)
- NEVER use `transition: all` - be explicit about animated properties
- MUST handle SVG transform cross-browser compatibility

## Layout

- SHOULD prioritize optical alignment over mathematical alignment
- MUST be responsive across all device sizes
- MUST respect safe area insets on mobile devices
- SHOULD let browsers handle sizing through flexbox/grid rather than JavaScript
- MUST manage scrollbar appearance consistently
- SHOULD balance contrast in text/icon combinations

## Content

- MUST mirror final content structure in skeleton screens
- MUST design all UI states: empty, sparse, dense, error, loading
- MUST use semantic HTML elements
- MUST ensure accessible names for all interactive elements
- SHOULD use proper typographic details (curly quotes, no widows/orphans)
- MUST use `tabular-nums` for numeric data display
- SHOULD provide redundant status cues (not just color)
- MUST provide labels for icons
- MUST build proper heading hierarchies (h1 > h2 > h3)
- MUST handle user-generated content resiliently
- SHOULD use locale-aware formatting for dates/numbers

## Forms

- MUST enable Enter key to submit forms
- MUST provide labels for all form fields
- MUST allow clicking labels to activate inputs
- SHOULD allow incomplete form submission to surface validation errors
- NEVER block typing even for number-only fields
- MUST show errors next to related fields
- SHOULD use proper `autocomplete` attributes
- SHOULD be selective about spellcheck
- MUST use correct `input type` and `inputmode`
- SHOULD warn about unsaved changes before navigation
- MUST ensure password manager compatibility

## Performance

- MUST test across devices and browsers
- SHOULD batch DOM reads and writes to prevent layout thrashing
- SHOULD virtualize large lists
- SHOULD preload critical resources
- MUST prevent layout shift during loading
- SHOULD preconnect to external origins
- SHOULD preload fonts and use font subsetting
- SHOULD move expensive work to Web Workers

## Design

- SHOULD use layered shadows for depth
- SHOULD combine borders and shadows appropriately
- MUST calculate nested border radii correctly (inner = outer - padding)
- SHOULD maintain hue consistency across color palette
- SHOULD use colorblind-friendly palettes
- SHOULD prefer APCA over WCAG 2 for contrast calculations
- MUST ensure interactive states have higher contrast than rest states
- SHOULD set `theme-color` meta tag for browser chrome
- SHOULD declare `color-scheme` for system integration
- MUST handle text anti-aliasing during transforms
- SHOULD mitigate gradient banding

---

## Vercel Copywriting Standards

- Use active voice, not passive
- Use Title Case for headings (Chicago style)
- Be concise - remove unnecessary words
- Prefer ampersand (&) over "and" in UI
- Use action-oriented language
- Use consistent noun terminology
- Write in second person (you/your)
- Use consistent placeholders
- Use numerals for numbers
- Format currency consistently
- Use non-breaking spaces between numbers and units
- Frame messages positively
- Error messages should guide toward recovery
- Labels should be specific and clear

---

## Quick Reference

### MUST Rules (Non-negotiable)
1. Keyboard accessibility
2. `prefers-reduced-motion` respect
3. Semantic HTML
4. Accessible names for interactions
5. Form labels
6. Enter key form submission
7. No paste blocking
8. Error placement near action
9. `h-dvh` not `h-screen`
10. `aria-label` for icon-only buttons

### NEVER Rules
1. NEVER add animation without explicit request
2. NEVER animate layout properties
3. NEVER use `useEffect` for render logic
4. NEVER use gradients without explicit request
5. NEVER use `transition: all`
6. NEVER block paste
7. NEVER use arbitrary z-index values
8. NEVER modify letter-spacing without explicit request

### SHOULD Preferences
1. Optimistic updates
2. Skeleton loading states
3. Tailwind defaults before custom values
4. `text-balance` / `text-pretty`
5. CSS animations over JS
6. Layered shadows for depth
7. One accent color per view
