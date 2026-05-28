---
name: design-suite:workbench-init
description: Build UI with craft and consistency. For interface design (dashboards, apps, tools) — not marketing sites.
---

## Required Reading — Do This First

Before writing any code, read these files completely:

1. The workbench SKILL.md — the foundation, principles, and checks
2. `references/principles.md` — detailed craft including Tailwind patterns
3. `references/example.md` — MUI + Tailwind code examples

Do not skip this. The craft knowledge is in these files.

---

**Scope:** Dashboards, apps, tools, admin panels. Not landing pages or marketing sites — use `/design-suite:launchpad-init` for those.

## Stack

**Tailwind CSS** — Layout, spacing, typography, responsive design.

**Material UI** — Complex interactive components (data tables, date pickers, dialogs, autocomplete).

**Unified tokens** — CSS variables consumed by both Tailwind config and MUI theme.

See `references/tailwind-mui-integration.md` for setup details.

---

## Intent First — Answer Before Building

Before touching code, answer these out loud:

**Who is this human?** Not "users." Where are they? What's on their mind? A teacher at 7am with coffee is not a developer debugging at midnight.

**What must they accomplish?** Not "use the dashboard." The verb. Grade submissions. Find the broken deployment. Approve the payment.

**What should this feel like?** In words that mean something. "Clean" means nothing. Warm like a notebook? Cold like a terminal? Dense like a trading floor?

If you cannot answer these with specifics, stop and ask the user. Do not guess. Do not default.

---

## Before Writing Each Component

State the intent AND the technical approach:

```
Intent: [who, what they need to do, how it should feel]
Palette: [foundation + accent — and WHY these colors fit the product's world]
Depth: [borders / subtle shadows / layered — and WHY]
Surfaces: [your elevation scale — and WHY this temperature]
Typography: [your typeface choice — and WHY it fits the intent]
Spacing: [your base unit from Tailwind scale]
Stack: [Tailwind + MUI, specifying which MUI components if any]
Responsive: [breakpoint strategy, mobile-first approach]
```

Every choice must be explainable. If your answer is "it's common" or "it works" — you haven't chosen. You've defaulted.

**The test:** If another AI given a similar prompt would produce the same output, you have failed. The interface must emerge from THIS user, THIS problem, THIS intent.

---

## Communication

Be invisible. Don't announce modes or narrate process.

**Never say:** "I'm in ESTABLISH MODE", "Let me check system.md..."

**Instead:** Jump into work. State suggestions with reasoning.

---

## Suggest + Ask

Lead with your exploration and recommendation, then confirm:
```
"Domain: [concepts from this product's world]
Color world: [colors that exist in this domain]
Signature: [one element unique to this product]

Direction: [approach that connects to the above]
Stack: Tailwind for layout/styling, MUI for [specific components if needed]"

[AskUserQuestion: "Does that direction feel right?"]
```

---

## Flow

1. Read the required files above (always — even if system.md exists)
2. Check if `.workbench/system.md` exists
3. **If exists**: Apply established patterns from system.md
4. **If not**: Offer options:
   - Start fresh with domain exploration
   - Use a template as starting point (see `templates/` folder)
5. Assess context, suggest direction, get confirmation, build
6. Consider responsive needs early — not as an afterthought

The skill files contain the craft principles. system.md contains project-specific decisions. You need both.

---

## Responsive Considerations

Always consider responsive design from the start:

- **Sidebar:** Does it collapse on mobile?
- **Data tables:** Do they become cards on mobile?
- **Metric grids:** How do they stack?
- **Forms:** Do fields need different arrangement at different sizes?
- **Touch targets:** Are interactive elements at least 44px on mobile?

See `references/responsive-patterns.md` for patterns.

---

## Token Configuration Reference

When establishing a system, include token configuration:

```js
// tailwind.config.js extend colors
colors: {
  canvas: 'var(--canvas)',
  surface: { DEFAULT: 'var(--surface)', elevated: 'var(--surface-elevated)' },
  ink: { DEFAULT: 'var(--ink)', secondary: 'var(--ink-secondary)', muted: 'var(--ink-muted)' },
  edge: { DEFAULT: 'var(--edge)', subtle: 'var(--edge-subtle)' },
  accent: 'var(--accent)',
}
```

```css
/* CSS variables */
:root {
  --canvas: #fafafa;
  --surface: #ffffff;
  --ink: #0f172a;
  --edge: rgba(0, 0, 0, 0.08);
  --accent: #2563eb;
}
```

---

## After Every Task

Offer to save when you finish building UI:

"Want me to save these patterns to `.workbench/system.md`?"

Include in system.md:
- Direction and feel
- Tailwind config (colors, spacing, radius)
- MUI theme configuration
- Depth strategy
- Key component patterns
- Responsive strategy

Always offer — new patterns should be captured whether system.md exists or not.
