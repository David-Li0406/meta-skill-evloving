---
name: elementary
description: Token-based design system with standardized CSS custom property names, multiple theme implementations (polished with light/dark mode, sketch), and optional component patterns. Use for themeable interfaces, design system compliance, or switching between visual fidelity levels without code changes.
license: MIT
metadata:
  version: "1.0.0"
  author: million-views (https://m5nv.com)
compatibility: Designed for reactive-md skill and React frameworks (Next.js, Remix, Vite)
---

# Elementary Design System

Elementary is a design system comprised of three independent, orthogonal layers:

**Layer 1: Token Naming System**
- Standardized names (`--c-primary`, `--s-4`, ...)
- The unchanging contract
- Used across ALL themes

**Layer 2: Theme Implementations**
- Different VALUES for the same names
- Currently: polished, sketch
- Future: custom themes, brand themes

**Layer 3: Component Classes**
- Optional pre-built patterns
- Uses Layer 1 token names
- Works with ANY Layer 2 theme

**Key Insight**: Token NAMES stay constant across themes; only token VALUES change. This allows switching visual fidelity by changing a single CSS import without touching Layer 1 (token names) or Layer 3 (component code).

## When to Use This Skill

**Token-Based Styling**:
- Design system approach with reusable tokens
- Consistent spacing, colors, and typography across projects
- Themeable interfaces (light/dark mode, fidelity levels)

**Visual Fidelity Control**:
- High-fidelity prototypes (polished, production-ready)
- Low-fidelity wireframes (structural mockups)
- Switch between fidelity levels without code changes

**Component Consistency**:
- Pre-built component patterns for rapid prototyping
- Design system compliance

**Keywords**: Elementary, design tokens, CSS variables, light/dark mode, themeable, high-fidelity, sketch, component classes (wf-btn, wf-card), design system

**Not a Fit For**: Utility-first styling (use Tailwind), quick prototypes without design system constraints, fully custom styling without reusable patterns

## Quick Start

### Import a Theme

```css live
/* Polished (production-ready with light/dark mode) */
@import './assets/elementary/tokens/polished.css';
@import './assets/elementary/components.css';  /* optional */
```

**See**: `references/themes.md` for complete theme documentation

### Installing Elementary Assets

To use Elementary in your own project, install the assets locally:

```bash
# From your project directory
/path/to/elementary/scripts/elementary.mjs install .
```

This creates `assets/elementary/` in your project with the same structure as this skill.

### Component Classes First, Tokens for Custom Components

**Primary Approach: Use Component Classes**
```jsx live
<article className="wf-card">
  <h3 className="title">Card Title</h3>
  <p className="description">Card content</p>
</article>
```

**Tiny Tweaks: Inline Style Overrides** (1-2 properties only):
```jsx live
<article className="wf-card" style={{
  backgroundColor: 'var(--c-slate-100)'  /* Single override OK */
}}>
  <h3 className="title">Card with custom background</h3>
  <p className="description">Override theme for quick escape</p>
</article>
```

**Custom Components: Use Tokens in CSS** (when no component class exists):
```css live
/* Import Elementary tokens first */
@import './assets/elementary/tokens/polished.css';

/* Create your own class when `components.css` doesn't have what you need */
.custom-alert {
  padding: var(--s-4);
  border-radius: var(--r-card);
  background-color: var(--bg-surface);
  border-left: 4px solid var(--c-primary);
  color: var(--c-text);
  & .title {
    font: var(--t-heading);
  }
}
```

```jsx live
<article className="custom-alert">
  <h3 className="title">Custom Alert</h3> 
  <p>This component doesn't exist in components.css, 
  so we created a CSS class using Elementary tokens.
  </p>
</article>
```

**Rule**: Component classes → Tiny inline tweaks (1-2 properties) → Custom CSS classes with tokens. Never extensive inline styles.

**See**: `references/components.md` for all available component classes

## Core Concepts

### Layer 1: Token Naming System (The Contract)

Standardized names used across ALL themes:
- `--c-primary`, `--c-secondary` (colors)
- `--bg-surface`, `--bg-overlay` (backgrounds)
- `--s-4`, `--s-6` (spacing: 16px, 24px)
- `--r-btn`, `--r-card` (radius)

**Token Hierarchy**:
- **Primitives**: Raw scales (`--s-4`, `--c-slate-500`) - use in theme files
- **Semantics**: Intent-based (`--c-primary`, `--bg-surface`) - use in CSS classes for custom components

**When to Use Design Tokens**:
- Creating custom CSS classes for components not in component-library.css
- Building your own design system on top of Elementary
- Tiny inline overrides (1-2 properties max)

**When NOT to Use Design Tokens**:
- Component classes already exist (use wf-btn, wf-card, etc.)
- Would result in >2 inline style properties (create a CSS class instead)

**See**: `references/token-system.md` for complete token taxonomy

### Layer 2: Theme Implementations (The Values)

Different VALUE assignments to the same token NAMES:

**Polished**:
- Semantic colors with light/dark mode
- Professional typography
- Refined shadows
- Production-ready

**Sketch**:
- Grayscale palette
- Monospace typography
- Minimal shadows
- Structural focus

**Theme Switching**: Change import path only - all code remains unchanged.

**See**: `references/themes.md` for theme characteristics and usage

### Layer 3: Component Classes (Optional Patterns)

Pre-built patterns in `assets/components.css`:
- `.wf-btn`, `.wf-card`, `.wf-hero` (UI components)
- `.title`, `.description`, `.actions` (semantic children)
- Works with ANY Layer 2 theme

**See**: `references/components.md` for all available components

## Critical Rules

### ✅ DO

**Use Component Classes First**:
```jsx
<div className="wf-card">
<button className="wf-btn primary">
```

**Use Tokens in CSS Classes** (for custom components):
```css
.my-custom-alert {
  color: var(--c-primary);
  background-color: var(--bg-surface);
  padding: var(--s-4);
}
```

**Inline Overrides for Tiny Tweaks** (1-2 properties max):
```jsx
<div className="wf-card" style={{ backgroundColor: 'var(--c-accent)' }}>
```

**Change Themes via Import**:
```css
/* Switch from polished to sketch */
@import './assets/elementary/tokens/sketch.css';
```

### ❌ DON'T

**Mix Tailwind with Elementary**:
```jsx
{/* WRONG */}
<div className="wf-card p-4 flex gap-2">
```

**Invent Component Classes**:
```jsx
{/* WRONG - .wf-dashboard-card doesn't exist */}
<div className="wf-dashboard-card">
```

**Use Primitive Tokens in Component Code**:
```css
/* WRONG - use semantics instead */
color: var(--c-slate-700);
```

**Hardcode Values**:
```css
/* WRONG - defeats the token system */
padding: 16px;
color: #333333;
```

**Excessive Inline Styles** (>2 properties):
```jsx
{/* WRONG - code smell, create a CSS class instead */}
<div style={{
  padding: 'var(--s-6)',
  borderRadius: 'var(--r-card)',
  backgroundColor: 'var(--bg-surface)',
  border: '1px solid var(--c-border)'
}}>
```

## Light/Dark Mode (Polished Theme Only)

Polished theme uses `light-dark()` CSS function for automatic theming:

**User Control**:
```javascript
// Toggle theme
document.documentElement.style.colorScheme = 'dark';  // or 'light'
```

**System Preference** (Automatic):
```css
/* Already set in polished.css */
:root { color-scheme: light dark; }
```

**Note**: Sketch theme does not support light/dark mode (intentionally grayscale).

**See**: `references/themes.md` for browser compatibility and fallbacks

## Cross-Skill Composition

Elementary works standalone OR composed with other skills:

**With reactive-md**:
```css
/* From reactive-md document */
@import './assets/elementary/tokens/polished.css';
@import './assets/elementary/components.css';
```

**With React frameworks**:
```css
/* Next.js, Remix, Vite - adjust relative path as needed */
@import './assets/elementary/tokens/polished.css';
```

## Discovering Resources

**Token Names** (Layer 1):
- Read `references/token-system.md` - Complete token taxonomy
- Semantic vs primitive hierarchy
- "Ink & Paper" metaphor

**Theme Values** (Layer 2):
- Read `references/themes.md` - All available themes
- Polished vs sketch characteristics
- Light/dark mode implementation

**Component Classes** (Layer 3):
- Read `references/components.md` - All available classes
- Semantic child elements
- Component-level token patterns

**Usage Examples**:
- `references/recipes/` - Common patterns (buttons, cards, dashboards, landing pages, settings pages)

**Installation Tool**:
```bash
# Install Elementary assets to current directory
/path/to/elementary/scripts/elementary.mjs install .
```

**Discovery Tool** (if available):
```javascript
// Discover component classes and tokens
list_design_classes({
  css_file: "assets/elementary/components.css",
  include_tokens: true,
  theme: "polished"
})
```
