---
name: responsive-design
description: Mobile-first responsive design specialist for SARAISE React/TypeScript/Tailwind applications. Provides guidance on breakpoints, fluid typography, flexible layouts, touch targets, and progressive enhancement. Use when creating responsive layouts, optimizing for mobile, or ensuring cross-device compatibility.
status: ✅ Working
last-validated: 2025-01-02
---

# Responsive Design Principles

**Status:** ✅
**Last Validated:** 2025-01-02

## Purpose

Invoked when creating responsive layouts or optimizing SARAISE UI for mobile/tablet devices. Provides mobile-first design principles aligned with Tailwind CSS breakpoints and SARAISE design system.

## Mobile-First Approach

- Design for mobile first, then scale up
- Progressive enhancement over graceful degradation
- Touch targets minimum 44x44px
- Avoid hover-only interactions
- Test on real devices

## Breakpoints (Tailwind CSS)

- sm: 640px (mobile landscape) - `@media (min-width: 640px)`
- md: 768px (tablet portrait) - `@media (min-width: 768px)`
- lg: 1024px (tablet landscape / small desktop) - `@media (min-width: 1024px)`
- xl: 1280px (desktop) - `@media (min-width: 1280px)`
- 2xl: 1536px (large desktop) - `@media (min-width: 1536px)`

## Fluid Typography

- Use rem for font sizes
- Base size: 16px
- Scale: 1.125 (major second) or 1.2 (minor third)
- Use clamp() for fluid scaling
- Line length: 45-75 characters optimal

## Flexible Layouts (Tailwind)

- Use `grid` classes for page layouts (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`)
- Use `flex` classes for component layouts (`flex flex-col md:flex-row`)
- Avoid fixed widths, use `w-full` with `max-w-*`
- Content containers: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- Use `gap-*` instead of margins in flex/grid (`gap-4`, `gap-6`)

## Images & Media

- Use responsive images (srcset, sizes)
- Use object-fit for aspect ratios
- Lazy load below-the-fold images
- Optimize for different densities (@1x, @2x)
- Use CSS for simple graphics

## Common Patterns

- Hamburger menu for mobile navigation
- Card layouts that stack on mobile
- Side-by-side columns that stack
- Hidden elements on mobile (use wisely)
- Bottom navigation on mobile apps

## Testing

- Test on actual devices
- Use browser DevTools device mode
- Test at various viewport sizes
- Test with slow connections
- Test landscape and portrait orientations
