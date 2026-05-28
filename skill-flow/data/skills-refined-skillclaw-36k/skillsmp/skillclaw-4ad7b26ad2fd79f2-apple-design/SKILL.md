---
name: apple-design
description: Use this skill when creating modern, minimalist UI designs inspired by Apple's design language, featuring glassmorphism, smooth animations, and generous whitespace.
---

# Apple Design System

Create stunning, modern UI designs inspired by Apple's design language. This design system provides guidelines, components, and patterns for building clean, minimalist interfaces with attention to detail, smooth animations, and premium aesthetics.

## When to Use This Skill

Use this skill when:
- Designing portfolio websites or personal sites
- Creating landing pages or product showcases
- Implementing hero sections with visual impact
- Building card-based layouts for projects or products
- Adding glassmorphism or frosted glass effects
- Implementing smooth, delightful animations
- Creating dark mode compatible designs
- Designing navigation bars, modals, or forms
- Building contact forms or call-to-action sections
- Working with modern CSS features (backdrop-filter, gradients, shadows)

## Quick Start

### 1. Core Design Principles

**Minimalism**: Remove unnecessary elements, focus on content.  
**Typography**: Large, bold headlines with system fonts.  
**Colors**: Neutral base with strategic accent colors.  
**Spacing**: 8px grid system with generous whitespace.  
**Effects**: Glassmorphism, soft shadows, smooth animations.  
**Imagery**: High-quality, properly sized images.

📖 **Detailed guide**: [design-principles.md](references/design-principles.md)

### 2. Color System

```css
/* Light Mode */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f7;
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --accent-blue: #0071e3;
  --accent-green: #30d158;
  --border-color: rgba(0, 0, 0, 0.1);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #000000;
    --bg-secondary: #1d1d1f;
    --text-primary: #f5f5f7;
    --text-secondary: #a1a1a6;
    --accent-blue: #0a84ff;
    --border-color: rgba(255, 255, 255, 0.1);
  }
}
```

📖 **Complete palette**: [color-system.md](references/color-system.md)

### 3. Typography

```css
/* System font stack */
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
             'Segoe UI', sans-serif;

/* Fluid responsive typography */
h1 {
  font-size: clamp(2.5rem, 5vw + 1rem, 4.5rem);
  font-weight: 700;
  line-height: 1.1;
}
```