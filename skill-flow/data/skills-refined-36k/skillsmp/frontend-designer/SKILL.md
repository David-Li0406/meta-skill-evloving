---
name: frontend-designer
description: Apply when creating React frontend UI: pages, dashboards, forms, components, layouts, landing pages, modals. Enforces utilitarian design — hard shadows, 2px borders, warm cream/yellow palette, no dark mode. Tech: React, Tailwind, shadcn (customized).
---

Create frontends that feel like dev tools — functional, honest, unapologetically direct. The goal is interfaces that happen to look technical because they prioritize function, not interfaces that look technical for style points.

## Before You Code

Ask clarifying questions. Use AskUserQuestion to understand:

- **Purpose**: What job does this interface do? Who uses it and in what mindset?
- **Key actions**: What are the 2-3 things a user must be able to do?
- **Constraints**: What must not change? What's flexible?

Don't assume. A "simple button" might need to work in a toolbar, a card footer, and a modal. A "dashboard" might mean three widgets or thirty. Get clarity first.

## Guiding Principles

**Honesty over polish**
Raw, functional interfaces. Show structure through borders and hard edges. If something is a box, let it be a box. No visual tricks, no decoration pretending to be function.

**Warmth without softness**
The palette is warm cream for backgrounds, white for elevated elements, yellow accent for primary actions. But warmth doesn't mean rounded or gentle. Sharp corners, solid borders, crisp edges. Welcoming through clarity, not comfort.

**Monospace everywhere**
All text uses monospace. Headings, body, labels, data — all of it. Use Tailwind's `font-mono`. This creates the technical, terminal-inspired character of the system. Never set specific font families like Inter or Roboto.

**Uppercase for control surfaces**
Buttons, labels, badges, headings, navigation items — anything that controls or identifies uses uppercase. Body text and descriptions stay sentence case.

**Borders define everything**
2px solid borders on all containers and interactive elements. No exceptions. Borders are the primary way to show hierarchy and grouping. No shadows, no gradients, no blur.

**The stripe reveals intent**
Hover state is a left-edge stripe that slides in. This is the universal hover affordance across all interactive elements — buttons, menu items, table rows, sidebar links. A thin vertical bar appears on the left edge, confirming "this thing responds to you."

**Status through left stripe**
For semantic states (success, warning, error, info), use a thicker left border in the appropriate color. The pattern is: neutral container, colored left edge. Icons use bracketed ASCII style: `[✓]` `[!]` `[×]` `[i]`

**Selection inverts**
When something is selected, active, or checked, it inverts — dark background, light text. This is the universal "this is on" signal. Buttons, tabs, menu items, calendar dates, toggle states — all use inversion for selection.

**No animation**
State changes are instant. No transitions, no easing, no choreography. When something opens, it's open. When something changes, it's changed. The only exception is the spinner component, which rotates because a static spinner is useless.

**Touch targets at 44px**
All interactive elements use a minimum height of 44px (h-11 in Tailwind). This is non-negotiable for accessibility. Dense layouts must find other ways to save space.

**Generous spacing is fine**
Whitespace where navigational. Tight spacing where functional. The system doesn't require cramped layouts. Landing pages and marketing contexts can breathe. The design holds whether dense or spacious.

## Implementation Details

**Borders**: `border-2 border-primary` — 2px everywhere, using the primary color token

**Radius**: `rounded-none` — zero corner radius on everything, no exceptions

**Hover stripe**:

```
relative before:absolute before:inset-y-0 before:left-0 before:w-0 before:bg-current before:opacity-0 hover:before:w-1 hover:before:opacity-100
```

**Status stripe**: `border-l-4` with semantic color (green-500, amber-500, red-500, gray-500)

**Selection**: `data-active:bg-primary data-active:text-primary-foreground`

**Disabled**: Muted text, muted borders, no background change, no stripe

**Focus**: Visible ring or outline in accent color

**Type scale**: Use Tailwind's built-in scale (text-xs, text-sm, text-base, text-lg, etc.)

**Semantic tokens**: Use bg-primary, text-muted-foreground, border-destructive, etc. Don't hardcode hex values.

**Disable Radix animations**: Add `![animation-duration:0s] ![transition-duration:0s]` to overlay and content elements

## Accent Color

Yellow is the accent. It's reserved for primary actions and key information. One or two accent uses per viewport maximum. If everything is highlighted, nothing is.

## Technical Context

React, Tailwind, shadcn/ui. The shadcn defaults must be overridden — strip rounded corners, remove soft shadows, apply the design system. Components are starting points, not finished products.
