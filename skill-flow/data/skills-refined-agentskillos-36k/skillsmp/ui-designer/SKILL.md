---
name: ui-designer
description: Generate distinctive, modern UI designs with HTML/CSS/JS. Use when creating UI mockups, design systems, component libraries, or visual prototypes. Applies frontend design best practices for typography, color, motion, and accessibility.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# UI Designer Skill

Generate distinctive, viewable HTML/CSS/JavaScript UI designs that avoid generic "on-distribution" outputs.

## When to Use

Activate this skill when:
- Creating UI mockups or prototypes
- Generating design options for user review
- Building component libraries
- Extracting design systems from reference images
- Implementing visual designs with modern patterns

## Core Principles

### 1. Output Viewable HTML

Always generate complete, self-contained HTML files that:
- Can be opened directly in any browser
- Use Tailwind CSS via CDN for rapid styling
- Include Alpine.js for lightweight interactivity
- Are responsive across all device sizes

### 2. Avoid Generic Defaults

**Typography:**
- AVOID: Inter, Roboto, system-ui as primary fonts
- USE: Playfair Display, Space Grotesk, DM Sans, Outfit, Sora
- Apply high-contrast pairings (serif + sans)
- Use extreme weight variations (900 headlines, 400 body)

**Colors:**
- AVOID: Timid, evenly-distributed palettes
- USE: Dominant color commitment with sharp accents
- Draw from IDEs, editorial design, cultural aesthetics
- Default to dark mode when appropriate

**Motion:**
- AVOID: Scattered, disconnected animations
- USE: Orchestrated page-load sequences
- Stagger reveals for visual hierarchy
- Always respect `prefers-reduced-motion`

**Backgrounds:**
- AVOID: Flat solid colors
- USE: Layered gradients, mesh gradients
- Subtle geometric patterns or grain textures
- Atmospheric depth through color layering

### 3. Generate 3 Diverse Options

When designing, create 3 meaningfully different approaches:

| Option | Layout | Style | Density |
|--------|--------|-------|---------|
| 1 | Traditional/Familiar | Conservative | Dense |
| 2 | Modern/Bold | Expressive | Balanced |
| 3 | Minimal/Clean | Elegant | Spacious |

### 4. Accessibility First

Every design MUST include:
- Skip link to main content
- Color contrast >= 4.5:1 (7:1 preferred)
- Touch targets >= 44x44px
- Proper heading hierarchy (h1 -> h2 -> h3)
- ARIA labels on icon buttons
- Focus-visible styles on all interactive elements
- `prefers-reduced-motion` media query support

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['DM Sans', 'system-ui', 'sans-serif'],
            display: ['Space Grotesk', 'system-ui', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0ea5e9',
              600: '#0284c7',
              700: '#0369a1',
              900: '#0c4a6e',
            }
          }
        }
      }
    }
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
  </style>
</head>
<body class="bg-gray-50 dark:bg-gray-900 min-h-screen antialiased">
  <!-- Skip Link -->
  <a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-brand-600 text-white px-4 py-2 rounded-lg z-50">
    Skip to main content
  </a>

  <!-- Content here -->
  <main id="main">
  </main>

  <!-- Alpine.js for interactivity -->
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</body>
</html>
```

## Reference Image Analysis

When provided with reference images, extract and document:

```markdown
## Extracted Design System

### Colors
- Primary: [hex]
- Secondary: [hex]
- Accent: [hex]
- Background: [hex]
- Text: [hex]
- Border: [hex]

### Typography
- Heading Font: [family]
- Body Font: [family]
- Heading Sizes: [h1: Xpx, h2: Xpx, h3: Xpx]
- Body Size: [Xpx]
- Line Height: [X]

### Spacing
- Base Unit: [Xpx]
- Section Padding: [X]
- Card Padding: [X]
- Element Gap: [X]

### Components
- Button Style: [description]
- Card Style: [description]
- Input Style: [description]
- Navigation: [description]

### Visual Tone
[Corporate / Playful / Minimal / Premium / etc.]
```

## File Output Structure

```
designs/
├── options/
│   ├── option-1.html
│   ├── option-2.html
│   ├── option-3.html
│   └── comparison.html
├── refined/
│   └── v1.html, v2.html...
├── final/
│   ├── index.html
│   ├── pages/
│   └── components/
└── design-system.md
```

## Interaction with User

1. Present 3 options with comparison page
2. Ask user to select direction
3. Refine based on feedback
4. Iterate until "approved"
5. Generate final deliverables
