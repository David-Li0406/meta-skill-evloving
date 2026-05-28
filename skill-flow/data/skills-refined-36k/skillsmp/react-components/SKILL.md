---
name: react-components
description: Best practices for building React components including hooks patterns, state management, composition, and performance optimization techniques
version: 1.0.0
priority: 25
tags:
  - react
  - components
  - hooks
  - typescript
  - builtin
triggers:
  - type: keyword
    pattern: react
  - type: keyword
    pattern: component
  - type: keyword
    pattern: hooks
  - type: glob
    pattern: "**/*.tsx"
  - type: glob
    pattern: "**/components/**"
globs:
  - "**/*.tsx"
  - "**/components/**/*.ts"
---

# React Components

Guidelines for building maintainable, performant React components with TypeScript.

## Rules

- **Single Responsibility**: Each component should do one thing well
- **Props Over State**: Prefer controlled components; lift state when needed
- **Type Everything**: Use TypeScript interfaces for all props and state
- **Composition Over Inheritance**: Build complex UIs by composing simple components
- **Avoid Inline Functions in Render**: Use `useCallback` for event handlers passed to children
- **Memoize Expensive Calculations**: Use `useMemo` for costly computations
- **Key Prop Stability**: Never use array index as key for dynamic lists
- **Error Boundaries**: Wrap major sections with error boundaries
- **Accessibility First**: Include ARIA attributes and keyboard navigation

## Patterns

### Component Structure

```typescript
import { type FC, useState, useCallback, useMemo } from "react";

// Props interface with clear documentation
interface UserCardProps {
  /** User data to display */
  user: User;
  /** Called when edit button is clicked */
  onEdit?: (userId: string) => void;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Displays user information in a card format.
 * Supports optional edit functionality.
 */
export const UserCard: FC<UserCardProps> = ({
  user,
  onEdit,
  className,
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleEdit = useCallback(() => {
    onEdit?.(user.id);
  }, [onEdit, user.id]);

  const displayName = useMemo(
    () => `${user.firstName} ${user.lastName}`.trim(),
    [user.firstName, user.lastName]
  );

  return (
    <article className={`user-card ${className ?? ""}`}>
      <h3>{displayName}</h3>
      {onEdit && (
        <button onClick={handleEdit} aria-label={`Edit ${displayName}`}>
          Edit
        </button>
      )}
    </article>
  );
};
```markdown

### Custom Hooks

```typescript
import { useState, useEffect, useCallback } from "react";

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
```markdown

### Compound Components

```typescript
import { createContext, useContext, type FC, type ReactNode } from "react";

// Context for compound component communication
interface TabsContextValue {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error("Tab components must be used within Tabs");
  }
  return context;
}

// Parent component
interface TabsProps {
  defaultTab: string;
  children: ReactNode;
}

export const Tabs: FC<TabsProps> & {
  List: typeof TabList;
  Tab: typeof Tab;
  Panel: typeof TabPanel;
} = ({ defaultTab, children }) => {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
};

// Child components
const TabList: FC<{ children: ReactNode }> = ({ children }) => (
  <div role="tablist">{children}</div>
);

const Tab: FC<{ id: string; children: ReactNode }> = ({ id, children }) => {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={activeTab === id}
      onClick={() => setActiveTab(id)}
    >
      {children}
    </button>
  );
};

const TabPanel: FC<{ id: string; children: ReactNode }> = ({ id, children }) => {
  const { activeTab } = useTabsContext();
  if (activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
};

Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;
```markdown

### Render Props & Children as Function

```typescript
interface RenderProps<T> {
  data: T;
  loading: boolean;
  error: Error | null;
}

interface DataLoaderProps<T> {
  url: string;
  children: (props: RenderProps<T>) => ReactNode;
}

export function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const { data, loading, error } = useFetch<T>(url);
  return <>{children({ data, loading, error })}</>;
}

// Usage
<DataLoader<User[]> url="/api/users">
  {({ data, loading, error }) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    return <UserList users={data ?? []} />;
  }}
</DataLoader>
```markdown

## Anti-Patterns

```typescript
// ❌ Props drilling through many levels
const App = ({ user }) => <Layout user={user} />;
const Layout = ({ user }) => <Sidebar user={user} />;
const Sidebar = ({ user }) => <Avatar user={user} />; // Use context instead

// ❌ Mutating state directly
const handleAdd = () => {
  items.push(newItem); // Wrong!
  setItems(items);
};
// ✅ Create new array
const handleAdd = () => setItems([...items, newItem]);

// ❌ Missing dependency in useEffect
useEffect(() => {
  fetchUser(userId); // userId not in deps!
}, []); // Will cause stale closures

// ❌ Index as key for dynamic lists
{items.map((item, i) => <Item key={i} {...item} />)} // Breaks on reorder

// ❌ Derived state in useState
const [fullName, setFullName] = useState(`${first} ${last}`);
// ✅ Compute during render or useMemo
const fullName = useMemo(() => `${first} ${last}`, [first, last]);

// ❌ Unnecessary useEffect for sync
useEffect(() => {
  setCount(items.length);
}, [items]); // Just compute: const count = items.length;
```markdown

## Examples

### Form with Validation

```typescript
import { type FC, type FormEvent, useState, useCallback } from "react";

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

export const LoginForm: FC<{ onSubmit: (data: FormData) => void }> = ({
  onSubmit,
}) => {
  const [data, setData] = useState<FormData>({ email: "", password: "" });
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Set<keyof FormData>>(new Set());

  const validate = useCallback((values: FormData): FormErrors => {
    const errs: FormErrors = {};
    if (!values.email.includes("@")) errs.email = "Invalid email";
    if (values.password.length < 8) errs.password = "Min 8 characters";
    return errs;
  }, []);

  const handleChange = useCallback((field: keyof FormData, value: string) => {
    setData((prev) => ({ ...prev, [field]: value }));
  }, []);

  const handleBlur = useCallback((field: keyof FormData) => {
    setTouched((prev) => new Set(prev).add(field));
    setErrors(validate(data));
  }, [data, validate]);

  const handleSubmit = useCallback(
    (e: FormEvent) => {
      e.preventDefault();
      const validationErrors = validate(data);
      setErrors(validationErrors);
      if (Object.keys(validationErrors).length === 0) {
        onSubmit(data);
      }
    },
    [data, onSubmit, validate]
  );

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={data.email}
          onChange={(e) => handleChange("email", e.target.value)}
          onBlur={() => handleBlur("email")}
          aria-invalid={touched.has("email") && !!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {touched.has("email") && errors.email && (
          <span id="email-error" role="alert">{errors.email}</span>
        )}
      </div>
      <button type="submit">Login</button>
    </form>
  );
};
```markdown

### List with Virtualization Hook

```typescript
import { useRef, useState, useEffect, useMemo, type CSSProperties } from "react";

interface UseVirtualListOptions {
  itemCount: number;
  itemHeight: number;
  overscan?: number;
}

export function useVirtualList({ itemCount, itemHeight, overscan = 3 }: UseVirtualListOptions) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scrollTop, setScrollTop] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleScroll = () => setScrollTop(container.scrollTop);
    const handleResize = () => setContainerHeight(container.clientHeight);

    container.addEventListener("scroll", handleScroll, { passive: true });
    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      container.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const { startIndex, endIndex, offsetY } = useMemo(() => {
    const start = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
    const visibleCount = Math.ceil(containerHeight / itemHeight);
    const end = Math.min(itemCount - 1, start + visibleCount + overscan * 2);
    return { startIndex: start, endIndex: end, offsetY: start * itemHeight };
  }, [scrollTop, containerHeight, itemHeight, itemCount, overscan]);

  const totalHeight = itemCount * itemHeight;

  return { containerRef, startIndex, endIndex, offsetY, totalHeight };
}
```

## References

- [React Documentation](https://react.dev/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [Patterns.dev - React Patterns](https://www.patterns.dev/react/)
- [Kent C. Dodds Blog](https://kentcdodds.com/blog)
