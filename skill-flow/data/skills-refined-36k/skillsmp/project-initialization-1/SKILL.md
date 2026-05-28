---
name: project-initialization
description: |
  PROJECT.md and BRAND.md creation patterns and templates.

  ACTIVATE when: new project setup, /project-guide command, /brand-guide command,
  user mentions "create project", "new project", "brand guidelines", "project definition".

  <example>
  User runs /project-guide
  → Load this skill for PROJECT.md template and question patterns
  </example>

  <example>
  User runs /brand-guide
  → Load this skill for BRAND.md template and Refactoring UI color/typography guidance
  </example>
---

# Project Initialization Skill

Patterns and templates for creating PROJECT.md and BRAND.md files.

## PROJECT.md Structure

### Required Sections
1. **Project Name & Tagline** - One-sentence description
2. **Mission** - Core purpose (1-2 sentences)
3. **Vision** - Long-term goal
4. **Target Audience** - Who uses this
5. **Problem Statement** - What problem it solves
6. **Solution** - How it solves the problem
7. **Core Features** - Top 3-5 features

### Optional Sections
- Success Metrics
- Competitive Landscape
- Technical Constraints

## BRAND.md Structure

### Required Sections
1. **Brand Personality** - Character attributes
2. **Color Palette** - Primary, secondary, semantic colors
3. **Typography** - Font stack and scale
4. **Tone of Voice** - Communication style

### Optional Sections
- Logo Usage
- Spacing System
- Iconography
- Shadow Scale

## Color System (Refactoring UI)

### Creating a Color Palette

1. **Choose base primary color**
   - Must work as button background with white text
   - Start with HSL for easier manipulation

2. **Create 9 shades (100-900)**
   - 500 is the base color
   - Lighter: Increase L, decrease S slightly
   - Darker: Decrease L, increase S

3. **HSL Manipulation Rules**
   - Lighter shades: Rotate H toward nearest bright point (60°, 180°, 300°)
   - Darker shades: Rotate H toward nearest dark point (0°, 120°, 240°)
   - Avoid going below 10% S for colors (use grays instead)

4. **Add neutral grays (8-10 shades)**
   - Should have slight tint from primary
   - Cool grays for tech, warm for friendly brands

5. **Add semantic colors**
   - Success: Green-based
   - Warning: Yellow/orange-based
   - Error: Red-based
   - Info: Blue-based

### Color Palette Template
```
Primary:
  50:  hsl(H, S%, 97%)  - Lightest background
  100: hsl(H, S%, 94%)  - Light background
  200: hsl(H, S%, 86%)  - Light accent
  300: hsl(H, S%, 74%)  - Border
  400: hsl(H, S%, 60%)  - Disabled state
  500: hsl(H, S%, 50%)  - Primary (base)
  600: hsl(H, S%, 42%)  - Hover
  700: hsl(H, S%, 34%)  - Active
  800: hsl(H, S%, 26%)  - Dark accent
  900: hsl(H, S%, 18%)  - Darkest
```

## Typography Scale (Refactoring UI)

### Base Scale (4px baseline)
| Name | Size | Line Height | Use |
|------|------|-------------|-----|
| xs | 12px | 16px (1.33) | Captions, fine print |
| sm | 14px | 20px (1.43) | Labels, meta |
| base | 16px | 24px (1.5) | Body text |
| lg | 18px | 28px (1.56) | Large body, emphasis |
| xl | 20px | 28px (1.4) | Small headings |
| 2xl | 24px | 32px (1.33) | Section headings |
| 3xl | 30px | 36px (1.2) | Page headings |
| 4xl | 36px | 40px (1.11) | Large headings |
| 5xl | 48px | 48px (1) | Hero text |

### Font Weight Guidelines
- 400 (Regular): Body text
- 500 (Medium): Subtle emphasis
- 600 (Semibold): Headings, labels
- 700 (Bold): Strong emphasis, buttons

## Spacing System (4px Grid)

| Token | Value | Usage |
|-------|-------|-------|
| 0 | 0 | None |
| px | 1px | Borders |
| 0.5 | 2px | Micro |
| 1 | 4px | Tight |
| 2 | 8px | Small gaps |
| 3 | 12px | Compact |
| 4 | 16px | Default |
| 5 | 20px | Comfortable |
| 6 | 24px | Section gaps |
| 8 | 32px | Large gaps |
| 10 | 40px | Extra large |
| 12 | 48px | Major separation |
| 16 | 64px | Hero spacing |

## Shadow Scale

| Level | CSS Value | Usage |
|-------|-----------|-------|
| xs | 0 1px 2px 0 rgb(0 0 0 / 0.05) | Subtle |
| sm | 0 1px 3px 0 rgb(0 0 0 / 0.1) | Buttons |
| md | 0 4px 6px -1px rgb(0 0 0 / 0.1) | Cards |
| lg | 0 10px 15px -3px rgb(0 0 0 / 0.1) | Dropdowns |
| xl | 0 20px 25px -5px rgb(0 0 0 / 0.1) | Modals |
| 2xl | 0 25px 50px -12px rgb(0 0 0 / 0.25) | Hero |

## References
- [references/project-template.md](references/project-template.md) - Full PROJECT.md template
- [references/brand-template.md](references/brand-template.md) - Full BRAND.md template
- [references/questions.md](references/questions.md) - Interactive wizard questions
