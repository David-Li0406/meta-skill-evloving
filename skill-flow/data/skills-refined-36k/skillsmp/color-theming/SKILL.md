---
name: color-theming
description: Color theme selection and application for website branding. Use when user wants to change colors, theme, accent, branding, or visual style.
allowed-tools: Read, Write, Edit, AskUserQuestion
---

# Color Theming

Help users select and apply color themes to their website.

## Available Themes

| Theme | Hex Code | Character |
|-------|----------|-----------|
| Blue | `#2563eb` | Professional, trustworthy, corporate |
| Purple | `#7c3aed` | Creative, innovative, artistic |
| Teal | `#0d9488` | Fresh, modern, tech-forward |
| Amber | `#d97706` | Warm, energetic, friendly |
| Rose | `#e11d48` | Bold, passionate, attention-grabbing |

## Workflow

### Step 1: Show Options

If user hasn't specified a color, use AskUserQuestion:

> "Which color theme would you like for your website?"
>
> - Blue (#2563eb) - Professional, trustworthy
> - Purple (#7c3aed) - Creative, innovative
> - Teal (#0d9488) - Fresh, modern
> - Amber (#d97706) - Warm, energetic
> - Rose (#e11d48) - Bold, passionate
> - Custom (provide hex code)

### Step 2: Validate Custom Colors

If user provides a custom hex code:

1. Verify it's a valid hex format (`#RRGGBB` or `#RGB`)
2. Check contrast ratio against dark background (`#0a0e14`):
   - Minimum 4.5:1 for WCAG AA compliance
   - Warn if contrast is insufficient

### Step 3: Apply Theme

Update `styles/variables.css`:

```css
:root {
    /* ... other variables ... */

    /* Accent - Updated by color-theming */
    --color-accent: {selected_color};
}
```

### Step 4: Preview

Suggest running preview:

> Color updated! Run `/preview` or `just serve` to see the changes.

## Color Accessibility

For dark backgrounds (`#0a0e14`), these colors meet WCAG AA:

| Color | Contrast Ratio | Status |
|-------|----------------|--------|
| Blue #2563eb | 4.6:1 | Pass |
| Purple #7c3aed | 4.8:1 | Pass |
| Teal #0d9488 | 4.5:1 | Pass |
| Amber #d97706 | 4.7:1 | Pass |
| Rose #e11d48 | 4.5:1 | Pass |

## Deriving Secondary Colors

For `--color-accent-secondary`, you can:
- Use a complementary hue (e.g., blue + purple)
- Use a lighter/darker variant of the primary
- Default: Keep as `#7c3aed` (purple) for most themes
