# Token Naming System (Layer 1)

**This is the contract**: Standardized CSS custom property names used across ALL themes.

## Core Philosophy: Ink & Paper

Every property belongs to one of four categories:

1. **Ink (`--c-`)**: The pigment. Anything *on top* of surfaces (text, icons, borders)
2. **Paper (`--bg-`)**: The substrate. Surface layers that hold ink (backgrounds, cards)
3. **Structure (`--s-`, `--r-`, `--b-`)**: The physics. Dimensions, spacing, geometry
4. **Atmosphere (`--x-`, `--a-`)**: The feel. Lighting, depth, motion

**Rule**: When styling, ask "Is this ink or paper?"

## Token Hierarchy

### Primitives (The Warehouse)
Raw building blocks with numeric scales:
- `--s-4` (spacing: 16px)
- `--c-slate-500` (color: gray)
- `--r-3` (radius: medium)

**Usage**: Internal to theme files. Rarely used directly in components.

### Semantics (The Blueprint)
Intent-based aliases that reference primitives:
- `--c-primary` (maps to a primitive color)
- `--bg-surface` (maps to a primitive background)
- `--r-btn` (maps to a primitive radius)

**Usage**: Use these in component code. This is what you customize for themes.

## Complete Token Taxonomy

| Prefix | Category | Scale Logic | Examples |
|--------|----------|-------------|----------|
| `--c-` | Color (Ink) | 050–950 | `--c-primary`, `--c-slate-500` |
| `--bg-` | Background (Paper) | Semantic | `--bg-surface`, `--bg-overlay` |
| `--s-` | Space | 0–9 (4px steps) | `--s-4` = 16px, `--s-8` = 32px |
| `--ff-` | Font Family | Categorical | `--ff-sans`, `--ff-mono` |
| `--fw-` | Font Weight | 100–900 | `--fw-400` = normal, `--fw-700` = bold |
| `--fs-` | Font Size | 1–9 | `--fs-3` = body, `--fs-7` = heading |
| `--t-` | Typography | Semantic | `--t-heading`, `--t-body` (shorthand) |
| `--r-` | Radius | 0–6 | `--r-btn`, `--r-card`, `--r-3` |
| `--b-` | Border | 0–4 | `--b-1` = 1px, `--b-2` = 2px |
| `--x-` | Effects (Shadows) | 0–5 | `--x-card`, `--x-overlay` |
| `--o-` | Opacity | 0–9 | `--o-0` = transparent, `--o-9` = opaque |
| `--z-` | Z-Index | 0–6 | `--z-dropdown`, `--z-modal` |
| `--a-` | Animation | Semantic | `--a-fast`, `--a-smooth` |
| `--w-` | Width | Semantic | `--w-container`, `--w-prose` |
| `--h-` | Height | Semantic | `--h-screen`, `--h-hero` |
| `--p-` | Padding | Maps to `--s-` | `--p-card` = `--s-6` |
| `--m-` | Margin | Maps to `--s-` | `--m-section` = `--s-8` |
| `--g-` | Gap | Maps to `--s-` | `--g-grid` = `--s-4` |

### Scale Explanations

**Space Scale (`--s-`)**: 4px increments
```
--s-0: 0px
--s-1: 4px
--s-2: 8px
--s-3: 12px
--s-4: 16px (most common)
--s-5: 20px
--s-6: 24px
--s-7: 28px
--s-8: 32px
--s-9: 36px
```

**Color Scale (`--c-`)**: Lightness/density
```
050: Lightest (almost white)
100-400: Light tones
500: Base color
600-900: Dark tones
950: Darkest (almost black)
```

**Radius Scale (`--r-`)**: Corner roundness
```
--r-0: 0px (square)
--r-1: 2px (subtle)
--r-2: 4px (soft)
--r-3: 8px (medium)
--r-4: 12px (rounded)
--r-5: 16px (very rounded)
--r-6: 24px (pill-like)
```

## Critical Constraints

### The Zero Protocol

Zero tokens (`--s-0`, `--r-0`, `--b-0`, `--x-0`, `--o-0`) are **functional resets**, not design choices:

- `--s-0: 0px` - Remove padding/margin entirely
- `--r-0: 0px` - Square corners (no rounding)
- `--b-0: 0` - Remove border
- `--x-0: none` - Remove shadows/effects
- `--o-0: 0` - Fully transparent

**Use case**: Explicitly resetting properties, not default styling.

### The Font Size Exception

**`--fs-0` does not exist** and never will.

**Why**: There is no valid "neutral" font size:
- `0px` is invisible (meaningless)
- `inherit` breaks the numeric scale
- `initial` resets to browser default (16px), which is larger than `--fs-1`

**Rule**: Font size scale starts at `--fs-1` (smallest legible text). If you need to hide text, use `display: none` or `visibility: hidden`, not font-size.

## Usage Patterns

### ✅ Correct: Use Semantic Tokens
```css
color: var(--c-primary);
background-color: var(--bg-surface);
padding: var(--s-4);
border-radius: var(--r-btn);
```

### ⚠️ Avoid: Direct Primitive Usage
```css
/* Only use in theme files, not component code */
color: var(--c-slate-700);
padding: var(--s-4); /* This is OK - space primitives are commonly used */
```

### ❌ Wrong: Hardcoded Values
```css
/* Never hardcode - defeats the token system */
color: #333333;
padding: 16px;
```

## Component-Level Tokens

Follow `--<property>-of-<element>` pattern:
- `--r-badge` = radius of badge
- `--c-title` = color of title
- `--fw-heading` = font-weight of heading
- `--m-actions` = margin of actions

## Key Insights

1. **Token NAMES are the contract** - They stay constant across all themes
2. **Token VALUES change per theme** - This is how you switch visual fidelity
3. **Use semantics over primitives** - Enables consistent theming
4. **Primitives = warehouse, Semantics = blueprint** - Separate what you have from how you use it

## See Also

- `themes.md` - How token values differ across themes
- `components.md` - How component classes use these tokens
- `../assets/elementary/tokens/polished.css` - Polished theme values for primitive and semantic tokens
- `../assets/elementary/tokens/sketch.css` - Sketch theme values for primitive and semantic tokens
