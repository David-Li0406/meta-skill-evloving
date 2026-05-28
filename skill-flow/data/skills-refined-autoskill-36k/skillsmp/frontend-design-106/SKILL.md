---
name: frontend-design
description: |
  Designs dark-themed UI with Tailwind CSS, accent gradients, and custom animations for XOP.ai marketing website.
  Use when: Creating new pages, components, or modifying visual elements
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Frontend Design Skill

XOP.ai uses a dark theme with green/purple/yellow accent colors, gradient CTAs, and CSS keyframe animations. The design emphasizes tech credibility for MSP decision-makers through high contrast, bold typography, and purposeful motion.

## Quick Start

### Dark Card with Gradient Border

```tsx
<div className="bg-gray-900 border border-gray-800 rounded-lg p-6 hover:border-green-500 transition-all">
  <div className="text-green-400 mb-4">{icon}</div>
  <h3 className="text-xl font-semibold mb-2">{title}</h3>
  <p className="text-gray-400">{description}</p>
</div>
```

### Gradient CTA Button

```tsx
<Link
  href="/contact"
  className="cta-button bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transform hover:scale-105 transition-all"
>
  Get Started
</Link>
```

### Animated Hero Text

```tsx
<h1 className="text-4xl md:text-6xl font-bold mb-6 animate-fadeIn">
  Static Text Here<br />
  <span className="text-gradient">Animated Gradient Text</span>
</h1>
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Base theme | All pages | `bg-black text-white` |
| Primary accent | Solutions nav, positive states | `text-green-400` |
| Secondary accent | Apps nav, emphasis | `text-yellow-400` |
| Tertiary accent | Resources nav, CTAs | `text-purple-400` |
| Cards | Content containers | `bg-gray-900 border-gray-800 rounded-lg` |
| CTA gradient | Primary actions | `from-purple-600 to-pink-600` |
| Hover state | All interactive | `hover:text-green-400 transition-colors` |

## Common Patterns

### Staggered Card Grid

**When:** Service listings, feature grids

```tsx
<div className="grid md:grid-cols-3 gap-6">
  {items.map((item, index) => (
    <div
      key={index}
      className="service-card bg-gray-900 border border-gray-800 rounded-lg animate-fadeIn"
      style={{ animationDelay: `${(index + 1) * 0.1}s` }}
    >
      {/* Card content */}
    </div>
  ))}
</div>
```

### Form Input

**When:** Contact forms, lead capture

```tsx
<input
  type="text"
  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-[#8BC34A] transition-colors"
/>
```

## See Also

- [aesthetics](references/aesthetics.md)
- [components](references/components.md)
- [layouts](references/layouts.md)
- [motion](references/motion.md)
- [patterns](references/patterns.md)

## Related Skills

- See the **tailwind** skill for utility class patterns
- See the **react** skill for component state management
- See the **nextjs** skill for App Router page structure