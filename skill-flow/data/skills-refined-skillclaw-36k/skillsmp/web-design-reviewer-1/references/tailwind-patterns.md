# Tailwind CSS Patterns for LucidData

Common Tailwind CSS patterns and conventions used in the LucidData project.

## Layout Patterns

### Responsive Containers

```tsx
// Full-width on mobile, constrained on desktop
<div className="container mx-auto px-4 sm:px-6 lg:px-8">
  {/* content */}
</div>

// Max width with centered content
<div className="max-w-7xl mx-auto px-4">
  {/* content */}
</div>

// Responsive padding
<div className="p-4 sm:p-6 lg:p-8">
  {/* content */}
</div>
```

### Flexbox Layouts

```tsx
// Horizontal stack with responsive wrapping
<div className="flex flex-wrap gap-4">
  {/* items */}
</div>

// Vertical on mobile, horizontal on desktop
<div className="flex flex-col md:flex-row gap-4">
  {/* items */}
</div>

// Space between with centering
<div className="flex items-center justify-between">
  <h1>Title</h1>
  <Button>Action</Button>
</div>

// Centered content
<div className="flex items-center justify-center min-h-screen">
  {/* centered content */}
</div>
```

### Grid Layouts

```tsx
// Responsive grid (1 col mobile, 2 tablet, 3 desktop)
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* grid items */}
</div>

// Auto-fit grid (responsive columns)
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  {/* auto-sizing grid items */}
</div>

// Form grid
<div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4">
  {/* form fields */}
</div>
```

## Typography Patterns

### Headings

```tsx
<h1 className="text-3xl md:text-4xl font-bold tracking-tight">
  Page Title
</h1>

<h2 className="text-2xl md:text-3xl font-semibold">
  Section Title
</h2>

<h3 className="text-xl md:text-2xl font-medium">
  Subsection Title
</h3>
```

### Body Text

```tsx
<p className="text-base leading-relaxed">
  Standard paragraph text
</p>

<p className="text-sm text-muted-foreground">
  Secondary or helper text
</p>

<span className="text-xs font-medium uppercase tracking-wider">
  Label or tag
</span>
```

### Truncation

```tsx
// Single line truncate
<p className="truncate">
  Long text that will be cut off with ellipsis
</p>

// Multi-line truncate (3 lines)
<p className="line-clamp-3">
  Long text that will be cut off after three lines
</p>
```

## Spacing Patterns

### Consistent Spacing

```tsx
// Vertical spacing between sections
<div className="space-y-6">
  <section>Section 1</section>
  <section>Section 2</section>
  <section>Section 3</section>
</div>

// Horizontal spacing between items
<div className="flex space-x-4">
  <Button>Button 1</Button>
  <Button>Button 2</Button>
</div>

// Gap in flex/grid (preferred over space-*)
<div className="flex gap-4">
  <Button>Button 1</Button>
  <Button>Button 2</Button>
</div>
```

### Card Spacing

```tsx
<Card className="p-6">
  <CardHeader className="px-0 pt-0">
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent className="px-0 pb-0">
    {/* content */}
  </CardContent>
</Card>
```

## Color Patterns

### Using CSS Variables

```tsx
// Primary colors
<Button className="bg-primary text-primary-foreground hover:bg-primary/90">
  Primary Button
</Button>

// Muted colors
<div className="bg-muted text-muted-foreground p-4">
  Muted background content
</div>

// Destructive colors
<Button variant="destructive" className="bg-destructive text-destructive-foreground">
  Delete
</Button>

// Border colors
<div className="border border-border rounded-lg">
  {/* content */}
</div>
```

### Opacity Modifiers

```tsx
// 90% opacity
<div className="bg-primary/90">Content</div>

// 50% opacity
<div className="bg-black/50">Overlay</div>

// Hover opacity
<Button className="hover:bg-primary/80">
  Hover me
</Button>
```

## Responsive Patterns

### Show/Hide Based on Breakpoint

```tsx
// Hidden on mobile, visible on desktop
<div className="hidden md:block">
  Desktop-only content
</div>

// Visible on mobile, hidden on desktop
<div className="block md:hidden">
  Mobile-only content
</div>

// Different layouts per breakpoint
<>
  <div className="block lg:hidden">
    <MobileLayout />
  </div>
  <div className="hidden lg:block">
    <DesktopLayout />
  </div>
</>
```

### Responsive Sizing

```tsx
// Full width on mobile, auto on desktop
<Button className="w-full md:w-auto">
  Responsive Button
</Button>

// Responsive height
<div className="h-64 md:h-96 lg:h-screen">
  Responsive height container
</div>

// Responsive max-width
<div className="max-w-full md:max-w-2xl lg:max-w-4xl">
  Responsive width content
</div>
```

## Interactive States

### Hover States

```tsx
<Button className="hover:bg-primary/90 hover:scale-105 transition-all">
  Hover me
</Button>

<a className="text-primary hover:underline hover:text-primary/80">
  Link
</a>
```

### Focus States

```tsx
<Input className="focus:ring-2 focus:ring-primary focus:ring-offset-2" />

<Button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
  Keyboard accessible
</Button>
```

### Active/Selected States

```tsx
<Button
  className={cn(
    "hover:bg-muted",
    isSelected && "bg-muted text-foreground"
  )}
>
  Selectable item
</Button>
```

## Utility Combinations

### className Merger with cn()

```tsx
import { cn } from '@/lib/utils';

// Merge class names with proper precedence
<div className={cn(
  "base-classes",
  condition && "conditional-classes",
  customClassName  // User-provided classes override
)}>
  Content
</div>
```

### Common Combinations

```tsx
// Card with hover effect
<Card className="transition-shadow hover:shadow-lg cursor-pointer">

// Disabled state
<Button
  disabled={isDisabled}
  className={cn(
    "bg-primary text-primary-foreground",
    isDisabled && "opacity-50 cursor-not-allowed"
  )}
>

// Loading state
<Button className={cn(
  isLoading && "opacity-70 pointer-events-none"
)}>
  {isLoading ? "Loading..." : "Submit"}
</Button>
```

## Accessibility Patterns

### Screen Reader Only

```tsx
<span className="sr-only">
  Screen reader only text
</span>
```

### Focus-Visible

```tsx
<a className="focus-visible:ring-2 focus-visible:ring-offset-2">
  Link
</a>
```

### ARIA with Tailwind

```tsx
<button
  aria-expanded={isOpen}
  aria-label="Open menu"
  className="p-2 hover:bg-muted rounded-md focus-visible:ring-2"
>
  <MenuIcon className="h-5 w-5" />
</button>
```

## Animation Patterns

### Transitions

```tsx
// Smooth transition
<div className="transition-all duration-300 ease-in-out">

// Specific property transitions
<div className="transition-colors duration-200">
<div className="transition-transform duration-300">
<div className="transition-opacity duration-150">
```

### Transforms

```tsx
// Hover scale
<div className="hover:scale-105 transition-transform">

// Rotation
<div className="rotate-45">
<div className="hover:rotate-180 transition-transform">

// Translate
<div className="translate-x-4 translate-y-2">
```

## Dark Mode (Future)

```tsx
// Dark mode support (when implemented)
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content
</div>

<p className="text-gray-600 dark:text-gray-400">
  Secondary text
</p>
```

## Best Practices

1. **Mobile-first**: Start with mobile styles, add larger breakpoint styles
2. **Use CSS variables**: Prefer `bg-primary` over `bg-blue-500` for themability
3. **Consistent spacing**: Use spacing scale (4, 6, 8, 12, 16, 24)
4. **Avoid arbitrary values**: Use design tokens instead of `w-[347px]`
5. **Group utilities logically**: Layout → spacing → typography → colors → states
6. **Use cn() utility**: For conditional classes and merging
7. **Avoid !important**: Rely on specificity and cn() utility

---

**For more information:**
- [shadcn Components](shadcn-components.md)
- [Accessibility Guide](accessibility.md)
- [Main Skill Documentation](../SKILL.md)
