---
name: www-audit
description: Use this skill when auditing external websites for design inspiration, tech stack analysis, and pattern extraction. Triggers include "audit this website", "how was this made", "analyze this site", "extract patterns from", or when referencing external work for design/build decisions. Produces structured site cards for www-studio consumption.
---

# www-audit

extract tech stack, design patterns, and UI components from external websites. produces structured **site cards** for design inspiration and implementation guidance.

## philosophy

| principle | application |
|-----------|-------------|
| **product-first** | understand what the app DOES before how it's built |
| **full-page exploration** | scroll through entire experience, not just above-fold |
| reference-driven | learn from production sites, not hypotheticals |
| structured extraction | patterns over prose, facts over interpretation |
| specialist depth | 12-specialist fanout for granular craft analysis |
| gist-per-specialist | each specialist produces focused 80-150 line gist |
| terse voice | technical language, no AI-speak |
| reusable artifacts | gists and references for www-studio consumption |

## when to use

| use | skip |
|-----|------|
| "audit this site", "how was this made" | internal codebase analysis (use project-review) |
| design inspiration research | just need a quick screenshot |
| tech stack investigation | already know the stack |
| extracting UI patterns | simple content grab |
| pre-build reference gathering | post-build review |

## companion skill: www-studio

`www-audit` extracts references. `www-studio` consumes them when building.

```
www-audit (extract) → gist/reference → www-studio (build)
```

## modes

| mode | trigger | orchestration | output |
|------|---------|---------------|--------|
| **full** (default) | "audit this site", "use www-audit on X" | 12-specialist fanout | Main Index + 11 specialist gists + 2 asset gists |
| **quick** | "quick look at" | solo | tech stack + 3 key patterns |
| **extract** | "extract the nav from" | solo | single component deep-dive |
| **compare** | "compare X and Y" | 2× full fanout | side-by-side diff of Main Indexes |

## decision tree: mode selection

```
What mode should I use?
├── User says "quick look" or "just the stack"?
│   └── mode: quick (solo)
├── User wants specific component only?
│   └── mode: extract (solo)
├── User comparing multiple sites?
│   └── mode: compare (2× full fanout = 24 specialists)
├── User says "audit", "www-audit", or "how was this made"?
│   └── mode: full (12-specialist fanout)
└── Default
    └── mode: full (12-specialist fanout)
```

---

## orchestration: 12-specialist distributed architecture (v2)

**full mode uses 12 parallel specialists** for granular craft analysis and gist-per-specialist output.

**CRITICAL**: All specialists must follow [agent-browser state management protocol](references/agent-browser-state-management.md) for clean screenshots.

### specialist roster

| Specialist | Type | Domain | Gist Responsibility | Screenshot Responsibility |
|-----------|------|--------|---------------------|---------------------------|
| **00. Orchestrator** | System | Workflow management | Main Index (AUDIT.md) | None (aggregates) |
| **01. Photographer** | Copilot | Baseline Coverage | Asset Gists (Desktop/Mobile) | Core scrolls (every ~900px), page navigation, responsive breakpoints |
| **02. Director** | Copilot | UX & Journey | product-experience.md | Multi-page flows, 404 page, success states |
| **03. Visual System** | Copilot | Color & Theme | visual-system.md | Dark/light mode toggles, color contrast |
| **04. Typography** | Copilot | Type & Hierarchy | typography.md | Type scales, font rendering, webfont loading |
| **05. Layout Engineer** | Copilot | Spacing & Grid | layout-grid.md | Breakpoint behaviors, grid overlays, container shifts |
| **06. Materials** | Codex | CSS & Effects | materials-effects.md | Glassmorphism, shadows, gradients, blend modes |
| **07. Components** | Codex | UI Library | component-library.md | Input states, button variants, card states |
| **08. Motion** | Copilot | Animation | motion-interaction.md | Hover states, transition sequences, loading skeletons |
| **09. Content** | Copilot | Copy & Voice | content-voice.md | Empty states, error messages, microcopy |
| **10. Tech Lead** | Codex | Stack & Performance | tech-performance.md | Network waterfalls, bundle analysis (no visual screenshots) |
| **11. Architect** | Codex | Data & Routing | architecture-data.md | CMS structure, state management diagrams |
| **12. Feature Lead** | Copilot | Deep Dives | feature-[name].md | Complex UI (e.g., Stem FM player interface) |

**Estimated gist sizes**:
- Main Index (AUDIT.md): 50-80 lines (<2 min read)
- Specialist gists: 80-150 lines (focused domain analysis)
- Asset gists: Screenshot galleries (Desktop: ~30 images, Mobile: ~5 images)

**Total gists per audit**: ~14-15 gists (1 Main + 2 Assets + 11-12 Specialists)

### decision tree: specialist assignment

```
Which specialists handle what?
├── Full-page screenshot coverage?
│   └── Photographer: Core scrolls, responsive breakpoints
├── Product understanding (what is this)?
│   └── Director: UX journey, multi-page flows
├── Colors, gradients, themes, brand?
│   └── Visual System: Color palette, theme detection
├── Fonts, type scale, hierarchy?
│   └── Typography: Type system, webfont loading
├── Spacing, grid, responsive layout?
│   └── Layout Engineer: Spacing ramp, breakpoints
├── Glassmorphism, shadows, effects?
│   └── Materials: CSS effects, blend modes
├── Buttons, inputs, cards, component library?
│   └── Components: UI library, state variants
├── Hover states, transitions, animations?
│   └── Motion: Timing curves, interaction craft
├── Microcopy, empty states, error messages?
│   └── Content: Voice, messaging patterns
├── Tech stack, performance, headers?
│   └── Tech Lead: Framework detection, bundle analysis
├── Routing, CMS, data architecture?
│   └── Architect: Page structure, state management
├── Complex features (players, dashboards)?
│   └── Feature Lead: Deep dive on specific UI
└── Orchestration and aggregation?
    └── Orchestrator: Compile Main Index gist
```

### specialist brief template

each specialist receives a focused brief:

```markdown
# {Domain} Specialist Brief

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus
{specific domain focus}

## CRITICAL: Theme Detection
Before ANY screenshots:
1. Check site theme: `agent-browser eval "getComputedStyle(document.body).backgroundColor"`
2. Set browser to match: `agent-browser set media light` or `agent-browser set media dark`
3. DO NOT use system preference - match the SITE's theme

## CRITICAL: Full Scroll Exploration
1. Get page height: `agent-browser eval "document.body.scrollHeight"`
2. Scroll through ENTIRE page, not just above-fold
3. Capture screenshots at every ~900px interval
4. Document what happens as you scroll (parallax, sticky, animations)

## Required Deliverables
1. **Findings JSON** - structured data for AUDIT.md
2. **Notes** - 3-5 brief technical observations (NO AI-speak)
3. **Screenshots** - z-prefixed, 8-12 minimum covering scroll journey
4. **Validation Table** - REQUIRED artifact for ALL screenshots (see state management protocol)
5. **CSS Snippets** - implementation-ready code blocks where relevant

## CRITICAL: Validation Table (REQUIRED ARTIFACT)

**Format:**
```
| Screenshot | Pass/Fail | Validation Note |
|------------|-----------|-----------------|
| z-home.png | PASS | Clean hero, no overlays, size 245KB |
| z-menu-open.png | PASS | Products menu open, no other dropdowns, size 198KB |
```

**Orchestrator enforcement:** Output without validation table = REJECTED

**State management protocol:** See [agent-browser-state-management.md](references/agent-browser-state-management.md) for:
- Clean-state checklist (before EVERY screenshot)
- Interaction capture loop (capture → close → wait → verify → proceed)
- Pre-flight protocol (dismiss banners before first screenshot)
- Post-interaction cleanup (verify clean via snapshot)

## Voice Rules
- terse, factual, technical
- NO: "masterclass", "chef's kiss", "psychologically optimized"
- YES: "150ms ease-out", "tight tracking (-0.04em)", "cream vs pure white"

## Tools Available
- agent-browser: open, snapshot -i -c, eval, screenshot, get html, scroll, set media
- WebFetch: for static content analysis

## Output Contract
```json
{
  "domain": "{your domain}",
  "status": "success",
  "site_theme": "dark | light | both",
  "findings": { /* structured data */ },
  "notes": [
    "cream background (#FFFCEC) instead of pure white",
    "tight tracking on headlines (-0.04em)"
  ],
  "screenshots": ["z-home.png", "z-scroll-1.png", "z-scroll-2.png", ...],
  "scroll_effects": ["parallax hero", "sticky nav at 100px", "fade-in sections"],
  "confidence": 8
}
```
```

### Product & Experience Specialist (Copilot 1) - MOST IMPORTANT

This specialist answers: **"What does this app/site actually DO?"**

```markdown
# Product & Experience Specialist Brief

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus (PRIORITY ORDER)
1. **What IS this?** - Product, company, or service being sold/shown
2. **Who is it for?** - Target user
3. **What's the user journey?** - From landing to conversion
4. **What happens when you scroll?** - Effects, animations, reveals
5. **What are the signature interactions?** - Hover states, clicks, transitions
6. **What are ALL the pages?** - Multi-page sites need comprehensive coverage

## CRITICAL: Multi-Page Exploration

**REQUIRED for ALL sites**: Discover and document all publicly accessible pages.

### Page Discovery Protocol

```bash
# 1. After loading homepage, find all navigation links
agent-browser open {URL}
agent-browser wait --load networkidle
agent-browser snapshot -i -c

# 2. Extract all internal links
agent-browser eval "Array.from(document.querySelectorAll('a[href]')).map(a => a.href).filter(h => h.includes(window.location.hostname)).slice(0, 50)"

# 3. Identify key pages to capture:
# - Product/feature pages
# - Pricing page
# - About page
# - Use case pages
# - Blog/resources (capture 1-2 examples, not all posts)
# - App/dashboard pages (if publicly accessible)
# - Any unique routes (e.g., /set/:id for stemplayer.com Stem FM)

# 4. Navigate to each key page and capture
agent-browser click 'a[href="/pricing"]'
agent-browser wait --load networkidle
agent-browser screenshot z-pricing.png
# etc.
```

### Decision Tree: Which Pages to Screenshot

```
Is this a multi-page site?
├── Navigation has 2+ links?
│   └── YES: Explore and screenshot ALL pages
├── Single-page with anchor links only?
│   └── NO: Just scroll and screenshot sections
└── If multi-page:
    ├── Product/feature pages? → SCREENSHOT
    ├── Pricing page? → SCREENSHOT
    ├── About/company page? → SCREENSHOT
    ├── Use case/customer pages? → SCREENSHOT (1-2 examples)
    ├── Blog/resources? → SCREENSHOT (1 example post)
    ├── Documentation? → SCREENSHOT (index + 1 page)
    ├── App/dashboard routes? → SCREENSHOT (if public)
    ├── User-generated content? → SCREENSHOT (1-2 examples)
    └── Total pages: Aim for comprehensive coverage (8-15 pages)
```

### Page Screenshot Naming

| Page Type | Filename |
|-----------|----------|
| Homepage | `z-home.png` |
| Pricing | `z-pricing.png` |
| About | `z-about.png` |
| Features | `z-features.png` |
| Specific feature | `z-feature-{name}.png` |
| Use case | `z-usecase-{name}.png` |
| Blog post example | `z-blog-example.png` |
| App/dashboard | `z-app-{section}.png` |
| User content example | `z-{type}-example.png` |

**Example for stemplayer.com**:
- `z-home.png` - Main homepage
- `z-stemfm-set-example.png` - Stem FM set page (e.g., /set/00000005...)
- `z-stemfm-browse.png` - Browse page (if exists)
- `z-stemfm-player.png` - Player interface detail

## Required: Full Page Scroll (HOMEPAGE)
You MUST scroll through the ENTIRE page and document:
- What content appears at each scroll position
- Parallax effects, sticky elements, scroll-triggered animations
- How the narrative unfolds as user scrolls

## Screenshots Required (8+ minimum)
- z-home.png (hero/above-fold)
- z-scroll-1.png through z-scroll-N.png (every ~900px)
- z-footer.png
- z-mobile.png
- z-mobile-scroll.png

## CRITICAL: Self-Validate Each Screenshot

After capturing each screenshot, use Read tool to visually verify:

```bash
# After: agent-browser screenshot z-home.png
# Immediately validate
```

**Validation checklist (visual analysis):**
- [ ] Shows actual content (not blank, not loading spinner)
- [ ] Correct viewport (desktop: wide layout, mobile: stacked)
- [ ] Text is readable, UI elements visible
- [ ] No obvious capture errors (cut off, error page, cookie banner)
- [ ] File size >10KB (blank screenshots are <5KB)

**If validation fails:** Re-capture immediately. Do NOT proceed to next screenshot.

**Common failures:**
- Blank white screen → page didn't load, wait longer
- Loading spinner → content still loading, wait for complete
- Mobile layout on desktop → wrong viewport set
- Cookie banner covers content → dismiss banner first

## Output Contract
```json
{
  "domain": "product_experience",
  "status": "success",
  "site_theme": "dark | light",
  "product": {
    "what_is_it": "...",
    "target_user": "...",
    "value_prop": "...",
    "cta": "..."
  },
  "user_journey": [
    {"position": "0vh", "content": "hero with..."},
    {"position": "100vh", "content": "features section..."},
    {"position": "200vh", "content": "testimonials..."}
  ],
  "scroll_effects": [
    {"type": "parallax", "element": "hero background", "description": "..."},
    {"type": "sticky", "element": "nav", "trigger": "100px scroll"},
    {"type": "fade-in", "element": "feature cards", "trigger": "scroll into view"}
  ],
  "interactions": [
    {"element": "CTA button", "trigger": "hover", "effect": "scale 1.05"}
  ],
  "screenshots": ["z-home.png", "z-scroll-1.png", ...],
  "confidence": 9
}
```
```

### Motion & Interaction Specialist (Copilot 4) - INTERACTION CRAFT

This specialist captures **how the site FEELS** - the craft of interaction design.

```markdown
# Motion & Interaction Specialist Brief

**Site**: {URL}
**Reference Dir**: ~/.agents/references/web/{ref-name}/

## Your Focus (PRIORITY ORDER)
1. **Hover states** - Buttons, cards, links - what happens on hover?
2. **Click interactions** - Menus, modals, dropdowns - what opens/closes?
3. **Transitions** - Page changes, state transitions, loading sequences
4. **Animation timing** - Duration, easing curves, delays - extract exact values
5. **Scroll-linked motion** - Parallax, fade-ins tied to scroll position

## CRITICAL: Capture Interaction States

You MUST capture discrete interaction states as screenshots:
- z-button-hover.png - primary button hover state
- z-button-active.png - button pressed/active state
- z-menu-open.png - navigation menu expanded
- z-modal-open.png - modal/dialog open state
- z-dropdown-expanded.png - dropdown menu open
- z-card-hover.png - card hover effect
- z-tooltip-visible.png - tooltip shown
- z-loading-state.png - loading spinner/skeleton

## Interaction Capture Pattern

```bash
# 1. Set viewport and theme
agent-browser set viewport 1440 900
agent-browser set media {detected_theme}

# 2. Capture default state
agent-browser screenshot z-button-default.png

# 3. Trigger hover (use hover command if available, or eval)
agent-browser eval "document.querySelector('button').classList.add('hover')"
# OR
agent-browser hover button
agent-browser screenshot z-button-hover.png

# 4. Open interactive elements
agent-browser click '[data-menu-trigger]'
agent-browser screenshot z-menu-open.png

# 5. Modals/overlays
agent-browser click '[data-modal-trigger]'
agent-browser screenshot z-modal-open.png
```

## CRITICAL: Self-Validate Each Screenshot

After EVERY screenshot, immediately validate using Read tool:

```bash
# After: agent-browser screenshot z-button-hover.png
# Immediately validate visually
```

**Validation checklist (visual analysis):**
- [ ] Shows the INTERACTION STATE from filename (hover shows hover, open shows open)
- [ ] Not the default/resting state (unless that's the filename)
- [ ] Correct element is highlighted/changed
- [ ] Viewport matches expected (1440×900 for desktop)
- [ ] Text readable, no capture artifacts
- [ ] File size >10KB

**Interaction state matching:**
- z-button-hover.png → button MUST show hover effect (color change, scale, etc.)
- z-menu-open.png → menu MUST be expanded/visible
- z-modal-open.png → modal MUST be displayed over content
- z-card-hover.png → card MUST show hover state (not default)

**If validation fails:** Re-trigger interaction and re-capture. Do NOT proceed.

**Common failures:**
- z-button-hover.png shows default button → hover didn't trigger, use `agent-browser hover` correctly
- z-menu-open.png shows closed menu → click didn't register, try different selector
- Interaction triggered wrong element → refine selector, verify with snapshot first
- Screenshot timing off → add `agent-browser wait 200` after interaction trigger

## Video Capture (Optional - for complex sequences)

For animations that can't be captured in stills:
```bash
# Record animation sequence (if supported)
# Note: agent-browser doesn't have native video recording
# Document in findings if video would be beneficial
```

## Timing Extraction

Extract exact CSS/JS values:
```bash
agent-browser eval "getComputedStyle(document.querySelector('.button')).transition"
agent-browser eval "getComputedStyle(document.querySelector('.card')).transform"
agent-browser eval "getComputedStyle(document.querySelector('.modal')).animation"

# Check for CSS custom properties
agent-browser eval "getComputedStyle(document.documentElement).getPropertyValue('--transition-speed')"
```

## Required Deliverables

1. **Interaction state screenshots** (5-10 minimum):
   - Key button states (default, hover, active, disabled)
   - Navigation states (menu open, submenu expanded)
   - Modal/overlay states
   - Card/component hover effects
   - Loading/skeleton states

2. **Timing data** (exact values):
   - Transition durations (e.g., 200ms, 0.3s)
   - Easing functions (e.g., cubic-bezier(0.4, 0, 0.2, 1))
   - Animation delays (e.g., stagger delays)
   - Keyframe definitions (if notable)

3. **Interaction notes** (terse, factual):
   - "Button scales 1.05 on hover with 200ms ease-out"
   - "Menu slides in from right, 300ms cubic-bezier(0.16, 1, 0.3, 1)"
   - "Card lifts 8px on hover with box-shadow transition"

## Output Contract
```json
{
  "domain": "motion_interaction",
  "status": "success",
  "site_theme": "dark|light",
  "interaction_states": [
    {"element": "primary button", "state": "hover", "screenshot": "z-button-hover.png", "effect": "scale 1.05, 200ms ease-out"},
    {"element": "nav menu", "state": "open", "screenshot": "z-menu-open.png", "effect": "slide-in 300ms cubic-bezier(0.16, 1, 0.3, 1)"}
  ],
  "timing_system": {
    "duration_fast": "150ms",
    "duration_standard": "300ms",
    "duration_slow": "500ms",
    "easing_primary": "cubic-bezier(0.4, 0, 0.2, 1)",
    "easing_bounce": "cubic-bezier(0.175, 0.885, 0.32, 1.275)"
  },
  "scroll_linked_animations": [
    {"element": "hero", "effect": "parallax", "description": "background moves 0.5x scroll speed"}
  ],
  "loading_patterns": [
    {"state": "skeleton", "screenshot": "z-loading-skeleton.png", "description": "pulsing gray placeholders"}
  ],
  "notes": [
    "Consistent 300ms duration across all transitions",
    "Custom easing curve for all motion",
    "Reduced motion: respects prefers-reduced-motion media query"
  ],
  "confidence": 9
}
```
```

### orchestration workflow: 4-phase model

**Phase 1: Capture (Sequential Start)**
```bash
1. Orchestrator creates reference directory structure
2. Launch Photographer specialist (Copilot)
   - Detects site theme (dark/light)
   - Captures core desktop scrolls (every ~900px)
   - Captures responsive breakpoints (mobile: 375×812)
   - Validates all screenshots (>10KB, no blanks)
   - Creates 2 Asset gists (Desktop + Mobile) via git workflow
3. Photographer returns Asset Gist URLs to orchestrator
```

**Phase 2: Analysis (Parallel Fanout)**
```bash
1. Orchestrator launches 11 specialists in parallel via direct CLI:
   - 4× Codex (Materials, Components, Tech Lead, Architect)
   - 7× Copilot (Director, Visual System, Typography, Layout Engineer, Motion, Content, Feature Lead)
2. Each specialist receives:
   - Target URL
   - Asset Gist URLs (for baseline reference)
   - Reference directory path
3. Specialists execute in parallel:
   - Browse live site with agent-browser
   - Analyze domain-specific aspects
   - **Capture own screenshots** (hover states, theme toggles, interactions, etc.)
   - Extract craft details (CSS values, timing curves, etc.)
   - Validate screenshots (>10KB, z- prefix, clean state)
   - Compile domain.md with findings + validation table
4. Screenshot approach (photography as shared skill):
   - Each specialist has agent-browser access
   - Captures domain-specific screenshots during analysis
   - Either: Adds to Asset gists OR includes in specialist gist
   - Validates own captures (no blanks, clean state protocol)
```

**Phase 3: Reporting (Asynchronous Completion)**
```bash
1. Each specialist:
   - Validates their output (validation table present, no placeholders)
   - Creates specialist gist via `gh gist create domain.md`
   - Returns to orchestrator:
     * Gist URL
     * One-line summary
     * Confidence score (1-10)
2. Orchestrator polls for completion (waits for all 11 specialists)
```

**Phase 4: Assembly**
```bash
1. Orchestrator aggregates findings:
   - Compiles Main Index (AUDIT.md) with:
     * Executive summary (3 sentences)
     * Key metrics table
     * Specialist findings (linked by domain)
     * Asset links (Desktop/Mobile galleries)
2. Creates Main gist via `gh gist create AUDIT.md`
3. Updates reference.json with:
   - Main gist URL
   - Asset gist URLs
   - Specialist gist URLs
   - Validation metrics
4. Returns Main gist URL to user
```

**Total gist output**: 1 Main + 2 Assets + 11 Specialists = 14 gists

### specialist execution patterns

**CRITICAL: Theme Detection First**

Before ANY screenshots, detect and match the site's actual theme:

```bash
# Detect site theme (check for dark background, theme toggle, etc.)
agent-browser eval "getComputedStyle(document.body).backgroundColor"
agent-browser eval "document.documentElement.classList.contains('dark')"

# Set browser to match site's theme (NOT system preference)
agent-browser set media light    # for light-mode sites
agent-browser set media dark     # for dark-mode sites

# If site is dark-only (like stemplayer.com), use dark
# If site is light-only (like async.app), use light
# If site has toggle, capture both states
```

**CRITICAL: Full Scroll Exploration**

Specialists MUST scroll through the entire page, not just above-fold:

```bash
# Scroll exploration pattern
agent-browser scroll down 1000    # First scroll
agent-browser screenshot z-scroll-1.png
agent-browser scroll down 1000    # Second scroll
agent-browser screenshot z-scroll-2.png
# Continue until page bottom

# Or use page height detection
agent-browser eval "document.body.scrollHeight"
# Then systematically capture at intervals
```

**Codex specialists** (deep technical):
```bash
# Codex 1: Tech Stack
agent-browser eval "typeof __NEXT_DATA__"
agent-browser eval "Array.from(document.scripts).map(s => s.src)"
# Headers analysis, framework detection, performance patterns

# Codex 2: Code Patterns
agent-browser eval "getComputedStyle(document.querySelector('button')).transition"
# CSS custom properties, animation keyframes, methodology detection

# Codex 3: Architecture
agent-browser snapshot -i -c
# Page structure, routing patterns, CMS indicators
```

**Copilot 1: Product & Experience (NEW - most important)**
```bash
# 1. Understand what this IS
agent-browser snapshot -i -c
# Read: What is this product? What does it do?

# 2. Scroll through ENTIRE page
agent-browser eval "document.body.scrollHeight"  # Get total height
agent-browser set viewport 1440 900
agent-browser set media {detected_theme}

# 3. Capture scroll journey (8-12 screenshots minimum)
agent-browser screenshot z-home.png              # Hero/above-fold
agent-browser scroll down 900
agent-browser screenshot z-scroll-1.png          # First section
agent-browser scroll down 900
agent-browser screenshot z-scroll-2.png          # Second section
# ... continue to bottom

# 4. Document scroll effects
# - Parallax? Sticky elements? Scroll-triggered animations?
# - What happens as you scroll?

# 5. Check other pages (if multi-page site)
agent-browser click {nav_link}
agent-browser screenshot z-{page}.png
```

**Copilot 2: Visual System**
```bash
agent-browser set viewport 1440 900
agent-browser set media {detected_theme}  # Match site theme!
agent-browser eval "Array.from(document.fonts).map(f => f.family)"
# Color extraction, gradient analysis, theme detection, motion timing
```

**Copilot 3: Component & Layout**
```bash
agent-browser set viewport 1440 900
agent-browser screenshot z-components.png
agent-browser set viewport 375 812
agent-browser screenshot z-mobile.png
# Component inventory, spacing analysis, responsive behavior
```

---

## site card format: Main Index (AUDIT.md)

**v2 architecture**: Main Index is a 50-80 line summary that links to specialist gists.

**gold standard**: Designed to be read in < 2 minutes.

```markdown
# {domain}

| | |
|---|---|
| **url** | {url} |
| **date** | {YYYY-MM-DD} |
| **stack** | {framework}, {styling}, {hosting} |
| **confidence** | {N}/10 |

---

## Executive Summary

{2-3 sentences. factual, terse. what it is, what tech, what's notable.}

Example:
> A masterclass in tactile web design. The site uses a "fleshy" material system with unique subsurface scattering effects. Navigation is unconventional (scroll-jacking with spring physics).

---

## Key Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Pages analyzed | {N} | {multi-page or single-page} |
| Screenshots | Desktop: {N}, Mobile: {N} | {total count} |
| Tech stack | {framework} + {styling} | {version if known} |
| Performance | {lighthouse score or N/A} | {if measured} |
| Accessibility | {score or N/A} | {if measured} |

---

## Specialist Deep Dives

### Visuals
- **[Visual System](gist-url)**: {one-line summary - colors, themes, brand}
- **[Typography](gist-url)**: {one-line summary - fonts, scales, hierarchy}
- **[Layout & Grid](gist-url)**: {one-line summary - spacing, grid, responsive}
- **[Materials & Effects](gist-url)**: {one-line summary - glassmorphism, shadows, gradients}

### Experience
- **[Product & UX Journey](gist-url)**: {one-line summary - what app does, user flow}
- **[Motion & Interaction](gist-url)**: {one-line summary - hover states, transitions, timing}
- **[Content & Voice](gist-url)**: {one-line summary - microcopy, messaging, tone}

### Engineering
- **[Tech Stack & Performance](gist-url)**: {one-line summary - framework, hosting, bundle analysis}
- **[Architecture & Data](gist-url)**: {one-line summary - routing, CMS, state management}
- **[Component Library](gist-url)**: {one-line summary - buttons, inputs, cards, variants}

### Features (if applicable)
- **[Feature: {Name}](gist-url)**: {one-line summary - deep dive on complex UI like Stem FM player}

---

## Top 3 Highlights

1. **{Standout feature}**: {brief description}
2. **{Craft detail}**: {brief description}
3. **{Unique pattern}**: {brief description}

## Top 3 Issues

1. **{Critical issue}**: {brief description}
2. **{Problem area}**: {brief description}
3. **{Opportunity}**: {brief description}

---

## Assets

| Viewport | Gist | Count |
|----------|------|-------|
| Desktop (1440×900) | [{domain}-screens-desktop](gist_url) | {N} |
| Mobile (375×812) | [{domain}-screens-mobile](gist_url) | {N} |

---

## Tags

`{tag1}`, `{tag2}`, `{tag3}`
```

---

## specialist gist format

Each specialist produces an 80-150 line focused gist following this structure:

```markdown
# {Domain}: {Site Name}

**Audit Date**: {YYYY-MM-DD}
**Site**: {URL}
**Main Index**: [AUDIT.md](main-gist-url)

---

## Overview

{2-3 sentence summary of findings for this domain}

---

## {Domain-Specific Section 1}

{tables, lists, code snippets - detailed craft analysis}

Example for Materials specialist:
### Glassmorphism Implementation

| Layer | Backdrop Blur | Opacity | Shadow |
|-------|---------------|---------|--------|
| Primary | 40px | 0.95 | 0 20px 40px rgba(0,0,0,0.1) |
| Secondary | 20px | 0.85 | 0 10px 20px rgba(0,0,0,0.05) |

```css
.glass-surface {
  backdrop-filter: blur(40px);
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}
```

---

## {Domain-Specific Section 2}

{continue with focused craft details}

---

## Screenshots

{if specialist captured domain-specific screenshots}

- `z-{domain}-{description}.png` - {what it shows}
- `z-{domain}-{description}.png` - {what it shows}

---

## Validation

| Requirement | Status | Evidence |
|-------------|--------|----------|
| No blank screenshots | PASS | All {N} screenshots > 10KB |
| Theme matched | PASS | {dark/light} mode detected and applied |
| Clean state protocol | PASS | No overlays in unrelated screenshots |
| z- prefix naming | PASS | All screenshots use z- prefix |

---

## Craft Observations

{3-5 brief, factual observations specific to this domain}

- {observation 1}
- {observation 2}
- {observation 3}

---

## Confidence: {N}/10

{brief note on confidence level and any gaps}
```

---
---

## voice guidelines

**terse, technical, no AI-speak.**

### banned phrases (AI giveaways)

| phrase | problem |
|--------|---------|
| "masterclass in X" | cliché |
| "chef's kiss" | cringe |
| "premium editorial move" | flowery |
| "psychologically optimized/right" | pseudo-science |
| "signals taste and confidence" | marketing speak |
| "humanizes the X system" | anthropomorphizing |
| "shows someone who cares" | presumptuous |
| "dev-aesthetic cosplay" | trying too hard |
| "calm authority" | vague descriptor |

### writing style

| do | don't |
|----|-------|
| "cream tone instead of pure white" | "the refined paper color humanizes the cool blue" |
| "tight tracking (-0.04em)" | "tracking shows someone who cares how letters sit" |
| "150ms ease-out throughout" | "psychologically optimized timing" |
| "burgundy diverges from typical SaaS blue" | "editorial cue that frames product as judgment" |

### notes sections

keep brief. 3-5 bullet points max. facts over interpretation.

```markdown
### Notes

- no pure black on pure white—softened throughout
- 12-step gradients in CSS custom properties
- single family with mono accents
```

---

## screenshot best practices

### CRITICAL: Theme Matching

**Screenshots must match the site's actual theme, NOT your system preference.**

```bash
# FIRST: Detect site theme
agent-browser eval "getComputedStyle(document.body).backgroundColor"
# Dark sites: rgb(0, 0, 0) or similar dark value
# Light sites: rgb(255, 255, 255) or similar light value

# THEN: Set browser to match
agent-browser set media light    # for light-mode-only sites
agent-browser set media dark     # for dark-mode-only sites
```

| Site Theme | Browser Setting | Example Sites |
|------------|-----------------|---------------|
| Dark only | `set media dark` | stemplayer.com, linear.app |
| Light only | `set media light` | async.app, internet.dev |
| Both (toggle) | Capture both states | arc.net (capture z-home.png + z-home-dark.png) |

### Screenshot Quantity: 15-25 minimum

**3 screenshots is NOT enough.** Full audits require comprehensive scroll AND interaction coverage:

#### Scroll Coverage (8-12 screenshots)

| Screenshot | Name | Required |
|------------|------|----------|
| Hero/above-fold | `z-home.png` | YES |
| First scroll section | `z-scroll-1.png` | YES |
| Second scroll section | `z-scroll-2.png` | YES |
| Third scroll section | `z-scroll-3.png` | if exists |
| Footer area | `z-footer.png` | YES |
| Mobile hero | `z-mobile-home.png` | YES |
| Mobile scrolled | `z-mobile-scroll.png` | YES |
| Secondary page | `z-{page}.png` | if multi-page |
| Dark mode (if toggle) | `z-home-dark.png` | if applicable |

#### Interaction Coverage (5-10 screenshots)

| Screenshot | Name | Required |
|------------|------|----------|
| Button hover | `z-button-hover.png` | YES |
| Button active | `z-button-active.png` | if notable |
| Nav menu open | `z-menu-open.png` | YES |
| Modal open | `z-modal-open.png` | if exists |
| Dropdown expanded | `z-dropdown-open.png` | if exists |
| Card hover | `z-card-hover.png` | if notable |
| Tooltip visible | `z-tooltip.png` | if notable |
| Loading state | `z-loading.png` | if notable |
| Skeleton state | `z-skeleton.png` | if notable |

**Gist cohesion priority**: Focus on capturing the craft - what makes this site's interactions special. Every screenshot should demonstrate care and attention to detail.

### Scroll Capture Pattern

```bash
# 1. Set theme and viewport
agent-browser set media {light|dark}  # Match site theme!
agent-browser set viewport 1440 900

# 2. Get page height
agent-browser eval "document.body.scrollHeight"
# Example: 4500px = ~5 viewport heights

# 3. Capture at each viewport interval
agent-browser screenshot z-home.png           # 0px
agent-browser scroll down 900
agent-browser screenshot z-scroll-1.png       # 900px
agent-browser scroll down 900
agent-browser screenshot z-scroll-2.png       # 1800px
agent-browser scroll down 900
agent-browser screenshot z-scroll-3.png       # 2700px
agent-browser scroll down 900
agent-browser screenshot z-footer.png         # 3600px (or bottom)

# 4. Mobile
agent-browser set viewport 375 812
agent-browser scroll up 10000                 # Back to top
agent-browser screenshot z-mobile.png
agent-browser scroll down 800
agent-browser screenshot z-mobile-scroll.png
```

### naming convention

all screenshots use `z-` prefix so they sort after AUDIT.md in gists:

#### Scroll Screenshots

| screenshot | name |
|------------|------|
| Home/hero | `z-home.png` |
| Scroll positions | `z-scroll-1.png`, `z-scroll-2.png`, etc. |
| Footer | `z-footer.png` |
| Mobile viewport | `z-mobile-home.png` |
| Mobile scrolled | `z-mobile-scroll.png` |
| Dark mode | `z-home-dark.png` |
| Specific page | `z-{page}.png` |

#### Page Screenshots (Multi-Page Sites)

| screenshot | name |
|------------|------|
| Pricing page | `z-pricing.png` |
| About page | `z-about.png` |
| Features page | `z-features.png` |
| Specific feature | `z-feature-{name}.png` |
| Use case page | `z-usecase-{name}.png` |
| Blog post example | `z-blog-example.png` |
| App/dashboard | `z-app-{section}.png` |
| User content example | `z-{type}-example.png` (e.g., z-set-example.png for Stem FM) |

#### Interaction Screenshots

| screenshot | name |
|------------|------|
| Button states | `z-button-hover.png`, `z-button-active.png` |
| Navigation | `z-menu-open.png`, `z-menu-submenu.png` |
| Modals | `z-modal-open.png`, `z-modal-{name}.png` |
| Dropdowns | `z-dropdown-open.png` |
| Card interactions | `z-card-hover.png`, `z-card-expanded.png` |
| Tooltips | `z-tooltip-{name}.png` |
| Loading states | `z-loading.png`, `z-skeleton.png` |
| Form states | `z-input-focus.png`, `z-input-error.png` |

### gist organization

**AUDIT.md stays text-only.** Screenshots live in separate, linked gists:

```
{domain}/
├── AUDIT.md                    → main gist (text-only analysis)
├── screenshots/
│   ├── desktop/               → {domain}-screens-desktop gist
│   │   ├── z-home.png
│   │   ├── z-scroll-1.png
│   │   ├── z-scroll-2.png
│   │   └── z-footer.png
│   └── mobile/                → {domain}-screens-mobile gist
│       ├── z-mobile-home.png
│       ├── z-mobile-scroll.png
│       └── z-mobile-footer.png
```

**Benefits:**
- AUDIT.md loads fast, no image bloat
- Agents can fetch specific viewport gist as needed
- Humans can browse screenshots visually in gist gallery

### embedding in AUDIT.md

```markdown
## Screenshots

| Viewport | Gist | Count |
|----------|------|-------|
| Desktop (1440×900) | [domain-screens-desktop](https://gist.github.com/...) | 5 |
| Mobile (375×812) | [domain-screens-mobile](https://gist.github.com/...) | 3 |
```

---

## decision tree: tool selection

```
Which tool for exploration?
├── Need interactive exploration?
│   └── agent-browser (snapshot -i -c)
├── Need static content?
│   └── WebFetch (faster)
├── Need GitHub repo?
│   └── gh CLI
├── Need both interactive + repo?
│   └── agent-browser + gh in parallel
└── Rate limited?
    └── fall back to WebFetch
```

## decision tree: quality gate (STRENGTHENED POST-AAVE DOGFOODING)

```
Is site card ready to publish?
├── Has Product section explaining what this IS?
│   └── NO: FAIL - add Product section first
├── Has Experience section with scroll behavior?
│   └── NO: FAIL - add scroll journey documentation
├── Scroll screenshots >= 8?
│   └── NO: FAIL - capture more scroll positions
├── Interaction screenshots >= 5?
│   └── NO: FAIL - capture hover states, menu open, modal, etc.
├── Multi-page site (navigation has 2+ links)?
│   ├── YES: Has screenshots of ALL key pages (pricing, about, features, etc.)?
│   │   └── NO: FAIL - navigate and capture all pages
│   ├── YES: Has ## Pages section documenting all pages?
│   │   └── NO: FAIL - document page inventory
│   └── NO (single-page): Skip multi-page checks
├── Screenshots match site theme (not system preference)?
│   └── NO: FAIL - retake with correct `set media light/dark`
├── ALL specialists provided validation tables?
│   └── NO: FAIL - reject specialist output, require table
├── Any screenshots with FAIL status in validation tables?
│   └── YES: FAIL - specialist must re-capture failed screenshots
├── Cookie banner visible in ANY screenshot?
│   └── YES: FAIL - delete screenshots, dismiss banner, re-capture
├── Dropdown/modal open in scroll screenshots?
│   └── YES: FAIL - delete screenshots, close overlays, re-capture
├── Multiple interaction states in single screenshot?
│   └── YES: FAIL - delete screenshot, capture one state at a time
├── Inconsistent naming (non-z- prefix)?
│   └── YES: FAIL - rename all screenshots to z- prefix
├── Screenshot filename doesn't match content?
│   └── YES: FAIL - z-menu-open must show open menu, not closed
├── Captures the CRAFT (what makes interactions special)?
│   └── NO: FAIL - focus on interaction quality, not just coverage
├── Header uses table metadata format?
│   └── NO: FAIL - fix to table format
├── All headings single-word (Summary, Tech, Colors...)?
│   └── NO: FAIL - shorten headings
├── Summary under 3 sentences?
│   └── NO: FAIL - tighten
├── Any banned AI phrases present?
│   ├── "masterclass", "chef's kiss", "psychologically"
│   └── YES: FAIL - rewrite in terse technical voice
├── Notes sections under 5 bullets each?
│   └── NO: FAIL - trim
└── All checks pass?
    └── PASS - ready to publish gists
```

**Hard fail-fast rules (immediate DELETE + re-capture):**
1. Cookie banner in screenshot → delete, dismiss banner, re-capture
2. Dropdown open in scroll screenshot → delete, close dropdown, re-capture
3. >1 interaction state → delete, isolate one state, re-capture
4. Blank/loading screenshot → delete, wait for load, re-capture
5. Wrong viewport → delete, set correct viewport, re-capture

## decision tree: voice check

```
Does prose pass voice check?
├── Contains "masterclass"?
│   └── FAIL: remove
├── Contains "chef's kiss"?
│   └── FAIL: remove
├── Contains "humanizes" or "signals"?
│   └── FAIL: rewrite factually
├── Contains "psychologically"?
│   └── FAIL: rewrite technically
├── Sentence over 20 words?
│   └── WARN: consider splitting
├── Interpretation instead of fact?
│   └── WARN: prefer facts
└── All checks pass?
    └── voice approved
```

---

## workflow: full mode

### phase 1: setup

```bash
# parse target
TARGET_URL="${1:-}"
REF_NAME="${2:-$(echo $TARGET_URL | sed 's|https://||' | sed 's|/.*||' | sed 's/\./-/g')}"
REF_DIR="$HOME/.agents/references/web/$REF_NAME"

# create directory
mkdir -p "$REF_DIR/screenshots"
```

### phase 2: execute specialists

Execute 7 specialists in parallel using direct CLI:

```bash
# Create specialist briefs
cat > /tmp/tech-stack-brief.md << 'EOF'
# Tech Stack Deep Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/code-patterns-brief.md << 'EOF'
# Code Patterns Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/architecture-brief.md << 'EOF'
# Architecture Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/product-experience-brief.md << 'EOF'
# Product & Experience Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/visual-system-brief.md << 'EOF'
# Visual System Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/component-layout-brief.md << 'EOF'
# Component & Layout Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

cat > /tmp/motion-interaction-brief.md << 'EOF'
# Motion & Interaction Specialist Brief
**Site**: $TARGET_URL
**Reference Dir**: $REF_DIR

[... full specialist brief from template ...]
EOF

# Execute specialists in parallel (background with -o flag)
# Codex specialists (network access needed)
codex exec /tmp/tech-stack-brief.md --dangerously-bypass-approvals-and-sandbox \
  -o "$REF_DIR/tech-stack-findings.json" &
PID_TECH=$!

codex exec /tmp/code-patterns-brief.md --dangerously-bypass-approvals-and-sandbox \
  -o "$REF_DIR/code-patterns-findings.json" &
PID_CODE=$!

codex exec /tmp/architecture-brief.md --dangerously-bypass-approvals-and-sandbox \
  -o "$REF_DIR/architecture-findings.json" &
PID_ARCH=$!

# Copilot specialists (fast analysis)
cat /tmp/product-experience-brief.md | copilot --model gemini-3-pro-preview --silent \
  > "$REF_DIR/product-findings.json" &
PID_PRODUCT=$!

cat /tmp/visual-system-brief.md | copilot --model gemini-3-pro-preview --silent \
  > "$REF_DIR/visual-findings.json" &
PID_VISUAL=$!

cat /tmp/component-layout-brief.md | copilot --model gemini-3-pro-preview --silent \
  > "$REF_DIR/component-findings.json" &
PID_COMPONENT=$!

cat /tmp/motion-interaction-brief.md | copilot --model gemini-3-pro-preview --silent \
  > "$REF_DIR/motion-findings.json" &
PID_MOTION=$!

# Wait for all specialists to complete (poll for output files)
echo "Waiting for specialists to complete..."
for specialist in tech-stack code-patterns architecture product visual component motion; do
  while [ ! -f "$REF_DIR/${specialist}-findings.json" ]; do
    sleep 10
  done
  echo "✓ $specialist specialist complete"
done

# Verify all processes completed
wait $PID_TECH $PID_CODE $PID_ARCH $PID_PRODUCT $PID_VISUAL $PID_COMPONENT $PID_MOTION
```

### phase 3: aggregate findings

1. Wait for all specialists to complete
2. Read each specialist's output
3. Merge findings into AUDIT.md using site card template
4. Ensure craft observations are integrated into each section

### phase 4: validate screenshots (CRITICAL QUALITY GATE)

**NEVER upload screenshots without visual validation.** Blank screens, wrong viewports, loading spinners = garbage reference.

```bash
# For EACH screenshot captured, validate using Read tool (vision analysis)
for screenshot in "$REF_DIR/screenshots/desktop"/z-*.png; do
  # Read the image (Claude can see it)
  # Ask: Is this image valid for the reference?
done
```

**Validation checklist per screenshot:**

| Check | Good | Bad | Action if Bad |
|-------|------|-----|---------------|
| File size | >10KB | <5KB (likely blank) | Re-capture or delete |
| Visual content | Shows UI | Blank white, loading spinner, error page | Re-capture or delete |
| Viewport match | Desktop: 1440×900, Mobile: 375×812 | Wrong dimensions | Re-capture with correct viewport |
| Interaction state | Matches filename (z-button-hover shows hover) | Default state, wrong element | Re-capture with correct interaction |
| Image clarity | Sharp, readable text | Blurry, cut off | Re-capture |
| Color accuracy | Matches site (if known) | Over/under exposed | Re-capture |

**Visual analysis prompt template:**

```
Validate this screenshot for www-audit reference quality:

Filename: {filename}
Expected: {parse filename for expectations}

Questions:
1. Is this image blank, loading, or showing actual content?
2. Does it match the viewport? (desktop: wide layout, mobile: stacked)
3. Does the interaction state match filename? (hover, open, active, etc.)
4. Is text readable and UI elements visible?
5. Any obvious capture issues? (cut off, wrong page, error state)

Pass/Fail: {boolean}
Issues: {list}
Recommendation: {keep, re-capture, delete}
```

**Aggregation pattern:**

```bash
# Count valid screenshots
DESKTOP_VALID=$(find "$REF_DIR/screenshots/desktop" -name "z-*.png" | wc -l)
MOBILE_VALID=$(find "$REF_DIR/screenshots/mobile" -name "z-*.png" | wc -l)

# Minimum thresholds
if [ "$DESKTOP_VALID" -lt 15 ]; then
  echo "QUALITY GATE FAIL: Only $DESKTOP_VALID desktop screenshots (need 15+)"
  # Re-execute Product/Motion specialists via codex/copilot CLI
fi

if [ "$MOBILE_VALID" -lt 5 ]; then
  echo "QUALITY GATE FAIL: Only $MOBILE_VALID mobile screenshots (need 5+)"
  # Re-execute Product/Motion specialists via codex/copilot CLI
fi
```

**Common validation failures:**

| Failure | Visual Indicator | Fix |
|---------|------------------|-----|
| Blank screenshot | Solid white/gray, no content | Re-capture after page load |
| Loading spinner | Spinner icon, "Loading..." text | Wait for content, re-capture |
| Mobile on desktop | Narrow stacked layout at 1440px | Check `agent-browser set viewport` |
| Desktop on mobile | Wide layout at 375px, horizontal scroll | Check `agent-browser set viewport` |
| Wrong interaction | z-menu-open.png shows closed menu | Re-trigger interaction before screenshot |
| Cookie banner | Banner covers content | Dismiss banner first |
| Modal overlay | Wrong modal open | Close modal, open correct one |

### phase 5: create gists (3 total)

**CRITICAL**: `gh gist create` and `gh gist edit --add` **reject binary files**. Must use git workflow for PNGs.

```bash
# 1. Create AUDIT.md gist (text-only - works with gh gist)
AUDIT_GIST=$(gh gist create "$REF_DIR/AUDIT.md" \
  --desc "{domain} site card - design system, patterns" \
  --public)

# 2. Create desktop screenshots gist (git workflow for binary files)
# Step 2a: Create initial gist with README
cd /tmp && mkdir {domain}-desktop-gist && cd {domain}-desktop-gist
echo "# {domain} desktop screenshots" > README.md
DESKTOP_GIST=$(gh gist create README.md \
  --desc "{domain} desktop screenshots (1440×900)" \
  --public)

# Step 2b: Clone, add PNGs, push via git
cd /tmp && git clone "$DESKTOP_GIST.git" {domain}-desktop-upload
cd {domain}-desktop-upload
cp "$REF_DIR/screenshots/desktop"/z-*.png .
git add z-*.png
git commit -m "Add desktop screenshots"
git push

# 3. Create mobile screenshots gist (git workflow for binary files)
# Step 3a: Create initial gist with README
cd /tmp && mkdir {domain}-mobile-gist && cd {domain}-mobile-gist
echo "# {domain} mobile screenshots" > README.md
MOBILE_GIST=$(gh gist create README.md \
  --desc "{domain} mobile screenshots (375×812)" \
  --public)

# Step 3b: Clone, add PNGs, push via git
cd /tmp && git clone "$MOBILE_GIST.git" {domain}-mobile-upload
cd {domain}-mobile-upload
cp "$REF_DIR/screenshots/mobile"/z-*.png .
git add z-*.png
git commit -m "Add mobile screenshots"
git push

# 4. Extract gist IDs from URLs (format: https://gist.github.com/{user}/{id})
DESKTOP_GIST_ID=$(echo "$DESKTOP_GIST" | sed 's|.*/||')
MOBILE_GIST_ID=$(echo "$MOBILE_GIST" | sed 's|.*/||')

# 5. Update AUDIT.md with gist IDs, re-push via git
cd /tmp && git clone "$AUDIT_GIST.git" {domain}-audit-update
cd {domain}-audit-update
sed -i '' "s|{desktop_gist_url}|https://gist.github.com/{user}/$DESKTOP_GIST_ID|g" AUDIT.md
sed -i '' "s|{mobile_gist_url}|https://gist.github.com/{user}/$MOBILE_GIST_ID|g" AUDIT.md
git add AUDIT.md
git commit -m "Update screenshot gist URLs"
git push
```

**Directory structure for screenshots:**
```
screenshots/
├── desktop/
│   ├── z-home.png
│   ├── z-scroll-1.png
│   ├── z-scroll-2.png
│   └── z-footer.png
└── mobile/
    ├── z-mobile-home.png
    ├── z-mobile-scroll.png
    └── z-mobile-footer.png
```

### phase 6: finalize reference

```bash
# create reference.json
cat > "$REF_DIR/reference.json" << EOF
{
  "name": "$REF_NAME",
  "domain": "$DOMAIN",
  "url": "$TARGET_URL",
  "type": "web",
  "created": "$(date -Iseconds)",
  "stack": { ... },
  "patterns": [ ... ],
  "tags": [ ... ],
  "gist": {
    "auditUrl": "$GIST_URL",
    "createdAt": "$(date -Iseconds)"
  },
  "audit_by": "Codex (Tech/Code/Arch) + Copilot (Color/Type/Component)",
  "audit_confidence": 9,
  "pages_analyzed": N
}
EOF
```

---

## workflow: quick mode

solo execution for fast tech stack checks:

```bash
# quick stack detection
agent-browser open "$URL"
agent-browser eval "typeof __NEXT_DATA__"
agent-browser get html head

# 3 key patterns
agent-browser snapshot -i -c

# single screenshot
agent-browser screenshot /tmp/z-home.png

# output brief summary (no full site card)
```

---

## concrete values

| metric | value | source |
|--------|-------|--------|
| specialists (full mode) | 7 (3 Codex + 4 Copilot) | optimal coverage + motion |
| **scroll screenshots** | **8-12 minimum** | full scroll coverage |
| **interaction screenshots** | **5-10 minimum** | interaction craft coverage |
| **total screenshots** | **15-25 minimum** | scroll + interaction |
| **scroll capture interval** | every ~900px (1 viewport) | comprehensive journey |
| **state cleanup wait** | **500ms after close** | ensures overlay animation complete (aave dogfooding) |
| **cookie banner dismiss** | **required before first screenshot** | aave audit: banner in z-scroll-1, z-scroll-2 |
| **max simultaneous states** | **1 interaction at a time** | aave audit: z-button-products-hover had 2 panels |
| **state reset frequency** | **after EVERY interaction** | prevents pollution in scroll screenshots |
| **pre-flight check** | **before FIRST screenshot** | dismiss banners, close auto-modals |
| **post-interaction check** | **after EVERY interaction screenshot** | close + wait + verify clean via snapshot |
| **validation table** | **required artifact from all specialists** | orchestrator enforcement |
| **screenshot naming** | **z- prefix only, no exceptions** | aave audit: inconsistent a-, b-, c- prefixes |
| **multi-page exploration** | **required for all sites** | stemplayer dogfooding: Stem FM pages missed |
| **pages to screenshot** | **8-15 pages for multi-page sites** | comprehensive coverage |
| **single-page sites** | **homepage scroll only** | if no navigation to other pages |
| **page examples minimum** | **1-2 per page type** | blog posts, use cases, user content |
| notes per section | 3-5 bullets max | brevity |
| summary length | 2-3 sentences | terse |
| desktop viewport | 1440 × 900 | standard capture |
| mobile viewport | 375 × 812 | iPhone size |
| screenshot size target | < 1MB each | gist efficiency |
| confidence threshold | 8+ for complete | quality gate |
| heading style | single word (Summary, Tech) | clean format |
| metadata format | table (not inline) | clean rendering |

### standard headings

| section | heading |
|---------|---------|
| overview | `## Summary` |
| **what it does** | `## Product` |
| **scroll/interactions** | `## Experience` |
| framework | `## Tech` |
| palette | `## Colors` |
| fonts | `## Typography` |
| **timing/interactions** | `## Motion` |
| spacing | `## Layout` |
| ui patterns | `## Components` |
| signatures | `## Patterns` |
| urls | `## Pages` |
| todos | `## Notes` |
| images | `## Screenshots` |
| keywords | `## Tags` |

**Note**: Motion section now includes interaction states table, scroll-linked animations, and timing system.

---

## anti-patterns (UPDATED POST-AAVE DOGFOODING 2026-01-22)

| pattern | problem | fix | evidence | remediation |
|---------|---------|-----|----------|-------------|
| **dropdown pollution** | opening menu, scrolling without closing, pollutes subsequent screenshots | close dropdown + wait 500ms + verify clean before scrolling | aave z-scroll-1.png: Products menu still open | Interaction loop: capture → Esc → wait 500ms → snapshot verify → scroll |
| **cookie banner persistence** | not dismissing banner before capturing, clutters all screenshots | dismiss immediately after page load (pre-flight), before ANY screenshot | aave z-scroll-1.png, z-scroll-2.png: banner visible | Pre-flight: dismiss banner, wait 200ms, verify via snapshot |
| **multiple simultaneous states** | 2+ dropdowns/modals/panels open, unclear what screenshot demonstrates | one interaction state per screenshot, close previous before opening next | aave z-button-products-hover.png: Products dropdown + Aave Web panel both open | Interaction loop: after capture, close current before triggering next |
| **inconsistent naming prefixes** | using a-, b-, c-, d- instead of z- prefix, breaks gist sort order | always use z- prefix for ALL screenshots | aave: a-default-state.png, c-products-menu-open.png | Quality gate FAIL: any non-z- prefix |
| **state cleanup failure** | not resetting page between interactions, leaving overlays active | explicit cleanup: close + wait + verify clean after each interaction | aave scroll screenshots polluted with open menus | Required validation table proves cleanup happened |
| **screenshot-filename mismatch** | filename says z-menu-open but screenshot shows closed menu | validate content matches filename, add to validation table as PASS only if matches | common when interaction doesn't trigger | If mismatch: delete, re-trigger, re-capture, re-validate |
| **skipping pre-flight check** | capturing first screenshot before dismissing banner or checking auto-modals | run clean-state checklist before FIRST screenshot | aave had cookie banner from first capture onward | Pre-flight mandatory: load → wait networkidle → clean-state checklist → capture |
| **no cleanup confirmation** | closing dropdown but not verifying it's closed before proceeding | after closing, take confirmation snapshot and check output | specialists assume close worked | Post-interaction: close → wait 500ms → snapshot -i -c → verify no overlay |
| **blank/empty screenshots** | white screen, loading spinner, no content | validate EVERY screenshot immediately after capture | common issue, 3 blank in initial aave audit | Use Read tool validation, check file size >10KB |
| **mobile on desktop** | narrow stacked layout at 1440px wide | verify `agent-browser set viewport 1440 900` before capture | wrong viewport setting | Pre-capture checklist: verify viewport dimensions |
| **desktop on mobile** | wide layout at 375px, horizontal scroll | verify `agent-browser set viewport 375 812` before capture | wrong viewport setting | Pre-capture checklist: verify viewport dimensions |
| **wrong interaction state** | z-button-hover.png shows default button, not hover | validate interaction triggered before screenshot, check via snapshot | interaction didn't trigger | After trigger: wait 100ms, snapshot -i -c, verify hover class present |
| **wrong theme in screenshots** | dark screenshots for light-only site (or vice versa) | `set media light/dark` to match site, not system preference | theme detection failure | Pre-flight: eval background color, set media to match |
| **only scroll screenshots** | misses interaction craft and hover states | capture 5-10 interaction states (hover, menu open, modal, etc.) | incomplete audit | Motion & Interaction specialist required |
| **only homepage captured** | multi-page site but only homepage screenshotted, misses pricing/features/app pages | navigate and screenshot ALL pages (pricing, about, features, user content examples) | stemplayer: Stem FM pages missed | Multi-page exploration protocol required |
| **no scroll exploration** | only captures above-fold | scroll through entire page systematically, every ~900px | incomplete audit | Product & Experience specialist: full scroll required |
| **tech-first, product-last** | misses what the app actually does | understand product BEFORE tech stack | incomplete audit | Product section must come first |
| **coverage without craft** | screenshots don't show what's special | focus on interaction quality, not just quantity | gist doesn't demonstrate craft | Capture what makes interactions special |
| solo full audit | shallow, misses depth | use 7-specialist fanout | structural requirement | Always use full specialist roster |
| `--full` screenshots | 18MB files, whitespace | viewport-only default (no --full flag) | file size bloat | Standard capture without --full |
| no z- prefix | wrong sort order in gist | always z-prefix all screenshots | sorting issue | Quality gate: enforce z- prefix |
| **gh gist create *.png** | "binary file not supported" error | git workflow: create README gist, clone, add PNGs, push | GitHub gist limitation | See phase 5 gist workflow |
| **gh gist edit --add X.png** | silently fails, PNGs don't upload | use git workflow (clone, add, commit, push) | GitHub gist limitation | See phase 5 gist workflow |
| wordy headings | "Executive Summary", "Tech Stack" | single words: "Summary", "Tech" | readability | Use standard heading format |
| AI-speak prose | "masterclass", "chef's kiss" | terse technical language | voice guideline violation | See banned phrases table |
| flowery observations | "psychologically optimized" | factual: "150ms ease-out" | voice guideline violation | Technical precision |
| metadata on one line | renders collapsed | use table format | rendering issue | Use table for metadata |
| verbose notes sections | walls of interpretation | 3-5 bullet points max | brevity principle | Trim to essentials |

**See also:** [agent-browser-state-management.md](references/agent-browser-state-management.md) for detailed anti-pattern examples with code.

---

## output contract

```json
{
  "mode": "full | quick | extract | compare",
  "status": "success | partial | failed",
  "domain": "arc.net",
  "ref_name": "arc-net",
  "ref_path": "~/.agents/references/web/arc-net/",
  "specialists_used": 6,
  "stack": {
    "framework": "next.js",
    "styling": "stitches",
    "hosting": "vercel"
  },
  "design_system": {
    "colors": { "primary": "#3139FB", "background": "#FFFCEC" },
    "typography": { "display": "Marlin Soft", "body": "Inter" },
    "motion": { "duration": "150ms", "easing": "ease-out" },
    "spacing_base": "8px"
  },
  "patterns": ["wave-dividers", "8px-grid", "150ms-transitions"],
  "gist": {
    "url": "https://gist.github.com/...",
    "screenshot_count": 6
  },
  "confidence": 9,
  "summary": "Browser Company marketing site. Next.js + Stitches. Dual-gradient color system, 8px grid, 150ms motion timing."
}
```

---

## trails integration

```bash
trails trail record --agent claude --action completed \
  --task "www-audit: $DOMAIN (6-specialist)" \
  --confidence $CONFIDENCE \
  --gist \
  --json -q
```

---

## references

- **[references/agent-browser-state-management.md](references/agent-browser-state-management.md)** - **agent-browser best practices** (NEW - based on aave dogfooding)
- [references/common-stacks.md](references/common-stacks.md) - tech stack detection
- [references/pattern-vocabulary.md](references/pattern-vocabulary.md) - UI pattern naming
- [references/specialist-briefs.md](references/specialist-briefs.md) - full specialist brief templates
- `~/.agents/references/` - reference bank
- `~/.agents/rules/agent-browser.md` - agent-browser CLI
- `~/.agents/rules/codex.md` - Codex CLI patterns
- `~/.agents/rules/copilot.md` - Copilot CLI patterns

**Key improvement (2026-01-22)**: Added mandatory state management protocol and validation table requirement based on aave.com dogfooding that revealed enforcement gaps.
