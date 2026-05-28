# Component Patterns

Modern React component architecture for the application emphasizing type safety, lazy loading, and Suspense boundaries.

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
- Modal/dialog content (not shown initially)
- Below-the-fold content

### How to Lazy Load

```typescript
import React from 'react';

// Lazy load heavy component
const PostDataGrid = React.lazy(() =>
    import('./grids/PostDataGrid')
);

// For named exports
const MyComponent = React.lazy(() =>
    import('./MyComponent').then(module => ({
        default: module.MyComponent
    }))
);
```

**Example from PostTable.tsx:**

```typescript
/**
 * Main game table container component
 */
import React, { useState, useCallback } from 'react';
import { Card, CardBody } from '@/components/ui';

// Lazy load GameDataGrid to optimize bundle size
const GameDataGrid = React.lazy(() => import('./grids/GameDataGrid'));

import { SuspenseLoader } from '@/components/SuspenseLoader';

export const GameTable: React.FC<GameTableProps> = ({ userId }) => {
    return (
        <Card variant="default" padding="md">
            <CardBody>
                <SuspenseLoader>
                    <GameDataGrid userId={userId} />
                </SuspenseLoader>
            </CardBody>
        </Card>
    );
};

export default GameTable;
```

---

## Suspense Boundaries

### SuspenseLoader Component

**Import:**
```typescript
import { SuspenseLoader } from '~components/SuspenseLoader';
// Or
import { SuspenseLoader } from '@/components/SuspenseLoader';
```

**Usage:**
```typescript
<SuspenseLoader>
    <LazyLoadedComponent />
</SuspenseLoader>
```

**What it does:**
- Shows loading indicator while lazy component loads
- Smooth fade-in animation
- Consistent loading experience
- Prevents layout shift

### Where to Place Suspense Boundaries

**Route Level:**
```typescript
// routes/my-route/index.tsx
const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));

function Route() {
    return (
        <SuspenseLoader>
            <MyPage />
        </SuspenseLoader>
    );
}
```

**Component Level:**
```typescript
function ParentComponent() {
    return (
        <div className="flex flex-col gap-4">
            <Header />
            <SuspenseLoader>
                <HeavyDataGrid />
            </SuspenseLoader>
        </div>
    );
}
```

**Multiple Boundaries:**
```typescript
function Page() {
    return (
        <div className="grid grid-cols-12 gap-4">
            <div className="col-span-12">
                <SuspenseLoader>
                    <HeaderSection />
                </SuspenseLoader>
            </div>

            <div className="col-span-8">
                <SuspenseLoader>
                    <MainContent />
                </SuspenseLoader>
            </div>

            <div className="col-span-4">
                <SuspenseLoader>
                    <Sidebar />
                </SuspenseLoader>
            </div>
        </div>
    );
}
```

Each section loads independently, better UX.

---

## Component Structure Template

### Recommended Order

```typescript
/**
 * Component description
 * What it does, when to use it
 */
import React, { useState, useCallback, useMemo, useEffect } from 'react';
import { Button, Card, CardBody, Alert } from '@/components/ui';
import { useSuspenseQuery } from '@tanstack/react-query';

// Feature imports
import { myFeatureApi } from '../api/myFeatureApi';
import type { MyData } from '@/types/myData';

// Component imports
import { SuspenseLoader } from '@/components/SuspenseLoader';

// Hooks
import { useAuth } from '@/contexts/AuthContext';

// 1. PROPS INTERFACE (with JSDoc)
interface MyComponentProps {
    /** The ID of the entity to display */
    entityId: number;
    /** Optional callback when action completes */
    onComplete?: () => void;
    /** Display mode */
    mode?: 'view' | 'edit';
}

// 2. COMPONENT DEFINITION (use Tailwind classes for styling)
export const MyComponent: React.FC<MyComponentProps> = ({
    entityId,
    onComplete,
    mode = 'view',
}) => {
    // 3. HOOKS (in this order)
    // - Context hooks first
    const { user } = useAuth();

    // - Data fetching
    const { data } = useSuspenseQuery({
        queryKey: ['myEntity', entityId],
        queryFn: () => myFeatureApi.getEntity(entityId),
    });

    // - Local state
    const [selectedItem, setSelectedItem] = useState<string | null>(null);
    const [isEditing, setIsEditing] = useState(mode === 'edit');

    // - Memoized values
    const filteredData = useMemo(() => {
        return data.filter(item => item.active);
    }, [data]);

    // - Effects
    useEffect(() => {
        // Setup
        return () => {
            // Cleanup
        };
    }, []);

    // 4. EVENT HANDLERS (with useCallback)
    const handleItemSelect = useCallback((itemId: string) => {
        setSelectedItem(itemId);
    }, []);

    const handleSave = useCallback(async () => {
        try {
            await myFeatureApi.updateEntity(entityId, { /* data */ });
            showSuccess('Entity updated successfully');
            onComplete?.();
        } catch (error) {
            showError('Failed to update entity');
        }
    }, [entityId, onComplete, showSuccess, showError]);

    // 6. RENDER
    return (
        <Card variant="default" padding="md">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-text-heading">My Component</h2>
                <Button variant="primary" onClick={handleSave}>Save</Button>
            </div>

            <CardBody>
                {filteredData.map(item => (
                    <div key={item.id} className="py-2 border-b border-border-primary">
                        {item.name}
                    </div>
                ))}
            </CardBody>
        </Card>
    );
};

// 7. EXPORT (default export at bottom)
export default MyComponent;
```

---

## Component Separation

### When to Split Components

**Split into multiple components when:**
- Component exceeds 300 lines
- Multiple distinct responsibilities
- Reusable sections
- Complex nested JSX

**Example:**

```typescript
// ❌ AVOID - Monolithic
function MassiveComponent() {
    // 500+ lines
    // Search logic
    // Filter logic
    // Grid logic
    // Action panel logic
}

// ✅ PREFERRED - Modular
function ParentContainer() {
    return (
        <div className="space-y-4">
            <SearchAndFilter onFilter={handleFilter} />
            <DataGrid data={filteredData} />
            <ActionPanel onAction={handleAction} />
        </div>
    );
}
```

### When to Keep Together

**Keep in same file when:**
- Component < 200 lines
- Tightly coupled logic
- Not reusable elsewhere
- Simple presentation component

---

## Export Patterns

### Named Const + Default Export (PREFERRED)

```typescript
export const MyComponent: React.FC<Props> = ({ ... }) => {
    // Component logic
};

export default MyComponent;
```

**Why:**
- Named export for testing/refactoring
- Default export for lazy loading convenience
- Both options available to consumers

### Lazy Loading Named Exports

```typescript
const MyComponent = React.lazy(() =>
    import('./MyComponent').then(module => ({
        default: module.MyComponent
    }))
);
```

---

## Component Communication

### Props Down, Events Up

```typescript
// Parent
function Parent() {
    const [selectedId, setSelectedId] = useState<string | null>(null);

    return (
        <Child
            data={data}                    // Props down
            onSelect={setSelectedId}       // Events up
        />
    );
}

// Child
interface ChildProps {
    data: Data[];
    onSelect: (id: string) => void;
}

export const Child: React.FC<ChildProps> = ({ data, onSelect }) => {
    return (
        <div onClick={() => onSelect(data[0].id)}>
            {/* Content */}
        </div>
    );
};
```

### Avoid Prop Drilling

**Use context for deep nesting:**
```typescript
// ❌ AVOID - Prop drilling 5+ levels
<A prop={x}>
  <B prop={x}>
    <C prop={x}>
      <D prop={x}>
        <E prop={x} />  // Finally uses it here
      </D>
    </C>
  </B>
</A>

// ✅ PREFERRED - Context or TanStack Query
const MyContext = createContext<MyData | null>(null);

function Provider({ children }) {
    const { data } = useSuspenseQuery({ ... });
    return <MyContext.Provider value={data}>{children}</MyContext.Provider>;
}

function DeepChild() {
    const data = useContext(MyContext);
    // Use data directly
}
```

---

## Advanced Patterns

### Compound Components

```typescript
// GameCard.tsx
export const GameCard: React.FC<GameCardProps> & {
    Header: typeof GameCardHeader;
    Body: typeof GameCardBody;
    Footer: typeof GameCardFooter;
} = ({ children }) => {
    return <Card variant="default">{children}</Card>;
};

GameCard.Header = GameCardHeader;
GameCard.Body = GameCardBody;
GameCard.Footer = GameCardFooter;

// Usage
<Card>
    <Card.Header>Title</Card.Header>
    <Card.Body>Content</Card.Body>
    <Card.Footer>Actions</Card.Footer>
</Card>
```

### Render Props (Rare, but useful)

```typescript
interface DataProviderProps {
    children: (data: Data) => React.ReactNode;
}

export const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
    const { data } = useSuspenseQuery({ ... });
    return <>{children(data)}</>;
};

// Usage
<DataProvider>
    {(data) => <Display data={data} />}
</DataProvider>
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
- [complete-examples.md](complete-examples.md) - Full working examples
