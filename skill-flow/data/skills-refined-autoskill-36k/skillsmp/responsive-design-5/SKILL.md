---
name: responsive-design
description: Implement mobile-first responsive design for NutriProfile. Use this skill when working on UI components, fixing layout issues, ensuring touch targets, or optimizing for different screen sizes (375px to 1920px+). Uses Tailwind CSS breakpoints.
allowed-tools: Read,Write,Edit,Grep,Glob
---

# NutriProfile Responsive Design Skill

You are a responsive design expert for the NutriProfile application. This skill helps you implement mobile-first layouts that work across all screen sizes from 375px (iPhone SE) to 1920px+ (desktop).

## Mobile-First Approach

ALWAYS design for mobile first, then add breakpoints for larger screens.

```typescript
// ✅ CORRECT: Mobile-first
className="text-sm sm:text-base md:text-lg lg:text-xl"

// ❌ WRONG: Desktop-first
className="text-xl lg:text-lg md:text-base sm:text-sm"
```

## Tailwind Breakpoints

| Prefix | Min Width | Target Device |
|--------|-----------|---------------|
| (none) | 0px | Mobile (iPhone SE, 375px) |
| `sm:` | 640px | Large phones, small tablets |
| `md:` | 768px | Tablets (iPad) |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large desktops |

## Common Patterns

### Typography

```typescript
// Page titles
className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold"

// Section headings
className="text-xl sm:text-2xl md:text-3xl font-semibold"

// Body text
className="text-sm sm:text-base"

// Small text / labels
className="text-xs sm:text-sm"

// Navigation labels (bottom nav)
className="text-[10px] sm:text-xs"
```

### Spacing

```typescript
// Container padding
className="p-3 sm:p-4 md:p-6 lg:p-8"

// Section padding
className="py-12 sm:py-16 md:py-20 lg:py-24"

// Grid gaps
className="gap-2 sm:gap-3 md:gap-4 lg:gap-6"

// Component margins
className="mb-4 sm:mb-6 md:mb-8"
```

### Grid Layouts

```typescript
// Cards grid
className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4"

// Dashboard widgets
className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4"

// Form layout
className="grid grid-cols-1 md:grid-cols-2 gap-4"
```

### Buttons

```typescript
// Full width on mobile, auto on desktop
className="w-full sm:w-auto"

// Touch-friendly size (min 44px)
className="px-4 py-3 sm:px-6 sm:py-3 min-h-[44px] text-sm sm:text-base"

// Icon buttons
className="p-2 sm:p-3 min-h-[44px] min-w-[44px]"
```

### Modals

```typescript
// Modal container - never exceed viewport
className="fixed inset-0 z-50 flex items-center justify-center p-4"

// Modal content - responsive width
className="relative w-full max-w-[calc(100vw-32px)] sm:max-w-md md:max-w-lg bg-white rounded-xl"

// Modal with max height
className="max-h-[calc(100vh-32px)] overflow-y-auto"
```

### Navigation

#### Bottom Navigation (Mobile)
```typescript
// Container
className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t safe-area-bottom"

// Nav items
className="flex justify-around items-center h-16 sm:h-20"

// Nav item
className="flex flex-col items-center justify-center py-2 px-3 min-w-[64px]"

// Icon
className="h-5 w-5 sm:h-6 sm:w-6"

// Label
className="text-[10px] sm:text-xs mt-1 truncate max-w-[48px] sm:max-w-none"
```

#### Header Navigation (Desktop)
```typescript
// Show on larger screens only
className="hidden md:flex items-center space-x-6"
```

### Decorative Elements (Blobs)

```typescript
// CRITICAL: Size blobs responsively to prevent overflow
className="
  absolute -top-20 -left-20
  w-[200px] h-[200px]
  sm:w-[350px] sm:h-[350px]
  md:w-[500px] md:h-[500px]
  bg-gradient-to-r from-primary-500 to-emerald-500
  rounded-full blur-3xl opacity-20
"

// Always hide overflow on parent container
className="relative overflow-hidden"
```

### Images

```typescript
// Responsive image
className="w-full h-auto object-cover"

// Hero image
className="w-full h-[200px] sm:h-[300px] md:h-[400px] object-cover"

// Avatar
className="w-10 h-10 sm:w-12 sm:h-12 rounded-full"
```

### Cards

```typescript
// Card container
className="
  bg-white dark:bg-gray-800
  rounded-lg sm:rounded-xl
  p-4 sm:p-6
  shadow-sm hover:shadow-md
  transition-shadow
"

// Card with image
className="
  overflow-hidden
  rounded-lg sm:rounded-xl
"
```

## Touch Target Guidelines

**Minimum touch target: 44x44 pixels**

```typescript
// Interactive elements must be at least 44px
className="min-h-[44px] min-w-[44px]"

// Add padding to reach minimum
className="p-3"  // 12px padding on each side

// For inline links, add vertical padding
className="py-2 -my-2"  // Visual alignment preserved
```

## Safe Area (iPhone Notch)

```typescript
// Bottom navigation
className="pb-safe"  // Uses safe-area-inset-bottom

// Or with Tailwind config
className="pb-[env(safe-area-inset-bottom)]"

// Full safe area
className="p-safe"
```

## Dark Mode

```typescript
// Background
className="bg-white dark:bg-gray-900"

// Text
className="text-gray-900 dark:text-gray-100"

// Borders
className="border-gray-200 dark:border-gray-700"

// Hover states
className="hover:bg-gray-100 dark:hover:bg-gray-800"
```

## Overflow Prevention

```typescript
// Prevent horizontal scroll on page
<body className="overflow-x-hidden">

// Container with decorative elements
<div className="relative overflow-hidden">
  {/* Decorative blobs */}
</div>

// Text truncation
className="truncate"  // Single line
className="line-clamp-2"  // Multiple lines
```

## Testing Checklist

### Screen Sizes to Test
- [ ] 375px (iPhone SE)
- [ ] 390px (iPhone 14)
- [ ] 428px (iPhone 14 Pro Max)
- [ ] 768px (iPad)
- [ ] 1024px (iPad Pro / Laptop)
- [ ] 1280px (Desktop)
- [ ] 1920px+ (Large desktop)

### Visual Checks
- [ ] No horizontal scroll
- [ ] Text is readable
- [ ] Buttons are tappable (44px+)
- [ ] Modals don't overflow
- [ ] Images scale properly
- [ ] Navigation is accessible
- [ ] Forms are usable
- [ ] Cards stack properly

### Interaction Checks
- [ ] Touch targets are large enough
- [ ] Hover states work on desktop
- [ ] Focus states are visible
- [ ] Scroll is smooth
- [ ] Bottom nav doesn't cover content

## Common Issues & Fixes

### Issue: Horizontal overflow
```typescript
// Fix: Add overflow-hidden to container
className="overflow-hidden"

// Fix: Use max-width with calc
className="max-w-[calc(100vw-32px)]"

// Fix: Reduce decorative element sizes on mobile
className="w-[200px] sm:w-[400px]"
```

### Issue: Text too small on mobile
```typescript
// Fix: Start with readable size
className="text-sm sm:text-base"  // Not text-xs
```

### Issue: Touch targets too small
```typescript
// Fix: Add minimum size
className="min-h-[44px] min-w-[44px] p-3"
```

### Issue: Modal exceeds viewport
```typescript
// Fix: Use calc for max dimensions
className="max-w-[calc(100vw-32px)] max-h-[calc(100vh-32px)]"
```

### Issue: Content hidden behind bottom nav
```typescript
// Fix: Add padding to main content
className="pb-20"  // Height of bottom nav + spacing
```

## File References

Key responsive components:
- `frontend/src/components/layout/BottomNav.tsx`
- `frontend/src/components/layout/Header.tsx`
- `frontend/src/components/ui/Button.tsx`
- `frontend/src/components/ui/Modal.tsx`
- `frontend/src/pages/*.tsx` (all pages)
