# React & TypeScript Best Practices

## React Best Practices

### useEffect Usage

**DO NOT overuse useEffect.** Only use for synchronizing with external systems.

#### ❌ BAD: Using useEffect only to update state

```tsx
// Anti-pattern: useEffect only updating state based on props
const Component = ({ userId }: Props) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const foundUser = users.find(u => u.id === userId);
    setUser(foundUser);
  }, [userId]);

  return <div>{user?.name}</div>;
};
```

#### ✅ GOOD: Derive state during render

```tsx
const Component = ({ userId }: Props) => {
  const user = users.find(u => u.id === userId);
  return <div>{user?.name}</div>;
};
```

#### ✅ GOOD: Valid useEffect use cases

```tsx
// Synchronizing with external API
useEffect(() => {
  const controller = new AbortController();
  fetch('/api/data', { signal: controller.signal })
    .then(res => res.json())
    .then(setData);
  return () => controller.abort();
}, []);

// Subscribing to external event
useEffect(() => {
  const handleResize = () => setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

// Synchronizing with third-party library
useEffect(() => {
  const map = new MapLibrary('#map');
  map.setCenter(coordinates);
  return () => map.destroy();
}, [coordinates]);
```

### State Management

#### Avoid Redundant State

```tsx
// ❌ BAD
const [items, setItems] = useState(items);
const [itemCount, setItemCount] = useState(items.length); // Redundant!

// ✅ GOOD
const [items, setItems] = useState(items);
const itemCount = items.length; // Always in sync
```

#### Avoid State Mirroring Props

```tsx
// ❌ BAD
const Component = ({ initialValue }: Props) => {
  const [value, setValue] = useState(initialValue); // Won't update if prop changes!
};

// ✅ GOOD: Controlled component
const Component = ({ value, onChange }: Props) => {
  return <input value={value} onChange={e => onChange(e.target.value)} />;
};
```

### useMemo and useCallback

**Only use when necessary.** Don't premature optimize.

```tsx
// ✅ GOOD: Expensive calculation
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => expensiveCompare(a, b));
}, [items]);

// ❌ BAD: Simple calculation
const sum = useMemo(() => a + b, [a, b]); // Overkill!

// ✅ GOOD: Just calculate directly
const sum = a + b;
```

```tsx
// ✅ GOOD: Passed to memoized child component
const handleClick = useCallback(() => {
  // handle click
}, []);
return <MemoizedChild onClick={handleClick} />;

// ❌ BAD: Not passed to any memoized component
const handleClick = useCallback(() => {
  console.log('clicked');
}, []); // Unnecessary!
```

### React.memo

**Use for expensive list items or rarely changing components.**

```tsx
// ✅ GOOD: Memoize expensive list items
const ListItem = React.memo(({ item, onClick }: Props) => {
  return (
    <div onClick={() => onClick(item.id)}>
      <ExpensiveVisualization data={item} />
    </div>
  );
});

// ❌ BAD: Over-memoizing simple components
const SimpleText = React.memo(({ text }: Props) => {
  return <span>{text}</span>; // Too simple to benefit from memo
});
```

### Hooks Placement

**Don't call all hooks at the top. Split components and place hooks where needed.**

```tsx
// ❌ BAD: All hooks at the top
const Component = ({ mode }: Props) => {
  const { data: projectData } = useGetApi('/api/projects');  // Only for mode="project"
  const { data: userData } = useGetApi('/api/user-stats');    // Only for mode="user"
  // ...
};

// ✅ GOOD: Split components
const Component = ({ mode }: Props) => {
  if (mode === 'project') return <ProjectView />;
  if (mode === 'user') return <UserView />;
  return <SettingsView />;
};

const ProjectView = () => {
  const { data } = useGetApi('/api/projects'); // Only fetches when needed
  return <div>{/* ... */}</div>;
};
```

### Props Guidelines

#### Keep Props Count Low

```tsx
// ❌ BAD: Too many props
<UserCard id={...} name={...} email={...} avatar={...} role={...} ... />

// ✅ GOOD: Group related props
<UserCard
  user={user}
  actions={{ onEdit, onDelete }}
  options={{ showActions: true }}
/>
```

#### Avoid Prop Drilling

```tsx
// ❌ BAD: Passing through many levels
const Dashboard = ({ user, theme }) => <Sidebar user={user} theme={theme} />;
const Sidebar = ({ user, theme }) => <UserMenu user={user} theme={theme} />;

// ✅ GOOD: Use Context or Redux
const UserMenu = () => {
  const { user } = useAuth();
  const { theme } = useSharedTheme();
  return <div>{/* ... */}</div>;
};
```

### Lists and Keys

```tsx
// ❌ BAD
items.map((item, index) => <Item key={index} {...item} />);
items.map(item => <Item key={Math.random()} {...item} />);

// ✅ GOOD
items.map(item => <Item key={item.id} {...item} />);
```

## Conditional Rendering

### The `&&` Operator Pitfall

```tsx
// ❌ BAD: Renders "0" when count is 0
{count && <div>Count: {count}</div>}

// ✅ GOOD
{count > 0 && <div>Count: {count}</div>}
{!!count && <div>Count: {count}</div>}
{count ? <div>Count: {count}</div> : null}
```

### Nullish Coalescing (`??`)

```tsx
// ❌ BAD: || ignores 0, false, ''
const displayCount = count || 10; // If count is 0, uses 10 (wrong!)

// ✅ GOOD: ?? only checks for null/undefined
const displayCount = count ?? 10; // If count is 0, uses 0 (correct!)
```

### Multiple Conditions

```tsx
// ❌ BAD: Deeply nested ternaries
{status === 'loading' ? <Spinner /> : status === 'error' ? <Error /> : <Content />}

// ✅ GOOD: Early returns
if (status === 'loading') return <Spinner />;
if (status === 'error') return <Error />;
return <Content />;

// ✅ ALSO GOOD: Object mapping
const statusComponents = {
  loading: <Spinner />,
  error: <Error />,
  success: <Content />,
};
return statusComponents[status] || <Content />;
```

## TypeScript Best Practices

### Never Use `any` Type

```tsx
// ❌ BAD
const handleData = (data: any) => { ... };
const items: any[] = [];

// ✅ GOOD
interface User { id: string; name: string; }
const handleData = (data: User) => { ... };
const items: User[] = [];

// ✅ GOOD: Use unknown when type is truly unknown
const parseData = (data: unknown) => {
  if (typeof data === 'string') {
    return JSON.parse(data);
  }
  throw new Error('Invalid data type');
};
```

### Use Generated API Types

```tsx
import type { components } from '@generated/api.d.ts';

// ✅ GOOD
type Project = components['schemas']['Project'];

// ❌ BAD: Manual type definition
type Project = { id: string; name: string; }; // Can get out of sync!
```

### Type vs Interface

```tsx
// ✅ Use type for component props
type ButtonProps = {
  onClick: () => void;
  scheme: 'primary' | 'secondary';
};

// ✅ Use interface for extensible data models
interface User {
  id: string;
  name: string;
}

interface AdminUser extends User {
  permissions: string[];
}
```

### Type Guards

```tsx
const isUser = (value: unknown): value is User => {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
};

const processData = (data: unknown) => {
  if (isUser(data)) {
    console.log(data.email); // TypeScript knows data is User
  }
};
```

### Generics

```tsx
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string;
};

const List = <T,>({ items, renderItem, keyExtractor }: ListProps<T>) => {
  return (
    <div>
      {items.map(item => (
        <div key={keyExtractor(item)}>{renderItem(item)}</div>
      ))}
    </div>
  );
};
```

### Const Assertions

```tsx
const ROUTES = {
  HOME: '/home',
  PROFILE: '/profile',
} as const;
// Type: { readonly HOME: "/home"; readonly PROFILE: "/profile" }

const useToggle = (initial: boolean) => {
  const [value, setValue] = useState(initial);
  return [value, () => setValue(v => !v)] as const;
};
// Return type: readonly [boolean, () => void]
```

## Security Best Practices

### Never Use dangerouslySetInnerHTML

```tsx
// ❌ BAD: XSS vulnerability
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// ✅ GOOD: Use text content
<div>{userInput}</div>

// ✅ GOOD: Use markdown library
import { MarkDownText } from '@src/component/molecules/MarkDownText';
<MarkDownText text={markdown} />
```

### Validate API Responses

```tsx
// ✅ GOOD
const response = await client.GET('/api/projects');
if (response.error) {
  throw new Error('Failed to fetch');
}
return response.data;

// ❌ BAD
const response = await client.GET('/api/projects');
return response.data; // Might be undefined!
```

## Common Mistakes Checklist

### Styling
- ❌ Inline styles
- ❌ Hardcoded colors
- ❌ Missing className prop
- ❌ Using deprecated constants

### React
- ❌ Overusing useEffect
- ❌ Cascading useEffects
- ❌ Redundant state
- ❌ Index as key
- ❌ Components inside components
- ❌ Missing cleanup in useEffect

### TypeScript
- ❌ Using `any` type
- ❌ Manual API types (use generated)
- ❌ Overusing type assertions

### Security
- ❌ dangerouslySetInnerHTML
- ❌ Unvalidated user input
- ❌ Missing API error checks
