# Core Craft Principles

These apply regardless of brand direction. This is the quality floor for landing pages.

---

## The Anti-Template Mindset

Before looking at any pattern, internalize this: **if another AI could produce the same output, you've failed.**

Landing pages reward boldness. Dashboards reward consistency. A dashboard that surprises is confusing. A landing page that doesn't surprise is forgettable.

---

## Typography as Personality

Typography isn't holding your content — it IS your content. The personality of letters shapes how the product feels before anyone reads a word.

### Display Typography

Headlines need drama. Not just "big" — dramatic:

```jsx
// Hero headline — massive, commanding, tight
className="text-[clamp(3rem,8vw,6rem)] font-display font-black tracking-tight leading-[0.9]"

// Display — section headers with presence
className="text-[clamp(2rem,5vw,4rem)] font-display font-bold tracking-tight leading-[1.1]"

// Subheadline — supporting but still bold
className="text-[clamp(1.25rem,3vw,1.75rem)] font-display font-semibold"
```

### Body Typography

Body text needs readability and personality:

```jsx
// Lead paragraph — larger, comfortable
className="text-lg md:text-xl text-ink-muted leading-relaxed max-w-2xl"

// Body — readable baseline
className="text-base text-ink-muted leading-relaxed"

// Small/metadata
className="text-sm text-ink-muted"
```

### Font Pairing

Choose fonts with intention:

**Display fonts** — Personality carriers. Should feel ownable. Examples:
- Clash Display (geometric, modern)
- Cabinet Grotesk (humanist, warm)
- Satoshi (clean, contemporary)
- Space Grotesk (technical, precise)

**Body fonts** — Readability with character. Examples:
- Inter (neutral, reliable)
- Plus Jakarta Sans (friendly, modern)
- DM Sans (geometric, clean)

**The test:** If you're using Inter for headlines, you're not designing.

---

## Color as Emotion

Color isn't decoration — it's emotion. Every color choice should be explainable.

### Brand Color Architecture

```css
:root {
  /* Brand — the dominant personality */
  --brand: #ff6b35;
  --brand-dark: #e55a2b;
  --brand-light: #ff8f66;

  /* Surface — backgrounds */
  --surface: #ffffff;
  --surface-alt: #fafafa;

  /* Ink — text hierarchy */
  --ink: #0f172a;
  --ink-muted: #64748b;

  /* Accent — secondary emphasis */
  --accent: #00d4aa;
}
```

### Color in Tailwind

```jsx
// Brand as hero element
className="bg-brand text-white"

// Brand as text accent
className="text-brand"

// Surfaces for sections
className="bg-surface"      // Default white
className="bg-surface-alt"  // Slight contrast

// Text hierarchy
className="text-ink"        // Primary, high contrast
className="text-ink-muted"  // Secondary, softer
```

### The One-Color Rule

One dominant brand color that owns the page. One accent that punctuates. Everything else is surface and ink. If you have three "brand" colors competing, nothing is brand.

---

## Spacing for Drama

Landing pages need room to breathe. Generous spacing creates drama.

### Section Spacing

```jsx
// Hero section — maximum breathing room
className="py-24 md:py-32 lg:py-40"

// Standard sections — generous
className="py-20 md:py-28 lg:py-32"

// Compact sections — still spacious
className="py-16 md:py-20 lg:py-24"
```

### Element Spacing

```jsx
// Between major elements
className="space-y-8 md:space-y-12"

// Between related elements
className="space-y-4 md:space-y-6"

// Tight groupings
className="space-y-2"
```

### Container Strategy

```jsx
// Full-width hero
className="w-full px-6 md:px-8"

// Contained content
className="max-w-7xl mx-auto px-6 md:px-8"

// Narrow content (readable width)
className="max-w-3xl mx-auto px-6"

// Extra narrow (focused content)
className="max-w-xl mx-auto px-6"
```

---

## Layout as Tension

Centered everything creates monotony. Create tension through asymmetry.

### Asymmetric Splits

```jsx
// 60/40 split
className="grid grid-cols-1 lg:grid-cols-5 gap-12"
// Content: col-span-3, Image: col-span-2

// 70/30 split
className="grid grid-cols-1 lg:grid-cols-10 gap-12"
// Content: col-span-7, Sidebar: col-span-3

// Offset grid
className="grid grid-cols-12 gap-6"
// Content starts at col-2, spans 8
```

### Breaking the Grid

```jsx
// Full-bleed image breaking container
<div className="max-w-7xl mx-auto px-6">
  <div className="-mx-6 md:-mx-8 lg:-mx-16">
    <img className="w-full" />
  </div>
</div>

// Overlapping elements
className="relative -mt-20 z-10"
```

### Rhythm Through Contrast

Don't repeat the same section layout. Alternate:
- Full-width → Contained
- Left-aligned → Right-aligned
- Image-left → Image-right
- Dense → Spacious

---

## The Signature Element

Every landing page needs ONE unforgettable moment.

### Types of Signatures

**Visual signature:**
- A distinctive illustration style
- An unusual color combination
- A unique gradient or texture

**Typographic signature:**
- An extreme headline treatment
- A distinctive pull quote style
- Animated text reveals

**Interactive signature:**
- A magnetic button effect
- A cursor-following element
- A scroll-triggered transformation

**Structural signature:**
- An unexpected section shape
- Overlapping content layers
- A non-linear scroll experience

### Signature Placement

The signature should appear:
- Once prominently (hero or key moment)
- Echoed subtly (supporting elements)
- Never repeated to exhaustion

---

## Animation with Purpose

Motion should reveal, not decorate.

### Entrance Animations

```jsx
// Framer Motion — fade up
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}

// Staggered children
variants={{
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}}
```

### Scroll-Triggered Reveals

```jsx
// Reveal when in view
whileInView={{ opacity: 1, y: 0 }}
initial={{ opacity: 0, y: 30 }}
viewport={{ once: true, margin: "-100px" }}
transition={{ duration: 0.6 }}
```

### Hover States

```jsx
// Subtle scale
className="transition-transform duration-200 hover:scale-105"

// Color shift
className="transition-colors duration-200 hover:bg-brand-dark"

// Lift effect
className="transition-all duration-200 hover:-translate-y-1 hover:shadow-lg"
```

### Animation Rules

1. **Once, not loop** — Reveals happen once per session
2. **Fast, not slow** — 200-600ms, never longer
3. **Ease out** — Natural deceleration
4. **Purpose** — Every animation should answer "why does this move?"

---

## CTA Craft

The CTA isn't just a button — it's the entire reason this page exists.

### Primary CTA

```jsx
<button className="
  inline-flex items-center justify-center
  px-8 py-4
  bg-brand hover:bg-brand-dark
  text-white font-semibold
  rounded-full
  transition-all duration-200
  hover:scale-105 hover:shadow-lg
">
  Start free trial
</button>
```

### CTA Hierarchy

```jsx
// Primary — the ONE action
className="bg-brand text-white px-8 py-4 font-semibold"

// Secondary — alternative path
className="border border-edge text-ink px-6 py-3 font-medium"

// Tertiary — low commitment
className="text-brand underline-offset-4 hover:underline"
```

### CTA Placement

- Hero: Always present, prominently
- After each value section: Reinforce
- Sticky/floating: For long pages
- Final: Strong close

---

## Avoid

These are the clearest signs of AI-generated landing pages:

- **Purple-to-blue gradients** — `from-purple-500 to-blue-600`
- **Floating blobs** — Abstract decorative shapes
- **Inter for headlines** — No personality
- **Centered everything** — No tension
- **Feature grids with icons** — Generic and forgettable
- **Gray backgrounds everywhere** — Safe, not bold
- **Same section rhythm** — Predictable is forgettable
- **"Clean and modern"** — Means nothing
- **Multiple competing CTAs** — Confuses the one action
- **Stock illustrations** — Screams template

---

## The Craft Checks

Before presenting work, run these:

1. **Squint test:** Blur your eyes. Is there clear hierarchy? Is anything jarring?

2. **Swap test:** If you swapped your type/color/layout for defaults, would it feel different?

3. **Signature test:** Can you point to the one unforgettable element?

4. **Generic test:** Remove the logo. Could this be any company's page?

5. **Scroll test:** Is there a reason to keep scrolling beyond "more content"?

If any check fails, iterate before showing.
