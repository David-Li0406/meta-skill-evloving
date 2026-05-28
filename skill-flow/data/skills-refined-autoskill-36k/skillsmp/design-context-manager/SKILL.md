---
name: design-context-manager
description: Initialize and maintain design context files. Use when design-context/ folder doesn't exist, after design-relevant code changes (colors, fonts, spacing), or when foundation elements change. The agent should invoke this after modifying design tokens to keep context in sync.
---

# Design Context Manager

Initialize and maintain the design context files that ground all design decisions.

## When to Use

### Initial Setup
- Project has no `design-context/` folder
- Starting a new project from scratch

### After Design-Relevant Code Changes
Invoke this skill after modifying:
- `tailwind.config.*` (colors, fonts, spacing, breakpoints)
- CSS variables in `globals.css`, `index.css`, or similar
- Font imports or typography configuration
- Component library setup or theming

### After Feature/Flow Changes
Invoke this skill after:
- Adding new pages or routes
- Implementing major features
- Changing core user flows or navigation

### Foundation Changes
- Rebrand or design system migration
- Major style overhaul
- New component library adoption

## Output Structure

Creates `design-context/` folder in project root with:

### Modular Design Spec Files (6 markdown files)
| File | Content |
|------|---------|
| `brand.md` | Brand identity, voice, tone, personality |
| `colors.md` | Color system, palettes, semantic colors |
| `typography.md` | Font families, type scale, semantic styles |
| `layout.md` | Spacing, grid, responsive breakpoints |
| `components.md` | Component guidelines, patterns |
| `logo.md` | Logo usage, variations, clear space |

### Machine-Readable Tokens
| File | Content |
|------|---------|
| `design-tokens.json` | W3C Design Tokens format (colors + typography) |

### Product Context
| File | Content |
|------|---------|
| `product-context.md` | Product overview, audience, personas |
| `user-journeys.md` | Key pages and workflows |

## Process Selection

### Path A: Extraction (Preferred for Existing Codebases)

Use when project has existing design patterns to extract.

**Check for:**
- `tailwind.config.*` - Color, font, spacing configuration
- `package.json` - UI library dependencies (shadcn, radix, mui, etc.)
- `app/globals.css` or `src/index.css` - CSS variables
- `components/` or `src/components/` - Component structure
- `README.md`, `CLAUDE.md` - Product documentation

**Process:**
1. Read and analyze configuration files
2. Extract design tokens (colors, fonts, spacing)
3. Identify component library and patterns
4. Generate design-context files with confidence annotations
5. Ask clarifying questions for uncertain values

See [extraction-guide.md](references/extraction-guide.md) for detailed instructions.

### Path B: Interactive (For New Projects)

Use when project lacks design patterns or starting fresh.

**Process:**
1. Ask about product and audience
2. Ask about visual direction preferences
3. Generate templates with placeholder guidance
4. Recommend design system setup steps

See [questionnaire-guide.md](references/questionnaire-guide.md) for question flow.

## Context File Templates

See [templates/](templates/) for the full structure of each context file:
- `brand-template.md` - Brand identity, voice, tone
- `colors-template.md` - Color system and palettes
- `typography-template.md` - Fonts and type scale
- `layout-template.md` - Spacing, grid, breakpoints
- `components-template.md` - Component patterns
- `logo-template.md` - Logo usage guidelines
- `product-context-template.md` - Product overview, personas
- `user-journeys-template.md` - Flows, pages, interactions
- `design-tokens-template.json` - W3C format tokens

## Maintenance Mode

When the agent has made design-relevant code changes, follow this workflow to sync context.

### Step 1: Identify Affected Context Files

| Code Change | Update These Files |
|-------------|-------------------|
| `theme.colors.*` or CSS `--color-*` | colors.md, design-tokens.json |
| `theme.fontFamily.*` or font imports | typography.md, design-tokens.json |
| `theme.spacing.*` or CSS `--spacing-*` | layout.md, design-tokens.json |
| `theme.screens.*` (breakpoints) | layout.md |
| Component library changes | components.md |
| Brand voice/tone changes | brand.md |
| New routes or user flows | user-journeys.md |
| Product positioning changes | product-context.md |

### Step 2: Read Existing Context

Read `design-context/[affected-file].md` and preserve:
- Custom additions not from extraction
- User-provided overrides
- Sections marked with `<!-- Manual -->` annotation

### Step 3: Update Specific Sections

**Do NOT regenerate entire files.** Update only the sections affected by the code change.

For each changed value:
1. Update the value
2. Update the source annotation: `(Extracted from tailwind.config.ts)`
3. Set confidence to `High` (you know what you just changed)

### Step 4: Update Metadata

At the bottom of each modified file, update:
```markdown
_Source: Extracted from [files]_
_Last Updated: [ISO date]_
_Recent Change: [Brief description]_
```

### Step 5: Sync design-tokens.json

If colors, typography, or spacing changed, update the affected sections in `design-tokens.json` to keep it in sync with the markdown files.

---

## Self-Invocation Guidance

The agent should proactively invoke this skill after completing work that affects design foundations.

### Trigger Recognition

After completing a task, ask:
> "Did I just modify any design-system-level values (colors, fonts, spacing, breakpoints, component patterns)?"

If yes, invoke this skill with context about what changed.

### What Triggers Maintenance

| Change Type | Example | Triggers? |
|-------------|---------|-----------|
| Color value change | Changed primary from blue to indigo | **Yes** |
| Font family change | Switched body font to Inter | **Yes** |
| Spacing/breakpoint change | Changed base unit or added breakpoint | **Yes** |
| New page or route | Added `/settings` page | **Yes** |
| Major feature | Implemented checkout flow | **Yes** |
| User flow change | Restructured onboarding | **Yes** |
| Component style tweak | Adjusted button padding | No |
| Content/copy change | Updated page text | No |
| Bug fix | Fixed overflow issue | No |

### How to Self-Invoke

After completing a triggering change, the agent should invoke this skill with context:

- "I updated the primary color to #2563eb in tailwind.config.ts"
- "I added a /settings page with account and notification preferences"

The agent then follows Maintenance Mode (above) to update the affected context files.

---

## Quality Standards

**DO:**
- Extract from actual code, not assumptions
- Include source annotations: `(Extracted from tailwind.config.ts)`
- Use semantic names, not hardcoded values
- Note confidence levels for uncertain values
- Keep files focused and scannable

**DON'T:**
- Create empty placeholder files
- Invent patterns not in the codebase
- Override intentional design decisions
- Include internal/admin-only information
