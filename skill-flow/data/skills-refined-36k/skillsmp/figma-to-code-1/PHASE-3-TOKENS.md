# Phase 3: Design Token Extraction

Extract design tokens from Figma to ensure pixel-perfect implementation.

## Step 1: Extract Figma Variables

Use Figma MCP to extract all variables:

```typescript
// Use mcp__figma__get_variable_defs to extract:
// - Colors (primitives and semantic)
// - Spacing scale
// - Typography (families, sizes, weights, line heights, letter spacing)
// - Border radius, shadows
```

## Step 2: Create Design Tokens

Create `/docs/design-tokens.json`:

```json
{
  "colors": {
    "primary": "#1a365d",
    "secondary": "#2d3748",
    "background": "#ffffff",
    "text": "#1a202c"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "typography": {
    "fontFamily": {
      "heading": "Playfair Display",
      "body": "Inter"
    },
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "24px",
      "2xl": "32px"
    }
  },
  "borderRadius": {
    "sm": "4px",
    "md": "8px",
    "lg": "16px",
    "full": "9999px"
  }
}
```

## Step 3: Create CSS Custom Properties

Create `/src/styles/tokens.css`:

```css
:root {
  /* Colors */
  --color-primary: #1a365d;
  --color-secondary: #2d3748;
  --color-background: #ffffff;
  --color-text: #1a202c;

  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Typography */
  --font-heading: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
}
```

## Step 4: Update Tailwind Config

Update `tailwind.config.ts`:

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      },
      fontFamily: {
        heading: ['var(--font-heading)'],
        body: ['var(--font-body)'],
      },
      spacing: {
        // Add custom spacing if needed
      },
    },
  },
  plugins: [],
};

export default config;
```

## Step 5: Create Design Token Reference Document

Create `/docs/design-tokens.md` with ALL extracted tokens in structured markdown tables. Include colors, typography, spacing, breakpoints, and component specs. This document is the single source of truth for QA in Phase 12. See [EXAMPLE-DESIGN-TOKENS.md](EXAMPLE-DESIGN-TOKENS.md) for the template format.

## Step 6: Document Token Mapping

Add to `CLAUDE.md`:

```markdown
## Design Tokens

- Colors: Use Tailwind classes or CSS variables
- Fonts: `font-heading` for headings, `font-body` for body text
- Spacing: Follow Figma spacing scale
- See `/docs/design-tokens.json` for all values
```

## Git Commit

```bash
git commit -m "feat: design tokens extracted from Figma"
```

## Checkpoint

```bash
osascript -e 'display notification "Phase 3: Design tokens extracted" with title "Claude Code" sound name "Ping"'
```

**Next:** Proceed to [PHASE-4-ASSETS.md](PHASE-4-ASSETS.md)
