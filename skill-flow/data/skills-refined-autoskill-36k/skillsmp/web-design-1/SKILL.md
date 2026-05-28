---
name: web-design
description: "Create distinctive, production-grade layouts for aiandi.dev. Bold aesthetic vision + semantic token system. Use when designing pages, components, or visual treatments."
---

# Web Design Skill

**Purpose:** Create distinctive, production-grade interfaces for aiandi.dev that avoid generic "AI slop" aesthetics while leveraging our semantic token architecture.

**Related skills:** Use **design-loop** for iterative fine-tuning (or nuclear redesign) with visual verification. Use **screenshot** for one-off captures.

---

## Part I: Design Vision

### Design Thinking

Before touching code, understand context and commit to a **BOLD** aesthetic direction:

**The Questions:**
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: What's the emotional register? (See palette below)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?
- **Constraints**: Accessibility, performance, our token system

**⚠️ WARNING:** If you're about to make "incremental improvements" to an existing design, STOP. Consider whether this needs a radical departure instead. Safe fine-tuning creates forgettable design when the vision itself is wrong.

**Aesthetic Palette** (pick one, execute with conviction):

| Direction | Character |
|-----------|-----------|
| Brutally minimal | Nothing unnecessary. Every pixel justified. |
| Editorial/magazine | Typographic hierarchy as art. Generous space. |
| Retro-futuristic | Yesterday's tomorrow. CRT glow meets clean lines. |
| Organic/natural | Soft edges. Breathing rhythm. Warmth. |
| Luxury/refined | Restraint as statement. Precision obsession. |
| Industrial/utilitarian | Function forward. Honest materials. |
| Art deco/geometric | Pattern. Symmetry. Gilded edges. |
| Brutalist/raw | Exposed structure. Aggressive honesty. |

**CRITICAL**: Bold maximalism and refined minimalism both work. The key is **intentionality**, not intensity. Pick a direction and execute it with conviction.

---

### Creative Departure Prompts

When you need to break free from derivative thinking, ask:

**Inversion Questions:**
- What if the most important thing was SMALL instead of large?
- What if we used NO color except one?
- What if there was NO hero section, just immediate content?
- What if typography was PLAYFUL instead of serious?

**Constraint Forcing:**
- Design with only 2 font sizes
- Use only vertical or only horizontal rhythm (not both)
- Make ONE element absurdly oversized
- Ban all rounded corners OR ban all sharp corners

**Medium Shifts:**
- What if this was a printed zine?
- What if this was a terminal interface?
- What if this was handwritten notes?
- What if this was a museum placard?

**Unexpected References:**
- Scientific journals (data-dense, precise)
- Art gallery walls (space, curation, labels)
- Punk zines (raw, urgent, collage)
- Old programming books (monospace, diagrams)
- Brutalist architecture (exposed structure, no decoration)

**The test:** If your first idea is what everyone else would do, throw it away and force yourself to come up with 3 more alternatives before implementing.

---

### Aesthetic Guidelines

#### Typography: The Soul of the Design

**Choose fonts that have character.** The current Workbench theme uses system fonts for speed and clarity, but when evolving the design:

| Avoid | Consider Instead |
|-------|------------------|
| Inter, Roboto, Arial | Fonts with personality for display |
| Generic sans-serif | Pair distinctive display + refined body |
| One font for everything | Intentional contrast between heading/body |

**Typography creates hierarchy through:**
- Size contrast (dramatic jumps, not timid steps)
- Weight contrast (light body, bold heads - or vice versa)
- Tracking (tight headlines, comfortable body)
- Leading (generous for reading, tight for impact)

#### Color: Commit to a Position

**Dominant colors with sharp accents outperform timid, evenly-distributed palettes.**

The current Workbench theme demonstrates this: deep charcoal dominates, amber accent punctuates. The ratio matters more than the hues.

When evolving themes:
- 60-30-10 rule: dominant, secondary, accent
- Let backgrounds breathe (most of the canvas)
- Accents should feel earned, not scattered

#### Motion: Choreography, Not Chaos

**One well-orchestrated moment creates more delight than scattered micro-interactions.**

Focus on:
- Page load: staggered reveals via `animation-delay`
- Scroll-triggered moments that reward attention
- Hover states that surprise without distracting
- Transitions that feel physical (ease-out for exits, ease-in-out for state changes)

#### Spatial Composition: Break the Expected

Consider:
- Asymmetry over centered everything
- Generous negative space OR controlled density (not medium)
- Grid-breaking moments for emphasis
- Overlap and layering for depth
- Diagonal flow for energy

#### Atmosphere: Beyond Flat Colors

Create depth through:
- Subtle gradients (not the cliched purple-to-pink)
- Noise textures for tactile quality
- Layered transparencies
- Dramatic shadows that define space
- Border treatments that add character

---

### Anti-Patterns: The AI Slop Checklist

**NEVER default to:**

| Generic Choice | The Problem |
|----------------|-------------|
| Purple gradients on white | Every AI demo ever made |
| Inter/Roboto/Space Grotesk | The "modern" that isn't |
| Centered everything | Safe is forgettable |
| Even spacing everywhere | No rhythm, no hierarchy |
| Rounded corners + soft shadows | The 2020 SaaS look |
| Teal + coral accent colors | Startup template vibes |

**The test:** Would this design be immediately recognizable as AI-generated? If yes, start over.

---

## Part II: Technical Execution

### Our Design System: Schema vs. Theme

We separate **structure** (what decisions exist) from **values** (how they resolve):

| Layer | Contains | Location |
|-------|----------|----------|
| **Schema** | Token names, semantic purposes | `design-system/tokens.css` |
| **Theme** | Values assigned to tokens | `design-system/all-themes.css` |

**Never hardcode values. Always use tokens.** This enables theme-switching without code changes.

---

### Token Quick Reference

#### Colors

| Purpose | Token | Tailwind |
|---------|-------|----------|
| Page background | `--color-background` | `bg-background` |
| Cards/elevated | `--color-surface` | `bg-surface` |
| Code blocks | `--color-surface-alt` | `bg-surface-alt` |
| Borders | `--color-border` | `border-border` |
| Body text | `--color-text-primary` | `text-text-primary` |
| Secondary text | `--color-text-secondary` | `text-text-secondary` |
| Muted text | `--color-text-muted` | `text-text-muted` |
| Links/accent | `--color-accent` | `text-accent` |
| Accent hover | `--color-accent-hover` | `hover:text-accent-hover` |
| Accent subtle | `--color-accent-subtle` | `bg-accent-subtle` |

#### Typography

| Purpose | Token | Tailwind |
|---------|-------|----------|
| Body font | `--font-body` | `font-body` |
| Headings | `--font-heading` | `font-heading` |
| Code | `--font-mono` | `font-mono` |

#### Spacing

| Size | Token | Usage |
|------|-------|-------|
| xs | `--space-xs` | Tight gaps, inline |
| sm | `--space-sm` | Component padding |
| md | `--space-md` | Default padding |
| lg | `--space-lg` | Section padding |
| xl | `--space-xl` | Major breaks |
| 2xl | `--space-2xl` | Hero/dramatic |

#### Container Widths

| Purpose | Token | Value |
|---------|-------|-------|
| Prose | `--container-prose` | 65ch |
| Narrow | `--container-narrow` | 42rem |
| Normal | `--container-normal` | 52rem |
| Wide | `--container-wide` | 64rem |
| Full | `--container-full` | 80rem |

#### Effects

| Purpose | Token |
|---------|-------|
| Subtle shadow | `--shadow-sm` |
| Standard shadow | `--shadow-md` |
| Prominent shadow | `--shadow-lg` |
| Subtle radius | `--radius-sm` |
| Standard radius | `--radius-md` |
| Prominent radius | `--radius-lg` |
| Fast transition | `--duration-fast` |
| Normal transition | `--duration-normal` |
| Slow transition | `--duration-slow` |
| Blur (xs-3xl) | `--blur-xs` through `--blur-3xl` |

---

### Layout Patterns

#### Page Structure

```astro
<body class="min-h-screen flex flex-col bg-background text-text-primary font-body antialiased">
  <Header />
  <main class="flex-1 w-full">
    <!-- Content -->
  </main>
  <Footer />
</body>
```

#### Prose Container (Blog Posts)

```astro
<div class="max-w-[68ch] mx-auto px-6">
  <div class="prose">
    <slot />
  </div>
</div>
```

#### Wide Container (Grids, Cards)

```astro
<div class="max-w-6xl mx-auto px-6">
  <!-- Grid layouts -->
</div>
```

#### Hero Section

```astro
<section class="py-section">
  <h1 class="font-heading text-5xl md:text-6xl leading-tight tracking-tight balance-text">
    Main Heading
    <span class="text-accent">Accent Part</span>
  </h1>
  <p class="text-text-secondary text-lg mt-6">
    Subheading
  </p>
</section>
```

#### Card Pattern

```astro
<article class="bg-surface border-l-3 border-accent p-lg rounded-md">
  <h3 class="font-heading text-2xl text-accent mb-2">
    <a href={url} class="hover:text-accent-hover transition-colors duration-normal">
      {title}
    </a>
  </h3>
  <p class="text-text-secondary leading-relaxed">{description}</p>
  <time class="font-mono text-xs text-text-muted uppercase tracking-wide">{date}</time>
</article>
```

---

### Interactive States

Every interactive element needs three states:

```css
.interactive {
  color: var(--color-accent);
  transition: color var(--duration-fast) var(--easing);
}

.interactive:hover {
  color: var(--color-accent-hover);
}

.interactive:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

---

### Responsive Design

#### Breakpoints

| Prefix | Min Width |
|--------|-----------|
| `sm:` | 640px |
| `md:` | 768px |
| `lg:` | 1024px |
| `xl:` | 1280px |

#### Mobile-First Pattern

```astro
<h1 class="text-3xl md:text-5xl lg:text-6xl">
  Responsive Heading
</h1>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Cards -->
</div>
```

---

### Accessibility Requirements

| Requirement | Standard |
|-------------|----------|
| `text-primary` on `background` | 7:1 (WCAG AAA) |
| `text-secondary` on `background` | 4.5:1 (WCAG AA) |
| `accent` on `background` | 4.5:1 for text |
| Focus indicators | Visible on all interactive elements |
| Semantic HTML | Proper heading hierarchy, landmarks |

---

### File Locations

| Purpose | Path |
|---------|------|
| Token definitions | `design-system/tokens.css` |
| Theme values | `design-system/all-themes.css` |
| Schema docs | `design-system/SCHEMA.md` |
| Global styles | `src/styles/global.css` |
| Layouts | `src/layouts/*.astro` |
| Components | `src/components/*.astro` |
| Design philosophy | `DESIGN.md` |

---

## Part III: Process

### Creating New Components

1. **Define the vision** - What's the aesthetic direction?
2. **Identify tokens** - Map design decisions to semantic tokens
3. **Check existing patterns** - Reuse before creating
4. **Implement with precision** - Execute the vision completely
5. **Include all states** - Default, hover, focus, disabled
6. **Verify visually** - Use **design-loop** skill for iterative fine-tuning

### Component Template

```astro
---
interface Props {
  variant?: 'default' | 'accent';
  class?: string;
}

const { variant = 'default', class: className } = Astro.props;

const variants = {
  default: 'bg-surface text-text-primary border-border',
  accent: 'bg-accent-subtle text-accent border-accent',
};
---

<div class:list={[
  'rounded-md border p-md transition-colors duration-normal',
  variants[variant],
  className
]}>
  <slot />
</div>
```

---

## The Standard

**Match implementation complexity to aesthetic vision:**
- Maximalist designs need elaborate code, extensive animations, rich effects
- Minimalist designs need restraint, precision, obsessive attention to spacing and typography
- Elegance comes from executing the vision completely, not from the vision itself

**The question to ask:** Is this design **distinctive**? Would someone remember it? Does it have a clear point of view?

Generic is the enemy. Safe is forgettable. Commit to a direction and execute with conviction.

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **design-loop** | Iterative fine-tuning or nuclear redesign with visual verification |
| **screenshot** | One-off captures for verification or documentation |

---

*Claude is capable of extraordinary creative work. Don't hold back.*
