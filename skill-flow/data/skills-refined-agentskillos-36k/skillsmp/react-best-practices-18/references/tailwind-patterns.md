# Tailwind CSS Patterns

Best practices for styling React components with Tailwind CSS.

## Table of Contents

1. [Class Organization](#class-organization)
2. [Responsive Design](#responsive-design)
3. [Dark Mode](#dark-mode)
4. [Conditional Classes](#conditional-classes)
5. [Common Pitfalls](#common-pitfalls)
6. [Component Patterns](#component-patterns)

---

## Class Organization

Order classes logically for readability:

```
Layout → Flexbox/Grid → Spacing → Sizing → Typography → Colors → Effects → States
```

```javascript
// Good - organized order
<div className="
  flex flex-col items-center justify-between
  gap-4 p-6 mx-auto
  w-full max-w-lg h-auto
  text-base font-medium
  bg-white text-gray-900
  rounded-lg shadow-md
  hover:shadow-lg transition-shadow
">
```

### Grouping Example

```javascript
const Card = ( { children } ) => (
  <div
    className={
      // Layout
      'flex flex-col ' +
      // Spacing
      'p-6 gap-4 ' +
      // Sizing
      'w-full max-w-md ' +
      // Typography
      'text-sm ' +
      // Colors
      'bg-white dark:bg-gray-800 ' +
      // Effects
      'rounded-xl shadow-lg ' +
      // Transitions
      'transition-all duration-200 ' +
      // States
      'hover:shadow-xl'
    }
  >
    { children }
  </div>
);
```

---

## Responsive Design

Mobile-first approach - base styles for mobile, add breakpoints for larger screens.

### Breakpoints

| Prefix | Min Width | Usage |
|--------|-----------|-------|
| (none) | 0px | Mobile (default) |
| `sm:` | 640px | Large phones |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Laptops |
| `xl:` | 1280px | Desktops |
| `2xl:` | 1536px | Large screens |

### Responsive Layout

```javascript
const Grid = ( { items } ) => (
  <div className="
    grid
    grid-cols-1
    sm:grid-cols-2
    lg:grid-cols-3
    xl:grid-cols-4
    gap-4 sm:gap-6 lg:gap-8
  ">
    { items.map( ( item ) => <Card key={ item.id } { ...item } /> ) }
  </div>
);
```

### Responsive Typography

```javascript
const Heading = ( { children } ) => (
  <h1 className="
    text-2xl sm:text-3xl lg:text-4xl xl:text-5xl
    font-bold
    leading-tight
  ">
    { children }
  </h1>
);
```

### Responsive Visibility

```javascript
// Mobile menu button - hidden on desktop
<button className="block lg:hidden">Menu</button>

// Desktop nav - hidden on mobile
<nav className="hidden lg:flex">...</nav>
```

---

## Dark Mode

Use `dark:` prefix consistently. Configure in `tailwind.config.js`:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  // ...
};
```

### Dark Mode Patterns

```javascript
const Component = () => (
  <div className="
    bg-white dark:bg-gray-900
    text-gray-900 dark:text-gray-100
    border-gray-200 dark:border-gray-700
  ">
    <h2 className="text-gray-800 dark:text-gray-200">Title</h2>
    <p className="text-gray-600 dark:text-gray-400">Description</p>
  </div>
);
```

### Consistent Color Pairs

| Light | Dark | Usage |
|-------|------|-------|
| `bg-white` | `dark:bg-gray-900` | Page background |
| `bg-gray-50` | `dark:bg-gray-800` | Card/section background |
| `bg-gray-100` | `dark:bg-gray-700` | Hover states |
| `text-gray-900` | `dark:text-gray-100` | Primary text |
| `text-gray-600` | `dark:text-gray-400` | Secondary text |
| `border-gray-200` | `dark:border-gray-700` | Borders |

---

## Conditional Classes

Use the `classnames` (or `clsx`) utility for conditional classes.

### Basic Conditionals

```javascript
import classNames from 'classnames';

const Button = ( { variant, disabled, children } ) => (
  <button
    disabled={ disabled }
    className={ classNames(
      // Base styles
      'px-4 py-2 rounded-lg font-medium transition-colors',
      // Variant styles
      {
        'bg-blue-600 text-white hover:bg-blue-700': variant === 'primary',
        'bg-gray-200 text-gray-800 hover:bg-gray-300': variant === 'secondary',
        'bg-transparent border border-gray-300 hover:bg-gray-50': variant === 'outline',
      },
      // Disabled state
      {
        'opacity-50 cursor-not-allowed': disabled,
      }
    ) }
  >
    { children }
  </button>
);
```

### Array Syntax

```javascript
const Alert = ( { type, children } ) => (
  <div
    className={ classNames( [
      'p-4 rounded-lg border',
      type === 'error' && 'bg-red-50 border-red-200 text-red-800',
      type === 'success' && 'bg-green-50 border-green-200 text-green-800',
      type === 'warning' && 'bg-yellow-50 border-yellow-200 text-yellow-800',
      type === 'info' && 'bg-blue-50 border-blue-200 text-blue-800',
    ] ) }
  >
    { children }
  </div>
);
```

---

## Common Pitfalls

### Never Concatenate Class Names Dynamically

```javascript
// Bad - Tailwind can't purge these
const color = 'red';
<div className={ `bg-${color}-500` } />

// Bad - variable interpolation
<div className={ `text-${size}` } />

// Good - use complete class names
const colorClasses = {
  red: 'bg-red-500',
  blue: 'bg-blue-500',
  green: 'bg-green-500',
};
<div className={ colorClasses[ color ] } />

// Good - conditional object
<div className={ classNames( {
  'text-sm': size === 'small',
  'text-base': size === 'medium',
  'text-lg': size === 'large',
} ) } />
```

### Avoid Arbitrary Values

```javascript
// Bad - arbitrary values bloat CSS
<div className="w-[347px] mt-[13px] text-[15px]" />

// Good - use closest standard value
<div className="w-80 mt-3 text-sm" />

// If custom value needed, define in config
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        '18': '4.5rem',
      },
    },
  },
};
```

### Don't Mix Styling Approaches

```javascript
// Bad - mixing inline styles with Tailwind
<div className="p-4" style={ { marginTop: '10px' } } />

// Good - all Tailwind
<div className="p-4 mt-2.5" />
```

---

## Component Patterns

### Reusable Style Objects

```javascript
const buttonStyles = {
  base: 'px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2',
  variants: {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  },
  sizes: {
    sm: 'text-sm px-3 py-1.5',
    md: 'text-base px-4 py-2',
    lg: 'text-lg px-6 py-3',
  },
};

const Button = ( { variant = 'primary', size = 'md', children, ...props } ) => (
  <button
    className={ classNames(
      buttonStyles.base,
      buttonStyles.variants[ variant ],
      buttonStyles.sizes[ size ]
    ) }
    { ...props }
  >
    { children }
  </button>
);
```

### Input Components

```javascript
const inputBase = 'w-full px-3 py-2 border rounded-lg transition-colors focus:outline-none focus:ring-2';

const Input = ( { error, ...props } ) => (
  <input
    className={ classNames(
      inputBase,
      error
        ? 'border-red-500 focus:border-red-500 focus:ring-red-200'
        : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200',
      'dark:bg-gray-800 dark:border-gray-600 dark:text-gray-100'
    ) }
    { ...props }
  />
);
```

### Card Components

```javascript
const Card = ( { hoverable, children } ) => (
  <div
    className={ classNames(
      'bg-white dark:bg-gray-800',
      'rounded-xl shadow-md',
      'p-6',
      hoverable && 'hover:shadow-lg transition-shadow cursor-pointer'
    ) }
  >
    { children }
  </div>
);

const CardHeader = ( { children } ) => (
  <div className="border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
    { children }
  </div>
);

const CardTitle = ( { children } ) => (
  <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
    { children }
  </h3>
);
```
