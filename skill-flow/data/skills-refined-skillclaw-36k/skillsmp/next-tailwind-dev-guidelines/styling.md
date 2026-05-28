# Tailwind CSS Styling Guide

## Tailwind v4 Configuration

This project uses Tailwind CSS v4 with PostCSS:

```javascript
// postcss.config.mjs
import tailwindcss from "@tailwindcss/postcss";

export default {
  plugins: [tailwindcss()],
};
```

## Design System Tokens

### Color Palette

The project uses a custom purple-blue gradient theme optimized for DeFi:

```typescript
// Tailwind color utilities
"bg-gray-950"; // Deep black background
"bg-gray-900"; // Card backgrounds
"bg-gray-800"; // Hover states
"bg-purple-600"; // Primary actions
"bg-blue-600"; // Secondary actions
"text-white"; // Primary text
"text-gray-400"; // Secondary text
"text-purple-400"; // Accent text

// Gradients
"bg-gradient-to-r from-purple-600 to-blue-600";
"bg-gradient-to-br from-purple-900/20 to-blue-900/20";
```

### Z-Index System

```typescript
// src/constants/design-system.ts
export const Z_INDEX = {
  CONTENT: 'z-10',
  BANNER: 'z-20',
  HEADER: 'z-30',
  MODAL: 'z-40',
  TOOLTIP: 'z-50',
} as const;

// Usage
<div className={Z_INDEX.MODAL}>
  <Modal />
</div>
```

### Layout Constants

```typescript
export const HEADER = {
  HEIGHT: "h-16",
  TOP_OFFSET: "top-16",
} as const;

export const CONTAINER = {
  MAX_WIDTH: "max-w-7xl",
  PADDING: "px-4 md:px-6 lg:px-8",
} as const;
```

## Component Styling Patterns

### Gradient Button

```typescript
<button className="
  relative rounded-lg font-semibold
  bg-gradient-to-r from-purple-600 to-blue-600
  hover:from-purple-700 hover:to-blue-700
  text-white px-4 py-2
  transition-all duration-200
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Connect Wallet
</button>
```

### Glass Morphism Card

```typescript
<div className="
  rounded-lg backdrop-blur-lg
  bg-gradient-to-br from-purple-900/20 to-blue-900/20
  border border-purple-500/20
  p-6 shadow-xl
">
  <h3 className="text-xl font-bold mb-4">Card Title</h3>
  <p className="text-gray-400">Card content</p>
</div>
```

### Grid Layout

```typescript
<div className="
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
  gap-4 md:gap-6
">
  {items.map(item => (
    <Card key={item.id} />
  ))}
</div>
```

### Flex Layout

```typescript
// Centered content
<div className="flex items-center justify-center min-h-screen">
  <Content />
</div>

// Space between
<div className="flex items-center justify-between">
  <Logo />
  <Navigation />
</div>

// Vertical stack
<div className="flex flex-col space-y-4">
  <Item1 />
  <Item2 />
</div>
```

## Responsive Design

### Breakpoints

```
sm:  640px   // Tablets
md:  768px   // Small laptops
lg:  1024px  // Laptops
xl:  1280px  // Desktops
2xl: 1536px  // Large desktops
```

### Mobile-First Approach

```typescript
<div className="
  px-4 py-2         // Mobile (default)
  md:px-6 md:py-3   // Tablet and up
  lg:px-8 lg:py-4   // Laptop and up
">
  Content
</div>

// Grid responsive
<div className="
  grid-cols-1       // Mobile: 1 column
  md:grid-cols-2    // Tablet: 2 columns
  lg:grid-cols-3    // Laptop: 3 columns
  gap-4 md:gap-6
">
  {cards}
</div>
```

### Hide/Show at Breakpoints

```typescript
// Hide on mobile, show on desktop
<div className="hidden lg:block">
  <DesktopNav />
</div>

// Show on mobile, hide on desktop
<div className="block lg:hidden">
  <MobileMenu />
</div>
```

## Custom Animations

### Fade In

```typescript
<div className="
  animate-fade-in
  opacity-0 animate-delay-100
">
  Content
</div>

// Tailwind config for custom animation
// tailwind.config.js
{
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    }
  }
}
```

### Pulse for Loading

```typescript
<div className="animate-pulse space-y-4">
  <div className="h-8 bg-gray-800 rounded w-1/3" />
  <div className="h-32 bg-gray-800 rounded" />
</div>
```

### Spin for Loaders

```typescript
<div className="
  animate-spin rounded-full
  h-8 w-8 border-2 border-gray-300
  border-t-purple-600
" />
```

## State Variants

### Hover States

```typescript
<button className="
  bg-purple-600 hover:bg-purple-700
  text-white hover:text-gray-100
  transform hover:scale-105
  transition-all duration-200
">
  Hover Me
</button>
```

### Focus States

```typescript
<input className="
  bg-gray-900 border border-gray-700
  focus:border-purple-500 focus:ring-2 focus:ring-purple-500/50
  focus:outline-none
  rounded-lg px-4 py-2
  transition-all duration-200
" />
```

### Active States

```typescript
<button className="
  bg-purple-600 active:bg-purple-800
  active:scale-95
  transition-all duration-100
">
  Click Me
</button>
```

### Disabled States

```typescript
<button className="
  bg-purple-600 disabled:bg-gray-700
  text-white disabled:text-gray-500
  disabled:cursor-not-allowed
  disabled:opacity-50
" disabled={isDisabled}>
  Submit
</button>
```

## Typography

### Headings

```typescript
<h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
  Main Heading
</h1>

<h2 className="text-3xl md:text-4xl font-bold text-white mb-3">
  Section Heading
</h2>

<h3 className="text-2xl md:text-3xl font-semibold text-white mb-2">
  Subsection
</h3>
```

### Body Text

```typescript
<p className="text-base md:text-lg text-gray-300 leading-relaxed">
  Body paragraph with comfortable line height
</p>

<span className="text-sm text-gray-400">
  Secondary information
</span>

<small className="text-xs text-gray-500">
  Fine print
</small>
```

### Text Truncation

```typescript
// Single line truncation
<p className="truncate w-full">
  Very long text that will be truncated...
</p>

// Multi-line truncation
<p className="line-clamp-3">
  Long text that will be truncated after 3 lines...
</p>
```

## Spacing System

### Margin and Padding Scale

```
0:    0px
px:   1px
0.5:  2px (0.125rem)
1:    4px (0.25rem)
2:    8px (0.5rem)
3:    12px (0.75rem)
4:    16px (1rem)
6:    24px (1.5rem)
8:    32px (2rem)
12:   48px (3rem)
16:   64px (4rem)
```

### Consistent Spacing

```typescript
// Component spacing
<div className="space-y-6">  // Vertical spacing between children
  <Section1 />
  <Section2 />
  <Section3 />
</div>

<div className="space-x-4">  // Horizontal spacing
  <Button1 />
  <Button2 />
</div>

// Card padding
<div className="p-6 md:p-8">  // Consistent padding
  Content
</div>
```

## Dark Mode Optimization

The project uses dark mode by default:

```typescript
// Always assume dark background
<div className="bg-gray-950 text-white">
  {/* Content optimized for dark mode */}
</div>

// Text contrast
<p className="text-white">Primary text</p>
<p className="text-gray-300">Secondary text</p>
<p className="text-gray-400">Tertiary text</p>
<p className="text-gray-500">Muted text</p>
```

## Utility Patterns

### Centering

```typescript
// Flex centering
<div className="flex items-center justify-center min-h-screen">
  <Content />
</div>

// Grid centering
<div className="grid place-items-center min-h-screen">
  <Content />
</div>

// Absolute centering
<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
  <Content />
</div>
```

### Full Screen

```typescript
<div className="min-h-screen w-full">
  <Content />
</div>
```

### Aspect Ratio

```typescript
<div className="aspect-video bg-gray-900">
  <Video />
</div>

<div className="aspect-square bg-gray-900">
  <Image />
</div>
```

## Performance Optimization

### Conditional Classes with clsx

```typescript
import clsx from 'clsx';

function Button({ variant, disabled }: ButtonProps) {
  return (
    <button className={clsx(
      'px-4 py-2 rounded-lg font-semibold transition-all',
      {
        'bg-purple-600 hover:bg-purple-700': variant === 'primary',
        'bg-gray-800 hover:bg-gray-700': variant === 'secondary',
        'opacity-50 cursor-not-allowed': disabled,
      }
    )}>
      Click Me
    </button>
  );
}
```

### Avoid Inline Styles

```typescript
// ❌ Bad: Inline styles
<div style={{ backgroundColor: '#1a1a1a', padding: '16px' }}>
  Content
</div>

// ✅ Good: Tailwind utilities
<div className="bg-gray-900 p-4">
  Content
</div>
```

## Accessibility

### Screen Reader Classes

```typescript
<span className="sr-only">
  Screen reader only text
</span>

<button aria-label="Close modal" className="p-2">
  <XIcon className="w-6 h-6" />
  <span className="sr-only">Close</span>
</button>
```

### Focus Visible

```typescript
<button className="
  focus:outline-none
  focus-visible:ring-2 focus-visible:ring-purple-500
  focus-visible:ring-offset-2 focus-visible:ring-offset-gray-950
">
  Accessible Button
</button>
```

## Best Practices

1. **Mobile-First**: Start with mobile styles, add breakpoints for larger screens
2. **Consistent Spacing**: Use the spacing scale (4, 6, 8, 12, 16)
3. **Color Contrast**: Ensure sufficient contrast for accessibility
4. **Semantic Colors**: Use purple for primary actions, blue for secondary
5. **Animation Performance**: Use `transform` and `opacity` for smooth animations
6. **Class Order**: Group related utilities (layout → spacing → colors → typography)
7. **Extract Components**: Reuse common patterns as components
8. **Avoid !important**: Use Tailwind's layering system instead
