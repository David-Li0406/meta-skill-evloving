# Layouts Reference

## Contents
- Page Structure
- Grid Patterns
- Spacing Scale
- Responsive Breakpoints
- Container Widths

## Page Structure

Every page follows this structure:

```tsx
<div className="min-h-screen bg-black text-white">
  <Navigation />
  
  {/* Hero Section */}
  <section className="px-6 py-16 text-center">
    <div className="max-w-4xl mx-auto">
      {/* Hero content */}
    </div>
  </section>
  
  {/* Content Sections */}
  <section className="px-6 py-16">
    <div className="max-w-6xl mx-auto">
      {/* Section content */}
    </div>
  </section>
  
  <Footer />
</div>
```

### WARNING: Missing min-h-screen

**The Problem:**
```tsx
// BAD - Page can collapse if content is short
<div className="bg-black text-white">
```

**Why This Breaks:** Footer won't stick to bottom on short pages.

**The Fix:**
```tsx
// GOOD - Always use min-h-screen on page wrapper
<div className="min-h-screen bg-black text-white">
```

## Grid Patterns

### Three-Column Service Grid

```tsx
<div className="grid md:grid-cols-3 gap-6">
  {services.map((service, index) => (
    <div key={index}>{/* Card */}</div>
  ))}
</div>
```

### Four-Column Stats Grid

```tsx
<div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
  {stats.map((stat, index) => (
    <div key={index}>
      <div className="text-3xl md:text-4xl font-bold text-green-400">{stat.value}</div>
      <div className="text-sm text-gray-400 mt-2">{stat.label}</div>
    </div>
  ))}
</div>
```

### Two-Column Form Layout

```tsx
<div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto">
  <div className="bg-gray-900 rounded-lg p-8">
    {/* Form */}
  </div>
  <div className="space-y-8">
    {/* Info cards */}
  </div>
</div>
```

### Two-Column Feature Grid

```tsx
<div className="grid md:grid-cols-2 gap-8">
  {features.map((feature, index) => (
    <div key={index}>{/* Feature card */}</div>
  ))}
</div>
```

## Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| `gap-4` | 1rem | Tight grouping (buttons, form fields) |
| `gap-6` | 1.5rem | Card grids |
| `gap-8` | 2rem | Section internal spacing |
| `py-12` | 3rem | Small sections |
| `py-16` | 4rem | Standard sections |
| `mb-4` | 1rem | Heading to content |
| `mb-6` | 1.5rem | Subheading to content |
| `mb-8` | 2rem | Hero text to CTA |
| `mb-12` | 3rem | Section heading to grid |

## Responsive Breakpoints

Tailwind defaults, mobile-first:

| Prefix | Min-width | Usage |
|--------|-----------|-------|
| (none) | 0 | Mobile base |
| `md:` | 768px | Tablet, grid columns |
| `lg:` | 1024px | Desktop, 5-column footer |

### Common Responsive Patterns

```tsx
// Typography
<h1 className="text-4xl md:text-6xl font-bold">

// Grid columns
<div className="grid md:grid-cols-3 gap-6">

// Footer grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">

// Flex direction
<div className="flex flex-col sm:flex-row gap-4">
```

## Container Widths

| Class | Usage |
|-------|-------|
| `max-w-3xl mx-auto` | Centered text blocks |
| `max-w-4xl mx-auto` | Hero sections |
| `max-w-5xl mx-auto` | CTA sections |
| `max-w-6xl mx-auto` | Content sections |
| `max-w-7xl mx-auto` | Full-width grids |
| `container mx-auto` | Navigation, footer |

### Section Pattern

```tsx
<section className="px-6 py-16">
  <div className="max-w-6xl mx-auto">
    <h2 className="text-3xl font-bold text-center mb-12">{title}</h2>
    {/* Content */}
  </div>
</section>
```

### Alternating Background

```tsx
{/* Standard section */}
<section className="px-6 py-16">

{/* Highlighted section */}
<section className="px-6 py-16 bg-gray-900/50">

{/* Gradient section */}
<section className="px-6 py-16 bg-gradient-to-r from-gray-900 to-black">