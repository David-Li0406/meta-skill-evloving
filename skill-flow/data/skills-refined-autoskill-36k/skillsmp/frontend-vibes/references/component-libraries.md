# Component Libraries: Aceternity UI & Magic UI

Curated catalog of modern background effects, animated components, and interaction patterns from Aceternity UI and Magic UI. These components provide production-ready implementations of expressive visual effects that align with the frontend-vibes aesthetic.

## Usage Philosophy

**Don't use all of them.** Select 1-3 contextually appropriate effects per interface. These are accent pieces, not the foundation. Overuse creates visual chaos; strategic use creates memorable moments.

**Integration Pattern:**
1. Choose effects that reinforce your aesthetic direction
2. Use subtle effects (grids, gradients) for foundations
3. Reserve dramatic effects (glowing stars, ripples) for hero sections or key interactions
4. Ensure effects don't interfere with readability or usability

---

## Backgrounds

Textured backgrounds create atmosphere and depth without overwhelming content. Use these instead of solid colors to add warmth and technical character.

### Grid Backgrounds

**Dotted Glow Background**
https://ui.aceternity.com/components/dotted-glow-background

**Description:** Subtle dot grid with glowing accent points that pulse gently. Creates technical blueprint aesthetic without being distracting.

**When to Use:**
- Hero sections for technical products
- Dashboard backgrounds (lower opacity)
- Documentation pages
- Developer tool interfaces

**Integration Tips:**
- Set opacity to 0.3-0.5 for subtle effect
- Use warm dark background (#131313) behind grid
- Accent dots should match your primary accent color (orange/coral)

**Aesthetic Fit:** ★★★★★ - Perfect technical romance vibe, low cognitive load

---

**Grid and Dot Backgrounds**
https://ui.aceternity.com/components/grid-and-dot-backgrounds

**Description:** Various grid patterns (square grid, dot grid, small dot grid). Clean, technical foundation that references graph paper and technical drawings.

**When to Use:**
- Foundation for entire sections
- Behind content containers
- Portfolio project showcases
- Technical documentation

**Integration Tips:**
- Prefer dot grids over line grids (softer, less geometric)
- Use #1a1a1a for grid color on #131313 background (subtle contrast)
- Combine with glassmorphism cards for layered depth

**Aesthetic Fit:** ★★★★★ - Core aesthetic element, very versatile

---

**Retro Grid**
https://magicui.design/docs/components/retro-grid

**Description:** Perspective grid that recedes into distance, like 1980s computer graphics or Tron aesthetic. Strong retrofuture vibe.

**When to Use:**
- Hero sections for creative/design work
- Landing pages with dramatic flair
- AI/LLM product pages
- Game or entertainment interfaces

**Integration Tips:**
- Use sparingly (one per page maximum)
- Pair with neon accents (cyan, magenta, electric green)
- Works best full-bleed at top of page
- Reduce opacity (0.4-0.6) if placing content over it

**Aesthetic Fit:** ★★★★☆ - Strong aesthetic but can overpower if misused

---

**Flickering Grid**
https://magicui.design/docs/components/flickering-grid

**Description:** Grid with randomized cell animations that flicker on and off. Suggests data transmission, matrix code, or system activity.

**When to Use:**
- Loading states or transitions
- System status dashboards
- AI processing visualizations
- "Live" data displays

**Integration Tips:**
- Use as temporary state (during loading), not permanent background
- Flicker rate should be subtle (1-2 cells per second max)
- Combine with status indicators ("Processing...", "Analyzing...")

**Aesthetic Fit:** ★★★★☆ - Great for dynamic contexts, avoid for static content

---

### Ambient Background Effects

**Background Beams**
https://ui.aceternity.com/components/background-beams

**Description:** Animated light beams that sweep across the background. Creates sense of movement and energy without being distracting.

**When to Use:**
- Hero sections
- Feature highlight areas
- Call-to-action sections
- Loading or transitional states

**Integration Tips:**
- Use one beam color matching your accent (orange/coral)
- Slow animation speed (20-30 seconds per sweep)
- Keep opacity low (0.2-0.4) so content remains readable
- Works best on dark backgrounds (#131313)

**Aesthetic Fit:** ★★★★☆ - Adds energy, but can feel busy

---

**Glowing Stars Effect**
https://ui.aceternity.com/components/glowing-stars-effect

**Description:** Particle field of glowing points that drift and pulse. Creates ethereal, space-like atmosphere.

**When to Use:**
- Creative portfolio hero sections
- Inspirational or aspirational content
- AI/ML product pages (suggests neural networks)
- About/mission pages

**Integration Tips:**
- Use warm colors (amber, orange) not cold blue
- Low density (30-50 particles) to avoid overcrowding
- Subtle glow radius (2-4px) for sophistication
- Slow drift speed for calm aesthetic

**Aesthetic Fit:** ★★★☆☆ - Beautiful but can feel decorative rather than purposeful

---

**Background Ripple Effect**
https://ui.aceternity.com/components/background-ripple-effect

**Description:** Concentric ripples emanate from a point, like water droplets. Creates organic, fluid motion.

**When to Use:**
- Interactive hover states (ripple from cursor)
- Attention-drawing moments (feature announcements)
- Loading states with purpose
- Contact/interaction sections

**Integration Tips:**
- Trigger on user interaction, not continuous
- Use as accent effect, not persistent background
- Ripple color should match accent palette
- Keep animation duration short (1-2 seconds)

**Aesthetic Fit:** ★★★☆☆ - Organic feel may conflict with technical aesthetic

---

**Background Boxes**
https://ui.aceternity.com/components/background-boxes

**Description:** Grid of 3D boxes that shift and rotate, creating depth and dimensionality.

**When to Use:**
- Hero sections for 3D/spatial products
- Architecture or design portfolios
- Technical showcases
- Sections emphasizing structure or organization

**Integration Tips:**
- Keep box count low (8x8 grid maximum)
- Use subtle rotation angles (5-10 degrees)
- Warm color palette (#d97757 accents on #131313)
- Consider performance impact on mobile

**Aesthetic Fit:** ★★★☆☆ - Interesting depth but potentially heavy

---

**Light Rays**
https://magicui.design/docs/components/light-rays

**Description:** Radiating light beams from center or edge, suggesting illumination or energy source.

**When to Use:**
- Hero sections with central focal point
- "Illumination" or "insight" themed content
- Product spotlight sections
- Behind logo or key visual element

**Integration Tips:**
- Position rays behind main content (z-index layering)
- Use warm colors (amber, coral) for welcoming feel
- Subtle opacity (0.1-0.3) to avoid overpowering
- Static rays often better than animated for this aesthetic

**Aesthetic Fit:** ★★★☆☆ - Can feel decorative, use purposefully

---

**Warp Background**
https://magicui.design/docs/components/warp-background

**Description:** Distorted grid or mesh that warps and bends, suggesting speed or dimensional travel.

**When to Use:**
- Loading transitions between pages
- Speed/performance-themed sections
- Futuristic product launches
- Technical showcases emphasizing power

**Integration Tips:**
- Use as transition effect, not persistent state
- Pair with motion blur for speed feeling
- Keep duration short (1-2 seconds)
- Warm color palette to maintain aesthetic cohesion

**Aesthetic Fit:** ★★★☆☆ - Strong visual but potentially gimmicky

---

## Borders & Container Effects

Subtle enhancements for cards, buttons, and containers that add technical sophistication without overwhelming.

**Border Beam**
https://magicui.design/docs/components/border-beam

**Description:** Animated light beam that travels around element border. Suggests active status or scanning.

**When to Use:**
- Active cards or selected states
- Featured product cards
- Call-to-action buttons (on hover)
- System status indicators ("Live", "Active")

**Integration Tips:**
- Use sparingly (1-2 elements per view)
- Match beam color to accent palette (orange/coral)
- Slow animation speed (3-5 seconds per loop)
- Combine with subtle scale transform on hover

**Aesthetic Fit:** ★★★★★ - Technical aesthetic, purposeful animation

---

**Glowing Effect**
https://ui.aceternity.com/components/glowing-effect

**Description:** Soft glow emanates from element edges. Creates premium, highlighted appearance.

**When to Use:**
- Primary CTAs
- Featured content cards
- Navigation active states
- Important status indicators

**Integration Tips:**
- Glow color should match accent (orange/coral for warmth)
- Subtle blur radius (4-8px)
- Animate glow intensity on hover (increase 20-30%)
- Combine with warm background for cohesion

**Aesthetic Fit:** ★★★★★ - Premium feel, aligns perfectly with aesthetic

---

**Hover Border Gradient**
https://ui.aceternity.com/components/hover-border-gradient

**Description:** Border color transitions through gradient on hover, suggesting interactivity.

**When to Use:**
- Interactive cards
- Navigation items
- Form inputs on focus
- Buttons in secondary hierarchy

**Integration Tips:**
- Use warm gradient (orange → coral → amber)
- Transition duration 200-300ms
- Combine with subtle scale (1.02) for depth
- Ensure gradient doesn't clash with content

**Aesthetic Fit:** ★★★★☆ - Nice interaction, but avoid overuse

---

**Shine Border**
https://magicui.design/docs/components/shine-border

**Description:** Reflective shimmer passes across border, like light catching metal edge.

**When to Use:**
- Premium product cards
- Special announcements or badges
- Awards or achievement displays
- Limited-time offers or featured items

**Integration Tips:**
- Trigger on hover or scroll into view, not constant
- Use warm metallic colors (gold, copper, bronze)
- Short animation duration (1-2 seconds)
- Pair with high-contrast backgrounds

**Aesthetic Fit:** ★★★☆☆ - Premium but can feel excessive

---

**Magic Card**
https://magicui.design/docs/components/magic-card

**Description:** Card with holographic or iridescent effect on hover, creating depth and interactivity.

**When to Use:**
- Portfolio project showcases
- Feature comparison cards
- Product tier selections
- Creative work galleries

**Integration Tips:**
- Use on cards with significant content (not empty decoration)
- Warm iridescent palette (orange/coral/amber shifts)
- Subtle effect intensity (don't overwhelm content)
- Ensure text remains readable during animation

**Aesthetic Fit:** ★★★☆☆ - Creative but potentially distracting

---

## Text Animation

Dynamic typography effects that create memorable moments without sacrificing readability.

**Text Generate Effect**
https://ui.aceternity.com/components/text-generate-effect

**Description:** Text appears character-by-character or word-by-word with animation, like typing or decoding.

**When to Use:**
- Hero headlines on page load
- Key messages or statements
- Loading states with context ("Analyzing your data...")
- Reveal moments for important information

**Integration Tips:**
- Use for 1-2 key headlines per page maximum
- Stagger word appearance (50-100ms delay between words)
- Pair with spring animation (slight bounce on each word)
- Ensure final state is perfectly readable

**Aesthetic Fit:** ★★★★★ - Terminal/command-line aesthetic, perfect fit

---

**Typewriter Effect**
https://ui.aceternity.com/components/typewriter-effect

**Description:** Classic typewriter animation with cursor, suggesting live typing or code output.

**When to Use:**
- Developer tool interfaces
- Command-line themed sections
- Code examples or terminal output
- AI/chatbot response displays

**Integration Tips:**
- Use monospace font for authenticity
- Include blinking cursor (use CSS animation)
- Typing speed: 50-80ms per character
- Consider sound effects for enhanced feedback (optional)

**Aesthetic Fit:** ★★★★★ - Perfect technical romance aesthetic

---

**Aurora Text**
https://magicui.design/docs/components/aurora-text

**Description:** Text with shifting, aurora-borealis-like color gradient animation.

**When to Use:**
- Hero headlines for creative work
- Brand names or logos
- Special announcements
- Inspirational or mission statements

**Integration Tips:**
- Use warm aurora colors (orange/coral/amber gradients)
- Slow color shift (10-20 second cycles)
- Ensure text remains readable throughout animation
- Use on large display text only (48px+)

**Aesthetic Fit:** ★★★☆☆ - Beautiful but can feel decorative

---

**Hyper Text**
https://magicui.design/docs/components/hyper-text

**Description:** Text with glitch or scramble effect that resolves to final text. Suggests decryption or data processing.

**When to Use:**
- Tech product reveals
- Data transformation visualizations
- AI/ML processing displays
- Cyberpunk or hacker aesthetic contexts

**Integration Tips:**
- Quick scramble duration (500-800ms)
- Use on page load or scroll trigger, not continuous
- Monospace font enhances technical feel
- Pair with dark background for high contrast

**Aesthetic Fit:** ★★★★☆ - Strong technical aesthetic, very on-brand

---

**Highlighter**
https://magicui.design/docs/components/highlighter

**Description:** Background highlight that draws behind text, like a marker highlighting important content.

**When to Use:**
- Key phrases in body text
- Pull quotes or important statements
- Feature callouts
- Annotations or emphasis

**Integration Tips:**
- Use accent color (orange/coral) at 20-30% opacity
- Animate on scroll into view (draw left-to-right)
- Don't overuse (1-3 highlights per section)
- Ensure text contrast remains sufficient

**Aesthetic Fit:** ★★★★☆ - Editorial feel, works well for emphasis

---

**Text Hover Effect**
https://ui.aceternity.com/components/text-hover-effect

**Description:** Text transforms or reveals additional styling on hover, suggesting interactivity.

**When to Use:**
- Navigation links
- Call-to-action text
- Interactive headings
- Links within body content

**Integration Tips:**
- Subtle transform (scale 1.05 or slight color shift)
- Spring animation for organic feel (stiffness: 300, damping: 25)
- Maintain readability throughout animation
- Ensure effect doesn't cause layout shift

**Aesthetic Fit:** ★★★★☆ - Nice interaction, enhances usability

---

**Hero Highlight**
https://ui.aceternity.com/components/hero-highlight

**Description:** Animated spotlight or gradient that draws attention to hero text, creating dramatic focus.

**When to Use:**
- Hero section headlines
- Key value propositions
- Product launch announcements
- Landing page primary messages

**Integration Tips:**
- Use warm gradient (orange → coral)
- Subtle animation on page load (fade in + slight scale)
- Ensure surrounding text doesn't compete for attention
- Keep effect within text bounds (no overflow)

**Aesthetic Fit:** ★★★★☆ - Dramatic but purposeful

---

## Cards & Containers

Interactive card components that create depth and encourage exploration.

**Card Hover Effect**
https://ui.aceternity.com/components/card-hover-effect

**Description:** Card transforms on hover with scale, shadow, or 3D rotation. Suggests interactivity and depth.

**When to Use:**
- Project portfolio grids
- Product feature cards
- Blog post previews
- Service offerings

**Integration Tips:**
- Subtle scale (1.02-1.05) with spring animation
- Increase shadow on hover (y-offset: 8-16px)
- Combine with border glow for premium feel
- Ensure card content remains readable

**Aesthetic Fit:** ★★★★★ - Standard interaction pattern, works everywhere

---

**Focus Cards**
https://ui.aceternity.com/components/focus-cards

**Description:** Card grid where hovered card enlarges while others fade/shrink, creating focus.

**When to Use:**
- Project showcases (3-6 items)
- Feature comparisons
- Team member profiles
- Product variations

**Integration Tips:**
- Works best with 3-4 cards (not too many)
- Use spring animation for smooth focus transition
- Fade non-focused cards to 50-60% opacity
- Ensure adequate spacing for expanded state

**Aesthetic Fit:** ★★★★☆ - Strong interaction but requires space

---

**Expandable Card**
https://ui.aceternity.com/components/expandable-card

**Description:** Card expands to reveal additional content on click or hover. Reduces initial cognitive load.

**When to Use:**
- Case studies or detailed project information
- FAQ sections
- Feature deep-dives
- Product specifications

**Integration Tips:**
- Clear affordance ("+", arrow, or "Learn more" text)
- Smooth spring animation (stiffness: 300, damping: 30)
- Expanded state should feel intentional, not accidental
- Provide way to collapse (click outside or close button)

**Aesthetic Fit:** ★★★★★ - Functional and elegant

---

**Card Stack**
https://ui.aceternity.com/components/card-stack

**Description:** Cards layered in z-space that fan out on interaction, suggesting depth and multiple items.

**When to Use:**
- Testimonials (multiple quotes stacked)
- Image galleries (polaroid stack aesthetic)
- Feature highlights (stacked benefits)
- Content previews (article stacks)

**Integration Tips:**
- Stack 3-5 cards maximum (more feels cluttered)
- Offset each card by 8-16px for depth illusion
- Fan out on hover with spring animation
- Use subtle rotation (2-3 degrees) for organic feel

**Aesthetic Fit:** ★★★★☆ - Creative presentation, works for portfolios

---

**Direction Aware Hover**
https://ui.aceternity.com/components/direction-aware-hover

**Description:** Hover overlay enters from the direction cursor approached, creating spatial awareness.

**When to Use:**
- Image galleries
- Project thumbnails
- Product category cards
- Portfolio grids

**Integration Tips:**
- Use warm overlay color (orange/coral at 80-90% opacity)
- Quick transition (200-300ms) for responsiveness
- Include action text in overlay ("View Project", "Learn More")
- Ensure overlay doesn't obscure important information

**Aesthetic Fit:** ★★★★☆ - Clever interaction, enhances spatial UX

---

**Infinite Moving Cards**
https://ui.aceternity.com/components/infinite-moving-cards

**Description:** Horizontal carousel of cards that auto-scrolls infinitely, suggesting continuous content.

**When to Use:**
- Testimonial rotations
- Partner logos
- Feature highlights
- Social proof displays

**Integration Tips:**
- Slow scroll speed (20-30 seconds per loop)
- Pause on hover for reading
- Duplicate content seamlessly for infinite loop
- Ensure accessible (keyboard navigation, skip option)

**Aesthetic Fit:** ★★★☆☆ - Good for social proof but can feel marketing-heavy

---

## Scroll & Parallax Effects

**Parallax Scroll**
https://ui.aceternity.com/components/parallax-scroll

**Description:** Elements move at different speeds during scroll, creating depth illusion.

**When to Use:**
- Hero sections with layered content
- Visual storytelling sections
- Image showcases
- About/mission pages

**Integration Tips:**
- Subtle speed differences (1.0x foreground, 0.5x background)
- Don't overuse (1 parallax section per page)
- Ensure text remains readable during scroll
- Consider disabling on mobile for performance

**Aesthetic Fit:** ★★★☆☆ - Can feel gimmicky, use purposefully

---

**Tracing Beam**
https://ui.aceternity.com/components/tracing-beam

**Description:** Animated line traces path alongside content as user scrolls, suggesting progress.

**When to Use:**
- Long-form content or articles
- Timeline presentations
- Step-by-step guides
- Process explanations

**Integration Tips:**
- Place beam in left or right margin (not over content)
- Use accent color (orange/coral)
- Beam should progress with scroll position
- Include waypoint markers for milestones

**Aesthetic Fit:** ★★★★★ - Technical aesthetic, excellent for documentation

---

**Hero Parallax**
https://ui.aceternity.com/components/hero-parallax

**Description:** Hero section with layered elements that parallax on scroll, creating cinematic intro.

**When to Use:**
- Landing page hero sections
- Product launch pages
- Portfolio intros
- Marketing campaign pages

**Integration Tips:**
- Limit to top hero section only
- Use warm backgrounds (#131313) for cohesion
- Ensure CTA remains visible and accessible
- Test on mobile (simplify or disable parallax)

**Aesthetic Fit:** ★★★☆☆ - Dramatic but can feel heavy

---

## Forms & Inputs

**Placeholders and Vanish Input**
https://ui.aceternity.com/components/placeholders-and-vanish-input

**Description:** Input placeholder animates out elegantly as user types, reducing visual clutter.

**When to Use:**
- Contact forms
- Search interfaces
- Email subscriptions
- Login/signup forms

**Integration Tips:**
- Placeholder text should be helpful, not decorative
- Smooth fade-out animation (200-300ms)
- Ensure label remains accessible (ARIA labels)
- Use accent color for active/focus state

**Aesthetic Fit:** ★★★★★ - Clean, functional, removes visual noise

---

## Loaders & Transitions

**Multi-Step Loader**
https://ui.aceternity.com/components/multi-step-loader

**Description:** Loading state that shows progress through steps, providing context and reducing perceived wait.

**When to Use:**
- Multi-step processes (file upload, data processing)
- Onboarding flows
- Installation or setup wizards
- AI/ML processing with stages

**Integration Tips:**
- Show current step and total steps ("Step 2 of 4")
- Use descriptive step labels ("Analyzing data...", "Generating report...")
- Progress bar should move smoothly (spring animation)
- Include estimated time if possible

**Aesthetic Fit:** ★★★★★ - Functional and informative, reduces anxiety

---

## Container Components

**Tabs**
https://ui.aceternity.com/components/tabs

**Description:** Tab navigation with animated underline or background indicator.

**When to Use:**
- Content organization (Overview, Features, Pricing)
- Settings panels
- Dashboard views
- Documentation navigation

**Integration Tips:**
- Active indicator should use accent color (orange/coral)
- Spring animation for indicator movement (stiffness: 300, damping: 30)
- Ensure sufficient touch target size (44px minimum height)
- Keyboard accessible (arrow keys navigate)

**Aesthetic Fit:** ★★★★★ - Standard pattern, works everywhere

---

**Sticky Banner**
https://ui.aceternity.com/components/sticky-banner

**Description:** Banner that sticks to viewport edge during scroll, useful for announcements or CTAs.

**When to Use:**
- Limited-time announcements
- Cookie consent notices
- Sale/promotion banners
- Important system messages

**Integration Tips:**
- Dismissible (close button)
- Use warm background (#1a1a1a) with accent text
- Position at top or bottom (not both)
- Ensure doesn't cover critical content

**Aesthetic Fit:** ★★★★☆ - Functional, but can annoy if misused

---

**Animated Testimonials**
https://ui.aceternity.com/components/animated-testimonials

**Description:** Testimonial cards with smooth transitions between quotes.

**When to Use:**
- Social proof sections
- Customer success stories
- Team endorsements
- Product reviews

**Integration Tips:**
- Cycle slowly (5-7 seconds per testimonial)
- Include customer photo/logo for credibility
- Use spring animation for smooth transitions
- Provide manual navigation (dots or arrows)

**Aesthetic Fit:** ★★★★☆ - Good for social proof, standard pattern

---

**Bento Grid**
https://ui.aceternity.com/components/bento-grid

**Description:** Asymmetric grid layout where cells have varying sizes, creating visual interest.

**When to Use:**
- Feature showcases (varied importance)
- Portfolio project grids
- Dashboard overview sections
- Marketing feature highlights

**Integration Tips:**
- 2-3 cell sizes maximum (small, medium, large)
- Most important items in larger cells
- Maintain 16-24px gap for breathing room
- Use consistent padding within cells (24-32px)
- Ensure responsive (stack on mobile)

**Aesthetic Fit:** ★★★★★ - Core aesthetic element, very on-brand

---

## Overlays & Effects

**Dither Shader**
https://ui.aceternity.com/components/dither-shader

**Description:** Dithering effect applied to elements, creating retro print/screen aesthetic.

**When to Use:**
- Images with artistic treatment
- Background overlays
- Retro computing aesthetic sections
- Print-inspired designs

**Integration Tips:**
- Use subtly (10-30% effect strength)
- Combine with warm color palette
- Works well with ASCII art aesthetic
- Consider performance (WebGL shader)

**Aesthetic Fit:** ★★★★★ - Perfect retro technical aesthetic

---

## Installation & Usage

### Aceternity UI Components

```bash
# Install Aceternity UI
npm install framer-motion clsx tailwind-merge

# Copy component code from website into your project
# Each component is standalone, no package installation
```

### Magic UI Components

```bash
# Install Magic UI
npm install @magicui/core framer-motion

# Import components
import { RetroGrid } from "@magicui/core";
```

### General Integration Pattern

```typescript
// Most components follow this pattern:
import { ComponentName } from "./components/ui/component-name";

<ComponentName
  className="..." // Tailwind classes for customization
  // Component-specific props
>
  {children}
</ComponentName>
```

## Performance Considerations

**Heavy Effects (Limit Usage):**
- WebGL-based backgrounds (Background Boxes, Warp Background)
- Continuous particle systems (Glowing Stars)
- Complex parallax with many layers

**Light Effects (Safe for Multiple):**
- CSS-based grids and gradients
- Spring animations on hover
- Text effects on page load
- Border and glow effects

**Mobile Optimizations:**
- Disable or simplify parallax effects
- Reduce particle counts by 50%
- Use CSS fallbacks where possible
- Test on mid-range devices

## Accessibility Notes

**Motion Preferences:**
Always respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Keyboard Navigation:**
Ensure all interactive components are keyboard accessible:
- Tab order makes sense
- Focus states are visible
- Enter/Space trigger actions
- Escape dismisses overlays

**Screen Readers:**
- Decorative animations should have `aria-hidden="true"`
- Important content should not rely solely on animation
- Provide text alternatives where needed

---

## Selection Guide by Context

**Developer Tools & Documentation:**
- ✅ Grid backgrounds, Tracing Beam, Tabs, Border Beam
- ❌ Aurora Text, Glowing Stars, Parallax effects

**Creative Portfolios:**
- ✅ Bento Grid, Focus Cards, Direction Aware Hover, Card Stack
- ❌ Corporate/conservative effects

**AI/LLM Products:**
- ✅ Retro Grid, Typewriter Effect, Flickering Grid, Hyper Text
- ❌ Organic effects (ripples, natural motion)

**Marketing/Landing Pages:**
- ✅ Hero Parallax, Background Beams, Text Generate, Bento Grid
- ❌ Overly technical effects (flickering grids, dithering)

**Technical Dashboards:**
- ✅ Grid backgrounds, Border Beam, Multi-Step Loader, Tabs
- ❌ Decorative effects without purpose

---

## Recommended Starting Kit

For most projects in this aesthetic, start with these core effects:

**Foundation (Always):**
1. Grid/Dot background (subtle, 0.3 opacity)
2. Border Beam (on primary CTAs and active states)
3. Glowing Effect (on cards and important elements)

**Typography (1-2 per page):**
1. Text Generate Effect (hero headline)
2. Typewriter Effect (code/terminal sections)

**Containers (As needed):**
1. Bento Grid (feature showcases)
2. Card Hover Effect (interactive grids)
3. Expandable Card (detailed content)

**Navigation (Standard):**
1. Tabs (with animated indicator)
2. Tracing Beam (long-form content)

This kit provides consistent aesthetic without overwhelming users or sacrificing performance.
