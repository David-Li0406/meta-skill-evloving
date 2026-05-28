# React Code Review Guide

Review points specific to React components and patterns.

## Component Patterns

### Functional Components

```typescript
// Preferred: Function declaration with explicit props
interface UserCardProps {
  user: User;
  onSelect?: (user: User) => void;
}

function UserCard({ user, onSelect }: UserCardProps) {
  return (
    <div onClick={() => onSelect?.(user)}>
      {user.name}
    </div>
  );
}

// Also acceptable: Arrow function
const UserCard = ({ user, onSelect }: UserCardProps) => (
  <div onClick={() => onSelect?.(user)}>
    {user.name}
  </div>
);
```

### Props Interface Design

```typescript
// Good: Specific props
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// Extending HTML element props
type InputProps = React.ComponentProps<'input'> & {
  label: string;
  error?: string;
};

// With children as function (render props)
interface DataLoaderProps<T> {
  url: string;
  children: (data: T | null, loading: boolean) => React.ReactNode;
}
```

### Component Composition

```typescript
// Compound components
interface TabsProps {
  defaultTab: string;
  children: React.ReactNode;
}

function Tabs({ defaultTab, children }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: React.ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabs();
  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultTab="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="tab1">Content 1</Tabs.Panel>
  <Tabs.Panel value="tab2">Content 2</Tabs.Panel>
</Tabs>
```

## Hooks Best Practices

### useState

```typescript
// Simple state
const [count, setCount] = useState(0);

// Complex state - consider useReducer
const [form, setForm] = useState<FormState>({
  name: '',
  email: '',
  errors: {},
});

// Functional updates for derived state
setCount((prev) => prev + 1);
setForm((prev) => ({ ...prev, name: newName }));

// Lazy initialization for expensive defaults
const [data, setData] = useState(() => computeExpensiveDefault());
```

### useEffect

```typescript
// With cleanup
useEffect(() => {
  const subscription = subscribe(id);
  return () => subscription.unsubscribe();
}, [id]);

// Async effect pattern
useEffect(() => {
  let cancelled = false;

  async function load() {
    const data = await fetchData(id);
    if (!cancelled) {
      setData(data);
    }
  }

  load();

  return () => {
    cancelled = true;
  };
}, [id]);

// Empty dependency array - runs once
useEffect(() => {
  initializeApp();
}, []);
```

### useCallback & useMemo

```typescript
// useCallback for stable function reference
const handleClick = useCallback((id: string) => {
  onSelect(id);
}, [onSelect]);

// useMemo for expensive computations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// useMemo for stable object reference
const style = useMemo(
  () => ({ color: theme.primary, fontSize: size }),
  [theme.primary, size]
);
```

### useRef

```typescript
// DOM reference
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

// Mutable value that doesn't trigger re-render
const timerRef = useRef<NodeJS.Timeout | null>(null);

function startTimer() {
  timerRef.current = setInterval(() => {
    // ...
  }, 1000);
}

function stopTimer() {
  if (timerRef.current) {
    clearInterval(timerRef.current);
  }
}
```

### Custom Hooks

```typescript
// Reusable data fetching
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const response = await fetch(url);
        const json = await response.json();
        if (!cancelled) setData(json);
      } catch (e) {
        if (!cancelled) setError(e as Error);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}

// Debounced value
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

## Performance Optimization

### memo for Components

```typescript
// Memoize expensive components
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item) => (
        <ExpensiveItem key={item.id} item={item} />
      ))}
    </ul>
  );
});

// With custom comparison
const UserCard = memo(
  function UserCard({ user }: { user: User }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
);
```

### List Keys

```typescript
// BAD: Index as key
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// GOOD: Stable ID
{items.map((item) => (
  <Item key={item.id} data={item} />
))}
```

### Avoiding Unnecessary Renders

```typescript
// BAD: New object every render
<Child config={{ size: 'large' }} />

// GOOD: Stable reference
const config = useMemo(() => ({ size: 'large' }), []);
<Child config={config} />

// BAD: Inline function
<Button onClick={() => handleClick(id)} />

// GOOD: Stable callback
const handleButtonClick = useCallback(() => handleClick(id), [id]);
<Button onClick={handleButtonClick} />
```

## Context Usage

### Creating Context

```typescript
interface ThemeContextValue {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const value = useMemo(
    () => ({
      theme,
      toggleTheme: () => setTheme((t) => (t === 'light' ? 'dark' : 'light')),
    }),
    [theme]
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
```

### Context Best Practices

```typescript
// Split contexts to avoid unnecessary re-renders
const UserContext = createContext<User | null>(null);
const UserActionsContext = createContext<UserActions | null>(null);

function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const actions = useMemo(
    () => ({
      login: async (credentials: Credentials) => { /* ... */ },
      logout: () => setUser(null),
    }),
    []
  );

  return (
    <UserContext.Provider value={user}>
      <UserActionsContext.Provider value={actions}>
        {children}
      </UserActionsContext.Provider>
    </UserContext.Provider>
  );
}
```

## Review Checklist

### Component Design
- [ ] Props interface clearly defined
- [ ] Appropriate component size
- [ ] Composition over inheritance

### Hooks
- [ ] useEffect has correct dependencies
- [ ] useEffect has cleanup when needed
- [ ] useCallback/useMemo used appropriately
- [ ] Custom hooks for reusable logic

### Performance
- [ ] memo() for expensive components
- [ ] Stable keys in lists
- [ ] No inline objects/functions causing re-renders

### State Management
- [ ] State at appropriate level
- [ ] Context split to avoid re-renders
- [ ] Complex state uses useReducer

### Error Handling
- [ ] Error boundaries where appropriate
- [ ] Loading states handled
- [ ] Empty states handled
