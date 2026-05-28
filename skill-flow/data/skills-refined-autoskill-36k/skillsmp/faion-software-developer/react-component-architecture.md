---
id: react-component-architecture
name: "React Component Architecture"
domain: DEV
skill: faion-software-developer
category: "development"
---

# React Component Architecture

## Overview

React component architecture defines how to structure, organize, and compose components for maintainable, scalable applications. This methodology covers component patterns, file organization, composition strategies, and best practices for modern React development.

## When to Use

- Starting new React/Next.js projects
- Organizing large component libraries
- Establishing team coding standards
- Refactoring component structure
- Building design systems

## Key Principles

1. **Single responsibility** - Each component does one thing well
2. **Composition over inheritance** - Build complex UIs from simple parts
3. **Colocation** - Keep related files together
4. **Prop drilling avoidance** - Use context/state management appropriately
5. **Separation of concerns** - UI, logic, and data fetching separated

## Best Practices

### Directory Structure

```
src/
├── components/              # Shared/reusable components
│   ├── ui/                 # Base UI primitives
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   └── Card/
│   │
│   ├── forms/              # Form components
│   │   ├── TextField/
│   │   ├── Select/
│   │   └── FormField/
│   │
│   └── layout/             # Layout components
│       ├── Header/
│       ├── Footer/
│       └── Sidebar/
│
├── features/               # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── hooks/
│   │   │   └── useAuth.ts
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── index.ts
│   │
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       └── index.ts
│
├── hooks/                  # Shared custom hooks
├── utils/                  # Pure utility functions
├── types/                  # Shared TypeScript types
├── lib/                    # Third-party wrappers
└── app/                    # Next.js app router / pages
```

### Component File Structure

```
Button/
├── Button.tsx              # Main component
├── Button.test.tsx         # Tests
├── Button.stories.tsx      # Storybook stories
├── Button.module.css       # Styles (if CSS Modules)
├── types.ts                # Component-specific types
└── index.ts                # Public exports
```

### Functional Component Pattern

```tsx
// Button/Button.tsx
import { forwardRef, type ComponentPropsWithoutRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends ComponentPropsWithoutRef<'button'>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <Spinner className="mr-2 h-4 w-4 animate-spin" />
            Loading...
          </>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

### Compound Component Pattern

```tsx
// Card/Card.tsx
import { createContext, useContext, type ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface CardContextValue {
  variant: 'default' | 'outlined';
}

const CardContext = createContext<CardContextValue | null>(null);

function useCardContext() {
  const context = useContext(CardContext);
  if (!context) {
    throw new Error('Card components must be used within Card');
  }
  return context;
}

interface CardProps {
  variant?: 'default' | 'outlined';
  className?: string;
  children: ReactNode;
}

function Card({ variant = 'default', className, children }: CardProps) {
  return (
    <CardContext.Provider value={{ variant }}>
      <div
        className={cn(
          'rounded-lg bg-card text-card-foreground',
          variant === 'outlined' && 'border',
          variant === 'default' && 'shadow-sm',
          className
        )}
      >
        {children}
      </div>
    </CardContext.Provider>
  );
}

function CardHeader({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <div className={cn('flex flex-col space-y-1.5 p-6', className)}>
      {children}
    </div>
  );
}

function CardTitle({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <h3 className={cn('text-2xl font-semibold leading-none tracking-tight', className)}>
      {children}
    </h3>
  );
}

function CardContent({ className, children }: { className?: string; children: ReactNode }) {
  return <div className={cn('p-6 pt-0', className)}>{children}</div>;
}

function CardFooter({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <div className={cn('flex items-center p-6 pt-0', className)}>
      {children}
    </div>
  );
}

// Export compound component
Card.Header = CardHeader;
Card.Title = CardTitle;
Card.Content = CardContent;
Card.Footer = CardFooter;

export { Card };
```

### Usage of Compound Component

```tsx
// Usage
<Card variant="outlined">
  <Card.Header>
    <Card.Title>Account Settings</Card.Title>
  </Card.Header>
  <Card.Content>
    <p>Manage your account preferences here.</p>
  </Card.Content>
  <Card.Footer>
    <Button>Save Changes</Button>
  </Card.Footer>
</Card>
```

### Container/Presenter Pattern

```tsx
// UserList/UserListContainer.tsx (Logic)
import { useUsers } from '@/features/users/hooks/useUsers';
import { UserList } from './UserList';

export function UserListContainer() {
  const { users, isLoading, error, refetch } = useUsers();

  if (isLoading) return <UserListSkeleton />;
  if (error) return <ErrorMessage error={error} onRetry={refetch} />;

  return <UserList users={users} />;
}

// UserList/UserList.tsx (Presentation)
interface UserListProps {
  users: User[];
}

export function UserList({ users }: UserListProps) {
  if (users.length === 0) {
    return <EmptyState message="No users found" />;
  }

  return (
    <ul className="space-y-4">
      {users.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </ul>
  );
}
```

### Render Props Pattern

```tsx
// components/Toggle.tsx
import { useState, type ReactNode } from 'react';

interface ToggleProps {
  initialState?: boolean;
  children: (props: {
    isOn: boolean;
    toggle: () => void;
    setOn: () => void;
    setOff: () => void;
  }) => ReactNode;
}

export function Toggle({ initialState = false, children }: ToggleProps) {
  const [isOn, setIsOn] = useState(initialState);

  const toggle = () => setIsOn((prev) => !prev);
  const setOn = () => setIsOn(true);
  const setOff = () => setIsOn(false);

  return <>{children({ isOn, toggle, setOn, setOff })}</>;
}

// Usage
<Toggle>
  {({ isOn, toggle }) => (
    <button onClick={toggle}>
      {isOn ? 'ON' : 'OFF'}
    </button>
  )}
</Toggle>
```

### Polymorphic Component

```tsx
// components/Box.tsx
import { type ElementType, type ComponentPropsWithoutRef } from 'react';

type BoxProps<T extends ElementType> = {
  as?: T;
  className?: string;
} & ComponentPropsWithoutRef<T>;

export function Box<T extends ElementType = 'div'>({
  as,
  className,
  children,
  ...props
}: BoxProps<T>) {
  const Component = as || 'div';

  return (
    <Component className={className} {...props}>
      {children}
    </Component>
  );
}

// Usage
<Box as="section" className="container">Content</Box>
<Box as="article">Article content</Box>
<Box as="a" href="/link">Link</Box>
```

### Index File Exports

```tsx
// Button/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button';

// features/auth/index.ts
export { LoginForm } from './components/LoginForm';
export { RegisterForm } from './components/RegisterForm';
export { useAuth } from './hooks/useAuth';
export type { User, AuthState } from './types';
```

## Anti-patterns

### Avoid: Prop Drilling

```tsx
// BAD - passing props through many levels
<App user={user}>
  <Layout user={user}>
    <Sidebar user={user}>
      <UserMenu user={user} />
    </Sidebar>
  </Layout>
</App>

// GOOD - use context
const UserContext = createContext<User | null>(null);

<UserContext.Provider value={user}>
  <App>
    <Layout>
      <Sidebar>
        <UserMenu />  {/* Uses useContext(UserContext) */}
      </Sidebar>
    </Layout>
  </App>
</UserContext.Provider>
```

### Avoid: Giant Components

```tsx
// BAD - doing too much
function Dashboard() {
  // 500 lines of JSX, multiple concerns
}

// GOOD - composed from smaller parts
function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <DashboardStats />
      <RecentActivity />
      <DashboardSidebar />
    </DashboardLayout>
  );
}
```

### Avoid: Business Logic in Components

```tsx
// BAD - logic mixed with UI
function OrderForm() {
  const handleSubmit = async () => {
    // Validation logic
    // API calls
    // Error handling
    // State updates
  };
}

// GOOD - extract to hooks/services
function OrderForm() {
  const { submitOrder, isLoading, error } = useOrderSubmission();
  // Component only handles UI
}
```

## References

- [React Documentation](https://react.dev/)
- [Patterns.dev - React Patterns](https://www.patterns.dev/react)
- [Bulletproof React](https://github.com/alan2207/bulletproof-react)
- [Component Patterns](https://www.patterns.dev/posts/compound-pattern)
