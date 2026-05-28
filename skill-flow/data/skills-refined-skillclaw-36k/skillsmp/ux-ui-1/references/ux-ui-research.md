# ux-ui Research

Research document for the UX/UI design skill. This skill helps developers create accessible, consistent, and user-centered interfaces.

## Phase 1: Upstream Survey

### Dammyjay93/claude-design-engineer (Primary Upstream)

Source: [Dammyjay93/claude-design-engineer](https://github.com/Dammyjay93/claude-design-engineer)

#### Overview
A design engineering plugin for Claude Code that provides craft, memory, and enforcement for consistent UI. It features smart workflows with automatic mode detection, system.md loading every session, post-write validation hooks, and specialized commands.

#### Installation
**Via Plugin Marketplace:**
```bash
/plugin marketplace add Dammyjay93/claude-design-engineer
```

**Manual Installation:**
```bash
git clone https://github.com/Dammyjay93/claude-design-engineer.git
cd claude-design-engineer
cp -r .claude/* ~/.claude/
cp -r .claude-plugin/* ~/.claude-plugin/
```

#### Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| APPLY | When `.design-engineer/system.md` exists | Loads established patterns, validates before finishing, updates system if new patterns emerge |
| ESTABLISH | New projects without system | Scans project (package.json, framework, file structure), infers product type, suggests direction, asks ONE smart question with default, builds components, offers to save system |
| EXTEND | Adding to existing patterns | Extends established patterns with new components while maintaining consistency |

#### Commands

| Command | Purpose |
|---------|---------|
| `/design-engineer:init` | Smart dispatcher (detects mode automatically) |
| `/design-engineer:status` | Show current design system |
| `/design-engineer:audit <path>` | Check code against established system |
| `/design-engineer:extract` | Extract patterns from existing code |

#### Design System Features
- **Pattern Reuse**: Button: 36px, Card: 16px padding
- **Spacing Grid**: 4px, 8px, 12px, 16px increments
- **Violation Detection**: Catches inconsistencies before finishing
- **Memory Persistence**: Decisions stored in `.design-engineer/system.md`

#### Core Philosophy
> "Decisions compound — A spacing value chosen once becomes a pattern. A depth strategy becomes an identity."

> "Consistency beats perfection — A coherent system with 'imperfect' values beats a scattered interface with 'correct' ones."

> "Memory enables iteration — When you can see what you decided and why, you can evolve intentionally instead of drifting accidentally."

---

### obra/superpowers

Source: [obra/superpowers](https://github.com/obra/superpowers)

Superpowers does **not include dedicated UX/UI design skills**. The framework focuses on software development methodology rather than visual design capabilities.

#### Design-Adjacent Capability
The closest feature is **brainstorming**, described as "Socratic design refinement" that refines rough ideas through questions, explores alternatives, and presents design in sections for validation. However, this targets **software architecture and feature specification** rather than visual or UX design.

#### Available Skills (No UX/UI)
- Testing: test-driven-development
- Debugging: systematic-debugging, verification-before-completion
- Collaboration: brainstorming, writing-plans, executing-plans, code-review
- Meta: writing-skills, using-superpowers

---

### VoltAgent/awesome-claude-code-subagents

Source: [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

#### UI Designer Subagent
Location: `categories/01-core-development/ui-designer.md`
- **Role**: Visual design and interaction specialist
- **Focus**: Interface aesthetics and user interaction patterns
- **Approach**: Isolated context windows with specialized prompts

#### UX Researcher Subagent
Location: `categories/08-business-product/ux-researcher.md`
- **Role**: User research expert
- **Focus**: Conducting research to inform design decisions
- **Capabilities**: User studies, persona development, usability analysis

#### PowerShell UI Architect
Location: `categories/06-developer-experience/powershell-ui-architect.md`
- **Role**: PowerShell UI/UX specialist
- **Focus**: WinForms, WPF, Metro frameworks, and TUIs
- **Target**: Windows-specific interface development

---

## Phase 2: Research Findings

### 1. UI Component Library Best Practices

Sources:
- [Atomic Design Methodology - Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/)
- [Best Practices for Scalable Component Libraries - UXPin](https://www.uxpin.com/studio/blog/best-practices-for-scalable-component-libraries/)
- [Atomic Design Principles - InkBot Design](https://inkbotdesign.com/atomic-design-principles/)
- [Best Atomic UI Frameworks 2026 - DEV Community](https://dev.to/ninarao/best-atomic-ui-component-frameworks-for-lightning-fast-web-development-in-2026-3894)

#### Atomic Design Hierarchy

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 1 | Atoms | Basic building blocks | `<Button />`, `<Input />`, `<Icon />` |
| 2 | Molecules | Groups of atoms | `<SearchBar />`, `<FormField />` |
| 3 | Organisms | Complex UI sections | `<NavBar />`, `<ProductCard />` |
| 4 | Templates | Page-level layouts | `<DashboardLayout />` |
| 5 | Pages | Specific instances | `<UserDashboard />` |

#### Design Tokens (Sub-Atomic Particles)

Design tokens are the foundation below atoms — variables that store visual design attributes:

```css
:root {
  /* Primitive Tokens */
  --color-blue-500: #0066cc;
  --spacing-4: 16px;

  /* Semantic Tokens */
  --color-primary: var(--color-blue-500);
  --color-error: var(--color-red-500);
  --spacing-component: var(--spacing-4);
}
```

#### Best Practices

1. **Start with foundational elements**: Build buttons, inputs, and typography before complex patterns
2. **Never let organisms override atom styles**: If an organism needs a smaller button, create a "Small Button" variant at the atomic level
3. **Use governance models**: Prevent duplication and maintain consistency
4. **Document in Storybook**: Visual documentation for all components
5. **Automated testing with CI**: Catch issues early in the pipeline

#### Recommended Frameworks (2025-2026)

| Framework | Best For | Notes |
|-----------|----------|-------|
| Tailwind CSS | Atomic styling, flexibility | Utility-first, no fighting predefined styles |
| shadcn/ui | Accessible components | Pre-built, customizable, React-focused |
| Material UI | Enterprise, B2B SaaS | Comprehensive, well-documented |
| Radix UI | Accessibility-first | Unstyled primitives |
| gluestack | Cross-platform | Web + Native support |

---

### 2. Accessibility Standards (WCAG 2.1/2.2)

Sources:
- [WCAG 2 Overview - W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [What's New in WCAG 2.2 - W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [WCAG 2.2 Complete Guide - AllAccessible](https://www.allaccessible.org/blog/wcag-22-complete-guide-2025)
- [ARIA Labels Implementation Guide](https://www.allaccessible.org/blog/implementing-aria-labels-for-web-accessibility)

#### WCAG Structure

WCAG 2.2 has **13 guidelines** organized under **4 principles** (POUR):

| Principle | Description |
|-----------|-------------|
| **Perceivable** | Information must be presentable in ways users can perceive |
| **Operable** | UI components must be operable by all users |
| **Understandable** | Information and UI operation must be understandable |
| **Robust** | Content must be robust enough for assistive technologies |

#### Conformance Levels

| Level | Requirements | Legal Status |
|-------|--------------|--------------|
| A | Minimum accessibility | Basic requirement |
| AA | Recommended standard | **Legal standard** (ADA, EAA) |
| AAA | Highest accessibility | Often not fully achievable |

#### WCAG 2.2 New Success Criteria (2023)

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| 2.4.11 Focus Not Obscured (Minimum) | AA | Focused element not fully hidden |
| 2.4.12 Focus Not Obscured (Enhanced) | AAA | Focused element not partially hidden |
| 2.4.13 Focus Appearance | AAA | 2px outline, 3:1 contrast |
| 2.5.7 Dragging Movements | AA | Single-pointer alternative |
| 2.5.8 Target Size (Minimum) | AA | **24×24 CSS pixels minimum** |
| 3.2.6 Consistent Help | A | Help in consistent location |
| 3.3.7 Redundant Entry | A | Don't re-ask for same info |
| 3.3.8 Accessible Authentication (Minimum) | AA | No cognitive tests for login |
| 3.3.9 Accessible Authentication (Enhanced) | AAA | No object/content recognition |

#### Legal Requirements (2025)

| Region | Law | Requirement |
|--------|-----|-------------|
| EU | European Accessibility Act (June 2025) | WCAG 2.1 AA |
| US | ADA Title II (April 2024) | WCAG 2.1 AA (state/local gov) |
| US | ADA (private sector) | WCAG 2.1 AA (de facto standard) |

#### ARIA Best Practices

**The First Rule of ARIA:**
> "If you can use a native HTML element with the semantics and behavior you require, instead of re-purposing an element and adding ARIA, then do so."

**Key ARIA Attributes:**

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `aria-label` | Accessible name | `<button aria-label="Close dialog">×</button>` |
| `aria-labelledby` | Reference another element | `<div aria-labelledby="heading-id">` |
| `aria-describedby` | Additional description | `<input aria-describedby="help-text">` |
| `aria-expanded` | Expandable state | `<button aria-expanded="false">Menu</button>` |
| `aria-hidden` | Hide from AT | `<span aria-hidden="true">👋</span>` |
| `aria-live` | Announce updates | `<div aria-live="polite">Status message</div>` |

**Landmark Roles:**

```html
<header role="banner">
<nav role="navigation">
<main role="main">
<aside role="complementary">
<footer role="contentinfo">
```

---

### 3. Responsive Design Patterns

Sources:
- [Responsive Design Best Practices - UXPin](https://www.uxpin.com/studio/blog/best-practices-examples-of-excellent-responsive-design/)
- [9 Responsive Design Best Practices 2025 - NextNative](https://nextnative.dev/blog/responsive-design-best-practices)
- [Mobile-First Development Guide - EngageCoders](https://www.engagecoders.com/responsive-web-design-mobile-first-development-best-practices-2025-guide/)
- [Responsive Design Breakpoints 2025 - DEV Community](https://dev.to/gerryleonugroho/responsive-design-breakpoints-2025-playbook-53ih)

#### Traffic Statistics (2025-2026)
- **Mobile**: 59-67% of all web traffic
- **Desktop**: 33-41% of all web traffic

#### Mobile-First Approach

```css
/* Mobile-first: Start with base styles */
.container {
  padding: 1rem;
}

/* Then add complexity for larger screens */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 3rem;
  }
}
```

#### Recommended Breakpoints (2025)

| Breakpoint | Size | Target |
|------------|------|--------|
| xs | 320px | Small phones |
| sm | 640px | Large phones |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

#### Modern CSS Techniques

**Fluid Typography with clamp():**
```css
/* Fluid font size: min 1rem, preferred 2vw + 1rem, max 2rem */
h1 {
  font-size: clamp(1rem, 2vw + 1rem, 2rem);
}
```

**Container Queries (2025 mainstream):**
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

**CSS Grid for Layouts:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
```

#### Image Optimization

```html
<!-- Responsive images with srcset -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px,
         (max-width: 1000px) 800px,
         1200px"
  alt="Description"
  loading="lazy"
>

<!-- Modern formats -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

#### Touch-Friendly Design

- **Minimum touch target**: 44×44px (Apple), 48×48dp (Android), 24×24px (WCAG 2.2 AA)
- **Adequate spacing**: Prevent accidental taps
- **Test both orientations**: Portrait and landscape

---

### 4. Color Theory and Contrast Ratios

Sources:
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Color Contrast Accessibility Guide - AllAccessible](https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025)
- [Understanding WCAG Contrast - W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Color Contrast Best Practices - DeveloperUX](https://developerux.com/2025/07/28/best-practices-for-accessible-color-contrast-in-ux/)

#### WCAG Contrast Requirements

| Content Type | Level AA | Level AAA |
|-------------|----------|-----------|
| Normal text (< 18pt / 24px) | 4.5:1 | 7:1 |
| Large text (≥ 18pt / ≥ 14pt bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

#### Contrast Ratio Examples

| Ratio | Example | Passes |
|-------|---------|--------|
| 21:1 | Black on white | AAA |
| 7:1 | #595959 on white | AAA |
| 4.5:1 | #767676 on white | AA |
| 3:1 | #949494 on white | Large text AA |
| 2:1 | #AAAAAA on white | Fails |

#### The #1 Accessibility Problem

> Color contrast is the #1 accessibility violation on the web — affecting **83.6% of all websites** according to WebAIM's 2024 Million analysis.

#### Color Palette Guidelines

```css
:root {
  /* Ensure sufficient contrast for all combinations */
  --color-text-primary: #1a1a1a;      /* 16:1 on white */
  --color-text-secondary: #4a4a4a;    /* 9:1 on white */
  --color-text-muted: #6b6b6b;        /* 5.5:1 on white - AA */

  /* Error/Success states */
  --color-error: #c41e3a;             /* Test against backgrounds */
  --color-success: #0f7b0f;           /* Test against backgrounds */

  /* Interactive elements */
  --color-link: #0066cc;              /* 5.9:1 on white - AA */
  --color-link-visited: #551a8b;      /* 10:1 on white - AAA */
}
```

#### Non-Text Element Contrast

WCAG 2.1 expanded contrast rules to include:
- Form field borders
- Button boundaries
- Icons conveying information
- Focus indicators
- Charts and graphs

```css
/* Button with sufficient border contrast */
.button-outline {
  background: transparent;
  border: 2px solid #0066cc;  /* 3:1+ against background */
  color: #0066cc;             /* 4.5:1+ for text */
}

/* Form field with visible border */
input {
  border: 1px solid #6b6b6b;  /* 3:1+ against white */
}
```

#### Testing Tools

| Tool | Type | Features |
|------|------|----------|
| [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) | Web | Quick checks, WCAG levels |
| [Stark Plugin](https://www.getstark.co/) | Figma/Sketch | Design tool integration |
| [WAVE](https://wave.webaim.org/) | Browser extension | Full page analysis |
| [Tanaguru Contrast Finder](https://contrast-finder.tanaguru.com/) | Web | Suggests compliant alternatives |
| axe DevTools | Browser extension | Automated testing |

---

### 5. Typography Best Practices

Sources:
- [Typography Guide 2025 - adoc Studio](https://www.adoc-studio.app/blog/typography-guide)
- [Typography - U.S. Web Design System](https://designsystem.digital.gov/components/typography/)
- [Modern Web Typography 2025 - FrontendTools](https://www.frontendtools.tech/blog/modern-web-typography-techniques-2025-readability-guide)
- [Website Font Size Guide 2025 - ScopeDesign](https://scopedesign.com/website-font-size-guide-2025-ux-typography-best-practices/)

#### Font Size Guidelines

| Element | Desktop | Mobile | Notes |
|---------|---------|--------|-------|
| Body text | 16-20px | 16px minimum | WCAG requirement |
| H1 | 32-48px | 28-36px | Use sparingly |
| H2 | 24-32px | 22-28px | Section headers |
| H3 | 20-24px | 18-22px | Subsections |
| Small/Caption | 12-14px | 12px minimum | Limited use |
| Interactive text | 18-24px | 16-20px | For long-form reading |

#### Line Height (Leading)

| Content Type | Line Height | Ratio |
|--------------|-------------|-------|
| Headings (1-2 lines) | 1.0-1.35 | Tight |
| Body text | 1.5-1.8 | Comfortable |
| UI labels | 1.2-1.4 | Moderate |
| Long-form reading | 1.6-2.0 | Generous |

```css
body {
  line-height: 1.6;  /* 160% - comfortable reading */
}

h1, h2, h3 {
  line-height: 1.2;  /* Tighter for headings */
}
```

#### Line Length (Measure)

**Optimal**: 50-75 characters per line
**Acceptable range**: 45-90 characters per line

```css
.prose {
  max-width: 65ch;  /* ch = width of '0' character */
}
```

#### Fluid Typography

```css
/* Modern approach with clamp() */
:root {
  --font-size-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --font-size-lg: clamp(1.25rem, 1vw + 1rem, 1.5rem);
  --font-size-xl: clamp(1.5rem, 2vw + 1rem, 2.5rem);
}

body {
  font-size: var(--font-size-base);
}
```

#### Font Pairing Principles

1. **Contrast**: Pair serif with sans-serif
2. **Limit typefaces**: 2-3 maximum per project
3. **Limit weights**: 3 weights maximum for performance
4. **Hierarchy**: Clear distinction between heading and body

#### Recommended System Font Stacks

```css
/* Modern system font stack */
body {
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Oxygen,
    Ubuntu,
    Cantarell,
    'Fira Sans',
    'Droid Sans',
    'Helvetica Neue',
    sans-serif;
}

/* Monospace for code */
code {
  font-family:
    ui-monospace,
    SFMono-Regular,
    'SF Mono',
    Menlo,
    Consolas,
    'Liberation Mono',
    monospace;
}
```

#### Accessibility Considerations

- **Allow 200% zoom**: Use relative units (rem/em)
- **Avoid thin weights**: 300 and below for small text
- **Text alignment**: Left-aligned for LTR languages (avoid justified)
- **Sufficient contrast**: 4.5:1 minimum for body text

---

### 6. Design Tokens and CSS Variables

Sources:
- [Design Tokens Guide - Penpot](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/)
- [Design Tokens - U.S. Web Design System](https://designsystem.digital.gov/design-tokens/)
- [Design Tokens Best Practices - Substack](https://designtokens.substack.com/p/using-design-tokens-as-variables)
- [Figma Variables 2025/2026 Playbook](https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66)

#### Token Hierarchy

```
Primitive Tokens → Semantic Tokens → Component Tokens
     ↓                   ↓                  ↓
  #0066cc        color-primary      button-background
```

#### Implementation Pattern

```css
:root {
  /* ============================================
     PRIMITIVE TOKENS (Raw values)
     ============================================ */

  /* Colors */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-700: #1d4ed8;
  --color-gray-50: #f9fafb;
  --color-gray-900: #111827;

  /* Spacing */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-6: 24px;
  --spacing-8: 32px;

  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;

  /* ============================================
     SEMANTIC TOKENS (Purpose-based)
     ============================================ */

  /* Colors */
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-background: var(--color-gray-50);
  --color-surface: #ffffff;
  --color-primary: var(--color-blue-500);
  --color-primary-hover: var(--color-blue-700);

  /* Spacing */
  --spacing-component: var(--spacing-4);
  --spacing-section: var(--spacing-8);

  /* ============================================
     COMPONENT TOKENS (Specific components)
     ============================================ */

  --button-padding-x: var(--spacing-4);
  --button-padding-y: var(--spacing-2);
  --button-background: var(--color-primary);
  --button-text: #ffffff;
  --card-padding: var(--spacing-4);
  --card-radius: var(--spacing-2);
}
```

#### Dark Mode with Tokens

```css
/* Light mode (default) */
:root {
  --color-background: #ffffff;
  --color-surface: #f9fafb;
  --color-text-primary: #111827;
  --color-text-secondary: #4b5563;
}

/* Dark mode */
[data-theme="dark"],
.dark {
  --color-background: #111827;
  --color-surface: #1f2937;
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
}

/* System preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-background: #111827;
    --color-surface: #1f2937;
    --color-text-primary: #f9fafb;
    --color-text-secondary: #9ca3af;
  }
}
```

#### Best Practices

1. **Always set fallback values**: `var(--color-primary, #0066cc)`
2. **Use semantic naming**: `--color-error` not `--color-red`
3. **Define in `:root`**: Make tokens globally available
4. **Document tokens**: Maintain a living style guide
5. **Use references/aliases**: Create relationships between tokens

#### Benefits of Design Tokens

| Benefit | Description |
|---------|-------------|
| Velocity | Effortless updates across brands, themes, products |
| Reliability | Reduces human error, ensures consistency |
| Accessibility | Guarantees standards compliance from the start |
| Automation | Enables AI-driven pipelines, automated audits |
| Collaboration | Designers and developers speak the same language |

---

### 7. User Testing and Heuristic Evaluation

Sources:
- [10 Usability Heuristics - Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [How to Conduct Heuristic Evaluation - NN/g](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)
- [Heuristic Evaluation Guide - Adam Fard](https://adamfard.com/blog/heuristic-evaluation)
- [Best UX Research Methods 2025 - ProCreator](https://procreator.design/blog/best-ux-research-methods/)

#### Nielsen's 10 Usability Heuristics

| # | Heuristic | Description |
|---|-----------|-------------|
| 1 | **Visibility of System Status** | Keep users informed through appropriate feedback |
| 2 | **Match System & Real World** | Use familiar language and concepts |
| 3 | **User Control & Freedom** | Provide undo/redo and clear exits |
| 4 | **Consistency & Standards** | Follow platform conventions |
| 5 | **Error Prevention** | Design to prevent problems |
| 6 | **Recognition over Recall** | Make options visible, minimize memory load |
| 7 | **Flexibility & Efficiency** | Accelerators for experts, simplicity for novices |
| 8 | **Aesthetic & Minimalist Design** | Remove unnecessary information |
| 9 | **Help Users with Errors** | Plain language, suggest solutions |
| 10 | **Help & Documentation** | Easy to search, task-focused |

#### Conducting Heuristic Evaluation

**When to Use:**
- After wireframes/prototypes, before visual design
- During competitor analysis
- Early design phase (catch issues before they're embedded)

**Evaluator Count:**
- 1 evaluator: ~35% of issues found
- 3-5 evaluators: Comprehensive assessment
- 5-8 evaluators: 80%+ of usability issues identified

**Process:**
1. Evaluators work **independently** (no influence)
2. Each evaluator reviews against all 10 heuristics
3. Document issues with severity ratings
4. Consolidate findings
5. Prioritize and address

**Severity Scale:**

| Rating | Severity | Action |
|--------|----------|--------|
| 0 | Not a usability problem | No action |
| 1 | Cosmetic only | Fix if time permits |
| 2 | Minor | Low priority |
| 3 | Major | High priority |
| 4 | Catastrophic | Must fix before release |

#### Cost Comparison

> Heuristic evaluation can cut costs by **78%** compared to usability testing.

> Heuristic evaluation identifies, on average, **50%** of usability problems found in user testing.

#### Complementary Methods

| Method | Best For | Timing |
|--------|----------|--------|
| Heuristic Evaluation | Expert review, budget constraints | Pre-development |
| Usability Testing | Real user behavior | Prototype/Production |
| Tree Testing | Navigation structure | Information architecture |
| A/B Testing | Comparing alternatives | Production |
| Field Studies | Real-world context | Discovery/Validation |

#### Best Practice
> "Don't limit yourself to just one method. Combining heuristic analysis with cognitive walkthrough and user testing ensures your product's design is up to standard — from both a design expert's and an end user's point of view."

---

### 8. Common UI/UX Anti-Patterns to Avoid

Sources:
- [Dark Patterns Examples - Eleken](https://www.eleken.co/blog-posts/dark-patterns-examples)
- [Deceptive Patterns in UX - Nielsen Norman Group](https://www.nngroup.com/articles/deceptive-patterns/)
- [10 Dark Patterns to Avoid - Bejamas](https://bejamas.com/blog/10-dark-patterns-in-ux-design)
- [Dark Patterns in UX - CareerFoundry](https://careerfoundry.com/en/blog/ux-design/dark-patterns-ux/)

#### What Are Dark Patterns?

> "A Dark Pattern is an interface design technique intentionally created to deceive, manipulate, or pressure users into making decisions they probably wouldn't make if the information were presented clearly and transparently."

Coined by Harry Brignull in 2010.

#### 12 Types of Dark Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Roach Motel** | Easy to get in, hard to get out | Easy signup, impossible cancellation |
| **Confirmshaming** | Guilt-tripping to influence decisions | "No thanks, I don't want to save money" |
| **Bait and Switch** | Promise one thing, deliver another | Free trial that auto-converts to paid |
| **Hidden Costs** | Reveal fees at checkout | Shipping shown only at final step |
| **Sneak into Basket** | Add items without consent | Pre-checked add-ons |
| **Forced Continuity** | Auto-renew without clear notice | Subscription continues after trial |
| **Friend Spam** | Request contacts, spam them | "Invite friends" that mass-emails |
| **Disguised Ads** | Ads that look like content | "Download" buttons that are ads |
| **Privacy Zuckering** | Confuse users into sharing data | Complex privacy settings |
| **Misdirection** | Draw attention away from important info | Highlighted "Accept All" cookies |
| **Trick Questions** | Confusing wording | Double negatives in opt-outs |
| **Fake Urgency/FOMO** | False scarcity or time pressure | "Only 2 left!" (always) |

#### Sludge Pattern

> "Any aspect of choice architecture consisting of friction that makes it harder for people to obtain an outcome that will make them better off."

Example: Cookie consent requiring multiple clicks to reject tracking.

#### Impact on Vulnerable Groups

- People with low digital literacy
- Users with cognitive impairments
- Visually impaired users (low-contrast disclaimers)
- Elderly users (unclear prompts)

#### Legal Consequences

| Region | Law | Penalty |
|--------|-----|---------|
| EU | GDPR, Digital Services Act | Significant fines |
| California | CPRA | 30-day fix window, then penalties |
| US | FTC enforcement | Case-by-case action |

#### Why Dark Patterns Backfire

> "Deceptive patterns rarely show their full impact immediately — they accumulate over time. After a week, users might just feel minor irritation. After three months, that irritation becomes distrust. And after a year, it often transforms into user churn and negative word-of-mouth."

#### Ethical Alternatives

| Dark Pattern | Ethical Alternative |
|--------------|---------------------|
| Pre-checked boxes | Unchecked by default |
| Hidden unsubscribe | Clear, easy cancellation |
| Fake urgency | Honest availability info |
| Confirmshaming | Neutral option text |
| Cookie walls | Clear accept/reject with equal prominence |

---

## Audit Checklist Summary

### Critical (Must Have)

- [ ] **Color contrast**: 4.5:1 for text, 3:1 for UI components
- [ ] **Touch targets**: Minimum 24×24px (WCAG 2.2 AA), ideally 44×44px
- [ ] **Focus indicators**: Visible, 2px minimum, 3:1 contrast
- [ ] **Keyboard navigation**: All interactive elements accessible
- [ ] **Alt text**: All meaningful images have descriptions
- [ ] **Semantic HTML**: Use native elements before ARIA
- [ ] **No dark patterns**: Transparent, ethical design
- [ ] **Responsive**: Works on mobile devices (test portrait + landscape)
- [ ] **Font size**: 16px minimum for body text
- [ ] **Error handling**: Clear messages with recovery paths

### Important (Should Have)

- [ ] **Design tokens**: Centralized CSS variables for theming
- [ ] **Consistent spacing**: Use 4px/8px grid system
- [ ] **Component library**: Atomic design structure
- [ ] **Line height**: 1.5-1.8 for body text
- [ ] **Line length**: 45-90 characters per line
- [ ] **ARIA landmarks**: Header, nav, main, footer marked up
- [ ] **Skip links**: "Skip to main content" for keyboard users
- [ ] **Form labels**: All inputs have associated labels
- [ ] **Loading states**: Visible feedback for async operations
- [ ] **Error prevention**: Validation before submission

### Recommended (Nice to Have)

- [ ] **Dark mode**: System preference support with manual toggle
- [ ] **Reduced motion**: Respect `prefers-reduced-motion`
- [ ] **Container queries**: Component-level responsiveness
- [ ] **Fluid typography**: clamp() for responsive text
- [ ] **Image optimization**: WebP/AVIF, srcset, lazy loading
- [ ] **Focus-visible**: Use `:focus-visible` for cleaner focus styles
- [ ] **Heuristic evaluation**: Regular expert reviews
- [ ] **AAA contrast**: 7:1 for critical content
- [ ] **Print styles**: Usable when printed
- [ ] **Storybook documentation**: Component visual documentation

---

## Sources

### Upstream Repositories
- [Dammyjay93/claude-design-engineer](https://github.com/Dammyjay93/claude-design-engineer)
- [obra/superpowers](https://github.com/obra/superpowers)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

### Accessibility Standards
- [WCAG 2 Overview - W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [What's New in WCAG 2.2 - W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [ARIA Overview - W3C WAI](https://www.w3.org/WAI/standards-guidelines/aria/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### Design Systems
- [Atomic Design - Brad Frost](https://atomicdesign.bradfrost.com/chapter-2/)
- [U.S. Web Design System - Design Tokens](https://designsystem.digital.gov/design-tokens/)
- [Best Practices for Scalable Component Libraries - UXPin](https://www.uxpin.com/studio/blog/best-practices-for-scalable-component-libraries/)

### Typography
- [Typography Guide 2025 - adoc Studio](https://www.adoc-studio.app/blog/typography-guide)
- [U.S. Web Design System - Typography](https://designsystem.digital.gov/components/typography/)
- [Font Size Guidelines - Learn UI Design](https://www.learnui.design/blog/mobile-desktop-website-font-size-guidelines.html)

### Responsive Design
- [Responsive Design Best Practices - UXPin](https://www.uxpin.com/studio/blog/best-practices-examples-of-excellent-responsive-design/)
- [Mobile-First Development Guide - EngageCoders](https://www.engagecoders.com/responsive-web-design-mobile-first-development-best-practices-2025-guide/)

### Usability & Testing
- [10 Usability Heuristics - Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [How to Conduct Heuristic Evaluation - NN/g](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)
- [Heuristic Evaluation Guide - Adam Fard](https://adamfard.com/blog/heuristic-evaluation)

### Anti-Patterns
- [Deceptive Patterns in UX - Nielsen Norman Group](https://www.nngroup.com/articles/deceptive-patterns/)
- [Dark Patterns Examples - Eleken](https://www.eleken.co/blog-posts/dark-patterns-examples)
