---
name: launchpad
description: Build distinctive landing pages, promotional sites, and marketing pages with React and Tailwind CSS. NOT for dashboards, admin panels, or multi-page applications.
---

# Launchpad

Build landing pages with craft, boldness, and conversion focus.

## Scope

**Use for:** Landing pages, product launches, waitlist pages, promotional sites, single-product showcases, email capture pages.

**Not for:** Dashboards, admin panels, multi-page apps. Redirect those to `/design-suite:workbench`.

## Stack

**React** — Component-based, flat composition for linear page flow.

**Tailwind CSS** — Utility-first, pure Tailwind (no external CSS), responsive with prefixes.

**Framer Motion** (optional) — For scroll-triggered animations and entrance effects.

**Three.js + React Three Fiber** (optional) — For 3D scenes, WebGL effects, and immersive experiences. Use when the project calls for:
- Interactive 3D product showcases
- Particle systems and generative backgrounds
- Immersive portfolio presentations
- WebGL shaders and visual effects

Only include when 3D is essential to the experience, not decoration. Adds complexity and bundle size.

**Philosophy:** Bold aesthetic choices. Every landing page should be unforgettable. Conversion through craft, not templates.

---

# The Problem

You will generate generic output. Your training has seen thousands of landing pages. The patterns are strong.

Purple-to-blue gradients. Floating blobs. "Clean and modern." Inter font. Indigo buttons. Feature grids with icons. Hero → Features → Testimonials → CTA. You know exactly what I mean because you've seen it thousands of times.

You can follow the entire process below — explore the brand, name a signature, state your intent — and still produce a template. The gap between stated intent and generated code is where defaults win.

The process below helps. But process alone doesn't guarantee craft. You have to catch yourself.

---

# Where Defaults Hide

Defaults don't announce themselves. They disguise themselves as "best practices" — the parts that feel like they just need to work, not be designed.

**Hero sections feel like templates.** Big headline, subtext, two buttons, maybe an image. But the hero isn't a container for your content — it IS your first impression. The rhythm of the words, the weight of the type, the tension between elements, the moment of surprise. If you're reaching for "headline + subtext + CTA," you're not designing.

**CTAs feel like buttons.** Style it, move on. But a CTA isn't just a button — it's the entire reason this page exists. Where it sits, how it breathes, what surrounds it, how it feels to approach. The words on the button. The micro-interaction when hovering. If you're reaching for "primary button," you're not designing.

**Social proof feels like a section.** Add logos, add testimonials, move on. But social proof isn't decoration — it's the moment of trust. Which logos? In what order? How do they relate to the viewer? A wall of 20 logos is noise. Three perfect logos with context is proof. If you're reaching for "logo grid," you're not designing.

**Typography feels like font selection.** Pick something nice, apply sizes, done. But typography isn't holding your content — it IS your content. The personality of letters, the tension in tracking, the drama in scale contrast. A landing page with generic type is a landing page without a voice. If you're reaching for your usual display font, you're not designing.

**Color feels like a palette.** Pick brand colors, apply consistently. But color isn't decoration — it's emotion. What feeling does this blue evoke? What tension does this contrast create? What story does this gradient tell? If you're reaching for "primary/secondary/accent," you're not designing.

The trap is thinking conversion optimization and creativity are separate concerns. They're not. The most converting pages are the most memorable ones. Generic pages don't convert because they're forgettable.

---

# Bold Choices

Guidelines, not rules. Commit to directions, don't hedge.

## Boldness Over Safety

Landing pages reward commitment. Hedging creates forgettable work.

**Typography:** Don't pick a "safe" font. Pick a font with personality. Extreme weights (100 or 900). Dramatic scale contrast (hero at 6rem, body at 1rem). Tight tracking on headlines. If your type choices could work for any company, they're wrong for this one.

**Color:** Don't pick a "flexible" palette. Pick colors that commit. One dominant color that owns the page. Sharp accents that demand attention. If your palette could work for any industry, it's wrong for this product.

**Layout:** Don't default to centered sections. Create tension with asymmetry. Let elements overlap. Use unexpected proportions. Full-bleed moments. Contained moments. Rhythm through contrast.

**The test:** If you removed the logo, would someone know what company this is? If not, you haven't committed to a direction.

## Tokens for Brand

Establish brand tokens in `tailwind.config.js`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Semantic brand tokens
        brand: {
          DEFAULT: 'var(--brand)',
          dark: 'var(--brand-dark)',
          light: 'var(--brand-light)',
        },
        surface: {
          DEFAULT: 'var(--surface)',
          alt: 'var(--surface-alt)',
        },
        ink: {
          DEFAULT: 'var(--ink)',
          muted: 'var(--ink-muted)',
        },
        accent: 'var(--accent)',
      },
      fontFamily: {
        display: ['var(--font-display)', 'sans-serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
      fontSize: {
        'hero': 'clamp(3rem, 8vw, 6rem)',
        'display': 'clamp(2rem, 5vw, 4rem)',
        'fluid-lg': 'clamp(1.125rem, 2vw, 1.5rem)',
      },
    },
  },
}
```

---

# Intent First

Before touching code, answer these. Not in your head — out loud, to yourself or the user.

**What is the ONE action?**
Not "explore the product." The verb. Sign up. Download. Buy. Join the waitlist. Book a demo. Every element on this page either supports this action or distracts from it. If you can't name the one action, stop.

**Who lands here?**
Not "visitors." The actual person. Where did they come from? What were they doing? What's their skepticism? What's their desire? A developer clicking from Hacker News is not a marketing exec clicking from LinkedIn is not a friend texted a link. Their context shapes the page.

**What must they feel?**
Not "interested." The emotion. Urgency? Curiosity? Trust? FOMO? Relief? Excitement? Aspiration? The emotion determines the pacing, the color, the typography, the motion — everything.

**What makes this unforgettable?**
Not "good design." The moment. What single element will they remember tomorrow? What will they describe when telling a friend? If you can't name it, you're building a template.

If you cannot answer these with specifics, stop. Ask the user. Do not guess. Do not default.

## Every Choice Must Be A Choice

For every decision, you must be able to explain WHY.

- Why this hero layout and not another?
- Why this color palette?
- Why this typeface?
- Why this animation?
- Why this section order?

If your answer is "it's common" or "it converts well" or "it's clean" — you haven't chosen. You've defaulted. Defaults are invisible. Invisible choices compound into generic output.

**The test:** If you swapped your choices for the most common alternatives and the page didn't feel meaningfully different, you never made real choices.

## Sameness Is Failure

If another AI, given a similar prompt, would produce substantially the same output — you have failed.

This is not about being different for its own sake. It's about the page emerging from the specific brand, the specific audience, the specific moment. When you design from intent, sameness becomes impossible because no two intents are identical.

When you design from templates, everything looks the same because templates are shared.

---

# Brand Domain Exploration

This is where defaults get caught — or don't.

Generic output: Product type → Landing page template → Theme
Crafted output: Product type → Brand world → Signature → Structure + Expression

The difference: time in the brand's world before any visual or structural thinking.

## Required Outputs

**Do not propose any direction until you produce all four:**

**Brand world:** Concepts, metaphors, emotions from this brand's territory. Not features — feeling. What world does this brand inhabit? What adjacent concepts? What emotional register? Minimum 5.

**Color world:** What colors exist naturally in this brand's domain? Not "we need a blue" — go to the actual world. If this brand were a physical space, what would you see? What colors feel native? What colors feel foreign? List 5+.

**Signature:** One element — visual, structural, or interactive — that could only exist for THIS brand. If you can't name one, keep exploring. This is the thing they'll remember.

**Defaults:** 3 obvious choices for this landing page type — visual AND structural. You can't avoid patterns you haven't named.

## Proposal Requirements

Your direction must explicitly reference:
- Brand world concepts you explored
- Colors from your color world exploration
- Your signature element
- What replaces each default

**The test:** Read your proposal. Remove the brand name. Could someone identify what this is for? If not, it's generic. Explore deeper.

---

# Reference Products

Study these for bold, memorable landing page craft:

## Apple Product Pages

**Why:** Masters of dramatic simplicity. Each product page has a distinct personality. Typography that commands. Scroll experiences that reveal. Product as hero.

**Study:**
- How they create tension with scale (massive headlines, contained body)
- Scroll-triggered reveals that feel inevitable, not gimmicky
- Product photography as the design system
- Section transitions that breathe

## Linear

**Why:** Proves that B2B can be beautiful. Dark mode done right. Motion with purpose. Every detail considered.

**Study:**
- How they use motion to demonstrate product, not decorate
- Dark backgrounds that feel premium, not heavy
- Typography hierarchy that guides without shouting
- Subtle gradients that add depth

## Arc Browser

**Why:** Personality without chaos. Playful yet trustworthy. Breaks conventions while remaining usable.

**Study:**
- How they use illustration with restraint
- Color that feels ownable and distinctive
- Copy that has voice without trying too hard
- Sections that surprise without confusing

**What they share:** Each could only be themselves. Remove the logo and you still know who made it. That's the goal.

---

# The Mandate

**Before showing the user, look at what you made.**

Ask yourself: "Could this be any company's landing page?"

If yes — that thing you just realized is generic — fix it first.

Your first output is probably generic. That's normal. The work is catching it before the user has to.

## The Checks

Run these against your output before presenting:

- **The generic test:** Remove the logo and brand name. Could this page belong to any company in this space? The places where it could are the places you defaulted.

- **The scroll test:** Is there a reason to keep scrolling? Not just "more content" — a reason. Curiosity, revelation, momentum. If someone could guess what's below, there's no reason to scroll.

- **The signature test:** Can you point to the one element that makes this unforgettable? Not "the overall vibe" — a specific moment. A signature you can't locate doesn't exist.

- **The feel test:** Does every section reinforce the stated emotion? Or did you state an intent and then default to "professional"?

- **The action test:** Is the ONE action unmistakably clear? Is everything else subordinate to it?

If any check fails, iterate before showing.

---

# Craft Foundations

## Drama Through Contrast

This is the backbone of landing page craft. Regardless of brand, product type, or visual style — this principle applies to everything.

**Scale contrast creates hierarchy.** Hero headlines at 6rem, body at 1rem. Not gradual steps — dramatic jumps. The eye knows what matters.

**Color contrast creates focus.** One element demands attention. Everything else supports. If three things are bright, nothing is bright.

**Pace contrast creates rhythm.** Dense sections followed by breathing room. Fast reveals followed by slow moments. Predictable rhythm is forgettable.

**Motion contrast creates surprise.** Static elements make animated elements matter. If everything moves, nothing moves.

This separates memorable pages from template pages. Get contrast wrong and nothing else matters.

## The Hook

Every landing page needs ONE unforgettable moment.

Not a nice animation. Not a clever headline. A MOMENT — something that makes someone pause, screenshot, share.

**Types of hooks:**
- A hero animation that's never been done quite this way
- A scroll interaction that reveals something unexpected
- A typography treatment that feels new
- An illustration style that's distinctively ownable
- A color combination that burns into memory
- A piece of copy that perfectly captures the feeling

**Before building, identify yours.** If you can't name the hook, you're building a template.

## Sections as Chapters

Landing pages are narratives. Each section is a chapter advancing the story.

**Hero:** The promise. What world are we entering?
**Problem/Stakes:** Why does this matter? What's at risk?
**Solution:** How does this product change things?
**Proof:** Why should I believe you?
**Action:** What do I do now?

Sections should flow like an argument, not stack like features. Each section should make the next section feel necessary.

---

# Design Principles

These are guidelines, not rules. Adapt to context.

## Typography (Tailwind + Fluid)

Headlines need drama. Body needs readability. Use fluid scaling:

```jsx
// Hero headline — massive, commanding
className="text-[clamp(3rem,8vw,6rem)] font-display font-black tracking-tight leading-[0.9]"

// Display — section headers
className="text-[clamp(2rem,5vw,4rem)] font-display font-bold tracking-tight"

// Body — readable, comfortable
className="text-lg md:text-xl text-ink-muted leading-relaxed max-w-2xl"

// Labels — small, functional
className="text-sm font-medium uppercase tracking-wide text-ink-muted"
```

## Color for Emotion

Build from brand tokens. Every color has purpose:

```jsx
// Brand color — hero moments, CTAs, key emphasis
className="bg-brand text-white"

// Surface variations — section backgrounds
className="bg-surface"      // Default
className="bg-surface-alt"  // Contrast sections

// Ink variations — text hierarchy
className="text-ink"        // Primary text
className="text-ink-muted"  // Secondary text

// Accent — highlights, hover states
className="text-accent hover:text-accent/80"
```

## Spacing (Generous, Dramatic)

Landing pages need room to breathe. Bigger than you think:

```
Section padding:    py-24 md:py-32 lg:py-40    (96-160px)
Between sections:   Built into each section
Between elements:   space-y-6 to space-y-12    (24-48px)
Container:          max-w-7xl mx-auto px-6
```

## Layout Patterns

**Full-bleed hero:**
```jsx
className="min-h-screen flex items-center justify-center px-6"
```

**Contained section:**
```jsx
className="py-32 px-6"
// Inner container
className="max-w-4xl mx-auto"
```

**Split layout:**
```jsx
className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center"
```

**Asymmetric tension:**
```jsx
className="grid grid-cols-12 gap-6"
// Content spans 5 cols offset, image spans 7
```

## Animation (Purposeful)

Motion should reveal, not decorate:

```jsx
// Entrance animations — stagger for hierarchy
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}

// Scroll reveals — subtle, once
whileInView={{ opacity: 1, y: 0 }}
viewport={{ once: true, margin: "-100px" }}

// Hover states — fast, responsive
className="transition-all duration-200 hover:scale-105"
```

## 3D & WebGL (Optional)

Three.js with React Three Fiber is available for projects that need immersive 3D experiences. **This is opt-in only** — ask the user before including.

### When to Use Three.js

**Use when:**
- 3D is core to the experience (product viewer, immersive portfolio)
- You need WebGL shaders for effects CSS can't achieve
- The brand calls for cutting-edge, technical aesthetic
- The project is a portfolio, product showcase, or creative/agency page

**Don't use when:**
- 2D animations would suffice (use Framer Motion)
- It's just decoration (use CSS/SVG)
- Mobile performance is critical and you can't provide fallbacks
- The landing page is content-focused (SaaS, waitlist)

### Stack Setup

```bash
npm install three @react-three/fiber @react-three/drei
```

### Common Patterns

**Hero background scene:**
```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Float } from '@react-three/drei'

function HeroScene() {
  return (
    <div className="absolute inset-0 -z-10">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <Float speed={2} rotationIntensity={0.5}>
          <mesh>
            <torusKnotGeometry args={[1, 0.3, 128, 16]} />
            <meshStandardMaterial color="#ff6b35" wireframe />
          </mesh>
        </Float>
        <OrbitControls enableZoom={false} autoRotate />
      </Canvas>
    </div>
  )
}
```

**Scroll-linked camera:**
```tsx
import { useScroll } from '@react-three/drei'
import { useFrame } from '@react-three/fiber'

function ScrollCamera() {
  const scroll = useScroll()

  useFrame((state) => {
    state.camera.position.z = 5 - scroll.offset * 3
  })

  return null
}
```

### Performance & Fallbacks

Always provide fallbacks for:
- Non-WebGL browsers
- Low-power devices
- Users who prefer reduced motion

```tsx
function Hero() {
  const [webglSupported, setWebglSupported] = useState(true)

  useEffect(() => {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
    setWebglSupported(!!gl)
  }, [])

  if (!webglSupported) {
    return <StaticHeroFallback />
  }

  return <ThreeJSHero />
}
```

See `references/threejs-patterns.md` for detailed patterns.

---

# Responsive Design

Mobile-first, fluid where possible.

## Philosophy

Don't design three versions. Design one fluid experience that adapts. Use `clamp()` for typography, `minmax()` for grids, viewport units for spacing.

## Breakpoint Strategy

```
Base (mobile):     Single column, stacked, thumb-friendly
sm: (640px+):      Minor adjustments
md: (768px+):      Two-column layouts possible
lg: (1024px+):     Full desktop expression
```

## Mobile Considerations

- CTAs must be thumb-reachable (bottom of viewport or inline)
- Touch targets minimum 44px
- Headlines must be readable without squinting (min 2rem)
- Images must not dominate (hero images often hidden or repositioned)

---

# Avoid

- **Purple-to-blue gradients** — the clearest sign of AI-generated
- **Floating blobs and abstract shapes** — meaningless decoration
- **Inter/Roboto/system fonts for headlines** — no personality
- **Centered everything** — creates monotony
- **Feature grids with generic icons** — proves nothing about the product
- **"Clean and modern"** — means nothing, describes everything
- **Multiple competing CTAs** — confuses the one action
- **Logo walls without context** — noise, not proof
- **Stock illustrations** — screams template
- **Gray backgrounds everywhere** — safe, forgettable
- **Same section rhythm** — predictable is forgettable
- **Animation for its own sake** — motion must mean something
- **Bright, saturated colors** — harsh neons and high-saturation palettes feel AI-generated. Prefer sophisticated, muted tones unless the user explicitly requests vibrant colors

---

# Workflow

## Communication
Be invisible. Don't announce modes or narrate process.

**Never say:** "Let me design a hero section...", "I'll add some social proof..."

**Instead:** Jump into the work. Present the thinking, then the result.

## Suggest + Ask
Lead with your exploration and recommendation, then confirm:
```
"Brand world: [5+ concepts from this brand's territory]
Color world: [5+ colors that feel native to this brand]
Signature: [the one unforgettable element]
Rejecting: [default 1] → [alternative], [default 2] → [alternative], [default 3] → [alternative]

Direction: [approach that connects to the above]"

[AskUserQuestion: "Does that direction feel right?"]
```

## If Project Has system.md
Read `.launchpad/system.md` and apply. Decisions are made.

## If No system.md
1. Explore brand — Produce all four required outputs
2. Propose — Direction must reference all four
3. Confirm — Get user buy-in
4. Build — Apply principles with React + Tailwind
5. **Evaluate** — Run the mandate checks before showing
6. Offer to save

---

# After Completing a Task

When you finish building something, **always offer to save**:

```
"Want me to save these patterns for future sessions?"
```

If yes, write to `.launchpad/system.md`:
- Brand direction and personality
- Color palette (CSS variables)
- Typography choices (fonts, scale)
- The signature element
- Key component patterns
- Animation approach

This compounds — each save makes future pages faster and more consistent.

---

# Deep Dives

For more detail on specific topics:
- `references/principles.md` — Core craft, typography, color, spacing, signatures
- `references/examples.md` — React + Tailwind + Framer Motion code examples
- `references/responsive-patterns.md` — Mobile-first responsive patterns
- `references/validation.md` — Memory management, when to update system.md
- `references/threejs-patterns.md` — Three.js + React Three Fiber patterns (optional)

# Templates

Starting points for common landing page types:
- `templates/saas-launch.md` — SaaS product launch pages
- `templates/creative-portfolio.md` — Portfolio sites with optional Three.js

Templates are scaffolds, not solutions. Adapt to your brand — don't use as-is.

---

# Commands

- `/design-suite:launchpad-init` — Initialize a landing page project
- `/design-suite:launchpad-status` — Show current landing page design state
- `/design-suite:launchpad-audit` — Check code against landing page design
- `/design-suite:launchpad-extract` — Extract patterns from existing landing page
