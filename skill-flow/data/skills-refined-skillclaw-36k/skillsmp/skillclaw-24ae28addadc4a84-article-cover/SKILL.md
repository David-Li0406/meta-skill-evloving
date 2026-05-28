---
name: article-cover
description: Use this skill when you want to generate professional article cover images in SVG format for blogs, technical articles, or documentation, ensuring they are visually appealing and well-structured.
---

# Article Cover SVG Generation

Generate professional, visually striking article cover images in SVG format for technical blogs, documentation, and articles.

## Critical Rules

1. **ViewBox Standard**: Use `viewBox="0 0 1200 630"` (social media friendly 1.91:1 ratio).

2. **Text Readability (MUST follow)**:
   - Main title: 44-48px, bold, high contrast.
   - Subtitle: 28-32px, white or light color.
   - Labels/tags: 14-16px.
   - Never use fonts smaller than 11px.

3. **Background Design**:
   - Always use gradient backgrounds (avoid flat solid colors).
   - Dark tech themes: `#0d1117` → `#161b22` (GitHub dark style).
   - Add subtle grid patterns or decorative elements for depth.

4. **Visual Hierarchy**:
   - Title area: bottom 1/3 of the image (y: 420-540).
   - Diagram/illustration area: top 2/3 (y: 80-400).
   - Tags/labels: bottom edge (y: 550-600).

5. **Color Contrast**: Ensure text is readable against backgrounds.
   - Light text on dark backgrounds.
   - Use gradients for emphasis (orange/yellow for tech, blue/cyan for data).

## Design Patterns

### Tech Article Cover (Comparison Layout)
Best for: Performance comparisons, version upgrades, before/after scenarios.

```
┌─────────────────────────────────────────────────┐
│  [Logo]                           [Badge: 100x+]│
│                                                 │
│  ┌─────────┐    VS    ┌─────────┐    ┌────────┐│
│  │ Before  │  ────►   │ Middle  │ ►  │ After  ││
│  │  ❌     │          │   ⚠     │    │   ✓    ││
│  └─────────┘          └─────────┘    └────────┘│
│                                                 │
│         Main Title (Large, Gradient)            │
│           Subtitle (Medium, White)              │
│                                                 │
│    [Tag1]  [Tag2]  [Tag3]  [Tag4]  [Tag5]      │
└─────────────────────────────────────────────────┘
```

### Tech Article Cover (Flow Layout)
Best for: Process explanations, architecture overviews.

```
┌─────────────────────────────────────────────────┐
│  [Logo]                                         │
│                                                 │
│  [Input] ──► [Process Box] ──► [Output]       │
└─────────────────────────────────────────────────┘
```