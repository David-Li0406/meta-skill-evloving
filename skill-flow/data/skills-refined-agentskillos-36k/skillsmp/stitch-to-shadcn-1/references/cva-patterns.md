# CVA (Class Variance Authority) Patterns

Reference for implementing type-safe component variants.

## Table of Contents
- [Setup](#setup)
- [Basic Pattern](#basic-pattern)
- [Compound Variants](#compound-variants)
- [Size Variants](#size-variants)
- [State Variants](#state-variants)
- [Composing Variants](#composing-variants)

---

## Setup

Required dependencies:
```bash
npm install class-variance-authority clsx tailwind-merge
```

Create cn() utility at `@/lib/utils.ts`:
```typescript
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## Basic Pattern

```typescript
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"
import * as React from "react"

// 1. Define variants with cva()
const componentVariants = cva(
  // Base styles (always applied)
  "base-classes-here",
  {
    variants: {
      // Each variant category
      variant: {
        default: "variant-default-classes",
        secondary: "variant-secondary-classes",
      },
      size: {
        sm: "size-sm-classes",
        md: "size-md-classes",
        lg: "size-lg-classes",
      },
    },
    // Always set defaults
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

// 2. Define props interface extending VariantProps
export interface ComponentProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {
  // Additional custom props here
}

// 3. Create component with forwardRef
const Component = React.forwardRef<HTMLDivElement, ComponentProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(componentVariants({ variant, size, className }))}
        {...props}
      />
    )
  }
)
Component.displayName = "Component"

// 4. Export both component and variants
export { Component, componentVariants }
```

---

## Compound Variants

Use when variant combinations need special styling:

```typescript
const alertVariants = cva(
  "relative w-full rounded-lg border p-4",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive: "border-destructive/50 text-destructive",
        success: "border-green-500/50 text-green-700",
        warning: "border-yellow-500/50 text-yellow-700",
      },
      size: {
        sm: "p-2 text-sm",
        md: "p-4",
        lg: "p-6 text-lg",
      },
    },
    // Special styles for specific combinations
    compoundVariants: [
      {
        variant: "destructive",
        size: "lg",
        className: "border-2 font-semibold", // Extra emphasis for large destructive
      },
      {
        variant: ["success", "warning"],
        size: "sm",
        className: "rounded-md", // Smaller radius for compact success/warning
      },
    ],
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)
```

---

## Size Variants

Common size scale pattern:

```typescript
const sizeVariants = cva("", {
  variants: {
    size: {
      xs: "h-6 px-2 text-xs",
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
      xl: "h-14 px-8 text-lg",
    },
  },
  defaultVariants: {
    size: "md",
  },
})
```

Icon button sizes:
```typescript
const iconButtonVariants = cva(
  "inline-flex items-center justify-center rounded-md",
  {
    variants: {
      size: {
        sm: "h-8 w-8",
        md: "h-10 w-10",
        lg: "h-12 w-12",
      },
    },
    defaultVariants: {
      size: "md",
    },
  }
)
```

---

## State Variants

Handle interactive states:

```typescript
const inputVariants = cva(
  "flex w-full rounded-md border bg-background px-3 py-2 text-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      state: {
        default: "border-input",
        error: "border-destructive focus-visible:ring-destructive",
        success: "border-green-500 focus-visible:ring-green-500",
      },
    },
    defaultVariants: {
      state: "default",
    },
  }
)
```

Loading state pattern:
```typescript
const buttonVariants = cva(
  "inline-flex items-center justify-center",
  {
    variants: {
      isLoading: {
        true: "cursor-wait opacity-70",
        false: "",
      },
    },
    defaultVariants: {
      isLoading: false,
    },
  }
)
```

---

## Composing Variants

### Extending Base Variants

```typescript
// Base button variants
const baseButtonVariants = cva("inline-flex items-center justify-center rounded-md font-medium", {
  variants: {
    size: {
      sm: "h-9 px-3",
      md: "h-10 px-4",
      lg: "h-11 px-8",
    },
  },
  defaultVariants: {
    size: "md",
  },
})

// Extended with color variants
const colorButtonVariants = cva("", {
  variants: {
    color: {
      primary: "bg-primary text-primary-foreground hover:bg-primary/90",
      secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
      accent: "bg-accent text-accent-foreground hover:bg-accent/80",
    },
  },
  defaultVariants: {
    color: "primary",
  },
})

// Combine in component
const Button = ({ className, size, color, ...props }) => (
  <button
    className={cn(
      baseButtonVariants({ size }),
      colorButtonVariants({ color }),
      className
    )}
    {...props}
  />
)
```

### Slot-Based Variants (for compound components)

```typescript
const cardVariants = cva("rounded-lg border bg-card text-card-foreground", {
  variants: {
    variant: {
      default: "shadow-sm",
      elevated: "shadow-lg",
      outlined: "shadow-none",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})

const cardHeaderVariants = cva("flex flex-col space-y-1.5 p-6", {
  variants: {
    variant: {
      default: "",
      compact: "p-4 space-y-1",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})

const cardContentVariants = cva("p-6 pt-0", {
  variants: {
    variant: {
      default: "",
      compact: "p-4 pt-0",
    },
  },
  defaultVariants: {
    variant: "default",
  },
})
```

---

## Type Export Pattern

Always export variant types for consumers:

```typescript
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(/* ... */)

// Export the variant props type
export type ButtonVariants = VariantProps<typeof buttonVariants>

// Use in interface
export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    ButtonVariants {
  asChild?: boolean
}

// Consumer can now type-check variants:
// const variant: ButtonVariants["variant"] = "default"
```

---

## Anti-Patterns to Avoid

### DON'T: Inline variant logic
```typescript
// BAD
const Button = ({ variant }) => (
  <button className={variant === "primary" ? "bg-blue-500" : "bg-gray-500"} />
)
```

### DON'T: Skip defaultVariants
```typescript
// BAD - missing defaults
const variants = cva("base", {
  variants: { size: { sm: "...", lg: "..." } }
  // No defaultVariants!
})
```

### DON'T: Mix CVA with manual className conditionals
```typescript
// BAD - inconsistent approach
const Component = ({ variant, isActive, className }) => (
  <div
    className={cn(
      variants({ variant }),
      isActive && "border-2", // Should be in CVA
      className
    )}
  />
)
```

### DO: Keep all variant logic in CVA
```typescript
// GOOD
const variants = cva("base", {
  variants: {
    variant: { /* ... */ },
    isActive: {
      true: "border-2",
      false: "",
    },
  },
  defaultVariants: {
    variant: "default",
    isActive: false,
  },
})
```
