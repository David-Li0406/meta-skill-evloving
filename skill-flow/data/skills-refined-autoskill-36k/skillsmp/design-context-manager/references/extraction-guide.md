# Design Context Extraction Guide

Step-by-step guide for extracting design context from an existing codebase.

## File Locations to Check

### 1. Tailwind Configuration
**Files:** `tailwind.config.js`, `tailwind.config.ts`, `tailwind.config.mjs`

**Extract:**
- `theme.colors` → colors.md
- `theme.fontFamily` → typography.md
- `theme.spacing` → layout.md
- `theme.screens` → layout.md (breakpoints)
- `theme.extend.*` → respective files

**Example extraction:**
```javascript
// tailwind.config.ts
theme: {
  colors: {
    primary: '#3b82f6',  // → colors.md: Primary brand color
    secondary: '#64748b',
  },
  fontFamily: {
    sans: ['Inter', 'sans-serif'],  // → typography.md: Body font
    display: ['Cal Sans', 'sans-serif'],  // → typography.md: Display font
  }
}
```

### 2. CSS Variables
**Files:** `app/globals.css`, `src/index.css`, `styles/variables.css`

**Look for:**
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  /* ... */
}
```

**Extract:** CSS custom properties → design-tokens.json, colors.md

### 3. Package.json Dependencies
**File:** `package.json`

**Look for UI libraries:**
- `@radix-ui/*` → components.md: Radix UI primitives
- `@shadcn/*` or component imports → components.md: shadcn/ui
- `@mui/material` → components.md: Material UI
- `tailwindcss` → layout.md: Tailwind-based spacing
- Font packages (`@fontsource/*`, `next/font`) → typography.md

### 4. Component Structure
**Directories:** `components/`, `src/components/`, `app/components/`

**Analyze:**
- Directory organization (by feature, by type)
- Common patterns (Button variants, Card usage)
- Naming conventions

### 5. Layout Files
**Files:** `app/layout.tsx`, `pages/_app.tsx`, `src/App.tsx`

**Extract:**
- Font imports and configuration
- Global wrapper components
- Theme providers

### 6. Documentation
**Files:** `README.md`, `CLAUDE.md`, `docs/`

**Extract:**
- Product description → product-context.md
- Tech stack information → components.md
- User information → product-context.md

## Extraction Process

### Step 1: Gather Configuration
```
Read in this order:
1. package.json (understand tech stack)
2. tailwind.config.* (design tokens)
3. CSS variable files (additional tokens)
4. Layout files (fonts, providers)
5. README/docs (product context)
```

### Step 2: Map to Context Files

| Source | Target File |
|--------|-------------|
| `theme.colors`, CSS `--color-*` | colors.md |
| `theme.fontFamily`, font imports | typography.md |
| `theme.spacing`, `theme.screens` | layout.md |
| UI library deps, component dirs | components.md |
| README, product description | product-context.md |
| Routes, page structure | user-journeys.md |

### Step 3: Generate with Confidence Annotations

Include source annotations for extracted values:

```markdown
## Primary Color
- Value: `#3b82f6`
- Source: `tailwind.config.ts:theme.colors.primary`
- Confidence: High
```

Confidence levels:
- **High**: Explicitly defined in config
- **Medium**: Inferred from usage patterns
- **Low**: Guessed from limited data

### Step 4: Fill Gaps with Questions

For missing information, ask the user:

**Brand/Product:**
- "What is this product? Who is it for?"
- "What visual style best describes it? (minimal, playful, corporate, etc.)"

**Technical:**
- "I didn't find font configuration. What fonts should be used?"
- "No color system found. Should I generate one or do you have preferences?"

## Common Extraction Patterns

### Shadcn/ui Projects
```
package.json: @radix-ui/* deps
components/ui/: shadcn components
tailwind.config: CSS variable-based colors
globals.css: HSL color definitions
```

### Next.js + Tailwind
```
tailwind.config.ts: Full theme config
app/globals.css: CSS variables
app/layout.tsx: next/font imports
```

### Vite + React
```
tailwind.config.js: Theme config
src/index.css: Global styles
vite.config.ts: Plugin configuration
```

## Design Tokens JSON Structure

Generate W3C Design Tokens format:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "$metadata": {
    "name": "Project Design System",
    "generator": "design-context-manager"
  },
  "color": {
    "brand": {
      "primary": {
        "500": { "$value": "#3b82f6", "$type": "color" }
      }
    }
  },
  "typography": {
    "fontFamily": {
      "display": { "$value": "Cal Sans, sans-serif", "$type": "fontFamily" }
    }
  }
}
```

## Error Handling

### No Configuration Found
- Inform user: "No design configuration found"
- Offer to generate starter context
- Ask clarifying questions about intended design

### Partial Configuration
- Extract what's available
- Mark missing sections with placeholders
- Ask user to fill gaps

### Conflicting Values
- Note the conflict
- Ask user which is correct
- Default to most explicit configuration
