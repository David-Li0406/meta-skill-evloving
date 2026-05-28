# Specialist Brief Templates

Full prompts for the 6-agent fanout in www-audit full mode.

---

## Codex 1: Tech Stack Deep

```markdown
# Tech Stack Deep Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus

Deep technical analysis of the site's framework, hosting, bundling, and performance patterns. You are the infrastructure expert.

## Required Deliverables

1. **Framework detection** with evidence (not just "Next.js" but how you know)
2. **Hosting/CDN analysis** from headers
3. **Performance patterns** (ISR, caching, image optimization, font loading)
4. **Build tooling** (bundler, chunk splitting)
5. **Analytics/tracking** tools detected
6. **3-5 Technical Observations** on *why* their infrastructure choices work

## Extraction Commands

```bash
agent-browser open "{URL}"

# Framework detection
agent-browser eval "typeof __NEXT_DATA__ !== 'undefined' ? 'Next.js' : typeof __NUXT__ !== 'undefined' ? 'Nuxt' : 'unknown'"
agent-browser eval "window.__NEXT_DATA__?.buildId"

# Scripts analysis
agent-browser eval "Array.from(document.scripts).map(s => s.src).filter(Boolean)"

# Headers (via fetch)
agent-browser eval "fetch(location.href).then(r => Object.fromEntries(r.headers))"

# Performance hints
agent-browser eval "performance.getEntriesByType('resource').slice(0,20).map(r => ({name: r.name, type: r.initiatorType, duration: r.duration}))"
```

## Output Contract

```json
{
  "domain": "tech-stack",
  "status": "success",
  "findings": {
    "framework": { "name": "Next.js", "version": "16.x", "evidence": ["__NEXT_DATA__ present", "/_next/static/ paths"] },
    "hosting": { "provider": "Vercel + Cloudflare", "evidence": ["x-vercel-id header", "Server: cloudflare"] },
    "styling": { "approach": "Stitches CSS-in-JS", "evidence": ["<style id='stitches'>"] },
    "analytics": { "tools": ["Plausible"], "evidence": ["/js/script.js path"] },
    "performance": {
      "image_optimization": "Next.js Image with fetchPriority",
      "caching": "ISR (max-age=0, must-revalidate)",
      "font_loading": "Self-hosted with display=fallback",
      "script_splitting": "18 chunks, per-page splitting"
    }
  },
  "craft_observations": [
    "Plausible over Google Analytics shows privacy-first values—aligns with browser product positioning",
    "ISR with must-revalidate gives fresh content without cold starts",
    "Self-hosted fonts avoid GDPR issues with Google Fonts"
  ],
  "confidence": 9
}
```
```

---

## Codex 2: Code Patterns

```markdown
# Code Patterns Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus

CSS methodology, animation implementation, and unique code patterns. You are the implementation expert.

## Required Deliverables

1. **CSS methodology** (Tailwind, CSS-in-JS, modules, SASS, etc.)
2. **Design tokens** (CSS custom properties extraction)
3. **Animation implementation** (library or pure CSS, keyframes)
4. **Transition patterns** (timing, easing curves)
5. **Unique implementations** (signature effects, clever techniques)
6. **Implementation-ready CSS snippets** for notable patterns
7. **3-5 Code Observations** on technical craft

## Extraction Commands

```bash
agent-browser open "{URL}"

# CSS methodology
agent-browser eval "document.body.className"
agent-browser eval "document.querySelector('[class*=\"_\"]')?.className"

# Design tokens
agent-browser eval "(() => { const s = getComputedStyle(document.documentElement); const t = {}; for (let i = 0; i < s.length; i++) { if (s[i].startsWith('--')) t[s[i]] = s.getPropertyValue(s[i]).trim(); } return t; })()"

# Transitions
agent-browser eval "getComputedStyle(document.querySelector('button')).transition"
agent-browser eval "getComputedStyle(document.querySelector('a')).transition"

# Animation libraries
agent-browser eval "typeof gsap !== 'undefined' ? 'GSAP' : typeof anime !== 'undefined' ? 'anime.js' : typeof MotionOne !== 'undefined' ? 'Motion One' : 'CSS only'"

# Keyframes (search stylesheets)
agent-browser eval "Array.from(document.styleSheets).flatMap(s => { try { return Array.from(s.cssRules).filter(r => r.type === 7).map(r => r.name) } catch(e) { return [] } })"
```

## Output Contract

```json
{
  "domain": "code-patterns",
  "status": "success",
  "findings": {
    "css_methodology": "Stitches CSS-in-JS with utility classes",
    "design_tokens": {
      "--colors-primary1": "rgb(255, 234, 231)",
      "--colors-primary6": "rgb(255, 99, 71)",
      "--spacing-1": "4px"
    },
    "transitions": {
      "default_duration": "150ms",
      "default_easing": "ease-out",
      "properties": ["transform", "opacity", "box-shadow"]
    },
    "animation_library": "CSS only (no external library)",
    "keyframes": ["shimmer", "fade-in", "slide-up"],
    "unique_patterns": [
      {
        "name": "wave-divider",
        "description": "SVG mask for organic section dividers",
        "css": "mask-image: url(...); mask-repeat: repeat-x;"
      }
    ]
  },
  "craft_observations": [
    "No animation library—pure CSS shows confidence and reduces bundle",
    "150ms is psychologically optimal—feels instant but visible",
    "Wave dividers via SVG mask is clever—scales infinitely without image requests"
  ],
  "css_snippets": [
    "/* Wave Divider */\n.wave { mask-image: url(...); mask-repeat: repeat-x; height: 120px; }"
  ],
  "confidence": 8
}
```
```

---

## Codex 3: Architecture

```markdown
# Architecture Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus

Site structure, page architecture, routing patterns, CMS detection, and data flow. You are the architecture expert.

## Required Deliverables

1. **Page inventory** (all discoverable pages)
2. **Routing patterns** (dynamic routes, catch-all, etc.)
3. **CMS detection** (Sanity, Contentful, none, etc.)
4. **Data fetching patterns** (SSR, SSG, client-side)
5. **Navigation structure** (header, footer, sitemap)
6. **3-5 Architecture Observations** on structural decisions

## Extraction Commands

```bash
agent-browser open "{URL}"
agent-browser snapshot -i -c

# Navigation links
agent-browser eval "Array.from(document.querySelectorAll('nav a, header a')).map(a => ({text: a.textContent.trim(), href: a.href}))"

# Footer links
agent-browser eval "Array.from(document.querySelectorAll('footer a')).map(a => ({text: a.textContent.trim(), href: a.href}))"

# CMS detection
agent-browser eval "document.querySelector('[class*=\"sanity\"]') ? 'Sanity' : document.querySelector('[class*=\"contentful\"]') ? 'Contentful' : 'none detected'"

# Page structure
agent-browser eval "Array.from(document.querySelectorAll('main > section, main > div')).length"

# Navigate to key pages and snapshot
agent-browser open "{URL}/about"
agent-browser snapshot -i -c
agent-browser open "{URL}/pricing"
agent-browser snapshot -i -c
```

## Output Contract

```json
{
  "domain": "architecture",
  "status": "success",
  "findings": {
    "pages": [
      { "name": "Home", "path": "/", "type": "marketing" },
      { "name": "About", "path": "/about", "type": "marketing" },
      { "name": "Pricing", "path": "/pricing", "type": "marketing" },
      { "name": "Blog", "path": "/blog", "type": "content" },
      { "name": "Docs", "path": "/docs", "type": "documentation" }
    ],
    "routing": "App Router with static + dynamic routes",
    "cms": "None detected (static content)",
    "data_fetching": "ISR for marketing pages, SSG for docs",
    "navigation": {
      "header": ["Overview", "Features", "Pricing", "Blog"],
      "footer": ["Company", "Legal", "Social"]
    }
  },
  "craft_observations": [
    "No CMS keeps deployment simple—content changes require code changes, but that's fine for a product site",
    "Clear URL structure (/about, /pricing) shows SEO awareness",
    "Separate /blog and /docs suggests content strategy maturity"
  ],
  "confidence": 8
}
```
```

---

## Copilot 1: Color & Theming

```markdown
# Color & Theming Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/screenshots/

## Your Focus

Complete color system analysis with emotional intent. You are the color expert—think like a brand designer.

## Required Deliverables

1. **Brand palette** with hex, RGB, and emotional intent for each color
2. **Surface colors** (backgrounds, cards, sections)
3. **Gradient systems** (if present)
4. **Dark mode analysis** (or strategic dark section usage)
5. **Accessibility colors** (focus rings, error states)
6. **"Why this color?" callout** for the most distinctive choice
7. **5-10 Color Observations** on brand/emotional decisions
8. **Screenshots** of color usage (z-prefixed)

## Extraction Commands

```bash
agent-browser open "{URL}"
agent-browser set viewport 1440 900

# Body colors
agent-browser eval "({bg: getComputedStyle(document.body).backgroundColor, color: getComputedStyle(document.body).color})"

# Key element colors
agent-browser eval "getComputedStyle(document.querySelector('h1')).color"
agent-browser eval "getComputedStyle(document.querySelector('button')).backgroundColor"
agent-browser eval "getComputedStyle(document.querySelector('a')).color"

# CSS custom properties (colors)
agent-browser eval "(() => { const s = getComputedStyle(document.documentElement); const t = {}; for (let i = 0; i < s.length; i++) { if (s[i].includes('color')) t[s[i]] = s.getPropertyValue(s[i]).trim(); } return t; })()"

# Screenshots
agent-browser screenshot ~/.agents/references/web/{ref}/screenshots/z-hero-colors.png
```

## Output Contract

```json
{
  "domain": "color-theming",
  "status": "success",
  "findings": {
    "brand_palette": [
      { "name": "Brand Blue", "hex": "#3139FB", "rgb": "rgb(49, 57, 251)", "usage": "Primary CTAs", "intent": "Technical trust, modern energy" },
      { "name": "Coral Red", "hex": "#FB3A4D", "rgb": "rgb(251, 58, 77)", "usage": "Accent CTAs", "intent": "Urgency without aggression" },
      { "name": "Off-white", "hex": "#FFFCEC", "rgb": "rgb(255, 252, 236)", "usage": "Background", "intent": "Warmth, premium feel" }
    ],
    "surfaces": {
      "background_primary": "#FFFCEC",
      "background_secondary": "#E0E0F7",
      "background_dark": "#36566B"
    },
    "gradients": [
      { "name": "Primary Scale", "stops": ["#FFF0ED", "#FF6347", "#090201"], "steps": 12 }
    ],
    "theme_strategy": "Light only with strategic dark sections",
    "accessibility": {
      "focus_ring": "#96C4FF",
      "error": "#FB3A4D"
    },
    "distinctive_choice": {
      "color": "#FFFCEC",
      "observation": "Off-white instead of pure white humanizes the cool blue system—this is refined paper, not bleached brightness"
    }
  },
  "craft_observations": [
    "The off-white background (#FFFCEC) is a micro-decision most brands miss—creates premium feel",
    "#3139FB is perfectly saturated—bold enough for attention without aggression",
    "No dark mode toggle, but dark sections provide contrast without system complexity",
    "Warm coral (#FB3A4D) for CTAs avoids typical red=danger associations",
    "12-step gradient scales show design system maturity"
  ],
  "screenshots": ["z-hero-colors.png"],
  "confidence": 9
}
```
```

---

## Copilot 2: Typography & Motion

```markdown
# Typography & Motion Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/screenshots/

## Your Focus

Font ecosystem and animation timing. You are the typography and motion expert—think like a brand typographer and motion designer.

## Required Deliverables

1. **Font families** with weights, sources, and use cases
2. **Type scale** (h1-h6, body, small)
3. **Font loading strategy** (preload, display values)
4. **Transition timing** (duration, easing, properties)
5. **Micro-interaction inventory** (button, link, card hovers)
6. **Signature animations** (if any unique patterns)
7. **5-10 Typography/Motion Observations**
8. **Screenshots** of type hierarchy

## Extraction Commands

```bash
agent-browser open "{URL}"
agent-browser set viewport 1440 900

# Fonts
agent-browser eval "Array.from(document.fonts).map(f => ({family: f.family, weight: f.weight, style: f.style}))"

# Type scale
agent-browser eval "['h1','h2','h3','h4','p','small'].map(tag => { const el = document.querySelector(tag); if (!el) return null; const s = getComputedStyle(el); return {tag, fontFamily: s.fontFamily, fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight, letterSpacing: s.letterSpacing}; }).filter(Boolean)"

# Transitions
agent-browser eval "getComputedStyle(document.querySelector('button')).transition"
agent-browser eval "getComputedStyle(document.querySelector('a')).transition"

# Screenshots
agent-browser screenshot ~/.agents/references/web/{ref}/screenshots/z-typography.png
```

## Output Contract

```json
{
  "domain": "typography-motion",
  "status": "success",
  "findings": {
    "fonts": [
      { "family": "Marlin Soft SQ", "weights": [400, 500, 700, 900], "source": "Self-hosted", "usage": "Display headings" },
      { "family": "Inter", "weights": [400, 500, 600], "source": "Self-hosted variable", "usage": "Body text" }
    ],
    "type_scale": [
      { "element": "H1", "size": "45.51px", "weight": 700, "lineHeight": "0.927", "letterSpacing": "-0.04em" },
      { "element": "Body", "size": "20px", "weight": 400, "lineHeight": "1.2", "letterSpacing": "normal" }
    ],
    "font_loading": {
      "strategy": "Self-hosted with display=fallback for brand fonts",
      "total_fonts": 38
    },
    "motion": {
      "default_duration": "150ms",
      "default_easing": "ease-out",
      "philosophy": "Responsive restraint—fast enough to feel instant, slow enough to notice"
    },
    "micro_interactions": [
      { "element": "Button", "effect": "scale(1.05) + shadow lift", "duration": "150ms" },
      { "element": "Link", "effect": "opacity fade", "duration": "200ms" },
      { "element": "Card", "effect": "translateY(-4px)", "duration": "150ms" }
    ]
  },
  "craft_observations": [
    "Marlin Soft SQ lives between trendy (Montserrat) and austere (Helvetica)—confident but approachable",
    "-0.04em headline tracking shows someone who obsesses over letter fit",
    "150ms + ease-out is psychologically optimized—feels instant but never abrupt",
    "Self-hosted 38 fonts sounds heavy but variable fonts compress well",
    "Tight headlines (<1.0 line-height) vs spacious body (1.2) creates hierarchy through rhythm"
  ],
  "screenshots": ["z-typography.png"],
  "confidence": 9
}
```
```

---

## Copilot 3: Component & Layout

```markdown
# Component & Layout Specialist

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/screenshots/

## Your Focus

Component library and layout system. You are the UI systems expert—think like a design systems engineer.

## Required Deliverables

1. **Layout system** (container, max-width, padding)
2. **Grid/spacing** (base unit, scale)
3. **Responsive breakpoints**
4. **Component inventory** (buttons, cards, inputs, nav)
5. **Component CSS** (implementation-ready)
6. **Unique UI patterns** (signature components)
7. **5-10 Component/Layout Observations**
8. **Screenshots** of key components and responsive states

## Extraction Commands

```bash
agent-browser open "{URL}"
agent-browser set viewport 1440 900

# Container
agent-browser eval "getComputedStyle(document.querySelector('main, .container, [class*=\"container\"]')).maxWidth"

# Buttons
agent-browser eval "(() => { const btn = document.querySelector('button'); const s = getComputedStyle(btn); return {bg: s.backgroundColor, color: s.color, padding: s.padding, borderRadius: s.borderRadius, fontSize: s.fontSize}; })()"

# Cards
agent-browser eval "(() => { const card = document.querySelector('[class*=\"card\"], article'); if (!card) return null; const s = getComputedStyle(card); return {bg: s.backgroundColor, boxShadow: s.boxShadow, borderRadius: s.borderRadius, border: s.border}; })()"

# Screenshots
agent-browser screenshot ~/.agents/references/web/{ref}/screenshots/z-components.png

# Mobile
agent-browser set viewport 375 812
agent-browser screenshot ~/.agents/references/web/{ref}/screenshots/z-mobile.png
```

## Output Contract

```json
{
  "domain": "component-layout",
  "status": "success",
  "findings": {
    "layout": {
      "container_max_width": "1200px",
      "horizontal_padding": { "desktop": "32px", "tablet": "24px", "mobile": "16px" },
      "vertical_hero": "72px",
      "vertical_content": "48-64px"
    },
    "grid": {
      "base_unit": "8px",
      "spacing_scale": [4, 8, 12, 16, 24, 32, 40, 48, 56, 64, 72]
    },
    "breakpoints": [
      { "name": "mobile", "max": "600px" },
      { "name": "tablet", "range": "600-800px" },
      { "name": "desktop", "min": "800px" }
    ],
    "components": {
      "buttons": {
        "primary": { "bg": "#FF3333", "color": "white", "padding": "8px 16px", "borderRadius": "8px" },
        "secondary": { "bg": "white", "color": "#2702C2", "borderRadius": "12px" }
      },
      "cards": {
        "default": { "shadow": "0 2px 2px rgba(0,0,0,0.1)", "border": "1px solid #D6D6D6", "radius": "24px" }
      },
      "inputs": {
        "style": "border-bottom",
        "focus": "2px solid #96C4FF"
      }
    },
    "unique_patterns": [
      { "name": "Wave Divider", "description": "SVG squiggle mask between sections" },
      { "name": "Gradient Text", "description": "background-clip: text for hero headings" }
    ]
  },
  "craft_observations": [
    "8px base unit with no exceptions shows discipline—no arbitrary 11px anywhere",
    "24px card radius is bold—most sites use 8-12px, this feels more friendly",
    "Wave dividers break corporate rigidity without feeling unprofessional",
    "Focus ring (#96C4FF) is visible but not jarring—accessibility without ugliness"
  ],
  "screenshots": ["z-components.png", "z-mobile.png"],
  "confidence": 9
}
```
```

---

## Specialist Handoff

After all specialists complete, orchestrator aggregates:

1. Merge all `findings` into appropriate AUDIT.md sections
2. Integrate `craft_observations` into section-specific observation blocks
3. Collect all `screenshots` for gist upload
4. Use highest `confidence` as overall confidence
