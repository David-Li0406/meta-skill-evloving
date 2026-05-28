---
name: tailwind
description: |
  Applies Tailwind CSS utilities for dark theme, animations, and responsive design
  Use when: Styling components, creating layouts, implementing animations, or building responsive interfaces
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Tailwind Skill

This project uses Tailwind CSS 3.x with a dark theme design system. The site features a black background (`bg-black`) with green, purple, and pink accent colors. Custom animations are defined in `app/globals.css` and applied via utility classes.

## Quick Start

### Page Layout Pattern

```tsx
<div className="min-h-screen bg-black text-white">
  <Navigation />
  <section className="px-6 py-16">
    <div className="max-w-7xl mx-auto">
      {/* Content */}
    </div>
  </section>
  <Footer />
</div>
```

### Card Pattern

```tsx
<div className="bg-gray-900 border border-gray-800 rounded-lg p-8">
  <h2 className="text-2xl font-semibold mb-6">Card Title</h2>
  <p className="text-gray-400">Card content</p>
</div>
```

### CTA Button Pattern

```tsx
<button className="cta-button bg-gradient-to-r from-purple-600 to-pink-600 px-8 py-4 rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transform hover:scale-105 transition-all duration-300">
  Take Action
</button>
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Dark theme base | All pages | `bg-black text-white` |
| Accent colors | Links, highlights | `text-green-400`, `text-purple-400` |
| Cards | Content containers | `bg-gray-900 border-gray-800 rounded-lg` |
| Gradients | Buttons, highlights | `from-purple-600 to-pink-600` |
| Custom animations | Entry effects | `animate-fadeIn`, `animate-float` |
| Animation delays | Staggered entry | `.delay-100` through `.delay-500` |

## Common Patterns

### Responsive Grid

**When:** Displaying cards or content in columns

```tsx
<div className="grid md:grid-cols-3 gap-6">
  {items.map((item, index) => (
    <div key={index} className="bg-gray-900 rounded-lg p-6">
      {item.content}
    </div>
  ))}
</div>
```

### Form Input Styling

**When:** Creating form fields

```tsx
<input
  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
/>
```

### Status Messages

**When:** Showing success or error states

```tsx
// Success
<div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4 text-green-300">
  Success message
</div>

// Error
<div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-300">
  Error message
</div>
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **react** skill for component patterns and state management
- See the **nextjs** skill for App Router conventions and page structure
- See the **typescript** skill for type-safe component props

## Documentation Resources

> Fetch latest Tailwind CSS documentation with Context7.

**How to use Context7:**
1. Use `mcp__context7__resolve-library-id` to search for "tailwindcss"
2. **Prefer website documentation** (IDs starting with `/websites/`) over source code repositories
3. Query with `mcp__context7__query-docs` using the resolved library ID

**Library ID:** `/websites/v3_tailwindcss` _(Tailwind CSS v3 documentation - highest benchmark score)_

**Recommended Queries:**
- "responsive design breakpoints"
- "dark mode configuration"
- "custom animations keyframes"
- "gradient backgrounds"