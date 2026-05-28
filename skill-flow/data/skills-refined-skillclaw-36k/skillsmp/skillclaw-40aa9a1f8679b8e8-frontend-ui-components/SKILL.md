---
name: frontend-ui-components
description: Use this skill when implementing UI features using Shadcn/Radix components and the shared @eridu/ui package.
---

# Frontend UI Components

This skill outlines how to build and use UI components in frontend applications, leveraging the shared `@eridu/ui` package and Shadcn patterns.

## The `@eridu/ui` Package

All generic UI components (Buttons, Inputs, Dialogs, etc.) live in `packages/ui`. Do NOT create local copies of generic components in apps.

### Usage

```typescript
import { Button } from '@eridu/ui/components/button';
import { Input } from '@eridu/ui/components/input';

export function MyForm() {
  return (
    <div className="flex gap-4">
      <Input placeholder="Search..." />
      <Button variant="default">Search</Button>
    </div>
  );
}
```

## Styling Pattern (Tailwind CSS v4)

We use **Tailwind CSS v4** with `clsx` and `tailwind-merge` for conditional styling.

### The `cn` Utility

Use the `cn` utility from `@eridu/ui/lib/utils` to merge classes safely.

```typescript
import { cn } from '@eridu/ui/lib/utils';

interface CardProps {
  className?: string;
  children: React.ReactNode;
}

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)}>
      {children}
    </div>
  );
}
```

## Creating New Components

When creating **app-specific** features:
1. Compose them using primitives from `@eridu/ui`.
2. Keep them in `src/components/{feature-name}/`.

When creating **new generic** primitives:
1. Add them to `packages/ui/src/components/`.
2. Follow the Radix UI + Tailwind pattern (Shadcn style).
3. Export them via `packages/ui/package.json`.

## Component Design Patterns

### Composition Over Large Components

Build complex UIs by composing small, focused components instead of creating large monolithic components.

**Benefits**:
- Easier to test and maintain
- Better performance (smaller re-render scope)
- More reusable components
- Clearer separation of concerns

```typescript
// ❌ BAD: Large monolithic component
function UserDashboard() {
  return (
    <div>
      <header>{/* Complex header logic */}</header>
      <nav>{/* Complex navigation */}</nav>
      <main>
        <div>{/* User stats */}</div>
        <div>{/* Activity feed */}</div>
        <div>{/* Recommendations */}</div>
      </main>
      <footer>{/* Footer content */}</footer>
    </div>
  );
}

// ✅ GOOD: Composed from smaller components
function UserDashboard() {
  return (
    <div>
      <DashboardHeader />
      <DashboardNav />
      <main>
        <UserStats />
        <ActivityFeed />
        <Recommendations />
      </main>
      <DashboardFooter />
    </div>
  );
}
```

## Checklist

- [ ] Import generic components from `@eridu/ui`.
- [ ] Use `cn()` for class merging.
- [ ] Ensure components are accessible (Radix UI primitives).
- [ ] Use Tailwind text/bg colors that map to the theme (e.g., `bg-primary`, `text-muted-foreground`).