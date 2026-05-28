---
name: ui-skills
description: Use this skill when building or reviewing UI components to ensure adherence to best practices and guidelines for accessibility, performance, and design.
---

# UI Skills

Opinionated constraints for building better interfaces with agents.

## How to use

- `/ui-skills`  
  Apply these constraints to any UI work in this conversation.

- `/ui-skills <file>`  
  Review the file against all constraints below and output:
  - violations (quote the exact line/snippet)
  - why it matters (1 short sentence)
  - a concrete fix (code-level suggestion)

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
- NEVER modify `letter-spacing` (`tracking-*`) unless explicitly requested

## Layout

- MUST use a fixed `z-index` scale (no arbitrary `z-*`)
- SHOULD use `size-*` for square elements instead of `w-*` + `h-*`

## Performance

- MUST test across devices and browsers
- NEVER animate large `blur()` or `backdrop-filter` surfaces
- NEVER apply `will-change` outside an active animation
- NEVER use `useEffect` for anything that can be expressed as render logic
- SHOULD batch DOM reads and writes to prevent layout thrashing
- SHOULD virtualize large lists
- SHOULD preload critical resources
- MUST prevent layout shift during loading
- SHOULD preconnect to external origins
- SHOULD preload fonts and use font subsetting
- SHOULD move expensive work to Web Workers

## Design

- NEVER use gradients unless explicitly requested
- NEVER use purple or multicolor gradients
- NEVER use glow effects as primary affordances
- SHOULD use Tailwind CSS default shadow scale unless explicitly requested
- MUST give empty states one clear next action
- SHOULD limit accent color usage to one per view
- SHOULD use existing theme or Tailwind CSS color tokens before introducing new ones
- SHOULD prioritize optical alignment over mathematical alignment
- MUST be responsive across all device sizes
- MUST respect safe area insets on mobile devices
- SHOULD balance contrast in text/icon combinations

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