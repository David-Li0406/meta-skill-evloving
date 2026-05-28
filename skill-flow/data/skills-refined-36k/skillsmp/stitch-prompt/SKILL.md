---
name: stitch-prompt
description: Generate optimized UI prompts for Google Stitch (Gemini 2.5). Convert design ideas, specs, or wireframe descriptions into structured prompts following the 5-part pattern. Use when creating UI mockups, prototyping web/mobile apps, designing frontend layouts, or generating high-fidelity screen designs. Supports multi-screen build orders and incremental refinements.
---

# Stitch Prompt Generator

Generate well-structured prompts for Google Stitch to create high-fidelity UI designs.

## Overview

Google Stitch is an AI-powered UI design tool (Gemini 2.5) that generates responsive interfaces from natural language. This skill helps craft effective prompts that produce consistent, high-quality results.

**Default Output:** Detailed, structured prompts with specific measurements, hex colors, and component specs. Follow the examples in [references/examples.md](references/examples.md).

**Stitch UI Modes:**
- *Experimental* — Recommended when available (best quality)
- *High-fidelity* — Use if Experimental requires image upload
- *Standard* — Fast mode for quick wireframes or Figma exports

## Workflow

### 1. Gather Requirements

Ask the user for:
- **App/Screen purpose**: What is being designed and for whom?
- **Visual style**: Theme, colors (hex preferred), mood adjectives
- **Key components**: Navigation, cards, inputs, buttons, etc.
- **Reference apps**: Similar interfaces for inspiration (e.g., "like Linear", "Warp-style")

### 2. Generate Prompt Using 5-Part Structure

Every Stitch prompt follows this pattern:

```
1. CONTEXT      → What the app/page is for
2. USERS/GOALS  → Who uses it and why
3. LAYOUT       → Key structural components (nav, cards, grids)
4. VISUAL STYLE → Colors (hex), typography, mood
5. STATES       → Interactions and behaviors (optional but recommended)
```

**Target length:** 800-1500 characters for full screens. Use structured bullets with specs, not prose paragraphs. Favor density over verbosity.

### 3. Refine with Follow-up Prompts

For changes after initial generation:
- **One change per prompt** — Never combine multiple modifications
- **Reference existing elements** — "Keep the header, add X below it"
- **Be surgical** — Target specific components, not entire layouts
- **Explicit preservation** — "Update EXISTING [element]. DO NOT recreate. Keep [X] same."

## Output Format

**Multi-screen prompts:** Stitch can generate 2 screens per prompt. Use clear header labels to delineate each screen. This is faster than one-screen-per-prompt.

```
Generate two screens for [app name]:

=== SCREEN 1: [Name] ===

[Context and purpose]

LAYOUT:
- [Component specs...]

STYLE:
- [Color/typography specs...]

STATES:
- [State variations if needed]

=== SCREEN 2: [Name] ===

[Context and purpose]

LAYOUT:
- [Component specs...]

STYLE:
- [Same theme or variations...]

STATES:
- [State variations if needed]
```

**Single screen or modal with states:** One screen can show multiple states side-by-side (e.g., Install modal → Installing → Complete).

Output prompts in a code block. Minimize conversational preamble.

## Golden Rules

1. **Be specific and incremental** — Generic prompts → generic results
2. **One major change per refinement** — When editing existing screens, one change at a time (initial generation can have 2 screens)
3. **Use UI/UX terminology** — "CTA button", "hero section", "card layout"
4. **NO ASCII DIAGRAMS** — Stitch reads them as literal text. Use prose descriptions.

See [references/best-practices.md](references/best-practices.md) for detailed rules and pitfalls.

## Visual Style Guidelines

- **Hex colors encouraged** — `#FFA344` is better than "amber"
- **Reference apps welcome** — "Warp Terminal aesthetic", "Linear-style"
- **Mood adjectives** — "minimal", "vibrant", "professional", "dark theme"

## Resources

- **Best Practices**: See [references/best-practices.md](references/best-practices.md) for detailed rules, pitfalls, and length guidelines
- **Examples**: See [references/examples.md](references/examples.md) for real-world prompt patterns

## Build Order Pattern

For complex apps, generate screens in batches of 2 per prompt:

| Prompt | Screens |
|--------|---------|
| 1 | Foundation layout + Main content area |
| 2 | Input controls + Status elements |
| 3 | Settings modal + Model selector modal |
| 4 | History panel + Slash commands modal |
| 5 | Install modal (with states) + Think intensity dialog |
| 6 | Loading states + Error states |

**Tips:**
- Group related screens in same prompt (e.g., two modals, or a screen + its states)
- One screen can show multiple states side-by-side (Install → Installing → Complete)
- Each prompt builds on previous. Verify output before next batch.

**For large build orders (>6 prompts):** Use the Task tool to generate the full sequence in a separate file `stitch-build-order.md`.
