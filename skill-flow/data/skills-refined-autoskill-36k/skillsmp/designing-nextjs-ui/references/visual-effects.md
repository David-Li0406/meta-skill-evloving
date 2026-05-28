# Visual Effects for Modern UIs

Advanced Tailwind CSS utilities for creating stunning visual effects.

## Gradient Backgrounds

Create eye-catching gradient backgrounds using `bg-gradient-to-{direction}`.

```tsx
// Left to right gradient
<div className="bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
  <h1 className="text-white">Beautiful Gradient</h1>
</div>

// Top to bottom gradient
<div className="bg-gradient-to-b from-blue-500 to-purple-600">
  {/* Content */}
</div>

// Diagonal gradients
<div className="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
  {/* Content */}
</div>
```

**Gradient directions:**
- `bg-gradient-to-r` - Left to right
- `bg-gradient-to-l` - Right to left
- `bg-gradient-to-t` - Bottom to top
- `bg-gradient-to-b` - Top to bottom
- `bg-gradient-to-br` - Top-left to bottom-right
- `bg-gradient-to-bl` - Top-right to bottom-left
- `bg-gradient-to-tr` - Bottom-left to top-right
- `bg-gradient-to-tl` - Bottom-right to top-left

## Gradient Text (Eye-Catching!)

Create stunning gradient text effects using `bg-clip-text`.

```tsx
<h1 className="text-5xl font-extrabold">
  <span className="bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent">
    Hello World
  </span>
</h1>

// Alternative gradient combinations
<span className="bg-gradient-to-r from-teal-400 to-blue-500 bg-clip-text text-transparent">
  Beautiful Gradient Text
</span>

<span className="bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 bg-clip-text text-transparent">
  Multi-stop Gradient
</span>
```

**Pattern:** Always combine these three classes:
1. `bg-gradient-to-{direction}` + color stops
2. `bg-clip-text`
3. `text-transparent`

## Animations

### Bounce Animation (Attention Grabber)

Use `animate-bounce` for scroll indicators or call-to-action elements.

```tsx
<div className="flex justify-center">
  <div className="animate-bounce rounded-full bg-white p-2 shadow-lg">
    <svg className="size-6 text-violet-500" /* ... */>
      <path d="M19 14l-7 7m0 0l-7-7m7 7V3" />
    </svg>
  </div>
</div>
```

### Pulse Animation (Loading States)

Use `animate-pulse` for skeleton loaders and loading indicators.

```tsx
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
  <div className="h-4 bg-gray-200 rounded"></div>
  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
</div>

// Skeleton Card
<div className="rounded-lg bg-white p-4 shadow">
  <div className="flex animate-pulse space-x-4">
    <div className="size-10 bg-gray-200 rounded-full"></div>
    <div className="flex-1 space-y-3 py-1">
      <div className="h-2 bg-gray-200 rounded"></div>
      <div className="h-2 bg-gray-200 rounded w-5/6"></div>
    </div>
  </div>
</div>
```

### Spin Animation (Loading Spinners)

```tsx
<div className="animate-spin rounded-full h-8 w-8 border-b-2 border-violet-500" />
```

## Shadows (Depth & Elevation)

Create visual hierarchy with shadows.

```tsx
// Shadow scale: none, sm, md (default), lg, xl, 2xl
<div className="shadow-sm">Subtle elevation</div>
<div className="shadow-md">Medium elevation</div>
<div className="shadow-lg">Strong elevation</div>
<div className="shadow-xl">Extra strong</div>
<div className="shadow-2xl">Maximum depth</div>

// Colored shadows (requires custom config)
<div className="shadow-lg shadow-purple-500/50">
  Purple glow
</div>

// Drop shadow on text
<h1 className="text-4xl font-bold text-white drop-shadow-lg">
  Text with shadow
</h1>
```

**Shadow tips:**
- Use `shadow-md` for cards at rest
- Use `shadow-lg` or `shadow-xl` for elevated cards
- Use `shadow-2xl` sparingly for modals/dialogs
- Combine with `hover:shadow-xl` for interactive elements

## Backdrop Blur (Glass Morphism)

Create modern frosted glass effects.

```tsx
// Basic backdrop blur
<div className="bg-white/30 backdrop-blur-md rounded-lg p-6">
  <p>Frosted glass effect</p>
</div>

// Blur levels
<div className="backdrop-blur-none">No blur</div>
<div className="backdrop-blur-sm">Subtle blur (4px)</div>
<div className="backdrop-blur-md">Medium blur (12px)</div>
<div className="backdrop-blur-lg">Strong blur (16px)</div>
<div className="backdrop-blur-xl">Extra blur (24px)</div>

// Complete glass morphism card
<div className="relative overflow-hidden rounded-xl bg-white/10 backdrop-blur-lg p-6 shadow-xl ring-1 ring-black/5">
  <div className="relative z-10">
    <h3 className="text-lg font-semibold text-white">Glass Card</h3>
    <p className="text-white/80">Beautiful frosted effect</p>
  </div>
</div>
```

**Glass morphism pattern:**
1. `bg-white/10` or `bg-white/20` - Semi-transparent background
2. `backdrop-blur-lg` or `backdrop-blur-md` - Blur effect
3. `ring-1 ring-black/5` - Subtle border
4. `shadow-xl` - Depth

## Hover & Transition Effects

Make interfaces feel responsive and alive.

```tsx
// Scale on hover
<button className="transform transition hover:scale-105">
  Hover me
</button>

// Shadow lift on hover
<div className="transition-shadow hover:shadow-xl">
  Card with hover effect
</div>

// Combined hover effects
<button className="rounded-lg bg-violet-500 px-6 py-3 text-white transition-all hover:scale-105 hover:shadow-2xl">
  Call to Action
</button>

// Color transition
<a className="text-gray-600 transition-colors hover:text-violet-600">
  Link with color change
</a>

// Background transition
<div className="bg-white transition-colors hover:bg-gray-50">
  Hover background
</div>
```

**Transition utilities:**
- `transition` - All properties (default)
- `transition-colors` - Color properties only
- `transition-transform` - Transform only
- `transition-shadow` - Shadow only
- `transition-all` - All properties

**Duration modifiers:**
- `duration-75` - 75ms
- `duration-150` - 150ms (default)
- `duration-300` - 300ms
- `duration-500` - 500ms
- `duration-700` - 700ms

## Border Radius (Softness)

Control the roundness of corners.

```tsx
// Border radius scale
<div className="rounded-none">Sharp corners (0)</div>
<div className="rounded-sm">Subtle (0.125rem)</div>
<div className="rounded">Default (0.25rem)</div>
<div className="rounded-md">Medium (0.375rem)</div>
<div className="rounded-lg">Large (0.5rem)</div>
<div className="rounded-xl">Extra large (0.75rem)</div>
<div className="rounded-2xl">2X large (1rem)</div>
<div className="rounded-3xl">3X large (1.5rem)</div>
<div className="rounded-full">Perfect circle</div>

// Individual corners
<div className="rounded-t-lg">Top corners only</div>
<div className="rounded-b-lg">Bottom corners only</div>
<div className="rounded-l-lg">Left corners only</div>
<div className="rounded-r-lg">Right corners only</div>
<div className="rounded-tl-lg">Top-left only</div>
<div className="rounded-tr-lg">Top-right only</div>
<div className="rounded-bl-lg">Bottom-left only</div>
<div className="rounded-br-lg">Bottom-right only</div>
```

## Complete Example: Modern Hero Section

```tsx
export function HeroSection() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      {/* Glass morphism card */}
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="max-w-2xl rounded-2xl bg-white/10 p-8 backdrop-blur-lg ring-1 ring-white/20 shadow-2xl">
          {/* Gradient text heading */}
          <h1 className="text-6xl font-extrabold sm:text-7xl">
            <span className="bg-gradient-to-r from-yellow-200 to-pink-200 bg-clip-text text-transparent">
              Beautiful Design
            </span>
          </h1>

          {/* Description */}
          <p className="mt-6 text-xl text-white/90">
            Create stunning websites with modern visual effects
          </p>

          {/* CTA Button with hover effects */}
          <button className="mt-8 rounded-full bg-white px-8 py-3 font-semibold text-purple-600 shadow-xl transition-all hover:scale-105 hover:shadow-2xl">
            Get Started
          </button>

          {/* Bounce indicator */}
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2">
            <div className="animate-bounce rounded-full bg-white p-2">
              <svg className="size-6 text-purple-600">
                {/* Down arrow icon */}
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

## Dark Mode Considerations

Always provide dark mode variants for visual effects.

```tsx
// Gradients in dark mode
<div className="bg-gradient-to-r from-purple-400 to-pink-600 dark:from-purple-600 dark:to-pink-800">
  {/* Content */}
</div>

// Shadows in dark mode
<div className="shadow-lg dark:shadow-none dark:ring-1 dark:ring-white/10">
  {/* Dark mode: replace shadow with subtle ring */}
</div>

// Glass morphism in dark mode
<div className="bg-white/10 backdrop-blur-lg dark:bg-black/20 dark:ring-white/10">
  {/* Adapts to dark backgrounds */}
</div>
```
