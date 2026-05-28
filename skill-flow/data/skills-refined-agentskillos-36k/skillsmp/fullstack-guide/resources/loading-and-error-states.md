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

**Option 1: SuspenseLoader (PREFERRED for new components)**

```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';

const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

export const MyComponent: React.FC = () => {
    return (
        <SuspenseLoader>
            <HeavyComponent />
        </SuspenseLoader>
    );
};
```

**Option 2: LoadingOverlay (for existing components)**

```typescript
import { LoadingOverlay } from '~components/LoadingOverlay';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <Box sx={{ position: 'relative' }}>
            {isLoading && <LoadingOverlay />}
            <Content data={data} />
        </Box>
    );
};
```

---

## SuspenseLoader Component

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
    fallback 
}) => {
    const defaultFallback = (
        <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center',
            minHeight: 200,
            p: 4 
        }}>
            <CircularProgress />
        </Box>
    );

    return (
        <Suspense fallback={fallback || defaultFallback}>
            {children}
        </Suspense>
    );
};
```

---

## Error Handling

### useMuiSnackbar Hook

**ALWAYS use `useMuiSnackbar` for user feedback:**

```typescript
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

export const MyComponent: React.FC = () => {
    const { showSnackbar } = useMuiSnackbar();

    const handleAction = async () => {
        try {
            await doSomething();
            showSnackbar('Success!', 'success');
        } catch (error) {
            showSnackbar('Something went wrong', 'error');
        }
    };
};
```

**NEVER use react-toastify** - always use MUI snackbars for consistency.

### Mutation Error Handling

```typescript
const mutation = useMutation({
    mutationFn: userApi.create,
    onSuccess: () => {
        showSnackbar('User created!', 'success');
    },
    onError: (error) => {
        showSnackbar(error.message || 'Failed to create user', 'error');
    },
});
```

---

## Error Boundaries

### Component-Level Errors

```typescript
import { ErrorBoundary } from '~components/ErrorBoundary';

export const MyFeature: React.FC = () => {
    return (
        <ErrorBoundary fallback={<ErrorMessage />}>
            <RiskyComponent />
        </ErrorBoundary>
    );
};
```

### ErrorBoundary Implementation

```typescript
interface Props {
    children: React.ReactNode;
    fallback?: React.ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
    state: State = { hasError: false };

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, info: React.ErrorInfo) {
        console.error('ErrorBoundary caught:', error, info);
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback || <DefaultError />;
        }
        return this.props.children;
    }
}
```

---

## Skeleton Loading

### MUI Skeleton Component

```typescript
import { Skeleton, Box } from '@mui/material';

export const MyComponent: React.FC = () => {
    const { data, isLoading } = useQuery({ ... });

    return (
        <Box sx={{ p: 2 }}>
            {isLoading ? (
                <>
                    <Skeleton variant="text" width={200} height={40} />
                    <Skeleton variant="rectangular" width="100%" height={200} />
                    <Skeleton variant="text" width="100%" />
                </>
            ) : (
                <>
                    <Typography variant="h5">{data.title}</Typography>
                    <img src={data.image} />
                    <Typography>{data.description}</Typography>
                </>
            )}
        </Box>
    );
};
```

**Key**: Skeleton must have **same layout** as actual content (no shift)

---

## Summary

**Loading States:**
- ✅ **PREFERRED**: SuspenseLoader + useSuspenseQuery
- ✅ **ACCEPTABLE**: LoadingOverlay
- ✅ **OK**: Skeleton with same layout
- ❌ **NEVER**: Early returns or conditional layout

**Error Handling:**
- ✅ **ALWAYS**: useMuiSnackbar for user feedback
- ❌ **NEVER**: react-toastify
- ✅ Use onError callbacks in queries/mutations
- ✅ Error boundaries for component-level errors

**See Also:**
- [component-patterns.md](component-patterns.md) - Suspense integration
- [data-fetching.md](data-fetching.md) - useSuspenseQuery details
