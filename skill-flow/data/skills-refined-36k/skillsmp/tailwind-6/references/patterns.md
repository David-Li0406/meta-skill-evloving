# Tailwind Patterns Reference

## Contents
- Dark Theme Design System
- Component Patterns
- Animation Patterns
- Responsive Patterns
- Anti-Patterns

---

## Dark Theme Design System

This project uses a consistent dark theme. NEVER deviate from these base colors.

### Color Palette

```tsx
// Base colors - ALWAYS use these
bg-black         // Page background
text-white       // Primary text
text-gray-300    // Secondary text
text-gray-400    // Muted text, descriptions
bg-gray-900      // Card backgrounds
border-gray-800  // Card borders

// Accent colors
text-green-400   // Primary accent, success states
text-purple-400  // Secondary accent
text-yellow-400  // Tertiary accent
text-blue-400    // Links

// Gradient accent (buttons, highlights)
from-purple-600 to-pink-600
from-green-600 to-emerald-600
```

### Status Color Patterns

```tsx
// Success state
className="bg-green-900/20 border border-green-500/30 text-green-300"

// Error state
className="bg-red-900/20 border border-red-500/30 text-red-300"

// Info/highlight state
className="bg-blue-900/20 border border-blue-500/30 text-blue-300"
```

---

## Component Patterns

### Page Container

```tsx
// DO - Standard page structure
<div className="min-h-screen bg-black text-white">
  <Navigation />
  <section className="px-6 py-16">
    <div className="max-w-7xl mx-auto">
      <h1 className="text-4xl md:text-6xl font-bold text-center mb-6">
        Page Title
      </h1>
    </div>
  </section>
  <Footer />
</div>

// DON'T - Missing responsive padding
<div className="bg-black">
  <div className="max-w-7xl">  {/* Missing mx-auto, px-6 */}
    <h1 className="text-6xl">  {/* Missing responsive text-4xl md:text-6xl */}
```

### Card Component

```tsx
// DO - Consistent card styling
<div className="bg-gray-900 border border-gray-800 rounded-lg p-8">
  <h2 className="text-2xl font-semibold mb-6">Title</h2>
  <p className="text-gray-400">Description</p>
</div>

// DON'T - Inconsistent backgrounds
<div className="bg-gray-800 rounded-lg p-8">  {/* Wrong bg color */}
```

### Interactive Card with Hover

```tsx
// From app/page.tsx - service cards
<div className="service-card rounded-lg cursor-pointer group animate-fadeIn 
  border-4 border-gray-800 border-b-purple-500 bg-gray-900 overflow-hidden"
>
  <div className="h-3 bg-gradient-to-r from-green-500 to-green-400 shimmer"></div>
  <div className="p-6">
    <h3 className="text-xl font-semibold group-hover:text-green-400 transition-colors duration-300">
      {title}
    </h3>
  </div>
</div>
```

### Form Input

```tsx
// DO - Consistent input styling with focus states
<input
  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg 
    focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
/>

// DON'T - Missing focus states
<input className="px-4 py-2 bg-gray-800 border rounded">
```

### CTA Button

```tsx
// Primary CTA
<button className="cta-button bg-gradient-to-r from-purple-600 to-pink-600 
  px-8 py-4 rounded-full font-semibold 
  hover:shadow-lg hover:shadow-purple-500/50 
  transform hover:scale-105 transition-all duration-300">
  Primary Action
</button>

// Secondary CTA
<button className="cta-button bg-gray-800 px-8 py-4 rounded-full font-semibold 
  hover:bg-gray-700 hover:shadow-lg transform hover:scale-105 transition-all duration-300">
  Secondary Action
</button>

// Outline CTA
<button className="border border-green-500/30 px-6 py-3 rounded-full font-semibold 
  hover:bg-green-500/10 transition-colors">
  Tertiary Action
</button>
```

---

## Animation Patterns

Custom animations are defined in `app/globals.css`. Use these classes:

### Available Animation Classes

| Class | Effect | Duration |
|-------|--------|----------|
| `animate-fadeIn` | Fade in + slide up | 0.6s |
| `animate-slideIn` | Slide in from left | 0.8s |
| `animate-float` | Gentle up/down float | 6s infinite |
| `animate-pulse-slow` | Scale pulse | 3s infinite |
| `shimmer` | Gradient shimmer | 2s infinite |

### Staggered Animation Entry

```tsx
// Using animation delays for staggered entry
{items.map((item, index) => (
  <div
    key={index}
    className="animate-fadeIn"
    style={{ animationDelay: `${(index + 1) * 0.1}s` }}
  >
    {item.content}
  </div>
))}
```

### Service Card Stagger (CSS-based)

The `globals.css` includes nth-child delays for `.service-card`:

```tsx
// Automatic stagger - just add the class
<div className="service-card animate-fadeIn">
  {/* Animation delay applied via CSS nth-child rules */}
</div>
```

---

## Responsive Patterns

### Breakpoint Usage

```tsx
// Mobile-first responsive text
<h1 className="text-4xl md:text-6xl font-bold">

// Responsive grid
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

// Responsive flex direction
<div className="flex flex-col sm:flex-row gap-4">

// Hide/show based on breakpoint
<div className="hidden md:flex">  {/* Desktop only */}
<div className="md:hidden">       {/* Mobile only */}
```

### Responsive Container Pattern

```tsx
// Standard responsive container
<div className="max-w-7xl mx-auto px-6">

// Narrower content container
<div className="max-w-4xl mx-auto px-6">

// Full-width with padding
<div className="container mx-auto px-6">
```

---

## Anti-Patterns

### WARNING: Inline Style Objects for Tailwind Values

**The Problem:**

```tsx
// BAD - Using inline styles for values Tailwind handles
<div style={{ backgroundColor: '#1f2937', padding: '2rem' }}>
```

**Why This Breaks:**
1. Loses Tailwind's responsive utilities
2. Can't use hover/focus states
3. Inconsistent with rest of codebase
4. Increases bundle size with duplicate CSS

**The Fix:**

```tsx
// GOOD - Use Tailwind utilities
<div className="bg-gray-800 p-8">
```

### WARNING: Arbitrary Values for Standard Utilities

**The Problem:**

```tsx
// BAD - Using arbitrary values when standard utilities exist
<div className="text-[#22c55e] p-[32px] rounded-[8px]">
```

**Why This Breaks:**
1. Harder to maintain consistency
2. Increases CSS bundle size
3. Misses theme integration

**The Fix:**

```tsx
// GOOD - Use standard utilities
<div className="text-green-500 p-8 rounded-lg">
```

### WARNING: Missing Transition Classes

**The Problem:**

```tsx
// BAD - Hover without transition
<button className="hover:bg-gray-700">
```

**Why This Breaks:**
- Jarring, instant state changes
- Poor user experience
- Inconsistent with other interactive elements

**The Fix:**

```tsx
// GOOD - Include transition
<button className="hover:bg-gray-700 transition-colors">

// For multiple properties
<button className="hover:scale-105 hover:shadow-lg transition-all duration-300">