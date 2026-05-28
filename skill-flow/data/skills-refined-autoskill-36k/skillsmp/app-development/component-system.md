# Component System Skill

This skill provides comprehensive guidance for building UI components, implementing the design token system, and following styling patterns.

## Purpose

Use this skill when:
- Building new UI components
- Implementing design tokens and styling
- Understanding component hierarchy
- Working with Tailwind CSS v4
- Creating layouts and responsive designs
- Following component composition patterns

## Core Documentation

### Component Architecture

@components/component-system.md - Overall component system architecture
@components/core-components.md - Atomic building blocks
@components/composed-components.md - Composed component patterns
@components/domain-components.md - Business logic components
@components/layout-system.md - Layout patterns and grid systems

### Design System

@components/design-token-system.md - Token-first design system
@components/styling-patterns.md - CSS and Tailwind patterns
@token-tailwind-mapping.md - Complete token to Tailwind mapping reference

## Component Hierarchy

Components follow a strict four-tier hierarchy:

### 1. Core Components (`@core-components/*`)
**Atomic, reusable building blocks with no business logic**

Examples:
- `Button.tsx` - Base button component
- `Input.tsx` - Form input fields
- `Card.tsx` - Container component
- `Badge.tsx` - Status indicators

Characteristics:
- Accept design tokens via props
- Highly reusable
- No data fetching
- No business logic

### 2. Composed Components (`@components/composed/*`)
**Combinations of core components**

Examples:
- `SearchBar.tsx` - Input + Button + Icon
- `DataCard.tsx` - Card + Badge + Button
- `FormGroup.tsx` - Label + Input + ErrorMessage

Characteristics:
- Compose multiple core components
- May have internal state
- No API calls
- Reusable across domains

### 3. Domain Components (`@components/domain/*`)
**Business logic and data-aware components**

Examples:
- `StudentCard.tsx` - Shows student data
- `RoadmapProgress.tsx` - Displays progress tracking
- `IncentiveTracker.tsx` - Tracks student incentives

Characteristics:
- Connected to business logic
- May use React Query hooks
- Domain-specific
- Uses composed/core components

### 4. Feature Components (`@app/*/components/*`)
**Complete feature implementations**

Examples:
- `StudentDashboard.tsx`
- `IncentivesManagementPage.tsx`
- `RoadmapsEditor.tsx`

Characteristics:
- Page-level components
- Orchestrate multiple domain components
- Handle routing and navigation
- Feature-complete implementations

## Design Token System

### Token-First Approach

All styling uses design tokens (semantic Tailwind classes):

```typescript
// DON'T use raw Tailwind classes in components
<button className="bg-blue-600 hover:bg-blue-700 text-white">
  Click me
</button>

// DO use design tokens
import { buttonVariants } from "@/lib/ui/tokens/button-tokens";

<button className={buttonVariants.primary}>
  Click me
</button>
```

### Token Categories

Located in `src/lib/ui/tokens/`:

1. **Color Tokens** - `text-*`, `bg-*`, `border-*`
2. **Spacing Tokens** - `p-*`, `m-*`, `gap-*`
3. **Typography Tokens** - `text-sm`, `font-*`
4. **Component Tokens** - Button, Card, Input variants

### Using Tokens

```typescript
// Import tokens
import { textColors } from "@/lib/ui/tokens/text-tokens";
import { spacing } from "@/lib/ui/tokens/spacing-tokens";

// Use in components
<div className={`${textColors.primary} ${spacing.padding.md}`}>
  Content
</div>
```

## Styling Patterns

### Tailwind CSS v4

This project uses Tailwind CSS v4 with:
- CSS-first configuration
- Design tokens in CSS variables
- Optimized builds
- Dark mode support

### Component Styling Pattern

```typescript
import { cn } from "@/lib/utils";

interface ComponentProps {
  variant?: "primary" | "secondary";
  className?: string;
}

export function Component({ variant = "primary", className }: ComponentProps) {
  return (
    <div className={cn(
      // Base styles
      "rounded-lg border p-4",
      // Variant styles
      variant === "primary" && "bg-blue-600 text-white",
      variant === "secondary" && "bg-gray-200 text-gray-900",
      // Custom overrides
      className
    )}>
      Content
    </div>
  );
}
```

### Responsive Design

Use Tailwind breakpoints:

```typescript
<div className="
  grid
  grid-cols-1      // Mobile
  md:grid-cols-2   // Tablet
  lg:grid-cols-3   // Desktop
  gap-4
">
  {/* Content */}
</div>
```

### Dark Mode

```typescript
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-gray-100
">
  Content
</div>
```

## Layout System

### Container Pattern

```typescript
<div className="container mx-auto px-4 py-8">
  {/* Page content */}
</div>
```

### Grid Layouts

```typescript
// Equal columns
<div className="grid grid-cols-3 gap-4">
  <div>Col 1</div>
  <div>Col 2</div>
  <div>Col 3</div>
</div>

// Sidebar layout
<div className="grid grid-cols-[250px_1fr] gap-6">
  <aside>Sidebar</aside>
  <main>Main content</main>
</div>
```

### Flexbox Layouts

```typescript
// Horizontal centering
<div className="flex justify-center items-center">
  Content
</div>

// Space between
<div className="flex justify-between items-center">
  <div>Left</div>
  <div>Right</div>
</div>
```

## Common Component Patterns

### Form Input Pattern

```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, className, ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-2">
      {label && <label className="text-sm font-medium">{label}</label>}
      <input
        className={cn(
          "border rounded-md px-3 py-2",
          error && "border-red-500",
          className
        )}
        {...props}
      />
      {error && <span className="text-sm text-red-500">{error}</span>}
    </div>
  );
}
```

### Card Pattern

```typescript
interface CardProps {
  title?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export function Card({ title, children, footer }: CardProps) {
  return (
    <div className="border rounded-lg overflow-hidden">
      {title && (
        <div className="border-b px-4 py-3 bg-gray-50">
          <h3 className="font-semibold">{title}</h3>
        </div>
      )}
      <div className="p-4">
        {children}
      </div>
      {footer && (
        <div className="border-t px-4 py-3 bg-gray-50">
          {footer}
        </div>
      )}
    </div>
  );
}
```

### Button Pattern

```typescript
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        "rounded-md font-medium transition-colors",
        // Size variants
        size === "sm" && "px-3 py-1.5 text-sm",
        size === "md" && "px-4 py-2",
        size === "lg" && "px-6 py-3 text-lg",
        // Color variants
        variant === "primary" && "bg-blue-600 hover:bg-blue-700 text-white",
        variant === "secondary" && "bg-gray-200 hover:bg-gray-300 text-gray-900",
        variant === "danger" && "bg-red-600 hover:bg-red-700 text-white",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

## Best Practices

### Component Guidelines

1. **Single Responsibility** - Each component should do one thing well
2. **Composition over Inheritance** - Build complex UIs from simple components
3. **Props over Context** - Prefer explicit props for clarity
4. **TypeScript** - Always type props and use interfaces
5. **Accessibility** - Use semantic HTML and ARIA attributes

### Performance

1. **React.memo** - Memoize expensive components
2. **Lazy Loading** - Use `React.lazy()` for code splitting
3. **Avoid Inline Functions** - Define callbacks outside render
4. **Keys in Lists** - Always use stable, unique keys

### Testing Considerations

1. **Data Testids** - Add `data-testid` for integration tests
2. **Pure Components** - Keep components testable (minimize side effects)
3. **Props Validation** - Type props properly for better errors

## File Organization

```
src/components/
├── core/                 # Atomic components
│   ├── Button.tsx
│   ├── Input.tsx
│   └── Card.tsx
├── composed/             # Composed components
│   ├── SearchBar.tsx
│   └── DataCard.tsx
├── domain/              # Domain components
│   ├── students/
│   │   └── StudentCard.tsx
│   └── roadmaps/
│       └── RoadmapProgress.tsx
└── ui/                  # shadcn/ui components
    ├── button.tsx
    └── dialog.tsx
```

## Integration with Other Skills

- For overall architecture → Use `architecture` skill
- For data fetching and state → Use `data-flow` skill
- For table components → Use `tanstack-table` skill
- For implementation workflows → Use `workflows` skill
