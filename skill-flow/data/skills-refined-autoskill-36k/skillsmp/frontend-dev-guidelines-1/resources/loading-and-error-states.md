# Loading & Error States

**CRITICAL**: Proper loading and error state handling prevents layout shift and provides better user experience.

---

## ⚠️ CRITICAL RULE: Never Use Early Returns

### The Problem

```typescript
// ❌ NEVER DO THIS - Early return with loading spinner
const Component = () => {
    const { data, isLoading } = useQuery();

    // WRONG: This causes layout shift and poor UX
    if (isLoading) {
        return <LoadingSpinner />;
    }

    return <Content data={data} />;
};
```

**Why this is bad:**
1. **Layout Shift**: Content position jumps when loading completes
2. **CLS (Cumulative Layout Shift)**: Poor Core Web Vital score
3. **Jarring UX**: Page structure changes suddenly
4. **Lost Scroll Position**: User loses place on page

### The Solutions

**Option 1: Suspense Boundary (PREFERRED for new components)**

```typescript
import { Suspense } from 'react';
import { Spinner } from '@/components/ui';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

export const MyComponent: React.FC = () => {
    return (
        <Suspense fallback={<div className="flex justify-center p-8"><Spinner size="lg" /></div>}>
            <HeavyComponent />
        </Suspense>
    );
};
```

**Option 2: Inline Loading State (for legacy useQuery patterns)**

```typescript
import { Spinner } from '@/components/ui';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <div className="relative min-h-[200px]">
            {isLoading && (
                <div className="flex justify-center items-center p-8">
                    <Spinner size="lg" />
                </div>
            )}
            {!isLoading && <Content data={data} />}
        </div>
    );
};
```

---

## Suspense Boundaries

### What They Do

- Shows loading indicator while components/data load
- Prevents layout shift with consistent fallback UI
- Built-in React feature (no custom component needed)
- Consistent loading experience across app

### Basic Usage with Lazy Loading

```typescript
import { Suspense } from 'react';
import { Spinner } from '@/components/ui';

const LazyComponent = React.lazy(() => import('./LazyComponent'));

export const MyComponent: React.FC = () => {
    return (
        <Suspense fallback={<div className="flex justify-center p-8"><Spinner size="lg" /></div>}>
            <LazyComponent />
        </Suspense>
    );
};
```

### With useSuspenseQuery

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { Suspense } from 'react';
import { Spinner } from '@/components/ui';

const Inner: React.FC = () => {
    // No isLoading needed!
    const { data } = useSuspenseQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),
    });

    return <Display data={data} />;
};

// Outer component wraps in Suspense
export const Outer: React.FC = () => {
    return (
        <Suspense fallback={<div className="flex justify-center p-8"><Spinner size="lg" /></div>}>
            <Inner />
        </Suspense>
    );
};
```

### Multiple Suspense Boundaries

**Pattern**: Separate loading for independent sections

```typescript
import { Suspense } from 'react';
import { Spinner } from '@/components/ui';

const LoadingFallback = () => (
    <div className="flex justify-center p-4">
        <Spinner size="md" />
    </div>
);

export const Dashboard: React.FC = () => {
    return (
        <div className="space-y-4">
            <Suspense fallback={<LoadingFallback />}>
                <Header />
            </Suspense>

            <Suspense fallback={<LoadingFallback />}>
                <MainContent />
            </Suspense>

            <Suspense fallback={<LoadingFallback />}>
                <Sidebar />
            </Suspense>
        </div>
    );
};
```

**Benefits:**
- Each section loads independently
- User sees partial content sooner
- Better perceived performance

### Nested Suspense

```typescript
export const ParentComponent: React.FC = () => {
    return (
        <Suspense fallback={<Spinner size="lg" />}>
            {/* Parent suspends while loading */}
            <ParentContent>
                <Suspense fallback={<Spinner size="sm" />}>
                    {/* Nested suspense for child */}
                    <ChildComponent />
                </Suspense>
            </ParentContent>
        </Suspense>
    );
};
```

---

## Inline Loading States

### When to Use

- Legacy components with `useQuery` (not refactored to Suspense yet)
- Need overlay loading state
- Can't use Suspense boundaries

### Pattern with Conditional Rendering

```typescript
import { Spinner } from '@/components/ui';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),
    });

    return (
        <div className="relative min-h-[400px]">
            {isLoading && (
                <div className="flex justify-center items-center p-8">
                    <Spinner size="lg" label="Loading data..." />
                </div>
            )}
            {!isLoading && data && (
                <div className="p-4">
                    <Content data={data} />
                </div>
            )}
        </div>
    );
};
```

**Key Points:**
- Fixed min-height prevents layout shift
- Conditional rendering avoids early returns
- Content area structure remains consistent

---

## Error Handling

### Toast Notifications (REQUIRED)

**Project standard**: react-hot-toast for user feedback

```typescript
import { toast } from 'react-hot-toast';
import { Button } from '@/components/ui';

export const MyComponent: React.FC = () => {
    const handleAction = async () => {
        try {
            await api.doSomething();
            toast.success('Operation completed successfully');
        } catch (error) {
            toast.error('Operation failed');
        }
    };

    return <Button onClick={handleAction}>Do Action</Button>;
};
```

**Available Methods:**
- `toast.success(message)` - Green success message
- `toast.error(message)` - Red error message
- `toast.loading(message)` - Loading indicator
- `toast(message)` - Default message
- `toast.promise(promise, { loading, success, error })` - Automatic state handling

### TanStack Query Error Callbacks

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';

export const MyComponent: React.FC = () => {
    const { data } = useSuspenseQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),

        // Handle errors
        onError: (error) => {
            toast.error('Failed to load data');
            console.error('Query error:', error);
        },
    });

    return <Content data={data} />;
};
```

### Toast with Promises

```typescript
import { toast } from 'react-hot-toast';

const saveData = async (data: any) => {
    const promise = api.save(data);

    toast.promise(promise, {
        loading: 'Saving...',
        success: 'Saved successfully!',
        error: 'Failed to save',
    });

    return promise;
};
```

### Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary';
import { Alert, Button } from '@/components/ui';

function ErrorFallback({ error, resetErrorBoundary }) {
    return (
        <div className="p-8 text-center">
            <Alert variant="danger" title="Something went wrong">
                {error.message}
            </Alert>
            <Button
                variant="primary"
                onClick={resetErrorBoundary}
                className="mt-4"
            >
                Try Again
            </Button>
        </div>
    );
}

export const MyPage: React.FC = () => {
    return (
        <ErrorBoundary
            FallbackComponent={ErrorFallback}
            onError={(error) => console.error('Boundary caught:', error)}
        >
            <Suspense fallback={<Spinner size="lg" />}>
                <ComponentThatMightError />
            </Suspense>
        </ErrorBoundary>
    );
};
```

### Alert Component for Inline Errors

For non-critical errors that don't need toasts:

```typescript
import { Alert } from '@/components/ui';

export const MyComponent: React.FC = () => {
    const { data, error } = useQuery({
        queryKey: ['data'],
        queryFn: () => api.getData(),
    });

    if (error) {
        return (
            <Alert variant="danger" title="Failed to load data">
                Please try again later or contact support if the problem persists.
            </Alert>
        );
    }

    return <Content data={data} />;
};
```

---

## Complete Examples

### Example 1: Modern Component with Suspense

```typescript
import React, { Suspense } from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Card, CardBody, Spinner } from '@/components/ui';
import { myFeatureApi } from '../api/myFeatureApi';

// Inner component uses useSuspenseQuery
const InnerComponent: React.FC<{ id: number }> = ({ id }) => {
    const { data } = useSuspenseQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    // data is always defined - no isLoading needed!
    return (
        <Card variant="default">
            <CardBody>
                <h2 className="text-xl font-semibold text-text-heading">{data.title}</h2>
                <p className="text-text-primary mt-2">{data.description}</p>
            </CardBody>
        </Card>
    );
};

// Outer component provides Suspense boundary
export const OuterComponent: React.FC<{ id: number }> = ({ id }) => {
    return (
        <Suspense fallback={
            <div className="flex justify-center p-8">
                <Spinner size="lg" />
            </div>
        }>
            <InnerComponent id={id} />
        </Suspense>
    );
};

export default OuterComponent;
```

### Example 2: Legacy Pattern with Inline Loading

```typescript
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardBody, Spinner, Alert } from '@/components/ui';
import { myFeatureApi } from '../api/myFeatureApi';

export const LegacyComponent: React.FC<{ id: number }> = ({ id }) => {
    const { data, isLoading, error } = useQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
    });

    return (
        <div className="relative min-h-[300px]">
            {isLoading && (
                <div className="flex justify-center items-center p-8">
                    <Spinner size="lg" label="Loading..." />
                </div>
            )}

            {error && (
                <Alert variant="danger" title="Error loading data">
                    {error.message}
                </Alert>
            )}

            {!isLoading && data && (
                <Card variant="default">
                    <CardBody>
                        <Content data={data} />
                    </CardBody>
                </Card>
            )}
        </div>
    );
};
```

### Example 3: Error Handling with Toast

```typescript
import React from 'react';
import { useSuspenseQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { Button } from '@/components/ui';
import { myFeatureApi } from '../api/myFeatureApi';

export const EntityEditor: React.FC<{ id: number }> = ({ id }) => {
    const queryClient = useQueryClient();

    const { data } = useSuspenseQuery({
        queryKey: ['entity', id],
        queryFn: () => myFeatureApi.getEntity(id),
        onError: () => {
            toast.error('Failed to load entity');
        },
    });

    const updateMutation = useMutation({
        mutationFn: (updates) => myFeatureApi.update(id, updates),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['entity', id] });
            toast.success('Entity updated successfully');
        },

        onError: () => {
            toast.error('Failed to update entity');
        },
    });

    return (
        <Button
            variant="primary"
            onClick={() => updateMutation.mutate({ name: 'New' })}
            loading={updateMutation.isPending}
        >
            Update
        </Button>
    );
};
```

---

## Loading State Anti-Patterns

### ❌ What NOT to Do

```typescript
// ❌ NEVER - Early return
if (isLoading) {
    return <Spinner />;
}

// ❌ NEVER - Conditional rendering without layout preservation
{isLoading ? <Spinner /> : <Content />}

// ❌ NEVER - Layout changes
if (isLoading) {
    return (
        <div className="h-[100px]">
            <Spinner />
        </div>
    );
}
return (
    <div className="h-[500px]">  // Different height!
        <Content />
    </div>
);
```

### ✅ What TO Do

```typescript
// ✅ BEST - useSuspenseQuery + Suspense
<Suspense fallback={<Spinner size="lg" />}>
    <ComponentWithSuspenseQuery />
</Suspense>

// ✅ ACCEPTABLE - Inline loading with preserved layout
<div className="relative min-h-[400px]">
    {isLoading && <Spinner />}
    {!isLoading && <Content />}
</div>

// ✅ OK - Tailwind skeleton with same layout
<div className="h-[500px]">
    {isLoading ? (
        <div className="animate-pulse space-y-4">
            <div className="h-8 bg-bg-secondary rounded w-1/4"></div>
            <div className="h-48 bg-bg-secondary rounded"></div>
            <div className="h-4 bg-bg-secondary rounded"></div>
        </div>
    ) : (
        <Content />
    )}
</div>
```

---

## Skeleton Loading (Alternative)

### Tailwind Skeleton Pattern

```typescript
import { Card, CardBody } from '@/components/ui';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <Card variant="default">
            <CardBody>
                {isLoading ? (
                    <div className="animate-pulse space-y-4">
                        <div className="h-6 bg-bg-secondary rounded w-48"></div>
                        <div className="h-40 bg-bg-secondary rounded"></div>
                        <div className="h-4 bg-bg-secondary rounded"></div>
                    </div>
                ) : (
                    <>
                        <h2 className="text-xl font-semibold">{data.title}</h2>
                        <img src={data.image} className="my-4" />
                        <p>{data.description}</p>
                    </>
                )}
            </CardBody>
        </Card>
    );
};
```

**Key**: Skeleton must have **same layout** as actual content (no shift)

---

## Summary

**Loading States:**
- ✅ **PREFERRED**: Suspense + useSuspenseQuery (modern pattern)
- ✅ **ACCEPTABLE**: Inline loading with preserved layout
- ✅ **OK**: Tailwind skeleton with same layout
- ❌ **NEVER**: Early returns or conditional layout

**Error Handling:**
- ✅ **ALWAYS**: react-hot-toast for user feedback
- ✅ **Alert component**: For inline, non-critical errors
- ✅ Use onError callbacks in queries/mutations
- ✅ Error boundaries for component-level errors

**See Also:**
- [component-patterns.md](component-patterns.md) - Suspense integration
- [data-fetching.md](data-fetching.md) - useSuspenseQuery details
- [styling-guide.md](styling-guide.md) - UI component library reference
