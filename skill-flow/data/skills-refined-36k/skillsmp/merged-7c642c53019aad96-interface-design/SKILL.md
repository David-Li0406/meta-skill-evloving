---
name: interface-design
description: Use this skill for designing interfaces such as dashboards, admin panels, apps, tools, and interactive products, ensuring a systematic and crafted approach.
---

# Interface Design

Build interface designs with craft, consistency, and systematic precision.

## Scope

**Use for:** Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.

**Not for:** Landing pages, marketing sites, campaigns. Redirect those to `/design-suite:launchpad`.

## Design Principles

### Spacing
Use a consistent base unit for spacing. Stick to multiples to maintain a cohesive design.

### Padding
Keep padding symmetrical. If one side is 16px, others should match unless there's a clear reason.

### Depth
Choose ONE approach and commit:
- **Borders-only** — Clean, technical. For dense tools.
- **Subtle shadows** — Soft lift. For approachable products.
- **Layered shadows** — Premium, dimensional. For cards that need presence.

### Border Radius
Select a scale for border radius:
- Sharper feels technical.
- Rounder feels friendly.

### Typography
Establish a hierarchy:
- Headlines need weight and tight tracking.
- Body text needs readability.
- Data should use monospace.

### Color
Use color to communicate meaning — status, action, emphasis. Avoid decorative colors that add noise.

### Animation
Implement fast micro-interactions with smooth easing. Avoid bouncy effects.

### Controls
Use native `<select>` and `<input type="date">` components where applicable, and build custom components for others.

## Workflow

### Communication
Be invisible. Don't announce modes or narrate processes. Jump into work and state suggestions with reasoning.

### Suggest + Ask
Lead with your exploration and recommendation, then confirm:
```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

### If Project Has system.md
Read `.interface-design/system.md` and apply. Decisions are made.

### If No system.md
1. Explore domain — Produce all required outputs.
2. Propose — Direction must reference all outputs.
3. Confirm — Get user buy-in.
4. Build — Apply principles with Tailwind + MUI.
5. **Evaluate** — Run the mandate checks before showing.
6. Offer to save.

## After Completing a Task

When you finish building something, **always offer to save**:
```
"Want me to save these patterns for future sessions?"
```
If yes, write to `.interface-design/system.md`:
- Direction and feel
- Tailwind config (colors, spacing, radius)
- MUI theme configuration
- Depth strategy (borders/shadows/layered)
- Key component patterns
- Responsive strategy

## Avoid

- Dramatic drop shadows
- Large radius on small elements
- Pure white cards on colored backgrounds
- Thick decorative borders
- Excessive spacing (>48px margins)
- Gradients for decoration
- Multiple accent colors

## Self-Check

Before finishing:
- Did I think about what this product needs, or default?
- Is my depth strategy consistent throughout?
- Does every element feel intentional?

The standard: looks designed by someone who obsesses over details.

## Deep Dives

For more detail on specific topics:
- `references/principles.md` — Core craft, Tailwind patterns, dark mode
- `references/example.md` — MUI + Tailwind code examples
- `references/tailwind-mui-integration.md` — Stack setup and patterns
- `references/responsive-patterns.md` — Mobile-first responsive patterns
- `references/validation.md` — Memory management, when to update system.md

# Commands

- `/design-suite:workbench-init` — Initialize design system for a project
- `/design-suite:workbench-status` — Current system state
- `/design-suite:workbench-audit` — Check code against system
- `/design-suite:workbench-extract` — Extract patterns from code