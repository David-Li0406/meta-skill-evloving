/**
 * Component Scaffold Template
 *
 * Base template for creating shadcn-style components with:
 * - TypeScript support
 * - Variant support via class-variance-authority (cva)
 * - Proper forwardRef pattern
 * - Accessibility considerations
 *
 * Usage:
 * 1. Copy this template
 * 2. Rename ComponentName and update displayName
 * 3. Customize variants and default styles
 * 4. Add ARIA attributes as needed
 */

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

// ==========================================
// VARIANT DEFINITIONS
// ==========================================

const componentVariants = cva(
  // Base styles (always applied)
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      // Visual variants
      variant: {
        default:
          "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline:
          "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      // Size variants
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    // Compound variants (combinations)
    compoundVariants: [
      {
        variant: "outline",
        size: "sm",
        className: "border-2",
      },
    ],
    // Default values
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

// ==========================================
// TYPE DEFINITIONS
// ==========================================

export interface ComponentNameProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof componentVariants> {
  /** Optional: Make component behave as a different element */
  asChild?: boolean;
  /** Optional: Loading state */
  loading?: boolean;
  /** Optional: Disabled state */
  disabled?: boolean;
}

// ==========================================
// COMPONENT IMPLEMENTATION
// ==========================================

const ComponentName = React.forwardRef<HTMLDivElement, ComponentNameProps>(
  (
    {
      className,
      variant,
      size,
      asChild = false,
      loading = false,
      disabled = false,
      children,
      ...props
    },
    ref
  ) => {
    // If using Radix Slot pattern for asChild
    // import { Slot } from "@radix-ui/react-slot";
    // const Comp = asChild ? Slot : "div";

    return (
      <div
        ref={ref}
        className={cn(componentVariants({ variant, size, className }))}
        aria-disabled={disabled || loading}
        data-loading={loading}
        {...props}
      >
        {loading ? (
          <>
            {/* Loading spinner */}
            <svg
              className="mr-2 h-4 w-4 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            <span>Loading...</span>
          </>
        ) : (
          children
        )}
      </div>
    );
  }
);

ComponentName.displayName = "ComponentName";

export { ComponentName, componentVariants };

// ==========================================
// USAGE EXAMPLES
// ==========================================

/**
 * Basic usage:
 * ```tsx
 * import { ComponentName } from "@/components/ui/component-name";
 *
 * <ComponentName>Default</ComponentName>
 * <ComponentName variant="destructive">Destructive</ComponentName>
 * <ComponentName variant="outline" size="sm">Small Outline</ComponentName>
 * <ComponentName loading>Loading...</ComponentName>
 * ```
 *
 * With custom classes:
 * ```tsx
 * <ComponentName className="custom-class">Custom</ComponentName>
 * ```
 *
 * As a different element (with Radix Slot):
 * ```tsx
 * <ComponentName asChild>
 *   <a href="/link">Link Component</a>
 * </ComponentName>
 * ```
 */

// ==========================================
// ALTERNATIVE: BUTTON COMPONENT EXAMPLE
// ==========================================

/*
import { Slot } from "@radix-ui/react-slot";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };
*/

// ==========================================
// ALTERNATIVE: CARD COMPONENT EXAMPLE
// ==========================================

/*
const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-xl border bg-card text-card-foreground shadow",
      className
    )}
    {...props}
  />
));
Card.displayName = "Card";

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn("font-semibold leading-none tracking-tight", className)}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
));
CardContent.displayName = "CardContent";

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
*/
