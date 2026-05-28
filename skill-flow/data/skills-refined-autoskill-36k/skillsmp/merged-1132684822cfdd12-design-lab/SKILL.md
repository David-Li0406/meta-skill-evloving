---
name: design-lab
description: Use this skill to conduct design interviews, generate multiple distinct UI variations, collect feedback, and produce implementation plans for exploring UI design options or redesigning existing components.
---

# Design Lab Skill

This skill implements a complete design exploration workflow: interview, generate variations, collect feedback, refine, preview, and finalize.

## CRITICAL: Cleanup Behavior

**All temporary files MUST be deleted when the process ends, whether by:**
- User confirms final design → cleanup, then generate plan
- User aborts/cancels → cleanup immediately, no plan generated

**Never leave `.claude-design/` or `__design_lab` routes behind.** If the user says "cancel", "abort", "stop", or "nevermind" at any point, confirm and then delete all temporary artifacts.

---

## Phase 0: Preflight Detection

Before starting the interview, automatically detect:

### Package Manager
Check for lock files in the project root:
- `pnpm-lock.yaml` → use `pnpm`
- `yarn.lock` → use `yarn`
- `package-lock.json` → use `npm`
- `bun.lockb` → use `bun`

### Framework Detection
Check for config files:
- `next.config.js` or `next.config.mjs` or `next.config.ts` → **Next.js**
  - Check for `app/` directory → App Router
  - Check for `pages/` directory → Pages Router
- `vite.config.js` or `vite.config.ts` → **Vite**
- `remix.config.js` → **Remix**
- `nuxt.config.js` or `nuxt.config.ts` → **Nuxt**
- `astro.config.mjs` → **Astro**

### Styling System Detection
Check `package.json` dependencies and config files:
- `tailwind.config.js` or `tailwind.config.ts` → **Tailwind CSS**
- `@mui/material` in dependencies → **Material UI**
- `@chakra-ui/react` in dependencies → **Chakra UI**
- `antd` in dependencies → **Ant Design**
- `styled-components` in dependencies → **styled-components**
- `@emotion/react` in dependencies → **Emotion**
- `.css` or `.module.css` files → **CSS Modules**

### Design Memory Check
Look for existing Design Memory file:
- `docs/design-memory.md`
- `DESIGN_MEMORY.md`
- `.claude-design/design-memory.md`

If found, read it and use to prefill defaults and skip redundant questions.

### Visual Style Inference (CRITICAL)

**DO NOT use generic/predefined styles. Extract visual language from the project:**

**If Tailwind detected**, read `tailwind.config.js` or `tailwind.config.ts`:
```javascript
// Extract and use:
theme.colors      // Color palette
theme.spacing     // Spacing scale
theme.borderRadius // Radius values
theme.fontFamily  // Typography
theme.boxShadow   // Elevation system
```

**If CSS Variables exist**, read `globals.css`, `variables.css`, or `:root` definitions:
```css
:root {
  --color-*     /* Color tokens */
  --spacing-*   /* Spacing tokens */
  --font-*      /* Typography tokens */
  --radius-*    /* Border radius tokens */
}
```

**If UI library detected** (MUI, Chakra, Ant), read the theme configuration:
- MUI: `theme.ts` or `createTheme()` call
- Chakra: `theme/index.ts` or `extendTheme()` call
- Ant: `ConfigProvider` theme prop

**Always scan existing components** to understand patterns:
- Find 2-3 existing buttons → note their styling patterns
- Find 2-3 existing cards → note padding, borders, shadows
- Find existing forms → note input styles, label placement
- Find existing typography → note heading sizes, body text

**Store inferred styles in the Design Brief** for consistent use across all variants.

---

## Phase 1: Interview

Use the **AskUserQuestion** tool for all interview steps. Adapt questions based on Design Memory if it exists.

### Step 1.1: Scope & Target

Ask these questions (can combine into single AskUserQuestion with multiple questions):

**Question 1: Scope**
- Header: "Scope"
- Question: "Are we designing a single component or a full page?"
- Options:
  - "Component" - A reusable UI element (button, card, form, modal, etc.)
  - "Page" - A complete page or screen layout

**Question 2: New or Redesign**
- Header: "Type"
- Question: "Is this a new design or a redesign of something existing?"
- Options:
  - "New" - Creating something from scratch
  - "Redesign" - Improving an existing component/page

If "Redesign" selected, ask:
**Question 3: Existing Path**
- Header: "Location"
- Question: "What is the file path or route of the existing UI?"
- Options: (let user provide via "Other")

If target is unclear, propose a name based on repo patterns and confirm.

### Step 1.2: Pain Points & Inspiration

**Question 1: Pain Points**
- Header: "Problems"
- Question: "What are the top pain points with the current design (or what should this new design avoid)?"
- Options:
  - "Too cluttered/dense" - Information overload, hard to scan
  - "Unclear hierarchy" - Primary actions aren't obvious
  - "Poor mobile experience" - Doesn't work well on small screens
  - "Outdated look" - Feels old or inconsistent with brand
- multiSelect: true

**Question 2: Visual Inspiration**
- Header: "Visual style"
- Question: "What products or brands should I reference for visual inspiration?"
- Options:
  - "Stripe" - Clean, minimal, trustworthy
  - "Linear" - Dense, keyboard-first, developer-focused
  - "Notion" - Flexible, content-focused, playful
  - "Apple" - Premium, spacious, refined
- multiSelect: true

**Question 3: Functional Inspiration**
- Header: "Interactions"
- Question: "What interaction patterns should I emulate?"
- Options:
  - "Inline editing" - Edit in place without modals
  - "Progressive disclosure" - Show more as needed
  - "Optimistic updates" - Instant feedback, sync in background
  - "Keyboard shortcuts" - Power user efficiency

### Step 1.3: Brand & Style Direction

**Question 1: Brand Adjectives**
- Header: "Brand tone"
- Question: "What 3-5 adjectives describe the desired brand feel?"
- Options:
  - "Minimal" - Clean, simple, uncluttered
  - "Premium" - High-end, polished, refined
  - "Playful" - Fun, friendly, approachable
  - "Utilitarian" - Functional, efficient, no-nonsense
- multiSelect: true

**Question 2: Density**
- Header: "Density"
- Question: "What information density do you prefer?"
- Options:
  - "Compact" - More information visible, tighter spacing
  - "Comfortable" - Balanced spacing, easy scanning
  - "Spacious" - Generous whitespace, focused attention

**Question 3: Dark Mode**
- Header: "Dark mode"
- Question: "Is dark mode required?"
- Options:
  - "Yes" - Must support dark mode
  - "No" - Light mode only
  - "Nice to have" - Support if easy, not required

### Step 1.4: Persona & Jobs-to-be-Done

**Question 1: Primary User**
- Header: "User"
- Question: "Who is the primary end user?"
- Options:
  - "Developer" - Technical, keyboard-oriented
  - "Designer" - Visual, detail-oriented
  - "Business user" - Efficiency-focused, less technical
  - "End consumer" - General public, varied technical ability

**Question 2: Context**
- Header: "Context"
- Question: "What's the primary usage context?"
- Options:
  - "Desktop-first" - Primarily used on larger screens
  - "Mobile-first" - Primarily used on phones
  - "Both equally" - Must work well on all devices

**Question 3: Key Tasks**
- Header: "Key tasks"
- Question: "What are the top 3 tasks users must complete?"
- (Let user provide via "Other" - this is open-ended)

### Step 1.5: Constraints

**Question 1: Must-Keep Elements**
- Header: "Keep"
- Question: "Are there elements that must be preserved?"
- Options:
  - "Existing copy/labels" - Keep current text
  - "Current fields/inputs" - Keep form structure
  - "Navigation structure" - Keep current nav
  - "None" - Free to change everything

**Question 2: Technical Constraints**
- Header: "Constraints"
- Question: "Any technical constraints?"
- Options:
  - "No new dependencies" - Use existing libraries only
  - "Use existing components" - Build on current design system
  - "Must be accessible (WCAG)" - Strict accessibility requirements
  - "None" - No special constraints
- multiSelect: true

---

## Phase 2: Generate Design Brief

After the interview, create a structured Design Brief as JSON and save to `.claude-design/design-brief.json`:

```json
{
  "scope": "component|page",
  "isRedesign": true|false,
  "targetPath": "src/components/Example.tsx",
  "targetName": "Example",
  "painPoints": ["Too dense", "Primary action unclear"],
  "inspiration": {
    "visual": ["Stripe", "Linear"],
    "functional": ["Inline validation"]
  },
  "brand": {
    "adjectives": ["minimal", "trustworthy"],
    "density": "comfortable",
    "darkMode": true
  },
  "persona": {
    "primary": "Developer",
    "context": "desktop-first",
    "keyTasks": ["Complete checkout", "Review order", "Apply discount"]
  },
  "constraints": {
    "mustKeep": ["existing fields"],
    "technical": ["no new dependencies", "WCAG accessible"]
  },
  "framework": "nextjs-app",
  "packageManager": "pnpm",
  "stylingSystem": "tailwind"
}
```

Display a summary to the user before proceeding.

---

## Phase 3: Generate Design Lab

### Directory Structure

Create all files under `.claude-design/`:

```
.claude-design/
├── lab/
│   ├── page.tsx                 # Main lab page (framework-specific)
│   ├── variants/
│   │   ├── VariantA.tsx
│   │   ├── VariantB.tsx
│   │   ├── VariantC.tsx
│   │   ├── VariantD.tsx
│   │   └── VariantE.tsx
│   ├── components/
│   │   └── LabShell.tsx         # Lab layout wrapper
│   ├── feedback/                # Interactive feedback system
│   │   ├── types.ts             # TypeScript interfaces
│   │   ├── selector-utils.ts    # Element identification
│   │   ├── format-utils.ts      # Feedback formatting
│   │   ├── FeedbackOverlay.tsx  # Main overlay component
│   │   └── index.ts             # Module exports
│   └── data/
│       └── fixtures.ts          # Shared mock data
├── design-brief.json
└── run-log.md
```

### Feedback System Setup (CRITICAL - NEVER SKIP)

**The FeedbackOverlay is the PRIMARY feature of the Design Lab.** Without it, users cannot provide interactive feedback. NEVER generate a Design Lab without the FeedbackOverlay.

**Reliability Strategy:** To avoid import path issues across different project configurations, create the FeedbackOverlay **directly in the route directory** (e.g., `app/design-lab/FeedbackOverlay.tsx`), NOT in `.claude-design/`. This ensures a simple relative import (`./FeedbackOverlay`) always works.

**Required Files in Route Directory:**
```
app/design-lab/           # or app/__design_lab/ if underscores work
├── page.tsx              # Main lab page with variants
└── FeedbackOverlay.tsx   # Self-contained overlay component (copy from templates)
```

**Template Source:** `design-and-refine/templates/feedback/FeedbackOverlay.tsx`

**Why this approach:**
- `.claude-design/` paths can fail due to bundler configurations
- Relative imports from the same directory always work
- The route directory gets deleted during cleanup anyway

### Route Integration

**Next.js App Router:**
Create `app/__design_lab/page.tsx` that imports from `.claude-design/lab/`

**Next.js Pages Router:**
Create `pages/__design_lab.tsx` that imports from `.claude-design/lab/`

**Vite React:**
- If React Router exists: add route to `/__design_lab`
- If no router: create a conditional render in `App.tsx` based on `?design_lab=true` query param

**Other frameworks:**
Create the most appropriate temporary route for the detected framework.

### Variant Generation Guidelines

**IMPORTANT:** Read `DESIGN_PRINCIPLES.md` for UX, interaction, and motion best practices. But **DO NOT use predefined visual styles**—infer them from the project.

**Apply universal principles (from DESIGN_PRINCIPLES.md):**
- **UX**: Nielsen's heuristics, cognitive load reduction, progressive disclosure
- **Component behavior**: Button states, form anatomy, card structure
- **Interaction**: Feedback patterns, state handling, optimistic updates
- **Motion**: Timing (150-300ms), easing (ease-out entrances, ease-in exits)
- **Accessibility**: Focus states, ARIA patterns, touch targets (44px min)

**Infer visual styles from the project:**
- Colors → from Tailwind config, CSS variables, or existing components
- Typography → from existing headings, body text in the codebase
- Spacing → from the project's spacing scale or existing patterns
- Border radius → from existing cards, buttons, inputs
- Shadows → from existing elevated components

---

Each variant MUST explore a different design axis. Do not create minor variations—make them meaningfully distinct. **Use the project's existing visual language for all variants.**

**Variant A: Information Hierarchy Focus**
- Restructure content hierarchy (what's most important?)
- Apply Gestalt proximity—group related items closer
- One primary action per view
- Use existing typography scale to create clear levels

**Variant B: Layout Model Exploration**
- Try a different layout approach (card vs list vs table vs split-pane)
- Apply card anatomy or table behavior patterns from DESIGN_PRINCIPLES
- Consider responsive behavior at each breakpoint
- Use the project's existing grid/layout system

**Variant C: Density Variation**
- If brief says "comfortable", try a more compact version
- If brief says "compact", try a more spacious version
- Use the project's existing spacing tokens—just apply them differently
- Show the tradeoffs: more visible data vs easier scanning

**Variant D: Interaction Model**
- Different interaction pattern (modal vs inline vs panel vs drawer)
- Apply feedback patterns: immediate → progress → completion
- Implement all required states (loading, error, empty, disabled)
- Consider optimistic updates for non-destructive actions

**Variant E: Expressive Direction**
- Push the brand direction the user described in the interview
- Explore different uses of the project's existing design tokens
- More or less use of shadows, borders, background colors
- Apply motion where it adds meaning (hover, focus, transitions)

### Lab Page Requirements

The Design Lab page must include:

1. **Header** with:
   - Design Brief summary (target, scope, key requirements)
   - Instructions for reviewing

2. **Variant Grid** with:
   - Clear labels (A, B, C, D, E)
   - Brief rationale for each variant ("Why this exists")
   - The actual rendered variant
   - Notes highlighting key differences
   - **IMPORTANT:** Each variant container must have `data-variant="