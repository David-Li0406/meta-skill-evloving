# Design System Integration

## Overview

This project uses `@szum-tech/design-system`, a shadcn/ui-based design system that provides pre-styled components and design tokens.

## Setup

```css
/* app/globals.css */
@import "tailwindcss";
@import "@szum-tech/design-system/tailwind/global.css";
@source "../node_modules/@szum-tech/design-system";
```

The import order is important:
1. `tailwindcss` - Base Tailwind utilities
2. Design system CSS - Component styles and tokens
3. `@source` - Scan design system for class names

## Using Components

### Basic Import

```tsx
import { Button, Card, Input, Badge } from "@szum-tech/design-system";

export function MyComponent() {
  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Card Title</h2>
      <Input placeholder="Enter text..." className="mb-4" />
      <Button>Submit</Button>
    </Card>
  );
}
```

### Component Variants

Most components support variants via props:

```tsx
// Button variants
<Button variant="default">Default</Button>
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="destructive">Destructive</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>

// Button sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon"><Icon /></Button>
```

### Extending with className

Add custom styles using className prop:

```tsx
// Additional padding
<Card className="p-8">Extended padding</Card>

// Custom colors
<Badge className="bg-purple-500">Custom color</Badge>

// Responsive styles
<Button className="w-full md:w-auto">Responsive width</Button>

// Animation
<Card className="transition-shadow hover:shadow-lg">
  Hoverable card
</Card>
```

## Design Tokens

The design system provides CSS custom properties that can be used directly:

### Colors

```tsx
// Using design system colors
<div className="bg-background text-foreground">
  Using semantic colors
</div>

<div className="bg-muted text-muted-foreground">
  Muted content
</div>

<div className="border-border">
  Using border color token
</div>
```

### Radius

```tsx
// Using design system radius
<div className="rounded-radius">
  Uses --radius token
</div>
```

## Common Patterns

### Form Layout

```tsx
import { Button, Input, Label } from "@szum-tech/design-system";

function ContactForm() {
  return (
    <form className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="message">Message</Label>
        <Textarea
          id="message"
          placeholder="Your message..."
          className="min-h-[120px]"
        />
      </div>

      <Button type="submit" className="w-full">
        Send Message
      </Button>
    </form>
  );
}
```

### Card Grid

```tsx
import { Card } from "@szum-tech/design-system";

function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map(product => (
        <Card key={product.id} className="p-0 overflow-hidden">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-48 object-cover"
          />
          <div className="p-4">
            <h3 className="font-semibold text-lg">{product.name}</h3>
            <p className="text-muted-foreground mt-1">
              {product.description}
            </p>
            <p className="text-lg font-bold mt-4">
              ${product.price}
            </p>
          </div>
        </Card>
      ))}
    </div>
  );
}
```

### Navigation

```tsx
import { Button } from "@szum-tech/design-system";
import Link from "next/link";

function Navigation() {
  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b border-border">
      <Link href="/" className="text-xl font-bold">
        Logo
      </Link>

      <div className="flex items-center gap-4">
        <Link
          href="/features"
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          Features
        </Link>
        <Link
          href="/pricing"
          className="text-muted-foreground hover:text-foreground transition-colors"
        >
          Pricing
        </Link>
        <Button variant="outline" asChild>
          <Link href="/login">Log in</Link>
        </Button>
        <Button asChild>
          <Link href="/signup">Get Started</Link>
        </Button>
      </div>
    </nav>
  );
}
```

### Data Table

```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
  Badge,
} from "@szum-tech/design-system";

function UsersTable({ users }) {
  return (
    <div className="border border-border rounded-lg overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Email</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map(user => (
            <TableRow key={user.id}>
              <TableCell className="font-medium">{user.name}</TableCell>
              <TableCell>{user.email}</TableCell>
              <TableCell>
                <Badge variant={user.active ? "default" : "secondary"}>
                  {user.active ? "Active" : "Inactive"}
                </Badge>
              </TableCell>
              <TableCell className="text-right">
                <Button variant="ghost" size="sm">
                  Edit
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

## Customizing Components

### Wrapping Components

Create custom wrappers for project-specific variants:

```tsx
// components/ui/primary-button.tsx
import { Button, ButtonProps } from "@szum-tech/design-system";
import { cn } from "~/utils/cn";

interface PrimaryButtonProps extends ButtonProps {
  loading?: boolean;
}

export function PrimaryButton({
  children,
  loading,
  disabled,
  className,
  ...props
}: PrimaryButtonProps) {
  return (
    <Button
      variant="primary"
      disabled={disabled || loading}
      className={cn(
        "min-w-[120px]",
        loading && "cursor-wait",
        className
      )}
      {...props}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <Spinner className="h-4 w-4" />
          Loading...
        </span>
      ) : (
        children
      )}
    </Button>
  );
}
```

### Extending Styles

Use the `cn()` utility to merge class names:

```tsx
import { cn } from "~/utils/cn";
import { Card } from "@szum-tech/design-system";

interface CustomCardProps {
  variant?: "default" | "elevated" | "bordered";
  children: React.ReactNode;
  className?: string;
}

export function CustomCard({
  variant = "default",
  children,
  className
}: CustomCardProps) {
  return (
    <Card
      className={cn(
        // Base styles
        "p-6",
        // Variant styles
        {
          "shadow-none": variant === "default",
          "shadow-lg": variant === "elevated",
          "border-2 border-primary shadow-none": variant === "bordered",
        },
        // Additional className
        className
      )}
    >
      {children}
    </Card>
  );
}
```

## cn() Utility

The `cn()` function merges Tailwind classes intelligently:

```tsx
// utils/cn.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Usage:

```tsx
// Handles conflicts correctly
cn("px-4 py-2", "px-6")
// Result: "py-2 px-6" (not "px-4 py-2 px-6")

// Conditional classes
cn(
  "base-class",
  isActive && "active-class",
  { "conditional-class": condition }
)

// Merging with props
cn("default-styles", className)
```

## Dark Mode

Design system components automatically support dark mode:

```tsx
// Automatically adapts to color scheme
<Card>This card adapts to dark/light mode</Card>

// Force specific mode
<div className="dark">
  <Card>Always dark</Card>
</div>

<div className="light">
  <Card>Always light</Card>
</div>
```

## Accessibility

Design system components include accessibility features:

```tsx
// Buttons have proper focus states
<Button>Accessible by default</Button>

// Forms have proper labeling
<div>
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" />
</div>

// Dialogs trap focus
<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Modal Title</DialogTitle>
    </DialogHeader>
    <p>Modal content with proper focus management.</p>
  </DialogContent>
</Dialog>
```

## Documentation

For full component documentation, see:
[https://szum-tech-design-system.vercel.app/?path=/docs/components--docs](https://szum-tech-design-system.vercel.app/?path=/docs/components--docs)
