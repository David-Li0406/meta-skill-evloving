# Utility Class Patterns

## Layout Utilities

### Flexbox

```tsx
// Basic flex container
<div className="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

// Flex column with gap
<div className="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

// Centering content
<div className="flex items-center justify-center min-h-screen">
  <div>Centered content</div>
</div>

// Flex wrap
<div className="flex flex-wrap gap-2">
  {items.map(item => <Tag key={item.id}>{item.name}</Tag>)}
</div>
```

### Grid

```tsx
// Basic grid
<div className="grid grid-cols-3 gap-4">
  <div>Col 1</div>
  <div>Col 2</div>
  <div>Col 3</div>
</div>

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {products.map(product => <ProductCard key={product.id} product={product} />)}
</div>

// Grid with span
<div className="grid grid-cols-4 gap-4">
  <div className="col-span-2">Wide item</div>
  <div>Normal</div>
  <div>Normal</div>
</div>

// Auto-fit grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  {items.map(item => <Card key={item.id} />)}
</div>
```

### Container

```tsx
// Centered container with padding
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  <main>Content</main>
</div>

// Full-width with max content width
<div className="w-full">
  <div className="mx-auto max-w-prose">
    <article>Readable width content</article>
  </div>
</div>
```

## Spacing Utilities

### Padding

```tsx
// All sides
<div className="p-4">Padding all sides</div>

// Horizontal & Vertical
<div className="px-6 py-4">Different x/y padding</div>

// Individual sides
<div className="pt-8 pb-4 pl-6 pr-6">Individual padding</div>

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">Responsive padding</div>
```

### Margin

```tsx
// Auto margin for centering
<div className="mx-auto max-w-md">Centered block</div>

// Negative margin
<div className="-mt-4">Overlapping element</div>

// Space between children
<div className="space-y-4">
  <p>Paragraph 1</p>
  <p>Paragraph 2</p>
  <p>Paragraph 3</p>
</div>
```

### Gap

```tsx
// Flex gap
<div className="flex gap-4">
  <button>Button 1</button>
  <button>Button 2</button>
</div>

// Grid gap
<div className="grid grid-cols-3 gap-x-4 gap-y-8">
  {/* Different horizontal and vertical gaps */}
</div>
```

## Typography Utilities

### Font Size & Weight

```tsx
// Headings
<h1 className="text-4xl font-bold">Main Heading</h1>
<h2 className="text-2xl font-semibold">Subheading</h2>
<h3 className="text-xl font-medium">Section Title</h3>

// Body text
<p className="text-base text-gray-700">Regular paragraph</p>
<p className="text-sm text-gray-500">Small text</p>
<span className="text-xs uppercase tracking-wide">Label</span>
```

### Text Alignment & Wrapping

```tsx
// Alignment
<p className="text-left">Left aligned</p>
<p className="text-center">Centered</p>
<p className="text-right">Right aligned</p>
<p className="text-justify">Justified text</p>

// Wrapping
<h1 className="text-balance">Balanced heading that wraps nicely</h1>
<p className="text-pretty">Pretty wrapped paragraph</p>

// Truncation
<p className="truncate">Long text that will be truncated...</p>
<p className="line-clamp-3">Text clamped to 3 lines maximum...</p>
```

### Text Color

```tsx
// Semantic colors
<p className="text-gray-900 dark:text-gray-100">Primary text</p>
<p className="text-gray-600 dark:text-gray-400">Secondary text</p>
<p className="text-gray-400 dark:text-gray-600">Muted text</p>

// Status colors
<span className="text-green-600">Success message</span>
<span className="text-red-600">Error message</span>
<span className="text-yellow-600">Warning message</span>
<span className="text-blue-600">Info message</span>
```

## Color Utilities

### Background Colors

```tsx
// Solid backgrounds
<div className="bg-white dark:bg-gray-900">Light/dark background</div>
<div className="bg-gray-100 dark:bg-gray-800">Subtle background</div>
<div className="bg-blue-500">Brand background</div>

// Transparent/opacity
<div className="bg-black/50">50% transparent black overlay</div>
<div className="bg-white/80 backdrop-blur-sm">Frosted glass effect</div>
```

### Gradients

```tsx
// Linear gradient
<div className="bg-gradient-to-r from-blue-500 to-purple-500">
  Horizontal gradient
</div>

// Diagonal gradient
<div className="bg-gradient-to-br from-pink-500 via-red-500 to-yellow-500">
  Diagonal with middle color
</div>

// Gradient text
<h1 className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
  Gradient Text
</h1>
```

## Border Utilities

### Border Width & Color

```tsx
// Basic border
<div className="border border-gray-200 dark:border-gray-700">
  Default border
</div>

// Specific sides
<div className="border-b border-gray-200">Bottom border only</div>
<div className="border-l-4 border-blue-500">Left accent border</div>

// Dividers
<div className="divide-y divide-gray-200">
  <div className="py-4">Section 1</div>
  <div className="py-4">Section 2</div>
  <div className="py-4">Section 3</div>
</div>
```

### Border Radius

```tsx
// Standard radii
<div className="rounded">Small radius</div>
<div className="rounded-md">Medium radius</div>
<div className="rounded-lg">Large radius</div>
<div className="rounded-xl">Extra large radius</div>
<div className="rounded-full">Fully rounded (pill/circle)</div>

// Specific corners
<div className="rounded-t-lg">Top corners only</div>
<div className="rounded-tl-lg rounded-br-lg">Diagonal corners</div>
```

## Shadow Utilities

```tsx
// Elevation shadows
<div className="shadow-sm">Subtle shadow</div>
<div className="shadow">Default shadow</div>
<div className="shadow-md">Medium shadow</div>
<div className="shadow-lg">Large shadow</div>
<div className="shadow-xl">Extra large shadow</div>

// Colored shadow
<div className="shadow-lg shadow-blue-500/25">Blue tinted shadow</div>

// Inner shadow
<div className="shadow-inner">Inset shadow</div>
```

## Interactive States

### Hover & Focus

```tsx
<button className="
  bg-blue-500 text-white
  hover:bg-blue-600
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-700
  transition-colors
">
  Interactive Button
</button>
```

### Disabled State

```tsx
<button
  disabled={isLoading}
  className="
    bg-blue-500 text-white
    disabled:bg-gray-300 disabled:text-gray-500
    disabled:cursor-not-allowed
  "
>
  {isLoading ? "Loading..." : "Submit"}
</button>
```

### Focus Visible

```tsx
// Only show focus ring on keyboard navigation
<button className="
  focus:outline-none
  focus-visible:ring-2 focus-visible:ring-blue-500
">
  Keyboard accessible
</button>
```

## Animation Utilities

### Transitions

```tsx
// Basic transition
<div className="transition-colors duration-200 hover:bg-gray-100">
  Color transition
</div>

// Multiple properties
<div className="transition-all duration-300 ease-in-out hover:scale-105 hover:shadow-lg">
  Transform + shadow
</div>

// Specific properties
<div className="transition-opacity duration-500">
  Opacity only
</div>
```

### Animations

```tsx
// Built-in animations
<div className="animate-spin">Spinning loader</div>
<div className="animate-pulse">Pulsing placeholder</div>
<div className="animate-bounce">Bouncing element</div>
<div className="animate-ping">Ping effect</div>
```

## Responsive Patterns

### Mobile-First Approach

```tsx
// Start with mobile, add larger breakpoints
<div className="
  p-4      // Base (mobile)
  sm:p-6   // 640px+
  md:p-8   // 768px+
  lg:p-10  // 1024px+
  xl:p-12  // 1280px+
">
  Responsive padding
</div>
```

### Hide/Show at Breakpoints

```tsx
// Hide on mobile, show on desktop
<div className="hidden md:block">Desktop only</div>

// Show on mobile, hide on desktop
<div className="block md:hidden">Mobile only</div>

// Different display types
<div className="hidden md:flex lg:grid">Responsive display</div>
```

### Responsive Text

```tsx
<h1 className="
  text-2xl
  sm:text-3xl
  md:text-4xl
  lg:text-5xl
  xl:text-6xl
">
  Responsive Heading
</h1>
```

## Dark Mode

### Basic Dark Mode

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Adapts to color scheme
</div>
```

### Dark Mode Components

```tsx
<div className="
  bg-white dark:bg-gray-800
  border border-gray-200 dark:border-gray-700
  text-gray-900 dark:text-gray-100
  shadow-sm dark:shadow-gray-900/20
  rounded-lg p-6
">
  <h3 className="text-lg font-semibold">Card Title</h3>
  <p className="text-gray-600 dark:text-gray-400 mt-2">
    Card description with muted text.
  </p>
</div>
```
