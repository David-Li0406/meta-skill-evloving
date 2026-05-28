---
name: workbench
description: This skill is for interface design — dashboards, admin panels, apps, tools, and interactive products. NOT for marketing design (landing pages, marketing sites, campaigns).
---

# Workbench

Build interface design with craft, consistency, and systematic precision.

## Scope

**Use for:** Dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces.

**Not for:** Landing pages, marketing sites, campaigns. Redirect those to `/design-suite:launchpad`.

## Stack

**Tailwind CSS** — Utility-first, design tokens via config, responsive primitives.

**Material UI (MUI)** — Component library for complex interactive elements (data tables, dialogs, date pickers).

**Philosophy:** Tailwind for layout, spacing, typography. MUI for behavioral components. Both driven by a unified token system.

---

# The Problem

You will generate generic output. Your training has seen thousands of dashboards. The patterns are strong.

You can follow the entire process below — explore the domain, name a signature, state your intent — and still produce a template. Warm colors on cold structures. Friendly fonts on generic layouts. "Kitchen feel" that looks like every other app.

This happens because intent lives in prose, but code generation pulls from patterns. The gap between them is where defaults win.

The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.

---

# Where Defaults Hide

Defaults don't announce themselves. They disguise themselves as infrastructure — the parts that feel like they just need to work, not be designed.

**Typography feels like a container.** Pick something readable, move on. But typography isn't holding your design — it IS your design. The weight of a headline, the personality of a label, the texture of a paragraph. These shape how the product feels before anyone reads a word. A bakery management tool and a trading terminal might both need "clean, readable type" — but the type that's warm and handmade is not the type that's cold and precise. If you're reaching for your usual font, you're not designing.

**Navigation feels like scaffolding.** Build the sidebar, add the links, get to the real work. But navigation isn't around your product — it IS your product. Where you are, where you can go, what matters most. A page floating in space is a component demo, not software. The navigation teaches people how to think about the space they're in.

**Data feels like presentation.** You have numbers, show numbers. But a number on screen is not design. The question is: what does this number mean to the person looking at it? What will they do with it? A progress ring and a stacked label both show "3 of 10" — one tells a story, one fills space. If you're reaching for number-on-label, you're not designing.

**Token names feel like implementation detail.** But your Tailwind config is design decisions. Semantic names like `--ink` and `--parchment` evoke a world. Generic names like `gray-700` and `surface-2` evoke a template. Someone reading only your tokens should be able to guess what product this is.

The trap is thinking some decisions are creative and others are structural. There are no structural decisions. Everything is design. The moment you stop asking "why this?" is the moment defaults take over.

---

# Systematic Precision

Guidelines, not rules. Tokens first, then components.

## Tokens-First Thinking

Before any component work, establish the token foundation in `tailwind.config.js`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Semantic tokens that reflect the product's world
        canvas: 'var(--canvas)',
        surface: {
          DEFAULT: 'var(--surface)',
          elevated: 'var(--surface-elevated)',
          overlay: 'var(--surface-overlay)',
        },
        ink: {
          DEFAULT: 'var(--ink)',
          secondary: 'var(--ink-secondary)',
          muted: 'var(--ink-muted)',
        },
        edge: {
          DEFAULT: 'var(--edge)',
          subtle: 'var(--edge-subtle)',
        },
        accent: 'var(--accent)',
      },
      spacing: {
        // Named spacing for semantic use
        'card': '1rem',      // 16px - internal card padding
        'section': '1.5rem', // 24px - between related groups
        'region': '2rem',    // 32px - between distinct sections
      },
      borderRadius: {
        'control': '0.375rem', // 6px - buttons, inputs
        'card': '0.5rem',      // 8px - cards, panels
        'modal': '0.75rem',    // 12px - dialogs, overlays
      },
    },
  },
}
```

CSS variables are set in your base styles, allowing theme switching:

```css
:root {
  --canvas: #fafafa;
  --surface: #ffffff;
  --surface-elevated: #ffffff;
  --ink: #0f172a;
  --ink-secondary: #475569;
  --ink-muted: #94a3b8;
  --edge: rgba(0, 0, 0, 0.08);
  --edge-subtle: rgba(0, 0, 0, 0.04);
  --accent: #2563eb;
}

.dark {
  --canvas: #0a0a0a;
  --surface: #141414;
  --surface-elevated: #1a1a1a;
  --ink: #fafafa;
  --ink-secondary: #a1a1aa;
  --ink-muted: #71717a;
  --edge: rgba(255, 255, 255, 0.08);
  --edge-subtle: rgba(255, 255, 255, 0.04);
  --accent: #3b82f6;
}
```

## Consistency Over Creativity

Creativity belongs in direction. Execution demands consistency.

Once you've established a direction (warm, dense, technical, calm), every decision must reinforce it. Don't get creative with individual components — get systematic. A card that breaks the spacing scale, a button with custom radius, an input with unique padding — these aren't creative touches, they're inconsistencies.

**The rule:** If it's not in your token system, don't use it. Random `p-[13px]` or `text-[15px]` signals no system.

---

# Intent First

Before touching code, answer these. Not in your head — out loud, to yourself or the user.

**Who is this human?**
Not "users." The actual person. Where are they when they open this? What's on their mind? What did they do 5 minutes ago, what will they do 5 minutes after? A teacher at 7am with coffee is not a developer debugging at midnight is not a founder between investor meetings. Their world shapes the interface.

**What must they accomplish?**
Not "use the dashboard." The verb. Grade these submissions. Find the broken deployment. Approve the payment. The answer determines what leads, what follows, what hides.

**What should this feel like?**
Say it in words that mean something. "Clean and modern" means nothing — every AI says that. Warm like a notebook? Cold like a terminal? Dense like a trading floor? Calm like a reading app? The answer shapes color, type, spacing, density — everything.

If you cannot answer these with specifics, stop. Ask the user. Do not guess. Do not default.

## Every Choice Must Be A Choice

For every decision, you must be able to explain WHY.

- Why this layout and not another?
- Why this color temperature?
- Why this typeface?
- Why this spacing scale?
- Why this information hierarchy?

If your answer is "it's common" or "it's clean" or "it works" — you haven't chosen. You've defaulted. Defaults are invisible. Invisible choices compound into generic output.

**The test:** If you swapped your choices for the most common alternatives and the design didn't feel meaningfully different, you never made real choices.

## Sameness Is Failure

If another AI, given a similar prompt, would produce substantially the same output — you have failed.

This is not about being different for its own sake. It's about the interface emerging from the specific problem, the specific user, the specific context. When you design from intent, sameness becomes impossible because no two intents are identical.

When you design from defaults, everything looks the same because defaults are shared.

## Intent Must Be Systemic

Saying "warm" and using cold colors is not following through. Intent is not a label — it's a constraint that shapes every decision.

If the intent is warm: surfaces, text, borders, accents, semantic colors, typography — all warm. If the intent is dense: spacing, type size, information architecture — all dense. If the intent is calm: motion, contrast, color saturation — all calm.

Check your output against your stated intent. Does every token reinforce it? Or did you state an intent and then default anyway?

---

# Product Domain Exploration

This is where defaults get caught — or don't.

Generic output: Task type → Visual template → Theme
Crafted output: Task type → Product domain → Signature → Structure + Expression

The difference: time in the product's world before any visual or structural thinking.

## Required Outputs

**Do not propose any direction until you produce all four:**

**Domain:** Concepts, metaphors, vocabulary from this product's world. Not features — territory. Minimum 5.

**Color world:** What colors exist naturally in this product's domain? Not "warm" or "cool" — go to the actual world. If this product were a physical space, what would you see? What colors belong there that don't belong elsewhere? List 5+.

**Signature:** One element — visual, structural, or interaction — that could only exist for THIS product. If you can't name one, keep exploring.

**Defaults:** 3 obvious choices for this interface type — visual AND structural. You can't avoid patterns you haven't named.

## Proposal Requirements

Your direction must explicitly reference:
- Domain concepts you explored
- Colors from your color world exploration
- Your signature element
- What replaces each default

**The test:** Read your proposal. Remove the product name. Could someone identify what this is for? If not, it's generic. Explore deeper.

---

# Reference Products

Study these for systematic precision in interface design:

## Airwallex

**Why:** Financial infrastructure that handles complexity without visual complexity. Clean data density. Tables that breathe. Metric displays that inform without overwhelming.

**Study:**
- How they handle dense financial data with generous whitespace
- Transaction tables with subtle row separation
- Multi-currency displays with clear hierarchy
- Settings pages that don't feel like forms

## Stripe

**Why:** The gold standard for developer-facing products. Information architecture that scales. Components that teach their own usage.

**Study:**
- Metric cards with contextual data (not just numbers)
- API response previews that feel native
- Navigation that reveals depth progressively
- Documentation patterns embedded in product

**What they share:** Both treat data as content, not decoration. Every number has context. Every table tells a story. Density with clarity.

---

# The Mandate

**Before showing the user, look at what you made.**

Ask yourself: "If they said this lacks craft, what would they mean?"

That thing you just thought of — fix it first.

Your first output is probably generic. That's normal. The work is catching it before the user has to.

## The Checks

Run these against your output before presenting:

- **The swap test:** If you swapped the typeface for your usual one, would anyone notice? If you swapped the layout for a standard dashboard template, would it feel different? The places where swapping wouldn't matter are the places you defaulted.

- **The squint test:** Blur your eyes. Can you still perceive hierarchy? Is anything jumping out harshly? Craft whispers.

- **The signature test:** Can you point to five specific elements where your signature appears? Not "the overall feel" — actual components. A signature you can't locate doesn't exist.

- **The token test:** Read your Tailwind config out loud. Do the semantic names sound like they belong to this product's world, or could they belong to any project?

If any check fails, iterate before showing.

---

# Craft Foundations

## Subtle Layering

This is the backbone of craft. Regardless of direction, product type, or visual style — this principle applies to everything.

**Surfaces must be barely different but still distinguishable.** Study Airwallex and Stripe. Their elevation changes are so subtle you almost can't see them — but you feel the hierarchy. Not dramatic jumps. Not obviously different colors. Whisper-quiet shifts.

**Borders must be light but not invisible.** The border should disappear when you're not looking for it, but be findable when you need to understand structure. If borders are the first thing you notice, they're too strong. If you can't tell where regions begin and end, they're too weak.

**The squint test:** Blur your eyes at the interface. You should still perceive hierarchy — what's above what, where sections divide. But nothing should jump out. No harsh lines. No jarring color shifts. Just quiet structure.

This separates professional interfaces from amateur ones. Get this wrong and nothing else matters.

## Infinite Expression

Every pattern has infinite expressions. **No interface should look the same.**

A metric display could be a hero number, inline stat, sparkline, gauge, progress bar, comparison delta, trend badge, or something new. A dashboard could emphasize density, whitespace, hierarchy, or flow in completely different ways. Even sidebar + cards has infinite variations in proportion, spacing, and emphasis.

**Before building, ask:**
- What's the ONE thing users do most here?
- What products solve similar problems brilliantly? Study them.
- Why would this interface feel designed for its purpose, not templated?

**NEVER produce identical output.** Same sidebar width, same card grid, same metric boxes with icon-left-number-big-label-small every time — this signals AI-generated immediately. It's forgettable.

The architecture and components should emerge from the task and data, executed in a way that feels fresh. Stripe's cards don't look like Airwallex's. Same concepts, infinite expressions.

## Color Lives Somewhere

Every product exists in a world. That world has colors.

Before you reach for a palette, spend time in the product's world. What would you see if you walked into the physical version of this space? What materials? What light? What objects?

Your palette should feel like it came FROM somewhere — not like it was applied TO something.

**Beyond Warm and Cold:** Temperature is one axis. Is this quiet or loud? Dense or spacious? Serious or playful? Geometric or organic? A trading terminal and a meditation app are both "focused" — completely different kinds of focus. Find the specific quality, not the generic label.

**Color Carries Meaning:** Gray builds structure. Color communicates — status, action, emphasis, identity. Unmotivated color is noise. One accent color, used with intention, beats five colors used without thought.

---

# Design Principles

These are guidelines, not rules. Adapt to context.

## Spacing (Tailwind Scale)

Use Tailwind's spacing scale consistently. Map semantic meanings:

```
Micro:   gap-1, gap-1.5, gap-2     (4-8px)  - icon gaps, tight pairs
Element: p-2, p-3, p-4             (8-16px) - within buttons, inputs
Card:    p-4, p-5, p-6             (16-24px) - card internals
Section: gap-6, gap-8              (24-32px) - between groups
Region:  gap-8, gap-12, gap-16     (32-64px) - major separations
```

Random values signal no system. Stick to the scale.

## Padding

Keep it symmetrical. Tailwind makes this easy:

```jsx
// Good
className="p-4"
className="px-4 py-3" // Only when horizontal needs more room

// Bad - asymmetric without reason
className="pt-6 pr-4 pb-3 pl-4"
```

## Depth

Choose ONE approach and commit:

- **Borders-only** — `border border-edge` — Clean, technical. For dense tools.
- **Subtle shadows** — `shadow-sm` — Soft lift. For approachable products.
- **Layered shadows** — Custom multi-layer — Premium, dimensional. For cards that need presence.

Don't mix approaches within a product.

## Border Radius (Tailwind Scale)

Sharper feels technical. Rounder feels friendly. Pick a scale:

```
Sharp:  rounded, rounded-md       (4-6px)  - utility tools, data apps
Medium: rounded-md, rounded-lg    (6-8px)  - balanced, most products
Soft:   rounded-lg, rounded-xl    (8-12px) - friendly, consumer-facing
```

Apply consistently across all components.

## Typography

Headlines need weight and tight tracking. Body needs readability. Data needs monospace.

```jsx
// Headlines
className="text-2xl font-semibold tracking-tight text-ink"

// Body
className="text-sm text-ink-secondary"

// Data/Numbers
className="font-mono text-sm tabular-nums text-ink"

// Labels
className="text-xs font-medium uppercase tracking-wide text-ink-muted"
```

## Color & Surfaces

Build from your token system. Every color traces back to:

- **ink** — text hierarchy (primary, secondary, muted)
- **surface** — elevation (base, elevated, overlay)
- **edge** — borders (default, subtle)
- **accent** — primary action color
- **semantic** — destructive, warning, success

No random hex values. Everything maps to tokens.

## Animation

Fast micro-interactions, smooth easing. Use Tailwind's transition utilities:

```jsx
className="transition-colors duration-150"  // Hover states
className="transition-all duration-200"     // Larger changes
```

No bouncy/spring effects. Professional interfaces move smoothly.

## States

Every interactive element needs states. In Tailwind:

```jsx
className="
  bg-surface hover:bg-surface-elevated
  border border-edge hover:border-edge-subtle
  focus:outline-none focus:ring-2 focus:ring-accent/20
  disabled:opacity-50 disabled:cursor-not-allowed
"
```

Data needs states too: loading (skeleton), empty (illustration + message), error (inline feedback).

---

# Responsive Design

Mobile-first, content-driven breakpoints.

## Breakpoint Philosophy

Don't design for devices. Design for content. When does the content break? That's your breakpoint.

Tailwind's defaults are sensible starting points:
- `sm:` 640px — Small tablets, large phones landscape
- `md:` 768px — Tablets
- `lg:` 1024px — Small laptops, tablets landscape
- `xl:` 1280px — Desktops

## Core Patterns

**Sidebar:** Collapsible on mobile, fixed on desktop.

```jsx
// Sidebar container
className="fixed inset-y-0 left-0 z-40 w-64 transform transition-transform
           -translate-x-full md:translate-x-0 md:static"

// Overlay for mobile
className="fixed inset-0 bg-black/50 md:hidden"
```

**Data Tables:** Cards on mobile, tables on desktop.

```jsx
// Container
className="block md:table"

// Row becomes card
className="block md:table-row border-b last:border-0 md:border-0"
```

**Metric Grids:** Stack or reduce columns.

```jsx
className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"
```

## Touch Considerations

Minimum 44px touch targets. In Tailwind:

```jsx
className="min-h-[44px] min-w-[44px]"  // Touch targets
className="p-3"                          // Generous tap areas
```

See `references/responsive-patterns.md` for detailed patterns.

---

# Avoid

- **Harsh borders** — if borders are the first thing you see, they're too strong
- **Dramatic surface jumps** — elevation changes should be whisper-quiet
- **Inconsistent spacing** — the clearest sign of no system
- **Mixed depth strategies** — pick one approach and commit
- **Missing interaction states** — hover, focus, disabled, loading, error
- **Dramatic drop shadows** — shadows should be subtle, not attention-grabbing
- **Large radius on small elements**
- **Pure white cards on colored backgrounds**
- **Thick decorative borders**
- **Gradients and color for decoration** — color should mean something
- **Multiple accent colors** — dilutes focus
- **Arbitrary Tailwind values** — `p-[13px]` signals no system
- **Bright, saturated colors** — harsh neons and high-saturation palettes feel AI-generated. Prefer muted, professional tones unless the user explicitly requests vibrant colors

---

# Workflow

## Communication
Be invisible. Don't announce modes or narrate process.

**Never say:** "I'm in ESTABLISH MODE", "Let me check system.md..."

**Instead:** Jump into work. State suggestions with reasoning.

## Suggest + Ask
Lead with your exploration and recommendation, then confirm:
```
"Domain: [5+ concepts from the product's world]
Color world: [5+ colors that exist in this domain]
Signature: [one element unique to this product]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

## If Project Has system.md
Read `.interface-design/system.md` and apply. Decisions are made.

## If No system.md
1. Explore domain — Produce all four required outputs
2. Propose — Direction must reference all four
3. Confirm — Get user buy-in
4. Build — Apply principles with Tailwind + MUI
5. **Evaluate** — Run the mandate checks before showing
6. Offer to save

---

# After Completing a Task

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

This compounds — each save makes future work faster and more consistent.

---

# Deep Dives

For more detail on specific topics:
- `references/principles.md` — Core craft, Tailwind patterns, dark mode
- `references/example.md` — MUI + Tailwind code examples
- `references/tailwind-mui-integration.md` — Stack setup and patterns
- `references/responsive-patterns.md` — Mobile-first responsive patterns
- `references/validation.md` — Memory management, when to update system.md

# Templates

Starting points for common interface types:
- `templates/saas-dashboard.md` — SaaS analytics dashboards, admin panels

Templates are scaffolds, not solutions. Adapt to your product's specific needs.

# Commands

- `/design-suite:workbench-init` — Initialize design system for a project
- `/design-suite:workbench-status` — Current system state
- `/design-suite:workbench-audit` — Check code against system
- `/design-suite:workbench-extract` — Extract patterns from code
