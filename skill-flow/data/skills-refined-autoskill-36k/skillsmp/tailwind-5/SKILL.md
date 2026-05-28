---
name: tailwind
description: >
  Tailwind CSS patterns and MiGestion design system.
  Trigger: When styling components with Tailwind CSS.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [web]
  auto_invoke: 'Working with Tailwind CSS'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## cn Utility (REQUIRED)

Use `cn()` for conditional class merging.

```typescript
import { cn } from '@/lib/utils';

// ✅ ALWAYS: Use cn() for conditional classes
className={cn(
  'base-classes',
  isActive && 'active-classes',
  'more-classes'
)}

// ❌ NEVER: Template literals for conditional classes
className={`base-classes ${isActive ? 'active-classes' : ''} more-classes`}
```

## MiGestion Design System

**Color Palette:** Neutral scale (white, black, grays)

```css
/* ✅ ALWAYS: Neutral colors */
bg-white text-neutral-900        /* Primary action */
bg-neutral-100 text-neutral-900 /* Secondary */
bg-neutral-900 text-white       /* Inverted */

/* ❌ NEVER: No gradients */
bg-gradient-to-r from-blue-500 to-purple-500
```

**Border-based Design:** No heavy shadows

```css
/* ✅ ALWAYS: Border-based */
border border-neutral-200 rounded

/* ❌ NEVER: Heavy shadows */
shadow-lg shadow-xl
```

## Typography

```css
text-sm text-base text-lg text-xl text-2xl text-3xl
font-normal font-medium font-semibold font-bold
text-neutral-600 text-neutral-900
leading-tight leading-normal leading-relaxed
```

## Spacing

```css
p-0 p-1 p-2 p-3 p-4 p-6 p-8
px-2 py-1
gap-2 gap-4 gap-6 gap-8
m-0 m-2 m-4 m-6 m-8
mx-auto my-auto
```

## Flexbox

```css
flex flex-row flex-col
justify-start justify-center justify-end justify-between
items-start items-center items-end
gap-2 gap-4
flex-1
```

## Grid

```css
grid grid-cols-1 grid-cols-2 grid-cols-3 grid-cols-4
gap-4
```

## Button Styles

```css
/* Primary */
bg-neutral-900 text-white hover:bg-neutral-800 focus-visible:ring-2

/* Secondary */
bg-white border border-neutral-300 hover:bg-neutral-50

/* Ghost */
bg-transparent text-neutral-600 hover:bg-neutral-100

/* Danger */
bg-red-600 text-white hover:bg-red-700
```

## Input Styles

```css
border border-neutral-300 rounded px-3 py-2
focus:outline-none focus:ring-2 focus:border-transparent
placeholder:text-neutral-400
```

## Responsive

```css
/* Mobile first, add larger breakpoints */
w-full md:w-auto
text-sm md:text-base
flex-col md:flex-row
hidden md:block
```

## Animation

```css
transition-colors duration-150
ease-in ease-out ease-in-out
```

## State

```css
/* Disabled */
disabled:opacity-50 disabled:cursor-not-allowed

/* Hover */
hover:bg-neutral-100

/* Focus */
focus:outline-none focus-visible:ring-2

/* Active */
active:bg-neutral-200
```

## Custom Components

```typescript
// ✅ Component with variants
const buttonVariants = {
  primary: 'bg-neutral-900 text-white hover:bg-neutral-800',
  secondary: 'bg-white border border-neutral-300 hover:bg-neutral-50',
  ghost: 'text-neutral-600 hover:bg-neutral-100',
};

export const Button = ({ variant = 'primary', className, ...props }) => {
  return (
    <button className={cn('base-styles', buttonVariants[variant], className)} {...props} />
  );
};
```

## Commands

```bash
npm run dev:web              # Tailwind runs in dev mode (JIT)
npm run build:web            # CSS is purged in production build
```

## Related Skills

- `migestion-web` - MiGestion Web component patterns
- `react-18` - React component patterns
