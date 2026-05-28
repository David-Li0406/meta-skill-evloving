---
name: ui-design-system
description: >
  UI design system toolkit for creating and maintaining design tokens, visual consistency, and developer handoff documentation.
  Trigger: When creating or updating design tokens, generating color palettes, documenting design system, or establishing visual consistency.
license: Apache-2.0
metadata:
  author: gero-cloud
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating design tokens, generating color palettes, documenting design system"
---

## When to Use

Use this skill when:
- Generating new design tokens from brand colors
- Updating or maintaining the design token system
- Creating color palettes or typography scales
- Documenting design system guidelines
- Calculating responsive breakpoints or spacing systems
- Creating developer handoff documentation

**Don't use this skill when:**
- Implementing components that USE tokens (use `ui-components` instead)
- Writing CSS for specific components (use `ui-components` instead)
- Making design decisions about user experience (use `ux-researcher-designer` instead)

---

## Relationship with Other Skills

```
ux-researcher-designer  →  Define user needs and design requirements
           ↓
ui-design-system       →  Create design tokens and visual system
           ↓
ui-components          →  Implement components using those tokens
```

---

## Current Design Token Structure

GeroCare uses a two-tier token system:

### 1. Base Tokens (`src/assets/themes/tokens.css`)
Raw color values that serve as the foundation:
- Color scales: `--token-color-primary-{50-900}`
- Semantic bases: `--token-color-success-*`, `--token-color-error-*`, etc.
- Neutral grays: `--token-color-neutral-{50-900}`

### 2. Semantic Tokens (`src/assets/themes/semantic.css`)
Context-aware design variables that components should use:
- Backgrounds: `--color-bg-primary`, `--color-bg-hover`
- Text: `--color-text-primary`, `--color-text-secondary`
- Interactive: `--color-button-primary-bg`, `--color-button-primary-text`
- Spacing: `--spacing-xs` through `--spacing-3xl`
- Typography: `--font-size-*`, `--font-weight-*`
- Shadows: `--shadow-{sm,md,lg,xl}`
- Borders: `--radius-{sm,md,lg,xl}`

**Critical Rule**: Components should ALWAYS use semantic tokens, never base tokens directly.

---

## Critical Patterns

### 1. When to Generate New Tokens

Use the token generator script when:
- Starting a new brand color scheme
- Rebranding with a new primary color
- Creating a new product variant
- Exploring design system variations

**Don't regenerate tokens when:**
- Tokens already exist and meet your needs
- You only need to adjust a few semantic tokens
- Making minor component-level style changes

### 2. Token Generator Usage

The `design_token_generator.py` script creates a complete design system:

```bash
# Generate tokens from brand color
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern json

# Arguments:
# 1. Brand color (hex): "#667eea"
# 2. Style: "modern" | "classic" | "playful"
# 3. Format: "json" | "css" | "scss" | "summary"

# Example output formats:
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern json > tokens.json
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern css > new-tokens.css
```

### 3. Integrating Generated Tokens

When adding new tokens to the project:

1. **Base tokens** → Update `src/assets/themes/tokens.css`
   - Add new color scales under `:root`
   - Keep existing structure and naming convention
   - Preserve existing tokens that are still in use

2. **Semantic tokens** → Update `src/assets/themes/semantic.css`
   - Map semantic concepts to base tokens
   - Use CSS `var()` to reference base tokens
   - Add dark mode overrides if needed

3. **Verify imports** → Check `src/assets/main.css`
   - Ensure `tokens.css` is imported before `semantic.css`
   - Tokens load in correct order: base → semantic

Example integration:

```css
/* In tokens.css - add new base tokens */
:root {
  --token-color-accent-500: #667eea;
  --token-color-accent-600: #5568d3;
  /* ... more scale values */
}

/* In semantic.css - map to semantic usage */
:root {
  --color-link: var(--token-color-accent-600);
  --color-link-hover: var(--token-color-accent-700);
}
```

### 4. Spacing System (8pt Grid)

GeroCare uses an 8-point grid system. All spacing should be multiples of 4px:

```
--spacing-xs:   0.25rem;  /* 4px */
--spacing-sm:   0.5rem;   /* 8px */
--spacing-md:   0.75rem;  /* 12px */
--spacing-lg:   1rem;     /* 16px */
--spacing-xl:   1.5rem;   /* 24px */
--spacing-2xl:  2rem;     /* 32px */
--spacing-3xl:  3rem;     /* 48px */
```

**Rule**: Never use arbitrary spacing values. Always use tokens.

### 5. Typography Scale

Typography follows a modular scale (1.25 ratio):

```
--font-size-xs:   0.75rem;   /* 12px */
--font-size-sm:   0.875rem;  /* 14px */
--font-size-base: 1rem;      /* 16px */
--font-size-lg:   1.125rem;  /* 18px */
--font-size-xl:   1.25rem;   /* 20px */
--font-size-2xl:  1.5rem;    /* 24px */
```

### 6. Dark Mode Support

All tokens must support dark mode through media queries:

```css
/* Light mode (default) */
:root {
  --color-bg-primary: var(--vt-c-white);
  --color-text-primary: var(--vt-c-text-light-1);
}

/* Dark mode - system preference */
@media (prefers-color-scheme: dark) {
  :root:not(.light) {
    --color-bg-primary: var(--vt-c-black);
    --color-text-primary: var(--vt-c-text-dark-1);
  }
}

/* Dark mode - manual toggle */
html.dark :root,
:root.dark {
  --color-bg-primary: var(--vt-c-black);
  --color-text-primary: var(--vt-c-text-dark-1);
}
```

---

## Token Generator Script Reference

### Features

The `design_token_generator.py` script generates:

1. **Color Palette**:
   - Primary color scale (50-900) from brand color
   - Secondary color (complementary hue)
   - Neutral grays
   - Semantic colors (success, error, warning, info)

2. **Typography System**:
   - Font families (modern/classic/playful styles)
   - Font size scale
   - Font weights (100-900)
   - Line heights and letter spacing
   - Pre-composed text styles (h1-h6, body, small, caption)

3. **Spacing System**:
   - 8pt grid-based spacing values
   - Semantic spacing names (xs, sm, md, lg, xl, 2xl, 3xl)

4. **Border & Radius**:
   - Radius values by style (modern/classic/playful)
   - Border widths

5. **Shadows**:
   - Elevation system (sm, md, lg, xl, 2xl, inner)

6. **Animation**:
   - Duration tokens (fast, base, slow)
   - Easing functions
   - Keyframe animations (fadeIn, slideUp, scale)

7. **Breakpoints**:
   - Responsive breakpoints (xs, sm, md, lg, xl, 2xl)

8. **Z-Index Scale**:
   - Layering system (base, dropdown, modal, tooltip, etc.)

### Usage Examples

```bash
# Quick summary of what would be generated
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern summary

# Generate JSON for review
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern json

# Generate CSS format (requires manual integration)
python .cursor/skills/ui-design-system/scripts/design_token_generator.py "#667eea" modern css
```

---

## Decision Trees

### When to Generate vs. Use Existing Tokens

```
Need new color scheme?
├─ Yes → Use token generator script
│       ↓
│   Integrate base tokens → tokens.css
│       ↓
│   Map to semantic tokens → semantic.css
│
└─ No → Need new semantic token?
    ├─ Yes → Add to semantic.css
    │       (reference existing base tokens)
    │
    └─ No → Use existing semantic token
```

### Adding New Tokens

```
Adding new design element?
├─ Color-related?
│   ├─ Base color scale needed? → Add to tokens.css
│   └─ Semantic usage? → Add to semantic.css (use var())
│
├─ Spacing-related?
│   └─ Use existing --spacing-* tokens
│       (if new size needed, add to semantic.css)
│
├─ Typography-related?
│   └─ Use existing --font-size-* tokens
│       (if new size needed, add to semantic.css)
│
└─ Other?
    └─ Evaluate: base or semantic?
        → Follow token structure pattern
```

---

## File Organization

```
src/assets/
├── themes/
│   ├── tokens.css      # Base tokens (raw values)
│   └── semantic.css    # Semantic tokens (component-level)
└── main.css            # Imports tokens → semantic

.cursor/skills/ui-design-system/
├── SKILL.md                                    # This file
└── scripts/
    └── design_token_generator.py               # Token generator
```

---

## Integration with Components

After updating tokens, verify components use them correctly:

1. **Check component styles** use semantic tokens
   ```css
   /* ✅ Correct */
   color: var(--color-text-primary);
   
   /* ❌ Wrong */
   color: var(--token-color-primary-500);
   color: #667eea;
   ```

2. **Verify dark mode** works with new tokens

3. **Test responsive** breakpoints if using new sizing tokens

---

## Developer Handoff Documentation

When documenting design system changes:

1. **Token Changes**: Document which tokens were added/modified
2. **Migration Path**: If breaking changes, provide upgrade guide
3. **Usage Examples**: Show before/after component examples
4. **Dark Mode**: Verify and document dark mode behavior

---

## Resources

- **Base Tokens**: `src/assets/themes/tokens.css`
- **Semantic Tokens**: `src/assets/themes/semantic.css`
- **Token Generator**: `.cursor/skills/ui-design-system/scripts/design_token_generator.py`
- **Component Usage**: See `ui-components` skill for how to use tokens in components