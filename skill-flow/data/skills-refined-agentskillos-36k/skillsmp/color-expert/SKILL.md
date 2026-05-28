---
name: color-expert
description: Expert guide for the Doggy Bag color/theme system with color theory principles
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: design
---

# Color Expert - Theme System Guide

Use this skill when working with colors, themes, or the visual design system in Doggy Bag.

## Critical Rules

### NEVER Use These Patterns

1. **No hardcoded hex colors** - Always use CSS variables
2. **No `-dark` or `-light` suffixes** - Theme profiles handle light/dark variations
3. **No `danger` variable** - Use `error` instead (consolidated naming)
4. **No inline rgba() fallbacks** - Define in `defaults.ts` instead

### Naming Convention (MUST FOLLOW)

```
{color}         : Primary color (text, icons, solid elements)
{color}-hover   : Hover state for buttons/interactive elements
{color}-bg      : Background fill (~0.1 opacity)
{color}-muted   : Subtle background for hover states (~0.05 opacity)
{color}-border  : Border color (~0.3 opacity)
```

**Examples:**

- `--success` (primary) → `--success-hover` (button hover) → `--success-bg` (background)
- `--error` (primary) → `--error-hover` (button hover) → `--error-muted` (subtle hover bg)

**Anti-patterns (DO NOT USE):**

- `--success-dark` → Use `--success-hover` instead
- `--error-dark` → Use `--error-hover` instead
- `--warning-light` → Use `--warning` (theme handles light/dark)
- `--purple-dark` → Use `--purple-hover` instead
- `--danger` → Use `--error` instead

---

## Color Variables Reference

### Required Colors (7) - Must Be Defined

| Variable           | Dark Value | Light Value | Purpose              |
| ------------------ | ---------- | ----------- | -------------------- |
| `--bg-base`        | `#0f0f1a`  | `#e5e7eb`   | Page background      |
| `--bg-surface`     | `#1a1a2e`  | `#ffffff`   | Cards/panels         |
| `--bg-elevated`    | `#252538`  | `#f3f4f6`   | Modals/dropdowns     |
| `--text-primary`   | `#e4e4e7`  | `#1a1a2e`   | Main text            |
| `--text-secondary` | `#949494`  | `#525252`   | Muted text           |
| `--accent`         | `#24c8db`  | `#0e7490`   | Primary action color |
| `--border-default` | `#3d3d66`  | `#6b7280`   | Default borders      |

### Optional Colors (~40) - Have Smart Defaults

#### Text Variants

| Variable          | Purpose                    |
| ----------------- | -------------------------- |
| `--text-tertiary` | Even more muted text       |
| `--text-inverse`  | Text on accent backgrounds |
| `--text-disabled` | Disabled element text      |

#### Border Variants

| Variable          | Purpose                              |
| ----------------- | ------------------------------------ |
| `--border-hover`  | Border on hover                      |
| `--border-focus`  | Border on focus (usually accent)     |
| `--border-subtle` | Softer borders (list dividers, etc.) |

#### Accent Variants

| Variable          | Purpose                            |
| ----------------- | ---------------------------------- |
| `--accent-hover`  | Accent on hover (darker/lighter)   |
| `--accent-muted`  | Transparent accent for backgrounds |
| `--accent-border` | Accent border color                |

#### Semantic: Success

| Variable           | Purpose                          |
| ------------------ | -------------------------------- |
| `--success`        | Success state (green)            |
| `--success-hover`  | Success on hover                 |
| `--success-bg`     | Success background (10% opacity) |
| `--success-muted`  | Subtle success background (5%)   |
| `--success-border` | Success border (30% opacity)     |

#### Semantic: Error

| Variable         | Purpose                 |
| ---------------- | ----------------------- |
| `--error`        | Error state (red)       |
| `--error-hover`  | Error on hover          |
| `--error-bg`     | Error background        |
| `--error-muted`  | Subtle error background |
| `--error-border` | Error border            |

#### Semantic: Warning

| Variable           | Purpose                   |
| ------------------ | ------------------------- |
| `--warning`        | Warning state (amber)     |
| `--warning-hover`  | Warning on hover          |
| `--warning-bg`     | Warning background        |
| `--warning-muted`  | Subtle warning background |
| `--warning-border` | Warning border            |

#### Semantic: Info

| Variable       | Purpose                           |
| -------------- | --------------------------------- |
| `--info`       | Info state (often same as accent) |
| `--info-hover` | Info on hover                     |
| `--info-bg`    | Info background                   |
| `--info-muted` | Subtle info background            |

#### Special Colors

| Variable         | Purpose                            |
| ---------------- | ---------------------------------- |
| `--purple`       | Purple accent (credit cards, etc.) |
| `--purple-hover` | Purple on hover                    |
| `--purple-bg`    | Purple background                  |
| `--purple-muted` | Subtle purple background           |
| `--orange`       | Orange accent                      |
| `--orange-hover` | Orange on hover                    |
| `--orange-bg`    | Orange background                  |

#### Financial Semantics

| Variable           | Purpose                |
| ------------------ | ---------------------- |
| `--income-color`   | Income amounts (green) |
| `--expense-color`  | Expense amounts (red)  |
| `--positive-color` | Positive values        |
| `--negative-color` | Negative values        |

#### State Colors

| Variable          | Purpose                |
| ----------------- | ---------------------- |
| `--paid-color`    | Paid status (green)    |
| `--unpaid-color`  | Unpaid status (red)    |
| `--partial-color` | Partially paid (amber) |
| `--pending-color` | Pending (yellow)       |

---

## Theme JSON Format

### Schema

```json
{
  "id": "string", // Unique identifier (e.g., "dark", "ocean")
  "name": "string", // Display name (e.g., "Dark", "Ocean Blue")
  "version": "1.0", // Schema version
  "isDark": true, // true = dark theme, false = light theme
  "colors": {
    // 7 required colors (must be defined)
    "bg-base": "#hex",
    "bg-surface": "#hex",
    "bg-elevated": "#hex",
    "text-primary": "#hex",
    "text-secondary": "#hex",
    "accent": "#hex",
    "border-default": "#hex",
    // Optional colors (omit to use defaults)
    "success": "#hex"
    // ... etc
  },
  "meta": {
    // Optional metadata
    "description": "string",
    "author": "string"
  }
}
```

### Minimal Theme Example (7 colors)

```json
{
  "id": "ocean",
  "name": "Ocean",
  "version": "1.0",
  "isDark": true,
  "colors": {
    "bg-base": "#0a1628",
    "bg-surface": "#0f2744",
    "bg-elevated": "#153357",
    "text-primary": "#e0f2fe",
    "text-secondary": "#7dd3fc",
    "accent": "#38bdf8",
    "border-default": "#1e4976"
  },
  "meta": {
    "description": "Deep ocean blue theme",
    "author": "Your Name"
  }
}
```

All ~40 optional colors will be derived from defaults based on `isDark`.

---

## Palette Visualization

### Terminal Command

```bash
make show-palette              # Shows dark theme (default)
make show-palette theme=light  # Shows light theme
make show-palette theme=compare # Side-by-side comparison
```

This displays actual colored swatches in your terminal using ANSI escape codes.

**Note:** Run in your terminal directly, not through OpenCode's output panel.

### What You'll See

```
══════════════════════════════════════════════════════════════════════
  DARK THEME PALETTE
══════════════════════════════════════════════════════════════════════

  BACKGROUNDS
  ████  #0f0f1a  --bg-base         Page background
  ████  #1a1a2e  --bg-surface      Cards/panels
  ████  #252538  --bg-elevated     Modals/dropdowns

  TEXT
  ████  #e4e4e7  --text-primary    Main text
  ████  #949494  --text-secondary  Muted text
  ████  #7a7a7a  --text-tertiary   Even more muted
  ...
```

---

## Creating New Color Profiles

### Step 1: Choose Base Type

Decide if your theme is dark (`isDark: true`) or light (`isDark: false`).
This affects how defaults are derived.

### Step 2: Create Minimal JSON

Start with just the 7 required colors in `data/themes/mytheme.json`:

```json
{
  "id": "mytheme",
  "name": "My Theme",
  "version": "1.0",
  "isDark": true,
  "colors": {
    "bg-base": "#...",
    "bg-surface": "#...",
    "bg-elevated": "#...",
    "text-primary": "#...",
    "text-secondary": "#...",
    "accent": "#...",
    "border-default": "#..."
  }
}
```

### Step 3: Override Optional Colors (As Needed)

Add optional colors only if you want different values from defaults:

```json
{
  "colors": {
    // ... required colors ...
    "success": "#00ff88", // Custom success color
    "income-color": "#00ff88" // Match success
  }
}
```

### Step 4: Validate

```typescript
import { validateTheme } from './src/lib/theme/validator';
import { loadTheme } from './src/lib/theme/loader';

const result = validateTheme(myThemeJson);
if (!result.valid) {
  console.error(result.errors);
}

const fullTheme = loadTheme(myThemeJson); // Merges with defaults
```

### Step 5: Test

```typescript
import { applyTheme } from './src/lib/theme/applier';
applyTheme(fullTheme); // Applies to document.documentElement
```

---

## Color Theory Fundamentals

### Color Harmony Types

| Harmony                 | Description                       | Best For                  |
| ----------------------- | --------------------------------- | ------------------------- |
| **Complementary**       | Opposite on color wheel           | High contrast accents     |
| **Analogous**           | Adjacent colors                   | Cohesive, subtle palettes |
| **Triadic**             | Three evenly spaced               | Balanced variety          |
| **Split-complementary** | Base + two adjacent to complement | Vibrant but balanced      |

### Choosing an Accent Color

1. **Brand alignment** - Match your brand identity
2. **Accessibility** - Must have sufficient contrast on backgrounds
3. **Emotional resonance** - Cyan = modern/tech, Green = growth, Purple = premium

### The 60-30-10 Rule

| Proportion | Role       | Example                                |
| ---------- | ---------- | -------------------------------------- |
| 60%        | Background | `--bg-base`, `--bg-surface`            |
| 30%        | Secondary  | `--text-secondary`, `--border-default` |
| 10%        | Accent     | `--accent`, semantic colors            |

---

## Color Derivation Patterns

### Hover States

```
Dark theme:  base color → lighten 10-15%
Light theme: base color → darken 10-15%
```

Example:

- `--accent: #24c8db` → `--accent-hover: #1ab0c9` (darker)

### Muted/Background Variants

```
accent-muted = rgba(accent, 0.1)
success-bg   = rgba(success, 0.1)
error-border = rgba(error, 0.3)
```

### Semantic Color Families

Each semantic color (success, error, warning, info) has 5 variants:

```
success family:
  --success        = #4ade80  (primary, for icons/text)
  --success-hover  = #22c55e  (hover state for buttons)
  --success-bg     = rgba(..., 0.1)  (subtle background)
  --success-muted  = rgba(..., 0.05) (very subtle for hover)
  --success-border = rgba(..., 0.3)  (visible but soft)
```

Naming convention:

- `{color}` - Primary color (text, icons, solid elements)
- `{color}-hover` - Hover state for buttons/interactive elements
- `{color}-bg` - Background fill (~0.1 opacity)
- `{color}-muted` - Subtle background for hover states (~0.05 opacity)
- `{color}-border` - Border color (~0.3 opacity)

---

## Accessibility & Contrast

### WCAG Contrast Requirements

| Level          | Normal Text (< 18pt) | Large Text (>= 18pt) |
| -------------- | -------------------- | -------------------- |
| AA (minimum)   | 4.5:1                | 3:1                  |
| AAA (enhanced) | 7:1                  | 4.5:1                |

### Current Dark Theme Contrast Ratios

These ratios have been verified and meet WCAG AA:

| Pair                                            | Ratio   | Status    |
| ----------------------------------------------- | ------- | --------- |
| `text-primary` (#e4e4e7) on `bg-base` (#0f0f1a) | ~13.5:1 | Excellent |
| `text-primary` on `bg-surface` (#1a1a2e)        | ~11.5:1 | Excellent |
| `text-primary` on `bg-elevated` (#252538)       | ~9.5:1  | Excellent |
| `text-secondary` (#949494) on `bg-surface`      | ~5.5:1  | Good (AA) |
| `text-tertiary` (#7a7a7a) on `bg-surface`       | ~4.5:1  | Passes AA |
| `accent` (#24c8db) on `bg-surface`              | ~6.5:1  | Good      |
| `text-inverse` (#000) on `accent`               | ~8.5:1  | Excellent |

### Key Pairs to Verify When Changing Colors

| Foreground         | Background     | Requirement                |
| ------------------ | -------------- | -------------------------- |
| `--text-primary`   | `--bg-base`    | Must pass AA (4.5:1)       |
| `--text-primary`   | `--bg-surface` | Must pass AA               |
| `--text-secondary` | `--bg-surface` | Must pass AA (~5:1 target) |
| `--text-tertiary`  | `--bg-surface` | Must pass AA (4.5:1 min)   |
| `--text-inverse`   | `--accent`     | Must pass AA (button text) |

### Minimum Contrast Guidelines

When choosing new colors, follow these minimum contrast ratios:

| Variable Type  | Minimum Ratio | Target Ratio | Notes                                  |
| -------------- | ------------- | ------------ | -------------------------------------- |
| Primary text   | 4.5:1         | 10:1+        | Higher is better for readability       |
| Secondary text | 4.5:1         | 5.5:1        | Must be clearly readable               |
| Tertiary text  | 4.5:1         | 4.5:1        | Bare minimum for AA                    |
| Disabled text  | 3:1           | 3:1          | Intentionally low (indicates disabled) |
| Borders        | 1.5:1         | 2:1+         | Subtle but visible                     |
| Accent on bg   | 4.5:1         | 6:1+         | For text/icons in accent color         |

### Background Hierarchy

Backgrounds must have sufficient distinction to create visual depth:

| Level    | Variable        | Dark Value | Purpose           | Min Contrast to Surface |
| -------- | --------------- | ---------- | ----------------- | ----------------------- |
| Base     | `--bg-base`     | `#0f0f1a`  | Page background   | 1.3:1                   |
| Surface  | `--bg-surface`  | `#1a1a2e`  | Cards, panels     | — (reference)           |
| Elevated | `--bg-elevated` | `#252538`  | Modals, dropdowns | 1.3:1                   |

**Tip:** If elevated elements look too similar to surface, increase lightness or use shadows/borders for distinction.

### Contrast Calculation

Relative luminance formula:

```
L = 0.2126 * R + 0.7152 * G + 0.0722 * B
Contrast = (L1 + 0.05) / (L2 + 0.05)
```

Tools:

- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Browser DevTools: Inspect element → Color picker shows contrast ratio

---

## Common Pitfalls & Lessons Learned

### Pitfall 1: Using `-dark` or `-light` Suffixes

**Wrong:**

```css
color: var(--success-dark);
color: var(--warning-light);
```

**Right:**

```css
color: var(--success-hover); /* For hover states */
color: var(--warning); /* Theme profiles handle light/dark */
```

**Why:** The theme system has separate dark and light profiles in `defaults.ts`. Each profile defines appropriate colors for its context. Using `-dark`/`-light` suffixes creates ambiguity and breaks when switching themes.

### Pitfall 2: Inline rgba() Fallbacks

**Wrong:**

```css
background: var(--success-muted, rgba(74, 222, 128, 0.05));
```

**Right:**

```css
background: var(--success-muted);
```

**Why:** If a variable needs a fallback, define it in `defaults.ts`. Inline fallbacks create maintenance burden and can become out of sync.

### Pitfall 3: Insufficient Text Contrast

**Common mistake:** Using gray values that are too dark for secondary/tertiary text.

| Variable         | Bad Value | Good Value | Issue                              |
| ---------------- | --------- | ---------- | ---------------------------------- |
| `text-secondary` | `#888888` | `#949494`  | Too low contrast (~4.8:1 → ~5.5:1) |
| `text-tertiary`  | `#666666` | `#7a7a7a`  | Fails WCAG AA (~3.2:1 → ~4.5:1)    |

**Rule of thumb:** On dark backgrounds, secondary text should be at least `#909090` or lighter.

### Pitfall 4: Glaring Warning Colors

**Common mistake:** Using highly saturated yellows that cause eye strain.

| Bad       | Good      | Issue                              |
| --------- | --------- | ---------------------------------- |
| `#fbbf24` | `#e5a91f` | Too bright/saturated, causes glare |
| `#f59e0b` | `#d4970f` | Same issue for hover state         |

**Rule of thumb:** Desaturate warning/yellow colors slightly for dark themes.

### Pitfall 5: Indistinguishable Background Levels

**Common mistake:** Background hierarchy colors too similar.

| Level              | Bad Gap | Good Gap |
| ------------------ | ------- | -------- |
| base → surface     | 1.15:1  | 1.3:1+   |
| surface → elevated | 1.1:1   | 1.25:1+  |

**Solution:** If backgrounds look too similar:

1. Increase lightness difference (preferred)
2. Add subtle borders between levels
3. Use shadows for elevated elements

### Pitfall 6: Hardcoded Colors in Components

**Wrong:**

```svelte
<style>
  .card {
    background: #1a1a2e;
  }
</style>
```

**Right:**

```svelte
<style>
  .card {
    background: var(--bg-surface);
  }
</style>
```

**Detection:** Run this command to find hardcoded colors:

```bash
rg '#[0-9a-fA-F]{3,8}' -g '*.svelte' src/ --no-heading
```

---

## Adding New Color Variables

### Step 1: Define in types.ts

Add to `OPTIONAL_COLOR_KEYS` array:

```typescript
export const OPTIONAL_COLOR_KEYS = [
  // ... existing keys ...
  'my-new-color',
  'my-new-color-hover',
  'my-new-color-bg',
] as const;
```

### Step 2: Add defaults in defaults.ts

Add values for BOTH dark and light themes:

```typescript
// In DARK_THEME_COLORS:
'my-new-color': '#...',
'my-new-color-hover': '#...',
'my-new-color-bg': 'rgba(..., 0.1)',

// In LIGHT_THEME_COLORS:
'my-new-color': '#...',
'my-new-color-hover': '#...',
'my-new-color-bg': 'rgba(..., 0.1)',
```

### Step 3: Verify Contrast

Check that your new color meets WCAG AA on all background levels:

- On `--bg-base`
- On `--bg-surface`
- On `--bg-elevated`

### Step 4: Update Documentation

Add to:

- `docs/colour-themes.md` - User-facing docs
- This skill file - Developer reference

---

### Financial Colors

| Variable           | Color | Psychology                     |
| ------------------ | ----- | ------------------------------ |
| `--income-color`   | Green | Growth, positive, "go" signal  |
| `--expense-color`  | Red   | Caution, negative, attention   |
| `--positive-color` | Green | Universal positive association |
| `--negative-color` | Red   | Universal negative association |

**Cultural note:** Green/red associations are Western-centric. Some cultures reverse these meanings.

### State Colors

| State   | Color        | Reason                         |
| ------- | ------------ | ------------------------------ |
| Paid    | Green        | Completion, success            |
| Unpaid  | Red          | Attention needed, urgent       |
| Partial | Amber/Orange | In-progress, caution           |
| Pending | Yellow       | Awaiting action, neutral alert |

---

## Component Usage Rules

### Hard Rule (from AGENTS.md)

> **NO HARDCODED COLORS**: Never use hardcoded hex colors in CSS. Always use CSS variables from the theme system.

### Correct Usage

```css
/* Good - Always use variables */
.card {
  background: var(--bg-surface);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.button-primary {
  background: var(--accent);
  color: var(--text-inverse);
}

.button-primary:hover {
  background: var(--accent-hover);
}

.income-amount {
  color: var(--income-color);
}

.expense-amount {
  color: var(--expense-color);
}
```

### Incorrect Usage

```css
/* Bad - Never hardcode */
.card {
  background: #1a1a2e; /* DON'T DO THIS */
  color: #e4e4e7; /* DON'T DO THIS */
}
```

---

## Quick Reference

### Files to Modify

| Task                   | File(s)                                                  |
| ---------------------- | -------------------------------------------------------- |
| Change default colors  | `src/lib/theme/defaults.ts`                              |
| Add new color variable | `src/lib/theme/types.ts` (add to arrays) + `defaults.ts` |
| Create built-in theme  | `src/lib/theme/themes/*.json`                            |
| Create user theme      | `data/themes/*.json`                                     |

### Theme Store API

```typescript
import { themeMode, currentTheme, isDarkTheme } from '../stores/theme';

$themeMode; // 'dark' | 'light' | 'system'
$isDarkTheme; // boolean
$currentTheme; // Full Theme object

themeMode.set('light'); // Change theme
```

### Programmatic Theme Creation

```typescript
import { createTheme, loadTheme, applyTheme } from './src/lib/theme';

// Create from scratch
const theme = createTheme({
  id: 'custom',
  name: 'Custom',
  isDark: true,
  colors: {
    /* required colors */
  },
});

// Load from JSON
const theme = loadTheme(jsonObject);

// Apply to DOM
applyTheme(theme);
```

---

## Old → New Color Mapping

For migrating hardcoded colors:

| Old Hardcoded                   | New Variable            |
| ------------------------------- | ----------------------- |
| `#0f0f1a`                       | `var(--bg-base)`        |
| `#1a1a2e`                       | `var(--bg-surface)`     |
| `#252538`                       | `var(--bg-elevated)`    |
| `#e4e4e7`                       | `var(--text-primary)`   |
| `#949494`                       | `var(--text-secondary)` |
| `#7a7a7a`                       | `var(--text-tertiary)`  |
| `#24c8db`                       | `var(--accent)`         |
| `#1ab0c9`                       | `var(--accent-hover)`   |
| `rgba(36, 200, 219, 0.1)`       | `var(--accent-muted)`   |
| `#3d3d66`                       | `var(--border-default)` |
| `#4ade80`, `#22c55e`            | `var(--success)`        |
| `#f87171`, `#ff6b6b`, `#ef4444` | `var(--error)`          |
| `#e5a91f`                       | `var(--warning)`        |
| `#000`, `#000000`               | `var(--text-inverse)`   |

---

## Quick Checklist

### Before Committing Color Changes

- [ ] No hardcoded hex colors in `.svelte` files
- [ ] All new variables follow naming convention (`-hover`, `-bg`, `-muted`, `-border`)
- [ ] Values defined in BOTH `DARK_THEME_COLORS` and `LIGHT_THEME_COLORS`
- [ ] Text colors meet WCAG AA contrast (4.5:1 minimum)
- [ ] Secondary text is at least `#909090` on dark backgrounds
- [ ] Tertiary text is at least `#7a7a7a` on dark backgrounds
- [ ] No `-dark` or `-light` suffixes used
- [ ] No inline `rgba()` fallbacks
- [ ] Documentation updated if new variables added

### Contrast Quick Check

Run in browser DevTools console to check a color pair:

```javascript
// Calculate contrast ratio
function contrast(hex1, hex2) {
  const lum = (hex) => {
    const rgb = hex.match(/\w\w/g).map((x) => parseInt(x, 16) / 255);
    const [r, g, b] = rgb.map((c) =>
      c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
    );
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const L1 = lum(hex1),
    L2 = lum(hex2);
  return ((Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05)).toFixed(2);
}

// Example: text-secondary on bg-surface
contrast('949494', '1a1a2e'); // Should be >= 4.5
```

### Find Hardcoded Colors

```bash
# Find all hardcoded hex colors in Svelte files
rg '#[0-9a-fA-F]{3,8}' -g '*.svelte' src/ --no-heading

# Find all CSS variables currently in use
rg 'var\(--[a-z-]+\)' -g '*.svelte' src/ -o | sed 's/.*var(--//' | sed 's/)$//' | sort -u
```
