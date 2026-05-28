# Component Patterns

Modern React component architecture emphasizing type safety, lazy loading, and Suspense boundaries.

---

## React.FC Pattern (PREFERRED)

### Why React.FC

All components use the `React.FC<Props>` pattern for:
- Explicit type safety for props
- Consistent component signatures
- Clear prop interface documentation
- Better IDE autocomplete

### Basic Pattern

```typescript
import React from 'react';

interface MyComponentProps {
    /** User ID to display */
    userId: number;
    /** Optional callback when action occurs */
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ userId, onAction }) => {
    return (
        <div>
            User: {userId}
        </div>
    );
};

export default MyComponent;
```

**Key Points:**
- Props interface defined separately with JSDoc comments
- `React.FC<Props>` provides type safety
- Destructure props in parameters
- Default export at bottom

---

## Lazy Loading Pattern

### When to Lazy Load

Lazy load components that are:
- Heavy (DataGrid, charts, rich text editors)
- Route-level components
- Conditionally rendered (modals, dialogs)

### Implementation

```typescript
import React, { lazy } from 'react';
import { SuspenseLoader } from '~components/SuspenseLoader';

// Lazy load the component
const HeavyDataGrid = lazy(() => import('./HeavyDataGrid'));

export const MyFeature: React.FC = () => {
    return (
        <SuspenseLoader>
            <HeavyDataGrid />
        </SuspenseLoader>
    );
};
```

### Named Export Handling

```typescript
// If component uses named export
const MyComponent = lazy(() =>
    import('./MyComponent').then((module) => ({ default: module.MyComponent }))
);
```

---

## SuspenseLoader Component

### Usage

```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';

// Basic usage
<SuspenseLoader>
    <MyComponent />
</SuspenseLoader>

// With custom fallback
<SuspenseLoader fallback={<CustomSkeleton />}>
    <MyComponent />
</SuspenseLoader>
```

### Implementation

```typescript
import React, { Suspense } from 'react';
import { Box, CircularProgress } from '@mui/material';

interface SuspenseLoaderProps {
    children: React.ReactNode;
    fallback?: React.ReactNode;
}

export const SuspenseLoader: React.FC<SuspenseLoaderProps> = ({ 
    children, 
    fallback = <DefaultLoader /> 
}) => {
    return (
        <Suspense fallback={fallback}>
            {children}
        </Suspense>
    );
};

const DefaultLoader: React.FC = () => (
    <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
    </Box>
);
```

---

## Data Fetching in Components

### useSuspenseQuery Pattern

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';

export const MyComponent: React.FC<Props> = ({ id }) => {
    // No isLoading - Suspense handles it!
    const { data } = useSuspenseQuery({
        queryKey: ['entity', id],
        queryFn: () => api.getEntity(id),
    });

    // data is ALWAYS defined here
    return <div>{data.name}</div>;
};
```

---

## Event Handlers

### useCallback Pattern

```typescript
import { useCallback } from 'react';

export const MyComponent: React.FC<Props> = ({ onSave }) => {
    const handleClick = useCallback(() => {
        // Logic
        onSave?.();
    }, [onSave]);

    const handleChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value);
    }, []);

    return <Button onClick={handleClick}>Save</Button>;
};
```

---

## Advanced Patterns

### Compound Components

```typescript
// Card.tsx
export const Card: React.FC<CardProps> & {
    Header: typeof CardHeader;
    Body: typeof CardBody;
    Footer: typeof CardFooter;
} = ({ children }) => {
    return <Paper>{children}</Paper>;
};

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;

// Usage
<Card>
    <Card.Header>Title</Card.Header>
    <Card.Body>Content</Card.Body>
    <Card.Footer>Actions</Card.Footer>
</Card>
```

---

## Summary

**Modern Component Recipe:**
1. `React.FC<Props>` with TypeScript
2. Lazy load if heavy: `React.lazy(() => import())`
3. Wrap in `<SuspenseLoader>` for loading
4. Use `useSuspenseQuery` for data
5. Import aliases (@/, ~types, ~components)
6. Event handlers with `useCallback`
7. Default export at bottom
8. No early returns for loading states

**See Also:**
- [data-fetching.md](data-fetching.md) - useSuspenseQuery details
- [loading-and-error-states.md](loading-and-error-states.md) - Suspense best practices
