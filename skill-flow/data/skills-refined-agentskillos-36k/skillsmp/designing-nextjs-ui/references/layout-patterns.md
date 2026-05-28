# Layout Patterns for Next.js

Responsive layout systems using Tailwind CSS utilities.

## Flexbox Layouts

### Basic Flex Container

```tsx
// Horizontal flex
<div className="flex">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

// Vertical flex
<div className="flex flex-col">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Alignment Patterns

```tsx
// Center everything
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>

// Space between items
<div className="flex justify-between items-center">
  <div>Left</div>
  <div>Right</div>
</div>

// Space around items
<div className="flex justify-around items-center">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

// Evenly spaced
<div className="flex justify-evenly items-center">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Flex Direction & Wrap

```tsx
// Responsive flex direction (stack on mobile, row on desktop)
<div className="flex flex-col md:flex-row">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Flex wrap (items wrap to next line)
<div className="flex flex-wrap gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>
```

### Flex Grow & Shrink

```tsx
// One item takes remaining space
<div className="flex">
  <div className="flex-shrink-0">Fixed width</div>
  <div className="flex-1">Grows to fill space</div>
  <div className="flex-shrink-0">Fixed width</div>
</div>

// Prevent shrinking
<div className="flex">
  <img className="flex-shrink-0 size-12" src="..." />
  <div className="flex-1">Content that wraps</div>
</div>
```

## Grid Layouts

### Basic Grid

```tsx
// 2 columns
<div className="grid grid-cols-2 gap-4">
  <div>01</div>
  <div>02</div>
  <div>03</div>
  <div>04</div>
</div>

// 3 columns
<div className="grid grid-cols-3 gap-4">
  <div>01</div>
  <div>02</div>
  <div>03</div>
</div>

// 4 columns
<div className="grid grid-cols-4 gap-4">
  <div>01</div>
  <div>02</div>
  <div>03</div>
  <div>04</div>
</div>
```

### Responsive Grid

```tsx
// Mobile: 1 col, Tablet: 2 cols, Desktop: 3 cols
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
  <div>Item 5</div>
  <div>Item 6</div>
</div>

// Mobile: 1 col, Desktop: 4 cols
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Grid items */}
</div>
```

### Grid Span (Bento Grid)

```tsx
// Dashboard with varied sizes
<div className="grid grid-cols-1 md:grid-cols-4 gap-4">
  {/* Takes 2 columns and 2 rows */}
  <div className="md:col-span-2 md:row-span-2 rounded-xl bg-white p-6 shadow">
    <h3>Main Chart</h3>
  </div>

  {/* Takes 1 column */}
  <div className="md:col-span-1 rounded-xl bg-white p-6 shadow">
    <h3>KPI 1</h3>
  </div>

  {/* Takes 1 column */}
  <div className="md:col-span-1 rounded-xl bg-white p-6 shadow">
    <h3>KPI 2</h3>
  </div>

  {/* Takes 2 columns */}
  <div className="md:col-span-2 rounded-xl bg-white p-6 shadow">
    <h3>Activity Feed</h3>
  </div>

  {/* Full width */}
  <div className="md:col-span-4 rounded-xl bg-white p-6 shadow">
    <h3>Table</h3>
  </div>
</div>
```

### Auto-Fit & Auto-Fill

```tsx
// Automatically fit columns (min 250px each)
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>

// Auto-fill (creates as many columns as fit)
<div className="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

## Spacing System

### Gap (Space Between Items)

```tsx
// Uniform gap
<div className="flex gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Different horizontal and vertical gaps
<div className="grid grid-cols-2 gap-x-6 gap-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
</div>

// Gap scale: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 56, 64
<div className="flex gap-2">Tight spacing (0.5rem)</div>
<div className="flex gap-4">Default spacing (1rem)</div>
<div className="flex gap-8">Loose spacing (2rem)</div>
```

### Padding

```tsx
// Uniform padding
<div className="p-4">Padding all sides (1rem)</div>
<div className="p-6">Padding all sides (1.5rem)</div>
<div className="p-8">Padding all sides (2rem)</div>

// Directional padding
<div className="px-4 py-2">Horizontal 1rem, Vertical 0.5rem</div>
<div className="pt-4 pb-8">Top 1rem, Bottom 2rem</div>
<div className="pl-6 pr-4">Left 1.5rem, Right 1rem</div>

// Individual sides
<div className="p-4 pl-8">All 1rem, except left 2rem</div>

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">
  Grows with screen size
</div>
```

### Margin

```tsx
// Uniform margin
<div className="m-4">Margin all sides</div>

// Auto margin for centering
<div className="mx-auto max-w-2xl">
  Centered container
</div>

// Directional margin
<div className="mt-8 mb-4">Top 2rem, Bottom 1rem</div>
<div className="ml-auto">Push to right</div>
<div className="mr-auto">Push to left</div>

// Negative margin (overlap)
<div className="-mt-8">Overlaps with previous element</div>

// Responsive margin
<div className="mt-4 md:mt-8 lg:mt-12">
  Increases with screen size
</div>
```

### Space Between (Legacy, prefer gap)

```tsx
// Space between children (useful for lists)
<div className="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<div className="space-x-4">
  <span>Tag 1</span>
  <span>Tag 2</span>
  <span>Tag 3</span>
</div>
```

## Responsive Design Breakpoints

Tailwind uses mobile-first breakpoints:

```tsx
// Default: Mobile styles (< 640px)
// sm: >= 640px (tablets)
// md: >= 768px (tablets landscape, small laptops)
// lg: >= 1024px (laptops, desktops)
// xl: >= 1280px (large desktops)
// 2xl: >= 1536px (extra large screens)

<div className="
  text-sm        /* Mobile: small text */
  sm:text-base   /* Tablet: normal text */
  lg:text-lg     /* Desktop: large text */
">
  Responsive text
</div>

<div className="
  p-4           /* Mobile: 1rem padding */
  md:p-6        /* Tablet: 1.5rem padding */
  lg:p-8        /* Desktop: 2rem padding */
">
  Responsive padding
</div>
```

## Container Patterns

### Max Width Containers

```tsx
// Centered container with max width
<div className="container mx-auto px-4">
  <div>Content</div>
</div>

// Custom max widths
<div className="max-w-sm mx-auto">Small container (384px)</div>
<div className="max-w-md mx-auto">Medium container (448px)</div>
<div className="max-w-lg mx-auto">Large container (512px)</div>
<div className="max-w-xl mx-auto">XL container (576px)</div>
<div className="max-w-2xl mx-auto">2XL container (672px)</div>
<div className="max-w-4xl mx-auto">4XL container (896px)</div>
<div className="max-w-6xl mx-auto">6XL container (1152px)</div>
<div className="max-w-7xl mx-auto">7XL container (1280px)</div>

// Responsive container
<div className="max-w-md md:max-w-2xl lg:max-w-4xl mx-auto px-4">
  Grows with screen size
</div>
```

### Full Width Sections with Constrained Content

```tsx
// Pattern: full-width background, constrained content
<section className="w-full bg-gray-50 py-16">
  <div className="container mx-auto max-w-6xl px-4">
    <h2>Section Title</h2>
    <p>Content stays centered and constrained</p>
  </div>
</section>
```

## Card Grid Pattern

Complete responsive card grid example:

```tsx
export function CardGrid() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-bold mb-8">Featured Products</h2>

      {/* Responsive grid: 1 col mobile, 2 tablet, 3 desktop */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {products.map((product) => (
          <div
            key={product.id}
            className="rounded-xl bg-white p-6 shadow-md transition-shadow hover:shadow-xl"
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-48 object-cover rounded-lg mb-4"
            />
            <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
            <p className="text-gray-600 mb-4">{product.description}</p>
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold text-violet-600">
                ${product.price}
              </span>
              <button className="rounded-lg bg-violet-500 px-4 py-2 text-white transition-colors hover:bg-violet-600">
                Add to Cart
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Sidebar Layout Pattern

```tsx
export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="hidden md:flex md:flex-shrink-0">
        <div className="flex flex-col w-64 bg-gray-900">
          <div className="flex flex-col flex-1 overflow-y-auto">
            <nav className="flex-1 px-4 py-4 space-y-2">
              {/* Navigation items */}
            </nav>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

## Hero Section Pattern

```tsx
export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-600" />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-white mb-6">
            Beautiful Design System
          </h1>
          <p className="text-xl md:text-2xl text-white/90 mb-8">
            Create stunning interfaces with modern layout patterns
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="rounded-full bg-white px-8 py-3 font-semibold text-purple-600">
              Get Started
            </button>
            <button className="rounded-full border-2 border-white px-8 py-3 font-semibold text-white">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </section>
  )
}
```

## Aspect Ratio Containers

```tsx
// 16:9 aspect ratio (videos, images)
<div className="aspect-video w-full">
  <iframe className="w-full h-full" src="..." />
</div>

// Square aspect ratio
<div className="aspect-square w-full">
  <img className="w-full h-full object-cover" src="..." />
</div>

// Custom aspect ratio
<div className="aspect-[4/3] w-full">
  {/* 4:3 content */}
</div>
```

## Sticky Positioning

```tsx
// Sticky header
<header className="sticky top-0 z-50 bg-white shadow">
  <nav className="container mx-auto px-4 py-4">
    {/* Navigation */}
  </nav>
</header>

// Sticky sidebar
<aside className="sticky top-4 h-screen overflow-y-auto">
  {/* Sidebar content */}
</aside>
```
