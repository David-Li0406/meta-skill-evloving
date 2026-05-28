---
name: pm7y-scss-patterns
description: |
  Discovers existing SCSS/CSS patterns (mixins, variables, utility classes, component patterns) in a codebase before writing new styles. Produces a "use these patterns" summary to ensure consistency and reuse.

  Use this skill when:
  - About to write new CSS/SCSS styles
  - Before creating a new component's styles
  - When unsure what design tokens or utilities exist
  - Before a CSS review to understand existing patterns
allowed-tools: Read, Glob, Grep
---

# SCSS/CSS Pattern Discovery Skill

Discovers existing styling patterns in a codebase to ensure new styles follow established conventions and reuse existing utilities.

---

## Overview

This skill scans a codebase to build a comprehensive inventory of:

- **Variables** - Colors, spacing, typography, breakpoints
- **Mixins** - Reusable style blocks
- **Utility classes** - Single-purpose helper classes
- **Component patterns** - Naming conventions, file structure, common approaches

**Output:** A "Use These Patterns" summary that provides actionable guidance for writing new styles.

**When to use:**

- Before writing CSS/SCSS for a new component
- Before creating new utility classes or mixins
- When onboarding to an unfamiliar codebase's styles
- Before running pm7y-css-review to understand what patterns exist

---

## Discovery Process

### Step 1: Find All Style Files

Locate CSS/SCSS files in the project:

```
# Search patterns
**/*.scss
**/*.css
**/styles/**/*
**/css/**/*

# Exclude patterns
node_modules/
dist/
build/
.next/
coverage/
```

Record the file structure - note any organizational patterns like:
- `styles/` or `css/` directories
- `_variables.scss`, `_mixins.scss` partial naming
- Component-colocated styles vs centralized stylesheets

### Step 2: Extract Variables

Search for SCSS/CSS variable definitions:

**SCSS variables:**
```
Pattern: $[a-zA-Z][a-zA-Z0-9-_]*:
```

**CSS custom properties:**
```
Pattern: --[a-zA-Z][a-zA-Z0-9-]*:
```

Categorize discovered variables:

| Category | Common Patterns |
|----------|-----------------|
| Colors | `$color-*`, `$primary`, `$secondary`, `--color-*` |
| Spacing | `$spacing-*`, `$gap-*`, `$margin-*`, `$padding-*` |
| Typography | `$font-*`, `$text-*`, `$heading-*`, `--font-*` |
| Breakpoints | `$breakpoint-*`, `$screen-*`, `$bp-*` |
| Sizing | `$width-*`, `$height-*`, `$size-*` |
| Z-index | `$z-*`, `$zindex-*` |
| Shadows | `$shadow-*`, `$box-shadow-*` |
| Borders | `$border-*`, `$radius-*` |

### Step 3: Extract Mixins

Search for SCSS mixin definitions:

```
Pattern: @mixin [name]
```

For each mixin, note:
- Name and purpose (infer from name/comments)
- Parameters (if any)
- Where it's used (`@include [name]`)

Common mixin categories:

| Category | Examples |
|----------|----------|
| Responsive | `@mixin mobile`, `@mixin tablet`, `@mixin desktop` |
| Flexbox | `@mixin flex-center`, `@mixin flex-between` |
| Typography | `@mixin heading`, `@mixin body-text` |
| Positioning | `@mixin absolute-center`, `@mixin fixed-bottom` |
| Animations | `@mixin fade-in`, `@mixin slide-up` |

### Step 4: Extract Utility Classes

Look for utility/helper class patterns:

**Common utility file locations:**
- `utilities.scss`, `helpers.scss`, `utils.scss`
- `_utilities.scss`, `_helpers.scss`
- Files in `utilities/` or `helpers/` directories

**Utility class patterns to identify:**
- Display: `.hidden`, `.visible`, `.block`, `.inline-*`
- Flexbox: `.flex`, `.flex-center`, `.flex-between`, `.flex-column`
- Grid: `.grid`, `.grid-*`
- Spacing: `.m-*`, `.p-*`, `.mt-*`, `.mb-*`, `.mx-*`, `.my-*`
- Text: `.text-center`, `.text-left`, `.text-bold`, `.truncate`
- Colors: `.text-primary`, `.bg-primary`, `.border-primary`

### Step 5: Detect CSS Framework

Check for framework usage that provides built-in utilities:

**Tailwind CSS:**
- `tailwind.config.js` or `tailwind.config.ts` exists
- `@tailwind` directives in CSS files
- Class usage patterns like `flex`, `p-4`, `text-gray-500`

**Bootstrap:**
- Bootstrap in `package.json` dependencies
- Bootstrap imports in SCSS
- Class patterns like `d-flex`, `justify-content-center`, `text-muted`

**Other frameworks:**
- Check `package.json` for: styled-components, emotion, CSS modules
- Look for framework-specific file extensions or patterns

### Step 6: Identify Component Patterns

Analyze how component styles are organized:

**Naming conventions:**
- BEM: `.block__element--modifier`
- OOCSS: Separation of structure and skin
- Utility-first: Composing utilities
- CSS Modules: Locally scoped class names

**File organization:**
- Colocated: `Component.tsx` + `Component.scss`
- Centralized: All styles in `styles/` directory
- Feature-based: Styles grouped by feature

**Common patterns to note:**
- How colors are applied (direct values vs variables)
- Responsive approach (mobile-first vs desktop-first)
- Animation patterns
- Icon handling

---

## Output Format

After completing discovery, produce a summary in this format:

```markdown
## Use These Patterns

### Design Tokens

**Colors:**
- Primary: `$color-primary` (#3B82F6)
- Secondary: `$color-secondary` (#10B981)
- Error: `$color-error` (#EF4444)
- [list all color variables]

**Spacing:**
- `$spacing-xs` (4px), `$spacing-sm` (8px), `$spacing-md` (16px), `$spacing-lg` (24px)
- [list all spacing variables]

**Typography:**
- `$font-family-sans`, `$font-family-mono`
- `$font-size-sm`, `$font-size-base`, `$font-size-lg`
- [list all typography variables]

### Available Mixins

| Mixin | Purpose | Usage |
|-------|---------|-------|
| `@mixin flex-center` | Center with flexbox | `@include flex-center;` |
| `@mixin mobile` | Mobile breakpoint | `@include mobile { ... }` |
| [list all mixins] |

### Utility Classes

**Layout:**
- `.flex`, `.flex-center`, `.flex-between`
- `.grid`, `.grid-2`, `.grid-3`

**Spacing:**
- `.m-{0-4}`, `.p-{0-4}`, `.mx-auto`

**Text:**
- `.text-center`, `.text-bold`, `.truncate`

[list all utility classes by category]

### CSS Framework: [Name or None]

[If framework detected, list key utilities to prefer]

### Naming Convention: [BEM/OOCSS/Utility-first/CSS Modules]

New classes should follow: `[example of the convention]`

### File Organization

Component styles go in: `[path pattern]`
Global styles go in: `[path pattern]`
```

---

## Discovery Checklist

Before producing the summary:

- [ ] Found all SCSS/CSS files (excluding node_modules, dist, build)
- [ ] Extracted SCSS variables ($name)
- [ ] Extracted CSS custom properties (--name)
- [ ] Categorized variables by type (colors, spacing, typography, etc.)
- [ ] Found all mixin definitions (@mixin)
- [ ] Identified mixin purposes and parameters
- [ ] Found utility/helper class files
- [ ] Cataloged utility classes by category
- [ ] Checked for Tailwind, Bootstrap, or other frameworks
- [ ] Identified naming convention (BEM, OOCSS, etc.)
- [ ] Noted file organization pattern
- [ ] Summary uses consistent formatting
- [ ] Summary includes example usage for each pattern

---

## Constraints

### DO:
- Focus on discovery only - do not modify any files
- Include actual values where helpful (e.g., color hex codes)
- Group related patterns together
- Provide usage examples for mixins
- Note any inconsistencies in existing patterns (but don't try to fix them)

### DO NOT:
- Create new variables, mixins, or utilities
- Modify existing files
- Make recommendations for changes
- Judge the quality of existing patterns
- Spend time on files in node_modules, dist, or build directories

---

## Example Output

For a typical React project with SCSS:

```markdown
## Use These Patterns

### Design Tokens

**Colors:**
- `$color-primary` (#2563EB) - Main brand color
- `$color-primary-dark` (#1D4ED8) - Hover states
- `$color-gray-100` through `$color-gray-900` - Neutral scale
- `$color-success` (#22C55E), `$color-error` (#EF4444), `$color-warning` (#F59E0B)

**Spacing:**
- Scale: `$spacing-1` (4px) through `$spacing-8` (64px)
- Use `$spacing-4` (16px) as the base unit

**Typography:**
- Font: `$font-sans` (Inter, system-ui)
- Sizes: `$text-sm` (14px), `$text-base` (16px), `$text-lg` (18px), `$text-xl` (20px)
- Weights: `$font-normal` (400), `$font-medium` (500), `$font-bold` (700)

### Available Mixins

| Mixin | Purpose | Usage |
|-------|---------|-------|
| `@mixin flex-center` | Center content with flexbox | `@include flex-center;` |
| `@mixin responsive($bp)` | Media query wrapper | `@include responsive(tablet) { ... }` |
| `@mixin truncate` | Single-line text truncation | `@include truncate;` |
| `@mixin visually-hidden` | Accessible hiding | `@include visually-hidden;` |

### Utility Classes

**Layout:** `.flex`, `.flex-center`, `.flex-between`, `.flex-col`, `.grid`, `.hidden`, `.block`

**Spacing:** `.m-0` through `.m-4`, `.p-0` through `.p-4`, `.mx-auto`, `.gap-1` through `.gap-4`

**Text:** `.text-center`, `.text-left`, `.text-right`, `.font-bold`, `.truncate`

### CSS Framework: None (custom utilities)

### Naming Convention: BEM

Example: `.card`, `.card__header`, `.card__body`, `.card--highlighted`

### File Organization

- Component styles: `src/components/[Component]/[Component].scss`
- Global styles: `src/styles/`
- Variables: `src/styles/_variables.scss`
- Mixins: `src/styles/_mixins.scss`
```

---

## When Discovery Finds Nothing

If the codebase has minimal or no existing CSS patterns:

```markdown
## Use These Patterns

### Status: Minimal existing patterns

This codebase has few established CSS patterns. Consider:
- Defining color variables before using colors
- Creating spacing scale variables
- Establishing a naming convention (BEM recommended)

### Files Found
- [list any CSS/SCSS files found]

### Framework: [detected or None]
```

This allows the user to make informed decisions about establishing new patterns.
